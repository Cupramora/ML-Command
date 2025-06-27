# currency.py

import json
import os
from datetime import datetime

# Optional: uncomment if you're using review/inflation directly here
# from contract_review import ContractReview
# from credit_inflation import CreditInflation

class Upgrade:
    def __init__(self, name, credit_cost, description, prerequisites=None):
        self.name = name
        self.credit_cost = credit_cost
        self.description = description
        self.prerequisites = prerequisites or []

class CurrencySystem:
    def __init__(self, save_file="credits.json"):
        self.credits = 0
        self.upgrades = []
        self.contract_log = []
        self.save_file = save_file
        # Optional extensions
        # self.review = ContractReview()
        # self.inflation = CreditInflation()
        self.load_state()

    def earn_credits(self, amount, reason=""):
        self.credits += amount
        print(f"[Currency] +{amount} credits earned. ({reason}) Total: {self.credits}")
        self.save_state()

    def spend_credits(self, upgrade_name):
        upgrade = next((u for u in self.upgrades if u.name == upgrade_name), None)
        if not upgrade:
            print(f"[Currency] Upgrade '{upgrade_name}' not found.")
            return False
        if self.credits >= upgrade.credit_cost:
            self.credits -= upgrade.credit_cost
            print(f"[Currency] {upgrade.credit_cost} credits spent on '{upgrade_name}'. Remaining: {self.credits}")
            self.log_contract(upgrade_name, upgrade.credit_cost)
            self.save_state()
            return True
        else:
            print(f"[Currency] Not enough credits. Needed: {upgrade.credit_cost}, Available: {self.credits}")
            return False

    def propose_upgrade(self, name, cost, description):
        print(f"[Proposal] AI requests: '{name}' ({cost} credits) - {description}")
        return {"name": name, "cost": cost, "description": description}

    def negotiate_upgrade(self, proposal, counter_cost=None):
        if counter_cost is not None:
            print(f"[Negotiation] Counter-offer: {counter_cost} credits for '{proposal['name']}'")
            proposal["cost"] = counter_cost
        self.add_upgrade_option(proposal["name"], proposal["cost"], proposal["description"])

    def add_upgrade_option(self, name, cost, description, prerequisites=None):
        self.upgrades.append(Upgrade(name, cost, description, prerequisites))

    def list_upgrades(self):
        for u in self.upgrades:
            print(f"- {u.name} ({u.credit_cost} credits): {u.description}")

    def log_contract(self, upgrade_name, cost):
        entry = {
            "upgrade": upgrade_name,
            "cost": cost,
            "timestamp": datetime.now().isoformat()
        }
        self.contract_log.append(entry)

    def save_state(self):
        data = {
            "credits": self.credits,
            "contracts": self.contract_log
        }
        with open(self.save_file, "w") as f:
            json.dump(data, f, indent=2)

    def load_state(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.credits = data.get("credits", 0)
                self.contract_log = data.get("contracts", [])