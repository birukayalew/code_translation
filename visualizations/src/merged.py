import pandas as pd
from scripts.batch_runner_per_code_type import batch_runner
from parser_scripts.llm_response_visualizer import plot_category_comparison

# Load LOC data
loc_df = pd.read_excel("loc_counts.xlsx")
loc_df.columns = [col.strip() for col in loc_df.columns]
loc_df["Code Type"] = loc_df["Code Type"].str.strip()

def normalize_category_counts(code_type, output_path):
    total_loc = loc_df[loc_df["Code Type"] == code_type]["Lines of Code"].sum()
    if total_loc == 0:
        raise ValueError(f"Total lines of code is zero for {code_type}. Cannot normalize warnings.")

    total_category_counts, _ = batch_runner(code_type, output_path)

    normalized = {
        category: (count / total_loc) * 1000
        for category, count in total_category_counts.items()
    }
    return normalized

# Get normalized counts
norm_data = {
    "c2rust": normalize_category_counts("c2rust", "visualizations/outputs/c2rust"),
    "c2saferust": normalize_category_counts("c2saferust", "visualizations/outputs/c2saferust"),
    "c2saferustv2": normalize_category_counts("c2saferustv2", "visualizations/outputs/c2saferustv2"),
    "human_written": normalize_category_counts("human_written", "visualizations/outputs/human_written"),
}

# Build combined DataFrame
all_categories = sorted(set().union(*[d.keys() for d in norm_data.values()]))
df = pd.DataFrame(index=all_categories)

for code_type, data in norm_data.items():
    df[code_type] = [data.get(cat, 0) for cat in df.index]
# df= df[::-1]
print(df)
plot_category_comparison(df, "Clippy")