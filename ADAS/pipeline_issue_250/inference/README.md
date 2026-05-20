# Inference Module

## Index
- [Overview](#overview)
- [Hardware](#hardware)
- [Hailo Platform](#hailo-platform)
- [API / Methods](#api--methods)
- [Data Contract](#data-contract)
- [Execution Flow](#execution-flow)
- [Notes](#notes)

## Overview
Executes models on the Hailo-8 accelerator and returns raw tensors for the subsequent pipeline stages.

The `HailoEngine` class was originally located in `core/hailo_engine.py`. During pipeline restructuring, it was moved to `inference/` because inference is a concrete functional stage of the execution flow, not a shared utility — which is the role of `core/`.

## Hardware
- **Accelerator:** Hailo-8 NPU
- **Models:** `yolo26n_seg_640.hef` (LKA), `yolo26n_v4.hef` (Object Detection)

## Hailo Platform
The inference module uses components from the `hailo_platform` library, which is the SDK responsible for providing access to the Hailo-8 accelerator and executing models compiled in the `.hef` format.

These imports do not belong to the pipeline's domain logic. They are part of the infrastructure required to load the model, configure the device, and execute inference on the hardware.

**`HEF`**
Responsible for loading the `.hef` file, which contains the model already compiled for execution on Hailo.

**`VDevice`**
Represents the virtual inference device. It is the abstraction used by the SDK to provide access to Hailo hardware and allow models to be configured and executed.

**`ConfigureParams`**
Responsible for creating configuration parameters used when loading the model onto the device.

**`HailoStreamInterface`**
Defines the communication interface used between the system and the Hailo device. In the current context, inference is configured to use `PCIe`.

**`InputVStreamParams`**
Responsible for configuring the input stream parameters of the network, i.e., how input data is sent to the model.

**`OutputVStreamParams`**
Responsible for configuring the output stream parameters, defining how inference results are read.

**`InferVStreams`**
Creates the inference pipeline used to send inputs to the model and receive network-generated outputs.

**`FormatType`**
Defines the output data format. In the current context, outputs are configured as `FLOAT32`, which facilitates post-processing in Python.

## API / Methods

### `HailoEngine.__init__(hef_path, target, debug=False)`
Loads the `.hef` model, prepares input metadata, and stores the necessary dependencies to configure the inference.

#### Parameters
- `hef_path` points to the `.hef` file to be executed.
- `target` is the `VDevice` or equivalent resource providing access to Hailo hardware.
- `debug` enables additional logs for loading, pre-processing, and output.

#### Effects
- Instantiates `HEF(hef_path)`.
- Reads the first `input_vstream_info` to get the input name.
- Initializes internal fields used by the context and execution.

### `HailoEngine.preprocess(img_rgb)`
Prepares an RGB frame for network input.

#### Behavior
- Resizes the frame to `self.net_size`.
- Adds batch dimension.
- Converts the array to `uint8`.

#### Output
- `numpy.ndarray` with shape `(1, net_size, net_size, 3)`.

#### Notes
- The method assumes RGB input.
- Debug logs show original shape, resized shape, and final dtype.

### `HailoEngine.__enter__()`
Configures the model on the Hailo device and prepares the inference pipeline.

#### Behavior
- Creates configuration parameters via `ConfigureParams.create_from_hef`.
- Configures the `target` with the `.hef`.
- Creates input and output stream parameters.
- Instantiates `InferVStreams` and opens the internal pipeline context.
- Updates `self.input_name` with the actual input stream key.

#### Effects
- Makes the engine ready for `infer()` calls.
- Returns its own instance for use with `with`.

### `HailoEngine.infer(img_rgb)`
Executes a complete inference for an RGB frame.

#### Behavior
- Calls `preprocess(img_rgb)`.
- Activates the network group with `self._ng.activate(...)`.
- Sends the input to `InferVStreams`.
- Returns the dictionary of raw network outputs.

#### Output
- `dict` with tensors produced by the model.

#### Notes
- In debug mode, logs output keys and shapes.
- The method depends on `__enter__` having been executed.

### `HailoEngine.__exit__(exc_type, exc_val, exc_tb)`
Closes the inference pipeline and releases resources associated with the context.

#### Behavior
- Emits a shutdown log in debug mode.
- Finalizes `self.pipeline` if it exists.

#### Effects
- Releases the context opened by `with`.
- Prevents leaving Hailo streams open after execution.

## Data Contract
| Field | Type | Shape |
|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(H, W, 3)` |

## Output
| Field | Type | Description |
|---|---|---|
| `outputs_lane` | `dict` | 4 raw tensors from the LKA model |
| `outputs_obj` | `dict` | 6 raw tensors from the Object Detection model |

## Execution Flow

Pre-processing pipeline per frame:
1. `cv2.resize(img_rgb, (640, 640))` — always 640×640 regardless of camera resolution.
2. `np.expand_dims(..., axis=0).astype(np.uint8)` — adds batch dimension, keeps uint8.
3. Input fed to `InferVStreams.infer()`. Outputs returned as `FLOAT32`.

The camera delivers RGB; no color conversion is performed here. Do not pass BGR frames.

## Initialization Order

- Data flow order: `camera → inference → post_processing → …`
- Resource initialization order: `VDevice → HailoEngine(lane) → HailoEngine(object) → Camera → loop`

Both engines share one `VDevice`. The engines must be ready before the camera loop starts to avoid producing frames before inference is available.

## Debug

### Lifecycle logs (always active)
None — the inference module does not emit lifecycle logs by default.

### Per-operation logs (`debug=True`)

| Event | Level | Message |
|---|---|---|
| HEF loading | `DEBUG` | `[INFERENCE] loading HEF: <path>` |
| Engine ready | `DEBUG` | `[INFERENCE] engine ready input_name=<name> net_size=640` |
| Frame preprocessed | `DEBUG` | `[INFERENCE] preprocess rgb=<shape> resized=<shape> batch=<shape> dtype=uint8` |
| Inference output | `DEBUG` | `[INFERENCE] output keys=[...]` |
| Output shapes | `DEBUG` | `[INFERENCE] output shapes={...}` |
| Engine closing | `DEBUG` | `[INFERENCE] closing engine: <path>` |

```python
engine = HailoEngine("model.hef", target, debug=True)
logging.basicConfig(level=logging.DEBUG)
```

## Notes
- `net_size` is hard-coded to 640. The model must have been compiled for 640×640 input.
- A new `_ng.activate()` context is opened on every `infer()` call. This is the correct pattern for Hailo SDK v4.x synchronous inference.
- Two `HailoEngine` instances sharing one `VDevice` is supported and is the pattern used in `main.py`.
