import pandas as pd
import json
from collections import defaultdict
from scripts.merge_categories import merge_categories


df = pd.read_excel("clippy_lints.xlsx")

# Clean up whitespace.
df.columns = [col.strip() for col in df.columns]
df["Lint Name"] = df["Lint Name"].str.strip()
df["Custom Category"] = df["Custom Category"].str.strip()

df["Merged Category"] = merge_categories()


# Build category → list of lints mapping.
category_to_lints = defaultdict(list)
for _, row in df.iterrows():
    cat = row["Merged Category"]
    lint = row["Lint Name"]
    if cat and "deprecated" not in cat.lower():
        category_to_lints[cat].append(lint)

# # ✅ Option 1: Write to TXT
# with open("category_lints.txt", "w", encoding="utf-8") as f:
#     for category, lints in sorted(category_to_lints.items()):
#         f.write(f"{category} ({len(lints)} lints):\n")
#         for lint in sorted(lints):
#             f.write(f"  - {lint}\n")
#         f.write("\n")

# ✅ Option 2: Write to JSON
with open("category_to_lints_mapping.json", "w", encoding="utf-8") as f:
    json.dump(category_to_lints, f, indent=2)
print("✅ Category to lint mapped and exported to category_to_lints_mapping.json")

