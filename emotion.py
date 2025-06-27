# emotion.py

import time
import math

class Emotion:
    def __init__(self, name, baseline, sensitivity, decay_rate):
        self.name = name
        self.baseline = baseline
        self.sensitivity = sensitivity
        self.decay_rate = decay_rate
        self.value = baseline
        self.last_update = time.time()
        self.last_spike_time = time.time()
    
    def adjust(self, stimulus_strength):
        now = time.time()
        elapsed = now - self.last_update
        delta = self.sensitivity * stimulus_strength
        self.value += delta
        self.last_spike_time = now
        self.last_update = now

    def evaluate(self):
        now = time.time()
        elapsed = now - self.last_spike_time
        decay = self.decay_rate * elapsed
        # Clamp decay so we don’t go below baseline
        self.value = max(self.baseline, self.value - decay)
        return self.value

# Create instances with different emotional personalities
emotions = {
    "joy":     Emotion("joy", baseline=0.30, sensitivity=1.2, decay_rate=0.01),
    "fear":    Emotion("fear", baseline=0.18, sensitivity=1.4, decay_rate=0.018),
    "disgust": Emotion("disgust", baseline=0.17, sensitivity=1.15, decay_rate=0.009),
    "anger":   Emotion("anger", baseline=0.15, sensitivity=1.3, decay_rate=0.025),
    "sadness": Emotion("sadness", baseline=0.15, sensitivity=1.0, decay_rate=0.015)
}

def get_emotion_vector():
    return {name: emo.evaluate() for name, emo in emotions.items()}

def normalize_emotions(emotion_values):
    total = sum(emotion_values.values())
    if total == 0:
        return emotion_values
    return {k: v / total for k, v in emotion_values.items()}
class EmotionalLobe:
    def __init__(self):
        self.emotions = emotions  # from your global dictionary

    def evaluate(self, logic_prediction: dict):
        # Example: use 'eruption' prediction confidence to drive fear/stress
        eruption_prob = logic_prediction.get("eruption", 0.0)

        # Stimulate emotions based on event prediction
        self.emotions["fear"].adjust(eruption_prob)
        self.emotions["sadness"].adjust(eruption_prob * 0.5)
        self.emotions["joy"].adjust(-eruption_prob * 0.3)  # suppress joy under danger
        self.emotions["anger"].adjust(eruption_prob * 0.1)

        # Evaluate and normalize emotional state
        raw = get_emotion_vector()
        normalized = normalize_emotions(raw)

        # Optionally compute urgency modifier
        urgency_mod = 1.0 + normalized.get("fear", 0) + normalized.get("stress", 0.0)

        # Return blended signal
        result = {
            **normalized,
            "urgency_mod": round(urgency_mod, 2)
        }
        return result