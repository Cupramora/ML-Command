# emotion_test.py

from logic import LogicalLobe
from emotion import EmotionalLobe

# Example observation: Volcano with eruption cues
observation = {
    "shape": "cone",
    "smoke": True,
    "temperature": "high"
}

# Initialize lobes
logic = LogicalLobe()
emotion = EmotionalLobe()

# Train logic with memory
logic.observe("volcano1", observation, "eruption")

# Run prediction
prediction = logic.predict_outcome(observation)

# Emotional response to that prediction
emotions = emotion.evaluate(prediction)

# Display results
print("\n--- Emotion Test Report ---")
print(f"Prediction: {prediction}")
print(f"Emotional State: {emotions}")

# Optional: Decide action based on emotion + logic fusion
def decide_behavior(pred, emo):
    urgency = pred.get("eruption", 0)
    fear = emo.get("fear", 0)
    mod = emo.get("urgency_mod", 1.0)

    score = urgency * mod
    if score > 0.8:
        return "Retreat and notify."
    elif score > 0.5:
        return "Enter watchful state."
    else:
        return "Remain in passive mode."

action = decide_behavior(prediction, emotions)
print(f"Behavioral Response: {action}")