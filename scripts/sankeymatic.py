import pandas as pd

df = pd.read_excel("../clippy_lints.xlsx")

# Clean up.
df.columns = [c.strip() for c in df.columns]
df["Group"] = df["Group"].str.strip()
df["Severity"] = df["Severity"].str.strip()
df["Custom Category"] = df["Custom Category"].str.strip()

# Group → Custom Category.
group_to_custom = (
    df.groupby(["Group", "Custom Category"])
    .size()
    .reset_index(name='Count')
)
group_to_custom["Source"] = group_to_custom.apply(lambda row: f"{row['Group']} [{row['Count']}]", axis=1)
group_to_custom["Target"] = group_to_custom["Custom Category"]

# Custom Category → Severity.
custom_to_severity = (
    df.groupby(["Custom Category", "Severity"])
    .size()
    .reset_index(name='Count')
)
custom_to_severity["Source"] = custom_to_severity.apply(lambda row: f"{row['Custom Category']} [{row['Count']}]", axis=1)
custom_to_severity["Target"] = custom_to_severity["Severity"]

# Combine both parts.
sankey_df = pd.concat([
    group_to_custom[["Source", "Target"]],
    custom_to_severity[["Source", "Target"]]
], ignore_index=True)

sankey_df = sankey_df[~sankey_df["Source"].str.lower().str.contains("deprecated")]
sankey_df = sankey_df[~sankey_df["Target"].str.lower().str.contains("deprecated")]

sankey_df.to_excel("../sankey_edges.xlsx", index=False)
print("✅ Sankey edge pairs saved to 'sankey_edges.xlsx'")
