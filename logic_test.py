from logic import LogicalLobe

logic = LogicalLobe()

# Simulate observations
logic.observe(
    description="Mountain with smoke + high temp",
    features={"shape": "cone", "smoke": True, "temp": "high"},
    outcome="eruption"
)

logic.observe(
    description="Mountain with no smoke",
    features={"shape": "cone", "smoke": False, "temp": "normal"},
    outcome="no_event"
)

# Now simulate a new scenario and predict outcome
new_features = {"shape": "cone", "smoke": True, "temp": "high"}
prediction = logic.predict_outcome(new_features)

print("Prediction:", prediction)