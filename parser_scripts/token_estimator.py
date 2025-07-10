import json
import tiktoken
from pathlib import Path

json_path = Path("parsed_chunks/c2rust_chunks.json")
with open(json_path, "r", encoding="utf-8") as f:
    program_chunks = json.load(f)

enc = tiktoken.encoding_for_model("gpt-4")

max_tokens = 0
max_info = None

for program, chunks in program_chunks.items():
    for i, chunk in enumerate(chunks):
        token_count = len(enc.encode(chunk))
        if token_count > max_tokens:
            max_tokens = token_count
            max_info = (program, i, token_count)

print(f"🔢 Max token count: {max_tokens} (Program: {max_info[0]}, Chunk index: {max_info[1]})")
