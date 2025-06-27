# logic.py

from collections import defaultdict
import datetime
import uuid

class LogicalLobe:
    def __init__(self):
        self.observation_log = []         # Raw incoming observations
        self.event_stats = defaultdict(lambda: {"count": 0, "outcomes": defaultdict(int)})
        self.patterns = {}                # Recognized probability patterns

    def observe(self, description, features, outcome=None):
        obs_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()

        observation = {
            "id": obs_id,
            "description": description,
            "features": features,  # e.g., {"shape": "cone", "smoke": True, "temp": "high"}
            "outcome": outcome,
            "timestamp": timestamp
        }

        self.observation_log.append(observation)
        self._update_stats(features, outcome)

        return obs_id

    def _update_stats(self, features, outcome):
        feature_key = tuple(sorted(features.items()))
        self.event_stats[feature_key]["count"] += 1

        if outcome:
            self.event_stats[feature_key]["outcomes"][outcome] += 1

    def predict_outcome(self, features):
        feature_key = tuple(sorted(features.items()))
        if feature_key in self.event_stats:
            outcomes = self.event_stats[feature_key]["outcomes"]
            total = self.event_stats[feature_key]["count"]
            probabilities = {k: v / total for k, v in outcomes.items()}
            return probabilities
        return {}

    def export(self):
        return {
            "observations": self.observation_log,
            "event_stats": dict(self.event_stats)
        }