# Step 2: Translation / Parsing (ONNX to HAR)

## Environment

Run **inside the Hailo Docker container**.

```bash
# Enter the container (if not already inside)
sudo docker exec -it hailo8_ai_sw_suite_2025-10_container /bin/bash
```

## Script

Use the `scripts/conversion/translate.sh` script (runs inside the container):

```bash
bash /local/shared_with_docker/scripts/translate.sh
```

The script is configured for `yolo26s_seg_416` at 416x416. For other models
or resolutions, edit the variables at the top of the script.

## Python Command (reference)

```python
from hailo_sdk_client import ClientRunner

# Settings
model_name = "yolo26s_seg_416"
onnx_path = "/local/shared_with_docker/best_cut.onnx"  # already cut ONNX (without Tiles)
har_path = f"/local/shared_with_docker/{model_name}.har"

runner = ClientRunner(hw_arch="hailo8")
runner.translate_onnx_model(
    onnx_path,
    model_name,
    net_input_shapes={"images": [1, 3, 416, 416]}
)
runner.save_har(har_path)
print(f"[OK] HAR saved at: {har_path}")
```

**IMPORTANT**: Always use `best_cut.onnx` (after cut_onnx.sh), not the original `best.onnx`.
The original ONNX has `Tile` nodes that the Hailo DFC does not support.

## Verification

```bash
ls -lh /local/shared_with_docker/*.har
```

The `.har` file should be between 50-100MB depending on the model size.

## Troubleshooting

- **"Unsupported operator" error**: The ONNX model has operations not supported by Hailo.
  Try further simplification with `onnxsim` or check that the opset version is compatible.
- **Shape error**: Check that `net_input_shapes` matches the actual model input.
  Use `netron` (https://netron.app) to visually inspect the ONNX.
- **Input name**: The `"images"` field may vary. Check the actual input name with:
  `python3 -c "import onnx; m=onnx.load('best.onnx'); print(m.graph.input[0].name)"`
