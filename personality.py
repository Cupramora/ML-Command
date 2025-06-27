# personality.py

class Personality:
    def __init__(self, traits):
        self.traits = {t: 0.5 for t in traits}  # e.g. {"curiosity": 0.5, "snark": 0.3}
        self.trait_history = []

    def adjust_traits(self, mood_snapshot, learning_rate=0.01):
        """
        Disturbance: a single day's mood vector, like {"anger": 0.2, "joy": 0.6}
        We'll update each trait slightly based on how that day's mood aligns.
        """
        # Example logic: if joy high, nudge curiosity; if sadness high, nudge caution
        for mood_key, value in mood_snapshot.items():
            if mood_key == "joy":
                self.traits["curiosity"] += learning_rate * (value - 0.5)
                self.traits["warmth"] += learning_rate * (value - 0.5)
            elif mood_key == "anger":
                self.traits["snark"] += learning_rate * (value - 0.5)
                self.traits["patience"] -= learning_rate * (value - 0.5)
            # Add mappings as needed...

        # Clamp all traits between 0 and 1
        for t in self.traits:
            self.traits[t] = min(max(self.traits[t], 0.0), 1.0)

        self.trait_history.append(mood_snapshot)

    def get_personality_vector(self):
        return self.traits.copy()