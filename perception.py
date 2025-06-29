# perception.py

import time
from capsule_flagger import flag_capsule
from state_manager import StateManager
from expansion_tracker import suggest_expansion
from short_term import ShortTermMemory
from dream_reflections import DreamReflections
from emotional_state import EmotionalState
from reinforcement_logger import ReinforcementLogger
from behavioral_cognition import BehaviorInterpreter
from self_reasoning import run_self_reasoning  # <-- introspection loop
from social_mind import SocialMind

# Initialize modules
short_term = ShortTermMemory()
dream_state = DreamReflections()
state_manager = StateManager(short_term, dream_state)
emotional_state = EmotionalState()
reinforcement = ReinforcementLogger()
behavior_engine = BehaviorInterpreter()
social_context = SocialMind()

class PerceptionCapsule:
    def __init__(self, stimulus, emotion_vector, behavior, context, feedback, reinforcement):
        self.timestamp = time.time()
        self.stimulus = stimulus
        self.emotion_vector = emotion_vector
        self.behavior = behavior
        self.context = context
        self.feedback = feedback
        self.reinforcement = reinforcement

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

def process_capsule(capsule: PerceptionCapsule):
    # 1. Update emotional state
    for emotion, value in capsule.emotion_vector.items():
        emotional_state.update_emotion(emotion, value)

    # 2. Flag capsule and add flags
    flags = flag_capsule(capsule)
    capsule.flags = flags

    # 3. Store in short-term memory
    short_term.add_capsule(capsule)

    # 4. Evaluate state
    wake_trigger = {
        "type": "sound" if "audio" in capsule.stimulus else "motion"
    }

    if flags.get("emotional_spike") or flags.get("novelty"):
        state_manager.evaluate_state(internal_drive={"novelty_detected": True})
    else:
        state_manager.evaluate_state(stimulus=wake_trigger)

    # 5. Reflect if introspective signal present
    if capsule.emotion_vector.get("guilt", 0) > 0.6 or capsule.behavior == "ruminate":
        run_self_reasoning()

    # 6. Log reinforcement feedback
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

    # 7. Generate cognitive state
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
