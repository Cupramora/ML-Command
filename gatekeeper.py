# gatekeeper.py

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json

# Must be 32 bytes (256 bits)
SECRET_KEY = b"your-32-byte-secret-key-here!!"  # Make this identical on both nodes

def encrypt_payload(data: dict) -> str:
    raw = json.dumps(data).encode()
    iv = get_random_bytes(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padding_len = 16 - len(raw) % 16
    padded = raw + bytes([padding_len] * padding_len)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(iv + encrypted).decode()

def decrypt_payload(enc: str) -> dict:
    enc_bytes = base64.b64decode(enc)
    iv = enc_bytes[:16]
    encrypted = enc_bytes[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    pad_len = decrypted[-1]
    json_str = decrypted[:-pad_len].decode()
    return json.loads(json_str)
