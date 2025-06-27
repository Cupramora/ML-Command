# handler.py

from sight import scan_area
from panic import trigger_panic
from speak import say

def handle_command(cmd):
    task = cmd.get("task", "").lower()

    # Vision task
    if task == "scan_area":
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
