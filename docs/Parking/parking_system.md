# Parking System — SennaTech

## Overview

The parking system implements an autonomous parallel parking maneuver. It is triggered via a dedicated CAN message (`CAN_ID_MODE_PARKING`) received by the motor thread, which then delegates full control to the parking state machine until the maneuver completes or an error occurs.

The system is entirely reactive — it does not plan a path in advance but instead uses real-time distance measurements to decide when to transition between maneuver phases.

---

## Sensing — Ultrasonic Distance

Two SRF08 ultrasonic sensors provide distance feedback: one mounted at the rear and one at the front of the car. They communicate over I2C and return distance in centimeters.

The sensors run on a dedicated ThreadX thread that continuously triggers measurements and publishes the results to a shared queue (`g_ultrasonic_data_queue`). The parking maneuver functions consume from this queue, blocking until a fresh reading is available. This decouples the sensing rate from the maneuver logic and ensures parking decisions are always based on recent data.

---

## State Machine

The parking maneuver is divided into three sequential phases, each implemented as an independent function returning a `e_parking_mode` value. The entry point `parking_mode_entry` drives the transitions:

```
FIRST_MANEUVER → SECOND_MANEUVER → FINAL_MANEUVER → done
                      ↓                   ↓
                ERROR_MANEUVER      ERROR_MANEUVER
```

If any phase returns `ERROR_MANEUVER`, the sequence aborts immediately and the car is brought to a full stop.

```c
typedef enum parking_mode {
    FIRST_MANEUVER  = 0,
    SECOND_MANEUVER = 1,
    FINAL_MANEUVER  = 2,
    ERROR_MANEUVER  = 3
} e_parking_mode;
```

---

## Phase 1 — Entry (First Maneuver)

The car begins fully stopped with the steering set to full right (`-1.0f`). It then moves backwards at a constant slow velocity until the rear sensor reads below `FIRST_MANEUVER_SAFE_DISTANCE_CM` (27 cm), indicating the car has reversed far enough into the parking slot.

The steering angle during this phase is what initiates the rotation into the slot. The car is essentially pivoting its rear end into position.

**Exit condition:** `back_distance_cm ≤ 27 cm`  
**Abort condition:** `back_distance_cm < safe_distance_threshold_cm`

---

## Phase 2 — Alignment (Second Maneuver)

Steering switches to full left (`+1.0f`). The car continues reversing until the rear sensor reads below `SECOND_MANEUVER_SAFE_DISTANCE_CM` (14 cm). This phase straightens the car's angle relative to the parking slot — the opposite steering lock counteracts the rotation introduced in phase 1.

**Exit condition:** `back_distance_cm ≤ 14 cm`  
**Abort condition:** `back_distance_cm < safe_distance_threshold_cm`

---

## Phase 3 — Centering (Final Maneuver)

Steering returns to center (`0.0f`) and the car moves forward. The goal is to position the car symmetrically within the slot — equidistant from both the front and rear walls.

Two conditions can trigger completion:

- **Front is open** — the front sensor reads beyond `FINAL_MANEUVER_THRESHOLD_CM * 2` (24 cm), meaning there is no obstacle ahead and the car has cleared far enough forward.
- **Both distances are balanced** — front and rear readings are within `FINAL_MANEUVER_THRESHOLD_CM` (12 cm) of each other, meaning the car is roughly centered in the slot.

```c
if (is_front_infinite(ultrasonic_data.front_distance_cm) ||
    stabilizing_two_values(ultrasonic_data.back_distance_cm,
                           ultrasonic_data.front_distance_cm))
```

**Exit condition:** front open or front/back within 12 cm of each other  
**Abort condition:** `back_distance_cm < safe_distance_threshold_cm`

---

## Safety

Throughout every phase, each distance reading is validated before any motion command is issued. The function `is_distance_safe` rejects any reading below 2 cm as a hard stop condition:

```c
UINT is_distance_safe(ULONG back_distance_cm, ULONG front_distance_cm)
{
    const ULONG safe_distance_threshold_cm = 2;

    if (back_distance_cm && back_distance_cm < safe_distance_threshold_cm)
        return 0;
    if (front_distance_cm && front_distance_cm < safe_distance_threshold_cm)
        return 0;
    return 1;
}
```

Passing `0` for a distance means that direction is not being monitored in that phase — for example, phase 1 and 2 only check the rear. A zero value is treated as safe by convention, since the sensor may not be aimed in that direction.

---

## Key Constants

| Constant | Value | Meaning |
|---|---|---|
| `FIRST_MANEUVER_SAFE_DISTANCE_CM` | 27 cm | Rear threshold to end phase 1 |
| `SECOND_MANEUVER_SAFE_DISTANCE_CM` | 14 cm | Rear threshold to end phase 2 |
| `FINAL_MANEUVER_THRESHOLD_CM` | 12 cm | Balance tolerance for centering |
| `CONSTANT_PARKING_VELOCITY` | -0.18f | Normalized reverse throttle (~18%) |
| `safe_distance_threshold_cm` | 2 cm | Hard abort distance |

---

## Limitations

- The system assumes the car enters the parking slot from a fixed, consistent position. There is no lateral positioning correction — if the initial alignment is off, the maneuver thresholds may need tuning.
- Distance readings from the SRF08 have a cone angle of ~55 degrees, meaning the sensor can pick up objects that are not directly in line with the car's axis. This can cause early or false abort conditions in tight environments.
- The maneuver uses fixed steering angles (full lock in both directions) rather than proportional correction, which means slot geometry and car turning radius are implicitly assumed to be compatible with the threshold values.
