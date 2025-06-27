# choice_test.py

from behavioral_cognition import BehaviorInterpreter
from choice import BehaviorSelector

# 1. Symbolic impression of the scene
scene_description = {
    "location": "white sand beach",
    "time": "night",
    "sky": "clear, full of stars",
    "soundscape": "gentle waves",
    "temperature": "warm breeze",
    "light_pollution": "low",
    "companionship": "alone but safe"
}

# 2. Emotional + cognitive state evoked by the scene
mock_state = {
    "emotional_vector": {
        "fear": 0.05,
        "joy": 0.85,
        "anger": 0.0,
        "curiosity": 0.4,
        "awe": 0.7,
        "sadness": 0.1
    },
    "prediction_vector": {
        "threat": 0.01,
        "eruption": 0.0,
        "novelty": 0.6
    },
    "mood": "serene",
    "urgency_mod": 0.1,
    "confidence": 0.9,
    "impression": scene_description  # Optional: pass symbolic context
}

# 3. Trait profile (optional personality flavor)
trait_profile = {
    "empathy": 0.7,
    "snark": 0.1,
    "boldness": 0.2,
    "imagination": 0.8
}

# 4. Interpret cognition into behavior
brain = BehaviorInterpreter()
behavior_plan = brain.filter_state(mock_state, traits=trait_profile)

# 5. Commit to the action with expressive output
selector = BehaviorSelector()
selector.commit_to_action(behavior_plan)