# listener.py (on drone)

from gatekeeper import decrypt_payload, encrypt_payload
import socket

HOST = '0.0.0.0'
PORT = 5050

def handle_command(cmd):
    if cmd["task"] == "scan_area":
        from sight import capture_and_detect
        results = capture_and_detect()
        return {
            "type": "result",
            "task": "scan_area",
            "status": "complete",
            "data": {
                "objects": ["person", "tree"],  # placeholder
                "avg_confidence": 0.87
            }
        }

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[Explorer] Listening for commands...")
    conn, addr = s.accept()
    with conn:
        print(f"[Explorer] Connected by {addr}")
        while True:
            data = conn.recv(4096)
            if not data:
                break
            #  Decrypt inbound command
            cmd = decrypt_payload(data.decode())
            print(f"[Explorer] Received: {cmd}")

            response = handle_command(cmd)

            #  Encrypt response
            encrypted_response = encrypt_payload(response)
            conn.sendall(encrypted_response.encode())