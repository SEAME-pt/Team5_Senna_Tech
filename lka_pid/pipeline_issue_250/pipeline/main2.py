import argparse
import logging
from camera.raspCam import Camera
from inference import HailoEngine, VDevice

# Configure logging to show DEBUG messages with timestamp
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


# Camera configuration
CAM_WIDTH, CAM_HEIGHT, CAM_FPS, DEBUG_CAM = 640, 360, 60, False
# Inference configuration
DEBUG_INFERENCE = True


def main():

    # -----------------------------------------------------------------------
    # Parse command-line arguments for HEF file paths
    # -----------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("lane_hef", help="Path to the lane inference HEF file")
    parser.add_argument("object_hef", help="Path to the object inference HEF file")
    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # Initialize Hailo Engines and Camera using Context Managers for automatic cleanup
    # -----------------------------------------------------------------------
    with VDevice() as target:
        with HailoEngine(args.lane_hef, target, debug=DEBUG_INFERENCE) as engine_lane, \
            HailoEngine(args.object_hef, target, debug=DEBUG_INFERENCE) as engine_obj, \
            Camera(CAM_WIDTH, CAM_HEIGHT, CAM_FPS, debug=DEBUG_CAM) as cam:
            try:
                while True:
                    # Read one RGB frame from the camera
                    rgb = cam.read_frame()
                    if rgb is None:
                        break

                    outputs_lane = engine_lane.infer(rgb)
                    outputs_obj = engine_obj.infer(rgb)

                    if DEBUG_INFERENCE:
                        logging.debug("[MAIN2] lane outputs: %s", list(outputs_lane.keys()))
                        logging.debug("[MAIN2] object outputs: %s", list(outputs_obj.keys()))
            except KeyboardInterrupt:
                # User pressed Ctrl+C — shutdown gracefully
                print("\nShutting down...")
    # -----------------------------------------------------------------------
    # All resources (Hailo engines and camera) are automatically released here due to context managers
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    main()
