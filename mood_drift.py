# mood_drift.py

import time
import random

class MoodDrift:
    def __init__(self):
        self.mood_vector = {
            "curiosity": 0.3,
            "melancholy": 0.1,
            "trust": 0.4,
            "anxiety": 0.2
        }
        self.last_update = time.time()

    def update_from_capsule(self, capsule):
        for emotion, intensity in capsule.emotion_vector.items():
            if emotion in self.mood_vector:
                delta = (intensity - self.mood_vector[emotion]) * 0.1
                self.mood_vector[emotion] += delta

    def decay_and_drift(self):
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now

        for emotion in self.mood_vector:
            drift = random.uniform(-0.01, 0.01)
            self.mood_vector[emotion] = max(0.0, min(1.0, self.mood_vector[emotion] + drift))

    def get_dominant_mood(self):
        return max(self.mood_vector, key=self.mood_vector.get)