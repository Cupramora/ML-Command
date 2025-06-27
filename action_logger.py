# action_logger.py

import time

class ActionLogger:
    def __init__(self, stm, ltm):
        self.stm = stm
        self.ltm = ltm

    def log_attempt(self, action_name, parameters, result, emotion_vector=None, reinforcement=0.0):
        capsule = self._build_capsule(action_name, parameters, result, emotion_vector, reinforcement)
        self.stm.add_capsule(capsule)

        if self.ltm._is_promotable(capsule):
            self.ltm.store_capsule(capsule)

    def _build_capsule(self, action_name, parameters, result, emotion_vector, reinforcement):
        from perception import PerceptionCapsule  # Assuming existing structure
        return PerceptionCapsule(
            stimulus={
                "action": action_name,
                "parameters": parameters,
                "result": result,
                "novelty_score": 0.6,
                "clarity": 0.8,
                "attention": 0.5
            },
            emotion_vector=emotion_vector or {"curiosity": 0.3},
            behavior="attempted_action",
            context=f"Tried '{action_name}' with result: {result}",
            feedback="positive" if reinforcement > 0 else "neutral",
            reinforcement=reinforcement
        )
