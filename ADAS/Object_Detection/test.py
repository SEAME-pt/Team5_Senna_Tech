import cv2
import numpy as np
import time

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

VIDEO_PATH = "pista02.avi"
HEF_PATH = "yolo26n_v2.hef"
OUTPUT_IMAGE = "resultado.jpg"

NET_SIZE = 640
NUM_CLASSES = 13

CONF_THRESH = 0.25
NMS_THRESH = 0.45


# -------------------- PREPROCESS --------------------
def preprocess(frame):

    h0, w0 = frame.shape[:2]

    img = cv2.resize(frame, (NET_SIZE, NET_SIZE))

    scale_x = w0 / NET_SIZE
    scale_y = h0 / NET_SIZE

    img = img.astype(np.uint8)

    return np.expand_dims(img, axis=0), scale_x, scale_y


# -------------------- UTIL --------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def make_grid(h, w):
    y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    return np.stack((x, y), axis=-1)


# -------------------- DECODE YOLO HAILO --------------------
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

    boxes = np.stack([x1, y1, x2, y2], axis=-1)

    boxes = boxes.reshape(-1, 4)
    cls = cls.reshape(-1, NUM_CLASSES)

    scores = np.max(cls, axis=1)
    classes = np.argmax(cls, axis=1)

    mask = scores > CONF_THRESH

    return boxes[mask], scores[mask], classes[mask]


# -------------------- NMS --------------------
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
        iou = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return keep


# -------------------- POSTPROCESS --------------------
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

        # 🔥 ESCALA DE VOLTA PARA IMAGEM ORIGINAL
        x1 = int(x1 * sx)
        y1 = int(y1 * sy)
        x2 = int(x2 * sx)
        y2 = int(y2 * sy)

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)

        cls = int(classes[i])
        score = float(scores[i])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"{cls}:{score:.2f}",
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    return frame


# -------------------- RUN --------------------
def run_one_frame(hef):

    cap = cv2.VideoCapture(VIDEO_PATH)
    ret, frame = cap.read()

    if not ret:
        print("Erro ao ler frame")
        return

    with VDevice() as target:

        cfg = ConfigureParams.create_from_hef(
            hef,
            interface=HailoStreamInterface.PCIe
        )

        network_group = target.configure(hef, cfg)[0]

        with network_group.activate(network_group.create_params()):

            input_params = InputVStreamParams.make(network_group)
            output_params = OutputVStreamParams.make(
                network_group,
                format_type=FormatType.FLOAT32
            )

            with InferVStreams(network_group, input_params, output_params) as pipeline:

                input_name = list(input_params.keys())[0]

                input_tensor, sx, sy = preprocess(frame)

                start = time.perf_counter()

                outputs = pipeline.infer({
                    input_name: input_tensor
                })


                result = postprocess(outputs, frame, sx, sy)

                cv2.imwrite(OUTPUT_IMAGE, result)
                print("Inference:", (time.perf_counter() - start) * 1000, "ms")

                print("Saved:", OUTPUT_IMAGE)

    cap.release()


# -------------------- MAIN --------------------
def main():

    hef = HEF(HEF_PATH)

    print("HEF loaded")

    for info in hef.get_output_vstream_infos():
        print(info.name, info.shape)

    run_one_frame(hef)


if __name__ == "__main__":
    main()