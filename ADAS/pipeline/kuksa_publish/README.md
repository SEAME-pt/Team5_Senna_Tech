# Kuksa Publish

## Index
- [Overview](#overview)
- [Classes](#classes)
  - [KuksaClient](#kuksaclient)
- [Data Contract](#data-contract)
- [Debug](#debug)
- [Notes](#notes)

## Overview
Publishes detected traffic and speed signals to the Kuksa databroker via gRPC. Receives the detection list from `post_processing`, selects the most relevant signal per category, maps class IDs to VSS integer codes, and writes them to two VSS paths.

## Classes

### `KuksaClient`
Manages the gRPC connection to the Kuksa databroker and publishes signal states each frame.

#### `__init__(address)`
| Parameter | Default | Description |
|---|---|---|
| `address` | `"localhost:55555"` | Address of the Kuksa databroker |

Creates the gRPC channel and `VALStub`.

#### `send(detections)`
Main entry point called once per frame. Selects the dominant speed sign and traffic sign from the detection list and publishes both to Kuksa.

**Input** — `list[Detection]` from `EnvironmentState.detections`.

**Publishes**
| VSS Path | Type | Description |
|---|---|---|
| `Vehicle.ADAS.SpeedLimitSign` | `uint32` | Speed limit sign code |
| `Vehicle.ADAS.TrafficSign` | `uint32` | Traffic sign / light code |

#### `detect_speed_signal(class_id) → int`
Maps `ClassID` to the VSS speed signal code.

| `class_id` | Output | Meaning |
|---|---|---|
| `0` (`SIGN_50`) | `11` | Speed 50 |
| `1` (`SIGN_80`) | `12` | Speed 80 |
| other | `10` | No speed sign |

#### `detect_traffic_signal(class_id) → int`
Maps `ClassID` to the VSS traffic sign code.

| `class_id` | Input class | Output |
|---|---|---|
| `3` | `CROSSWALK_SIGN` | `3` |
| `4` | `STOP_SIGN` | `1` |
| `5` | `YIELD_SIGN` | `4` |
| `7` | `DANGER_SIGN` | `2` |
| `9` | `LIGHT_GREEN` | `7` |
| `11` | `LIGHT_RED` | `5` |
| `12` | `LIGHT_YELLOW` | `6` |
| other | — | `0` |

#### `_select_signals(detections) → (Detection, Detection)`
Selects the speed sign and traffic sign with the largest relative area from the detection list.

**Output** — `(current_speed_signal, current_traffic_signal)`.

#### `close()`
Closes the gRPC channel. Called at pipeline shutdown.

## Data Contract
| Field | Type | Source | Destination |
|---|---|---|---|
| `detections` | `list[Detection]` | `EnvironmentState.detections` | `KuksaClient.send()` |
| `Vehicle.ADAS.SpeedLimitSign` | `uint32` | `KuksaClient` | Kuksa databroker |
| `Vehicle.ADAS.TrafficSign` | `uint32` | `KuksaClient` | Kuksa databroker |

## Debug

### Per-frame logs (always active)
| Event | Output | Meaning |
|---|---|---|
| Successful publish | `[KUKSA] Speed=X Traffic=Y` | Values sent to broker |
| Publish error | `[KUKSA] Erro: <message>` | gRPC error from broker |

## Notes
- `_select_signals` selects by largest `relative_area` — the closest/most prominent sign takes priority.
- Speed signs (`class_id` 0–1) and traffic signs (`class_id` 3–12) are selected independently.
- `class_id == 13` is used as a sentinel for "no detection" — it maps to code `0` in both signal types.
- `KuksaClient.close()` must be called at pipeline shutdown to release the gRPC channel.
- **Known import issue:** `kuksa_publish.py` imports `from object.perception_objects import Detection`, which assumes the working directory contains `object/`. When running from the pipeline root, this import fails. The correct import is `from post_processing.object.perception_objects import Detection`. The `Detection` type annotation is only used as documentation here; the method works with any list of objects with `class_id` and `relative_area` attributes.
