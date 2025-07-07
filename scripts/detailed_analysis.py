import re
import os
import json
from collections import Counter, defaultdict
from scripts.lint_to_category_mapper import mapper
import pandas as pd

DIR = "visualizations/outputs/"

# Regex pattern to match Clippy lint names.
lint_pattern = re.compile(r"https://rust-lang\.github\.io/rust-clippy/master/index\.html#([\w\-]+)")

# Load mappings and full category list
lint_to_custom_category, lint_to_severity, all_categories = mapper()

# Load category to lints mapping from JSON.
with open("category_to_lints_mapping.json", "r", encoding="utf-8") as f:
    lint_categories = json.load(f)

loc_df = pd.read_excel("loc_counts.xlsx")
loc_df.columns = [col.strip() for col in loc_df.columns]
loc_df["Code Type"] = loc_df["Code Type"].str.strip()

loc_totals = {
    "c2rust": loc_df[loc_df["Code Type"] == "c2rust"]["Lines of Code"].sum(),
    "c2saferust": loc_df[loc_df["Code Type"] == "c2saferust"]["Lines of Code"].sum(),
    "human_written": loc_df[loc_df["Code Type"] == "human_written"]["Lines of Code"].sum()
}

def analyze_lints(code_type, filepath, category_name):
    """Analyze and print lint statistics for a specific category."""
    path = os.path.join(DIR, code_type, filepath)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            clippy_output = f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    # Extract lint names.
    lint_names = lint_pattern.findall(clippy_output)
    lint_counts = Counter(lint_names)
    
    # Get lints for the current category.
    category_lints = lint_categories.get(category_name, [])
    if not category_lints:
        print(f"No lints found for category: {category_name}")
        return
    
    # Filter lints for the current category.
    category_summary = {lint: count for lint, count in lint_counts.items() 
                       if lint in category_lints}
    
    if not category_summary:
        return

    # Calculate normalized counts.
    total_loc = loc_totals.get(code_type, 1)
    total_category = (sum(category_summary.values()) / total_loc) * 1000
    
    print(f"\n📂 {category_name} Lints in file: {filepath} [{code_type}]")
    
    for lint, count in sorted(category_summary.items(), key=lambda x: -x[1]):
        normalized_count = (count / total_loc) * 1000
        percentage = (normalized_count / total_category) * 100 if total_category > 0 else 0
        print(f"🔸 {lint:30} | Count: {normalized_count:.3f} | {percentage:.2f}% of total")

# Analyze memory safety lints in c2saferust files.
# for filename in os.listdir(f"{DIR}/c2saferust"):
#     if filename.endswith(".txt"):
#         analyze_lints("c2saferust", filename, "Memory safety")

# # Analyze Attribute issues lints in human_written files.
# for filename in os.listdir(f"{DIR}/human_written"):
#     if filename.endswith(".txt"):
#         analyze_lints("human_written", filename, "Attribute issues")

# Analyze Documentation issues lints in c2rust files.
# for filename in os.listdir(f"{DIR}/c2rust"):
#     if filename.endswith(".txt"):
#         analyze_lints("c2rust", filename, "Documentation issues")

# Analyze Documentation issues lints in c2saferust files.
# for filename in os.listdir(f"{DIR}/c2saferust"):
#     if filename.endswith(".txt"):
#         analyze_lints("c2saferust", filename, "Documentation issues")

# # Analyze Redundant issues lints in human_written files.
# for filename in os.listdir(f"{DIR}/human_written"):
#     if filename.endswith(".txt"):
#         analyze_lints("human_written", filename, "Redundant")

# # Analyze Non-idiomatic issues lints in c2rust files.
# for filename in os.listdir(f"{DIR}/c2rust"):
#     if filename.endswith(".txt"):
#         analyze_lints("c2rust", filename, "Non-idiomatic")

# Analyze Non-idiomatic issues lints in c2rust files.
# for filename in os.listdir(f"{DIR}/c2saferust"):
#     if filename.endswith(".txt"):
#         analyze_lints("c2saferust", filename, "Non-idiomatic")

# Analyze Build configuration issues lints in human_written files.
# for filename in os.listdir(f"{DIR}/human_written"):
#     if filename.endswith(".txt"):
#         analyze_lints("human_written", filename, "Build configuration issues")

# Analyze Performance issues lints in human_written files.
for filename in os.listdir(f"{DIR}/human_written"):
    if filename.endswith(".txt"):
        analyze_lints("human_written", filename, "Performance")