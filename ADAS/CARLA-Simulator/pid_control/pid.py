import numpy as np

def clamp_symmetric(value, limit):
    if limit <= 0.0:
        return 0.0
    elif value > limit:
        return limit
    elif value < -limit:
        return -limit
    return value


def map_pid_to_servo(pid_value, min_angle, max_angle):
    # Clamp to [-1, 1]
    pid_value = max(-1.0, min(1.0, pid_value))

    servo_angle = (pid_value + 1.0) * (max_angle - min_angle) / 2.0 + min_angle
    return servo_angle


class PID:

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0.0
        self.integral = 0.0

        self.integral_limit = 1.0
        self.output_limit = 1.0

    def update(self, target, current, dt):

        if dt <= 0.0:
            return 0.0

        error = target - current

        proportional = self.kp * error

        self.integral += error * dt
        self.integral = clamp_symmetric(self.integral, self.integral_limit)

        integral = self.ki * self.integral

        derivative = self.kd * ((error - self.prev_error) / dt)

        self.prev_error = error

        output = proportional + integral + derivative

        return clamp_symmetric(output, self.output_limit)

    def reset(self):
        self.prev_error = 0.0
        self.integral = 0.0

    def set_integral_limit(self, limit):
        self.integral_limit = abs(limit)
        self.integral = clamp_symmetric(self.integral, self.integral_limit)

    def set_output_limit(self, limit):
        self.output_limit = abs(limit)