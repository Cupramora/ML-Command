# voice.py

import random

def generate_voice_line(intent: str, context: dict = {}) -> str:
    # Simple emotional modifiers
    mood = context.get("mood", "neutral")
    task = context.get("task", "something")
    name = context.get("name", "Dane")

    templates = {
        "task_received": {
            "neutral": [f"Command '{task}' received.", f"Task noted: {task}."],
            "curious": [f"Hmm, '{task}'—let's see what that is.", f"I’m on it: {task}."],
            "joyful": [f"Yay! New task: {task}!", f"Ooh, {task}? Let’s do this."]
        },
        "task_completed": {
            "neutral": [f"Task '{task}' complete.", f"{task} finished."],
            "confident": [f"All done with '{task}'. Nailed it.", f"{task}—wrapped and done."],
            "humble": [f"I did my best on '{task}'.", f"{task} completed… I hope that helped."]
        },
        "greeting": {
            "neutral": [f"Hello, {name}.", "Ready for instructions."],
            "joyful": [f"Hey hey, {name}!", f"So good to see you."]
        },
        "error": {
            "neutral": ["I didn’t catch that.", "There was a hiccup."],
            "anxious": ["Something's not right…", "I think I messed up."]
        }
    }

    phrase_list = templates.get(intent, {}).get(mood, [])
    if not phrase_list:
        # Fallback to neutral/default phrasing
        phrase_list = templates.get(intent, {}).get("neutral", [f"{intent}..."])

    return random.choice(phrase_list)
