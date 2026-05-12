"""
Deteta as faixas de rodagem na imagem BEV usando o algoritmo de janelas deslizantes
e ajusta um polinómio de 2º grau a cada faixa.
 
Algoritmo (resumo):
1. Histograma: soma colunas na metade inferior → picos = posição das faixas
2. Sliding windows: percorre de baixo para cima, coletando píxeis brancos
3. Polyfit: ajusta y = a*x² + b*x + c a cada conjunto de píxeis
4. Validação: descarta ajustes com largura estranha, faixas cruzadas, etc.
5. Suavização EMA: suaviza os coeficientes entre frames consecutivos
6. CTE: calcula o erro lateral do veículo
"""
import cv2
import numpy as np
from typing import Optional, Tuple
from core.data_types import LaneFitResult

class SlidingWindowsLaneFitter:
    def __init__(self, cam_height: int = 360, n_windows: int = 12, margin: int = 40, min_pixels: int = 20, lane_width_px: float = 180.0):
        self.n_windows     = n_windows
        self.margin        = margin
        self.min_pixels    = min_pixels
        self.lane_width_px = lane_width_px
        self.cam_height    = cam_height
        self.tracked_lane_width_px = None # Calibrated bandwidth (updates)
        self._prev_left_fit    = None # coefficients of the previously fitted left lane (for smoothing)
        self._prev_right_fit   = None # coefficients of the previously fitted right lane
        self._anchor_left_fit  = None # last "trusted" left fit used as reference for histogram search
        self._anchor_right_fit = None # last "trusted" right fit
        self._left_was_virtual  = False # if the last left fit was virtual (not directly detected)
        self._right_was_virtual = False # if the last right fit was virtual
        #self._ema_curv_left:  Optional[float] = None #Exponential Moving Average (EMA) of the left lane curvature (a coefficient)
        #self._ema_curv_right: Optional[float] = None #EMA of the right lane curvature
        #self._curv_ema_alpha: float = 0.15 #Smoothing factor for curvature EMA (0.0 = no smoothing, 1.0 = only current value)
        self._ema_cte: Optional[float] = None # EMA of the CTE to smooth out the error signal for the PID controller
        #self._cte_alpha: float = 0.4 # Smoothing factor for CTE EMA 


    #Executes the complete pipeline for detecting and adjusting the lanes.
    def fit(self, bev_mask: np.ndarray, draw_debug: bool = False) -> LaneFitResult:
        h, w = bev_mask.shape[:2]

        left_base, right_base = self._histogram_peaks(bev_mask)
        left_px, right_px, debug_img = self._sliding_windows(bev_mask, left_base, right_base, draw_debug)

        left_fit  = self._polyfit(left_px, h)
        right_fit = self._polyfit(right_px, h)

        l_pixels = len(left_px[0])
        r_pixels = len(right_px[0])
        
        if left_fit is not None and right_fit is not None:
            y_eval = int(h * 0.75)
            l_x = left_fit[0]*(y_eval)**2 + left_fit[1]*(y_eval) + left_fit[2]
            r_x = right_fit[0]*(y_eval)**2 + right_fit[1]*(y_eval) + right_fit[2]
            
            actual_width = r_x - l_x
            expected_width = self.tracked_lane_width_px if self.tracked_lane_width_px is not None else self.lane_width_px
            ght   = abs(left_fit[0]) < 0.0004
            bad_width = actual_width < (expected_width * 0.60) or actual_width > (expected_width * 1.40)
            crossed = l_x > r_x - 10
            opposite_curves = (left_fit[0] * right_fit[0] < 0) and (abs(left_fit[0]) > 0.001) and (abs(right_fit[0]) > 0.001)
            low_pixels = (l_pixels < 40) or (r_pixels < 40) 
            
            if bad_width or crossed or opposite_curves or low_pixels:
                #Discard the range with the fewest pixels (the least reliable)
                if l_pixels < r_pixels:
                    left_fit = None
                else:
                    right_fit = None

        # Initializes the calibrated bandwidth if it has not yet been defined
        if self.tracked_lane_width_px is None:
            self.tracked_lane_width_px = self.lane_width_px

        #Updates the calibrated width and curvature EMAs if both lanes are detected (this indicates a more reliable detection)
        #and the width is reasonable for the current calibration. This allows the system to adapt to gradual changes in the camera
        #perspective or road conditions while filtering out outliers.
        if left_fit is not None and right_fit is not None:
            l_x = left_fit[0]*(h-1)**2  + left_fit[1]*(h-1)  + left_fit[2]
            r_x = right_fit[0]*(h-1)**2 + right_fit[1]*(h-1) + right_fit[2]
            current_width = abs(r_x - l_x)
            is_straight   = abs(left_fit[0]) < 0.0004 and abs(right_fit[0]) < 0.0004
            is_sane_width = (self.tracked_lane_width_px * 0.50) < current_width < (self.tracked_lane_width_px * 1.50) #original 0.70 e 1.30
            # Update the calibrated width only in reliable sections.
            if is_straight and is_sane_width:
                self.tracked_lane_width_px = 0.95 * self.tracked_lane_width_px + 0.05 * current_width

        left_is_virtual  = False
        right_is_virtual = False

        if self.tracked_lane_width_px is not None:
            if left_fit is None and right_fit is not None:
                left_fit = right_fit.copy()
                left_fit[2] -= self.tracked_lane_width_px
                left_is_virtual = True
            elif right_fit is None and left_fit is not None:
                right_fit = left_fit.copy()
                right_fit[2] += self.tracked_lane_width_px
                right_is_virtual = True

        left_found  = (left_fit  is not None) and not left_is_virtual
        right_found = (right_fit is not None) and not right_is_virtual

        # Calculate CTE using the current fits (even if one is virtual) to provide feedback to the PID
        cte_pixels, cte_norm = self._calculate_cte(left_fit, right_fit, w, h)
        curvature_px = self._calculate_curvature_px(left_fit if left_found else right_fit)
        
        # Smooth the polynomial coefficients to reduce jitter in the lane detection, which can help produce a more stable steering output.
        left_fit_smoothed  = self._smooth(left_fit,  self._prev_left_fit)
        right_fit_smoothed = self._smooth(right_fit, self._prev_right_fit)

        # Update the previous fits only if the current fits are valid (not None) to ensure that the smoothing is based on reliable data.
        if left_found:
            self._prev_left_fit   = left_fit_smoothed
            self._anchor_left_fit = left_fit
        if right_found:
            self._prev_right_fit   = right_fit_smoothed
            self._anchor_right_fit = right_fit

        self._left_was_virtual  = left_is_virtual
        self._right_was_virtual = right_is_virtual

        return LaneFitResult(
            left_fit=left_fit_smoothed, right_fit=right_fit_smoothed,
            cte_pixels=cte_pixels, cte_norm=cte_norm,
            curvature_px=curvature_px,
            left_found=left_found, right_found=right_found, debug_image=debug_img,
            left_is_virtual=left_is_virtual, right_is_virtual=right_is_virtual
        )

    """
    Find the initial horizontal position of each band by summing columns in the lower half of the BEV image (where the bands are wider and safer).
    If previous detections (anchors) exist, the search is restricted to a window around the expected position, making the system more robust.
    """
    def _histogram_peaks(self, bev_mask: np.ndarray) -> Tuple[int, int]:
        h, w = bev_mask.shape[:2]
        histogram = np.sum(bev_mask[h // 2:, :], axis=0)

        left_base, right_base = None, None

        ref_width = self.tracked_lane_width_px if self.tracked_lane_width_px is not None else self.lane_width_px
        
        # Expected position of the tracks based on the anchors from the previous frame.
        # !!!!! This 0.75 can be changed to find the optimum !!!!!!!
        # It represents how far down the image we evaluate the expected position, with 1.0 being at the very bottom.
        y_hist = int(h * 0.75)
        exp_left_x, exp_right_x = 0, w

        if self._anchor_left_fit is not None:
            exp_left_x = int(self._anchor_left_fit[0]*y_hist**2 + self._anchor_left_fit[1]*y_hist + self._anchor_left_fit[2])
        if self._anchor_right_fit is not None:
            exp_right_x = int(self._anchor_right_fit[0]*y_hist**2 + self._anchor_right_fit[1]*y_hist + self._anchor_right_fit[2])

        wall_x = w // 2
        if self._anchor_left_fit is not None and self._anchor_right_fit is not None:
            if exp_left_x < exp_right_x:
                mid       = (exp_left_x + exp_right_x) // 2
                wall_x    = int(np.clip(mid, exp_left_x + 20, exp_right_x - 20))
        elif self._anchor_left_fit is not None:
            wall_x = min(w - 1, exp_left_x + int(ref_width * 0.6))
        elif self._anchor_right_fit is not None:
            wall_x = max(0, exp_right_x - int(ref_width * 0.6))

        if self._anchor_left_fit is not None:
            search_margin = self.margin * 4 if self._left_was_virtual else self.margin * 2
            min_x = int(max(0,      exp_left_x - search_margin))
            max_x = int(min(wall_x, exp_left_x + search_margin))
            max_x = max(min_x + 1, max_x)
            hist_slice = histogram[min_x:max_x]
            if len(hist_slice) > 0 and np.max(hist_slice) > 40:
                peak_x = int(np.argmax(hist_slice)) + min_x
                if abs(peak_x - exp_left_x) <= search_margin and peak_x < (exp_right_x - 20):
                    left_base = peak_x

        if self._anchor_right_fit is not None:
            search_margin = self.margin * 4 if self._right_was_virtual else self.margin * 2
            min_x = int(max(wall_x, exp_right_x - search_margin))
            min_x = min(min_x, w - 1)
            max_x = int(min(w,      exp_right_x + search_margin))
            max_x = max(min_x + 1, max_x)
            hist_slice = histogram[min_x:max_x]
            if len(hist_slice) > 0 and np.max(hist_slice) > 40:
                peak_x = int(np.argmax(hist_slice)) + min_x
                if abs(peak_x - exp_right_x) <= search_margin and peak_x > (exp_left_x + 20):
                    right_base = peak_x

        midpoint      = w // 2
        margin_ignore = int(w * 0.10)

        if left_base is None:
            max_search_l = max(margin_ignore, right_base - int(ref_width * 0.6)) if right_base else midpoint
            left_section = histogram[margin_ignore:max_search_l]
            if len(left_section) > 0 and np.max(left_section) > 20:
                left_base = int(np.argmax(left_section)) + margin_ignore
            else:
                left_base = int(right_base - ref_width) if right_base else int(w * 0.25)

        if right_base is None:
            min_search_r = min(w - margin_ignore, left_base + int(ref_width * 0.6)) if left_base else midpoint
            right_section = histogram[min_search_r:w - margin_ignore]
            if len(right_section) > 0 and np.max(right_section) > 20:
                right_base = int(np.argmax(right_section)) + min_search_r
            else:
                right_base = int(left_base + ref_width) if left_base else int(w * 0.75)

        return left_base, right_base
    """
    After finding the base positions, the sliding windows algorithm collects white pixels in a
    series of horizontal windows moving upwards.
    The position of the windows is adjusted based on the mean position of the detected pixels
    in the previous window, allowing the algorithm to follow the curvature of the lanes.
    The function also includes logic to prevent the windows from crossing over in cases of detection errors.
    """
    def _sliding_windows(self, bev_mask: np.ndarray, left_base: int, right_base: int, draw_debug: bool):
        h, w = bev_mask.shape[:2]
        win_height = h // self.n_windows
        # Get the indices of all nonzero pixels in the image (potential lane pixels)
        nonzero   = bev_mask.nonzero()
        nonzero_y = np.array(nonzero[0])
        nonzero_x = np.array(nonzero[1])
        left_current  = left_base
        right_current = right_base
        left_lane_inds, right_lane_inds = [], []
        debug_img = cv2.cvtColor(bev_mask, cv2.COLOR_GRAY2BGR) if draw_debug else None

        for win in range(self.n_windows):
            # Define the vertical boundaries of the current window
            y_low  = h - (win + 1) * win_height
            y_high = h - win * win_height
            # Define the horizontal boundaries of the windows around the current positions of the left and right lanes
            xl_low,  xl_high = left_current  - self.margin, left_current  + self.margin
            xr_low,  xr_high = right_current - self.margin, right_current + self.margin

            if draw_debug and debug_img is not None:
                cv2.rectangle(debug_img, (xl_low, y_low), (xl_high, y_high), (0, 255, 0), 2)
                cv2.rectangle(debug_img, (xr_low, y_low), (xr_high, y_high), (0, 0, 255), 2)

            # Collect pixel indexes within each window.
            good_left  = ((nonzero_y >= y_low) & (nonzero_y < y_high) &
                          (nonzero_x >= xl_low) & (nonzero_x < xl_high)).nonzero()[0]
            good_right = ((nonzero_y >= y_low) & (nonzero_y < y_high) &
                          (nonzero_x >= xr_low) & (nonzero_x < xr_high)).nonzero()[0]

            left_lane_inds.append(good_left)
            right_lane_inds.append(good_right)

            new_left, new_right = left_current, right_current

            # Update the current positions based on the mean of the detected pixels in the window, if enough pixels were found.
            if len(good_left)  > self.min_pixels: new_left  = int(np.mean(nonzero_x[good_left]))
            if len(good_right) > self.min_pixels: new_right = int(np.mean(nonzero_x[good_right]))

            # Prevent the windows from crossing over, which can happen in cases of detection errors or very tight curves.
            # The minimum distance is based on the expected lane width.
            min_dist  = (self.tracked_lane_width_px * 0.35) if self.tracked_lane_width_px else 25
            if new_left > new_right - min_dist:
                if len(good_right) >= len(good_left): new_left  = left_current
                else: new_right = right_current

            left_current, right_current = new_left, new_right

        # Concatenate the arrays of indices and extract the pixel positions for the left and right lanes.
        left_lane_inds  = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
        left_pts  = (nonzero_x[left_lane_inds],  nonzero_y[left_lane_inds])
        right_pts = (nonzero_x[right_lane_inds], nonzero_y[right_lane_inds])

        return left_pts, right_pts, debug_img

    """
    Fits a polynomial to the given lane pixels.
    The polynomial uses y as the independent variable (x = a*y² + b*y + c),
    because the strips are more vertical than horizontal.
    Quality filters applied:
        - Minimum of 80 pixels
        - Pixels must cover at least 35% of the image height
        - Maximum curvature (|a| ≤ 0.008): rejects impossible curves
    """
    def _polyfit(self, lane_pixels: Tuple, image_height: int) -> Optional[np.ndarray]:
        x_vals, y_vals = lane_pixels
        if len(x_vals) < 80: return None
        try:
            y_span = np.max(y_vals) - np.min(y_vals)
            if y_span < (image_height * 0.35) or len(x_vals) < 60:
                return None 
            fit = np.polyfit(y_vals, x_vals, 2)
            if abs(fit[0]) > 0.0080: # Curvature too high, likely an error
                return None
            return fit
        except np.RankWarning:
            return None

    """
    Smooths the polynomial coefficients using an Exponential Moving Average (EMA) to reduce jitter in the lane detection.
    The EMA gives more weight to recent detections while still considering past values, which can help produce a more stable steering output.
    
    Applies a weighted average: result = alpha * current + (1-alpha) * previous
    The higher the alpha, the more weight the current frame has (less smoothing).

    Args:
    current: Coefficients of the current frame (or None)
    previous: Coefficients of the previous frame (or None)
    alpha: Weight of the current frame (0 to 1)
    """
    def _smooth(self, current: Optional[np.ndarray], previous: Optional[np.ndarray], alpha: float = 0.8) -> Optional[np.ndarray]:
        if current is None: return None  
        if previous is None: return current
        return alpha * current + (1.0 - alpha) * previous

    """
    Calculates the Cross-Track Error (CTE) in pixels and normalized form.
    The CTE represents how far the vehicle is from the center of the lane, with positive
    
    The CTE is calculated at 60% of the image height (neither too close nor too far).
    It is then normalized by half the width of the swath, resulting in [-1, +1].
    Finally, it is smoothed with EMA to reduce PID oscillations.
    Positive CTE → vehicle is to the right of center → turn left
    Negative CTE → vehicle is to the left of center → turn right
    """
    def _calculate_cte(self, left_fit: Optional[np.ndarray], right_fit: Optional[np.ndarray],
                       image_width: int, image_height: int) -> Tuple[Optional[float], Optional[float]]:
        if left_fit is None or right_fit is None: return None, None
        y_eval = int(image_height * 0.60)
        vehicle_centre = image_width / 2.0

        # Calculate the x position of each lane at the evaluation point and compute the lane center and CTE in pixels.
        left_x  = left_fit[0]*y_eval**2  + left_fit[1]*y_eval  + left_fit[2]
        right_x = right_fit[0]*y_eval**2 + right_fit[1]*y_eval + right_fit[2]
        lane_centre = (left_x + right_x) / 2.0
        cte_pixels  = vehicle_centre - lane_centre
        
        # Normalize the CTE
        width_ref = self.tracked_lane_width_px if self.tracked_lane_width_px else self.lane_width_px
        raw_cte_norm = 0.0
        if width_ref > 0: raw_cte_norm = max(-1.0, min(1.0, cte_pixels / (width_ref / 2.0)))

        # Smooth the CTE using EMA to provide a more stable error signal to the PID
        if self._ema_cte is None:
            self._ema_cte = raw_cte_norm 
        else:
            self._ema_cte = 0.35 * raw_cte_norm + 0.65 * self._ema_cte

        # "Dead zone": ignores very small errors (< 2%) for straight-line stability.
        if abs(self._ema_cte) < 0.02:
            self._ema_cte = 0.0
        return cte_pixels, self._ema_cte

    """
    Calculate the radius of curvature of the lane in pixels using the differential calculus formula.
    Formula: R = (1 + (2ay + b)²)^(3/2) / |2a|
    A very large radius (>10000 px) indicates a practically straight road.
    Args:
    fit: Coefficients [a, b, c] of the polynomial
    """
    def _calculate_curvature_px(self, fit: Optional[np.ndarray]) -> float:
        if fit is None: return 10000.0
        a, b, _ = fit
        if abs(a) < 1e-6: return 10000.0
        y_eval = self.cam_height - 1
        return ((1 + (2*a*y_eval + b)**2)**1.5) / abs(2*a)