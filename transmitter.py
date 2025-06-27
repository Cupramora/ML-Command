# transmitter.py
import socket, time
from gatekeeper import encrypt_payload, decrypt_payload

RETRIES = 3
TIMEOUT = 4  # seconds

def send_command(command: dict, ip, port):
    command.setdefault("priority", "normal")
    payload = encrypt_payload(command)

    for attempt in range(RETRIES):
        try:
            with socket.create_connection((ip, port), timeout=TIMEOUT) as s:
                s.sendall(payload.encode())
                ack_data = s.recv(4096)
                result = decrypt_payload(ack_data.decode())

                if result.get("type") == "ack":
                    print(f"[Transmitter] ACK received: {result}")
                    return True
                else:
                    print(f"[Transmitter] Unexpected response: {result}")
        except Exception as e:
            print(f"[Transmitter] Attempt {attempt + 1} failed: {e}")
            time.sleep(1)

    print("[Transmitter] No ACK after retries. Command failed.")
    return False
