import pandas as pd

lint_excel_path = "clippy_lints.xlsx"
custom_excel_path = "clippy_custom_categories.xlsx"
output_excel_path = "clippy_lints.xlsx"  

df_main = pd.read_excel(lint_excel_path)

# Normalize lint names for lookup.
df_main["__lint_key"] = df_main["Lint Name"].str.strip().str.lower()

# Ensure Custom Category column exists.
if "Custom Category" not in df_main.columns:
    df_main["Custom Category"] = None

# Load all sheets from the custom workbook.
custom_sheets = pd.read_excel(custom_excel_path, sheet_name=None)

# Process each sheet.
for sheet_name, df_sheet in custom_sheets.items():
    df_sheet.columns = [col.strip().lower() for col in df_sheet.columns]

    lint_col = next((c for c in df_sheet.columns if "lint name" in c), None)
    category_col = next((c for c in df_sheet.columns if "custom category" in c), None)

    if not lint_col or not category_col:
        continue  # Skip sheet if required columns not found.

    for _, row in df_sheet.iterrows():
        lint_name = str(row[lint_col]).strip().lower()
        custom_category = row[category_col]

        # Find and update the matching row in df_main.
        mask = df_main["__lint_key"] == lint_name
        df_main.loc[mask, "Custom Category"] = custom_category

# Drop helper key.
df_main.drop(columns="__lint_key", inplace=True)

# Add additional lints at the end - from differnet versions of clippy.
additional_lints = [
    {
        "Lint Name": "logic_bug",
        "Group": "correctness",
        "Severity": "deny",
        "Custom Category": "Logical issues"
    },
    {
        "Lint Name": "let_underscore_drop",
        "Group": "pedantic",
        "Severity": "allow",
        "Custom Category": "Logical issues"
    },
    {
        "Lint Name": "drop_copy",
        "Group": "correctness",
        "Severity": "deny",
        "Custom Category": "Redundant"
    },
]

# Create DataFrame for additional lints and append to main DataFrame.
df_additional = pd.DataFrame(additional_lints)
df_main = pd.concat([df_main, df_additional], ignore_index=True)

# Save updated workbook.
df_main.to_excel(output_excel_path, index=False)
print(f"✅ All custom categories updated and saved to '{output_excel_path}'")
