import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://rust-lang.github.io/rust-clippy/master/index.html"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

# All lints are inside <article> elements.
lint_articles = soup.find_all("article")

lint_data = []

for article in lint_articles:
    lint_id = article.get("id", "").strip()
    header = article.find("h2", class_="panel-title")
    if not header:
        continue

    lint_name = header.find("span").text.strip()

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
df.to_excel("../clippy_lints.xlsx", index=False)
print("✅ Lint info scraped and saved to clippy_lints_full.csv")
