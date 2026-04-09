# Step 1: ONNX Export

## Environment

Run on the **host** (outside the container), with the venv activated.

## Commands

```bash
# Activate the virtual environment
source /path/to/hailo-env/bin/activate

# Export the model to ONNX — opset=17 required for YOLO26 at 640x640
cd /path/to/LKA_model/runs/yolov26sseg_cltusm_v/weights
yolo export model=best.pt format=onnx simplify=true imgsz=640 opset=17

# Copy to shared_with_docker
cp best.onnx /path/to/shared_with_docker/best.onnx

# Verify the generated file
ls -lh /path/to/shared_with_docker/best.onnx
```

## Notes

- **opset=17 required for YOLO26 at 640x640** — opset=12 causes a Reshape error in the attention:
  `Reshape: input shape {1,512,20,20} cannot be reshaped to {1,4,128,256}`
- `simplify=true` already provides sufficient simplification — additional `onnxsim` is not necessary
- `pipeline.sh` automates this entire step (export + copy) when called from the host
