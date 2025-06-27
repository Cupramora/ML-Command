# long_term.py

import time
import math

class LongTermMemory:
    def __init__(self):
        self.entries = []  # List of long-term memory entries

    def _log_decay(self, significance, age):
        # Logarithmic decay: slower fade for high-sig memories
        return round(significance / math.log(age + 2), 4)

    def _is_promotable(self, capsule, significance_threshold=0.75):
        return capsule.reinforcement >= 0.3 or max(capsule.emotion_vector.values()) >= significance_threshold

    def store_capsule(self, capsule):
        timestamp = time.time()
        significance = max(capsule.emotion_vector.values()) + abs(capsule.reinforcement)

        entry = {
            "timestamp": timestamp,
            "capsule": capsule,
            "significance": round(significance, 3),
            "tags": self._generate_tags(capsule)
        }

        self.entries.append(entry)

    def _generate_tags(self, capsule):
        tags = []
        if "Dane" in capsule.context:
            tags.append("Dane")
        if capsule.feedback == "positive":
            tags.append("reward")
        if max(capsule.emotion_vector.values()) > 0.8:
            tags.append("emotional_spike")
        return tags

    def recall_by_tag(self, tag):
        return [
            e["capsule"].to_dict()
            for e in self.entries
            if tag in e["tags"]
        ]

    def get_retained(self, min_significance=0.6):
        now = time.time()
        return [
            e["capsule"].to_dict()
            for e in self.entries
            if self._log_decay(e["significance"], now - e["timestamp"]) >= min_significance
        ]