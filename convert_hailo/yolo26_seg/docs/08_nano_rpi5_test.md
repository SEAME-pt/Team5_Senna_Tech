# YOLO26n-seg Test on RPi5 — test_yolo26_hailo3.py

Inference script for the nano model (yolo26n_seg_640.hef) with the full pipeline:
Hailo-8 → mask → BEV → sliding windows → CTE.

---

## Location

| File | Where |
|---|---|
| Script | `~/test_yolo26_hailo3.py` (RPi5) |
| HEF | `~/yolo26n_seg_640.hef` (RPi5) |
| Source | `convert_hailo/yolo26_seg/scripts/test_yolo26_hailo3.py` (host) |

---

## Execution modes

### 1. Camera mode — local display (Wayland on RPi5)

```bash
python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef
```

Opens `waylandsink` on the screen connected to the RPi5.

---

### 2. Camera mode — no display (terminal only)

```bash
python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef --no-display
```

Useful for measuring FPS/latency without display overhead.

---

### 3. Camera mode — remote (MJPEG stream via SSH)

On the host machine, redirects MJPEG output and opens with ffplay:

```bash
ssh <rpi5-host> "python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef --remote" \
  | ffplay -f mjpeg -i pipe:0 -loglevel quiet
```

`--remote` disables `waylandsink` and sends JPEG-encoded frames to stdout.
JPEG quality: 80. Display resolution: 1260×400.

---

### 4. Image mode

```bash
python3 test_yolo26_hailo3.py image photo.jpg yolo26n_seg_640.hef
# saves result_photo.jpg
```

---

### 5. Custom threshold

Third argument (camera) or fourth (image):

```bash
python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef 0.15
python3 test_yolo26_hailo3.py image photo.jpg yolo26n_seg_640.hef 0.15
```

Default: `0.25`. With the nano model (sparse detections) values of 0.15–0.20 give
more mask coverage.

---

## Camera and capture

| Parameter | Current value |
|---|---|
| Camera | Raspberry Pi Camera Module 3 (IMX708, 16:9, ~66° FOV) |
| Capture resolution | 640×360 |
| Sensor mode | `--mode 2304:1296:12:P` (2×2 binning, maximum FOV) |
| Target FPS | 30 |
| Flip | `--vflip --hflip` |

> **FOV note**: Camera Module 3 is natively 16:9. Capturing at 640×360 (16:9) already
> uses the full sensor. For ~102° a **v3 Wide** version would be required.

---

## Post-processing parameters (SlidingWindowsLaneFitter)

| Parameter | Value | Description |
|---|---|---|
| `n_windows` | 9 | Vertical sliding windows in BEV |
| `margin` | 80 | Search width per window (px) |
| `min_pixels` | 50 | Minimum white pixels for a valid window |
| `alpha` (smooth) | 0.25 | Weight of current frame in temporal smoothing |
| `TOP_K` | 200 | Maximum detections considered |
| `SCORE_THRESHOLD` | 0.25 | Detection confidence threshold |

---

## BEV trapezoid (DEFAULT_SRC)

Normalized coordinates [x, y] of the region of interest in the original image
that is transformed to bird's-eye view:

```python
[0.255, 0.44], [0.745, 0.44],  # top-left, top-right
[1.17,  1.00], [-0.17, 1.00]  # bottom-right, bottom-left
```

Calibrated for the current camera position on the vehicle with ~66° FOV.

---

## HEF output format (pre_concat4)

The nano HEF exposes 4 tensors (cut before Concat_4):

| Tensor | Shape | Content |
|---|---|---|
| `ew_mult1` | (1,1,8400,4) | bbox coords |
| `activation3` | (1,1,8400,1) | scores |
| `concat22` | (1,1,8400,32) | mask coefficients |
| `output1` | (1,160,160,32) | proto masks |

Different from the small (yolo26s) which exposes `(1,300,38) + proto`.
The `pre_concat4` mode is detected automatically in `find_output_keys()`.

---

## Measured performance (06/04/2026)

| Metric | Value |
|---|---|
| Hailo latency (HW) | ~10–15 ms |
| Camera FPS | ~21 fps |
| Mask coverage | ~2% (sparse detections — nano characteristic) |
| HEF size | 9.1 MB |
| Compilation contexts | 3 |

---

## Transfer to RPi5

```bash
# From host:
scp convert_hailo/yolo26_seg/scripts/test_yolo26_hailo3.py <rpi5-host>:~/
```

---

## Current state (06/04/2026) — pending items

- Yellow center line still shows temporal variation (unstable polyfit
  with 2% mask coverage). Smoothing at `alpha=0.25`.
- Line is drawn on BEV overlay and unwarped — partial transparency (0.4
  addWeighted) is the current accepted behaviour.
- Trapezoid calibrated and visually validated.
- Possible future improvement: increase mask coverage by adjusting threshold
  or training with more lane data.
