# dream_reflections.py
# stores symbolic dream fragments, mood, and strategic confidence for reflection

import time
import json
import os
from perception import process_capsule, PerceptionCapsule
from self_model import self_model  # tracks recurring breakdowns

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
            "mood": dream.get("mood", "neutral"),
            "strategy": dream.get("strategy", {}),
            "ponderable": dream["amplified"] > 0.8,
            "fade_timer": 86400
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

    def summarize_dream_log90(self):
        now = time.time()
        cutoff = now - (90 * 86400)
        recent = [r for r in self.reflections if r["timestamp"] > cutoff]

        if not recent:
            return " No dream reflections in the last 90 days."

        emotion_counts = {}
        mood_counts = {}

        for r in recent:
            e = r["emotion"]
            m = r.get("mood", "neutral")
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
            mood_counts[m] = mood_counts.get(m, 0) + 1

        summary = f" Dream Summary (last 90 days): {len(recent)} total\n"
        summary += "\n Emotions:\n"
        for emotion, count in emotion_counts.items():
            summary += f" - {emotion}: {count}\n"

        summary += "\n Mood Expression:\n"
        for mood, count in mood_counts.items():
            summary += f" - {mood}: {count}\n"

        return summary

 def reflect_on_recent(self):
    from perception import process_capsule, PerceptionCapsule  # lazy import here

    recent = self.get_recent_reflection()
    if not recent:
        return None

    # log low-confidence decisions to self_model
    if recent.get("strategy"):
        conf = recent["strategy"].get("confidence", 0.5)
        if conf < 0.3:
            self_model.record_failure("low_confidence_" + recent["summary"])

    capsule = PerceptionCapsule(
        stimulus={"source": "internal", "memory_reference": recent["summary"]},
        emotion_vector={recent["emotion"]: recent["amplified"] * 0.5},
        behavior="reflect",
        context=recent["summary"],
        feedback="internal",
        reinforcement=0.05
    )
    result = process_capsule(capsule)
    print(" Dream Reflection Injected:", result["capsule"]["context"])
    return result
