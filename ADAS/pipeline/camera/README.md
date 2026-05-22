# Camera Module

## Index
- [Overview](#overview)
- [Hardware](#hardware)
- [API / Methods](#api--methods)
- [Data Contract](#data-contract)
- [Notes](#notes)

## Overview
Captures video frames in a background thread and provides them to the pipeline in RGB format via a non-blocking interface.

## Hardware
- **Model:** Raspberry Pi Camera Module 3 (Wide NoIR)
- **Sensor:** Sony IMX708
- **Reference:** https://www.raspberrypi.com/products/camera-module-3/

## API / Methods

### `Camera.__init__(width, height, fps, debug=False)`
Stores the camera configuration and calculates the expected size of each frame in bytes.

#### Parameters
- `width` and `height` define the capture resolution.
- `fps` defines the nominal frames per second rate.
- `debug` enables additional logs per frame.

#### Effects
- Initializes `self.process`, `self._thread`, and `self._latest_frame` as `None`.
- Prepares the YUV420 frame size used for pipe reading.

### `Camera._read_exact(pipe, size)`
Reads exactly `size` bytes from `pipe`, blocking until all bytes are available.

#### Behavior
- Loops until the full frame is accumulated in a buffer.
- Returns `None` if the pipe closes before delivering the expected number of bytes.

#### Output
- `bytes` of length `size`, or `None` on pipe EOF.

### `Camera._capture_loop()`
Background thread loop that continuously reads and decodes frames from the camera pipe.

#### Behavior
- Runs while `self._running` is `True`.
- Calls `_read_exact()` to get a raw YUV420 frame.
- Converts to RGB and stores the result in `self._latest_frame` under a lock.
- Skips silently on incomplete reads (`None`).

#### Effects
- Keeps `self._latest_frame` updated with the most recent frame at all times.

### `Camera.__enter__()`
Starts the `rpicam-vid` process and launches the background capture thread.

#### Behavior
- Checks if another `rpicam-vid` process is already active.
- If it exists, does not start a second process and simply returns the instance.
- If it does not exist, executes `rpicam-vid` with output directed to the pipe (`stdout`).
- Starts a daemon thread (`_capture_loop`) that continuously reads and decodes frames.

#### Effects
- Creates `self.process` using `subprocess.Popen`.
- Starts `self._thread` — frames are available immediately via `get_frame()`.

### `Camera.get_frame()`
Returns the latest decoded frame. Non-blocking — always returns immediately.

#### Behavior
- Thread-safe: uses a lock to access the latest frame.
- Returns `None` if no frame has been captured yet.
- Returns a copy of the latest frame to avoid race conditions.

#### Output
- `numpy.ndarray` in RGB with shape `(height, width, 3)`, or `None` if no frame is available yet.

### `Camera.stop()`
Stops the background thread and terminates the camera process.

#### Behavior
- Sets `self._running = False` to signal the capture thread to exit.
- Terminates the `rpicam-vid` process and waits for it to finish.

### `Camera.__exit__(exc_type, exc_val, exc_tb)`
Calls `stop()` upon exiting the context, ensuring all resources are released.

## Data Contract
| Field | Type | Shape | Meaning |
|---|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(360, 640, 3)` | Frame delivered to the rest of the pipeline |

> The native camera format is `YUV420`. The module internally converts to RGB before delivering to the pipeline.

## Configuration
| Parameter | Value | Description |
|---|---|---|
| `width` | `640` | Frame width |
| `height` | `360` | Frame height |
| `fps` | `15` | Frames per second |
| `frame_size` | `width * height * 3 // 2` | YUV420 size in bytes |
| `--mode` | `640:360:8:P` | Sensor crop mode |
| `--exposure` | `sport` | Fast shutter exposure mode |
| `--shutter` | `3500` | Fixed shutter speed in microseconds |
| `--denoise` | `off` | Disables denoising for lower latency |
| `--vflip` / `--hflip` | enabled | Corrects physical mounting orientation of the camera |

## YUV420 Format
The sensor captures in YUV420 — a raw format that separates brightness (Y) from color (U, V):
- Y Plane: `640 × 360 = 230400 bytes` (1 value per pixel)
- U Plane: `57600 bytes` (1 value per every 4 pixels)
- V Plane: `57600 bytes` (1 value per every 4 pixels)
- Total: `345600 bytes` = `640 × 360 × 1.5`

The `reshape((540, 640))` organizes bytes into a matrix where Y occupies the first 360 rows and U+V the remaining 180.
`cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)` combines the 3 planes and returns RGB `(360, 640, 3)`.

We use RGB because it is the format expected by YOLO models on Hailo.

> For more info: [YUV420 format](https://en.wikipedia.org/wiki/YUV#Y%E2%80%B2UV420p_and_Y%E2%80%B2V12_or_YV12_to_RGB888_conversion)

## Threading Architecture
The capture runs in a background daemon thread (`_capture_loop`). This ensures:
- The main pipeline loop is never blocked waiting for a frame.
- `get_frame()` always returns the most recent available frame instantly.
- A `threading.Lock` protects `_latest_frame` from concurrent access.

## Debug

The module has two levels of logging that work independently:

### Lifecycle logs (always active)
These logs are always emitted regardless of the `debug` flag:

| Event | Level | Message |
|---|---|---|
| Camera started | `INFO` | `[CAMERA] Started 640x360 @ 15fps` |
| Camera stopped | `INFO` | `[CAMERA] Stopped` |
| Stuck process detected | `WARNING` | `[CAMERA] rpicam-vid already running with PID=<pid>. If safe, run: kill <pid>` |

### Per-frame logs (`debug=True`)
Only emitted when `Camera(..., debug=True)`:

| Event | Level | Message |
|---|---|---|
| Frame decoded | `DEBUG` | `[CAMERA] frame shape=(360, 640, 3) dtype=uint8` |

### How to enable
```python
cam = Camera(640, 360, 15, debug=True)
```
And ensure the logging level is set to `DEBUG`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Notes
- The first frame takes ~400ms (camera initialization), subsequent ones ~17ms (~60 FPS)
- If the pipeline crashes abruptly, the `rpicam-vid` process might stay stuck — check with `pgrep -f rpicam-vid` and terminate with `kill <PID>`
- The module automatically detects stuck processes and warns in the log — it does not kill them without user confirmation
- Camera parameters (`--mode`, `--exposure`, `--shutter`, `--denoise`) were validated on the RPi and should not be changed without testing
