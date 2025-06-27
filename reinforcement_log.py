# reinforcement_log.py

import time

class ReinforcementLogger:
    def __init__(self):
        self.log = []
        self.behavior_weights = {}  # e.g. {"tantrum": -0.2, "smile": +0.3}

    def log_feedback(self, emotion, intensity, behavior, context, feedback, reinforcement):
        entry = {
            "timestamp": time.time(),
            "emotion": emotion,
            "intensity": intensity,
            "behavior": behavior,
            "context": context,
            "feedback": feedback,
            "reinforcement": reinforcement
        }
        self.log.append(entry)
        self._update_behavior_weight(behavior, reinforcement)

    def _update_behavior_weight(self, behavior, reinforcement):
        current = self.behavior_weights.get(behavior, 0.0)
        updated = current + reinforcement
        self.behavior_weights[behavior] = max(min(updated, 1.0), -1.0)

    def get_behavior_weight(self, behavior):
        return self.behavior_weights.get(behavior, 0.0)

    def get_recent_logs(self, limit=10):
        return self.log[-limit:]
    