# cleanup_duplicates.py
import os
from collections import defaultdict

BASE_DIR = "path/to/your/repo"  # <- update this
DUPLICATES_LOG = "duplicates_found.txt"

file_index = defaultdict(list)

for root, _, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".py"):
            file_index[f].append(os.path.join(root, f))

with open(DUPLICATES_LOG, "w") as log:
    for filename, paths in file_index.items():
        if len(paths) > 1:
            log.write(f"\nDuplicate found: {filename}\n")
            for p in paths:
                log.write(f"  - {p}\n")

print(f"Scan complete. Duplicates logged in '{DUPLICATES_LOG}'")
