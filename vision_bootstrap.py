# vision_bootstrap.py
# Ensures OpenCV and Ultralytics YOLO are installed and ready

import subprocess
import sys

required = {
    "opencv-python": "cv2",
    "ultralytics": "ultralytics"
}

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ensure_packages():
    for pkg, module in required.items():
        try:
            __import__(module)
            print(f"[OK] {pkg} already installed.")
        except ImportError:
            print(f"[...] Installing {pkg}...")
            install(pkg)
    print("✅ All vision dependencies are now active.")

if __name__ == "__main__":
    ensure_packages()
