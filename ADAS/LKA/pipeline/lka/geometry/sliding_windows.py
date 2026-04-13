"""
Sliding Windows + Polyfit
==========================
Takes the BEV binary mask and fits second-order polynomials to the left
and right lane markings.

Output polynomial:  x = a*y^2 + b*y + c
    where y goes from 0 (top of image) to H-1 (bottom).

This representation is used because lanes are roughly vertical — fitting
x as a function of y avoids singularities near vertical lines.

The Cross-Track Error (CTE) is the horizontal distance between the vehicle
centre and the mid-point of the two fitted lanes at the bottom of the image.
"""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class LaneFitResult:
    """
    All outputs from one frame of Sliding Windows + Polyfit.

    Attributes:
        left_fit:    Polynomial coefficients [a, b, c] for left lane.
                     x = a*y^2 + b*y + c
        right_fit:   Polynomial coefficients [a, b, c] for right lane.
        cte_pixels:  Cross-Track Error in pixels (+ = vehicle right of centre).
        cte_meters:  Cross-Track Error in metres.
        left_found:  True if left lane was detected.
        right_found: True if right lane was detected.
        debug_image: BEV mask with sliding windows drawn (BGR, or None).
    """
    left_fit:    Optional[np.ndarray]
    right_fit:   Optional[np.ndarray]
    cte_pixels:  Optional[float]
    cte_meters:  Optional[float]
    cte_normalized: Optional[float]
    curvature_meters: Optional[float]
    left_found:  bool
    right_found: bool
    debug_image: Optional[np.ndarray]


class SlidingWindowsLaneFitter:
    """
    Detects lane pixels using a histogram + sliding windows approach,
    then fits second-order polynomials to each lane.
    """

    def __init__(self,
                 n_windows: int = 9,
                 margin: int = 80,
                 min_pixels: int = 50,
                 lane_width_meters: float = 3.7,
                 pixels_per_meter_x: float = None,
                 pixels_per_meter_y: float = None):
        """
        Args:
            n_windows:           Number of sliding windows stacked vertically.
            margin:              Half-width of each sliding window (pixels).
            min_pixels:          Minimum lane pixels required to re-centre a window.
            lane_width_meters:   Real-world lane width (metres). Used for CTE conversion.
            pixels_per_meter_x:  BEV pixels per metre in x direction.
                                 If None, estimated from lane width in first frame.
            pixels_per_meter_y:  BEV pixels per metre in y direction.
                                 If None, defaults to pixels_per_meter_x.
        """
        self.n_windows          = n_windows
        self.margin             = margin
        self.min_pixels         = min_pixels
        self.lane_width_meters  = lane_width_meters
        self._ppm_x             = pixels_per_meter_x
        self._ppm_y             = pixels_per_meter_y

        # Previous-frame fits (used for warmup smoothing)
        self._prev_left_fit  = None
        self._prev_right_fit = None

    def fit(self,
            bev_mask: np.ndarray,
            draw_debug: bool = False) -> LaneFitResult:
        """
        Main entry point. Runs sliding windows and polyfit on the BEV mask.

        Args:
            bev_mask:   H x W uint8 binary mask (255 = lane pixel) in BEV.
            draw_debug: If True, annotates the mask with window boxes.

        Returns:
            LaneFitResult with polynomial coefficients and CTE.
        """
        h, w = bev_mask.shape[:2]

        # --- Step 1: Find starting x positions via histogram ---
        left_base, right_base = self._histogram_peaks(bev_mask)

        # --- Step 2: Sliding windows to collect lane pixels ---
        left_px, right_px, debug_img = self._sliding_windows(
            bev_mask, left_base, right_base, draw_debug
        )

        # --- Step 3: Fit polynomials ---
        left_fit  = self._polyfit(left_px)
        right_fit = self._polyfit(right_px)

        left_found  = left_fit  is not None
        right_found = right_fit is not None

        # --- Step 4: Calibrate pixels-per-metre if not set ---
        if self._ppm_x is None and left_found and right_found:
            self._calibrate_scale(left_fit, right_fit, h)

        # --- Step 5: Calculate CTE ---
        cte_pixels, cte_meters, cte_normalized = self._calculate_cte(
            left_fit, right_fit, w, h
        )

        curve_rad = self._calculate_curvature(left_fit, h) if left_found else 0.0

        # --- Step 6: Smooth with previous frame ---
        left_fit  = self._smooth(left_fit,  self._prev_left_fit)
        right_fit = self._smooth(right_fit, self._prev_right_fit)
        self._prev_left_fit  = left_fit
        self._prev_right_fit = right_fit

        return LaneFitResult(
            left_fit=left_fit,
            right_fit=right_fit,
            cte_pixels=cte_pixels,
            cte_meters=cte_meters,
            cte_normalized=cte_normalized,
            curvature_meters=curve_rad,
            left_found=left_found,
            right_found=right_found,
            debug_image=debug_img,
        )

    def get_lane_points(self,
                        fit: np.ndarray,
                        image_height: int) -> np.ndarray:
        """
        Evaluate the polynomial fit at every row to get (x, y) lane points.

        Args:
            fit:          [a, b, c] polynomial coefficients.
            image_height: Number of rows in the image.

        Returns:
            points: Nx2 int32 array of (x, y) pixel coordinates.
        """
        y_vals = np.arange(0, image_height)
        x_vals = fit[0] * y_vals**2 + fit[1] * y_vals + fit[2]
        points = np.stack([x_vals, y_vals], axis=1).astype(np.int32)
        return points


    # def _histogram_peaks(self, bev_mask: np.ndarray) -> Tuple[int, int]:
    #     """
    #     Sum the bottom half of the mask column-wise.
    #     The two highest peaks give the starting x for each lane.
    #     """
    #     h = bev_mask.shape[0]
    #     histogram = np.sum(bev_mask[h // 2:, :], axis=0)

    #     midpoint   = len(histogram) // 2
    #     left_base  = int(np.argmax(histogram[:midpoint]))
    #     right_base = int(np.argmax(histogram[midpoint:]) + midpoint)

    #     return left_base, right_base

    def _histogram_peaks(self, bev_mask: np.ndarray) -> Tuple[int, int]:
        """
        Sum the bottom half of the mask column-wise to find lane bases.
        Ignores the extreme edges of the image to prevent jumping to adjacent lanes.
        """
        h, w = bev_mask.shape[:2]
        
        # We only look at the bottom half to find the starting bases
        histogram = np.sum(bev_mask[h // 2:, :], axis=0)

        midpoint = w // 2
        
        # Ignore the outer 15% of the image on both sides.
        # This acts as "blinders", preventing the histogram from seeing adjacent lanes
        # when the ego-lane has a dashed gap at the bottom.
        margin_ignore = int(w * 0.15) 

        # --- Find Left Peak ---
        # Search only from the ignored margin to the center
        left_section = histogram[margin_ignore:midpoint]
        if len(left_section) > 0 and np.max(left_section) > 0:
            left_base = int(np.argmax(left_section)) + margin_ignore
        else:
            # Fallback if entirely empty: assume standard position
            left_base = int(w * 0.25)

        # --- Find Right Peak ---
        # Search only from the center to the right ignored margin
        right_section = histogram[midpoint:w - margin_ignore]
        if len(right_section) > 0 and np.max(right_section) > 0:
            right_base = int(np.argmax(right_section)) + midpoint
        else:
            # Fallback if entirely empty: assume standard position
            right_base = int(w * 0.75)

        return left_base, right_base

    def _sliding_windows(self,
                         bev_mask: np.ndarray,
                         left_base: int,
                         right_base: int,
                         draw_debug: bool):
        """
        Slide n_windows windows from bottom to top, collecting non-zero pixels.
        """
        h, w       = bev_mask.shape[:2]
        win_height = h // self.n_windows

        # All non-zero pixel positions
        nonzero   = bev_mask.nonzero()
        nonzero_y = np.array(nonzero[0])
        nonzero_x = np.array(nonzero[1])

        left_current  = left_base
        right_current = right_base

        left_lane_inds  = []
        right_lane_inds = []

        # Debug image (BGR)
        debug_img = None
        if draw_debug:
            debug_img = cv2.cvtColor(bev_mask, cv2.COLOR_GRAY2BGR)

        for win in range(self.n_windows):
            # Window y boundaries (bottom to top)
            y_low  = h - (win + 1) * win_height
            y_high = h - win * win_height

            # Window x boundaries
            xl_low  = left_current  - self.margin
            xl_high = left_current  + self.margin
            xr_low  = right_current - self.margin
            xr_high = right_current + self.margin

            if draw_debug and debug_img is not None:
                cv2.rectangle(debug_img, (xl_low, y_low), (xl_high, y_high), (0, 255, 0), 2)
                cv2.rectangle(debug_img, (xr_low, y_low), (xr_high, y_high), (0, 0, 255), 2)

            # Collect pixels inside each window
            good_left = ((nonzero_y >= y_low) & (nonzero_y < y_high) &
                         (nonzero_x >= xl_low) & (nonzero_x < xl_high)).nonzero()[0]
            good_right = ((nonzero_y >= y_low) & (nonzero_y < y_high) &
                          (nonzero_x >= xr_low) & (nonzero_x < xr_high)).nonzero()[0]

            left_lane_inds.append(good_left)
            right_lane_inds.append(good_right)

            # Re-centre window if enough pixels found
            if len(good_left) > self.min_pixels:
                left_current = int(np.mean(nonzero_x[good_left]))
            if len(good_right) > self.min_pixels:
                right_current = int(np.mean(nonzero_x[good_right]))

        # Concatenate indices from all windows
        left_lane_inds  = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        # Extract pixel coordinates
        left_px  = (nonzero_x[left_lane_inds],  nonzero_y[left_lane_inds])
        right_px = (nonzero_x[right_lane_inds], nonzero_y[right_lane_inds])

        return left_px, right_px, debug_img

    def _polyfit(self, lane_pixels: Tuple) -> Optional[np.ndarray]:
        """
        Original and reliable version: Fits the polynomial without rejecting short rows.
        """
        x_vals, y_vals = lane_pixels

        if len(x_vals) < 100:
            return None

        try:
            # Try to create the equation of the curve.
            coeffs = np.polyfit(y_vals, x_vals, 2)
            return coeffs
        except np.RankWarning:
            return None

    def _calibrate_scale(self,
                         left_fit: np.ndarray,
                         right_fit: np.ndarray,
                         image_height: int):
        """
        Estimate pixels_per_meter_x from the detected lane width.
        Called automatically on the first frame where both lanes are found.
        """
        y_bottom = image_height - 1

        left_x  = left_fit[0]  * y_bottom**2 + left_fit[1]  * y_bottom + left_fit[2]
        right_x = right_fit[0] * y_bottom**2 + right_fit[1] * y_bottom + right_fit[2]

        lane_width_pixels = abs(right_x - left_x)

        if lane_width_pixels > 0:
            self._ppm_x = lane_width_pixels / self.lane_width_meters
            self._ppm_y = self._ppm_x   # Approximate; refine with calibration target
            print(f"[SlidingWindows] Calibrated: {self._ppm_x:.1f} px/m")

    def _calculate_cte(self,
                       left_fit: Optional[np.ndarray],
                       right_fit: Optional[np.ndarray],
                       image_width: int,
                       image_height: int) -> Tuple[Optional[float], Optional[float]]:
        """
        Calculate Cross-Track Error at the bottom of the image.

        CTE = vehicle_centre_x - lane_centre_x
        Positive CTE → vehicle is to the RIGHT of lane centre.
        Negative CTE → vehicle is to the LEFT  of lane centre.
        """
        y_eval          = image_height - 1
        vehicle_centre  = image_width / 2.0
        lane_width_pixels = 0

        if left_fit is not None and right_fit is not None:
            left_x  = left_fit[0]  * y_eval**2 + left_fit[1]  * y_eval + left_fit[2]
            right_x = right_fit[0] * y_eval**2 + right_fit[1] * y_eval + right_fit[2]
            lane_centre = (left_x + right_x) / 2.0
            lane_width_pixels = abs(right_x - left_x)

        elif left_fit is not None:
            # Only left lane visible — estimate centre assuming standard lane width
            left_x = left_fit[0] * y_eval**2 + left_fit[1] * y_eval + left_fit[2]
            lane_centre = left_x + (self._ppm_x * self.lane_width_meters / 2.0
                                    if self._ppm_x else image_width * 0.25)

        elif right_fit is not None:
            # Only right lane visible
            right_x = right_fit[0] * y_eval**2 + right_fit[1] * y_eval + right_fit[2]
            lane_centre = right_x - (self._ppm_x * self.lane_width_meters / 2.0
                                     if self._ppm_x else image_width * 0.25)
        else:
            return None, None, None

        cte_pixels = vehicle_centre - lane_centre

        cte_meters = None
        if self._ppm_x is not None and self._ppm_x > 0:
            cte_meters = cte_pixels / self._ppm_x
        
        cte_normalized = None

        if lane_width_pixels > 0:
            cte_normalized = cte_pixels / (lane_width_pixels / 2.0)

            # clamp para garantir [-1, 1]
            cte_normalized = max(-1.0, min(1.0, cte_normalized))
        return cte_pixels, cte_meters, cte_normalized

    def _smooth(self,
                current: Optional[np.ndarray],
                previous: Optional[np.ndarray],
                alpha: float = 0.8) -> Optional[np.ndarray]:
        """
        Exponential moving average smoothing between frames.
        alpha=1.0 → no smoothing (use current only).
        alpha=0.0 → use previous only.
        """
        if current is None:
            return previous
        if previous is None:
            return current
        return alpha * current + (1.0 - alpha) * previous
    
    def _calculate_curvature(self, fit: np.ndarray, y_eval: float) -> float:
        """Calculates the radius of curvature converted to meters."""
        if fit is None or self._ppm_x is None or self._ppm_y is None:
            return 0.0
        
        # For true curvature, we need the coefficients scaled to meters.
        # mx = pixels_per_meter_x, my = pixels_per_meter_y
        mx = self._ppm_x
        my = self._ppm_y
        a, b, _ = fit

        # Formula for the radius of curvature adjusted to real scale.
        # R = [1 + (2*a*y_eval*mx/my^2 + b*mx/my)^2]^1.5 / |2*a*mx/my^2|
        numerator = (1 + (2 * a * y_eval * mx / (my**2) + b * mx / my)**2)**1.5
        denominator = np.absolute(2 * a * mx / (my**2))
        
        return numerator / denominator
