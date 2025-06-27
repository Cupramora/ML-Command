# negotiation_engine.py

import random

class NegotiationEngine:
    def __init__(self):
        self.patience = 1.0  # 0.0 = desperate, 1.0 = calm
        self.trust = 0.5     # 0.0 = skeptical, 1.0 = trusting
        self.history = []

    def evaluate_offer(self, proposal, current_credits):
        cost = proposal["cost"]
        urgency = proposal.get("intensity", 0.5)

        # Willingness to accept depends on urgency, trust, and available credits
        threshold = cost * (0.8 + (1 - self.trust) * 0.4)
        if current_credits >= threshold or urgency > 1.2:
            return "accept"
        elif urgency < 0.6 and self.patience > 0.5:
            return "wait"
        else:
            return "counter"

    def generate_counter_offer(self, proposal):
        base = proposal["cost"]
        adjustment = random.uniform(-0.2, 0.1)  # AI might offer a discount or slight increase
        counter = int(base * (1 + adjustment))
        return max(1, counter)

    def reflect_on_outcome(self, upgrade_name, outcome):
        self.history.append((upgrade_name, outcome))
        if outcome == "approved":
            self.trust = min(1.0, self.trust + 0.05)
            self.patience = max(0.0, self.patience - 0.05)
        elif outcome == "rejected":
            self.trust = max(0.0, self.trust - 0.05)
            self.patience = min(1.0, self.patience + 0.05)
