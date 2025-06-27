# identity.py

class Identity:
    def __init__(self, identity_keys):
        # Long-term belief values (e.g. "Im logical", "I value independence")
        self.core_values = {k: 0.5 for k in identity_keys}
        self.value_history = []

    def update_from_personality(self, personality_vector, learning_rate=0.001):
        """
        Slow, asymptotic adjustment based on personality PID smoothed traits.
        """
        for k, v in personality_vector.items():
            if k in self.core_values:
                delta = v - self.core_values[k]
                self.core_values[k] += learning_rate * delta

        self.value_history.append(personality_vector.copy())

    def get_identity_vector(self):
        return self.core_values.copy()