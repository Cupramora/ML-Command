# eye.py

from sight import capture_and_detect, detect_from_file

def process_vision(known_labels, simulate=False, sim_path=None):
    if simulate and sim_path:
        print(f"[SIM] Running simulated perception on: {sim_path}")
        results = detect_from_file(sim_path)
    else:
        results = capture_and_detect()

    if results is None:
        return {"status": "no_frame"}

    detections = []
    for r in results:
        for box in r.boxes:
            label = r.names[int(box.cls)]
            if label not in known_labels:
                detections.append({"label": label, "confidence": float(box.conf)})

    return {"new_objects": detections}
