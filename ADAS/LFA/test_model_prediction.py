from ultralytics import YOLO
import cv2
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="YOLO inference em imagem ou vídeo")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--image",
        type=str,
        help="Caminho para a imagem"
    )

    group.add_argument(
        "--video",
        type=str,
        help="Caminho para o vídeo"
    )

    return parser.parse_args()


def run_image(model, image_path):
    results = model.predict(image_path, conf=0.25)
    result = results[0]

    print("OUTPUT .PT=", results)

    img = result.plot(boxes=False)

    cv2.imshow("Resultado - Imagem", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_video(model, video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        sys.exit(1)

    # Criar janela UMA vez
    cv2.namedWindow("Resultado - Vídeo", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, conf=0.25, verbose=False)
        result = results[0]

        annotated_frame = result.plot(boxes=False)

        # Reutiliza a mesma janela
        cv2.imshow("Resultado - Vídeo", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    args = parse_args()

    model = YOLO("LKA_trained_models/yolov26sseg_cltusm_v1.pt")

    if args.image:
        run_image(model, args.image)

    elif args.video:
        run_video(model, args.video)


if __name__ == "__main__":
    main()