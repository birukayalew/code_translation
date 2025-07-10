import os
import json
import openai
from time import sleep
from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
import time

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