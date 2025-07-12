import os
import json
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

all_categories = {"arithmetic_issues":"Arithmetic issues","attribute_issues":"Attribute issues", 
                  "compatibility_issues":"Compatibility issues","convention_violation":"Convention_violation", 
                  "documentation_issues":"Documentation_issues", "error_handling_issues":"Error handling issues",
                  "inflexible_code":"Inflexible code", "logical_issues":"Logical issues", "memory_safety":"Memory safety",
                "misleading_code":"Misleading code", "non_idiomatic":"Non-idiomatic", "non_production_code":"Non-production code",
                "performance":"Performance","readability_issues":"Readability issues","redundant":"Redundant",
                "panic_risks":"Runtime panic risks","thread_safety":"Thread safety", "type_safety":"Type safety"}

json_files = {
    "c2rust": "llm_results/c2rust_results.json",
    "c2saferust": "llm_results/c2saferust_results.json",
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
            category_totals[all_categories[category]] += 1
            

    return category_totals

# Build the full category count table.
all_category_counts = {}

for tool, path in json_files.items():
    if os.path.exists(path):
        tool_counts = extract_category_counts(path)
        all_category_counts[tool] = tool_counts

    else:
        print(f"⚠️ File not found: {path}")

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

# Visualize using grouped bar chart.
def plot_category_comparison(df):
    bar_height = 0.8  # Increased to 0.6 for testing
    padding = 2
    # Total height for each category group including padding
    group_height = bar_height * len(df.columns) + padding
    # Scale index with the full group height
    index = np.arange(len(df.index)) * group_height
    print("Index positions:", index)
    fig, ax = plt.subplots(figsize=(15, 12))  # Increased vertical size to 12

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, tool in enumerate(df.columns):
        ax.barh(
            index + i * bar_height,
            df[tool],
            height=bar_height,
            label=tool,
            color=colors[i % len(colors)]
        )

    # Center y-ticks within each group of bars
    ax.set_yticks(index + bar_height * (len(df.columns) - 1) / 2)
    ax.set_yticklabels(df.index)
    ax.set_xlabel("Warnings per 1000 LOC (log scale)")
    ax.set_ylabel("Warning Categories")
    ax.set_title("LLM-Based Warnings by Category and Tool (Normalized)")
    ax.set_xscale("log")
    ax.legend(loc="upper right")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    # Adjust y-axis limits to fully include the tallest bars
    max_bar_top = index[-1] + (len(df.columns) - 1) * bar_height
    ax.set_ylim(-bar_height, max_bar_top + padding)
    plt.tight_layout()
    plt.show()
# 🧮 Step 5: Display and plot
print(df)
plot_category_comparison(df)
