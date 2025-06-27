# sight.py

import cv2
from ultralytics import YOLO

def capture_and_detect():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    model = YOLO("yolov8n.pt")
    results = model(frame)
    return results