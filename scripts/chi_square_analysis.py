import pandas as pd
from scipy.stats import chi2_contingency

# Load data clearly
c2rust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=2, nrows=7, index_col='Program').fillna(0)
c2saferust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=14, nrows=7, index_col='Program').fillna(0)
human_written_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=26, nrows=7, index_col='Program').fillna(0)

# Sum counts across programs per category
contingency_table = pd.DataFrame({
    'C2Rust': c2rust_df.sum(),
    'C2SafeRust': c2saferust_df.sum(),
    'Human-Written': human_written_df.sum()
})

threshold = 5  # categories below this count in any translation will be grouped into "Other".
low_freq_rows = contingency_table[(contingency_table < threshold).any(axis=1)]
high_freq_rows = contingency_table[(contingency_table >= threshold).all(axis=1)]


other_counts = low_freq_rows.sum()
# high_freq_rows.loc['Other'] = other_counts
print(high_freq_rows)

# Perform Chi-square Test.
chi2, p_value, dof, expected = chi2_contingency(high_freq_rows)

print("Chi-square statistic:", chi2)
print("Degrees of freedom:", dof)
print("P-value:", p_value)

# Interpretation
alpha = 0.05
if p_value < alpha:
    print("Significant difference: Warning distributions differ across translation types.")
else:
    print("No significant difference: Warning distributions are similar across translation types.")
