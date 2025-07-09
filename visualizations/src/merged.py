import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scripts.batch_runner_per_code_type import batch_runner

# Load LOC data
loc_df = pd.read_excel("loc_counts.xlsx")
loc_df.columns = [col.strip() for col in loc_df.columns]
loc_df["Code Type"] = loc_df["Code Type"].str.strip()

def normalize_counts(code_type, output_path):
    total_loc = loc_df[loc_df["Code Type"] == code_type]["Lines of Code"].sum()
    if total_loc == 0:
        raise ValueError(f"Total lines of code is zero for {code_type}. Cannot normalize warnings.")
    
    total_category_counts, total_severity_counts = batch_runner(code_type, output_path)
    
    normalized_severity_counts = {
        category: {
            severity: (count / total_loc) * 1000
            for severity, count in sev_dict.items()
        }
        for category, sev_dict in total_severity_counts.items()
    }
    return normalized_severity_counts

# Get normalized severity counts for all code types
c2rust_norm = normalize_counts("c2rust", "visualizations/outputs/c2rust")
c2saferust_norm = normalize_counts("c2saferust", "visualizations/outputs/c2saferust")
human_norm = normalize_counts("human_written", "visualizations/outputs/human_written")

# Union of all categories
all_categories = sorted(set(c2rust_norm) | set(c2saferust_norm) | set(human_norm))

# Extract severity arrays
def get_severity_array(norm_dict, severity, all_categories):
    return [norm_dict.get(cat, {}).get(severity, 0) for cat in all_categories]

severities = ['deny', 'warn', 'allow', 'none']
colors = {'deny': '#d62728', 'warn': '#ff7f0e', 'allow': '#2ca02c', 'none': '#7f7f7f'}

# Initialize base arrays for stacking
n = len(all_categories)
bar_height = 0.2
bar_spacing = bar_height * 1.5
y_pos = np.arange(n)

fig, ax = plt.subplots(figsize=(15, 10))

# Plot each severity level as stacked bars
for i, severity in enumerate(severities):
    rust_vals = get_severity_array(c2rust_norm, severity, all_categories)
    saferust_vals = get_severity_array(c2saferust_norm, severity, all_categories)
    human_vals = get_severity_array(human_norm, severity, all_categories)

    rust_cum = np.sum([get_severity_array(c2rust_norm, s, all_categories) for s in severities[:i]], axis=0)
    saferust_cum = np.sum([get_severity_array(c2saferust_norm, s, all_categories) for s in severities[:i]], axis=0)
    human_cum = np.sum([get_severity_array(human_norm, s, all_categories) for s in severities[:i]], axis=0)

    label = severity.capitalize()  # show severity in legend only once

    ax.barh(y_pos - bar_spacing, rust_vals, left=rust_cum, height=bar_height, color=colors[severity], label=label)
    ax.barh(y_pos, saferust_vals, left=saferust_cum, height=bar_height, color=colors[severity])
    ax.barh(y_pos + bar_spacing, human_vals, left=human_cum, height=bar_height, color=colors[severity])

# Total values for annotation
rust_totals = np.sum([get_severity_array(c2rust_norm, s, all_categories) for s in severities], axis=0)
saferust_totals = np.sum([get_severity_array(c2saferust_norm, s, all_categories) for s in severities], axis=0)
human_totals = np.sum([get_severity_array(human_norm, s, all_categories) for s in severities], axis=0)

# Determine axis limit
max_total = max(np.max(rust_totals), np.max(saferust_totals), np.max(human_totals))

# Annotate total values
for i in range(n):
    xpos_rust = min(rust_totals[i] * 1.05, max_total * 1.45)
    xpos_safe = min(saferust_totals[i] * 1.05, max_total * 1.45)
    xpos_human = min(human_totals[i] * 1.05, max_total * 1.45)

    ax.text(xpos_rust, y_pos[i] - bar_spacing, f"{rust_totals[i]:.2f}", va='center', fontsize=9)
    ax.text(xpos_safe, y_pos[i], f"{saferust_totals[i]:.2f}", va='center', fontsize=9)
    ax.text(xpos_human, y_pos[i] + bar_spacing, f"{human_totals[i]:.2f}", va='center', fontsize=9)

# Final formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(all_categories)
ax.set_xlabel("Warnings per 1000 LOC (log scale)")
ax.set_title("Clippy Warnings by Category and Severity\nTop: C2Rust | Middle: C2SaferRust | Bottom: Human Written")
ax.set_xscale("log")
ax.grid(axis='x', linestyle='--', alpha=0.6)
ax.legend(loc='lower right', title="Severity")
ax.set_xlim(right=max_total * 2)
plt.tight_layout()
plt.show()
