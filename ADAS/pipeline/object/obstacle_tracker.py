"""
ObstacleTracker
---------------
Tracks the most relevant obstacle in the corridor frame by frame.
Calculates:

- current relative area
- area delta between frames (growth rate)
- normalized BEV position (0=left, 1=right)
- number of consecutive frames in the corridor

Based on this, classifies the situation as:
- CLEAR: no relevant obstacle in the corridor
- AVOIDANCE: obstacle detected in advance (slow growth)
- BRAKE: obstacle appeared suddenly (rapid growth)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from object.perception_objects import ClassID, ObstacleSituation

@dataclass
class ObstacleInfo:
    situation:          ObstacleSituation
    area:               float          # relative actual area  [0, 1]
    delta_area:         float          # area variation per frame
    bev_x_norm:         float          # normalized BEV position [0=left, 1=right]
    frames_in_corridor: int            # consecutive frames in the corridor
    side:               str            # "left" | "right" | "center"


class ObstacleTracker:
    """
    Parameters
    ----------
    area_brake_threshold   : if delta_area >= this value in a single frame → BRAKE
    area_avoidance_min     : minimum area to consider avoidance
    frames_to_confirm      : consecutive frames to confirm avoidance
    frame_width_bev        : width of the BEV image in px (= CAM_WIDTH)
    """

    def __init__(
        self,
        area_brake_threshold:  float = 0.025,
        area_avoidance_min:    float = 0.010,
        frames_to_confirm:     int   = 4,
        frame_width_bev:       int   = 640,
    ):
        self.area_brake_threshold  = area_brake_threshold
        self.area_avoidance_min    = area_avoidance_min
        self.frames_to_confirm     = frames_to_confirm
        self.frame_width_bev       = frame_width_bev

        self._prev_area:         float = 0.0
        self._frames_in_corridor: int  = 0
        self._last_bev_x_norm:   float = 0.5

    # ------------------------------------------------------------------
    def update(self, detections_in_corridor: list) -> ObstacleInfo:
        """
        detections_in_corridor : list of dicts with keys
            "class_id"       (int)
            "relative_area"  (float)
            "debug_info"     (dict with "bev_x")
        Only ClassID.OBSTACLE (value 8) is considered.
        """
        from object.perception_objects import ClassID

        # Filter only obstacles in the corridor
        obstacles = [
            d for d in detections_in_corridor
            if d.get("class_id") == ClassID.OBSTACLE.value
            and d.get("in_corridor", False)
        ]

        # No obstacle → reset and return CLEAR
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

        # Get the obstacle with the largest area (most relevant)
        best = max(obstacles, key=lambda d: d.get("relative_area", 0.0))
        area     = best.get("relative_area", 0.0)
        debug    = best.get("debug_info", {})
        bev_x    = debug.get("bev_x", self.frame_width_bev * 0.5)
        bev_x_norm = float(bev_x) / float(self.frame_width_bev)
        bev_x_norm = max(0.0, min(1.0, bev_x_norm))

        if self._frames_in_corridor == 0:
            delta_area = 0.0 # First frame seeing the object, no real delta
        else:
            delta_area = area - self._prev_area

        self._prev_area          = area
        self._last_bev_x_norm    = bev_x_norm
        self._frames_in_corridor += 1

        # Determine the side of the obstacle relative to the center (0.5)
        if bev_x_norm < 0.43:
            side = "left"
        elif bev_x_norm > 0.57:
            side = "right"
        else:
            side = "center"

        # ── Classification ──────────────────────────────────────────────
        # BRAKE: growth very rapid in a single frame
        if delta_area >= self.area_brake_threshold:
            situation = ObstacleSituation.BRAKE

        # AVOIDANCE: relevant area AND present for sufficient frames
        elif (
            area >= self.area_avoidance_min
            and self._frames_in_corridor >= self.frames_to_confirm
        ):
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
