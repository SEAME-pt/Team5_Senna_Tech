class AdaptiveCruiseControl:
    def __init__(self):
        self.stop_area     = 0.05   # security area
        self.follow_area   = 0.02   # area to start following
        self.max_throttle  = 9      # max throttle to apply in follow

    def compute_follow_error(self, lead_car_area: float) -> int:
        if lead_car_area >= self.stop_area:
            print(f"[ACC] TOO CLOSE, STOPPING")
            return 0

        ratio = (self.stop_area - lead_car_area) / (self.stop_area - self.follow_area)
        ratio = max(0.0, min(1.0, ratio))
        throttle = round(ratio * self.max_throttle)

        print(f"[ACC] FOLLOWING throttle={throttle}")
        return throttle