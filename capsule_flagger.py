# capsule_flagger.py

def flag_capsule(capsule, personality_profile=None):
    flags = {}

    # Emotional spike detection
    max_emotion = max(capsule.emotion_vector.values())
    flags["emotional_spike"] = max_emotion >= 0.75

    # Promotion logic
    flags["promotable"] = (
        max_emotion >= 0.7 or
        capsule.reinforcement >= 0.3 or
        capsule.feedback == "positive"
    )

    # Trust bias (simplified for now)
    if "Dane" in capsule.context:
        flags["trust_bias"] = "positive"
    else:
        flags["trust_bias"] = "neutral"

    # Error margin: how much weirdness to tolerate
    if capsule.behavior == "yelling" and flags["trust_bias"] == "positive":
        flags["diagnostic_hint"] = "possible_mood_swing"
        flags["error_margin"] = 0.3
    else:
        flags["error_margin"] = 0.1

    # Novelty detection (placeholder)
    if capsule.stimulus.get("novelty_score", 0.5) > 0.7:
        flags["novelty"] = True
    else:
        flags["novelty"] = False

    return flags