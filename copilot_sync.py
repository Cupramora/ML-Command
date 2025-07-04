# copilot_sync.py
# Author: Dane & Copilot
# Purpose: Index all cognition-related repos and generate a unified context bundle
# Usage: Run this from your parent directory to sweep all listed submodules

import os
import json
import zipfile

# === CONFIGURATION ===
REPOS = [
    "ML-Command", "ML-SensorHub", "ML-ElectricVariationControl", "ML-FlightControl",
    "ML-RenderMorph", "ML-Social", "ML-Upgrades", "OpenCV", "Toolbox", "ultralytics"
]
INCLUDE_EXT = [".py", ".json", ".md", ".sh"]
SUMMARY_FILE = "copilot_context_summary.json"
BUNDLE_FILE = "copilot_bundle.zip"

# === CRAWLER FUNCTION ===
def scan_repo(root_path):
    summary = {}
    for root, _, files in os.walk(root_path):
        for fname in files:
            ext = os.path.splitext(fname)[1]
            if ext in INCLUDE_EXT:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    first_line = content.splitlines()[0] if content else ""
                    summary[fpath] = {
                        "lines": len(content.splitlines()),
                        "preview": content[:300],
                        "mnemonic": first_line.strip() if first_line.startswith("#") else ""
                    }
                except Exception as e:
                    summary[fpath] = {"error": str(e)}
    return summary

# === ZIP FUNCTION ===
def zip_all(files, zip_name):
    with zipfile.ZipFile(zip_name, "w") as z:
        for f in files:
            try:
                z.write(f)
            except Exception as e:
                print(f" Could not add {f} to zip: {e}")

# === MAIN ===
if __name__ == "__main__":
    full_summary = {}
    all_files = []

    print("📡 Scanning all repositories for Copilot sync...\n")
    for repo in REPOS:
        if os.path.exists(repo):
            print(f" Indexing: {repo}")
            summary = scan_repo(repo)
            full_summary.update(summary)
            all_files.extend(summary.keys())
        else:
            print(f"⚠ Repo not found: {repo}")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(full_summary, f, indent=2)

    all_files.append(SUMMARY_FILE)
    zip_all(all_files, BUNDLE_FILE)

    print(f"\n Context bundle created: {BUNDLE_FILE}")
    print(f" Summary file: {SUMMARY_FILE}")
