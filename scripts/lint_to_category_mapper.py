import pandas as pd
from scripts.merge_categories import merge_categories

df = pd.read_excel("clippy_lints.xlsx")

# Clean up whitespace (optional but helpful)
df.columns = [col.strip() for col in df.columns]
df["Lint Name"] = df["Lint Name"].str.strip()
df["Custom Category"] = df["Custom Category"].str.strip()
df["Severity"] = df["Severity"].str.strip()

merged_df = merge_categories()

def mapper():

    lint_to_custom_category = dict(zip(df["Lint Name"], merged_df))
    lint_to_severity = dict(zip(df["Lint Name"], df["Severity"]))
    all_categories = sorted(
        cat for cat in set(merged_df)
        if cat and "deprecated" not in cat.lower()
    )
    return lint_to_custom_category, lint_to_severity, all_categories