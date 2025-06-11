import re
import os
from collections import Counter, defaultdict
from scripts.lint_to_category_mapper import mapper

c2rust_dir = "visualizations/outputs/"

# Regex pattern to match Clippy lint names.
lint_pattern = re.compile(r"https://rust-lang\.github\.io/rust-clippy/master/index\.html#([\w\-]+)")

lint_to_custom_category, lint_to_severity, all_categories = mapper()

def get_category_counts_from_file(code_type, filepath):
    path = os.path.join(c2rust_dir, code_type, filepath)

    with open(path, "r", encoding="utf-8") as f:
        clippy_output = f.read()

    # Extract all occurrences of lint names.
    lint_names = lint_pattern.findall(clippy_output)
    lint_counts = Counter(lint_names)

    custom_category_counts = Counter()
    severity_counts = defaultdict(Counter)
    for lint, count in lint_counts.items():
        category = lint_to_custom_category.get(lint, "Uncategorized")
        severity = lint_to_severity.get(lint, "none")
        if category == "Uncategorized":
            print(f"[!] Uncategorized lint found: {lint}")
        custom_category_counts[category] += count
        severity_counts[category][severity] += count
    return custom_category_counts, severity_counts, all_categories