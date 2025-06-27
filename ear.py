from sound import listen

def process_audio(threshold=0.2):
    data = listen()
    if data["volume"] > threshold:
        return {"event": "loud_noise", "intensity": data["volume"]}
    return {"event": "ambient", "intensity": data["volume"]}