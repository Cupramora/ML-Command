# dream_reflections.py
# Symbolic memory reflection core with strategic feedback overlay (ML-Command only)

from Toolbox.reflection_core import DreamReflections  # shared logic
from self_model import self_model  # local introspection tracking

def reflect_on_recent(reflections: DreamReflections):
    from perception import process_capsule, PerceptionCapsule  # lazy import to avoid circular conflict

    recent = reflections.get_recent_reflection()
    if not recent:
        return None

    # strategic confidence evaluation
    if recent.get("strategy"):
        conf = recent["strategy"].get("confidence", 0.5)
        if conf < 0.3:
            self_model.record_failure("low_confidence_" + recent["summary"])

    # symbolic capsule injection
    capsule = PerceptionCapsule(
        stimulus={"source": "internal", "memory_reference": recent["summary"]},
        emotion_vector={recent["emotion"]: recent["amplified"] * 0.5},
        behavior="reflect",
        context=recent["summary"],
        feedback="internal",
        reinforcement=0.05
    )
    result = process_capsule(capsule)
    print(" Dream Reflection Injected:", result["capsule"]["context"])
    return result
