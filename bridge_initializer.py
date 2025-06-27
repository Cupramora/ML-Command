# bridge_initializer.py
# Initializes predictive tools, signal bridges, and inter-module contracts

import json
from shared.math.predictive_kinematics import KinematicPlanner
from shared.math.vector_field_tools import VectorSynthesizer
from shared.interfaces.target_posture_builder import PostureBridge
from shared.mappings.module_interface_loader import ModuleInterfaceLoader


def load_interface_paths(config_path="bridge_config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config.get("interface_paths", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] Failed to load config: {e}")
        return []


def initialize_bridge():
    # Step 1: Load all module interface contracts
    interface_paths = load_interface_paths()
    loader = ModuleInterfaceLoader(interface_paths)
    interfaces = loader.load_all()

    # Optional: Print summary of what's wired
    loader.describe()

    # Step 2: Initialize core signal processing tools
    planner = KinematicPlanner()
    synthesizer = VectorSynthesizer()
    posture_bridge = PostureBridge()

    return {
        "interfaces": interfaces,
        "posture_bridge": posture_bridge,
        "planner": planner,
        "synthesizer": synthesizer
    }


if __name__ == "__main__":
    print("🔧 Bootstrapping system bridges...")
    systems = initialize_bridge()
    print("✅ Bridge initialized successfully.")
