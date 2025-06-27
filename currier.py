# currier.py

from gatekeeper import decrypt_payload
from golgi_handler import handle_capsule
import socket

HOST = '0.0.0.0'
PORT = 5151  # Currier listens here—separate from the command port

def run_currier():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[Currier] Standing by for delivery...")

        conn, addr = s.accept()
        with conn:
            print(f"[Currier] Received delivery from {addr}")
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    payload = decrypt_payload(data.decode())
                    if payload.get("type") == "capsule":
                        capsule = payload["data"]
                        result = handle_capsule(capsule)
                        print(f"[Currier] Capsule processed: {result}")
                    else:
                        print("[Currier] Non-capsule payload ignored.")

                except Exception as e:
                    print(f"[Currier] Error handling payload: {e}")
