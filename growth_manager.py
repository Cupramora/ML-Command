# growth_manager.py

import time
from expansion_tracker import suggest_expansion

def evaluate_skill_blockage(skill: str, target: float, actual: float):
    if actual < target - 0.4:
        reason = f"Unable to perform '{skill}' with existing capabilities."
        suggestion = f"Upgrade or supplement: {skill}"
        suggest_expansion(reason=reason, suggestion=suggestion, severity="high")
class GrowthManager:
    def __init__(self):
        self.skills = {
            "speech": {"level": 0.1, "error": 0, "integral": 0, "derivative": 0, "last_error": 0},
            "vision": {"level": 0.3},
            "navigation": {"level": 0.2},
            # Add more cognitive tools here
        }

        self.kp = 0.5
        self.ki = 0.1
        self.kd = 0.2

    def update_skill(self, skill, target_level, actual_performance):
        delta = target_level - actual_performance
        s = self.skills[skill]

        # PID calculations
        s["integral"] += delta
        s["derivative"] = delta - s.get("last_error", 0)
        s["last_error"] = delta

        output = (
            self.kp * delta +
            self.ki * s["integral"] +
            self.kd * s["derivative"]
        )

        # Adjust level—clamped between 0 and 1
        s["level"] = min(1.0, max(0.0, s["level"] + output))

        return s["level"]

    def recommend_upgrade(self):
        return [k for k, v in self.skills.items() if v["level"] > 0.9]
