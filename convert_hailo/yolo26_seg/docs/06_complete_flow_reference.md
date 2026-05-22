# BYOM Pipeline: YOLO26-seg for Hailo-8

## Overview

Conversion pipeline for YOLO26-seg (s/n) models to HEF format executable on Hailo-8.

```
best.pt -> best.onnx -> best_cut.onnx -> model.har -> model_quantized.har -> model.hef
  (export)   (cut_onnx)    (translate)     (quantize)                  (compile)
```

## Supported models

| Model | Params | GFLOPs | ONNX | Tested resolutions | ONNX cut | Compilation |
|--------|--------|--------|------|---------------------|------------|------------|
| yolo26s-seg | 10.4M | 34.1 | 39.9 MB | 416, 640 | cut_onnx_small.sh | greedy, 0.6 → 4 ctx |
| yolo26n-seg | 2.7M | 9.0 | 10.6 MB | 640 | cut_onnx_nano.sh | greedy, 0.9 → 3 ctx |

**IMPORTANT**: The two models use different ONNX cuts.
- small: `cut_onnx_small.sh` (10 outputs) — required to avoid `concat24 Agent infeasible`
- nano: `cut_onnx_nano.sh` (3 outputs) — required to avoid `matmul1 Agent infeasible` that occurs with 10 outputs

## Prerequisites

### On the host (outside container)
1. venv with `ultralytics` installed
2. Hailo Docker container running with GPU
3. Minimum **1024 calibration images** in `shared_with_docker/calibration_images/`
4. `best.pt` of the trained model

### Hardware requirements
- GPU with at least 8GB VRAM for quantization
- Noise analysis may stall on 8GB GPUs for large models (640x640 small)
- The nano model (2.7M params) fits better on smaller GPUs
- **CUDA 12.3+** required in the container for GPU mode. CUDA 11.8 causes `CUDA_ERROR_NOT_INITIALIZED` with drivers >= 560
  - Update inside the container: install NVIDIA repo and `sudo apt-get install -y cuda-toolkit-12-3`

## Step 0: Export ONNX

**IMPORTANT**: Use `opset=17`. opset=12 causes a Reshape error in the YOLO26 attention at 640x640.

```bash
cd /path/to/LKA_model
source /path/to/hailo-env/bin/activate

# Export (example: nano at 640)
yolo export model=runs/yolov26nseg_cltusm_v/weights/best.pt \
     format=onnx simplify=true imgsz=640 opset=17

# Copy to shared_with_docker
cp runs/yolov26nseg_cltusm_v/weights/best.onnx \
   /path/to/shared_with_docker/best.onnx
```

## Steps 1-4: Pipeline (run ON HOST, outside container)

### Option A: Automated pipeline (recommended)

```bash
# Run from the host — the pipeline manages the container automatically
cd /path/to/shared_with_docker/scripts
bash pipeline.sh yolov26sseg_cltusm_v yolo26s_seg_640 640 gpu
```

`pipeline.sh` runs in sequence:
1. Exports ONNX on the host (via hailo-env)
2. `cut_onnx_small.sh` — cuts into 10 separate outputs (**solution for Agent infeasible**)
3. `translate.sh` — ONNX -> HAR
4. `quantize.sh` — HAR -> quantized HAR (gpu mode uses CUDA 12.3 + QFT)
5. `compile_hef.sh` — quantized HAR -> HEF

**IMPORTANT**: For gpu mode, `quantize.sh` must be run from inside the container
(`pipeline.sh` does this automatically via `docker exec -t`).

### Option B: Individual scripts (inside container)

```bash
# Enter the CUDA 12 container
sudo docker run -it --runtime=nvidia --gpus all --net=host --privileged \
    -v /path/to/shared_with_docker:/local/shared_with_docker:rw \
    hailo8_cuda12_20260406 /bin/bash

# 1. Cut ONNX into 10 outputs (Agent infeasible solution)
bash /local/shared_with_docker/scripts/cut_onnx_small.sh 640

# 2. Translate ONNX -> HAR
bash /local/shared_with_docker/scripts/translate.sh yolo26s_seg_640 640

# 3. Quantize (GPU — run from inside container)
bash /local/shared_with_docker/scripts/quantize.sh yolo26s_seg_640 640 gpu

# 4. Compile HAR -> HEF
bash /local/shared_with_docker/scripts/compile_hef.sh yolo26s_seg_640
```

## Step 5: Deploy to RPi5

```bash
# Copy HEF to RPi5
scp /path/to/shared_with_docker/yolo26n_seg_640.hef \
    <rpi5-host>:~/

# On RPi5: test with camera
python3 test_yolo26_hailo.py camera yolo26n_seg_640.hef
```

## Scripts: Detailed description

### cut_onnx.sh
- **Input**: `best.onnx` (original ONNX with end-to-end Tiles)
- **Output**: `best_cut.onnx` (without Tiles, ready for Hailo)
- **Parameter**: `<input_size>` (416, 512, 640)
- **What it does**: Removes Tile/Gather/GatherElements nodes unsupported by the Hailo DFC. Cuts at `Concat_4` (raw detections) and keeps `output1` (proto for masks).
- **Auto-detects**: Number of channels (37 for s/1class, 38 for n, etc.)
- **Computes**: `NUM_ANCHORS = (size/8)^2 + (size/16)^2 + (size/32)^2`

### translate.sh
- **Input**: `best_cut.onnx`
- **Output**: `<model_name>.har`
- **Parameters**: `<model_name> <input_size>`
- **What it does**: Converts ONNX to HAR (Hailo Archive) format. Graph parsing.
- **Does not require GPU**

### quantize.sh
- **Input**: `<model_name>.har` + `calibration_images/`
- **Output**: `<model_name>_quantized.har`
- **Parameters**: `<model_name> <input_size>`
- **What it does**:
  1. Loads 1024 calibration images
  2. Applies QFT (Quantization-aware Fine-Tuning) with `batch_size=2`
  3. Runs Layer Noise Analysis (measures SNR per layer)
  4. Saves quantized HAR
- **GPU**: Configures TF with `memory_limit=2048MB` to avoid OOM in noise analysis
- **work_dir**: Saves checkpoint at `/tmp/hailo_workdir_<model>` (recoverable if process dies after QFT)

### compile_hef.sh
- **Input**: `<model_name>_quantized.har`
- **Output**: `<model_name>.hef`
- **Parameters**: `<model_name> <max_utilization> <strategy>`
- **What it does**: Compiles quantized HAR to HEF executable on Hailo-8
- **small optimization**: `resources_param(strategy=greedy, max_utilization=0.6)` → 4 contexts
- **nano optimization**: `resources_param(strategy=greedy, max_utilization=0.9)` → 3 contexts
- **Details**: See `docs/05_hef_compilation.md`

### recover_har.sh
- **Use**: When noise analysis stalls/crashes after QFT
- **What it does**: Attempts to reconstruct quantized HAR from checkpoint in work_dir
- **Parameter**: `<model_name>`

### pipeline.sh
- **Use**: Full automated pipeline (cut -> translate -> quantize -> compile)
- **Parameters**: `<model_name> <input_size>`
- **Stops on error** (`set -e`)

## Known issues

### Noise analysis stalls on GPU (8GB)
- **Symptom**: Progress bar stops at 50%, GPU at 0% utilization
- **Root cause**: TF pre-initialized in the script caused `multiprocessing.fork` to inherit corrupted CUDA state
  (not a VRAM issue as previously thought)
- **Applied solution**: Remove TensorFlow pre-initialization from `quantize.sh` GPU mode + CUDA 12.3 in container
- **Alternative (CPU)**: `CUDA_VISIBLE_DEVICES="" bash quantize.sh ...` to run everything on CPU (slow but completes)

### opset=12 fails on translate at 640x640
- **Symptom**: `Reshape: input shape {1,512,20,20} cannot be reshaped to {1,4,128,256}`
- **Cause**: Reshape in attention does not compute correct shapes with opset=12
- **Solution**: Export with `opset=17`

### Zeroed scores on Hailo (ch4 = zero-point)
- **Symptom**: All detections have the same score (e.g. 55), random masks
- **Cause**: Incomplete noise analysis (killed by OOM) — bad quantization ranges
- **Solution**: Ensure noise analysis completes. `test_yolo26_hailo.py` has a fallback: uses mask coefficient norm when scores have no variance

### Contexts in compilation
- Multi-context = model does not fit entirely in SRAM, runs in sequential parts
- Nano model (2.7M) requires more contexts than expected at 640x640 with proto
- See `docs/05_hef_compilation.md` for full error history and solutions

### concat24 Agent infeasible
- **Symptom**: Compilation fails immediately with `No successful assignments: concat24`
- **Cause**: Concat_4 (join of 3 scales) does not fit in SRAM in single/multi-context mode.
  The concatenated tensor [1,37,8400] (~1.2MB) is too large for the Hailo-8 DMA to allocate as a single output
- **Attempt 1**: `cut_onnx_nano.sh` (3 outputs: det + proto). Resolved concat24
  but generated `PrePostAgent infeasible` because the proto tensor [1,32,160,160] was still too large
- **Final solution**: `cut_onnx_small.sh` — exposes 10 separate outputs (9 heads + proto):
  ```
  cv2.0/1/2  -> bbox per scale:  [1,4,80,80]  [1,4,40,40]  [1,4,20,20]
  cv3.0/1/2  -> score per scale: [1,1,80,80]  [1,1,40,40]  [1,1,20,20]
  cv4.0/1/2  -> mask coef:       [1,32,80,80] [1,32,40,40] [1,32,20,20]
  proto      -> base masks:      [1,32,160,160]
  ```
  With smaller tensors per scale, the PrePostAgent can allocate DMA buffers without conflict.
  Post-processing manually concatenates the 3 scales of each type on the CPU (see `test_yolo26_hailo.py`, `per_scale` mode).

### PrePostAgent Agent infeasible
- **Symptom**: Partitioner finds a solution (5 contexts) but compilation fails when applying it
- **Cause**: DMA agent cannot allocate buffer for the proto tensor [1,32,160,160] (~800KB)
- **Solution**: Combination of `cut_onnx_small.sh` (10 smaller outputs) + `resources_param(strategy=greedy, max_utilization=0.6)` in `compile_hef.sh`
  `strategy=greedy` uses a different allocation algorithm that resolves the PrePostAgent buffer conflict

## Test files on RPi5

### test_yolo26_hailo.py
- **Auto-detects**: NET_SIZE, PROTO_SIZE and NUM_CHANNELS from HEF
- **Works with**: any yolo26 model (s, n) at any resolution
- **Modes**: `image <img> [hef]` or `camera [hef] [threshold]`
- **Flags**: `--no-display` (terminal only), `--remote` (MJPEG stream via stdout for SSH)
- **Pipeline**: Hailo inference -> mask -> BEV -> sliding windows -> CTE
- **Camera**: 640x360 @ 30fps (Full FoV via IMX708 2x2 ISP binning)
- **Display**: 1260x400 (resize of original frame after geometric overlay)
- **CPU stats**: shows user/sys/idle for all 4 cores via `/proc/stat`

#### Commands
```bash
# View on car screen (Wayland)
python3 test_yolo26_hailo.py camera yolo26s_seg_640.hef

# Terminal only, no display
python3 test_yolo26_hailo.py camera yolo26s_seg_640.hef --no-display

# Remote stream to host PC via SSH
ssh <rpi5-host> "python3 test_yolo26_hailo.py camera yolo26s_seg_640.hef --remote" | DISPLAY=:1 ffplay -f mjpeg -i -

# Image mode
python3 test_yolo26_hailo.py image photo.jpg yolo26s_seg_640.hef
```

#### Measured performance (RPi5, yolo26s_seg_640, 640x360)
- postproc: ~8ms | morph: ~1.3ms | BEV: ~2.4ms | sliding: ~9ms | total CPU: ~21ms
- CPU usage: ~27% of 1 core (~7% of total RPi5 with 4 cores)

### inspect_hef.py
- Shows input/output shapes, quantization, zero-points
- Useful to verify that quantization produced good ranges
