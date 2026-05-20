from ultralytics import YOLO
import cv2
import argparse
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 detecção - imagem ou vídeo")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--image", type=str, help="Caminho para imagem")
    group.add_argument("--video", type=str, help="Caminho para vídeo")
    group.add_argument("--webcam", type=str, help="Caminho para webcam")

    parser.add_argument("--model", type=str, default="best.pt", help="Caminho do modelo")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")

    return parser.parse_args()


def run_image(model, image_path, conf):
    results = model.predict(image_path, conf=conf)

    result = results[0]

    # Desenha bounding boxes
    img = result.plot()

    cv2.imshow("Resultado - Imagem", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_video(model, video_path, conf):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        sys.exit(1)

    cv2.namedWindow("YOLOV8 - Object detection", cv2.WINDOW_NORMAL)

    prev_time = 0

    while True:
        
        ret, frame = cap.read()
        if not ret:
            break

        # Inferência
        results = model.predict(frame, conf=conf, verbose=False)
        result = results[0]

        # Desenhar boxes
        annotated_frame = result.plot()

        cv2.imshow("YOLO - Object detection", annotated_frame)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_webcam(model, webcam_path, conf):
    cap = cv2.VideoCapture(webcam_path)

    if not cap.isOpened():
        print("Erro ao abrir a webcam")
        return

    cv2.namedWindow("YOLO - Object detection - webcam", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Erro ao ler frame")
            break

        # Inferência
        results = model(frame, conf=conf)  # mais direto que predict()
        result = results[0]

        annotated_frame = result.plot()

        cv2.imshow("YOLO - Object detection - webcam", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    args = parse_args()

    # Carregar modelo
    model = YOLO(args.model)

    if args.image:
        run_image(model, args.image, args.conf)

    elif args.video:
        run_video(model, args.video, args.conf)

    elif args.webcam: #passar /dev/video0 como argumento
        run_webcam(model, args.webcam, args.conf)


if __name__ == "__main__":
    main()
