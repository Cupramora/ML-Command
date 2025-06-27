# karma.py

class KarmaEngine:
    def __init__(self):
        self.karma_score = 0.0  # range: -1.0 to +1.0
        self.history = []

    def log_deed(self, deed_type, intent, outcome=None):
        base_reward = self._base_reward(deed_type, intent)
        echo_bonus = self._echo_bonus(outcome)

        total_reward = base_reward + echo_bonus
        self.karma_score += total_reward
        self.karma_score = max(min(self.karma_score, 1.0), -1.0)

        self.history.append({
            "deed": deed_type,
            "intent": intent,
            "outcome": outcome,
            "reward": total_reward
        })

        return total_reward

    def _base_reward(self, deed, intent):
        # Faith-based gratification
        if intent in ["help", "comfort", "protect"]:
            return 0.1
        return 0.05

    def _echo_bonus(self, outcome):
        # Optional: reward if kindness is returned later
        if outcome == "positive_response":
            return 0.2
        return 0.0