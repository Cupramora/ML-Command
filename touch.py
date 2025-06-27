# touch.py

import time
import random  # placeholder for real sensor input

def get_accelerometer_data():
    # Placeholder: Replace with real sensor polling
    return {
        "x": random.uniform(-1, 1),
        "y": random.uniform(-1, 1),
        "z": random.uniform(-1, 1)
    }

def interpret_motion(data):
    magnitude = (data["x"]**2 + data["y"]**2 + data["z"]**2) ** 0.5
    if magnitude > 2.5:
        return {"event": "jostled", "intensity": magnitude, "emotion_hint": "startled"}
    elif magnitude < 0.2:
        return {"event": "still", "emotion_hint": "calm"}
    else:
        return {"event": "moving", "emotion_hint": "alert"}

def sense_touch():
    data = get_accelerometer_data()
    return interpret_motion(data)

# Example loop
if __name__ == "__main__":
    while True:
        sensation = sense_touch()
        print(f"[Touch] {sensation}")
        time.sleep(1)