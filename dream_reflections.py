# dream_reflections.py

import time
import json
import os

class DreamReflections:
    def __init__(self, log_path="dream_reflections.json"):
        self.log_path = log_path
        self.reflections = []
        self._load()

    def _load(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                self.reflections = json.load(f)

    def _save(self):
        with open(self.log_path, "w") as f:
            json.dump(self.reflections, f, indent=2)

    def log_dream(self, dream):
        entry = {
            "timestamp": time.time(),
            "summary": dream["summary"],
            "emotion": dream["emotion"],
            "amplified": dream["amplified"],
            "ponderable": dream["amplified"] > 0.8,
            "fade_timer": 86400  # 1 day until it fades from active recall
        }
        self.reflections.append(entry)
        self._save()

    def get_recent_reflection(self):
        now = time.time()
        self.reflections = [
            r for r in self.reflections
            if now - r["timestamp"] < r["fade_timer"]
        ]
        self._save()
        return self.reflections[-1] if self.reflections else None

    def get_all_ponderables(self):
        return [r for r in self.reflections if r["ponderable"]]
        from perception import process_capsule, PerceptionCapsule

def reflect_on_recent(self):
    recent = self.get_recent_reflection()
    if not recent:
        return None

    capsule = PerceptionCapsule(
        stimulus={"source": "internal", "memory_reference": recent["summary"]},
        emotion_vector={recent["emotion"]: recent["amplified"] * 0.5},
        behavior="reflect",
        context=recent["summary"],
        feedback="internal",
        reinforcement=0.05
    )
    result = process_capsule(capsule)
    print("💭 Dream Reflection Injected:", result["context"])
    return result
