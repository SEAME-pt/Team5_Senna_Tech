# Camera Module

## Index
- [Overview](#overview)
- [Hardware](#hardware)
- [API / Methods](#api--methods)
- [Data Contract](#data-contract)
- [Notes](#notes)

## Overview
Captures video frames and provides them to the pipeline in RGB format.

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
- Initializes `self.process` as `None`.
- Prepares the YUV420 frame size used for pipe reading.

### `Camera.__enter__()`
Starts the `rpicam-vid` process and prepares continuous capture.

#### Behavior
- Checks if another `rpicam-vid` process is already active.
- If it exists, does not start a second process and simply returns the instance.
- If it does not exist, executes `rpicam-vid` with output directed to the pipe (`stdout`).

#### Effects
- Creates `self.process` using `subprocess.Popen`.
- Makes frames available for `read_frame()`.

### `Camera.read_frame()`
Reads a raw frame from the pipe, converts it from YUV420 to RGB, and returns the frame ready for the pipeline.

#### Behavior
- Fails safely if the camera is not active.
- Reads exactly the number of bytes expected per frame.
- Returns `None` if the pipe does not produce a complete frame.
- Converts the buffer to a `numpy.ndarray` and then to RGB.

#### Output
- `numpy.ndarray` in RGB with shape `(height, width, 3)`, or `None` in case of failure/incomplete reading.

### `Camera.__exit__(exc_type, exc_val, exc_tb)`
Terminates the camera process upon exiting the context.

#### Behavior
- Terminates the `rpicam-vid` process if it exists.
- Waits for the process to finish before exiting.

#### Effects
- Releases process resources captured by the context.

## Data Contract
| Field | Type | Shape | Meaning |
|---|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(360, 640, 3)` | Frame delivered to the rest of the pipeline |

> The native camera format is `YUV420`. The module internally converts to RGB before delivering to the pipeline.

## Notes
In the pipeline data flow, the camera is the first functional stage, as it originates the frames consumed by subsequent stages.

However, this does not mean it must always be the first resource initialized during application execution. In scenarios where inference depends on dedicated hardware like Hailo, it may make sense to initialize the inference infrastructure first and open the camera only after the system is ready to consume frames.

This distinction is important:

- In the data flow, the camera comes first;
- In the resource initialization order, it may come after inference preparation.

This choice avoids opening continuous capture before the rest of the pipeline is ready to process the generated data.

## Configuration
| Parameter | Value | Description |
|---|---|---|
| `width` | `640` | Frame width |
| `height` | `360` | Frame height |
| `fps` | `60` | Frames per second |
| `frame_size` | `width * height * 3 // 2` | YUV420 size in bytes |

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

## Notes
- The first frame takes ~400ms (camera initialization), subsequent ones ~17ms (~60 FPS)
- Dynamic FPS could be implemented via a `@property` setter by restarting the process
- If the pipeline crashes abruptly, the `rpicam-vid` process might stay stuck — check with `pgrep -f rpicam-vid` and terminate with `kill <PID>`
- The module automatically detects stuck processes and warns in the log — it does not kill them without user confirmation
