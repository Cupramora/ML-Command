from gatekeeper import decrypt_payload, encrypt_payload
from golgi_handler import handle_capsule
from ack_router import AckRouter

import socket

ack_router = AckRouter()

DRONE_IP = '192.168.1.42'  # Replace with actual IP
PORT = 5050

# 1. Prepare command and issue unique ID
command = {
    "type": "command",
    "task": "scan_area",
    "params": {
        "duration": 5,
        "mode": "vision"
    }
}
command = ack_router.issue_command_id(command)  # ✅ ID added here!

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((DRONE_IP, PORT))

    # 2. Encrypt and send
    encrypted_cmd = encrypt_payload(command)
    s.sendall(encrypted_cmd.encode())

    # 3. Receive and decrypt
    data = s.recv(4096)
    result = decrypt_payload(data.decode())
    print(f"[Core] Received result: {result}")

    # 4. ACK routing and capsule handling
    if result.get("type") == "ack":
        ack_router.receive_ack(result)

    elif result.get("type") == "capsule" and "data" in result:
        outcome = handle_capsule(result["data"])

    else:
        print("[Core] Unexpected response or structure.")

# Optional: Check for expired/unacknowledged tasks
ack_router.check_expired(timeout=10)