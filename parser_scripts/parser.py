import os
from tree_sitter_languages import get_language, get_parser

RUST_LANGUAGE = get_language('rust')
parser = get_parser('rust')

def get_code_lines(code, node):
    """Return list of code lines for the given node."""
    code = code.encode("utf8")
    snippet = code[node.start_byte:node.end_byte].decode("utf8", errors="replace")
    return snippet.splitlines()

def extract_chunked_code(filepath, max_lines=300):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    tree = parser.parse(code.encode("utf8"))
    root = tree.root_node

    all_chunks = []
    current_chunk = []
    current_line_count = 0
    count = 0
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

if __name__ == "__main__":
    test_file = os.path.join("example_code", "non_idiomatic.rs")
    chunks = extract_chunked_code(test_file, max_lines=300)
    print(chunks)

    # output_path = os.path.join(os.path.dirname(__file__), "chunked_output.json")
    # with open(output_path, "w", encoding="utf-8") as f:
    #     json.dump(chunks, f, indent=2)

    # print(f"Extracted {len(chunks)} chunks to {output_path}")
