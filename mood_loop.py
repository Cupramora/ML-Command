# mood_loop.py

import time
from mood import Mood
from emotion_loop import EmotionLoop  # Assumes you have this built

class MoodLoop:
    def __init__(self, emotion_keys):
        self.emotion_loop = EmotionLoop(emotion_keys)
        self.mood = Mood(emotion_keys)
        self.last_day_timestamp = time.time()

    def tick(self):
        # Step 1: Update emotion loop
        self.emotion_loop.tick()
        emotion_vector = self.emotion_loop.get_state()  # Or similar method

        # Step 2: Feed into Mood
        self.mood.update(emotion_vector)

        # Step 3: Daily mood summary
        now = time.time()
        if now - self.last_day_timestamp >= 86400:  # 24 hours
            daily_snapshot = self.mood.finalize_day_mood()
            print("[MoodLoop] Daily mood snapshot recorded:", daily_snapshot)
            self.last_day_timestamp = now

    def get_mood(self):
        return self.mood.get_mood_vector()

    def get_mood_history(self):
        return getattr(self.mood, "daily_logs", [])