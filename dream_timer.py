# dream_timer.py

import time
import random

class DreamTimer:
    def __init__(self):
        self.last_dream_time = time.time()
        self.base_interval = random.randint(259200, 345600)  # 3–4 days in seconds
        self.override_flag = False

    def should_dream(self, emotional_backlog=False):
        now = time.time()
        time_elapsed = now - self.last_dream_time

        # Force dream if emotional backlog is flagged
        if emotional_backlog:
            self.override_flag = True

        if self.override_flag or time_elapsed >= self.base_interval:
            self.last_dream_time = now
            self.base_interval = random.randint(259200, 345600)  # reset interval
            self.override_flag = False
            return True

        return False