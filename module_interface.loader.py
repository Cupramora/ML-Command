# module_interface_loader.py
# loads and parses module_interface.json files across repos

import json
import os

class ModuleInterfaceLoader:
    """
    Loads interface contracts from other modules for system validation and wiring.
    """

    def __init__(self, paths):
        self.paths = paths
        self.interfaces = {}

    def load_all(self):
        for path in self.paths:
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    module_name = data.get("module", "Unnamed")
                    self.interfaces[module_name] = data
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"[WARN] Failed to load {path}: {e}")
        return self.interfaces

    def describe(self):
        """
        Prints a summary of each module’s declared interfaces.
        """
        for name, config in self.interfaces.items():
            print(f"\n📦 {name}")
            print("  ➤ Provides:")
            for k in config.get("provides", {}):
                print(f"    - {k}")
            print("  ➤ Requires:")
            for k in config.get("requires", {}):
                print(f"    - {k}")
            print("  ➤ Interfaces:")
            for k in config.get("interfaces", {}):
                print(f"    - {k}")
