import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

c2rust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=2, nrows=7, index_col='Program').fillna(0)
c2saferust_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=14, nrows=7, index_col='Program').fillna(0)
human_written_df = pd.read_excel('warnings_per_program.xlsx', sheet_name='Summary', skiprows=26, nrows=7, index_col='Program').fillna(0)

# Label translation types.
c2rust_df['Translation'] = 'C2Rust'
c2saferust_df['Translation'] = 'C2SafeRust'
human_written_df['Translation'] = 'HumanWritten'

# Combine data.
df = pd.concat([c2rust_df, c2saferust_df, human_written_df]).reset_index()

# Get all warning categories (exclude Program, Translation, and LOC).
all_categories = [col for col in df.columns if col not in ['Program', 'Translation', 'Lines of Code']]
results = []

# Run Poisson regression for each category.
for category in all_categories:
    try:
        subset = df[['Program', 'Translation', 'Lines of Code', category]].copy()
        subset.columns = ['Program', 'Translation', 'LOC', 'Warnings']

        # Skip if all warnings are zero.
        if subset['Warnings'].sum() == 0:
            continue

        model = smf.glm(formula='Warnings ~ Translation + LOC', data=subset, family=sm.families.Poisson()).fit()
        pvalues = model.pvalues

        results.append({
            'Category': category,
            'P_C2SafeRust': pvalues.get('Translation[T.C2SafeRust]', None),
            'P_HumanWritten': pvalues.get('Translation[T.HumanWritten]', None),
            'P_LOC': pvalues.get('LOC', None)
        })

    except Exception as e:
        print(f"Skipped category '{category}' due to error: {e}")

results_df = pd.DataFrame(results)
results_df['Significant_C2SafeRust'] = results_df['P_C2SafeRust'] < 0.05
results_df['Significant_HumanWritten'] = results_df['P_HumanWritten'] < 0.05

print("\nPoisson Regression Summary (per category):")
print(results_df.sort_values(['Significant_C2SafeRust', 'Significant_HumanWritten'], ascending=False))

results_df.to_csv("poisson_category_significance.csv", index=False)
print("\n Results saved to 'poisson_category_significance.csv'")
