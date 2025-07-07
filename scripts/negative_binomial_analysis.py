import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings("ignore")

c2rust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=2, nrows=7, index_col='Program').fillna(0)
c2saferust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=14, nrows=7, index_col='Program').fillna(0)
human_written_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=26, nrows=7, index_col='Program').fillna(0)

c2rust_df['Translation'] = 'C2Rust'
c2saferust_df['Translation'] = 'C2SafeRust'
human_written_df['Translation'] = 'HumanWritten'

df = pd.concat([c2rust_df, c2saferust_df, human_written_df]).reset_index()

# All categories excluding meta columns.
all_categories = [col for col in df.columns if col not in ['Program', 'Translation', 'Lines of Code']]
results = []

for category in all_categories:
    try:
        data = df[['Program', 'Translation', 'Lines of Code', category]].copy()
        data.columns = ['Program', 'Translation', 'LOC', 'Warnings']

        # Skip if sum of warnings is zero.
        if data['Warnings'].sum() == 0:
            continue

        # Fit Negative Binomial regression.
        model = smf.glm(formula='Warnings ~ Translation + LOC', 
                        data=data, 
                        family=sm.families.NegativeBinomial(alpha=1)).fit()

        pvals = model.pvalues

        results.append({
            'Category': category,
            'P_C2SafeRust': pvals.get('Translation[T.C2SafeRust]', None),
            'P_HumanWritten': pvals.get('Translation[T.HumanWritten]', None),
            'P_LOC': pvals.get('LOC', None),
            'Coef_C2SafeRust': model.params.get('Translation[T.C2SafeRust]', None),
            'Coef_HumanWritten': model.params.get('Translation[T.HumanWritten]', None)
        })

    except Exception as e:
        print(f"Skipped '{category}' due to error: {e}")

# Summarize results.
results_df = pd.DataFrame(results)
results_df['Sig_C2SafeRust'] = results_df['P_C2SafeRust'] < 0.05
results_df['Sig_HumanWritten'] = results_df['P_HumanWritten'] < 0.05

print("\nNegative Binomial Regression Summary (all categories):")
print(results_df[['Category', 'P_C2SafeRust', 'Sig_C2SafeRust', 'P_HumanWritten', 'Sig_HumanWritten', 'P_LOC']].sort_values('Category'))

# results_df.to_csv("negative_binomial_category_significance.csv", index=False)
# print("\n✅ Results saved to 'negative_binomial_category_significance.csv'")  