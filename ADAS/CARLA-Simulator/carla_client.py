from Vehicle import Vehicle, IMG_HEIGHT, IMG_WIDTH
from CarlaEnvironment import CarlaEnvironment
import time
import cv2
import queue
from pid_control.pid import PID
from YOLOv8Detector import YOLOv8Detector
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from LKA.pipeline.lka.LKAPipeline import LKAPipeline

def record_video_from_queue(image_queue, duration_sec=60, fps=20, filename="carla_rgb.mp4"):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(
        filename,
        fourcc,
        fps,
        (IMG_WIDTH, IMG_HEIGHT)
    )

    max_frames = duration_sec * fps
    frame_count = 0

    print("Gravando vídeo...")

    return out, frame_count, max_frames

def main():

    pipeline = LKAPipeline(
        model_path="../LKA/LKA_trained_models/yolov26sseg_cltusm_v1.pt",  # ou outro
        image_width=IMG_WIDTH,
        image_height=IMG_HEIGHT,
        conf_threshold=0.3
    )
    pid = PID(kp=0.3, ki=0.0, kd=0.001)
    """
    yolov8n_detector = YOLOv8Detector("../LKA/LKA_trained_models/yolov8n_seg_3_datasets.pt")
    yolov8s_detector = YOLOv8Detector("../LKA/LKA_trained_models/yolov8s_seg_3_datasets.pt") 
    yolov8_detector = YOLOv8Detector("../LKA/LKA_trained_models/custom_yolo_v2.pt")"""

    best = YOLOv8Detector("../LKA/LKA_trained_models/yolov26sseg_cltusm_v1.pt")
    image_queue = queue.Queue()
    image_queue_seg = queue.Queue()

    env = CarlaEnvironment()
    vehicle = Vehicle(env, image_queue, image_queue_seg, pid)
    env.create_traffic()
    
    try:

        while True:

            env.world.tick()

            #discomment to update weather randomly at each iteration
            # env.update_weather()

            if not image_queue.empty() and not image_queue_seg.empty():
                
                bgr, rgb = image_queue.get()
                
                fit_result, annotated = pipeline.process(rgb)

                cte = fit_result.cte_normalized

                vehicle.pid_control_for_steering(cte, pid, annotated)
                
                cv2.imshow("LKA + PID", annotated)
                 
                #seg = image_queue_seg.get()
                #yolo_result, lane_mask = yolov8_detector.infer(bgr)
                #yolo_result3, lane_mask3 = yolov8n_detector.infer(bgr)
                #yolo_result2, lane_mask2 = yolov8s_detector.infer(bgr)
                best_result, lane_mask4 = best.infer(bgr)
                
                #cv2.imshow("YOLOv8 old custom trained", yolo_result)
                #cv2.imshow("YOLOv8n custom trained", yolo_result2)
                #cv2.imshow("YOLOv8s custom trained", yolo_result3)
                cv2.imshow("YOLOv8s-seg prediction", best_result)
               
            cv2.waitKey(1)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Closing...")

    finally:

        cv2.destroyAllWindows()
        vehicle.destroy()
        #video_writer.release()
        # Desativa modo síncrono ao finalizar
        settings = env.world.get_settings()
        settings.synchronous_mode = False
        env.world.apply_settings(settings)


if __name__ == "__main__":
    main()