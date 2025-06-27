# bridge_initializer.py
# imports mathematical tools, signal bridges, and interface expectations

from shared.math.predictive_kinematics import KinematicPlanner
from shared.math.vector_field_tools import VectorSynthesizer
from shared.interfaces.target_posture_builder import PostureBridge
from shared.mappings.module_interface_loader import load_interfaces

# Load declared interfaces from other modules
interfaces = load_interfaces([
    "../ML-FlightControl/module_interface.json",
    "../ML-SensorHub/module_interface.json",
    "../ML-ElectricVariationControl/module_interface.json"
])
