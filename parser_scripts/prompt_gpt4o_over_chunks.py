import os
import json
import openai
from dotenv import load_dotenv
from tqdm import tqdm
from openai import OpenAI
import time

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sources to process.
sources = [
    "c2rust",
    "c2saferrust",
    "translation_gym",
    "human_written"
]

with open("parser_scripts/prompt.txt", "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

def send_prompt(chunk_text):
    prompt = PROMPT_TEMPLATE.replace("<CHUNK>", chunk_text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful and precise Rust code reviewer and linter. You identify non-idiomatic constructs, unsafe patterns, unnecessary operations, or any issues and categorize them clearly to the predefined categories."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        # max_tokens=1024
    )
    return response.choices[0].message.content

def process_source(source_label):
    input_path = f"parsed_chunks/{source_label}_chunks.json"
    output_path = f"llm_results/{source_label}_results.json"

    with open(input_path, "r", encoding="utf-8") as f:
        all_chunks = json.load(f)

    responses_by_file = {}

    for file_key, chunks in all_chunks.items():
        chunks = all_chunks[file_key]
        file_responses = []

        for i, chunk in enumerate(tqdm(chunks, desc=f"Processing {source_label}/{file_key}")):
            try:
                result = send_prompt(chunk)
                file_responses.append(result)
                time.sleep(60)  # delay to avoid rate limits.
            except Exception as e:
                print(f"[ERROR] {file_key} chunk {i}: {e}")
                file_responses.append(f"[ERROR] {str(e)}")
                time.sleep(5)

        responses_by_file[file_key] = file_responses

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(responses_by_file, f, indent=2)

    print(f"\nAll responses for {source_label} saved to: {output_path}")

def main():
    for source in sources:
        process_source(source)

if __name__ == "__main__":
    main()