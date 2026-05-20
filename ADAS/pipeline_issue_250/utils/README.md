# Utils Module

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [CanSender](#cansender)
  - [Display](#display)
  - [HardwareMonitor](#hardwaremonitor)
  - [Timer](#timer)
- [Telemetry](#telemetry)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Shared utilities for hardware communication, display output, and system monitoring. These modules have no ADAS domain logic — they are infrastructure used by `main.py` to interface with external systems.

## Classes

### `CanSender`
Sends commands to the vehicle microcontroller over the CAN bus via SocketCAN.

#### `__init__(channel="can0", bitrate=500000)`
Opens a SocketCAN interface on the specified channel.

#### `send_drive_command(can_id, throttle, steering)`
Sends throttle and steering in a single 4-byte CAN frame.

| Parameter | Type | Description |
|---|---|---|
| `can_id` | `int` | CAN arbitration ID (e.g. `0x002`) |
| `throttle` | `int` | Throttle value (`int16`) |
| `steering` | `float [-1, 1]` | Steering angle, scaled by 100 and packed as `int16` |

**Payload layout:** `[throttle int16 LE][steering×100 int16 LE]`

#### `send_int16(can_id, value)`
Sends a single `int16` value in a 2-byte CAN frame.

#### `send_steering_percent(can_id, percent)`
Clamps `percent` to `[-1.0, 1.0]`, scales by 100, and sends as `int16`.

#### `send_fsm_state(can_id, state_value)`
Sends the FSM state as a single unsigned byte.

#### `close()`
Shuts down the CAN bus interface. Must be called on pipeline exit.

---

### `Display`
Manages the visual output of the pipeline. Supports three modes: local (GStreamer Wayland), remote (JPEG over stdout), and none.

#### `__init__(width, height, fps, mode="local")`

| Parameter | Default | Description |
|---|---|---|
| `width`, `height` | `1260`, `400` | Output resolution |
| `fps` | `15` | Frame rate for the GStreamer pipeline |
| `mode` | `"local"` | `"local"` / `"remote"` / `"none"` |

#### `__enter__() / __exit__()`
Context Manager. On `__enter__`, starts the GStreamer process if mode is `"local"`. On `__exit__`, calls `close()`.

#### `show(frame)`
Resizes the frame to `(width, height)` and sends it to the configured output.

- `"local"` → writes raw RGB bytes to the GStreamer stdin pipe
- `"remote"` → encodes as JPEG (quality 80) and writes to `sys.stdout.buffer`
- `"none"` → no-op

#### `close()`
Terminates the GStreamer process if running.

---

### `HardwareMonitor`
Reads system metrics from the Raspberry Pi: CPU temperature and CPU usage.

#### `__init__()`
Initialises CPU stat baseline from `/proc/stat`.

#### `read_temp() → float`
Returns CPU temperature in °C from `/sys/class/thermal/thermal_zone0/temp`.

#### `get_cpu_usage() → (float, float)`
Returns `(cpu_used_%, cpu_free_%)` since the last call. Reads from `/proc/stat`.

---

### `Timer`
Handles stage execution timing and FPS calculation for performance monitoring.

#### `start_loop()`
Starts the timer for the main loop cycle.

#### `get_loop_duration() → float`
Returns elapsed time since `start_loop` in ms.

#### `start_stage(stage_name)`
Starts timing a specific pipeline stage.

#### `end_stage(stage_name) → float`
Ends timing a stage and returns duration in ms.

#### `get_fps() → float`
Returns FPS based on time elapsed since the last call.

#### `get_report() → str`
Returns a formatted string of all tracked stage timings.

---

## Telemetry

The pipeline logs performance metrics every frame to the console.

### FPS (Frames Per Second)
Calculated using the `Timer.get_fps()` method, measuring the frequency based on the time elapsed between the current and the last frame processing cycle, providing an **instantaneous FPS** rather than a global average.

### Cycle Time
The Cycle Time (logged as `Cycle: Xms`) measures the **total time spent** to process a single frame, starting from the camera capture and ending after the display stage, managed by `Timer.get_loop_duration()`.

This metric includes:
- Camera input
- Model inference (lane + object)
- Post-processing (lane + object)
- FSM processing
- PID calculation
- CAN command dispatch
- Display overlay rendering

## Debug

### Lifecycle logs (always active)
| Event | Level | Message |
|---|---|---|
| Display started (local) | `INFO` | `[DISPLAY] Started local display WxH @ Xfps` |
| Display started (remote) | `INFO` | `[DISPLAY] Started remote display (JPEG stdout)` |
| Display stopped | `INFO` | `[DISPLAY] Stopped` |
| CAN send failure | `print` | `CAN send failed` / `CAN send failed (drive command)` |

## Notes
- `CanSender` requires the `can0` interface to be up before instantiation: `ip link set can0 up type can bitrate 500000`.
- `Display` in `"local"` mode requires a running Wayland compositor (`WAYLAND_DISPLAY=wayland-1`, `XDG_RUNTIME_DIR=/run/user/200`).
- `HardwareMonitor` reads from `/proc/stat` and `/sys/class/thermal/` — only available on Linux.
- `Display.show()` performs a `cv2.resize()` on every frame — if performance is critical, pre-resize before calling.
