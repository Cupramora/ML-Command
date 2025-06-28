# sim_single_impression.py
# Simulates a single frame input for SensorHub testing

import vision_bootstrap
vision_bootstrap.ensure_packages()

from sight import detect_from_file
from perception import PerceptionCapsule, process_capsule
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

    # Compose cognitive capsule
    perceptual_capsule = PerceptionCapsule(
        stimulus={"detected": [d["label"] for d in detections]},
        emotion_vector={"curiosity": 0.2, "awe": 0.15},  # tweak freely
        behavior="observe",
        context=f"Detected: {[d['label'] for d in detections]}",
        feedback="neutral",
        reinforcement=0.3
    )

    result = process_capsule(perceptual_capsule)

    print("\n Cognitive Outcome:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "guess1.png")  # Updated filename here
    run_simulated_impression(image_path, known_labels=["person", "wall"])
