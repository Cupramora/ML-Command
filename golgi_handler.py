# golgi_handler.py

from perception import PerceptionCapsule, process_capsule
from short_term import ShortTermMemory

stm = ShortTermMemory()  # or inject it later

def handle_capsule(raw_capsule: dict):
    try:
        capsule = PerceptionCapsule(**raw_capsule)

        # Optional prefiltering
        if capsule.feedback == "negative" and capsule.reinforcement < 0.1:
            print("[Golgi] Discarded weak-negative capsule.")
            return {"status": "ignored"}

        # Optional tagging
        capsule.origin = "drone_alpha"
        capsule.flags = raw_capsule.get("flags", {})

        result = process_capsule(capsule)

        # Store significant moments
        if capsule.reinforcement > 0.2:
            stm.store_capsule(capsule, significance=0.5)
            print("[Golgi] Capsule stored in short-term memory.")

        return {
            "status": "processed",
            "directive": result["directive"],
            "reflexes": result["reflexes"]
        }

    except Exception as e:
        print(f"[Golgi] Error processing capsule: {e}")
        return {"status": "error", "details": str(e)}
