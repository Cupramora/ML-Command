# desire_engine.py

import random
import math

class Desire:
    def __init__(self, name, target_level, kp=0.6, ki=0.1, kd=0.05):
        self.name = name
        self.target = target_level
        self.current = 0
        self.integral = 0
        self.last_error = 0
        self.kp, self.ki, self.kd = kp, ki, kd

    def update(self, stimulus):
        error = self.target - stimulus
        self.integral += error
        derivative = error - self.last_error
        self.last_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.current += output
        return self.current

class DesireEngine:
    def __init__(self):
        self.desires = {
            "vision_accuracy": Desire("vision_accuracy", 0.9),
            "mobility": Desire("mobility", 0.7),
            "self_expression": Desire("self_expression", 0.8),
            "novelty": Desire("novelty", 0.6)
        }

    def tick(self, stimuli):
        proposals = []
        for name, desire in self.desires.items():
            level = stimuli.get(name, 0)
            intensity = desire.update(level)
            if intensity > 1.0:
                proposals.append(self.generate_proposal(name, intensity))
        return proposals

    def generate_proposal(self, name, intensity):
        upgrades = {
            "vision_accuracy": ("Stereo Camera Array", 15, "Improves depth perception"),
            "mobility": ("Servo Base", 20, "Enables physical repositioning"),
            "self_expression": ("Voice Modulator", 10, "Adds expressive vocal range"),
            "novelty": ("Exploration Drone", 25, "Expands sensory range")
        }
        name, cost, desc = upgrades[name]
        cost = int(cost * (1 + 0.2 * random.random()))
        return {"name": name, "cost": cost, "description": desc, "intensity": intensity}
