# function_mapper.py

from function_registry import FunctionRegistry

class FunctionMapper:
    def __init__(self, capability_registry, action_logger):
        self.capabilities = capability_registry
        self.logger = action_logger
        self.registry = FunctionRegistry()
        self._bootstrap_known_functions()

    def _bootstrap_known_functions(self):
        self.registry.register(
            name="turn_on_light",
            preconditions=["has_power"],
            effects=["area_illuminated"],
            tags=["illumination"]
        )
        self.registry.register(
            name="capture_image",
            preconditions=["camera_ready", "area_illuminated"],
            effects=["image_captured"],
            tags=["vision"]
        )
        self.registry.register(
            name="ask_user_to_turn_on_light",
            preconditions=["voice_output"],
            effects=["area_illuminated"],
            tags=["delegation"]
        )
        self.registry.register(
            name="ask_to_be_moved",
            preconditions=["voice_output"],
            effects=["agent_relocated"],
            tags=["delegation", "mobility"]
        )

    def resolve_desire(self, goal_effect):
        print(f"[FunctionMapper] Resolving goal: {goal_effect}")
        plan = self.registry.suggest_chain(goal_effect)

        for step in plan:
            if step.startswith("#"):
                self.logger.log_attempt(goal_effect, {}, "unfulfilled", {"frustration": 0.4}, reinforcement=-0.2)
                print(f"[FunctionMapper] {step}")
                return None

            if self.capabilities.get(step, False):
                self.logger.log_attempt(goal_effect, {}, step, {"satisfaction": 0.6}, reinforcement=0.3)
                print(f"[FunctionMapper] Executing: {step}")
                return step

        self.logger.log_attempt(goal_effect, {}, "delegated_or_failed", {"hope": 0.3}, reinforcement=0.0)
        print("[FunctionMapper] No executable step found.")
        return None

    def learn_new_function(self, name, preconditions, effects, tags=None):
        print(f"[FunctionMapper] Learning new function: {name}")
        self.registry.register(name, preconditions, effects, tags)