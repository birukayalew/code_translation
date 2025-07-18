import pandas as pd
from scripts.batch_runner_per_code_type import batch_runner
import matplotlib.pyplot as plt
import numpy as np

# Load LOC data
loc_df = pd.read_excel("loc_counts.xlsx")
loc_df.columns = [col.strip() for col in loc_df.columns]
loc_df["Code Type"] = loc_df["Code Type"].str.strip()

def normalize_severity_counts(code_type, output_path):
    total_loc = loc_df[loc_df["Code Type"] == code_type]["Lines of Code"].sum()
    if total_loc == 0:
        raise ValueError(f"Total lines of code is zero for {code_type}. Cannot normalize warnings.")

    _, total_severity_counts = batch_runner(code_type, output_path)

    # Aggregate severity totals across all categories.
    severity_totals = {}
    for category_counts in total_severity_counts.values():
        for severity, count in category_counts.items():
            severity_totals[severity] = severity_totals.get(severity, 0) + count

    # Normalize per 1000 LOC.
    normalized = {
        severity: (count / total_loc) * 1000
        for severity, count in severity_totals.items()
    }

    return normalized

# Build the severity vs tool DataFrame.
tools_list = ["c2rust", "c2saferust", "c2saferustv2", "human_written"]
all_severities = ['deny', 'warn', 'allow']

severity_data = {}

for tool in tools_list:
    severity_counts = normalize_severity_counts(tool, f"visualizations/outputs/{tool}")
    severity_data[tool] = [severity_counts.get(sev, 0) for sev in all_severities]

df_severity = pd.DataFrame(severity_data, index=all_severities).T  
df_severity.index.name = "Tool"
df_severity.columns.name = "Severity"


# Plotting setup
severity_labels = df_severity.columns.tolist()
tool_labels = df_severity.index.tolist()
bar_width = 0.2
x = np.arange(len(tool_labels))

fig, ax = plt.subplots(figsize=(10, 6))

# Color mapping for severities
colors = {'deny': '#d62728', 'warn': '#ff7f0e', 'allow': '#2ca02c'}

# Plot each severity as a grouped bar
for i, severity in enumerate(severity_labels):
    values = df_severity[severity].values
    ax.bar(x + i * bar_width, values, width=bar_width, label=severity.capitalize(), color=colors[severity])

# Labeling and aesthetics
ax.set_xlabel("Tool")
ax.set_ylabel("Warnings per 1000 LOC")
ax.set_title("Normalized Clippy Warning Severities by Tool")
ax.set_xticks(x + bar_width)
ax.set_xticklabels(tool_labels)
ax.legend(title="Severity")
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print(df_severity)