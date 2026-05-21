# ADAS Pipeline

## Index
- [Overview](#overview)
- [Data Flow](#data-flow)
- [Rules for `main`](#rules-for-main)
- [Rules for New Modules](#rules-for-new-modules)
- [Module Documentation](#module-documentation)
- [Cross-Cutting Documentation](#cross-cutting-documentation)

## Overview
Execution pipeline for the ADAS prototype running on Raspberry Pi 5 + Hailo-8 NPU. Two YOLO models run in parallel on the same `VDevice`: `yolo26n_seg_640.hef` for lane segmentation and `yolo26n_v4.hef` for object/sign detection (13 custom classes). The pipeline is a synchronous main loop with real wall-clock `dt` fed to the PID on every cycle.

**Color space invariant:** the entire pipeline uses **RGB**. `rpicam-vid` outputs YUV420; `camera/` converts to RGB immediately. All downstream modules — inference, post-processing, display — receive and return RGB frames. Do not insert BGR conversions.

Entry point: `main.py`

### Key Parameters (defined in `main.py`)

| Parameter | Value | Description |
|---|---|---|
| Camera resolution | 640 × 360 | Input frame size; also BEV output size |
| Camera FPS | 15 | `rpicam-vid` target frame rate |
| Display resolution | 1260 × 400 | Output display / stream size |
| PID gains | kp=1.3, ki=0.1, kd=0.1 | Steering controller; `dt` from real loop time |
| `lane_offset` | 0.80 | Normalized CTE shift during avoidance maneuver |
| `blind_wait_time` | 2.5 s | Time to wait after obstacle disappears before returning |
| `return_duration_s` | 1.5 s | Duration of linear CTE lerp back to center |
| `area_brake_threshold` | 0.060 | Frame-over-frame area delta that triggers EMERGENCY |
| `area_avoidance_min` | 0.010 | Minimum obstacle BBox area (relative) to enter avoidance |
| `frames_to_confirm` | 4 | Consecutive in-corridor frames before avoidance activates |

## Usage

To execute the pipeline, provide the paths to the Lane Detection and Object Detection HEF models:

```bash
python3 main.py <lane_model.hef> <object_model.hef> [options]
```

### Options
- `--remote`: Streams JPEG-encoded frames to stdout (80% quality). Useful over SSH.
- `--no-display`: Headless mode — skips all display rendering (saves CPU).
- `--virtual`: Skips CAN send. Throttle and steering are computed but not transmitted. Safe for bench testing.

**Prerequisites:** HailoRT driver with `force_desc_page_size=4096` fix (see `docs/AGL/AGL_hailo_PCIe_config.md`), `can0` interface up, `rpicam-vid` available. Both HEF files must exist at the paths provided.

## Data Flow

| Step | Module | Input | Output |
|---|---|---|---|
| 01 | Camera | — | `rgb (H, W, 3) uint8` |
| 02 | Inference — Lane | `rgb` | `outputs_lane (dict)` |
| 03 | Inference — Object | `rgb` | `outputs_obj (dict)` |
| 04 | Post-Processing — Lane | `outputs_lane` | `binary_mask (H, W) uint8` |
| 05 | BEV Transform | `binary_mask` | `bev_mask (H, W) uint8` |
| 06 | Sliding Windows | `bev_mask` | `fit_result (LaneFitResult)` |
| 07 | Post-Processing — Object | `outputs_obj`, `rgb.shape` | `detections (list[dict])` |
| 08 | Object — CorridorChecker + ObstacleTracker | `detections`, `fit_result` | `EnvironmentState`, `ObstacleInfo` |
| 09 | Kuksa Publish | `EnvironmentState.detections` | VSS signals (gRPC) |
| 10 | FSM | `EnvironmentState`, `ObstacleInfo` | `State` |
| 11 | Path Planner | `State`, `obstacle_side` | `target_cte (float)` |
| 12 | PID | `target_cte`, `cte_actual`, `dt` | `steering (float [-1, 1])` |
| 13 | Adaptive Cruise Control | `lead_car_area` | `throttle (int [0, 8])` — only in `FOLLOW` state |
| 14 | CAN Bus | `steering`, `throttle` | CAN frame `0x002`: `[throttle int16 LE, steering×100 int16 LE]` (4 bytes) |

## Rules for `main`

`main` is the pipeline orchestrator — it coordinates execution order and data passing between modules. It must not contain business logic.

**Belongs in `main`:**
- Initialisation and teardown of resources (camera, engines, CAN, display)
- Sequential calls to modules in the correct order
- Blind wait timer management and obstacle tracker reset
- FPS logging and FSM state logging
- `KeyboardInterrupt` handling

**Does not belong in `main`:**
- Detection, classification, or filtering logic
- Lane geometry or BEV calculations
- FSM state transition rules
- PID or throttle control logic
- Any logic that can be encapsulated in an existing module

## Rules for New Modules

Before implementing a new module, answer:

1. Which layer does it belong to? (hardware / processing / decision / integration)
2. What is the expected input?
3. What is the expected output?
4. Does it add unnecessary coupling to `main`?
5. Can it be tested in isolation?

The module must:
- Expose a public API via `__init__.py`
- Have a `README.md` with overview, classes, data contract, and debug sections
- Communicate with other modules exclusively through defined data contracts (dataclasses, enums, documented types)
- Not import from higher-layer modules

## Module Documentation
- [camera](camera/README.md)
- [inference](inference/README.md)
- [post_processing](post_processing/README.md)
- [post_processing — obj](post_processing/obj/README.md)
- [post_processing — lane](post_processing/lane/README.md)
- [object](object/README.md)
- [LFA](LFA/README.md)
- [LFA geometry](LFA/geometry/README.md)
- [LFA visualization](LFA/visualization/README.md)
- [decision](decision/README.md)
- [kuksa_publish](kuksa_publish/README.md)
- [utils](utils/README.md)
- [core](core/README.md)

## Documentation Rules

Every module must have a `README.md` following this structure:

```
# Module Name

## Index
## Overview
## Classes
  ### ClassName
    #### __init__(params)
    #### method(params) → return_type
## Data Contract
## Debug
## Notes
```

**Overview** — one paragraph describing what the module does, what it receives, and what it produces.

**Classes** — one section per class. Each method documents:
- Parameters with types and default values (table format)
- Return type and description
- Any non-obvious behaviour or invariants

**Data Contract** — a table with all fields that cross module boundaries:

| Field | Type | Source | Destination |

**Debug** — two subsections:
- *Lifecycle logs* — logs emitted once (startup, shutdown, state transitions). Always active.
- *Per-frame logs* — logs emitted every frame. Must be gated behind a `debug` flag or logger level. Document how to enable.

If the module emits no logs, state it explicitly (`None`).

**Notes** — constraints, known limitations, dependencies on external state, or behaviour that would surprise a reader.

**`__init__.py`** — exposes only the public API of the module. Internal helpers and implementation details are not re-exported.

## Cross-Cutting Documentation
- [Architecture Proposal](docs/architecture_proposal.md)
