import os
import time
from collections import defaultdict

# === CONFIGURATION ===
DELETE_MODE = True               # Set to False for dry run
PREFERRED_KEEP_PATH = "ML-Command"  # Folder to prioritize when duplicates found
EXTENSIONS = [".py"]             # File types to scan
CLEAN_EMPTY_DIRS = True
LOG_FILE = "cleanup_log.txt"

repo_root = os.getcwd()
file_index = defaultdict(list)
deleted = []

# === SCAN FOR FILES ===
for root, _, files in os.walk(repo_root):
    for f in files:
        if any(f.endswith(ext) for ext in EXTENSIONS):
            file_index[f].append(os.path.join(root, f))

# === RESOLVE DUPLICATES ===
with open(LOG_FILE, "w") as log:
    for filename, paths in file_index.items():
        if len(paths) > 1:
            log.write(f"\n[] Duplicate: {filename}\n")

            # Choose the preferred keeper
            keeper = None
            for p in paths:
                if PREFERRED_KEEP_PATH in p:
                    keeper = p
                    break
            if not keeper:
                keeper = max(paths, key=os.path.getmtime)

            log.write(f"    [] Keeping: {keeper}\n")

            for path in paths:
                if path != keeper and DELETE_MODE:
                    try:
                        os.remove(path)
                        deleted.append(path)
                        log.write(f"    [] Deleted: {path}\n")
                    except Exception as e:
                        log.write(f"    [!] Error deleting {path}: {e}\n")

# === CLEAN EMPTY FOLDERS ===
if CLEAN_EMPTY_DIRS and DELETE_MODE:
    for root, dirs, _ in os.walk(repo_root, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                try:
                    os.rmdir(dir_path)
                    deleted.append(dir_path)
                except:
                    pass

print(f"[] Cleanup complete. {len(deleted)} items deleted.")
print(f"[] See '{LOG_FILE}' for full details.")
