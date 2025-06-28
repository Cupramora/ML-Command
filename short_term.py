# short_term.py

import time
import math

class ShortTermMemory:
    def __init__(self, max_slots=12):
        self.slots = []  # List of memory entries
        self.max_slots = max_slots

    def _calculate_significance(self, capsule):
        # Estimate how meaningful this capsule is
        emotion_intensity = max(capsule.emotion_vector.values()) if capsule.emotion_vector else 0.0
        novelty = capsule.stimulus.get("novelty_score", 0.5)
        clarity = capsule.stimulus.get("clarity", 0.5)
        attention = capsule.stimulus.get("attention", 0.5)

        return round(
            (emotion_intensity * 0.4) +
            (novelty * 0.3) +
            (clarity * 0.2) +
            (attention * 0.1), 3
        )

    def _decay_significance(self, entry):
        age = time.time() - entry["timestamp"]
        decay_rate = 0.0001  # Tune this to match your time scale
        decayed = entry["significance"] * math.exp(-decay_rate * age)
        return round(decayed, 4)

    def add_capsule(self, capsule):
        sig = self._calculate_significance(capsule)
        entry = {
            "timestamp": time.time(),
            "capsule": capsule,
            "significance": sig
        }

        self.slots.append(entry)
        self._prune_slots()

    def _prune_slots(self):
        if len(self.slots) > self.max_slots:
            self.slots.sort(key=lambda e: self._decay_significance(e))
            self.slots = self.slots[-self.max_slots:]

    def get_recent(self):
        return [e["capsule"].to_dict() for e in self.slots]

    def get_promotable(self, threshold=0.75):
        return [
            e["capsule"]
            for e in self.slots
            if self._decay_significance(e) >= threshold
        ]
