# Step 4: Compilation (Quantized HAR to HEF)

## Environment

Run **inside the Hailo Docker container**.

## Python Command

```python
from hailo_sdk_client import ClientRunner

# Settings
model_name = "yolo26s_seg"
quantized_har_path = f"/local/shared_with_docker/{model_name}_quantized.har"
hef_path = f"/local/shared_with_docker/{model_name}.hef"

# Load the quantized model
runner = ClientRunner(har=quantized_har_path)

# Compile to HEF
print("Compiling to HEF (this may take 5 to 15 minutes)...")
hef = runner.compile()

# Save the HEF binary
with open(hef_path, "wb") as f:
    f.write(hef)

print(f"[OK] HEF binary generated: {hef_path}")
```

## Verification

```bash
ls -lh /local/shared_with_docker/*.hef
```

The `.hef` file should be between 5-15MB depending on the model.

## After compilation

The `.hef` file can be copied to the Raspberry Pi 5 via SCP:

```bash
scp /path/to/shared_with_docker/yolo26s_seg.hef <user>@<rpi5-ip>:/destination/
```

## Internal compilation phases

The compiler runs internally:
1. **Partitioning** (~5-6 min) - splits the model into contexts for the Hailo-8
2. **Mapping** (~5-7 min) - allocates physical chip resources
3. **Kernel compilation** (~10s) - generates the final binary

## Troubleshooting

- **Resource error / concat24 Agent infeasible**: The compiler cannot allocate
  the multi-scale concatenation node. Solution: cut the ONNX BEFORE Concat_4,
  exposing the 3 separate tensors (box, score, mask_coef) as individual outputs.
  See `cut_onnx_nano.sh` (3 outputs) and `cut_onnx_small.sh` (10 outputs).

- **Performance Flow requires automatic resource utilization**: Occurs when
  `resources_param(max_memory_utilization=X)` is used together with
  `performance_param(compiler_optimization_level=max)`. The two are incompatible.
  Remove either `resources_param` or `performance_param`.

- **Partitioner stalls (progress bar stuck for 5+ min)**: The compiler is trying
  to maximize FPS with aggressive double buffering for large tensors (e.g. proto
  [1,32,160,160]). Solution: add `performance_param(fps=30)` to the .alls to
  force 60% resource utilization and give the partitioner more room.

- **PrePostAgent Agent infeasible (after successful partition)**: The DMA output
  agent cannot allocate buffers for large output tensors (~800KB for proto at 640x640).
  Attempted solutions in order:
  1. `resources_param(strategy=greedy, max_utilization=0.6)` — different allocation
     algorithm, may generate a partition compatible with PrePost.
  2. Reduce resolution to 416x416 (proto drops to [1,32,104,104], 58% smaller).
  3. Remove proto from HEF and run on CPU (split graph).

- **Invalid .alls commands (this DFC version)**: `normalization`,
  `output_format` and `max_context_clusters` are not compilation commands.
  `normalization` only works during the translation/optimization phase.
  Valid `resources_param` parameters: `max_apu_utilization`,
  `max_compute_utilization`, `max_compute_16bit_utilization`,
  `max_control_utilization`, `max_input_aligner_utilization`,
  `max_memory_utilization`, `max_utilization`, `strategy`.

- **Timeout**: Compilation can take up to 30 min for large models without GPU.
  Do not interrupt the process.

- **Hardware verification**: After copying the HEF to the RPi5, test with
  `TSHailo.py` or `hailortcli run` to validate inference.

## Recommended .alls configuration for models with proto head (segmentation)

```python
# For YOLOv8-seg / YOLO26-seg models with large proto output:
alls_script = """
resources_param(strategy=greedy, max_utilization=0.6)
"""
# If it still fails, try:
# performance_param(fps=30)
```

`strategy=greedy` uses a different allocation algorithm from the default that
can resolve the PrePostAgent infeasible error in segmentation models.
