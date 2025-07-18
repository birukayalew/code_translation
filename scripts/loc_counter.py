import os
import pandas as pd

# Define the root directories for each code type(tool).
base_paths = {
    "c2rust": "c2saferrust/coreutils/src",
    "c2saferust": "c2saferrust/coreutils/src",
    "c2saferustv2": "translation_gym/output",
    "human_written": "coreutils/src/uu"
}

# Define the 7 target programs.
target_programs = ["cat", "head", "pwd", "split", "tail", "truncate", "uniq"]

# # Shared dependency paths (used by human-written programs).
# shared_deps = [
#     "coreutils/src/uucore",
#     "coreutils/src/uucore_procs",
#     "coreutils/src/uuhelp_parser"
# ]

# Helper function to count lines in all .rs files under a directory.
def count_rs_lines(start_path):
    total_lines = 0
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.endswith(".rs"):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    pass  # Skip files that can't be read
    return total_lines

# Precompute shared dependency LOC.
# shared_loc = sum(count_rs_lines(dep) for dep in shared_deps)

results = []

# Iterate through code types and programs.
for code_type, root_path in base_paths.items():
    for program in target_programs:
        if code_type == "c2rust":
            full_path = os.path.join(root_path, program, "rust")
        elif code_type == "c2saferust":
            full_path = os.path.join(root_path, program, "rust_WIP")
        elif code_type == "human_written":
            full_path = os.path.join(root_path, program)
        elif code_type == "c2saferustv2":
            full_path = os.path.join(root_path, program)
        else:
            continue

        loc = count_rs_lines(full_path)
        # Add shared LOC for human-written programs.
        # if code_type == "human_written":
        #     loc += shared_loc
        results.append({
            "Code Type": code_type,
            "Program": program,
            "Lines of Code": loc
        })

df = pd.DataFrame(results)

output_file = "loc_counts.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ LOC summary saved to {output_file}")