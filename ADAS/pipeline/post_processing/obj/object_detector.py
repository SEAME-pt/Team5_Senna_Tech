import numpy as np
import cv2


class ObjectDetector:

    def __init__(self):
        self.class_names = [
            "50_sign", "80_sign", "gate", "crosswalk_sign",
            "stop_sign", "yeald_sign", "car", "danger_sign",
            "obstacle", "light_green", "light_off",
            "light_red", "light_yellow"
        ]
        self.conf_thresh = 0.25
        self.nms_thresh = 0.45
        self.num_classes = 13

    # ---------------- UTIL ----------------
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def make_grid(self, h, w):
        y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
        return np.stack((x, y), axis=-1)

    # ---------------- DECODE ----------------
    def decode_output(self, bbox, cls, stride):

        cls = self.sigmoid(cls)

        h, w, _ = bbox.shape
        grid = self.make_grid(h, w)

        l = bbox[..., 0]
        t = bbox[..., 1]
        r = bbox[..., 2]
        b = bbox[..., 3]

        cx = (grid[..., 0] + 0.5) * stride
        cy = (grid[..., 1] + 0.5) * stride

        x1 = cx - l * stride
        y1 = cy - t * stride
        x2 = cx + r * stride
        y2 = cy + b * stride

        boxes = np.stack([x1, y1, x2, y2], axis=-1).reshape(-1, 4)

        cls = cls.reshape(-1, self.num_classes)

        scores = np.max(cls, axis=1)
        classes = np.argmax(cls, axis=1)

        mask = scores > self.conf_thresh

        return boxes[mask], scores[mask], classes[mask]

    # ---------------- NMS ----------------
    def nms(self, boxes, scores):

        if len(boxes) == 0:
            return []

        x1, y1, x2, y2 = boxes.T
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]

        keep = []

        while order.size > 0:
            i = order[0]
            keep.append(i)

            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)

            inter = w * h
            iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)

            inds = np.where(iou <= self.nms_thresh)[0]
            order = order[inds + 1]

        return keep

    # ---------------- MAIN PROCESS ----------------
    def process(self, outputs, frame_shape):

        h0, w0 = frame_shape[:2]
        sx = w0 / 640
        sy = h0 / 640

        b80 = outputs["yolo26n/conv61"][0]
        c80 = outputs["yolo26n/conv64"][0]

        b40 = outputs["yolo26n/conv77"][0]
        c40 = outputs["yolo26n/conv80"][0]

        b20 = outputs["yolo26n/conv91"][0]
        c20 = outputs["yolo26n/conv94"][0]

        all_boxes, all_scores, all_classes = [], [], []

        for bbox, cls, stride in [
            (b80, c80, 8),
            (b40, c40, 16),
            (b20, c20, 32)
        ]:
            b, s, c = self.decode_output(bbox, cls, stride)
            all_boxes.append(b)
            all_scores.append(s)
            all_classes.append(c)

        if len(all_boxes) == 0:
            return []

        boxes = np.concatenate(all_boxes)
        scores = np.concatenate(all_scores)
        classes = np.concatenate(all_classes)

        keep = self.nms(boxes, scores)

        detections = []

        for i in keep:
            x1, y1, x2, y2 = boxes[i]

            x1 = int(x1 * sx)
            y1 = int(y1 * sy)
            x2 = int(x2 * sx)
            y2 = int(y2 * sy)

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "score": float(scores[i]),
                "class_id": int(classes[i]),
                "class_name": self.class_names[int(classes[i])]
            })

        return detections

    # ---------------- DRAW ----------------
    def draw(self, frame, detections):

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = det["class_name"]
            score = det["score"]

            in_corr  = det.get("in_corridor", False)
            rel_area = det.get("relative_area", 0.0)
            db       = det.get("debug_info", None)

            # Red for objects within our zone, green for those outside it
            color     = (0, 0, 255) if in_corr else (0, 100, 0)
            thickness = 2 if in_corr else 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

            # Text with the relative area value of the scaling
            text = f"{label} | A:{(rel_area * 100):.1f}%"
            cv2.putText(frame, text, (x1, max(y1 - 25, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

            # Draw the base of the bounding box
            bottom_center_x = int((x1 + x2) / 2)
            cv2.circle(frame, (bottom_center_x, y2), 5, (255, 0, 255), -1)

        return frame
