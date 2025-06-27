# speak.py

import time
from voice import generate_voice_line  # Core brain generates how to say it

VOICE_LOG = "voice_output_log.txt"

def say(intent: str, context: dict = {}):
    line = generate_voice_line(intent, context)
    timestamp = time.strftime("[%H:%M:%S] ", time.localtime())
    full_line = timestamp + line

    # Log output
    with open(VOICE_LOG, "a", encoding="ascii", errors="replace") as f:
        f.write(full_line + "\n")

    # Local echo (drone console)
    print("[Drone Voice]", line)

    # Optional future: pipe to pyttsx3 or external speaker
    # speak_aloud(line)
