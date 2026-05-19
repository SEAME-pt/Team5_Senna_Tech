# Utils

## Responsibility
Gathers infrastructure and external integration utilities used by the pipeline.

## Components
- `CanSender` - CAN interface via `socketcan`
- `hw_monitor` - hardware monitoring

## Internal Documentation

### 08 - CAN Bus
Sends the steering command to the vehicle via the CAN bus.

#### Input
| Field | Type | Description |
|---|---|---|
| `pid_return` | `float` | Normalized steering angle `[-1, 1]` |
| `current_state` | `FSMState` | Current state of the state machine |

#### Output
| Address | Description |
|---|---|
| `0x110` | Steering command (`pid_return * -1`) |
| `0x001` | FSM State |

#### Behavior
- Safety check: only sends if `abs(last_valid_pid - pid_return) <= 0.4`
- Does not send if the `--virtual` flag is active

#### Notes
- To be filled during testing
