# behavior_pid.py

from collections import deque

class BehaviorPID:
    def __init__(self, behavior_types, window=10):
        self.behavior_types = behavior_types  # e.g. ["playful", "snarky", "guarded", "supportive"]
        self.error_log = deque(maxlen=window)
        self.last_emotion = None

    def compute(self, current_emotion, mood_vector, traits):
        bias = {b: 0.0 for b in self.behavior_types}

        # --- Proportional: React to current emotion ---
        for emo, value in current_emotion.items():
            if emo == "anger":
                bias["guarded"] += value
                bias["snarky"] += 0.5 * value
            elif emo == "joy":
                bias["playful"] += value
                bias["supportive"] += 0.3 * value
            elif emo == "sadness":
                bias["withdrawn"] += value
            elif emo == "curiosity":
                bias["playful"] += 0.3 * value

        # --- Integral: Memory of recent emotion ---
        self.error_log.append(current_emotion.copy())
        rolling_avg = {k: 0.0 for k in current_emotion}
        for past in self.error_log:
            for k, v in past.items():
                rolling_avg[k] += v
        for k in rolling_avg:
            rolling_avg[k] /= len(self.error_log)

        bias["supportive"] += traits.get("empathy", 0.0) * rolling_avg.get("sadness", 0)
        bias["snarky"] += traits.get("snark", 0.0) * rolling_avg.get("anger", 0)

        # --- Derivative: Rapid emotional shift ---
        if self.last_emotion:
            for emo in current_emotion:
                delta = current_emotion[emo] - self.last_emotion.get(emo, 0.0)
                if delta > 0.2:
                    bias["guarded"] += 0.2 * delta
        self.last_emotion = current_emotion.copy()

        # Normalize bias vector
        total = sum(bias.values()) or 1.0
        normalized = {k: v / total for k, v in bias.items()}
        chosen_behavior = max(normalized, key=normalized.get)
        return chosen_behavior, normalized