# gps_logger.py

import time
import json
from gps import gps, WATCH_ENABLE  # Assumes gpsd is running
import os

LOG_FILE = "gps_log.jsonl"

def log_location():
    session = gps(mode=WATCH_ENABLE)
    while True:
        try:
            report = session.next()
            if report.get("class") == "TPV":
                fix = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "lat": getattr(report, "lat", None),
                    "lon": getattr(report, "lon", None),
                    "alt": getattr(report, "alt", None)
                }

                with open(LOG_FILE, "a") as f:
                    f.write(json.dumps(fix) + "\n")

                time.sleep(5)  # Track every 5s — you can tweak this

        except Exception as e:
            print("[GPS Logger] Error:", e)
            time.sleep(3)
