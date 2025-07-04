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
from self_reasoning import run_self_reasoning
from social_mind import SocialMind
from strategic_reasoner import StrategicReasoner
from goal_stack import GoalStack

# initialize modules
short_term = ShortTermMemory()
dream_state = DreamReflections()
state_manager = StateManager(short_term, dream_state)
emotional_state = EmotionalState()
reinforcement = ReinforcementLogger()
behavior_engine = BehaviorInterpreter()
social_context = SocialMind()
reasoner = StrategicReasoner(emotional_state)
goal_stack = GoalStack()

class PerceptionCapsule:
    def __init__(self, stimulus, emotion_vector, behavior, context, feedback, reinforcement):
        self.timestamp = time.time()
        self.stimulus = stimulus
        self.emotion_vector = emotion_vector
        self.behavior = behavior
        self.context = context
        self.feedback = feedback
        self.reinforcement = reinforcement
        self.flags = {}
        self.social_insight = {}
        self.goal_preview = {}

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "stimulus": self.stimulus,
            "emotion_vector": self.emotion_vector,
            "behavior": self.behavior,
            "context": self.context,
            "feedback": self.feedback,
            "reinforcement": self.reinforcement,
            "flags": self.flags,
            "social_insight": self.social_insight,
            "goal_preview": self.goal_preview
        }

def process_capsule(capsule: PerceptionCapsule):
    for emotion, value in capsule.emotion_vector.items():
        emotional_state.update_emotion(emotion, value)

    flags = flag_capsule(capsule)
    capsule.flags = flags

    social_result = social_context.evaluate_capsule_socially(capsule, agent="dane")
    capsule.social_insight = social_result

    short_term.add_capsule(capsule)

    wake_trigger = {
        "type": "sound" if "audio" in capsule.stimulus else "motion"
    }

    top_goal = goal_stack.get_top_goal()
    if top_goal:
        strategy = reasoner.simulate_outcome(top_goal, capsule.context)
        capsule.goal_preview = strategy

        if strategy["confidence"] < 0.4:
            top_goal.demote(0.1)
        elif strategy["confidence"] > 0.8:
            top_goal.promote(0.05)

        # log strategy into dream reflections
        dream_state.log_dream({
            "summary": capsule.context,
            "emotion": list(capsule.emotion_vector.keys())[0],
            "amplified": list(capsule.emotion_vector.values())[0],
            "mood": social_result.get("suggested_mood", "neutral"),
            "strategy": strategy
        })

    if flags.get("emotional_spike") or flags.get("novelty"):
        state_manager.evaluate_state(internal_drive={"novelty_detected": True})
    else:
        state_manager.evaluate_state(stimulus=wake_trigger)

    if capsule.emotion_vector.get("guilt", 0) > 0.6 or capsule.behavior == "ruminate":
        run_self_reasoning()

    dom_emotion = list(capsule.emotion_vector.keys())[0]
    dom_intensity = capsule.emotion_vector[dom_emotion]
    reinforcement.log_feedback(
        emotion=dom_emotion,
        intensity=dom_intensity,
        behavior=capsule.behavior,
        context=capsule.context,
        feedback=capsule.feedback,
        reinforcement=capsule.reinforcement,
        mood=social_result["suggested_mood"]
    )

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
