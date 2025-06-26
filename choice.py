# choice.py

class BehaviorSelector:
    def __init__(self):
        self.behavior_map = {
            "retreat_now": self.act_retreat,
            "pause_and_scan": self.act_scan,
            "observe": self.act_observe,
            "monitor": self.act_monitor
        }

    def commit_to_action(self, behavior_packet):
        directive = behavior_packet.get("directive", "observe")
        intensity = behavior_packet.get("intensity", "baseline")
        mode = behavior_packet.get("mode", "neutral")
        style = behavior_packet.get("style", "neutral")
        justification = behavior_packet.get("justification", "")

        print("\nCOMMITTED BEHAVIOR")
        print(f"> Action     : {directive}")
        print(f"> Intensity  : {intensity}")
        print(f"> Mode       : {mode}")
        print(f"> Style      : {style}")
        print(f"> Rationale  : {justification}")

        behavior_fn = self.behavior_map.get(directive, self.default_action)
        behavior_fn(intensity=intensity, mode=mode, style=style)

    def act_retreat(self, intensity, mode, style):
        self.speak("I don't feel safe. I'm moving back!", tone=style)
        self.flash_lights("alert")

    def act_scan(self, intensity, mode, style):
        self.speak("Something feels off... I'm checking around.", tone=style)
        self.flash_lights("pulse")

    def act_observe(self, intensity, mode, style):
        self.speak("Just watching quietly.", tone=style)
        self.set_lights("blue")

    def act_monitor(self, intensity, mode, style):
        self.speak("I'm keeping an eye on things.", tone=style)
        self.set_lights("soft_white")

    def default_action(self, **kwargs):
        self.speak("I don't know what to do.", tone="confused")
        self.flash_lights("neutral")

    # --- Voice & Light Output Hooks ---
    def speak(self, phrase, tone="neutral"):
        print(f"[Voice:{tone}] -> \"{phrase}\"")
        # (later: route to real text-to-speech engine)

    def flash_lights(self, pattern):
        print(f"[Light Effect] Flashing lights: {pattern}")

    def set_lights(self, color):
        print(f"[Light Effect] Ambient color set to {color}")