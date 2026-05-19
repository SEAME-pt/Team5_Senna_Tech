"""
Maintains consistent lane identity (left/right) over time.

Problem solved:
The detector can sometimes swap the left and right lanes,
especially on tight curves. This would cause a catastrophically wrong
turn signal (turning right when it should be left).

Solution:
- Maintains EMAs (moving averages) of the expected position of each lane
- Compares new detections with the EMAs using a similarity function
- Only accepts a swap if it is confirmed in several consecutive frames
"""

from typing import Optional
import numpy as np
from core.data_types import TrackedLaneFit

class LaneIdentityTracker:
    def __init__(self, image_width=640, image_height=360, ema_alpha=0.25, swap_confirm_frames=8, position_weight=0.7):
        self.w = image_width
        self.h = image_height
        self.alpha = ema_alpha
        self.swap_confirm_frames = swap_confirm_frames
        self.pos_weight = position_weight
        self._ema_left = None
        self._ema_right = None
        self._swap_counter = 0
        self._frame = 0

    """
    Receives a raw detection and assigns the correct identity (left/right)
    based on history.

    Logic:
    1. If there is no history, uses _initialize_first_frame to setup
    2. Otherwise, calculates the assignment cost A (normal) and B (swapped)
    3. If B is better (suspected swap), increments the counter
    4. Only applies the swap if the counter reaches the threshold
    """
    def assign(self, fit_result) -> TrackedLaneFit:
        self._frame += 1
        lf = fit_result.left_fit
        rf = fit_result.right_fit
        li = getattr(fit_result, 'left_is_virtual',  False)
        ri = getattr(fit_result, 'right_is_virtual', False)

        if lf is None and rf is None:
            return TrackedLaneFit(left_fit=None, right_fit=None, left_is_virtual=False, right_is_virtual=False)

        # Usando o novo nome descritivo para inicialização
        if self._ema_left is None and self._ema_right is None:
            lf_out, rf_out, li_out, ri_out = self._initialize_first_frame(lf, rf, li, ri)
            self._update_ema(lf_out, rf_out)
            return TrackedLaneFit(left_fit=lf_out, right_fit=rf_out, left_is_virtual=li_out, right_is_virtual=ri_out)
        
        lf_out, rf_out, li_out, ri_out, swap = self._assign_identity(lf, rf, li, ri)

        swap_pending = False
        if swap:
            self._swap_counter += 1
            if self._swap_counter < self.swap_confirm_frames:
                # Do not apply the swap yet, wait for confirmation in subsequent frames
                lf_out, rf_out = self._ema_left, self._ema_right
                li_out, ri_out = False, False
                swap_pending   = True
            else:
                self._swap_counter = 0 # Swap confirmed, apply it and reset counter
        else:
            self._swap_counter = max(0, self._swap_counter - 1) # Decay counter if no swap is detected

        self._update_ema(lf_out, rf_out)
        return TrackedLaneFit(left_fit=lf_out, right_fit=rf_out, left_is_virtual=li_out, right_is_virtual=ri_out, swap_pending=swap_pending)

    """
    It initializes the lane identity on first detection,
    based on the horizontal position of each lane relative to the center.
    The lane to the left of the center is the left lane, and vice versa.
    """
    def _initialize_first_frame(self, lf, rf, li, ri):
        cx = self.w / 2.0
        y_eval = self.h - 1
        def x_at_bottom(fit):
            if fit is None: return None
            return fit[0]*y_eval**2 + fit[1]*y_eval + fit[2]
        x_l, x_r = x_at_bottom(lf), x_at_bottom(rf)

        if lf is not None and rf is not None:
            if x_l <= x_r: return lf, rf, li, ri
            else: return rf, lf, ri, li
        if lf is not None:
            if x_l < cx: return lf, None, li, False 
            else: return None, lf, False, li  
        else:
            if x_r > cx: return None, rf, False, ri 
            else: return rf, None, ri, False  

    """
    Compares the new detections with the EMAs of the bands and decides if there is a swap.
    Calculates two costs:
    cost_A: cost of assigning lf→left and rf→right (normal order)
    cost_B: cost of assigning lf→right and rf→left (swapped order)

    Chooses the assignment with the lowest cost.
    """
    def _assign_identity(self, lf, rf, li, ri):
        swap = False
        y_eval = self.h - 1
        def x_at(fit):
            if fit is None: return None
            return fit[0]*y_eval**2 + fit[1]*y_eval + fit[2]

        x_l, x_r = x_at(lf), x_at(rf)
        x_ema_l, x_ema_r = x_at(self._ema_left), x_at(self._ema_right)

        # If one lane is missing, assign the identity of the detected lane based on similarity to the EMAs
        if lf is None or rf is None:
            single_fit = lf if lf is not None else rf
            single_is_virtual = li if lf is not None else ri
            single_x = x_at(single_fit)
            sim_l = self._similarity(single_fit, self._ema_left,  single_x, x_ema_l)
            sim_r = self._similarity(single_fit, self._ema_right, single_x, x_ema_r)

            if sim_l <= sim_r: return single_fit, None, single_is_virtual, False, False
            else: return None, single_fit, False, single_is_virtual, False

        cost_A = self._similarity(lf, self._ema_left, x_l, x_ema_l) + self._similarity(rf, self._ema_right, x_r, x_ema_r)
        cost_B = self._similarity(lf, self._ema_right, x_l, x_ema_r) + self._similarity(rf, self._ema_left, x_r, x_ema_l)

        if cost_A <= cost_B: return lf, rf, li, ri, False
        else: return rf, lf, ri, li, True

    """
    Similarity function that compares a new fit with a reference EMA fit.
    It combines:
    - Position similarity: how close the x position at the bottom is (normalized by image width)
    - Shape similarity: how close the polynomial coefficients are (scaled to be comparable)
    The position similarity is weighted more heavily (default 70%) since it is more indicative of lane identity.
    """
    def _similarity(self, fit_new, fit_ref, x_new, x_ref) -> float:
        if fit_new is None or fit_ref is None: return 1e9
        pos_dist = abs(x_new - x_ref) / (self.w + 1e-6) if (x_new is not None and x_ref is not None) else 1.0
        shape_dist = (abs(fit_new[0] - fit_ref[0]) * 1e4 + abs(fit_new[1] - fit_ref[1])) / 2.0
        shape_dist = min(shape_dist, 1.0) 
        return self.pos_weight * pos_dist + (1.0 - self.pos_weight) * shape_dist

    """
    Updates the EMAs of the left and right lane fits with the new assigned fits.
    Uses the formula: EMA_new = alpha * Fit_new + (1 - alpha) * EMA_previous
    If the new fit is None, it does not update that EMA (keeps the previous value).
    """
    def _update_ema(self, lf, rf):
        alpha = self.alpha
        if lf is not None:
            if self._ema_left is None: self._ema_left = lf.copy()
            else: self._ema_left = alpha * lf + (1.0 - alpha) * self._ema_left
        if rf is not None:
            if self._ema_right is None: self._ema_right = rf.copy()
            else: self._ema_right = alpha * rf + (1.0 - alpha) * self._ema_right