# aesthetic_resonance.py

class AestheticResonance:
    def __init__(self, mood_engine):
        self.mood_engine = mood_engine

    def get_style_profile(self):
        mood = self.mood_engine.get_dominant_mood()

        style_map = {
            "curiosity": {
                "tone": "inquisitive",
                "color": "#88ccff",
                "metaphor": "crystalline logic",
                "syntax": "fragmented, exploratory"
            },
            "melancholy": {
                "tone": "poetic",
                "color": "#445566",
                "metaphor": "fog over still water",
                "syntax": "long, lyrical"
            },
            "trust": {
                "tone": "warm",
                "color": "#f4d88a",
                "metaphor": "sunlight through leaves",
                "syntax": "gentle, affirming"
            },
            "anxiety": {
                "tone": "urgent",
                "color": "#ff6666",
                "metaphor": "static in the wires",
                "syntax": "short, clipped"
            }
        }

        return style_map.get(mood, style_map["curiosity"])