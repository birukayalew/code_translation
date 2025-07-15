import pandas as pd
from scipy.stats import mannwhitneyu

# Load and normalize data.
def load_and_normalize(skiprows):
    df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=skiprows, nrows=7, index_col='Program').fillna(0)
    loc = df['Lines of Code']
    normalized = df.drop(columns=['Lines of Code']).div(loc, axis=0) * 1000
    return normalized

c2rust_norm = load_and_normalize(2)
c2saferust_norm = load_and_normalize(14)
c2saferustv2_norm = load_and_normalize(26)
human_written_norm = load_and_normalize(38)

# Perform pairwise tests for each category.
results = []
categories = c2rust_norm.columns

for category in categories:
    data_c2rust = c2rust_norm[category]
    data_c2safe = c2saferust_norm[category]
    data_c2safev2 = c2saferustv2_norm[category]
    data_human = human_written_norm[category]

    # Mann-Whitney U tests.
    pairs = [
        ('C2Rust', 'C2SafeRust', data_c2rust, data_c2safe),
        ('C2Rust', 'HumanWritten', data_c2rust, data_human),
        ('C2Rust', 'C2SafeRustV2', data_c2rust, data_c2safev2),
        ('C2SafeRust', 'HumanWritten', data_c2safe, data_human),
        ('C2SafeRust', 'C2SafeRustV2', data_c2safe, data_c2safev2),
        ('C2SafeRustV2', 'HumanWritten', data_c2safev2, data_human),
    ]

    for grp1, grp2, d1, d2 in pairs:
        if d1.equals(d2):
            continue  # Skip identical data.
        u_stat, p_val = mannwhitneyu(d1, d2, alternative='two-sided')
        results.append({
            'Category': category,
            'Group1': grp1,
            'Group2': grp2,
            'U-Statistic': u_stat,
            'P-Value': p_val,
            'Significant (α=0.05)': p_val < 0.05
        })

# Summarize and save results.
results_df = pd.DataFrame(results)
print("\nPairwise Mann-Whitney U Test Results (normalized warnings per 1000 LOC):")
print(results_df.sort_values('P-Value'))

# results_df.to_csv("pairwise_mannwhitney_results.csv", index=False)
# print("\nResults saved to 'pairwise_mannwhitney_results.csv'")
