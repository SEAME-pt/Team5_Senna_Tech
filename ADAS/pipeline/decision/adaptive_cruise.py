class AdaptiveCruiseControl:

    def __init__(self):

        self.target_area = 0.035
        self.max_cte = 1

    def compute_follow_error(
        self,
        lead_car_area
    ):

        error = (
            self.target_area
            - lead_car_area
        )

        error = max(
            -self.max_cte,
            min(self.max_cte, error)
        )

        return error