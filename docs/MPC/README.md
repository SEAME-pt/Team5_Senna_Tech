# Model Predictive Control (MPC) for Steering — SEA:ME Project

## Table of Contents
1. [Introduction](#introduction)
2. [What is MPC?](#what-is-mpc)
3. [MPC vs PID — Why MPC for Autonomous Driving?](#mpc-vs-pid)
4. [How MPC Works — The Receding Horizon Principle](#how-mpc-works)
5. [Vehicle Model](#vehicle-model)
6. [Cost Function and Constraints](#cost-function-and-constraints)
7. [System Architecture](#system-architecture)
8. [KUKSA Integration](#kuksa-integration)
9. [Implementation Guide](#implementation-guide)
10. [Pseudo-Code](#pseudo-code)
11. [Tuning Guide](#tuning-guide)
12. [Known Issues and Limitations](#known-issues-and-limitations)
13. [Future Improvements](#future-improvements)

---

## Introduction

This document describes the design and implementation of a **Model Predictive Control (MPC)** steering controller for the SEA:ME autonomous vehicle project.

The vehicle stack runs on:
- **Raspberry Pi** — perception, lane detection, and high-level control (MPC)
- **STM32** — low-level servo control
- **CAN bus** — communication between Raspberry Pi and STM32
- **KUKSA Data Broker** — vehicle signal middleware

The MPC controller is responsible for computing the optimal steering angle at each control cycle based on the vehicle's current lane tracking error.

---

## What is MPC?

Model Predictive Control is a control strategy that uses a **mathematical model of the system** to predict its future behavior and compute the optimal sequence of control actions over a finite time window called the **prediction horizon**.

At each control cycle, MPC:
1. Reads the current system state
2. Uses the vehicle model to simulate future states over `N` time steps
3. Finds the sequence of control inputs that minimizes a cost function
4. Applies **only the first control input** from that sequence
5. Repeats the process at the next timestep (receding horizon)

The key insight is that MPC **continuously re-plans**: even though it computes a full sequence of N actions, it only ever acts on the first one and re-optimizes at the next cycle with fresh state information.

---

## MPC vs PID — Why MPC for Autonomous Driving?

A **PID controller** reacts to the current error (and its history/derivative) but has no knowledge of future states or constraints. It works well for simple linear systems but struggles in autonomous driving because:

- Road geometry introduces non-linearities
- Sharp curves cause large sudden errors that PID over- or under-corrects
- There is no mechanism to limit the rate of change of the steering angle

**MPC addresses all of these limitations:**

| Feature | PID | MPC |
|---|---|---|
| Uses a system model | ❌ | ✅ |
| Anticipates future states | ❌ | ✅ |
| Handles physical constraints (e.g. max steering angle) | ❌ | ✅ |
| Smooth control output | Limited | ✅ |
| Computational cost | Very low | Moderate |

For the SEA:ME project, MPC is preferred because it allows the vehicle to **look ahead**, handle curves proactively, and enforce the physical limits of the servo.

---

## How MPC Works — The Receding Horizon Principle

```
Time:   t     t+1   t+2   ...   t+N
        |-----|-----|-----|-----|
State:  x0    x1    x2         xN   ← predicted
Input:  δ0    δ1    δ2         δN-1 ← optimized
              ↑
        only δ0 is applied
```

At time `t`, the optimizer finds the sequence `[δ0, δ1, ..., δN-1]` that minimizes the total cost. Only `δ0` is sent to the actuator. At `t+1`, the state is re-measured and the whole process repeats.

This is called the **receding horizon** — the prediction window moves forward with time, always using the most current state.

### Parameters

| Parameter | Symbol | Description | Example value |
|---|---|---|---|
| Wheelbase | `L` | Distance between front and rear axles | `0.25 m` |
| Time step | `dt` | Duration of each prediction step | `0.1 s` |
| Horizon length | `N` | Number of steps to predict ahead | `10` |

A horizon of `N=10` with `dt=0.1s` means the controller predicts **1 second into the future** at each cycle.

---

## Vehicle Model

MPC requires a mathematical model to simulate future states. We use the **kinematic bicycle model**, which is a standard simplified model for low-speed autonomous vehicles.

### State Variables

- `cte` — Cross Track Error: signed lateral distance from the vehicle center to the lane center (meters)
- `ψ` (heading error) — difference between the vehicle's current heading and the desired lane heading (radians)
- `v` — longitudinal velocity (m/s)

### Control Input

- `δ` — steering angle (radians or degrees)

### Discrete-Time Update Equations

```
cte[t+1]     = cte[t] + v * sin(ψ[t]) * dt
ψ[t+1]       = ψ[t]   + (v / L) * δ[t] * dt
```

**Intuition:**
- If the vehicle has a heading error `ψ`, it is moving at an angle relative to the lane. The lateral drift over `dt` is `v * sin(ψ) * dt`, which adds to the CTE.
- The heading error evolves based on the steering angle: a steering input `δ` causes a yaw rate of `v/L * δ` (Ackermann geometry).

> **Note:** This is a simplified model. It assumes constant velocity, ignores tire slip, and is only valid at low speeds. For higher speeds or more aggressive maneuvers, a dynamic model would be required.

---

## Cost Function and Constraints

### Cost Function

The optimizer minimizes a weighted sum of penalties:

```
J = w_cte     * Σ cte[t]²
  + w_heading * Σ ψ[t]²
  + w_steer   * Σ δ[t]²
  + w_smooth  * Σ (δ[t+1] - δ[t])²
```

Each term penalizes a different undesired behavior:

| Term | What it penalizes | Effect of increasing weight |
|---|---|---|
| `w_cte * cte²` | Lateral deviation from lane center | More aggressive correction |
| `w_heading * ψ²` | Misalignment with lane direction | Faster heading correction |
| `w_steer * δ²` | Large steering angles | More conservative steering |
| `w_smooth * Δδ²` | Sudden changes in steering | Smoother, less jerky motion |

The balance between these weights determines the **character** of the controller. Tuning them is covered in the [Tuning Guide](#tuning-guide).

### Constraints

The steering angle must stay within the physical limits of the servo:

```
-δ_max ≤ δ[t] ≤ δ_max    for all t in [0, N-1]
```

For the SEA:ME servo, a reasonable limit is:

```
-25° ≤ δ ≤ 25°
```

This constraint is enforced directly in the optimization — the solver will never produce a steering command outside this range.

---

## System Architecture

```
┌─────────────────────────────────────────┐
│              Raspberry Pi               │
│                                         │
│  Camera → Lane Detection → CTE / ψ      │
│                    ↓                    │
│             KUKSA Data Broker           │
│      (Vehicle.Lane.CTE, .HeadingError)  │
│                    ↓                    │
│             MPC Controller              │
│      (reads state, solves, outputs δ)   │
│                    ↓                    │
│             CAN Bus Interface           │
└───────────────────┬─────────────────────┘
                    │ CAN frame (steering_angle)
        ┌───────────▼───────────┐
        │         STM32         │
        │  Servo PWM Controller │
        └───────────────────────┘
```

### Component Responsibilities

**Raspberry Pi:**
- Captures camera frames
- Runs lane detection to extract lane center
- Computes `cte` and heading error `ψ`
- Publishes these values to KUKSA
- Runs the MPC loop (reads state → solves → sends command)
- Sends steering angle over CAN

**STM32:**
- Receives CAN frame with steering angle
- Converts angle to PWM signal
- Drives the servo motor

**KUKSA Data Broker:**
- Acts as the vehicle signal bus between perception and control
- Decouples the lane detection pipeline from the MPC controller

---

## KUKSA Integration

KUKSA is a VSS-compliant (Vehicle Signal Specification) data broker. It acts as a publish/subscribe middleware for vehicle signals.

### Required Signals

| Signal path | Direction | Description |
|---|---|---|
| `Vehicle.Speed` | Input to MPC | Current vehicle speed |
| `Vehicle.Lane.CTE` | Input to MPC | Cross Track Error (custom signal) |
| `Vehicle.Lane.HeadingError` | Input to MPC | Heading error (custom signal) |
| `Vehicle.Control.Steering` | Output from MPC | Computed steering angle |

### ⚠️ Critical Missing Step

`Vehicle.Lane.CTE` and `Vehicle.Lane.HeadingError` are **not part of the standard VSS spec** and must be **manually registered** in the KUKSA broker before use.

This requires:
1. Defining the custom signals in a VSS extension file (`.vspec`)
2. Loading the extended spec when starting `kuksa-val-server` or `databroker`
3. Updating the perception pipeline to publish these values after each lane detection frame

**Until this is done, the MPC controller cannot read lane state from KUKSA.**

### Publishing from Perception (example)

```python
# After lane detection computes cte and heading_error:
kuksa_client.set_current_value("Vehicle.Lane.CTE", cte)
kuksa_client.set_current_value("Vehicle.Lane.HeadingError", heading_error)
```

### Reading in MPC (example)

```python
cte     = kuksa_client.get_current_value("Vehicle.Lane.CTE")
heading = kuksa_client.get_current_value("Vehicle.Lane.HeadingError")
v       = kuksa_client.get_current_value("Vehicle.Speed")
```

---

## Implementation Guide

### Step 1 — Compute CTE and Heading Error

In the lane detection module, after identifying the lane center:

```python
# image_center: horizontal center of the image (pixels)
# lane_center:  horizontal position of detected lane center (pixels)
# pixels_per_meter: calibration factor

cte = (lane_center - image_center) / pixels_per_meter

# heading_error: estimated from the slope of the lane center line
heading_error = math.atan2(lane_slope_dy, lane_slope_dx)
```

### Step 2 — Publish to KUKSA

After each detection frame, push the values to the data broker (see KUKSA Integration above).

### Step 3 — MPC Main Loop

The MPC loop runs independently on the Raspberry Pi at 10–20 Hz:

```python
while True:
    state = read_state_from_kuksa()   # [cte, heading, v]
    delta = solve_mpc(state)          # optimization
    send_steering_via_can(delta)      # actuate
    time.sleep(dt)
```

### Step 4 — Solve the Optimization

At each cycle, the solver searches for the steering value `δ` that minimizes the predicted cost over `N` steps. See [Pseudo-Code](#pseudo-code) for the full implementation.

### Step 5 — Send via CAN

Encode the steering angle into a CAN frame and transmit to STM32:

```python
import can

bus = can.interface.Bus(channel='can0', bustype='socketcan')

def send_steering_via_can(angle_deg):
    # Scale angle to integer (e.g. multiply by 100 for 0.01° resolution)
    value = int(angle_deg * 100)
    data = value.to_bytes(2, byteorder='big', signed=True)
    msg = can.Message(arbitration_id=0x200, data=data, is_extended_id=False)
    bus.send(msg)
```

---

## Pseudo-Code

### Main Loop

```python
# Parameters
L   = 0.25   # wheelbase (m)
dt  = 0.1    # time step (s)
N   = 10     # prediction horizon

# Cost weights
w_cte     = 1.0
w_heading = 0.5
w_steer   = 0.1
w_smooth  = 10.0

# Steering constraint
DELTA_MAX = math.radians(25)

while True:
    v       = get_speed()        # from KUKSA
    cte     = get_cte()          # from KUKSA
    heading = get_heading_error() # from KUKSA

    state = [cte, heading, v]
    steering = solve_mpc(state)

    send_can(steering)
    time.sleep(dt)
```

### MPC Solver (Simplified Grid Search)

```python
def solve_mpc(state):
    cte, heading, v = state

    best_cost  = float('inf')
    best_delta = 0.0

    # Discretize steering space
    possible_deltas = [i * math.radians(1) for i in range(-25, 26)]

    for delta in possible_deltas:
        cost        = 0.0
        cte_pred    = cte
        heading_pred = heading
        prev_delta  = delta

        for t in range(N):
            # Propagate model forward
            cte_pred     += v * math.sin(heading_pred) * dt
            heading_pred += (v / L) * delta * dt

            # Accumulate cost
            cost += w_cte     * cte_pred**2
            cost += w_heading * heading_pred**2
            cost += w_steer   * delta**2
            if t > 0:
                cost += w_smooth * (delta - prev_delta)**2

        if cost < best_cost:
            best_cost  = cost
            best_delta = delta

    return best_delta
```

> **Note on the solver:** This is a simplified grid search over discrete steering values. It is computationally cheap but coarse. For better precision, replace with a gradient-based solver or use the `scipy.optimize.minimize` function. For production-grade MPC, consider CasADi (see [Future Improvements](#future-improvements)).

---

## Tuning Guide

### Initial Weights

```python
w_cte     = 1.0   # lateral error penalty
w_heading = 0.5   # heading error penalty
w_steer   = 0.1   # steering magnitude penalty
w_smooth  = 10.0  # steering rate penalty (most important for smoothness)
```

### Symptom → Action

| Observed behavior | Likely cause | Adjustment |
|---|---|---|
| Oscillation / zig-zag | Too aggressive correction | Increase `w_smooth` or `w_steer` |
| Slow to correct lateral error | CTE not weighted enough | Increase `w_cte` |
| Drifts through curves | Heading error ignored | Increase `w_heading` |
| Jerky steering | Smoothness not penalized | Increase `w_smooth` |
| Instability at high speed | Model linearization breaks down | Reduce max speed or limit `δ_max` |

### Frequency Recommendations

| Component | Recommended rate |
|---|---|
| MPC loop (Raspberry Pi) | 10–20 Hz |
| CAN transmission | 10–20 Hz (same as MPC) |
| STM32 servo loop | 50–100 Hz |

The STM32 runs its servo control loop faster than MPC sends commands. This means the servo holds the last received angle between CAN updates, which is acceptable as long as MPC runs fast enough.

---

## Known Issues and Limitations

- **CTE and HeadingError not yet in KUKSA** — these custom signals must be defined and published before MPC can be integrated end-to-end. This is the single most critical blocker.
- **Grid search solver is coarse** — 1° resolution may not be sufficient for precise control. Consider finer discretization or a continuous optimizer.
- **Constant velocity assumption** — the kinematic model does not account for acceleration or braking. Integrating throttle control would require extending the state space.
- **No latency compensation** — the time between sensing and actuation (camera → detection → KUKSA → MPC → CAN → STM32) introduces a delay that can cause instability. A latency-aware MPC formulation would shift the initial predicted state forward in time to account for this.
- **Kinematic model only valid at low speed** — above ~1.5 m/s, tire slip becomes significant and the model loses accuracy.

---

## Future Improvements

| Improvement | Description |
|---|---|
| **Joint steering + throttle MPC** | Extend the state space to control both δ and acceleration simultaneously |
| **Latency compensation** | Model the actuator delay and shift the MPC initial state forward |
| **Dynamic vehicle model** | Replace kinematic model with a full dynamic model (includes tire forces) |
| **CasADi solver** | Replace grid search with a proper NLP solver for continuous, fast, accurate optimization |
| **Obstacle avoidance** | Add terms to the cost function penalizing proximity to detected obstacles |
| **Adaptive horizon** | Shorten N at high speed (stability), lengthen at low speed (smoother curves) |