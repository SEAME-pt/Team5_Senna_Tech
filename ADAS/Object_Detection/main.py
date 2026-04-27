import cv2
import sys
import numpy as np
import time
import subprocess
import os

from hailo_platform import (
    HEF,
    VDevice,
    ConfigureParams,
    HailoStreamInterface,
    InferVStreams,
    FormatType,
    InputVStreamParams,
    OutputVStreamParams
)

# ---------------- CLASSES ----------------
CLASS_NAMES = [
    "50_sign",
    "80_sign",
    "gate",
    "crosswalk_sign",
    "stop_sign",
    "yeald_sign",
    "car",
    "danger_sign",
    "obstacle",
    "light_green",
    "light_off",
    "light_red",
    "light_yellow"
]

# ---------------- CONFIG ----------------
NET_SIZE = 640
NUM_CLASSES = 13

CONF_THRESH = 0.25
NMS_THRESH = 0.45

CAM_WIDTH = 640
CAM_HEIGHT = 640
CAM_FPS = 40

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720


# ---------------- PREPROCESS ----------------
def preprocess(frame):
    h0, w0 = frame.shape[:2]

    img = cv2.resize(frame, (NET_SIZE, NET_SIZE))
    img = img.astype(np.uint8)

    sx = w0 / NET_SIZE
    sy = h0 / NET_SIZE

    return np.expand_dims(img, axis=0), sx, sy


# ---------------- UTIL ----------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def make_grid(h, w):
    y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    return np.stack((x, y), axis=-1)


# ---------------- DECODE ----------------
def decode_output(bbox, cls, stride):

    cls = sigmoid(cls)

    h, w, _ = bbox.shape
    grid = make_grid(h, w)

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

    cls = cls.reshape(-1, NUM_CLASSES)

    scores = np.max(cls, axis=1)
    classes = np.argmax(cls, axis=1)

    mask = scores > CONF_THRESH

    return boxes[mask], scores[mask], classes[mask]


# ---------------- NMS ----------------
def nms(boxes, scores, iou_threshold=0.45):

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

        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return keep


# ---------------- POSTPROCESS ----------------
def postprocess(outputs, frame, sx, sy):

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
        b, s, c = decode_output(bbox, cls, stride)
        all_boxes.append(b)
        all_scores.append(s)
        all_classes.append(c)

    if len(all_boxes) == 0:
        return frame

    boxes = np.concatenate(all_boxes)
    scores = np.concatenate(all_scores)
    classes = np.concatenate(all_classes)

    keep = nms(boxes, scores, NMS_THRESH)

    for i in keep:

        x1, y1, x2, y2 = boxes[i]

        # scale back
        x1 = int(x1 * sx)
        y1 = int(y1 * sy)
        x2 = int(x2 * sx)
        y2 = int(y2 * sy)

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)

        cls = int(classes[i])
        class_name = CLASS_NAMES[cls]
    
        score = float(scores[i])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"{class_name}:{score:.2f}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    return frame


# ---------------- CAMERA STREAM ----------------
def run_camera(hef):

    print("Starting camera...")

    cam_cmd = [
        "rpicam-vid", "-t", "0",
        "--codec", "yuv420",
        "--width", str(CAM_WIDTH),
        "--height", str(CAM_HEIGHT),
        "--framerate", str(CAM_FPS),
        "--mode", "2304:1296:12:P",
        "--vflip", "--hflip",
        "-o", "-", "--nopreview",
    ]

    camera = subprocess.Popen(cam_cmd, stdout=subprocess.PIPE)

    frame_size = CAM_WIDTH * CAM_HEIGHT * 3 // 2

    frame_count = 0
    t_start = time.perf_counter()
    last_fps = 0.0

    gst_cmd = (
        f"gst-launch-1.0 fdsrc ! rawvideoparse format=bgr "
        f"width={DISPLAY_WIDTH} height={DISPLAY_HEIGHT} framerate={CAM_FPS}/1 ! "
        f"videoconvert ! queue ! waylandsink sync=false"
    )

    display = subprocess.Popen(gst_cmd, stdin=subprocess.PIPE, shell=True)

    with VDevice() as target:

        cfg = ConfigureParams.create_from_hef(
            hef,
            interface=HailoStreamInterface.PCIe
        )

        ng = target.configure(hef, cfg)[0]

        with ng.activate(ng.create_params()):

            input_params = InputVStreamParams.make(ng)
            output_params = OutputVStreamParams.make(
                ng,
                format_type=FormatType.FLOAT32
            )

            with InferVStreams(ng, input_params, output_params) as pipeline:

                input_name = list(input_params.keys())[0]

                print("Running... CTRL+C to stop")

                while True:

                    raw = camera.stdout.read(frame_size)
                    if len(raw) < frame_size:
                        break

                    yuv = np.frombuffer(raw, dtype=np.uint8)
                    yuv = yuv.reshape((CAM_HEIGHT * 3 // 2, CAM_WIDTH))

                    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    input_tensor, sx, sy = preprocess(frame)

                    t0 = time.perf_counter()
                    outputs = pipeline.infer({input_name: input_tensor})
                    infer_ms = (time.perf_counter() - t0) * 1000

                    result = postprocess(outputs, frame, sx, sy)

                    # ---------------- FPS CALC ----------------
                    frame_count += 1
                    now = time.perf_counter()
                    elapsed = now - t_start

                    if elapsed > 0:
                        fps = frame_count / elapsed
                    else:
                        fps = 0.0

                    # reset opcional para estabilidade numérico
                    if frame_count % 100 == 0:
                        t_start = now
                        frame_count = 0

                    # ---------------- DRAW FPS ----------------
                    cv2.putText(
                        result,
                        f"FPS: {fps:.1f} | INF: {infer_ms:.1f}ms",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

                    display_frame = cv2.resize(result, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

                    display.stdin.write(display_frame.tobytes())
                    display.stdin.flush()


# ---------------- MAIN ----------------
def main():

    if len(sys.argv) < 2:
        print("Usage: python main.py <model.hef>")
        sys.exit(1)

    hef_path = sys.argv[1]

    hef = HEF(hef_path)

    print(f"HEF loaded: {hef_path}")

    for info in hef.get_output_vstream_infos():
        print(info.name, info.shape)

    run_camera(hef)


if __name__ == "__main__":
    main()
