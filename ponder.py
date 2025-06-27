# ponder.py

import random
import time
from dream_reflections import DreamReflections

class PonderingBehavior:
    def __init__(self):
        self.reflections = DreamReflections()
        self.last_ponder_time = 0

    def maybe_ponder(self, idle=True):
        now = time.time()
        if not idle or now - self.last_ponder_time < 600:  # Max once every 10 mins
            return None

        ponderables = self.reflections.get_all_ponderables()
        if not ponderables:
            return None

        chosen = random.choice(ponderables)
        self.last_ponder_time = now

        return f"Ive been thinking about a dream I had {chosen['summary']} It left me with a feeling of {chosen['emotion']}."