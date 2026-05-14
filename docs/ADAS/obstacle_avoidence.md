# Obstacle Avoidance System

This document describes the obstacle avoidance pipeline implemented for the autonomous driving platform. The system spans several modules that work together to detect, track, and safely navigate around obstacles in the vehicle's path.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Module Breakdown](#module-breakdown)
  - [1. Object Detection](#1-object-detection-objectdetectorpy)
  - [2. Corridor Check](#2-corridor-check-corridor_checkpy)
  - [3. Obstacle Tracker](#3-obstacle-tracker-obstacle_trackerpy)
  - [4. Decision FSM](#4-decision-fsm-decision_fsmpy)
  - [5. Path Planner](#5-path-planner-path_plannerpy)
- [Avoidance State Machine](#avoidance-state-machine)
- [Data Flow](#data-flow)
- [Tunable Parameters](#tunable-parameters)

---

## Overview

The obstacle avoidance system continuously monitors the vehicle's lane corridor using a YOLO-based object detector and a Bird's-Eye View (BEV) transform. When an obstacle is confirmed inside the corridor, the system transitions through a structured evasive maneuver, shifting the lane target, waiting for the obstacle to clear, and then smoothly returning to center, all coordinated between a Finite State Machine (FSM) and a Path Planner.

---

## Architecture

```
Camera Frame
     │
     ▼
┌─────────────────┐
│  ObjectDetector │  ← YOLO inference on NPU (Hailo-8)
└────────┬────────┘
         │ raw detections (bbox, class, score)
         ▼
┌─────────────────┐
│  CorridorChecker│  ← BEV projection + lane polynomial intersection
└────────┬────────┘
         │ detections enriched with in_corridor, relative_area, bev_x
         ▼
┌─────────────────┐
│ ObstacleTracker │  ← area growth rate + consecutive frame counting
└────────┬────────┘
         │ ObstacleInfo (situation: CLEAR | AVOIDANCE | BRAKE)
         ▼
┌─────────────────┐
│   VehicleFSM    │  ← state transitions based on environment + tracker
└────────┬────────┘
         │ current State
         ▼
┌─────────────────┐
│   PathPlanner   │  ← computes target CTE offset + blind wait timer
└────────┬────────┘
         │ target_cte
         ▼
      PID → steering angle → CAN Bus
```

---

## Module Breakdown

### 1. Object Detection (`ObjectDetector.py`)

Runs a custom YOLO model (YOLO26-sec) on the Hailo-8 NPU. Produce a list of detections, each with:

- `bbox` — pixel coordinates `(x1, y1, x2, y2)`
- `class_name` / `class_id` — one of 13 classes (e.g. `obstacle`, `car`, `stop_sign`, `light_red`, ...)
- `score` — confidence score

Relevant class for avoidance: **`ClassID.OBSTACLE` (id = 8)**.

---

### 2. Corridor Check (`corridor_check.py`)

Determines whether a detected object is inside the vehicle's current driving corridor.

**How it works:**

1. The bottom-center of the bounding box is projected into BEV space using a homography matrix (`cv2.perspectiveTransform`).
2. The BEV x-coordinate is compared against the left and right lane polynomials fitted by the sliding window algorithm.
3. A configurable margin (default `15 px`) is applied to avoid false negatives near the lane edges.
4. If no lane lines are found, a fixed central band (35%–65% of frame width) is used as a fallback corridor.

**Output per detection:**

| Field | Description |
|---|---|
| `in_corridor` | `True` if the object falls within the lane boundaries |
| `bev_x`, `bev_y` | BEV-space position of the object's base |
| `rel_area` | Bounding box area relative to total frame area |
| `l_x`, `r_x` | Left/right lane x-coordinates at the object's BEV depth |

---

### 3. Obstacle Tracker (`obstacle_tracker.py`)

Tracks the most relevant obstacle across frames to classify the urgency of the situation.

**Inputs:** all detections flagged as `in_corridor` with `class_id == OBSTACLE`.

**Per-frame logic:**

1. Selects the obstacle with the largest `relative_area` (closest / most critical).
2. Computes `delta_area = current_area − previous_area` (growth rate).
3. Increments a consecutive-frame counter (`frames_in_corridor`).
4. Normalizes the BEV x-position to `[0.0, 1.0]` and classifies the side:
   - `< 0.43` → `"left"`
   - `> 0.57` → `"right"`
   - otherwise → `"center"`

**Situation classification:**

| Situation | Condition |
|---|---|
| `BRAKE` | `delta_area ≥ area_brake_threshold` (sudden appearance) |
| `AVOIDANCE` | `area ≥ area_avoidance_min` AND `frames_in_corridor ≥ frames_to_confirm` |
| `CLEAR` | None of the above |

**Output:** `ObstacleInfo` dataclass with `situation`, `area`, `delta_area`, `bev_x_norm`, `frames_in_corridor`, `side`.

---

### 4. Decision FSM (`decision_fsm.py`)

A Finite State Machine that controls the vehicle's high-level behavior. States relevant to obstacle avoidance:

| State | Description |
|---|---|
| `PREPARE_AVOID` | Obstacle confirmed -> PathPlanner begins lateral offset |
| `AVOIDING` | Actively deviating around the obstacle |
| `BLIND_WAIT` | Obstacle no longer visible -> waiting before returning |
| `RETURNING` | Smoothly interpolating CTE back to center |
| `EMERGENCY` | Obstacle critically close, vehicle brakes immediately |

**Transition triggers:**

- `BRAKE situation` (from ObstacleTracker) → immediate transition to `EMERGENCY`, regardless of current state.
- `AVOIDANCE situation` OR `obstacle_ahead` flag (area ≥ threshold) confirmed for 5 frames via `ConfirmationBuffer` → transition to `PREPARE_AVOID`.
- During `AVOIDING`: if the obstacle disappears for `OBSTACLE_LOST_THRESHOLD` frames (default: 10) → transition to `BLIND_WAIT`.
- During `BLIND_WAIT`: timer expires (managed by PathPlanner) → transition to `RETURNING`.
- During `RETURNING`: PathPlanner signals interpolation complete → restore pre-avoidance speed state.

All other FSM logic (traffic lights, speed signs, stop signs, ACC) is **suspended** while any avoidance state is active.

---

### 5. Path Planner (`path_planner.py`)

Computes the **target Cross-Track Error (CTE)** to feed into the PID controller each frame.

**Target CTE per FSM state:**

| FSM State | Target CTE |
|---|---|
| `PREPARE_AVOID`, `AVOIDING`, `BLIND_WAIT` | `±lane_offset` (opposite side of obstacle) |
| `RETURNING` | Linearly interpolated from `±lane_offset` → `0.0` |
| All others | `0.0` (lane center) |

**Lateral offset direction:**

- Obstacle on the **right** or **center** → deviate **left** (`CTE = -lane_offset`)
- Obstacle on the **left** → deviate **right** (`CTE = +lane_offset`)

**Blind wait timer:**

`check_blind_wait_timeout()` is called every frame while in `BLIND_WAIT`. On first call it starts an internal `time.time()` timer; returns `True` when `blind_wait_time` seconds have elapsed. This is independent of frame rate.

**Return interpolation:**

Uses linear interpolation (`lerp`) over `return_duration_s` seconds using `time.perf_counter()` for accuracy:

```
CTE(t) = lerp(cte_at_return_start, 0.0, elapsed / return_duration_s)
```

---

## Avoidance State Machine

```
         obstacle confirmed (5 frames)
SPEED_XX ──────────────────────────────► PREPARE_AVOID
                                               │
                                    2 frames confirm
                                               │
                                               ▼
                                           AVOIDING
                                               │
                                  obstacle lost for 10 frames
                                               │
                                               ▼
                                          BLIND_WAIT
                                               │
                                    blind_wait_time elapsed
                                               │
                                               ▼
                                          RETURNING
                                               │
                                  return interpolation complete
                                               │
                                               ▼
                                       SPEED_XX (restored)

     ┌── BRAKE detected (any state) ──► EMERGENCY
     │                                      │
     │                          corridor clear for 15 frames
     │                                      │
     └──────────────────────────────────────┘
```

---

## Data Flow

Below is the per-frame sequence executed in `main.py`:

```
1. Read camera frame (YUV420 → BGR)
2. Run lane model  → binary mask → BEV mask → polynomial fit (CTE)
3. Run object model → raw detections
4. CorridorChecker  → enrich each detection with in_corridor, rel_area, bev_x
5. Build EnvironmentState (Detection list, corridor_clear flag)
6. ObstacleTracker.update() → ObstacleInfo (situation, side, area, ...)
7. Check BLIND_WAIT timer; signal FSM if expired
8. VehicleFSM.process() → current_state
9. PathPlanner.calculate_target_cte() → target_cte
10. PID.update(target_cte, actual_cte, dt) → steering_angle
11. CAN Bus → send throttle + steering
12. Display (optional)
```

---

## Tunable Parameters

| Parameter | Location | Default | Description |
|---|---|---|---|
| `area_brake_threshold` | `ObstacleTracker` | `0.060` | Area delta per frame that triggers `BRAKE` |
| `area_avoidance_min` | `ObstacleTracker` | `0.010` | Minimum relative area to start counting avoidance frames |
| `frames_to_confirm` | `ObstacleTracker` | `4` | Consecutive frames needed to report `AVOIDANCE` |
| `AREA_EMERGENCY` | `Thresholds` (FSM) | `0.05` | Area threshold for direct `EMERGENCY` transition |
| `AREA_AVOIDANCE` | `Thresholds` (FSM) | `0.015` | Area threshold for `obstacle_ahead` flag |
| `OBSTACLE_LOST_THRESHOLD` | `VehicleFSM` | `10` | Frames without obstacle before entering `BLIND_WAIT` |
| `lane_offset` | `PathPlanner` | `0.38` | Normalized lateral CTE deviation during avoidance |
| `blind_wait_time` | `PathPlanner` | `2.5 s` | Time to hold displaced CTE after obstacle disappears |
| `return_duration_s` | `PathPlanner` | `1.5 s` | Duration of the smooth CTE return to center |
| `corridor_margin` | `CorridorChecker` | `15 px` | BEV pixel tolerance at lane boundaries |