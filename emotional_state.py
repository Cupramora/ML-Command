# emotional_state.py

class EmotionalState:
    def __init__(self):
        self.emotions = {
            "joy": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "sadness": 0.0,
            "curiosity": 0.0
        }

    def update_emotion(self, emotion, value):
        self.emotions[emotion] = max(0.0, min(1.0, value))

    def get_emotion_tier(self, emotion):
        val = self.emotions.get(emotion, 0.0)
        if val < 0.2:
            return 0
        elif val < 0.4:
            return 1
        elif val < 0.6:
            return 2
        elif val < 0.8:
            return 3
        else:
            return 4

    def get_all_tiers(self):
        return {e: self.get_emotion_tier(e) for e in self.emotions}