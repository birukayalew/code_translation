import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

all_lints = set()
custom_sheets = pd.read_excel("clippy_custom_categories.xlsx", sheet_name=None)
URL = "https://rust-lang.github.io/rust-clippy/master/index.html"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
# script_dir = os.path.dirname(__file__)
# output_excel_path = os.path.join(script_dir, "clippy_lints.xlsx")


# All lints are inside <article> elements.
lint_articles = soup.find_all("article")

lint_data = []

# First, collect all lints from the custom sheet.
# Process each sheet.
for sheet_name, df_sheet in custom_sheets.items():
    df_sheet.columns = [col.strip().lower() for col in df_sheet.columns]
    lint_col = next((c for c in df_sheet.columns if "lint name" in c), None)
    category_col = next((c for c in df_sheet.columns if "custom category" in c), None)

    if not lint_col or not category_col:
        continue  # Skip sheet if required columns not found.

    for _, row in df_sheet.iterrows():
        lint_name = str(row[lint_col]).strip().lower()
        all_lints.add(lint_name)
        custom_category = row[category_col]

# Scrape.
for article in lint_articles:
    lint_id = article.get("id", "").strip()
    header = article.find("h2", class_="panel-title")
    if not header:
        continue

    lint_name = header.find("span").text.strip()

    # Skip lints not in the predefined custom sheet.
    if lint_name not in all_lints:
        continue

    # Group and severity.
    group_label = header.find("span", class_="label-group-restriction") or \
                  header.find("span", class_="label-group-style") or \
                  header.find("span", class_="label-group-pedantic") or \
                  header.find("span", class_="label-group-complexity") or \
                  header.find("span", class_="label-group-suspicious") or \
                  header.find("span", class_="label-group-nursery") or \
                  header.find("span", class_="label-group-cargo") or \
                  header.find("span", class_="label-group-deprecated") or \
                  header.find("span", class_="label-group-correctness") or \
                  header.find("span", class_="label-group-perf")
                  

    group = group_label.text.strip() if group_label else "none"

    level_label = header.find("span", class_="label-lint-level-allow") or \
                  header.find("span", class_="label-lint-level-warn") or \
                  header.find("span", class_="label-lint-level-deny") or \
                  header.find("span", class_="label-lint-level-none")

    severity = level_label.text.strip() if level_label else "none"

    # # Short description from the "What it does" section
    # doc_block = article.find("div", class_="lint-docs")
    # description = ""
    # if doc_block:
    #     what_it_does = doc_block.find("h3", string="What it does")
    #     if what_it_does:
    #         desc_p = what_it_does.find_next_sibling("p")
    #         if desc_p:
    #             description = desc_p.text.strip()

    lint_data.append({
        "Lint Name": lint_name,
        "Group": group,
        "Severity": severity,
        # "Description": description,
        # "URL": f"{URL}#{lint_id}"
    })

# Save to DataFrame.
df = pd.DataFrame(lint_data)
# df.to_csv("clippy_lints_full.csv", index=False)
df.to_excel("clippy_lints.xlsx", index=False)
print("✅ Lint info scraped and saved to clippy_lints.xlsx")
