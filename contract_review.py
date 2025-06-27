# contract_review.py

import json
from datetime import datetime

class ContractReview:
    def __init__(self, log_file="contracts.json"):
        self.log_file = log_file
        self.contracts = []
        self.load()

    def log_contract(self, upgrade, cost, outcome, notes=""):
        entry = {
            "upgrade": upgrade,
            "cost": cost,
            "outcome": outcome,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self.contracts.append(entry)
        self.save()

    def review_history(self):
        summary = {}
        for c in self.contracts:
            name = c["upgrade"]
            if name not in summary:
                summary[name] = {"attempts": 0, "successes": 0}
            summary[name]["attempts"] += 1
            if c["outcome"] == "approved":
                summary[name]["successes"] += 1
        return summary

    def save(self):
        with open(self.log_file, "w") as f:
            json.dump(self.contracts, f, indent=2)

    def load(self):
        try:
            with open(self.log_file, "r") as f:
                self.contracts = json.load(f)
        except FileNotFoundError:
            self.contracts = []
