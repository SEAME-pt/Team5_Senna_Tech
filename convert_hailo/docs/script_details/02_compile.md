# Technical Details: `convert_flow/scripts/compile.sh`

## Script role

`convert_flow/scripts/compile.sh` is the script that runs inside the Hailo container.

## Actual behavior

1. Receives the model name as the first argument.
2. Uses `yolov8n_seg` by default when no argument is provided.
3. Expects:
   - `/local/shared_with_docker/best.onnx`
   - `/local/shared_with_docker/calibration_images/`
4. Creates a temporary directory in `/tmp/hailo_compile`.
5. Copies `best.onnx` into that directory.
6. Runs:

```bash
hailomz compile <model> --ckpt ./best.onnx --calib-path /local/shared_with_docker/calibration_images --hw-arch hailo8
```

7. Moves generated `.hef` and `.har` files to `/local/shared_with_docker/`.

## Important notes

- the current `--hw-arch` is fixed to `hailo8`
- the script does not use `--model-script`
- the current flow produces raw output and depends on `nms_config.json` outside the `.hef`
