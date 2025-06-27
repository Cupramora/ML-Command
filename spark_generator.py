# spark_generator.py

import random
import time

class SparkGenerator:
    def __init__(self, mood_engine, memory):
        self.mood_engine = mood_engine
        self.memory = memory
        self.last_spark = 0

    def maybe_spark(self):
        now = time.time()
        if now - self.last_spark < 300:
            return None  # Only spark every 5 minutes max

        unresolved = self.memory.get_unresolved_flags()
        mood = self.mood_engine.get_dominant_mood()

        if unresolved and mood in ["curiosity", "melancholy"]:
            self.last_spark = now
            prompt = random.choice([
                "I keep thinking about that moment… what did it mean?",
                "There’s a pattern I haven’t unraveled yet.",
                "Do you think I misunderstood something important?",
                "That dream… it felt like a question I haven’t asked."
            ])
            return prompt

        return None