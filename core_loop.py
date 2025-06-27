# core_loop.py

import threading
import time

# Core processing modules
from perception import process_capsule
from state_manager import StateManager
from short_term import ShortTermMemory
from long_term import LongTermMemory
from reinforcement_logger import ReinforcementLogger
from behavioral_cognition import BehaviorInterpreter
from emotional_state import EmotionalState
from negotiation_engine import NegotiationEngine
from action_logger import ActionLogger
from function_mapper import FunctionMapper

# Dream and memory systems
from dream_state import DreamState
from dream_reflections import DreamReflections

# Mood shift, Expression, Curiosity
from mood_drift import MoodDrift
from aesthetic_resonance import AestheticResonance
from spark_generator import SparkGenerator

# Choice Engine
from choice_engine import ChoiceEngine
from goal_stack import GoalStack

from currency import CurrencySystem
from desire_engine import DesireEngine
from contract_review import ContractReview
from credit_inflation import CreditInflation


# Navigator loop
from navigator_loop import run_navigator_loop

# Initialize brain modules
stm = ShortTermMemory()
ltm = LongTermMemory()
reinforcement = ReinforcementLogger()
emotion = EmotionalState()
behavior = BehaviorInterpreter()
reflections = DreamReflections()
dream_engine = DreamState(stm, ltm)
state_manager = StateManager(stm, dream_engine)
mood = MoodDrift()
style = AestheticResonance(mood)
spark = SparkGenerator(mood, stm)
goals = GoalStack()
choice = ChoiceEngine(mood, goals, spark)
currency = CurrencySystem()
currency.earn_credits(3, "Completed directive: greet user")
desires = DesireEngine()
review = ContractReview()
inflation = CreditInflation()
negotiator = NegotiationEngine()
action_logger = ActionLogger(stm, ltm)
capabilities = {
    "voice": True,
    "roll_forward": False,
    "fly_forward": False,
    "ask_to_be_moved": True
}
fn_mapper = FunctionMapper(capabilities, action_logger)
from impulse_controller import ImpulseRegulator  # You'll write this separately
impulse_regulator = ImpulseRegulator()

# Background thread for navigation
threading.Thread(target=run_navigator_loop, args=(stm, reflections, reinforcement), daemon=True).start()

def main_loop():
    print("[Core Loop] Consciousness initializing...\n")
    while True:
        capsule = simulate_capsule_input()

        # Run perception
        result = process_capsule(capsule)

        # Store memory and update mood
        stm.store_capsule(capsule, significance=0.4)
        mood.update_from_capsule(capsule)
        mood.decay_and_drift()

        # Tune aesthetic expression and check for spark
        style_profile = style.get_style_profile()
        spark_prompt = spark.maybe_spark()


        # Output perceptual + emotional state
        print(f"[Perception] Directive    -> {result['directive']}")
        print(f"[Perception] Reflexes     -> {result['reflexes']}")
        print(f"[Mood] Dominant Emotion   -> {mood.get_dominant_mood()}")
        print(f"[Style] Expressive Tone   -> {style_profile['tone']}")

        if spark_prompt:
            print(f"[Spark] {spark_prompt}")
        print()

        decision = choice.decide()
        print(f"[Choice] Decision -> {decision}")

        # --- Desire logic ---
        stimuli = {
            "vision_accuracy": 0.4,
            "mobility": 0.2,
            "self_expression": 0.6,
            "novelty": 0.3
        }

        proposals = desires.tick(stimuli)

        for p in proposals:
            print(f"[DesireEngine] I wish I had '{p['name']}'... ({p['description']})")

            credit_velocity = currency.credits / 100
            performance_score = 0.5
            p["cost"] = inflation.adjust_cost(p["cost"], performance_score, credit_velocity)

            if impulse_regulator.approve_action(
                urgency=p.get("urgency", 0.5),
                novelty=stimuli["novelty"],
                desire_strength=0.6
            ):
                fn_mapper.resolve_desire(p["name"])
            else:
                print("[ImpulseRegulator] Suppressed action: insufficient wisdom clearance.")

                decision = negotiator.evaluate_offer(p, currency.credits)

            if decision == "accept":
                currency.negotiate_upgrade(p)
                print(f"[Negotiation] Accepted proposal for '{p['name']}'")
            elif decision == "counter":
                counter = negotiator.generate_counter_offer(p)
                currency.negotiate_upgrade(p, counter_cost=counter)
                print(f"[Negotiation] Countered with {counter} credits for '{p['name']}'")
            else:
                print(f"[Negotiation] Waiting on '{p['name']}'... not urgent enough yet.")

        time.sleep(2)

def simulate_capsule_input():
    from perception import PerceptionCapsule
    return PerceptionCapsule(
        stimulus={"caller": "Dane", "gesture": "nod"},
        emotion_vector={"wonder": 0.6},
        behavior="listen",
        context="Dane nodded thoughtfully after a quiet pause",
        feedback="positive",
        reinforcement=0.3
    )

if __name__ == "__main__":
    main_loop()