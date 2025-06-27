# emotion_loop.py

import time
from emotion import emotions, get_emotion_vector, normalize_emotions

class EmotionLoop:
    def __init__(self):
        self.last_tick = time.time()
        self.state = normalize_emotions(get_emotion_vector())

    def tick(self):
        now = time.time()
        elapsed = now - self.last_tick
        self.last_tick = now

        # Step 1: Evaluate each emotion over time
        current_vector = get_emotion_vector()

        # Step 2: Normalize the raw emotional output
        self.state = normalize_emotions(current_vector)

        # Step 3: Do something with this emotional fingerprint
        self.output_state()

    def output_state(self):
        print(f"\n[Emotion Loop] Current normalized state:")
        for name, value in self.state.items():
            print(f"  {name.capitalize()}: {value:.3f}")

# Run the loop once (you can later thread this or loop it on your scheduler)
if __name__ == "__main__":
    loop = EmotionLoop()
    while True:
        loop.tick()
        time.sleep(1)  # You can reduce/increase tick rate based on reaction frequency
