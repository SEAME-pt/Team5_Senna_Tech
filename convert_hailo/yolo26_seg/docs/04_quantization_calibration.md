# Step 3: Quantization and Calibration (HAR to Quantized HAR)

## Environment

Run **inside the Hailo Docker container**. This step uses the GPU if available.

## Calibration image preparation

Images must be in `shared_with_docker/calibration_images/`.
Minimum recommended: **1024 images** representative of the training dataset.

## Configuration script (.alls) — Optional

For raw output (without integrated NMS), the `.alls` may contain only normalization:

```
# Standard YOLO normalization (divide by 255)
normalization1 = normalization([0.0, 0.0, 0.0], [255.0, 255.0, 255.0])
```

## Python Command

```python
import numpy as np
import os
from PIL import Image
from hailo_sdk_client import ClientRunner

# Settings
model_name = "yolo26s_seg"
har_path = f"/local/shared_with_docker/{model_name}.har"
calib_dir = "/local/shared_with_docker/calibration_images"
quantized_har_path = f"/local/shared_with_docker/{model_name}_quantized.har"

# Model input dimensions
IMG_H, IMG_W = 640, 640

# Function to load and preprocess calibration images
def load_calibration_data(img_dir, count=1024):
    images = []
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    files = files[:count]

    for fname in files:
        img = Image.open(os.path.join(img_dir, fname)).convert("RGB")
        img = img.resize((IMG_W, IMG_H))
        img_array = np.array(img).astype(np.float32)
        # Do NOT divide by 255 here if normalization is defined in the .alls
        images.append(img_array)

    return np.array(images)

# Load the runner with the HAR
runner = ClientRunner(har=har_path)

# (Optional) Load .alls script with normalization
# alls_path = "/local/shared_with_docker/scripts/yolo26s_seg.alls"
# runner.load_model_script(alls_path)

# Load calibration data
print("Loading calibration images...")
calib_dataset = load_calibration_data(calib_dir)
print(f"  -> {calib_dataset.shape[0]} images loaded ({calib_dataset.shape})")

# Run optimization/quantization
# NOTE: optimization_level was removed in recent SDK versions.
# The 2025-10 suite SDK does not accept this parameter.

# To control QFT batch size (avoid OOM on GPUs with low VRAM):
# runner.load_model_script("post_quantization_optimization(finetune, batch_size=2)\n")
# Correct syntax: post_quantization_optimization (NOT quantization_param)

print("Running quantization (this may take a few minutes)...")
runner.optimize(calib_dataset)

# Save quantized HAR
runner.save_har(quantized_har_path)
print(f"[OK] Quantized HAR saved at: {quantized_har_path}")
```

## Verification

```bash
ls -lh /local/shared_with_docker/*quantized*.har
```

## Important notes

- **Data format**: Array must be `[N, H, W, C]` (channels last), float32
- **Normalization**: If defined in `.alls`, do NOT normalize in Python (would normalize twice)
- **If not using .alls**: Divide by 255.0 in Python before passing to `optimize()`
- **GPU**: This step benefits from GPU. Check with `nvidia-smi` inside the container
- **CUDA**: Requires CUDA 12.3+ in the container. CUDA 11.8 causes `CUDA_ERROR_NOT_INITIALIZED` with drivers >= 560.
  To update: `sudo apt-get install -y cuda-toolkit-12-3` inside the container (requires NVIDIA repo added)
- **GPU memory**: `quantize.sh` does not use `memory_growth` or `memory_limit` — TF allocates as needed.
  Noise analysis completes normally with CUDA 12.3 and without TF pre-initialized in the script.
  Older script versions had TF pre-init that caused a corrupted fork; this was removed.
- **optimization_level**: Parameter removed in Hailo SDK suite 2025-10.
  Older versions accepted values 2 (balanced) and 4 (maximum accuracy)
- **quantize.sh via docker exec**: Works correctly with `LD_LIBRARY_PATH` and `TF_ENABLE_ONEDNN_OPTS=0`
  passed via `-e` in `docker exec`. `pipeline.sh` does this automatically in gpu mode.
