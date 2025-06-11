import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from  scripts.batch_runner_per_code_type import batch_runner

# Uncomment this to normalize.

# loc_df = pd.read_excel("loc_counts.xlsx")
# loc_df.columns = [col.strip() for col in loc_df.columns]
# loc_df["Code Type"] = loc_df["Code Type"].str.strip()

# target_code_type = "c2saferust"
# total_loc = loc_df[loc_df["Code Type"] == target_code_type]["Lines of Code"].sum()

# if total_loc == 0:
#     raise ValueError("Total lines of code is zero. Cannot normalize warnings.")


total_category_counts, total_severity_counts = batch_runner("c2saferust", "visualizations/outputs/c2saferust")

# normalized_category_counts = {
#     category: (count / total_loc) * 1000
#     for category, count in total_category_counts.items()
# }

# normalized_severity_counts = {
#     category: {
#         severity: (count / total_loc) * 1000
#         for severity, count in sev_dict.items()
#     }
#     for category, sev_dict in total_severity_counts.items()
# }


# Sort categories by total count (descending)
categories = sorted(total_category_counts, key=total_category_counts.get, reverse=False)

# Extract severity counts (fill in missing severities as 0)
deny_vals = [total_severity_counts[cat].get('deny', 0) for cat in categories]
warn_vals = [total_severity_counts[cat].get('warn', 0) for cat in categories]
allow_vals = [total_severity_counts[cat].get('allow', 0) for cat in categories]
none_vals = [total_severity_counts[cat].get('none', 0) for cat in categories]

# Convert to numpy arrays for stacking
deny_arr = np.array(deny_vals)
warn_arr = np.array(warn_vals)
allow_arr = np.array(allow_vals)
none_arr = np.array(none_vals)

warn_cum = deny_arr + warn_arr
total_arr = deny_arr + warn_arr + allow_arr + none_arr

# Plot
plt.figure(figsize=(12, 6))
y_pos = np.arange(len(categories))

# Stacked horizontal bars
plt.barh(y_pos, deny_arr, color='#d62728', label='deny')   # red
plt.barh(y_pos, warn_arr, left=deny_arr, color='#ff7f0e', label='warn')  # orange
plt.barh(y_pos, allow_arr, left=warn_cum, color='#2ca02c', label='allow')  # green
plt.barh(y_pos, none_arr, left=warn_cum + allow_arr, color='#7f7f7f', label='none')  # gray



# Log scale
plt.xscale("log")

# Labels and formatting
plt.yticks(y_pos, categories)
plt.xlabel("Warnings count(log scale)")
plt.title("Clippy Warnings by Custom Category and Severity (C2SaferRust)")
plt.legend(loc='lower right')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()

# Annotate total count
for i, total in enumerate(total_arr):
    xpos = min(total * 1.05, max(total_arr) * 1.45)  # prevent overflow beyond axis limit
    plt.text(xpos, i, str(total), va='center', fontsize=9)
x_max = max(total_arr)
plt.xlim(right=x_max * 2)
    # plt.text(total * 1.05, i, str(total), va='center', fontsize=9)


plt.show()
