class AdaptiveCruiseControl:
    def __init__(self):
        self.stop_area    = 0.05      # max area allowed
        self.max_throttle = 7      # max throttle when following

    def compute_follow_error(self, lead_car_area: float) -> int:
        if lead_car_area >= self.stop_area:
            print(f"[ACC] TOO CLOSE, STOPPING | area={lead_car_area:.4f}")
            return 0  # stop motor

        print(f"[ACC] FOLLOWING | area={lead_car_area:.4f}")
        return self.max_throttle