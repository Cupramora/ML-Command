# handler.py

from sight import scan_area
from panic import trigger_panic
from speak import say
from long_term_memory import LongTermMemory
from self_reasoning import run_self_reasoning

long_term = LongTermMemory()

def handle_command(cmd):
    task = cmd.get("task", "").lower()

    # Reflective memory recall
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

    # Self-reasoning loop
    elif task == "self_reason":
        return run_self_reasoning()

    # Vision task
    elif task == "scan_area":
        return scan_area(cmd)

    # Voice task
    elif task == "say":
        text = cmd.get("params", {}).get("line", "I'm listening.")
        mood = cmd.get("params", {}).get("mood", "neutral")
        say("task_received", {"task": text, "mood": mood})
        return {
            "type": "capsule",
            "status": "spoken",
            "summary": f"Spoke line: {text}",
            "task": task
        }

    # Emergency failsafe
    elif task == "trigger_panic_mode":
        return trigger_panic(cmd)

    # Unknown command
    return {
        "type": "capsule",
        "status": "failed",
        "summary": f"Unrecognized task: {task}",
        "flags": {"unknown_command": True}
    }
