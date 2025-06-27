# function_registry.py

class FunctionRegistry:
    def __init__(self):
        self.functions = {}

    def register(self, name, preconditions, effects, tags=None):
        self.functions[name] = {
            "preconditions": preconditions,
            "effects": effects,
            "tags": tags or []
        }

    def find_by_goal(self, desired_effect):
        matches = []
        for name, meta in self.functions.items():
            if desired_effect in meta["effects"]:
                matches.append((name, meta))
        return matches

    def suggest_chain(self, goal):
        # Naive chaining: find a function whose effect matches the goal,
        # then recursively satisfy its preconditions
        plan = []
        visited = set()

        def resolve(effect):
            if effect in visited:
                return
            visited.add(effect)
            matches = self.find_by_goal(effect)
            if not matches:
                plan.append(f"# No known function for: {effect}")
                return
            fn, meta = matches[0]
            for pre in meta["preconditions"]:
                resolve(pre)
            plan.append(fn)

        resolve(goal)
        return plan
