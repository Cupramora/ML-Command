# credit_inflation.py

class CreditInflation:
    def __init__(self, base_rate=0.02):
        self.base_rate = base_rate
        self.history = []

    def adjust_cost(self, base_cost, performance_score, credit_velocity):
        inflation = self.base_rate + (credit_velocity * 0.05) - (performance_score * 0.03)
        inflation = max(0.0, min(inflation, 0.5))
        adjusted = int(base_cost * (1 + inflation))
        self.history.append(inflation)
        return adjusted

    def get_trend(self):
        if not self.history:
            return "Stable"
        avg = sum(self.history[-5:]) / min(5, len(self.history))
        if avg > 0.1:
            return "Rising"
        elif avg < 0.01:
            return "Deflating"
        return "Stable"
