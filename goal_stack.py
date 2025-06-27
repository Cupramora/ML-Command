# goal_stack.py

class Goal:
    def __init__(self, description, subgoals=None, completed=False):
        self.description = description
        self.subgoals = subgoals or []
        self.completed = completed

    def is_atomic(self):
        return len(self.subgoals) == 0

    def __repr__(self):
        return f"<Goal: {self.description}>"

class GoalStack:
    def __init__(self):
        self.stack = []

    def push(self, goal):
        print(f"[GoalStack] Pushed goal: {goal.description}")
        self.stack.append(goal)

    def pop(self):
        if self.stack:
            goal = self.stack.pop()
            print(f"[GoalStack] Completed goal: {goal.description}")
            return goal
        return None

    def peek(self):
        return self.stack[-1] if self.stack else None

    def step(self):
        if not self.stack:
            return None

        current = self.peek()

        if current.is_atomic():
            current.completed = True
            return self.pop()

        # Decompose into subgoals
        if current.subgoals:
            next_subgoal = current.subgoals.pop(0)
            self.push(next_subgoal)
        return None
