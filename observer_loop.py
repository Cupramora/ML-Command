# observer_loop.py

import os
import cv2
import time
import csv
import json

from speak import say

# YOLOv8 model loaded externally and passed in
from ultralytics import YOLO
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
label_dir = "labels"
os.makedirs(label_dir, exist_ok=True)

metadata_path = os.path.join(label_dir, "metadata_log.csv")
novelty_log_path = os.path.join(label_dir, "novelty_log.jsonl")

seen_classes = set()
frame_count = 0

# CSV setup
if not os.path.isfile(metadata_path):
    with open(metadata_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["frame", "timestamp", "num_detections", "classes", "avg_confidence"])
        writer.writeheader()

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Couldn't read from the camera.")
        break

    results = model(frame)[0]
    annotated_frame = results.plot()

    h, w = frame.shape[:2]
    image_path = os.path.join(label_dir, f"frame_{frame_count:05d}.jpg")
    label_path = os.path.join(label_dir, f"frame_{frame_count:05d}.txt")

    cv2.imwrite(image_path, frame)

    classes = []
    confidences = []

    with open(label_path, "w") as f:
        for box in results.boxes:
            cls_id = int(box.cls[0])
            x_center, y_center, bw, bh = box.xywh[0] / [w, h, w, h]
            confidence = float(box.conf[0])

            if confidence > 0.5:
                f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}\n")
                classes.append(cls_id)
                confidences.append(confidence)

                if cls_id not in seen_classes:
                    seen_classes.add(cls_id)
                    say("greeting", {"name": f"class_{cls_id}", "mood": "curious"})

                    # Log novelty to .jsonl
                    with open(novelty_log_path, "a") as novelty_log:
                        json.dump({
                            "timestamp": time.time(),
                            "frame": frame_count,
                            "new_class": cls_id,
                            "confidence": confidence
                        }, novelty_log)
                        novelty_log.write("\n")

    # Metadata logging
    with open(metadata_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["frame", "timestamp", "num_detections", "classes", "avg_confidence"])
        writer.writerow({
            "frame": frame_count,
            "timestamp": time.time(),
            "num_detections": len(classes),
            "classes": str(classes),
            "avg_confidence": sum(confidences)/len(confidences) if confidences else 0
        })

    cv2.imshow("Brainstem Vision", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(" Detection loop shutdown.")
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()