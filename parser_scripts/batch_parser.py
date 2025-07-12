import os
import json
from parser_scripts.parser import extract_chunked_code

# List of 7 programs.
programs = ["cat", "head", "pwd", "split", "tail", "truncate", "uniq"]

# Base directories where programs are located.
sources = [
    {
        "label": "c2rust",
        "base_dir": "c2saferrust/coreutils/src",
        "subfolder": "rust",
    },
    {
        "label": "c2saferrust",
        "base_dir": "c2saferrust/coreutils/src",
        "subfolder": "rust_WIP",
    },
    {
        "label": "translation_gym",
        "base_dir": "translation_gym/output",
        "subfolder": "",  # Each program is directly under base_dir.
    },
    {
        "label": "human_written",
        "base_dir": "coreutils/src/uu",
        "subfolder": "",
        # "shared_deps": [  # Source-specific dependencies.
        #     "coreutils/src/uucore",
        #     "coreutils/src/uucore_procs",
        #     "coreutils/src/uuhelp_parser"
        # ]
    },
]

def parse_rs_files(directory):
    chunks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".rs"):
                continue
                
            file_path = os.path.join(root, file)
            try:
                file_chunks = extract_chunked_code(file_path, max_lines=300)
                for chunk in  file_chunks:
                    chunks.append({
                        "chunk": chunk,
                        "file_name": file_path
                    })
                print(f"Parsed {file_path}")
            except Exception as e:
                print(f"Failed to parse {file_path}: {e}")
    return chunks

def main():
    for source in sources:
        label = source["label"]
        base_dir = source["base_dir"]
        subfolder = source["subfolder"]
        print(f"\nStarting extraction from {label}...")

        source_chunks = {}

        for program in programs:
            print(f"Processing {program}...")

            # Construct the program path.
            if subfolder:
                program_path = os.path.join(base_dir, program, subfolder)
            else:
                program_path = os.path.join(base_dir, program)

            source_chunks[program] = []

            source_chunks[program].extend(parse_rs_files(program_path))

        # # Process shared dependencies (if any).
        # if "shared_deps" in source:
        #     for dep_path in source["shared_deps"]:
        #         print(f"Processing dependency: {dep_path}...")
        #         dep_chunks = parse_rs_files(dep_path)
        #         for program in programs:
        #             source_chunks[program].extend(dep_chunks)


        # Save this source's chunked data.
        output_path = f"parsed_chunks/{label}_chunks.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(source_chunks, f, indent=2)

        print(f"{label} chunks saved to {output_path}")

if __name__ == "__main__":
    main()