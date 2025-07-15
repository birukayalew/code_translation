import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare
from scikit_posthocs import posthoc_nemenyi_friedman

# === File and block configuration ===
excel_file = "llm_warnings_per_program.xlsx"
sheet_name = "Summary"

tool_blocks = {
    "C2RUST": 3,
    "C2SaferRust": 15,
    "C2SaferRustV2": 27,
    "Human_Written": 39,
}

# === Extract normalized warnings per 1000 LOC ===
def extract_normalized_totals(start_row):
    df = pd.read_excel(
        excel_file,
        sheet_name=sheet_name,
        skiprows=start_row - 1,
        nrows=7
    )
    df["total_warnings"] = df.iloc[:, 2:].sum(axis=1)
    df["normalized_warnings"] = (df["total_warnings"] / df["Lines of Code"]) * 1000
    return df["normalized_warnings"].values

# === Load program names from first block ===
programs = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2, nrows=7)["Program"]
results_df = pd.DataFrame({"Program": programs})

# === Add normalized totals for each tool ===
for tool, start_row in tool_blocks.items():
    results_df[tool] = extract_normalized_totals(start_row)

# === Friedman Test ===
stat, p_value = friedmanchisquare(
    results_df["C2RUST"],
    results_df["C2SaferRust"],
    results_df["C2SaferRustV2"],
    results_df["Human_Written"]
)

print("\n=== Normalized Warning Counts per 1K LOC ===")
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
