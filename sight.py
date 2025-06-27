# sight.py

import vision_bootstrap
vision_bootstrap.ensure_packages()

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # preload once for both functions

def capture_and_detect():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    results = model(frame)
    return results

def detect_from_file(image_path):
    # Loads an image file (e.g., chair_frame.png) and runs detection
    results = model.predict(source=image_path, save=False, stream=True)
    return results