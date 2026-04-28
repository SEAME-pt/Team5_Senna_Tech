# BYOM (Bring Your Own Model) - Manual Flow

## Objective

Document the manual conversion process of custom YOLO models (e.g. YOLO26-seg)
to the Hailo-8 HEF format, using the `hailo_sdk_client` Python API (Dataflow Compiler).

This flow is required for models that **are not in the Hailo Model Zoo** and therefore
cannot be compiled with the `hailomz compile` command.

## When to use this flow

- Newer YOLO models (YOLO26, YOLOv13, etc.)
- Any custom ONNX model not supported by `hailomz`
- When full control over parsing, quantization and compilation is needed

## Pipeline

```
best.pt  -->  best.onnx  -->  best_cut.onnx  -->  model.har  -->  model_quantized.har  -->  model.hef
  (1)           (2)                (3)               (4)                  (5)                     (6)
```

1. **Training** - done externally (Ultralytics)
2. **ONNX Export** - `yolo export` with `opset=17` (on host, with venv)
3. **ONNX Cut** - `cut_onnx_small.sh` (small, 10 outputs) or `cut_onnx_nano.sh` (nano, 3 outputs) — avoids Agent infeasible (inside container)
4. **Translation/Parsing** - `ClientRunner.translate_onnx_model()` (inside container)
5. **Quantization/Calibration** - `ClientRunner.optimize()` (inside container, uses GPU)
6. **Compilation** - `ClientRunner.compile()` (inside container)

## Prerequisites

- Hailo Docker container running with `--runtime=nvidia --gpus all`
- Simplified `.onnx` model in the `shared_with_docker/` folder
- Calibration images in `shared_with_docker/calibration_images/` (minimum 1024)
- Access to `hailo_sdk_client` (available inside the container)
- **CUDA 12.3+** installed in the container for GPU mode (CUDA 11.8 causes `CUDA_ERROR_NOT_INITIALIZED` with drivers >= 560)
