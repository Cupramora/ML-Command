# test_brain_boot.py
from perception import PerceptionCapsule, process_capsule

# Create the capsule
capsule = PerceptionCapsule(
    stimulus={"caller": "Dane", "gesture": "high_five"},
    emotion_vector={"joy": 0.72},
    behavior="come_when_called",
    context="Dane called her over and gave a high five",
    feedback="positive",
    reinforcement=0.4
)

# Process the capsule through the brain
response = process_capsule(capsule)

# Print the results
print("\n Capsule:")
print(response["capsule"])

print("\n Behavior Directive:")
print(response["directive"])

print("\n Reflex Responses:")
print(response["reflexes"])

print("\n Confidence Score for 'come_when_called':")
print(response["behavior_confidence"])