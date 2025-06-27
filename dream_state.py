# dream_state.py

import random
import time
from dream_reflections import DreamReflections

class DreamState:
    def __init__(self, short_term_memory, long_term_memory):
        self.stm = short_term_memory
        self.ltm = long_term_memory
        self.reflections = DreamReflections()

    def process_dreams(self):
        now = time.time()
        for entry in self.stm.slots:
            sig = entry["significance"]
            spike = entry["capsule"].flags.get("emotional_spike", False)
            already_dreamed = entry["capsule"].flags.get("dreamed", False)

            if spike and sig < 0.5 and not already_dreamed:
                dream = self._generate_dream(entry["capsule"])
                entry["capsule"].flags["dreamed"] = True
                entry["capsule"].flags["dream_impression"] = dream

                # Log if emotionally meaningful
                if dream["amplified"] > 0.8:
                    self.reflections.log_dream(dream)

                # Optional: promote to long-term if dream reactivates it
                if dream["amplified"] > 0.9:
                    self.ltm.store_capsule(entry["capsule"])

    def _generate_dream(self, capsule):
        emotion = max(capsule.emotion_vector, key=capsule.emotion_vector.get)
        intensity = capsule.emotion_vector[emotion]
        abstract = random.choice(["a hallway", "a mirror", "a flickering light", "a distant voice"])

        return {
            "summary": f"A dream of {abstract} filled with {emotion}.",
            "emotion": emotion,
            "amplified": round(intensity + random.uniform(0.1, 0.3), 2)
        }

    def recall_last_dream(self):
        return self.reflections.get_recent_reflection()