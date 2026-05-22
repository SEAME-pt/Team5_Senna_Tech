"""
LaneFitResult contains all data resulting from lane detection and polynomial fitting.

Attributes:
left_fit:        Coefficients [a, b, c] of the 2nd-degree polynomial for the left lane
                         (x = a*y² + b*y + c, where y increases downward)
right_fit:       Same for the right lane
cte_pixels:      Lateral error in pixels (positive = vehicle to the right of centre)
cte_norm:        Lateral error normalised between -1.0 and +1.0
curvature_px:    Radius of curvature in pixels (>10000 = straight)
left_found:      True if the left lane was detected (not virtual)
right_found:     True if the right lane was detected (not virtual)
debug_image:     Debug image with sliding windows (or None)
left_is_virtual: True if the left lane was estimated (not directly detected)
right_is_virtual:True if the right lane was estimated
swap_pending:    True if the tracker suspects the lanes have been swapped
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class LaneFitResult:
    left_fit:        Optional[np.ndarray]
    right_fit:       Optional[np.ndarray]
    cte_pixels:      Optional[float]
    cte_norm:        Optional[float]
    curvature_px:    Optional[float]
    left_found:      bool
    right_found:     bool
    debug_image:     Optional[np.ndarray]
    left_is_virtual: bool = False
    right_is_virtual: bool = False
    swap_pending:    bool = False
