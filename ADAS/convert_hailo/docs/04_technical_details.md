# Updated and Centralized Flow

This manual process was replaced by the main script in `convert_flow/run_convert.sh`.

For the simplified current flow, use the documentation in **[01_run_convert.md](./01_run_convert.md)**.

---

# Technical Details of the ONNX-to-HEF Compilation Process with Hailo Dataflow Compiler

This document describes the main stages performed by the current compilation flow when converting a YOLOv8n-seg model from ONNX into HEF (Hailo Executable Format), based on the output of `hailomz compile`.

## General process

The `hailomz compile` command automates a series of complex steps. At a high level, it performs:

1. **Model parsing/translation:** converts the ONNX model into Hailo's internal representation (HAR - Hailo Archive).
2. **Optimization and quantization:** optimizes the model for Hailo hardware and quantizes it to 8 bits using the provided calibration data.
3. **Partitioning and mapping:** divides the model into contexts (subgraphs) that can run efficiently on Hailo hardware and allocates resources.
4. **HEF generation:** compiles the optimized and mapped model into the final HEF format.

## Compilation output analysis

### 1. Initialization and preliminary information

```text
Starting ONNX-to-HEF compilation...
ONNX model: best.onnx
Calibration data: /local/shared_with_docker/calibration_images/
Hailo architecture: hailo8
Hailo Model Zoo model: yolov8n_seg
--------------------------------------------------
[info] No GPU chosen and no suitable GPU found, falling back to CPU.
[info] First time Hailo Dataflow Compiler is being used. Checking system requirements...
[Info] No GPU connected.
# ... warnings about NumPy API ...
<Hailo Model Zoo INFO> Start run for network yolov8n_seg ...
<Hailo Model Zoo INFO> Initializing the hailo8 runner...
```

- **Initial messages:** confirm the input parameters (`.onnx`, calibration data, architecture, model name).
- **GPU/CPU:** this block represents a historical execution example. In the current flow, when Docker is correctly configured with an NVIDIA GPU, the expected log becomes `No GPU chosen, Selected GPU 0`.
- **Hailo Model Zoo INFO:** indicates that the Hailo Model Zoo is starting the process for model `yolov8n_seg`.

### 2. Translation/parsing (ONNX to HAR)

```text
[info] Translation started on ONNX model yolov8n_seg
[info] Restored ONNX model yolov8n_seg (completion time: 00:00:00.05)
[info] Extracted ONNXRuntime meta-data for Hailo model (completion time: 00:00:00.22)
[info] Start nodes mapped from original model: 'images': 'yolov8n_seg/input_layer1'.
[info] End nodes mapped from original model: '/model.22/cv2.2/cv2.2.2/Conv', '/model.22/cv3.2/cv3.2.2/Conv', '/model.22/cv4.2/cv4.2.2/Conv', '/model.22/cv2.1/cv2.1.2/Conv', '/model.22/cv3.1/cv3.1.2/Conv', '/model.22/cv4.1/cv4.1.2/Conv', '/model.22/cv2.0/cv2.0.2/Conv', '/model.22/cv3.0/cv3.0.2/Conv', '/model.22/cv4.0/cv4.0.2/Conv', '/model.22/proto/cv3/act/Mul'.
[info] Translation completed on ONNX model yolov8n_seg (completion time: 00:00:00.66)
[info] Saved HAR to: /local/shared_with_docker/yolov8n_seg.har
```

- **ONNX translation:** the compiler reads `best.onnx` and translates it to the internal HAR format.
- **Input/output nodes:** it identifies the input and output layers of the model. For segmentation models such as YOLOv8, there are multiple output nodes corresponding to different detection and segmentation heads.
- **HAR file:** a temporary `yolov8n_seg.har` file is produced. This is the model in Hailo's internal representation.

### 3. Calibration data preparation and optimization/quantization

```text
<Hailo Model Zoo INFO> Preparing calibration data...
[info] Loading model script commands to yolov8n_seg from /local/workspace/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/yolov8n_seg.alls
[info] Found model with 3 input channels, using real RGB images for calibration instead of sampling random data.
[info] Starting Model Optimization
[warning] Reducing optimization level to 0 (...) because there's less data than the recommended amount (1024), and there's no available GPU
[warning] Running model optimization with zero level of optimization is not recommended for production use and might lead to suboptimal accuracy results
[info] MatmulDecompose skipped
[info] Starting Mixed Precision
[info] Model Optimization Algorithm Mixed Precision is done (completion time is 00:00:00.34)
[info] Starting Statistics Collector
[info] Using dataset with 64 entries for calibration
Calibration: 100%|█████████████████████████| 64/64 [00:19<00:00, 3.20entries/s]
[info] Model Optimization Algorithm Statistics Collector is done (completion time is 00:00:20.63)
[info] Output layer yolov8n_seg/conv45 with sigmoid activation was detected. Forcing its output range to be [0, 1] ...
# ... additional output-layer adjustments ...
[info] Saved HAR to: /local/shared_with_docker/yolov8n_seg.har
```

- **Command loading:** the compiler loads extra configuration for `yolov8n_seg` from its own Model Zoo.
- **Calibration:** in this example, 64 images were used for calibration. Calibration determines the scale factors used to convert weights and activations to 8 bits with minimal accuracy loss.
- **Optimization warning:** the warning about `less data than recommended (1024)` applies to this historical example. In the current project flow, calibration was updated to 1024 images.
- **Optimization:** several techniques, such as Mixed Precision and Statistics Collector, are applied to prepare the model for Hailo hardware.

### 4. Partitioning and mapping

```text
[info] Starting Hailo allocation and compilation flow
[info] Building optimization options for network layers...
[info] Trying to compile the network in a single context
[info] Single context flow failed: Recoverable single context error
[info] Using Multi-context flow
# ... search for the best partition, optimizing performance ...
[info] Partitioner finished after 199 iterations, Time it took: 5m 42s 685ms
[info] Applying selected partition to 2 contexts...
[info] Validating layers feasibility
# ... layer validation ...
[info] Layers feasibility validated successfully
[info] Running resources allocation (mapping) flow, time per context: 59m 59s
# ... cluster and worker mapping ...
[info] Successful Mapping (allocation time: 6m 26s)
```

- **Allocation and compilation:** this is usually the most time-consuming stage. The compiler analyzes both the Hailo architecture and the model architecture to decide how layers will be executed across chip resources.
- **Multi-context flow:** the model was split into two contexts, meaning the compiler found a better way to execute it in multiple pieces on Hailo hardware.
- **Partitioning:** in this example, the best split took more than five minutes to find.
- **Mapping:** resource allocation also took several minutes. This stage ensures each model operation is mapped efficiently to physical chip resources.

### 5. HEF generation (final compilation)

```text
[info] Compiling kernels of yolov8n_seg_context_0...
[info] Compiling kernels of yolov8n_seg_context_1...
[info] Bandwidth of model inputs: 9.375 Mbps, outputs: 12.4664 Mbps (for a single frame)
[info] Bandwidth of DDR buffers: 0.0 Mbps (for a single frame)
[info] Bandwidth of inter context tensors: 10.9375 Mbps (for a single frame)
[info] Building HEF...
[info] Successful Compilation (compilation time: 7s)
[info] Saved HAR to: /local/shared_with_docker/yolov8n_seg.har
<Hailo Model Zoo INFO> HEF file written to yolov8n_seg.hef
--------------------------------------------------
Compilation to HEF completed successfully!
The HEF file was saved in the current directory with a standard name (for example `yolov8n_seg_hailo8.hef`).
yolov8n_seg.hef
```

- **Kernel compilation:** the compiler generates the executable code for each model partition.
- **Bandwidth report:** it estimates input, output, and inter-context bandwidth.
- **HEF generation:** the final HEF file is built.
- **Success:** `Successful Compilation` and `HEF file written to yolov8n_seg.hef` confirm that the process completed successfully.

This document explains the path taken by the model inside the Hailo Dataflow Compiler, from ONNX to HEF, and the purpose of each major phase.
