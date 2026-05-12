"""
Offline Test — no CARLA required
=================================
Tests the full LKA pipeline on:
  - A single image file  (jpg, png, etc.)
  - A video file         (.mp4, .avi, etc.)
  - Your webcam          (device index 0)

Usage:
    # Test with an image
    python test_offline.py --source path/to/image.jpg

    # Test with a video
    python test_offline.py --source path/to/video.mp4

    # Test with webcam
    python test_offline.py --source 0

    # Also save the annotated output
    python test_offline.py --source path/to/video.mp4 --save

    # Show BEV debug windows as well
    python test_offline.py --source path/to/image.jpg --debug
"""

import cv2
import numpy as np
import argparse
import os
import time

from pipeline.lka.LKAPipeline import LKAPipeline


# =============================================================================
# CONFIGURATION
# =============================================================================

MODEL_PATH = "weights/best.pt"   # Change to your model path
SAVE_DIR   = "debug_frames"

# =============================================================================


def parse_args():
    parser = argparse.ArgumentParser(description="LKA Pipeline — Offline Test")
    parser.add_argument("--source", type=str, required=True,
                        help="Image path, video path, or webcam index (0)")
    parser.add_argument("--model",  type=str, default=MODEL_PATH,
                        help="Path to YOLOv8-seg weights (.pt)")
    parser.add_argument("--conf",   type=float, default=0.25,
                        help="Detection confidence threshold (default: 0.25)")
    parser.add_argument("--save",   action="store_true",
                        help="Save annotated output to disk")
    parser.add_argument("--debug",  action="store_true",
                        help="Show BEV + sliding windows debug windows")
    return parser.parse_args()


def run_on_image(pipeline: LKAPipeline, image_path: str, args):
    """Test on a single image file."""
    frame_bgr = cv2.imread(image_path)
    if frame_bgr is None:
        print(f"[ERROR] Cannot read image: {image_path}")
        return

    h, w = frame_bgr.shape[:2]
    print(f"[Test] Image loaded: {w}x{h}  ({image_path})")

    # Convert to RGB for the pipeline
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Run pipeline
    t0 = time.time()
    fit_result, annotated = pipeline.process(frame_rgb, draw_debug=args.debug)
    elapsed_ms = (time.time() - t0) * 1000

    # Print results
    print(f"\n{'='*50}")
    print(f"  CTE (pixels): {fit_result.cte_pixels}")
    print(f"  CTE (metres): {fit_result.cte_meters}")
    print(f"  Left  lane:   {'FOUND' if fit_result.left_found  else 'NOT FOUND'}")
    print(f"  Right lane:   {'FOUND' if fit_result.right_found else 'NOT FOUND'}")
    print(f"  Processing:   {elapsed_ms:.1f} ms")
    print(f"{'='*50}\n")

    # Show result
    cv2.namedWindow("LKA Pipeline — Video Test", cv2.WINDOW_NORMAL)
    cv2.imshow("LKA Pipeline — Image Test", annotated)

    if args.debug and fit_result.debug_image is not None:
        cv2.namedWindow("BEV + Sliding Windows", cv2.WINDOW_NORMAL)
        cv2.imshow("BEV + Sliding Windows", fit_result.debug_image)

    # Save if requested
    if args.save:
        os.makedirs(SAVE_DIR, exist_ok=True)
        base = os.path.splitext(os.path.basename(image_path))[0]
        out_path = os.path.join(SAVE_DIR, f"{base}_annotated.jpg")
        cv2.imwrite(out_path, annotated)
        print(f"[Test] Saved: {out_path}")

    print("Press any key to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_on_video(pipeline: LKAPipeline, source, args):
    try:
        source = int(source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(source)          
    if not cap.isOpened():
        return

    # Define windows before the loop to ensure they are resizable
    cv2.namedWindow("LKA Pipeline", cv2.WINDOW_NORMAL)
    if args.debug:
        cv2.namedWindow("Debug BEV", cv2.WINDOW_NORMAL)

    paused = False
    show_debug = args.debug

    while True:
        if not paused:   
            ret, frame_bgr = cap.read()
            if not ret:
                break

            # resize frame before processing to ensure speed and visibility
            #frame_bgr = cv2.resize(frame_bgr, (1280, 720)) 
            
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            fit_result, annotated = pipeline.process(frame_rgb, draw_debug=show_debug)

            # Show the result in the correct window
            cv2.imshow("LKA Pipeline", annotated)
            
            if show_debug and fit_result.debug_image is not None:
                cv2.imshow("Debug BEV", fit_result.debug_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord(" "):
            paused = not paused
        elif key == ord("d"):
            show_debug = not show_debug
            if not show_debug: cv2.destroyWindow("Debug BEV")

    cap.release()
    cv2.destroyAllWindows()


def main():
    args = parser = parse_args()

    # ── Determine input size ──────────────────────────────────────────────────
    # For images we read the size after loading.
    # For video/webcam we read it from the capture object.
    # The pipeline needs to know the size at init time for BEV calibration,
    # so we probe the source first.

    source = args.source
    is_image = False

    try:
        int(source)   # webcam index
        probe_w, probe_h = 1280, 720
    except ValueError:
        ext = os.path.splitext(source)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".bmp", ".tiff"):
            is_image = True
            img = cv2.imread(source)
            if img is None:
                print(f"[ERROR] Cannot read: {source}")
                return
            probe_h, probe_w = img.shape[:2]
        else:
            cap = cv2.VideoCapture(source)
            probe_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            probe_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()

    print(f"[Test] Source size: {probe_w}x{probe_h}")

    # ── Initialise pipeline ──────────────────────────────────────────────────
    pipeline = LKAPipeline(
        model_path=args.model,
        image_width=probe_w,
        image_height=probe_h,
        conf_threshold=args.conf,
    )

    # ── Run test ─────────────────────────────────────────────────────────────
    if is_image:
        run_on_image(pipeline, source, args)
    else:
        run_on_video(pipeline, source, args)

if __name__ == "__main__":
    main()
