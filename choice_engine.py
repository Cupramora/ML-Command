# choice_engine.py

class ChoiceEngine:
    def __init__(self, mood_engine, goal_stack, spark_engine):
        self.mood = mood_engine
        self.goals = goal_stack
        self.spark = spark_engine

    def decide(self):
        # 1. Check for active goal
        current_goal = self.goals.peek()
        if current_goal:
            if current_goal.is_atomic():
                return f"Execute: {current_goal.description}"
            else:
                self.goals.step()
                return f"Decomposing goal: {current_goal.description}"

        # 2. Check for spark
        spark_prompt = self.spark.maybe_spark()
        if spark_prompt:
            return f"Sparked reflection: {spark_prompt}"

        # 3. Mood-driven fallback
        dominant = self.mood.get_dominant_mood()
        if dominant == "curiosity":
            return "Wander and observe"
        elif dominant == "melancholy":
            return "Reflect on recent memory"
        elif dominant == "trust":
            return "Engage with known entity"
        elif dominant == "anxiety":
            return "Seek safety or reduce input"

        return "Idle: No directive"
