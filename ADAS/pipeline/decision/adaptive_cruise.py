class AdaptiveCruiseControl:

    def __init__(self):

        self.target_area = 0.033  # target relative area of the lead car (~60cm distance)
        self.max_cte = 1.0
        self.gain = 20.0          # scales area error → throttle percent
        self.emergency_area = 0.04  # if lead car area exceeds this → emergency braking

    def compute_follow_error(self, lead_car_area: float) -> float:

        if lead_car_area >= self.emergency_area:
            print(f"[ACC] EMERGENCY BRAKE | area={lead_car_area:.4f}")
            return -1.0  # travagem máxima

        error = self.target_area - lead_car_area
        error = error * self.gain
        return max(-self.max_cte, min(self.max_cte, error))