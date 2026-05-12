import cv2
import numpy as np
import argparse
import os


def nothing(x):
    pass


def is_image(path):
    return os.path.splitext(path)[1].lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]


def is_video(path):
    return os.path.splitext(path)[1].lower() in [".mp4", ".avi", ".mov", ".mkv", ".webm"]


def process_stream(cap=None, frame_static=None):
    is_static = frame_static is not None

    if is_static:
        frame = frame_static
        h, w = frame.shape[:2]
    else:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao ler vídeo.")
            return
        h, w = frame.shape[:2]

    cv2.namedWindow("Calibrador BEV")

    cv2.createTrackbar("Center X", "Calibrador BEV", 50, 100, nothing)
    cv2.createTrackbar("Top Y", "Calibrador BEV", 65, 100, nothing)
    cv2.createTrackbar("Top Width", "Calibrador BEV", 8, 50, nothing)
    cv2.createTrackbar("Bottom Y", "Calibrador BEV", 93, 100, nothing)
    cv2.createTrackbar("Bottom Width", "Calibrador BEV", 45, 100, nothing)

    paused = False

    while True:
        if not is_static and not paused:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

        cx = cv2.getTrackbarPos("Center X", "Calibrador BEV") / 100.0
        ty = cv2.getTrackbarPos("Top Y", "Calibrador BEV") / 100.0
        tw = cv2.getTrackbarPos("Top Width", "Calibrador BEV") / 100.0
        by = cv2.getTrackbarPos("Bottom Y", "Calibrador BEV") / 100.0
        bw = cv2.getTrackbarPos("Bottom Width", "Calibrador BEV") / 100.0

        src = np.float32([
            [cx - tw, ty],
            [cx + tw, ty],
            [cx + bw, by],
            [cx - bw, by]
        ])

        dst = np.float32([
            [0.25, 0],
            [0.75, 0],
            [0.75, 1],
            [0.25, 1]
        ])

        src_px = (src * [w, h]).astype(np.float32)
        dst_px = (dst * [w, h]).astype(np.float32)

        M = cv2.getPerspectiveTransform(src_px, dst_px)
        warped = cv2.warpPerspective(frame, M, (w, h))

        vis_orig = frame.copy()
        cv2.polylines(vis_orig, [src_px.astype(np.int32)], True, (0, 255, 0), 2)
        cv2.polylines(warped, [dst_px.astype(np.int32)], True, (0, 255, 255), 2)

        res = np.hstack((vis_orig, warped))
        cv2.imshow("Calibrador BEV", cv2.resize(res, (w, h // 2)))

        key = cv2.waitKey(20) & 0xFF

        if key == ord('q'):
            break
        elif key == ord(' ') and not is_static:
            paused = not paused
        elif key == ord('s'):
            print(f"\n--- SEUS PONTOS CALIBRADOS ---")
            print(f"DEFAULT_SRC = np.float32({src.tolist()})")
            print("------------------------------")

    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="Calibrador BEV para imagem ou vídeo")
    parser.add_argument("input", type=str, help="Caminho para imagem ou vídeo")

    args = parser.parse_args()
    path = args.input

    if not os.path.exists(path):
        print(f"Erro: arquivo não encontrado: {path}")
        return

    if is_image(path):
        img = cv2.imread(path)
        if img is None:
            print("Erro ao carregar imagem.")
            return

        process_stream(frame_static=img)

    elif is_video(path):
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"Erro ao abrir vídeo: {path}")
            return

        process_stream(cap=cap)

    else:
        print("Formato não suportado.")


if __name__ == "__main__":
    main()