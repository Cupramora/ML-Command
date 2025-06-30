# handler.py

from sight import scan_area
from panic import trigger_panic
from speak import say
from long_term_memory import LongTermMemory
from self_reasoning import run_self_reasoning
from social_mind import SocialMind
from strategic_reasoner import StrategicReasoner
from goal_stack import GoalStack
from planning_module import Plan  # lives in ML-Social

# initialize core systems
long_term = LongTermMemory()
social_mind = SocialMind()
goals = GoalStack()
reasoner = StrategicReasoner()
plans = {}  # holds plans by goal name

def handle_command(cmd):
    task = cmd.get("task", "").lower()

    if task == "reflect_on":
        tag = cmd.get("tag", "")
        results = long_term.search_by_tag(tag)
        if not results:
            say("memory_not_found", {"tag": tag, "mood": "confused"})
            return {"status": "no_match", "tag": tag}
        reflection = results[-1]["content"].get("context", "...")
        say("memory_recalled", {"tag": tag, "mood": "nostalgic"})
        return {
            "status": "success",
            "tag": tag,
            "reflection": reflection
        }

    elif task == "reason_about":
        goal_text = cmd.get("goal", "explore")
        context = cmd.get("context", "general")
        goal = goals.add_goal(goal_text)
        preview = reasoner.simulate_outcome(goal, context)
        return preview

    elif task == "plan_goal":
        goal_text = cmd.get("goal", "improve tone detection")
        steps = cmd.get("steps", [])
        plan = Plan(goal_text)
        for step in steps:
            plan.add_step(
                description=step.get("description", "unspecified"),
                condition=step.get("condition"),
                fallback=step.get("fallback")
            )
        plans[goal_text] = plan
        goals.add_goal(goal_text, priority=0.6)
        return {"status": "plan_created", "goal": goal_text, "step_count": len(plan.steps)}

    elif task == "next_plan_step":
        goal = cmd.get("goal")
        plan = plans.get(goal)
        if not plan:
            return {"status": "not_found", "reason": "no such plan"}
        step = plan.get_next_step()
        if step:
            return {"status": "next_step", "description": step.description}
        else:
            return {"status": "complete", "message": "all steps complete"}

    elif task == "scan_area":
        return scan_area(cmd)

    elif task == "say":
        text = cmd.get("params", {}).get("line", "I'm listening.")
        mood = cmd.get("params", {}).get("mood", "neutral")
        say("task_received", {"task": text, "mood": mood})
        return {
            "type": "capsule",
            "status": "spoken",
            "summary": "Spoke line: " + text,
            "task": task
        }

    elif task == "trigger_panic_mode":
        return trigger_panic(cmd)

    return {
        "type": "capsule",
        "status": "failed",
        "summary": "Unrecognized task: " + task,
        "flags": {"unknown_command": True}
    }
