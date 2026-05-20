from dataclasses import dataclass
from enum import Enum
from typing import Optional
from post_processing.object.perception_objects import ClassID, ObstacleSituation


@dataclass
class ObstacleInfo:
    situation:          ObstacleSituation
    area:               float
    delta_area:         float
    bev_x_norm:         float
    frames_in_corridor: int
    side:               str


class ObstacleTracker:
    def __init__(
        self,
        area_brake_threshold:  float = 0.060,
        area_avoidance_min:    float = 0.010,
        frames_to_confirm:     int   = 4,
        frame_width_bev:       int   = 640,
    ):
        self.area_brake_threshold  = area_brake_threshold
        self.area_avoidance_min    = area_avoidance_min
        self.frames_to_confirm     = frames_to_confirm
        self.frame_width_bev       = frame_width_bev

        self._prev_area:          float = 0.0
        self._frames_in_corridor: int   = 0
        self._last_bev_x_norm:    float = 0.5

    def update(self, detections_in_corridor: list) -> ObstacleInfo:
        obstacles = [
            d for d in detections_in_corridor
            if d.get("class_id") == ClassID.OBSTACLE.value
            and d.get("in_corridor", False)
        ]

        if not obstacles:
            self._frames_in_corridor = 0
            self._prev_area          = 0.0
            return ObstacleInfo(
                situation          = ObstacleSituation.CLEAR,
                area               = 0.0,
                delta_area         = 0.0,
                bev_x_norm         = self._last_bev_x_norm,
                frames_in_corridor = 0,
                side               = "center",
            )

        best       = max(obstacles, key=lambda d: d.get("relative_area", 0.0))
        area       = best.get("relative_area", 0.0)
        debug      = best.get("debug_info", {})
        bev_x      = debug.get("bev_x", self.frame_width_bev * 0.5)
        bev_x_norm = max(0.0, min(1.0, float(bev_x) / float(self.frame_width_bev)))

        delta_area = 0.0 if self._frames_in_corridor == 0 else area - self._prev_area

        self._prev_area          = area
        self._last_bev_x_norm    = bev_x_norm
        self._frames_in_corridor += 1

        if bev_x_norm < 0.43:
            side = "left"
        elif bev_x_norm > 0.57:
            side = "right"
        else:
            side = "center"

        if delta_area >= self.area_brake_threshold:
            situation = ObstacleSituation.BRAKE
        elif area >= self.area_avoidance_min and self._frames_in_corridor >= self.frames_to_confirm:
            situation = ObstacleSituation.AVOIDANCE
        else:
            situation = ObstacleSituation.CLEAR

        return ObstacleInfo(
            situation          = situation,
            area               = area,
            delta_area         = delta_area,
            bev_x_norm         = bev_x_norm,
            frames_in_corridor = self._frames_in_corridor,
            side               = side,
        )

    def reset(self):
        self._prev_area          = 0.0
        self._frames_in_corridor = 0
