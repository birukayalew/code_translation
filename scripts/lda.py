import os
import re
import pandas as pd
from collections import defaultdict, Counter
from scripts.clippy_warning_outputs_analyzer import get_category_counts_from_file
from scripts.lint_to_category_mapper import mapper
from openpyxl.styles import Border, Side

def lda():
    base_path = "visualizations/outputs"
    all_data = defaultdict(lambda: defaultdict(Counter))
    _, _, all_categories = mapper()

    for code_type in ["c2rust", "c2saferust", "c2saferustv2","human_written"]:
        code_type_path = os.path.join(base_path, code_type)
        for filename in os.listdir(code_type_path):
            if filename.endswith(".txt"):
                parts = filename.split("_")
                program = parts[-2]
                category_counts, _, _ = get_category_counts_from_file(code_type, filename)

                for category in all_categories:
                    category_counts.setdefault(category, 0)
                all_data[code_type][program].update(category_counts)

    return all_data, all_categories


def save_to_excel(data, all_categories, output_file="warnings_per_program.xlsx"):
    loc_df = pd.read_excel("loc_counts.xlsx")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        row_offset = 0                        # where the next block should start

        for code_type in ["c2rust", "c2saferust", "c2saferustv2","human_written"]:
            program_data  = data[code_type]
            program_names = sorted(program_data.keys())

            # ---------------- Build the table ----------------
            df = pd.DataFrame(index=program_names, columns=all_categories)
            for prog in program_names:
                for cat in all_categories:
                    df.loc[prog, cat] = program_data[prog][cat]

            loc_subset = (loc_df[loc_df['Code Type'] == code_type]
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
            ws.cell(row=row_offset + 1, column=1).value = code_type.upper()

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

# Run
if __name__ == "__main__":
    data, all_categories = lda()
    save_to_excel(data, all_categories)