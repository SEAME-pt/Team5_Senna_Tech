import logging
from camera.raspCam import Camera

# Configure logging to show DEBUG messages with timestamp
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


# Camera configuration
CAM_WIDTH, CAM_HEIGHT, CAM_FPS, DEBUG_CAM = 640, 360, 60, False

def main():
    # -----------------------------------------------------------------------
    # Camera module is started and stopped automatically via Context Manager
    # -----------------------------------------------------------------------
    with Camera(CAM_WIDTH, CAM_HEIGHT, CAM_FPS, debug=DEBUG_CAM) as cam:
        try:
            while True:
                # Read one BGR frame from the camera
                bgr = cam.read_frame()
                if bgr is None:
                    break
        except KeyboardInterrupt:
            # User pressed Ctrl+C — shutdown gracefully
            print("\nShutting down...")
    # -----------------------------------------------------------------------
    # Camera process is automatically terminated here due to Context Manager
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    main()
