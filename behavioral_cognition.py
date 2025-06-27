# behavior_cognition.py

from behavior_pid import BehaviorPID
from emotional_state import EmotionalState
from command_responses import command_responses
from reinforcement_logger import ReinforcementLogger


class BehaviorInterpreter:
    def __init__(self):
        self.pid_filter = BehaviorPID(
            behavior_types=["playful", "snarky", "guarded", "supportive", "withdrawn"]
        )
        self.reinforcement = ReinforcementLogger()  # ✅ moved into __init__

    def filter_state(self, cognitive_state, traits={}):
        emotions = cognitive_state.get("emotional_vector", {})
        logic = cognitive_state.get("prediction_vector", {})
        mood = cognitive_state.get("mood", "neutral")
        urgency = cognitive_state.get("urgency_mod", 1.0)

        behavior_style, style_vector = self.pid_filter.compute(
            current_emotion=emotions,
            mood_vector={},  # Optional for now
            traits=traits
        )

        fear = emotions.get("fear", 0)
        danger = logic.get("threat", logic.get("eruption", 0))
        anger = emotions.get("anger", 0)
        confidence = cognitive_state.get("confidence", 0.5)

        if fear > 0.75 and danger > 0.85:
            return {
                "directive": "retreat_now",
                "intensity": "max",
                "mode": "reflexive",
                "style": behavior_style,
                "justification": "Instinctive override: threat + fear spike"
            }

        if anger > 0.5 and danger < 0.4:
            return {
                "directive": "pause_and_scan",
                "intensity": "moderate",
                "mode": "tempered",
                "style": "guarded",
                "justification": "Anger spike suppressed: no logical support"
            }

        if fear < 0.3 and danger < 0.2:
            return {
                "directive": "observe",
                "intensity": "low",
                "mode": "calm",
                "style": behavior_style,
                "justification": f"Mood '{mood}' confirmed by low threat"
            }

        return {
            "directive": "monitor",
            "intensity": "baseline",
            "mode": "attentive",
            "style": behavior_style,
            "style_weights": style_vector,
            "justification": "No reflex triggered; PID-style modulation applied"
        }

    def fallback_emotional_response(self, state: EmotionalState):
        tiers = state.get_all_tiers()
        reflexes = {}

        for emotion, tier in tiers.items():
            options = command_responses.get(emotion, ["idle"])
            candidate = options[tier]

            weight = self.reinforcement.get_behavior_weight(candidate)
            if weight < -0.5:
                reflexes[emotion] = "suppress_response"
            else:
                reflexes[emotion] = candidate

        return reflexes