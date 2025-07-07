import pandas as pd

df = pd.read_excel("clippy_lints.xlsx")

# Clean up whitespace (optional but helpful)
df.columns = [col.strip() for col in df.columns]
df["Lint Name"] = df["Lint Name"].str.strip()
df["Custom Category"] = df["Custom Category"].str.strip()
df["Severity"] = df["Severity"].str.strip()


# Merge rules.
MERGE_MAP = {
    "Precision issues": "Arithmetic issues",
    "Integer overflow": "Arithmetic issues",
    "Underflow issues": "Arithmetic issues",

    "Invalid pointer casting": "Type safety",
    "Unsafe transmutes": "Type safety",

    "Async concurrency issues": "Thread safety",

    "Implementation issues": "Convention violation",
    "Policy violation": "Convention violation",
    "Security": "Convention violation",

    "Resource leaks": "Memory safety",
    "Stack overflows": "Memory safety",
    "Pointer aliasing": "Memory safety",
    "Unsafe initialization": "Memory safety",
    "Missing unsafe block": "Memory safety",
}

def merge_categories():
    return df["Custom Category"].apply(
            lambda cat: MERGE_MAP.get(cat, cat)
    )