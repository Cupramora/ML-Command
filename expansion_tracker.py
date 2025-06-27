# expansion_tracker.py

import time
import json

EXPANSION_LOG = "expansion_log.jsonl"

def suggest_expansion(reason: str, suggestion: str, severity: str = "moderate"):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "suggestion": suggestion,
        "reason": reason,
        "severity": severity,
        "acknowledged": False
    }

    with open(EXPANSION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"[Expansion Tracker] Suggestion logged: {suggestion}")
    return entry
