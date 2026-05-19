# Decision

## Responsibility
Calculates steering and coordinates the high-level behavior of the pipeline based on cross-track error.

## Modules
- `PID` - proportional-integral-derivative controller
- `decision_fsm` - state machine for driving decisions

## Internal Documentation

### 07 - PID Controller
Calculates the steering angle based on CTE using a PID controller.

#### Input
| Field | Type | Description |
|---|---|---|
| `cte` | `float` | Normalized cross-track error `[-1, 1]` |
| `dt` | `float` | Time since last frame (seconds) |

#### Output
| Field | Type | Description |
|---|---|---|
| `pid_return` | `float` | Normalized steering angle `[-1, 1]` |

#### Gains
| Parameter | Value |
|---|---|
| `kp` | `1.5` |
| `ki` | `0.25` |
| `kd` | `0.15` |

#### Notes
- To be filled during testing
