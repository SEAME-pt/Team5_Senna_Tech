"""
Draw the detected bands over the original camera image.
Process:
1. Calculate the polynomial points for each y-axis.
2. Fill the corridor between the bands with semi-transparent green.
3. Draw the central line in cyan.
4. Draw each band (blue = real, cyan = virtual).
5. Unwarp everything back from BEV perspective to camera perspective.
6. Blend with the original image.
"""

import cv2
import numpy as np

def draw_lane_overlay(frame_bgr, fit_result, bev):
    h, w = frame_bgr.shape[:2]
    result = frame_bgr.copy()
    y_vals = np.arange(0, h)

    def poly_pts(f):
        if f is None: return None
        x = f[0]*y_vals**2 + f[1]*y_vals + f[2]
        return np.stack([x, y_vals], axis=1).astype(np.int32)

    if fit_result.left_fit is None and fit_result.right_fit is None:
        return result

    overlay = np.zeros_like(frame_bgr)
    lp = poly_pts(fit_result.left_fit)
    rp = poly_pts(fit_result.right_fit)

    if lp is not None and rp is not None:
        pts = np.vstack([lp, rp[::-1]])
        cv2.fillPoly(overlay, [pts], (0, 150, 0))# Semi-transparent green fill for the lane corridor
        cx = (lp[:, 0] + rp[:, 0]) / 2
        cp = np.stack([cx, y_vals], axis=1).astype(np.int32)
        cv2.polylines(overlay, [cp], False, (0, 255, 255), 2)# 

    if lp is not None:
        l_color = (0, 255, 255) if getattr(fit_result, 'left_is_virtual', False) else (255, 0, 0)
        cv2.polylines(overlay, [lp], False, l_color, 10)
        
    if rp is not None:
        r_color = (0, 255, 255) if getattr(fit_result, 'right_is_virtual', False) else (0, 0, 255)
        cv2.polylines(overlay, [rp], False, r_color, 10)

    unwarped = bev.unwarp(overlay)
    result = cv2.addWeighted(result, 1.0, unwarped, 0.4, 0)

    try:
        src_pts = (bev.DEFAULT_SRC * [w, h]).astype(np.int32)
        cv2.polylines(result, [src_pts], True, (255, 0, 255), 2)
    except: pass

    return result

def draw_text_overlay(frame, fit_result, model_name=None, fps=None, inf_ms=None):
    h, w = frame.shape[:2]
    result = frame 

    def put(txt, pos, color, scale=1.2, thick=2):
        cv2.putText(result, txt, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick)

    if fit_result.left_fit is not None or fit_result.right_fit is not None:
        curv_val = getattr(fit_result, 'curvature_px', None)
        curve_text = "Direction: Calculating..." 

        if curv_val is not None:
            a_coeff = fit_result.left_fit[0] if fit_result.left_fit is not None else fit_result.right_fit[0]
            if curv_val > 10000: curve_text = "Direction: Straight"
            elif a_coeff > 0.0001: curve_text = f"Curve: Right (R: {curv_val:.0f} px)"
            elif a_coeff < -0.0001: curve_text = f"Curve: Left (R: {curv_val:.0f} px)"
            else: curve_text = "Direction: Straight"
        
        put(curve_text, (20, 90), (255, 255, 255))
    else:
        cv2.putText(result, "NO LANES DETECTED", (w//2 - 200, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cte_val = getattr(fit_result, 'cte_norm', None) 
    if cte_val is not None:
        cte_txt = f"CTE Norm: {cte_val:+.3f}"
        color = (0, 255, 0) if abs(cte_val) < 0.2 else (0, 165, 255)
    else:
        cte_txt = "CTE: Aguardando faixas..."
        color = (128, 128, 128)
    
    put(cte_txt, (20, 50), color)

    bm = w // 2
    cv2.line(result, (bm - 100, 70), (bm + 100, 70), (200, 200, 200), 2)
    if cte_val is not None:
        dx = int(bm - cte_val * 100)
        cv2.circle(result, (np.clip(dx, bm-100, bm+100), 70), 7, color, -1)

    if model_name: put(model_name, (w - 250, 30), (200, 200, 200), scale=0.5, thick=1)
    
    label = ""
    if inf_ms is not None: label += f"Hailo: {inf_ms:.1f}ms  "
    if fps is not None: label += f"FPS: {fps:.1f}"
    put(label, (10, h - 35), (255, 255, 255), scale=0.6)

    return result