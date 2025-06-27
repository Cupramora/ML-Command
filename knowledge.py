# knowledge.py

import os
import json
import time
from command_display import log_categorization, log_correction

ENCYCLOPEDIA_ROOT = "encyclopedia"

def store_visual_concept(concept: str, capsule_data: dict, is_new: bool = False):
    base_dir = os.path.join(
        ENCYCLOPEDIA_ROOT,
        concept if not is_new else f"tentative_{concept}"
    )
    os.makedirs(base_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    uid = f"{concept}_{timestamp}"
    img_path = capsule_data.get("stimulus", {}).get("image_path", "unknown.jpg")

    summary = {
        "uid": uid,
        "timestamp": timestamp,
        "label": concept,
        "flags": capsule_data.get("flags", {}),
        "confidence": capsule_data.get("behavior_confidence", 0.0),
        "mood": capsule_data.get("capsule", {}).get("emotion_vector", {}),
        "source": capsule_data.get("capsule", {}).get("stimulus", {}).get("source", "unknown"),
        "image_path": img_path
    }

    # Save metadata next to image
    metadata_path = os.path.join(base_dir, f"{uid}.json")
    with open(metadata_path, "w") as f:
        json.dump(summary, f, indent=2)

    # Log to command display
    log_categorization(
        concept=concept,
        image_path=img_path,
        confidence=summary["confidence"],
        flags=summary["flags"],
        source=summary["source"],
        user_corrected=False
    )

    return summary

def apply_user_correction(old_concept: str, new_concept: str, image_path: str, reason: str, user: str = "Dane"):
    # Move the image and metadata
    os.makedirs(os.path.join(ENCYCLOPEDIA_ROOT, new_concept), exist_ok=True)

    base_filename = os.path.basename(image_path).rsplit(".", 1)[0]
    old_folder = os.path.dirname(image_path)
    new_folder = os.path.join(ENCYCLOPEDIA_ROOT, new_concept)

    for ext in [".jpg", ".json"]:
        old_path = os.path.join(old_folder, base_filename + ext)
        new_path = os.path.join(new_folder, base_filename + ext)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    # Log the correction
    log_correction(
        old_label=old_concept,
        new_label=new_concept,
        image_path=os.path.join(new_folder, base_filename + ".jpg"),
        reason=reason,
        user=user
    )