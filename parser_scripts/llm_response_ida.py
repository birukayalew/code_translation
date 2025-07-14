import os
import re
import json
import pandas as pd
from collections import defaultdict, Counter
from scripts.clippy_warning_outputs_analyzer import get_category_counts_from_file
from scripts.lint_to_category_mapper import mapper
from openpyxl.styles import Border, Side


all_categories = {"arithmetic_issues":"Arithmetic issues","attribute_issues":"Attribute issues", 
                  "compatibility_issues":"Compatibility issues","convention_violation":"Convention violation", 
                  "documentation_issues":"Documentation issues", "error_handling_issues":"Error handling issues",
                  "inflexible_code":"Inflexible code", "logical_issues":"Logical issues", "memory_safety":"Memory safety",
                "misleading_code":"Misleading code", "non_idiomatic":"Non-idiomatic", "non_production_code":"Non-production code",
                "performance":"Performance","readability_issues":"Readability issues","redundant":"Redundant",
                "panic_risks":"Runtime panic risks","thread_safety":"Thread safety", "type_safety":"Type safety"}


_, _, _corresponding_categories = mapper()
_corresponding_categories.remove("Build configuration issues")
json_files = {
    "c2rust": "llm_results/c2rust_results.json",
    "c2saferrust": "llm_results/c2saferrust_results.json",
    "c2saferrustv2": "llm_results/translation_gym_results.json",
    "human_written": "llm_results/human_written_results.json"
}

def data():
    all_data = defaultdict(lambda: defaultdict(Counter))

    for tool  in ["c2rust", "c2saferrust", "c2saferrustv2", "human_written"]:
        tool_path = json_files[tool]
        with open(tool_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for program, program_chunks in data.items():
            category_counts = defaultdict(int)
            for entry in program_chunks:
                category = entry["category"]
                if category in all_categories:
                    category_counts[all_categories[category]] += 1
                else:
                    print(f"Category not found: {category}")
            all_data[tool][program].update(category_counts)

    return all_data


def save_to_excel(data, all_categories, output_file="llm_warnings_per_program.xlsx"):
    loc_df = pd.read_excel("loc_counts.xlsx")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        row_offset = 0                        # where the next block should start

        for tool in ["c2rust", "c2saferrust", "c2saferrustv2", "human_written"]:
            program_data  = data[tool]
            program_names = sorted(program_data.keys())

            # ---------------- Build the table ----------------
            df = pd.DataFrame(index=program_names, columns=all_categories)
            for prog in program_names:
                for cat in all_categories:
                    df.loc[prog, cat] = program_data[prog][cat]

            loc_subset = (loc_df[loc_df['Code Type'] == tool]
                          .set_index('Program')['Lines of Code'])
            df = df.join(loc_subset, how='left')
            df = df[['Lines of Code', *all_categories]]   # LOC first

            # ---------------- Write to Excel ----------------
            header_row  = row_offset + 2                  # leave one row for title
            first_data  = header_row + 1

            df.to_excel(writer,
                        sheet_name="Summary",
                        startrow=header_row,
                        startcol=0,
                        index_label="Program")            # <<<  Program column label

            ws = writer.sheets["Summary"]

            # Put the code-type title above the table
            ws.cell(row=row_offset + 1, column=1).value = tool.upper()

            # Remove borders from the data cells
            no_border = Border(left=Side(border_style=None),
                               right=Side(border_style=None),
                               top=Side(border_style=None),
                               bottom=Side(border_style=None))

            last_data  = first_data + len(program_names) - 1
            last_col   = len(all_categories) + 2          # index + LOC + categories

            for row in ws.iter_rows(min_row=first_data,
                                    max_row=last_data,
                                    min_col=1,
                                    max_col=last_col):
                for cell in row:
                    cell.border = no_border

            # Advance row_offset for the next table (+1 title, +1 header,
            # +len(data) rows, +3 blank lines)
            row_offset += len(program_names) + 5

    print(f"✅ Saved clean Excel file to '{output_file}'")

if __name__ == "__main__":
    all_data = data()
    print(all_data)
    save_to_excel(all_data, _corresponding_categories)