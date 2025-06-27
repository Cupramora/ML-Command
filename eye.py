from sight import capture_and_detect

def process_vision(known_labels):
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