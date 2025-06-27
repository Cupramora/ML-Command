class ImpulseRegulator:
    def __init__(self):
        self.impulse_score = 0.5
        self.wisdom_score = 0.1  # Grows over time

    def update_from_experience(self, reward):
        if reward > 0:
            self.wisdom_score = min(1.0, self.wisdom_score + 0.01)
        else:
            self.impulse_score = max(0.0, self.impulse_score - 0.02)

    def approve_action(self, urgency, novelty, desire_strength):
        impulsiveness = (urgency + novelty + desire_strength) / 3
        regulation = impulsiveness - self.wisdom_score
        return regulation > 0.2  # Approve if still over threshold
