import time

class ReinforcementLogger:
    def __init__(self):
        self.log = []
        self.behavior_weights = {}      # e.g. {"tantrum": -0.2}
        self.behavior_confidence = {}   # e.g. {"smile": 0.6}

    def log_feedback(self, emotion, intensity, behavior, context, feedback, reinforcement, mood=None):
        entry = {
            "timestamp": time.time(),
            "emotion": emotion,
            "intensity": intensity,
            "behavior": behavior,
            "context": context,
            "feedback": feedback,
            "reinforcement": reinforcement
            "mood": mood
        }
        self.log.append(entry)
        self._update_behavior_weight(behavior, reinforcement)
        self._update_confidence(behavior, reinforcement)

    def _update_behavior_weight(self, behavior, reinforcement):
        current = self.behavior_weights.get(behavior, 0.0)
        updated = current + reinforcement
        self.behavior_weights[behavior] = max(min(updated, 1.0), -1.0)

    def _update_confidence(self, behavior, reinforcement):
        current = self.behavior_confidence.get(behavior, 0.5)  # neutral start
        delta = 0.1 * reinforcement
        updated = current + delta
        self.behavior_confidence[behavior] = max(min(updated, 1.0), 0.0)

    def get_behavior_weight(self, behavior):
        return self.behavior_weights.get(behavior, 0.0)

    def get_confidence(self, behavior):
        return self.behavior_confidence.get(behavior, 0.5)

    def get_recent_logs(self, limit=10):
        return self.log[-limit:]
