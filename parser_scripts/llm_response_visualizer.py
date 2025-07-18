import os
import json
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

all_categories = {"arithmetic_issues":"Arithmetic issues","attribute_issues":"Attribute issues", 
                  "compatibility_issues":"Compatibility issues","convention_violation":"Convention violation", 
                  "documentation_issues":"Documentation issues", "error_handling_issues":"Error handling issues",
                  "inflexible_code":"Inflexible code", "logical_issues":"Logical issues", "memory_safety":"Memory safety",
                "misleading_code":"Misleading code", "non_idiomatic":"Non-idiomatic", "non_production_code":"Non-production code",
                "performance":"Performance","readability_issues":"Readability issues","redundant":"Redundant",
                "panic_risks":"Runtime panic risks","thread_safety":"Thread safety", "type_safety":"Type safety"}

json_files = {  
    "c2rust": "llm_results/c2rust_results.json",
    "c2saferust": "llm_results/c2saferrust_results.json",
    "c2saferustv2": "llm_results/translation_gym_results.json",
    "human_written": "llm_results/human_written_results.json"
}



# Load LOC data
loc_df = pd.read_excel("loc_counts.xlsx")
loc_df.columns = [col.strip() for col in loc_df.columns]
loc_df["Code Type"] = loc_df["Code Type"].str.strip()
loc_map = dict(zip(loc_df["Code Type"], loc_df["Lines of Code"]))

def total_loc(tool):
    total = loc_df[loc_df["Code Type"] == tool]["Lines of Code"].sum()
    return total

# Function to extract category counts per tool.
def extract_category_counts(filepath):
    category_totals = defaultdict(int)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for program_chunks in data.values():
        for entry in program_chunks:
            category = entry["category"]
            if category in all_categories:
                category_totals[all_categories[category]] += 1
            else:
                print(f"Category not found: {category}")
            

    return category_totals

# Build the full category count table.
all_category_counts = {}

for tool, path in json_files.items():
    if os.path.exists(path):
        tool_counts = extract_category_counts(path)
        # print(tool, tool_counts)
        all_category_counts[tool] = tool_counts

    else:
        print(f"⚠️ File not found: {path}")

print(all_category_counts)

# Normalize.
for tool, categories in all_category_counts.items():
    for cat in categories:
        count = all_category_counts[tool][cat]
        all_category_counts[tool][cat] = (count / total_loc(tool)) * 1000



category_labels = list(all_categories.values())

# Create DataFrame with category values as index.
df = pd.DataFrame(index=category_labels)

for tool, counts in all_category_counts.items():
    df[tool] = [counts.get(cat, 0) for cat in category_labels]

df = df.fillna(0)
df = df[::-1]
# df = df[df.columns[::-1]]

# Visualize using grouped bar chart.
# ... [previous code remains the same until the plot_category_comparison function] ...

def plot_category_comparison(df, linter):
    bar_height = 4
    padding = 4
    group_height = bar_height * len(df.columns) + padding
    index = np.arange(len(df.index)) * group_height
    fig, ax = plt.subplots(figsize=(15, 10))

    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']

    # Create a copy for plotting (replace 0 with a small value for log scale)
    plot_df = df.replace(0, 0.001)

    for i, tool in enumerate(plot_df.columns):
        # Plot all bars (including zeros as small values)
        bars = ax.barh(
            index + i * bar_height,
            plot_df[tool],
            height=bar_height,
            color=colors[i % len(colors)],
            label=tool
        )
        
        # Modify zero bars to appear as faint lines
        for j, bar in enumerate(bars):
            if df[tool].iloc[j] == 0:  # Check original zero values.
                bar.set_color('lightgray')
                bar.set_edgecolor('dimgray')
                bar.set_alpha(0.7)
                bar.set_hatch('//////')  # Diagonal hatch pattern.
                bar.set_linewidth(0.5)

    # Add legend entry for zero values.
    zero_patch = plt.Rectangle(
        (0,0), 1, 1, 
        fc='lightgray', 
        ec='dimgray',
        alpha=0.7,
        hatch='//////',
        linewidth=0.5
    )
    handles, labels = ax.get_legend_handles_labels()
    handles.append(zero_patch)
    labels.append("Zero (no warnings)")

    # Configure plot appearance
    ax.set_yticks(index + bar_height * (len(df.columns) - 1) / 2)
    ax.set_yticklabels(df.index)
    ax.set_xlabel("Warnings per 1000 LOC (log scale)")
    ax.set_ylabel("Warning Categories")
    ax.set_title(f"{linter}-Based Warnings by Category and Tool (Normalized)")
    ax.set_xscale("log")
    ax.set_xlim(0.0005, df.max().max() * 10)  # Adjust scale to show faint lines
    ax.legend(handles, labels, loc="lower right")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    max_bar_top = index[-1] + (len(df.columns) - 1) * bar_height
    ax.set_ylim(-bar_height, max_bar_top + padding)
    
    plt.tight_layout()
    plt.show()


print(df)
plot_category_comparison(df, "LLM")
