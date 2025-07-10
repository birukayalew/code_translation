import os
import json
from parser_scripts.parser import extract_chunked_code

# Base directory where programs are located.
base_dir = "c2saferrust/coreutils/src"

# List of 7 programs.
programs = ["cat", "head", "pwd", "split", "tail", "truncate", "uniq"]

# Output dictionary.
program_chunks = {}

# Traverse each program.
for program in programs:
    print(f"Processing {program}...")
    rust_src_path = os.path.join(base_dir, program, "rust")

    program_chunks[program] = []

    # Walk the rust/ folder and find .rs files.
    for root, _, files in os.walk(rust_src_path):
        for file in files:
            if file.endswith(".rs"):
                file_path = os.path.join(root, file)
                print(f"Found {file_path}")

                # Extract chunks from each file.
                try:
                    chunks = extract_chunked_code(file_path, max_lines=500)
                    program_chunks[program].extend(chunks)
                except Exception as e:
                    print(f"Failed to parse {file_path}: {e}")

# Save all chunks to a single output file.
output_path = "parsed_chunks/c2rust_chunks.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(program_chunks, f, indent=2)

print(f"\n✅ All done. Chunked data saved to {output_path}")
