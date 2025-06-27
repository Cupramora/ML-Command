# mood.py

import time
from collections import deque

class Mood:
    def __init__(self, emotion_keys, window_seconds=86400):  # default: 24 hours
        self.current_mood = {k: 0.2 for k in emotion_keys}  # Neutral start
        self.history = deque()  # List of (timestamp, emotion_vector)
        self.window = window_seconds
        self.last_emotion = {k: 0.2 for k in emotion_keys}

    def update(self, new_emotion_vector, timestamp=None, smoothing=0.95):
        if timestamp is None:
            timestamp = time.time()

        # Log emotion input
        self.history.append((timestamp, new_emotion_vector.copy()))

        # Prune old logs
        cutoff = timestamp - self.window
        while self.history and self.history[0][0] < cutoff:
            self.history.popleft()

        # Smooth update to current mood
        for k in self.current_mood:
            delta = new_emotion_vector[k] - self.last_emotion.get(k, 0.0)
            self.current_mood[k] = (smoothing * self.current_mood[k]) + ((1 - smoothing) * new_emotion_vector[k])
            self.last_emotion[k] = new_emotion_vector[k]

    def get_mood_vector(self):
        return self.current_mood.copy()

    def summarize_recent_flux(self):
        """Returns the average emotional vector over the last 24 hours."""
        if not self.history:
            return self.current_mood.copy()

        summary = {k: 0.0 for k in self.current_mood}
        for _, vector in self.history:
            for k in vector:
                summary[k] += vector[k]

        count = len(self.history)
        if count == 0:
            return self.current_mood.copy()

        return {k: v / count for k, v in summary.items()}
    def finalize_day_mood(self):
        """Compute and store the average mood vector for this 24h window."""
        summary = self.summarize_recent_flux()
        timestamp = time.time()
        daily_snapshot = {"timestamp": timestamp, "mood_vector": summary}
        
        if not hasattr(self, "daily_logs"):
            self.daily_logs = []

        self.daily_logs.append(daily_snapshot)

        # Optional: Save to file for persistence
        # with open("mood_logs.json", "a") as f:
        #     json.dump(daily_snapshot, f)
        #     f.write("\n")

        return daily_snapshot
