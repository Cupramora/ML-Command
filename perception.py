# perception.py

import time
from capsule_flagger import flag_capsule
from state_manager import StateManager
from expansion_tracker import suggest_expansion
from short_term import ShortTermMemory
from dream_reflections import DreamReflections

def process_capsule(capsule):
    flags = capsule.get("flags", {})
    summary = capsule.get("summary", "").lower()

    if "missing_visual_context" in flags:
        suggest_expansion(
            reason="Visual data incomplete during scan.",
            suggestion="Add infrared or low-light camera.",
            severity="moderate"
        )

    if "terrain_mismatch" in flags and "mobility" in capsule.get("capsule_type", ""):
        suggest_expansion(
            reason="Chassis unsuitable for local terrain.",
            suggestion="Enhance mobility or request hover module.",
            severity="high"
        )
class PerceptionCapsule:
    def __init__(self, stimulus, emotion_vector, behavior, context, feedback, reinforcement):
        self.timestamp = time.time()
        self.stimulus = stimulus                  # e.g. {"caller": "Dane", "gesture": "high_five"}
        self.emotion_vector = emotion_vector      # e.g. {"joy": 0.7}
        self.behavior = behavior                  # e.g. "come_when_called"
        self.context = context                    # e.g. "Dane beckoned, then offered high five"
        self.feedback = feedback                  # e.g. "positive"
        self.reinforcement = reinforcement        # e.g. 0.4

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "stimulus": self.stimulus,
            "emotion_vector": self.emotion_vector,
            "behavior": self.behavior,
            "context": self.context,
            "feedback": self.feedback,
            "reinforcement": self.reinforcement
        }
from emotional_state import EmotionalState
from reinforcement_logger import ReinforcementLogger
from behavioral_cognition import BehaviorInterpreter

# Initialize modules (or pass them in later)
emotional_state = EmotionalState()
reinforcement = ReinforcementLogger()
behavior_engine = BehaviorInterpreter()
state_manager = StateManager()

def process_capsule(capsule: PerceptionCapsule):
    # 1. Update emotion
    for emotion, value in capsule.emotion_vector.items():
        emotional_state.update_emotion(emotion, value)

    # 2. Flag capsule
    flags = flag_capsule(capsule)
    capsule.flags = flags

    # 3. Evaluate state
    wake_trigger = {
        "type": "sound" if "audio" in capsule.stimulus else "motion"
    }

    if flags.get("emotional_spike") or flags.get("novelty"):
        state_manager.evaluate_state(internal_drive={"novelty_detected": True})
    else:
        state_manager.evaluate_state(stimulus=wake_trigger)

    # 4. Log feedback
    dom_emotion = list(capsule.emotion_vector.keys())[0]
    dom_intensity = capsule.emotion_vector[dom_emotion]
    reinforcement.log_feedback(
        emotion=dom_emotion,
        intensity=dom_intensity,
        behavior=capsule.behavior,
        context=capsule.context,
        feedback=capsule.feedback,
        reinforcement=capsule.reinforcement
    )

    # 5. Form cognitive state
    cognitive_state = {
        "emotional_vector": capsule.emotion_vector,
        "prediction_vector": {},
        "mood": "default",
        "urgency_mod": 1.0,
        "confidence": reinforcement.get_confidence(capsule.behavior)
    }

    directive = behavior_engine.filter_state(cognitive_state)
    reflexes = behavior_engine.fallback_emotional_response(emotional_state)

    return {
        "capsule": capsule.to_dict(),
        "directive": directive,
        "reflexes": reflexes,
        "behavior_confidence": cognitive_state["confidence"],
        "flags": flags,
        "state": state_manager.state
    }

