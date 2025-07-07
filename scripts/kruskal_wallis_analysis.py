import pandas as pd
from scipy.stats import kruskal

c2rust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=2, nrows=7, index_col='Program').fillna(0)
c2saferust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=14, nrows=7, index_col='Program').fillna(0)
human_written_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=26, nrows=7, index_col='Program').fillna(0)

# Extract LOC and normalize warning counts per 1000 LOC.
def normalize_df(df):
    loc = df['Lines of Code']
    normalized = df.drop(columns=['Lines of Code']).div(loc, axis=0) * 1000
    return normalized

c2rust_norm = normalize_df(c2rust_df)
c2saferust_norm = normalize_df(c2saferust_df)
human_written_norm = normalize_df(human_written_df)

# Conduct Kruskal-Wallis test per category.
categories = c2rust_norm.columns
results = []

for category in categories:
    data1 = c2rust_norm[category]
    data2 = c2saferust_norm[category]
    data3 = human_written_norm[category]

    # Skip categories with identical values across groups.
    if (data1.nunique() == 1 and data2.nunique() == 1 and data3.nunique() == 1 and
        data1.iloc[0] == data2.iloc[0] == data3.iloc[0]):
        print(f"Skipped '{category}' (identical values across all groups)")
        continue
    
    stat, p = kruskal(data1, data2, data3)
    results.append((category, stat, p))

# Summarize results.
results_df = pd.DataFrame(results, columns=['Category', 'Kruskal Statistic', 'P-Value'])
results_df['Significant (α=0.05)'] = results_df['P-Value'] < 0.05

print("Kruskal-Wallis Test Results (normalized warnings per 1000 LOC):")
print(results_df.sort_values('P-Value'))

# Interpretation.
sig_categories = results_df[results_df['Significant (α=0.05)']]

if not sig_categories.empty:
    print("\nCategories with significant differences:")
    print(sig_categories[['Category', 'P-Value']])
else:
    print("\nNo categories showed significant differences.")
