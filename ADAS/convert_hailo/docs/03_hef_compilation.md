# HEF Compilation

This document describes the real compilation flow used by the project.

## What triggers the compilation

The main flow `./convert_flow/run_convert.sh`:

- asks whether compilation should start
- checks the Hailo container state
- runs inside the container:

```bash
/local/shared_with_docker/scripts/compile.sh <model>
```

## Actual compilation script

The versioned source file is:

```bash
convert_flow/scripts/compile.sh
```

During the flow, it is copied to:

```bash
shared_with_docker/scripts/compile.sh
```

## What `compile.sh` does

Inside the container, it:

1. receives the Model Zoo model name, such as `yolov8n_seg`
2. uses `best.onnx` from `/local/shared_with_docker/`
3. uses calibration images from `/local/shared_with_docker/calibration_images/`
4. creates a temporary directory in `/tmp/hailo_compile`
5. runs `hailomz compile ... --hw-arch hailo8`
6. moves generated `.hef` and `.har` files to `/local/shared_with_docker/`

## Real dependencies

- running Hailo container
- `best.onnx` present in `/local/shared_with_docker/`
- calibration images present in `/local/shared_with_docker/calibration_images/`
- Model Zoo model compatible with the selection made in `run_convert.sh`

## Expected output

If everything works:

- the log shows `Successful Compilation`
- the `.hef` file is written to `shared_with_docker/`
- `run_convert.sh` prints the final summary and NMS parameters
