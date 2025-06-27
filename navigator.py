# navigator.py

import os
import shutil
import json

class Navigator:
    def __init__(self, base_path="mindspace/", correction_log="categorization_memory.json"):
        self.base_path = base_path
        self.correction_log = correction_log
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.correction_log):
            with open(self.correction_log, "r") as f:
                return json.load(f)
        return {}

    def _save_memory(self):
        with open(self.correction_log, "w") as f:
            json.dump(self.memory, f, indent=2)

    def categorize(self, file_candidates):
        for item in file_candidates:
            tag = item["tag"]
            folder = item["suggested_folder"]
            source = item["source"]

            # Learn from past corrections
            if tag in self.memory:
                folder = self.memory[tag]["preferred_folder"]

            # Simulate file placement
            target_path = os.path.join(self.base_path, folder)
            os.makedirs(target_path, exist_ok=True)

            # Placeholder: simulate file move
            print("[Navigator] Placing " + source + " -> " + folder + "/")

    def log_correction(self, tag, correct_folder):
        if tag not in self.memory:
            self.memory[tag] = {
                "preferred_folder": correct_folder,
                "corrections": 1
            }
        else:
            self.memory[tag]["preferred_folder"] = correct_folder
            self.memory[tag]["corrections"] += 1

        self._save_memory()