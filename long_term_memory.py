# long_term_memory.py

import json
import os
import time

class LongTermMemory:
    def __init__(self, memory_file="long_term_memory.json"):
        self.memory_file = memory_file
        self.entries = []
        self._load()

    def _load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.entries = json.load(f)

    def _save(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.entries, f, indent=2)

    def store_capsule(self, capsule_dict):
        entry = {
            "timestamp": time.time(),
            "content": capsule_dict,
            "tags": capsule_dict.get("context", "")
        }
        self.entries.append(entry)
        self._save()

    def search_by_tag(self, keyword):
        return [e for e in self.entries if keyword in e["tags"]]
