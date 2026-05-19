# ADAS Pipeline

## Index
- [Overview](#overview)
- [Data Flow](#data-flow)
- [Rules for `main`](#rules-for-main)
- [Rules for New Modules](#rules-for-new-modules)
- [Module Documentation](#module-documentation)
- [Cross-Cutting Documentation](#cross-cutting-documentation)

## Overview
Execution pipeline for the ADAS prototype running on Raspberry Pi 5 + Hailo-8. Each module is responsible for its own code and local documentation. The pipeline follows a layered architecture with a pipe-and-filter execution model — each stage receives a defined input, processes it, and produces an output consumed by the next stage.

Entry point: `main.py`

## Usage

To execute the pipeline, provide the paths to the Lane Detection and Object Detection HEF models:

```bash
python3 main.py <lane_model.hef> <object_model.hef> [options]
```

### Options
- `--remote`: Enables remote streaming of the display output via stdout.
- `--no-display`: Disables the display output, useful for running on headless systems.
- `--virtual`: Runs in virtual mode, preventing physical commands (steering/throttle) from being sent to the vehicle.

## Data Flow

| Step | Module | Input | Output |
|---|---|---|---|
| 01 | Camera | — | `rgb (H, W, 3) uint8` |
| 02 | Inference — Lane | `rgb` | `outputs_lane (dict)` |
| 03 | Inference — Object | `rgb` | `outputs_obj (dict)` |
| 04 | Post-Processing — Lane | `outputs_lane` | `binary_mask (H, W) uint8` |
| 05 | BEV Transform | `binary_mask` | `bev_mask (H, W) uint8` |
| 06 | Sliding Windows | `bev_mask` | `fit_result (LaneFitResult)` |
| 07 | Post-Processing — Object | `outputs_obj`, `fit_result` | `detections (list[dict])`, `EnvironmentState` |
| 08 | Obstacle Tracker | `detections` | `ObstacleInfo` |
| 09 | Kuksa Publish | `EnvironmentState.detections` | VSS signals (gRPC) |
| 10 | FSM | `EnvironmentState`, `ObstacleInfo` | `State` |
| 11 | Path Planner | `State`, `obstacle_side` | `target_cte (float)` |
| 12 | PID | `target_cte`, `cte_actual`, `dt` | `steering (float [-1, 1])` |
| 13 | Adaptive Cruise Control | `lead_car_area` | `throttle (int [0, 8])` |
| 14 | CAN Bus | `steering`, `throttle` | CAN command `0x002` |

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
- [post_processing — object](post_processing/object/README.md)
- [post_processing — lane](post_processing/lane/README.md)
- [LFA](LFA/README.md)
- [LFA geometry](LFA/geometry/README.md)
- [LFA tracking](LFA/tracking/README.md)
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
