from scripts.clippy_warning_outputs_analyzer import get_category_counts_from_file


category_counts, _, all_categories= get_category_counts_from_file("test", "test_clippy_output.txt")

print("\n=== Custom Category Counts ===")
for category, count in category_counts.items():
    print(f"{category}: {count}")
print(len(category_counts))