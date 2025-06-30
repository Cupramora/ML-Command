# state_manager.py

import time
import random
from dream_timer import DreamTimer
from self_reasoning import run_self_reasoning
from goal_stack import GoalStack  # lives in ML-Social

class StateManager:
    def __init__(self, short_term_memory, dream_state):
        self.state = "idle"
        self.last_active = time.time()
        self.energy = 1.0
        self.dream_timer = DreamTimer()
        self.stm = short_term_memory
        self.dream_state = dream_state
        self.goals = GoalStack()

    def evaluate_state(self, stimulus=None, internal_drive=None):
        now = time.time()
        time_since_active = now - self.last_active

        # dream logic (only when idle)
        if self.state == "idle":
            emotional_backlog = any(
                e["significance"] < 0.5 and e["capsule"].flags.get("emotional_spike")
                for e in self.stm.slots
            )

            if self.dream_timer.should_dream(emotional_backlog=emotional_backlog):
                self.dream_state.process_dreams()

            if self.energy < 0.4 and time_since_active > 180:
                if random.random() < 0.15:
                    self.state = "comfort"
                    return self.state

            if random.random() < 0.1:
                self.dream_state.reflect_on_recent()

            if random.random() < 0.03:
                run_self_reasoning()

            # check internal drive pressure
            drive_result = self.goals.check_drive_pressure()
            if drive_result:
                self.state = "active"
                self.energy = min(1.0, self.energy + 0.2)
                self.last_active = now
                return self.state

        # wake from external stimulus
        if stimulus and stimulus.get("type") in ["touch", "sound", "motion"]:
            self.state = "active"
            self.energy = min(1.0, self.energy + 0.3)
            self.last_active = now
            return self.state

        # wake from internal curiosity
        if internal_drive and internal_drive.get("novelty_detected"):
            self.state = "active"
            self.energy = min(1.0, self.energy + 0.2)
            self.last_active = now
            return self.state

        # natural idle decay
        if time_since_active > 300:
            self.energy = max(0.0, self.energy - 0.01)
            if self.energy < 0.3:
                self.state = "idle"

        return self.state

    def is_awake(self):
        return self.state == "active"

    def force_sleep(self):
        self.state = "idle"
        self.energy = 0.0
