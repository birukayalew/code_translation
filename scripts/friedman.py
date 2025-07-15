import pandas as pd
from scipy.stats import friedmanchisquare
from scikit_posthocs import posthoc_nemenyi_friedman


excel_file = "llm_warnings_per_program.xlsx"
sheet_name = "Summary"

# Define where each block starts.
tool_blocks = {
    "C2RUST": 3,
    "C2SaferRust": 15,
    "C2SaferRustV2": 27,
    "Human_Written": 39,
}

# Function to extract total warnings for a given tool block.
def extract_totals_from_block(start_row):
    df = pd.read_excel(
        excel_file,
        sheet_name=sheet_name,
        skiprows=start_row - 1,
        nrows=7
    )
    df["total_warnings"] = df.iloc[:, 2:].sum(axis=1)
    df["normalized_warnings"] = (df["total_warnings"] / df["Lines of Code"]) * 1000
    return df["normalized_warnings"].values

# Start with the program names from the first block
programs = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2, nrows=7)["Program"]
results_df = pd.DataFrame({"Program": programs})

# Fill in total warning counts for each tool
for tool, start_row in tool_blocks.items():
    results_df[tool] = extract_totals_from_block(start_row)


# Run Friedman test
stat, p_value = friedmanchisquare(
    results_df["C2RUST"],
    results_df["C2SaferRust"],
    results_df["C2SaferRustV2"],
    results_df["Human_Written"]
)

# Output results
print("=== Total Warnings Per Program ===")
print(results_df)
print("\n=== Friedman Test ===")
print(f"Test Statistic: {stat:.3f}")
print(f"P-value: {p_value:.6f}")

if p_value < 0.05:
    print("=> Significant difference found between tools (p < 0.05)")
else:
    print("=> No significant difference found between tools")


# === Nemenyi Post-Hoc Test ===
print("\n=== Nemenyi Post-Hoc Test ===")
data_matrix = results_df[["C2RUST", "C2SaferRust", "C2SaferRustV2", "Human_Written"]].to_numpy()
nemenyi = posthoc_nemenyi_friedman(data_matrix)
nemenyi.columns = ["C2RUST", "C2SaferRust", "C2SaferRustV2", "Human_Written"]
nemenyi.index = ["C2RUST", "C2SaferRust", "C2SaferRustV2", "Human_Written"]
print(nemenyi)