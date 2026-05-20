import cv2
import numpy as np

class CorridorChecker:
    def __init__(self, bev_transform):
        self.bev = bev_transform

    def map_point_to_bev(self, x, y):
        point = np.array([[[float(x), float(y)]]], dtype=np.float32)
        transformed = cv2.perspectiveTransform(point, self.bev.M)
        return transformed[0][0]

    def check_and_debug(self, bbox, fit_result, frame_shape):
        x1, y1, x2, y2 = bbox
        h_orig, w_orig = frame_shape[:2]
        
        obj_area = float((x2 - x1) * (y2 - y1))
        total_area = float(w_orig * h_orig)
        rel_area = obj_area / total_area if total_area > 0 else 0.0

        # BEV mapping of the bottom center of the bounding box
        bottom_center_x = (x1 + x2) / 2.0
        bottom_center_y = float(y2)
        bev_x, bev_y = self.map_point_to_bev(bottom_center_x, bottom_center_y)

        debug_info = {
            "bev_x": bev_x, "bev_y": bev_y,
            "l_x": 0.0, "r_x": w_orig, 
            "in_corridor": False, "rel_area": rel_area
        }

        if not fit_result.left_found and not fit_result.right_found:
            debug_info["in_corridor"] = (w_orig * 0.35) < bev_x < (w_orig * 0.65)
            return debug_info

        # intersection with the lines
        margin = 15 
        in_left = True
        if fit_result.left_fit is not None:
            l_x = (fit_result.left_fit[0] * (bev_y**2) + fit_result.left_fit[1] * bev_y + fit_result.left_fit[2])
            in_left = bev_x > (l_x - margin)
            debug_info["l_x"] = l_x

        in_right = True
        if fit_result.right_fit is not None:
            r_x = (fit_result.right_fit[0] * (bev_y**2) + fit_result.right_fit[1] * bev_y + fit_result.right_fit[2])
            in_right = bev_x < (r_x + margin)
            debug_info["r_x"] = r_x

        debug_info["in_corridor"] = bool(in_left and in_right)
        return debug_info