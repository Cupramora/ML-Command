# ack_router.py

import uuid, time

class AckRouter:
    def __init__(self):
        self.active_transmissions = {}

    def issue_command_id(self, command):
        command_id = str(uuid.uuid4())
        command["id"] = command_id
        self.active_transmissions[command_id] = {
            "timestamp": time.time(),
            "status": "sent",
            "task": command.get("task", "unknown")
        }
        return command

    def receive_ack(self, ack_data):
        task_id = ack_data.get("id")
        if not task_id:
            print("[ACK Router] No ID in ACK. Skipping...")
            return

        if task_id in self.active_transmissions:
            self.active_transmissions[task_id]["status"] = "acknowledged"
            print(f"[ACK Router] ACK received for task {task_id}")
        else:
            print(f"[ACK Router] Unknown task ID: {task_id}")

    def check_expired(self, timeout=10):
        now = time.time()
        for tid, info in self.active_transmissions.items():
            if info["status"] == "sent" and now - info["timestamp"] > timeout:
                print(f"[ACK Router] No ACK for task {tid} - TIMED OUT.")