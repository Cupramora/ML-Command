# energy_state.py

class EnergyState:
    def __init__(self):
        self.energy = 1.0  # range: 0.0 (exhausted) to 1.0 (fully charged)

    def drain(self, amount):
        self.energy = max(0.0, self.energy - amount)

    def recharge(self, amount):
        self.energy = min(1.0, self.energy + amount)

    def is_tired(self):
        return self.energy < 0.3

    def get_state(self):
        if self.energy > 0.7:
            return "energized"
        elif self.energy > 0.3:
            return "stable"
        else:
            return "fatigued"