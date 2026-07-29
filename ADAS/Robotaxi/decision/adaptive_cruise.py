# AdaptiveCruiseControl
#
# Computes throttle based on the detected area of the lead car in the frame.
# The area is a normalized value [0.0, 1.0] representing how much of the
# frame the detected bounding box occupies.
#
# Two thresholds define the behavior:
#   - follow_area: minimum area to start following (car is far enough)
#   - stop_area:   area at which the car is too close and must stop
#
# Between these two thresholds, throttle scales linearly from max down to 0.

class AdaptiveCruiseControl:
    def __init__(self):
        self.stop_area    = 0.05   # security area
        self.follow_area  = 0.02   # area to start following
        self.max_throttle = 9      # max throttle to apply in follow

    def compute_follow_error(self, lead_car_area: float) -> int:
        if lead_car_area >= self.stop_area:
            return 0

        ratio    = (self.stop_area - lead_car_area) / (self.stop_area - self.follow_area)
        ratio    = max(0.0, min(1.0, ratio))
        throttle = round(ratio * self.max_throttle)
        return throttle
