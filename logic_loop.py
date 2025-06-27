# logic_loop.py

import time

class LogicLoop:
    def __init__(self, setpoint=1.0, kp=1.0, ki=0.0, kd=0.0):
        self.setpoint = setpoint  # Desired outcome (e.g. "detect eruption")
        self.kp = kp              # Proportional gain
        self.ki = ki              # Integral gain
        self.kd = kd              # Derivative gain

        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = time.time()

    def update(self, current_value):
        now = time.time()
        dt = now - self.prev_time if self.prev_time else 1.0

        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0

        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )

        # Update state
        self.prev_error = error
        self.prev_time = now

        return output  # This can be interpreted as "urgency" or "confidence"