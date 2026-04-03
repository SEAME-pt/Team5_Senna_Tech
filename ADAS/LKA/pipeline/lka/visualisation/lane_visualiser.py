import cv2
import numpy as np
from typing import Optional
from ..geometry.bev_transform import BEVTransform
from ..geometry.sliding_windows import LaneFitResult

class LaneVisualiser:
    def __init__(self, bev: BEVTransform):
        self.bev = bev

    def draw(self, frame_bgr: np.ndarray, fit_result: LaneFitResult) -> np.ndarray:
        h, w = frame_bgr.shape[:2]
        annotated = frame_bgr.copy()

        if not fit_result.left_found and not fit_result.right_found:
            self._draw_no_lane_warning(annotated)
            return annotated

        # 1. Create an overlay for the lines in the BEV space.
        overlay = np.zeros_like(frame_bgr)
        y_vals = np.arange(0, h)

        def get_pts(fit):
            x = fit[0]*y_vals**2 + fit[1]*y_vals + fit[2]
            return np.stack([x, y_vals], axis=1).astype(np.int32)

        left_pts = get_pts(fit_result.left_fit) if fit_result.left_found else None
        right_pts = get_pts(fit_result.right_fit) if fit_result.right_found else None

        # 2. Drawing Green Area and Centerline
        if left_pts is not None and right_pts is not None:
            pts = np.vstack([left_pts, right_pts[::-1]])
            cv2.fillPoly(overlay, [pts], (0, 150, 0)) # dark green
            
            center_x = (left_pts[:, 0] + right_pts[:, 0]) / 2
            center_pts = np.stack([center_x, y_vals], axis=1).astype(np.int32)
            cv2.polylines(overlay, [center_pts], False, (0, 255, 255), 2) # yellow centerline

        # 3. Drawing Side Lines
        if left_pts is not None:
            cv2.polylines(overlay, [left_pts], False, (255, 0, 0), 10) # Blue
        if right_pts is not None:
            cv2.polylines(overlay, [right_pts], False, (0, 0, 255), 10) # Red

        # --- ADraw Curvature and Direction ---
        if fit_result.curvature_meters is not None:
            
            # Extract the 'a' coefficient to determine curve direction
            # Default to 0.0 (Straight) if no lanes are found
            a_coeff = 0.0
            if fit_result.left_found and fit_result.left_fit is not None:
                a_coeff = fit_result.left_fit[0]
            elif fit_result.right_found and fit_result.right_fit is not None:
                a_coeff = fit_result.right_fit[0]

            # Determine text based on radius and direction
            if fit_result.curvature_meters > 3000:
                curve_text = "Direction: Straight"
            else:
                # Use a small threshold (e.g., 0.0001) to ignore micro-noise
                if a_coeff > 0.0001:
                    curve_text = f"Curve: Right (R: {fit_result.curvature_meters:.1f} m)"
                elif a_coeff < -0.0001:
                    curve_text = f"Curve: Left (R: {fit_result.curvature_meters:.1f} m)"
                else:
                    curve_text = "Direction: Straight"
                
            # cv2.putText(annotated, curve_text, (20, 90), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
    
        # 4. Project back and merge with real image
        unwarped = self.bev.unwarp(overlay)
        annotated = cv2.addWeighted(annotated, 1.0, unwarped, 0.4, 0)

        # 5. Draw Texts and Indicators
        self._draw_cte(annotated, fit_result)

        # --- 6. Draw the BEV Trapezoid (Magenta Line for Debug) ---
        try:
            # Try to get the points from the BEV class. 
            # (We multiply by [w, h] if they are in percentages from 0 to 1)
            if hasattr(self.bev, 'DEFAULT_SRC'):
                src_pts = (self.bev.DEFAULT_SRC * [w, h]).astype(np.int32)
            elif hasattr(self.bev, 'src_points'):
                src_pts = (self.bev.src_points * [w, h]).astype(np.int32)
            
            # Draw the closed polygon in magenta
            cv2.polylines(annotated, [src_pts], isClosed=True, color=(255, 0, 255), thickness=2)
        except Exception as e:
            pass # If there's an error finding the variable, ignore it to avoid crashing the video
        
        return annotated

    def _draw_cte(self, frame_bgr: np.ndarray, fit_result: LaneFitResult):
        h, w = frame_bgr.shape[:2]
        
        # Security lock: only formats the text if the value is not None.
        if fit_result.cte_meters is not None:
            cte_text = f"CTE: {fit_result.cte_meters:+.3f} m"
            color = (0, 255, 0) if abs(fit_result.cte_meters) < 0.2 else (0, 165, 255)
        else:
            cte_text = "CTE: Calibrando..."
            color = (128, 128, 128)

        # Draw the CTE text
        cv2.putText(frame_bgr, cte_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
        
        # Visual indicator bar
        bar_mid = w // 2
        cv2.line(frame_bgr, (bar_mid - 100, 70), (bar_mid + 100, 70), (200, 200, 200), 2)
        
        if fit_result.cte_pixels is not None:
            dot_x = int(bar_mid - fit_result.cte_pixels * 0.2)
            cv2.circle(frame_bgr, (np.clip(dot_x, bar_mid-100, bar_mid+100), 70), 7, color, -1)

    def _draw_no_lane_warning(self, frame_bgr: np.ndarray):
        cv2.putText(frame_bgr, "NO LANES DETECTED", (frame_bgr.shape[1]//2 - 200, frame_bgr.shape[0]//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)