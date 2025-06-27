import os
import cv2
import time
import csv

# Output directory for labels
label_dir = "labels"
os.makedirs(label_dir, exist_ok=True)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Couldn't read from the camera.")
        break

    results = model(frame)[0]
    annotated_frame = results.plot()

    # Save the raw frame image
    image_path = os.path.join(label_dir, f"frame_{frame_count:05d}.jpg")
    cv2.imwrite(image_path, frame)

    # Save labels for each frame
    h, w = frame.shape[:2]
    label_path = os.path.join(label_dir, f"frame_{frame_count:05d}.txt")
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

    # Log metadata
    metadata_path = os.path.join(label_dir, "metadata_log.csv")
    log_exists = os.path.isfile(metadata_path)

    with open(metadata_path, "a", newline="") as csvfile:
        fieldnames = ["frame", "timestamp", "num_detections", "classes", "avg_confidence"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not log_exists:
            writer.writeheader()
        writer.writerow({
            "frame": frame_count,
            "timestamp": time.time(),
            "num_detections": len(classes),
            "classes": str(classes),
            "avg_confidence": sum(confidences)/len(confidences) if confidences else 0
        })

    # Show annotated frame
    cv2.imshow("Brainstem Vision", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(" Shutting down detection loop.")
        break

    frame_count += 1