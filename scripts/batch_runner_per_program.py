import os
from collections import defaultdict, Counter
from scripts.clippy_warning_outputs_analyzer import get_category_counts_from_file

def batch_runner_per_program():
    base_path = "visualizations/outputs"
    all_data = defaultdict(lambda: defaultdict(Counter))

    for code_type in ["c2rust", "c2saferust", "human_written"]:
        code_type_path = os.path.join(base_path, code_type)

        for filename in os.listdir(code_type_path):
            if filename.endswith(".txt"):
                parts = filename.split("_")
                program = parts[-2]
                category_counts, _, all_categories= get_category_counts_from_file(code_type, filename)
                # Make sure all categories are represented with 0 if missing.
                for category in all_categories:
                    category_counts.setdefault(category, 0)
                all_data[program][code_type].update(category_counts)

    return all_data
