# personality_loop.py

import time
from personality import Personality
from mood import Mood  # Or import from mood_loop if coupled

class PersonalityLoop:
    def __init__(self, trait_keys):
        self.personality = Personality(trait_keys)
        self.last_processed = None  # Last timestamp of applied mood

    def update(self, mood_day_snapshots):
        # Only process new mood logs
        for snapshot in mood_day_snapshots:
            ts = snapshot["timestamp"]
            if self.last_processed is None or ts > self.last_processed:
                mood_vector = snapshot["mood_vector"]
                self.personality.adjust_traits(mood_vector)
                self.last_processed = ts
                print(f"[PersonalityLoop] Updated traits with day @ {ts}")

    def get_personality_vector(self):
        return self.personality.get_personality_vector()