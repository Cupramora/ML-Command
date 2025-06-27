# command_display.py

import os
import json
import time

LOG_FILE = "categorization_log.jsonl"

def log_categorization(concept, image_path, confidence, flags=None, source="observer_loop", user_corrected=False):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "concept": concept,
        "image_path": image_path,
        "confidence": round(confidence, 3),
        "flags": flags or [],
        "source": source,
        "user_corrected": user_corrected
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"[CommandDisplay] Logged: {concept} ({confidence*100:.1f}%)")

def log_correction(old_label, new_label, image_path, reason, user="Dane"):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "action": "reclassified",
        "from": old_label,
        "to": new_label,
        "image_path": image_path,
        "reason": reason,
        "user": user
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"[CommandDisplay] Correction logged: {old_label} -> {new_label}")
