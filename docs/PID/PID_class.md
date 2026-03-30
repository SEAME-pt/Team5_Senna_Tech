# PID Class Documentation

## Overview

The `PID` class implements a standard discrete PID controller for steering/throttle.

It computes the control output from:
- Proportional term (current error)
- Integral term (accumulated error over time)
- Derivative term (rate of error change)

The class also includes:
- Integral anti-windup through symmetric clamping
- Output clamping to a symmetric range
- Reset of internal controller state

Default limits (set in constructor):
- Integral limit: `1.0`
- Output limit: `1.0`

## Mathematical Model

Given:
- $e(t) = target - current$
- $dt > 0$

The implementation computes:

$$
P = K_p \cdot e
$$

$$
I_{acc} = clamp(I_{acc} + e \cdot dt,\ -I_{lim},\ I_{lim})
$$

$$
I = K_i \cdot I_{acc}
$$

$$
D = K_d \cdot \frac{e - e_{prev}}{dt}
$$

$$
out = clamp(P + I + D,\ -O_{lim},\ O_{lim})
$$

Where:
- $I_{lim}$ is the integral limit
- $O_{lim}$ is the output limit

If `dt <= 0`, `update()` returns `0.0`.

## Public API

### Constructor

```cpp
PID(double kp, double ki, double kd)
```

Creates a PID controller with gains:
- `kp`: proportional gain
- `ki`: integral gain
- `kd`: derivative gain

Initial internal state:
- previous error = `0.0`
- integral accumulator = `0.0`
- integral limit = `1.0`
- output limit = `1.0`

### `update`

```cpp
double update(double target, double current, double dt)
```

Computes one control step and returns the clamped output.

Parameters:
- `target`: desired value (setpoint)
- `current`: measured value
- `dt`: elapsed time in seconds since last update

Behavior:
- Computes error as `target - current`
- Updates and clamps integral accumulator
- Computes derivative using previous error
- Stores current error for next step
- Returns output clamped to `[-outputLimit, outputLimit]`

### `reset`

```cpp
void reset()
```

Clears controller memory:
- previous error set to `0.0`
- integral accumulator set to `0.0`

Use this when restarting control or after long pauses.

### `setIntegralLimit`

```cpp
void setIntegralLimit(double limit)
```

Sets integral accumulator bound to `abs(limit)` and immediately reclamps the current accumulator.

### `setOutputLimit`

```cpp
void setOutputLimit(double limit)
```

Sets output bound to `abs(limit)`.

## Helper Functions in Current Implementation

### `mapPIDtoServo`

```cpp
double mapPIDtoServo(double pid_value, double min_angle, double max_angle)
```

Maps a PID output from `[-1, 1]` to a servo angle range `[min_angle, max_angle]`.

- Input is clamped to `[-1, 1]`
- Useful when PID output is normalized and actuator command is angular

### Symmetric Clamping Utility

The internal helper `clampSymmetric(value, limit)` clamps to `[-limit, limit]` and returns `0.0` when `limit <= 0.0`.

## Usage Example

```cpp
#include "PID.hpp"

PID steeringPid(0.45, 0.01, 0.08);

// Example loop step
const double dt = 0.02; // 20 ms
const double targetCenter = 0.0;
const double measuredOffset = -0.12;

double pidOutput = steeringPid.update(targetCenter, measuredOffset, dt);
double servoAngle = mapPIDtoServo(pidOutput, 60.0, 120.0);
```

## Suggested Initial Tuning Range

Common starting values for steering control:
- `kp`: `0.3` to `0.6`
- `ki`: `0.0` to `0.02`
- `kd`: `0.05` to `0.15`

Tune incrementally and validate with real system response to avoid oscillation or slow correction.
