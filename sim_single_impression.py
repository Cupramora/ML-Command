# sim_single_impression.py
# Simulates a single frame input for SensorHub testing

import vision_bootstrap
vision_bootstrap.ensure_packages()

from sight import detect_from_file
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def run_simulated_impression(image_path, known_labels):
    print(f"[Debug] Looking for image at: {image_path}")
    if not os.path.exists(image_path):
        print(f"[Error] File not found: {image_path}")
        return

    results = detect_from_file(image_path)
    detections = []

    for r in results:
        for box in r.boxes:
            label = r.names[int(box.cls)]
            if label not in known_labels:
                detections.append({
                    "label": label,
                    "confidence": float(box.conf)
                })

    capsule = {
        "type": "visual_impression",
        "origin": "sim_camera",
        "capsule_id": "sim-001",
        "timestamp": "now",
        "payload": detections
    }

    print(json.dumps(capsule, indent=2))

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "chair_frame.png")
    run_simulated_impression(image_path, known_labels=["person", "wall"])
