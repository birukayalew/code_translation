import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scripts.batch_runner_per_program import batch_runner_per_program

# Load and preprocess data
data = batch_runner_per_program()

records = []
for program, code_types in data.items():
    for code_type, category_counts in code_types.items():
        for category, count in category_counts.items():
            records.append({
                "Program": program,
                "Code Type": code_type,
                "Custom Category": category,
                "Count": count
            })

df = pd.DataFrame(records)
loc_df = pd.read_excel("loc_counts.xlsx")

# Ensure all combinations are included.
all_categories = sorted(df["Custom Category"].unique())
all_programs = sorted(df["Program"].unique())
all_code_types = ["c2rust", "c2saferust", "human_written"]

df = df.set_index(["Program", "Code Type", "Custom Category"]).reindex(
    pd.MultiIndex.from_product([all_programs, all_code_types, all_categories],
    names=["Program", "Code Type", "Custom Category"]),
    fill_value=0
).reset_index()
# print(df)

# Step 4: Merge in LOC info and normalize.
df = df.merge(loc_df, how="left", on=["Program", "Code Type"])
df["Lines of Code"] = df["Lines of Code"].fillna(1)  # avoid division by 0.
df["Normalized Count"] = ((df["Count"] / df["Lines of Code"]) * 1000).round()  # rounded to nearest int.


# Plot one figure per program.
for program in all_programs:
    subset = df[df["Program"] == program]

    plt.figure(figsize=(10, 12))
    sns.barplot(
        data=subset,
        x="Normalized Count", y="Custom Category", hue="Code Type",
        order=all_categories, hue_order=all_code_types
    )
    plt.title(f"{program} – Normalized Clippy Warnings (per 1,000 LOC)")
    plt.xlabel("Warnings per 1,000 LOC (log scale)")
    plt.ylabel("Custom Category")
    plt.xscale("log")
    plt.legend(title="Tool", loc="lower right")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()