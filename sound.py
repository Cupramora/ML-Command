# sound.py

import sounddevice as sd
import numpy as np

def listen(duration=2, samplerate=44100):
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    volume = np.linalg.norm(audio) / len(audio)
    return {"volume": volume}