from gatekeeper import decrypt_payload, encrypt_payload
from handler import handle_command
from speak import say

import socket
import time

# ASCII-safe voice log
def append_to_voice_log(text):
    timestamp = time.strftime("[%H:%M:%S] ", time.localtime())
    with open("voice_output_log.txt", "a", encoding="ascii", errors="replace") as f:
        f.write(timestamp + text + "\n")

HOST = "0.0.0.0"
PORT = 5050

def run_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("[Receiver] Listening for incoming commands...")

        conn, addr = s.accept()
        with conn:
            print("[Receiver] Connected by", addr)
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                try:
                    cmd = decrypt_payload(data.decode())
                    task = cmd.get("task", "unknown")
                    task_id = cmd.get("id")

                    print(f"[Receiver] Received command: {task} (ID: {task_id})")
                    say("task_received", {"task": task, "mood": "curious"})
                    append_to_voice_log(f"Command '{task}' received.")

                    ack = {
                        "type": "ack",
                        "task": task,
                        "status": "received",
                        "id": task_id
                    }
                    conn.sendall(encrypt_payload(ack).encode())

                    result = handle_command(cmd)
                    conn.sendall(encrypt_payload(result).encode())
                    say("task_completed", {"task": task, "mood": "confident"})

                    append_to_voice_log(f"Task '{task}' completed.")

                except Exception as e:
                    print("[Receiver] Error:", e)
                    append_to_voice_log("Error handling command.")

if __name__ == "__main__":
    run_receiver()