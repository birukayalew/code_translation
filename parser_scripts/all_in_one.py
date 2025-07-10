import os
import json
from tree_sitter_languages import get_language, get_parser
import json
import openai
from time import sleep
from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
import time


#................. Single file parser......................
RUST_LANGUAGE = get_language('rust')
parser = get_parser('rust')

def get_code_lines(code, node):
    """Return list of code lines for the given node."""
    snippet = code[node.start_byte:node.end_byte]
    return snippet.splitlines()

def extract_chunked_code(filepath, max_lines=500):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(code.encode("utf8"))
    root = tree.root_node

    all_chunks = []
    current_chunk = []
    current_line_count = 0

    for child in root.children:
        lines = get_code_lines(code, child)
        line_count = len(lines)

        if line_count > max_lines:
            # If there's something in current_chunk, save it.
            if current_chunk:
                all_chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_line_count = 0

            # Add full-size chunks directly.
            for i in range(0, line_count - max_lines + 1, max_lines):
                part = lines[i:i + max_lines]
                all_chunks.append('\n'.join(part))

            # Add leftover part to current_chunk (deferred processing).
            remainder_start = (line_count // max_lines) * max_lines
            if remainder_start < line_count:  # check if there are leftovers.
                current_chunk = lines[remainder_start:]
                current_line_count = len(current_chunk)
        else:
            # Would this exceed max_lines?
            if current_line_count + line_count > max_lines:
                all_chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_line_count = 0

            current_chunk.extend(lines) 
            current_line_count += line_count

    if current_chunk:
        all_chunks.append('\n'.join(current_chunk))

    return all_chunks


# ................batch runner.................
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


#.........................gpt request sender....................

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("parsed_chunks/c2rust_chunks.json", "r", encoding="utf-8") as f:
    all_chunks = json.load(f)

with open("parser_scripts/prompt.txt", "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

def send_prompt(chunk_text):
    prompt = PROMPT_TEMPLATE.replace("<CHUNK>", chunk_text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful and precise Rust code reviewer and linter. You identify non-idiomatic constructs, unsafe patterns, and unnecessary operations, and annotate them clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        # max_tokens=1024
    )
    return response.choices[0].message.content

def main():
    responses_by_file = {}

    for file_key, chunks in all_chunks.items():
        file_responses = []

        for i, chunk in enumerate(tqdm(chunks, desc=f"Processing {file_key}")):
            try:
                result = send_prompt(chunk)
                file_responses.append(result)
                time.sleep(60)  # delay to avoid rate limits.
            except Exception as e:
                print(f"[ERROR] {file_key} chunk {i}: {e}")
                file_responses.append(f"[ERROR] {str(e)}")
                time.sleep(5)

        responses_by_file[file_key] = file_responses

    # Save everything to a single JSON file.
    output_path = "llm_chunk_responses/c2rust_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(responses_by_file, f, indent=2)

    print(f"\nAll responses saved to: {output_path}")

if __name__ == "__main__":
    main()

