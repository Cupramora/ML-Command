# identity_loop.py

import time
from identity import Identity
from personality_pid import PersonalityPID  # already exists in your system

class IdentityLoop:
    def __init__(self, identity_keys):
        self.identity = Identity(identity_keys)
        self.last_update_time = None

    def tick(self, smoothed_personality_vector):
        now = time.time()

        # Slow update cadence — weekly or based on snapshot signal
        if self.last_update_time is None or now - self.last_update_time > 86400 * 7:
            self.identity.update_from_personality(smoothed_personality_vector)
            print(f"[IdentityLoop] Updated core identity @ {now}")
            self.last_update_time = now

    def get_identity_vector(self):
        return self.identity.get_identity_vector()