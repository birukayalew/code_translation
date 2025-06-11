import os
from collections import Counter, defaultdict
from scripts.clippy_warning_outputs_analyzer import get_category_counts_from_file


def batch_runner(code_type, directory):
    total_category_counts = Counter()
    total_severity_counts = defaultdict(Counter)
    # Go through all output files in the folder.
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            category_counts, severity_counts, all_categories = get_category_counts_from_file(code_type, filename)
            total_category_counts.update(category_counts)

            for category, sev_counter in severity_counts.items():
                total_severity_counts[category].update(sev_counter)

    # Make sure all categories are present.
    for cat in all_categories:
        if cat not in total_category_counts:
            total_category_counts[cat] = 0
        for sev in ['deny', 'warn', 'allow', 'none']:
            if sev not in total_severity_counts[cat]:   
                total_severity_counts[cat][sev] = 0

    print("\n📊 Total Warning Counts by Custom Category ({code_type}):")
    for category, count in total_category_counts.most_common():
        print(f"{category}: {count}")

    return total_category_counts, total_severity_counts

    