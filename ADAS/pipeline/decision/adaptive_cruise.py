class AdaptiveCruiseControl:

    def __init__(self):

        self.target_area = 0.033  # target relative area of the lead car (~60cm distance)
        self.max_cte = 1.0
        self.gain = 20.0          # scales area error → throttle percent

    def compute_follow_error(self, lead_car_area: float) -> float:

        error = self.target_area - lead_car_area

        # positive error → car is far → accelerate
        # negative error → car is close → decelerate
        error = error * self.gain
        return max(-self.max_cte, min(self.max_cte, error))