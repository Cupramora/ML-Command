class CognitionCore:
    def __init__(self, logic_lobe, emotion_lobe):
        self.logic = logic_lobe
        self.emotion = emotion_lobe

    def process_impression(self, impression, environment={}):
        logic_result = self.logic.predict_outcome(impression)
        emotion_result = self.emotion.evaluate(logic_result)
        
        convergence = self.resolve_consensus(logic_result, emotion_result, environment)
        return convergence

    def resolve_consensus(self, logic, emotion, env):
        fear = emotion.get("fear", 0)
        confidence = logic.get("danger", logic.get("eruption", 0))
        visibility = env.get("visibility", 1.0)  # 0.0 to 1.0

        # Mild cognitive dissonance example:
        if fear > 0.7 and confidence < 0.3:
            return {
                "mood": "uneasy_vigilance",
                "behavior": "pause_and_scan",
                "note": "emotional alert not supported by logic"
            }
        
        # Harmonious convergence
        elif confidence > 0.7 and fear > 0.6:
            return {
                "mood": "threat_response",
                "behavior": "retreat_and_alert",
                "note": "both lobes confirm risk"
            }

        # Default: casual observation
        return {
            "mood": "relaxed_attention",
            "behavior": "observe",
            "note": "low threat across systems"
        }