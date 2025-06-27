# psyche_report.py

import time
from collections import Counter

class PsycheReport:
    def __init__(self, short_term_memory, dream_reflections, reinforcement_log):
        self.stm = short_term_memory
        self.reflections = dream_reflections
        self.reinforcement = reinforcement_log

    def generate_report(self):
        dominant_emotions = self._get_dominant_emotions()
        recent_topics = self._get_recent_topics()
        unresolved_flags = self._get_unresolved_flags()
        file_candidates = self._suggest_file_placements()

        return {
            "timestamp": time.time(),
            "dominant_emotions": dominant_emotions,
            "recent_topics": recent_topics,
            "unresolved_flags": unresolved_flags,
            "file_candidates": file_candidates
        }

    def _get_dominant_emotions(self):
        emotions = []
        for entry in self.stm.slots:
            emotions.extend(entry["capsule"].emotion_vector.keys())
        return [e for e, _ in Counter(emotions).most_common(3)]

    def _get_recent_topics(self):
        topics = []
        for entry in self.stm.slots:
            if "Dane" in entry["capsule"].context:
                topics.append("Dane")
            if entry["capsule"].flags.get("diagnostic_hint"):
                topics.append(entry["capsule"].flags["diagnostic_hint"])
        return list(set(topics))

    def _get_unresolved_flags(self):
        flags = []
        for entry in self.stm.slots:
            for key, val in entry["capsule"].flags.items():
                if key.startswith("diagnostic") or key == "dreamed_but_not_logged":
                    flags.append(key)
        return list(set(flags))

    def _suggest_file_placements(self):
        candidates = []
        for reflection in self.reflections.get_all_ponderables():
            candidates.append({
                "source": "pondering",
                "tag": "symbolic",
                "suggested_folder": "reflections"
            })
        for entry in self.stm.slots:
            if entry["capsule"].flags.get("trust_bias") == "positive":
                candidates.append({
                    "source": "capsule",
                    "tag": "behavioral",
                    "suggested_folder": "trust_bias"
                })
        return candidates