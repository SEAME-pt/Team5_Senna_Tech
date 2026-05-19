import argparse
import logging
from camera.raspCam import Camera
from inference import HailoEngine, VDevice
from post_processing.lane.lane_post_processing import YoloSegDecoder, MaskFilters

# Configure logging to show INFO messages with timestamp
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


# Camera configuration
CAM_WIDTH, CAM_HEIGHT, CAM_FPS = 640, 360, 60


def main():

    # -----------------------------------------------------------------------
    # Parse command-line arguments for HEF file paths
    # -----------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("lane_hef", help="Path to the lane inference HEF file")
    parser.add_argument("object_hef", help="Path to the object inference HEF file")
    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # Initialize Post-processing components
    # -----------------------------------------------------------------------
    lane_decoder = YoloSegDecoder(score_threshold=0.3, debug=True)
    lane_filters = MaskFilters(debug=False)

    # -----------------------------------------------------------------------
    # Initialize Hailo Engines and Camera using Context Managers
    # -----------------------------------------------------------------------
    with VDevice() as target:
        with HailoEngine(args.lane_hef, target, debug=False) as engine_lane, \
            HailoEngine(args.object_hef, target, debug=False) as engine_obj, \
            Camera(CAM_WIDTH, CAM_HEIGHT, CAM_FPS, debug=False) as cam:

            logging.info("[MAIN2] Pipeline started with Lane Post-processing.")

            try:
                while True:
                    # Read one RGB frame from the camera
                    rgb = cam.read_frame()
                    if rgb is None:
                        break

                    # Inference
                    outputs_lane = engine_lane.infer(rgb)
                    outputs_obj = engine_obj.infer(rgb)

                    # --- Lane Post-processing ---
                    # 1. Decode raw outputs to binary mask
                    binary_mask = lane_decoder.decode_to_mask(outputs_lane, CAM_HEIGHT, CAM_WIDTH)

                    # 2. Apply morphological filters (Close/Open)
                    clean_mask = lane_filters.process(binary_mask)

            except KeyboardInterrupt:
                # User pressed Ctrl+C — shutdown gracefully
                logging.info("\n[MAIN2] Shutting down...")
    # -----------------------------------------------------------------------
    # All resources (Hailo engines and camera) are automatically released here due to context managers
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    main()
