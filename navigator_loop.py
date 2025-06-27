# navigator_loop.py

import time
from psyche_report import PsycheReport
from navigator import Navigator

def run_navigator_loop(short_term_memory, dream_reflections, reinforcement_log):
    psyche = PsycheReport(short_term_memory, dream_reflections, reinforcement_log)
    navigator = Navigator()

    while True:
        print("[Navigator Loop] Generating psyche report...")
        report = psyche.generate_report()

        print("[Navigator Loop] Categorizing file candidates...")
        navigator.categorize(report["file_candidates"])

        # Optional: log dominant emotions or unresolved flags
        print(f"[Navigator Loop] Dominant emotions: {report['dominant_emotions']}")
        print(f"[Navigator Loop] Unresolved flags: {report['unresolved_flags']}")

        # Sleep until next pass (e.g. every 6 hours)
        time.sleep(21600)