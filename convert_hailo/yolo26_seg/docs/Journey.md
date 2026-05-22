# Conversion Journey: YOLO26s and YOLO26n for Hailo-8

Chronological and technical log of all steps, decisions, errors, and solutions
found during the conversion of YOLO26s-seg and YOLO26n-seg models to the
executable HEF format on Hailo-8 (26 TOPS) via Raspberry Pi 5.

This document is written so that anyone on the team — even without prior
experience with Hailo — can understand what was done, why it was done,
and how to reproduce or adapt the process.

---

## Fundamental Concepts (read before continuing)

Before entering the journey, it is important to understand what each piece represents.

### What is the Hailo-8?

The Hailo-8 is an artificial intelligence chip (NPU — Neural Processing Unit)
specifically designed to execute neural networks with high energy efficiency.
It has **26 TOPS** (Tera Operations Per Second — trillions of operations per
second) of processing capacity and is connected to the Raspberry Pi 5 via PCIe.
[Ref: Hailo-8 Product Brief, hailo.ai]

**Why use an NPU instead of the Raspberry Pi CPU?**
The RPi5 CPU is a general-purpose processor — it knows how to do everything, but
nothing at extreme speed. The NPU is a radical specialist: it was built *only*
to perform matrix multiplications and additions (which is exactly what neural
networks do), consuming a fraction of the energy of a GPU.

*Analogy:* A CPU is like a Swiss Army knife — it's useful for everything. The NPU is like a
scalpel — it serves only one purpose, but with incomparable efficiency.

The chip **does not execute Python code**. It executes a compiled binary file
called **HEF (Hailo Executable Format)** — the equivalent of an "executable"
for Hailo hardware. All our work consists of converting the model trained in
PyTorch to this format. [Ref: Hailo Dataflow Compiler User Guide]

### What is the conversion pipeline?

Conversion is not direct (`.pt` → `.hef`). It goes through several stages:

```
best.pt          Trained model in PyTorch (Ultralytics)
   ↓  [export]
best.onnx        Open and portable format (Open Neural Network Exchange)
   ↓  [cut_onnx]
best_cut.onnx    Cut ONNX — we remove parts that Hailo does not support
   ↓  [translate]
model.har        HAR (Hailo Archive) — DFC's internal representation
   ↓  [quantize]
model_quantized.har    HAR with INT8 weights (quantized)
   ↓  [compile]
model.hef        Final binary executable on Hailo-8
```

Each arrow represents a different tool. The set of these tools is called the
**DFC (Dataflow Compiler)** — Hailo's compiler.
[Ref: Hailo Dataflow Compiler User Guide, Hailo Developer Zone]

**Why so many steps?**
Each format serves a different purpose:
- **`.pt` (PyTorch):** rich in training information, but tied to the Python
  framework. Not portable.
- **`.onnx` (Open Neural Network Exchange):** open standard that any tool
  can read. It is the "Esperanto" of AI — translates between frameworks.
  [Ref: onnx.ai]
- **`.har` (Hailo Archive):** Hailo has already "understood" the model graph
  and represented it in its internal language. It is not yet optimized for the chip.
- **`.hef` (Hailo Executable Format):** the final binary. It's like a Windows
  `.exe`, but specifically for the Hailo chip.

### What is quantization?

Trained models use floating-point numbers (**float32** — 32 bits per number,
precision of ~7 decimal places). The Hailo-8 operates with 8-bit integers
(**INT8** — 256 possible values, from -128 to 127). **Quantization** is the
process of converting model weights from float32 to INT8 without losing much
precision. [Ref: Jacob et al., "Quantization and Training of Neural Networks
for Efficient Integer-Arithmetic-Only Inference", CVPR 2018]

*Analogy:* Imagine a photo with 16 million colors (float32). Quantization is
converting that photo to 256 colors (INT8). If you choose the 256 most important
colors well, the image remains practically indistinguishable — and the file
becomes 4× smaller and much faster to process.

**Why does the chip operate in INT8?**
Simpler hardware, lower power consumption, and higher throughput. Multiplying
two 8-bit integers is much cheaper in silicon than multiplying two 32-bit floats.

For the conversion not to lose precision, the DFC needs **calibration images**:
representative samples of the real data the model will process in production.
It analyzes how numerical values are distributed in each layer of the network
and defines conversion limits (min/max per layer) to minimize rounding error.

We use **1024 images from the CULane dataset** (real road lanes) for calibration.
Using road images is critical — if we calibrated with cat photos, the
quantization limits would be bad for detecting lanes. [Ref: CULane Dataset,
Pan et al., "Spatial as Deep", CVPR 2018]

### What are "contexts" in Hailo?

The Hailo-8 has a limited amount of **SRAM** (Static RAM — internal chip
memory, extremely fast, but small). Large models do not fit entirely in SRAM.
The compiler divides the model into **contexts** — chunks that are loaded
sequentially into SRAM and executed one at a time.
[Ref: Hailo DFC User Guide — Model Compilation and Contexts]

*Analogy:* Imagine the chip is a kitchen with limited counter space. A large
model is like a recipe with 50 ingredients. With 3 contexts, you prepare the
recipe in 3 stages: use 17 ingredients, clean the counter, use another 17,
clean, use the last 16. It works, but it's slower than having all at once.

```
Context 1: backbone (feature extraction) → executes → result to SRAM
Context 2: neck (multi-scale fusion)       → executes → result to SRAM
Context 3: heads (detection and masks)     → executes → result to CPU
```

**Impact on performance:**
- Fewer contexts = faster execution (less data exchange between SRAM and RAM)
- More contexts = easier compilation (less pressure on SRAM space)

The `nano` ended up with **3 contexts** and the `small` with **4 contexts**.

### What are Tensors?

You will see this word often throughout the document. A **tensor** is simply a
multidimensional table of numbers.

- 1D Tensor (vector): a simple list — `[1.2, 3.4, 0.7]`
- 2D Tensor (matrix): a spreadsheet with rows and columns
- 3D Tensor: a stack of spreadsheets (e.g., an image is height × width × RGB channels)
- 4D Tensor: a batch of images (batch × height × width × channels)

When we write `[1,32,160,160]`, we are saying: 1 image, 32 channels (like 32
filtered "versions"), 160 pixels high, 160 pixels wide.
[Ref: TensorFlow Glossary — Tensors; PyTorch Docs — torch.Tensor]

### What is an "Agent" in the context of Hailo?

The Hailo-8 processes data in an internal pipeline. Internally, the compiler
assigns each operation to an "agent" — a hardware or software unit responsible
for executing that specific task. [Ref: Hailo DFC Internal Architecture]

The two most relevant agents in this journey were:

- **DMA Agent:** responsible for transferring data blocks between the chip's
  internal SRAM and external RAM. *Analogy: it is the factory's forklift
  operator — moving data from where it is to where it needs to be.*
- **PrePostAgent:** specifically handles transferring **output** tensors from the
  chip to the CPU at the end of each inference. It delivers the result.

When the compiler reports `Agent infeasible`, it means it tried all possible
layout combinations and **none of them** allowed allocating that tensor within
the agent's physical limits. It is almost always a size problem: the tensor is
too large to fit in the available contiguous buffer in that execution context.

---

## Starting Point — Why YOLO26?

The LKA (Lane Keeping Assist) project needed to detect road lanes in real-time,
onboard the vehicle, with low power consumption. The Raspberry Pi 5 with
Hailo-8 was chosen as the platform.

The initial model was **YOLOv8n-seg** — functional, but with heavy
post-processing on the RPi5 CPU due to NMS (Non-Maximum Suppression).

**YOLO26** was evaluated as a replacement for one main reason: it is
**NMS-free** (without Non-Maximum Suppression). The model already filters
detections internally, delivering the top 300 proposals directly without needing
NMS on the CPU. [Ref: Wang et al., "YOLOv10: Real-Time End-to-End Object
Detection", arXiv 2405.14458, 2024]

**What is NMS and why did it cost so much?**
In traditional models, the neural network spits out thousands of "guesses" of
where objects are (YOLOv8 generates ~8400 proposals per frame). NMS is the
algorithm that examines all these guesses and discards duplicates — keeping
only the best guess per detected object. Running NMS on 8400 boxes every frame,
on the RPi5's 4-core CPU, consumed precious processing time.

### Architectural difference between YOLOv8 and YOLO26

To understand the problems that will arise, it is important to know how each
model structures its outputs:

**YOLOv8-seg** produces 4 separate tensors by detection scale:
```
Scale 1 (small objects, stride 8):   bbox [1,4,80,80] + cls [1,1,80,80] + coef [1,32,80,80]
Scale 2 (medium objects, stride 16):  bbox [1,4,40,40] + cls [1,1,40,40] + coef [1,32,40,40]
Scale 3 (large objects, stride 32):   bbox [1,4,20,20] + cls [1,1,20,20] + coef [1,32,20,20]
Proto (base masks):                  [1,32,160,160]
```
The CPU receives these 10 tensors and needs to run NMS to decide which of the
~8400 proposals are real detections. This consumes CPU time.

**YOLO26-seg** does this work within the model itself:
```
Single detection output: [1,300,38]   ← already filtered, top-300
Proto (base masks):      [1,32,160,160]
```
The `38` is the composition of each detection: 4 (bbox) + 2 (score+class) + 32
(mask coefficients). The CPU receives only 300 already selected proposals — much less work.

**The problem:** this internal filtering uses operations (`Tile`, `Gather`,
`GatherElements`) that Hailo DFC does not support. This is exactly what makes
the conversion non-trivial.

---

## Fundamental Problem — Unsupported Operators by DFC

### Why doesn't Hailo support all ONNX operators?

Hailo is specialized hardware. Unlike a general-purpose GPU that executes any
CUDA instruction, the Hailo chip has a **fixed and limited** set of operations
it knows how to execute in silicon: convolutions, batch normalization,
activations (ReLU, Sigmoid), pooling, etc.
[Ref: Hailo DFC Supported Operators List, Hailo Developer Zone]

*Analogy:* A GPU is like a scientific calculator that can perform any
calculation. Hailo is like a specialized adding machine — it performs matrix
additions and multiplications at absurd speed, but doesn't know how to calculate
logarithms, for example.

**Dynamic** operations like `Tile` (which replicates a tensor based on values
calculated *at runtime*, not at compile time) are impossible to map to the
fixed hardware of the chip — because the hardware doesn't know beforehand how
many replicas it will need to create. Hailo's execution graph is completely
static: everything must be known at compile time.

This is expected and documented by Hailo — even official models like YOLOv8 have
their post-processing (NMS) running on the CPU, not on the chip.

### First attempt: export and compile directly

```bash
# Export model from PyTorch to ONNX
yolo export model=best.pt format=onnx simplify=true imgsz=640 opset=12

# Try to compile directly (inside the Docker container)
bash translate.sh yolo26s_seg_640 640
```

Immediate result:
```
Error: Unsupported operator: Tile
```

The DFC stopped at the first `Tile` instruction it encountered. There is no way
around this without modifying the model.

### Analyzing the ONNX graph to understand where to cut

To solve the problem, we needed to understand exactly where the `Tile` appeared
in the graph and what was before them (that could be executed on the chip).

Using `onnx.shape_inference` and inspecting the graph node by node, we mapped the
model's structure in the detection head (`/model.23/`):

```
Backbone + Neck  (convolutions, attention — all supported by Hailo)
    │
    ▼
Detection heads per scale:
  cv2.* → bbox       │
  cv3.* → scores     │  → 9 separate tensors by scale and type
  cv4.* → mask coefs │
    │
    ▼
Reshape (×9)  →  reorganizes each tensor to common format
    │
    ▼
Concat   → joins bboxes from all scales: [1,4,8400]
Concat_1 → joins scores:                  [1,1,8400]
Concat_2 → joins mask coefs:              [1,32,8400]
    │
    ▼
Concat_4  →  joins everything: [1,37,8400]   ← SAFE CUT POINT
    │
    ▼
Tile (×3), Gather, GatherElements  ← BLOCKAGE (not supported)
    │
    ▼
output0 [1,300,38]  ← original NMS-free output

(parallel to the flow above)
Proto branch → output1 [1,32,160,160]  ← always OK for Hailo
```

**Conclusion:** everything up to `Concat_4` is computation that Hailo can do.
Everything after is the top-k (filtering the top 300), which cannot run on the
chip.

The solution is to **cut the ONNX exactly at `Concat_4`** and move the top-k
to the RPi5 CPU. This is exactly what the `cut_onnx_*.sh` scripts do.

### Additional problem: opset=12 breaks the model at 640×640

During testing, we discovered that exporting with `opset=12` caused a second
failure in `translate`:

```
Reshape: input shape {1,512,20,20} cannot be reshaped to {1,4,128,256}
```

**What happens:** YOLO26 uses **PSA (Partial Self-Attention)** blocks. The
attention mechanism needs to reorganize data internally via `Reshape`
operations. With `opset=12`, ONNX cannot represent these shapes **statically**
for 640×640 resolution — the Ultralytics exporter generates symbolic dimensions
(like `?` instead of `20`) that DFC cannot resolve.
[Ref: ONNX Opset Changelog, opset 13+ resolve dynamic reshape shapes]

**What is opset?** The ONNX format has versions called "opsets". Each new
version adds or improves how certain operations are represented in the file.
Opset 17 correctly represents Reshape dimensions in attention blocks at any
fixed resolution.

**Solution:** always export with **opset=17**. In this version of the ONNX
format, shapes are correctly resolved by the Ultralytics exporter.

```bash
# CORRECT
yolo export model=best.pt format=onnx simplify=true imgsz=640 opset=17

# INCORRECT for 640×640
yolo export model=best.pt format=onnx simplify=true imgsz=640 opset=12
```

---

## Journey of YOLO26s-seg (small)

### Small model characteristics

| Property | Value | Comparison |
|---|---|---|
| Parameters | 10.4M | ~3× YOLOv8n-seg (3.4M) |
| GFLOPs | 34.1 | ~3× YOLOv8n-seg (~12.0) |
| Original ONNX | 39.9 MB | largest model of this journey |
| Resolution | 640×640 | maximum tested |

As it is larger, the small model presented more memory allocation challenges
on the chip.

---

### Attempt 1 — Generic cut (cut_onnx.sh): 2 outputs

**Idea:** cut the ONNX at `Concat_4` and expose two tensors:
- `Concat_4_output_0`: [1,37,8400] — all concatenated detections
- `output1`: [1,32,160,160] — proto (base masks)

The `cut_onnx.sh` script does this: removes all nodes after `Concat_4` (Tiles
and everything that follows) and defines these two outputs.

```bash
bash cut_onnx.sh 640
bash translate.sh yolo26s_seg_640 640
bash compile_hef.sh yolo26s_seg_640
```

**Result:**
```
No successful assignments: concat24 Agent infeasible
```

**Why did it fail?**

The `[1,37,8400]` tensor has approximately **1.2 MB** in float32 (37 × 8400 × 4
bytes = 1.244 MB). To transfer this tensor from SRAM to system memory, the DMA
agent needs a **contiguous buffer** — that is, a single, uninterrupted block of
physical memory of 1.2 MB.

*Analogy:* it's like trying to stack 1200 boxes at once in an elevator that has
a capacity for 400. No matter how you organize the boxes on the floor — the
elevator simply doesn't hold everything at once.

With 1.2 MB, the compiler tried all possible context partitioning combinations
— none created an SRAM layout with this contiguous space available.

**What we learned:** a single output tensor that is too large completely blocks
the compiler. The solution must be to divide this tensor into smaller pieces
— no parameter configuration solves a physical size problem.

---

### Attempt 2 — 3 output types (cut_onnx_nano.sh): 4 outputs

**Idea:** instead of exposing the entire `Concat_4` (37 concatenated channels),
cut before `Concat_4` and expose the 3 separate types + proto:

```
Concat   [1,4,8400]   → bboxes from all scales
Concat_1 [1,1,8400]   → scores from all scales
Concat_2 [1,32,8400]  → mask coefs from all scales
output1  [1,32,160,160] → proto (same as before)
```

In this way, the largest individual tensor goes from 1.2 MB to ~1 MB
(the `Concat_2` with 32 channels). Still large, but the hope was that the
compiler could manage it.

```bash
bash cut_onnx_nano.sh 640
bash translate.sh yolo26s_seg_640 640
bash compile_hef.sh yolo26s_seg_640 0.6 greedy
```

**Result:** the `concat24 Agent infeasible` disappeared! But a new error arose:

```
PrePostAgent Agent infeasible
```

**Why did it fail?**

The `PrePostAgent` is the agent responsible for transferring output tensors
from the chip to system memory after each inference. The proto tensor
`[1,32,160,160]` has approximately **800 KB** in INT8 (32 × 160 × 160 bytes).

The compiler found a partition of 5 contexts where the model fit in SRAM, but
when it tried to map the `PrePostAgent` to transfer the proto at the end of each
context, it did not find enough space in the output buffer.

We tried `max_utilization` at 0.6, 0.8, and 0.9 with `strategy=greedy` — all
combinations failed with the same error for small with 4 outputs. The 800 KB
proto continued to be too large for this layout.

**What we learned:** reducing detection outputs from 1 to 3 types was not
enough. The real problem is the 160×160 proto — we need a context layout where
the `PrePostAgent` has enough buffer for it.

---

### Attempt 3 — 10 separate outputs (cut_onnx_small.sh): SUCCESS

**Idea:** instead of concatenating the 3 scales into a single tensor per type,
expose each scale individually. This means cutting before Reshapes and Concats,
exposing raw tensors from each head:

```
cv2.0 [1,4,80,80]   cv2.1 [1,4,40,40]   cv2.2 [1,4,20,20]   ← bbox per scale
cv3.0 [1,1,80,80]   cv3.1 [1,1,40,40]   cv3.2 [1,1,20,20]   ← scores per scale
cv4.0 [1,32,80,80]  cv4.1 [1,32,40,40]  cv4.2 [1,32,20,20]  ← mask coefs per scale
conv109 [1,32,160,160]                                         ← proto
```

**Why does this solve the problem?**

The largest individual tensor is now `cv4.0` with `[1,32,80,80]` = 204 KB (much
smaller than the previous 1.2 MB). With smaller output tensors, the
`PrePostAgent` can allocate DMA buffers for each one without conflict.

The price to pay is on the CPU: post-processing in Python needs to manually
concatenate the 3 scales of each type before calculating detections. This is
done in `test_yolo26_hailo*.py` in `per_scale` mode. In practice, this
concatenation is a very fast `numpy.concatenate` operation — it is not a
measurable bottleneck compared to the ~13ms of on-chip inference.

```bash
bash cut_onnx_small.sh 640
bash translate.sh yolo26s_seg_640 640
bash quantize.sh yolo26s_seg_640 640 gpu
bash compile_hef.sh yolo26s_seg_640 0.6 greedy
```

**Result: SUCCESS**

| Metric | Value |
|---|---|
| Contexts | 4 |
| Compilation time | ~25 minutes |
| HEF size | 21.5 MB |
| Date | 04/06/2026 |

---

### Problems during small model quantization

Quantization (`quantize.sh` step) was the most laborious part. Two distinct
problems had to be solved.

#### Problem 1 — CUDA_ERROR_NOT_INITIALIZED with new drivers

The original Hailo container (`hailo8_ai_sw_suite_2025-10`) came with **CUDA
11.8** installed. This worked well with old host drivers. With newer host
drivers (version >= 560, required for RTX GPU), CUDA 11.8 in the container
became incompatible: [Ref: NVIDIA CUDA Compatibility Matrix,
docs.nvidia.com/deploy/cuda-compatibility]

```
CUDA_ERROR_NOT_INITIALIZED: initialization error
```

**Why does this happen in Docker?**
Docker isolates the container's file system, but **does not** isolate the kernel
or hardware drivers. The CUDA runtime inside the container (version 11.8) needs
to communicate with the host kernel driver (version >= 560). When these versions
are too incompatible, initialization fails.
[Ref: NVIDIA Container Runtime, github.com/NVIDIA/nvidia-container-toolkit]

**Solution:** create a new Docker container (`hailo8_cuda12_20260406`) from the
original image, but with CUDA 12.3 manually installed inside it:

```bash
# Inside the old container:
wget https://developer.download.nvidia.com/...  # CUDA 12.3 repository
sudo apt-get install -y cuda-toolkit-12-3

# Commit container as new image:
docker commit hailo8_ai_sw_suite_2025-10_container hailo8_cuda12_20260406
```

With CUDA 12.3 in the container and driver >= 560 on the host: compatibility OK.

#### Problem 2 — Noise Analysis hangs at 50% (fork + CUDA)

With the CUDA problem solved, quantization started but stopped at ~50% during
**Layer Noise Analysis** — GPU utilization went to 0% and the process stayed
suspended indefinitely.

**What is Layer Noise Analysis?**

It is a stage of quantization where DFC measures, layer by layer, how much the
float32→INT8 conversion degraded the signal. The metric used is **SNR (Signal-to-
Noise Ratio)**. The higher a layer's SNR, the better quantization preserved the
information. Layers with low SNR can compromise the entire model's accuracy.

To calculate SNR, DFC runs the model twice with each calibration image: once in
float32 (original version) and once in INT8 (quantized version), and compares
activations layer by layer. That's why it's slow — 1024 images × 2 passes × all
layers.

**Why did it hang?**

DFC's `ClientRunner.optimize()` uses Python's `multiprocessing.fork` to create
parallel processes during noise analysis. `fork` is a Linux call that creates an
exact copy of the current process — including all memory and all open states,
like GPU connections.

The problem: **CUDA does not support contexts inherited via fork**. If
TensorFlow (which opens a GPU connection) has already been imported in the
parent process, the child process inherits a CUDA connection in an invalid
state. It tries to use it, can't, and waits forever — silent deadlock.
[Ref: Python Multiprocessing Docs — "Safe importing of main module"; NVIDIA CUDA
Programming Guide — Context Management]

*Analogy:* it's like opening a video call and then trying to pass it to someone
else without hanging up first. The other person receives the phone with the
call stuck in a transition state — neither terminating nor continuing.

**How we identified the cause:**
The original `quantize.sh` imported TensorFlow at the beginning of the script
for other auxiliary operations. This import already initialized the CUDA
context before `ClientRunner.optimize()` was called.

**Solution:** remove any `import tensorflow` (and any code that implicitly
initializes it) from `quantize.sh` before the `ClientRunner` call. DFC
initializes TF internally, in the correct child process, without inheriting
contaminated state.

```python
# WRONG — initializes TF before fork
import tensorflow as tf
runner = ClientRunner(har=har_path)
runner.optimize(calib_data)   # fork here → child inherits initialized TF → deadlock

# CORRECT — no TF import before optimize
runner = ClientRunner(har=har_path)
runner.optimize(calib_data)   # fork here → child initializes clean TF → OK
```

**Alternative without GPU (CPU mode):**

If the GPU causes problems, it is possible to force quantization on the CPU:
```bash
CUDA_VISIBLE_DEVICES="" bash quantize.sh yolo26s_seg_640 640 cpu
```
Slower (hours vs minutes), but completes without hanging.

**The role of recover_har.sh:**

When noise analysis hung after completing **QFT (Quantization-aware Fine-
Tuning)**, quantized weights were already saved to disk in `work_dir`
(`/tmp/hailo_workdir_<model>/`).

**What is QFT?** It is the first phase of `optimize()`. It adjusts model weights
(still in float32) so that, when converted to INT8, precision is maximized. It
is a fine-tuning process specific to quantization.

`recover_har.sh` reconstructs the quantized HAR from this checkpoint, skipping
the hung noise analysis. This way we don't need to redo QFT (which can take 30-60
minutes) — only noise analysis needs to be redone, this time without pre-
initialized TensorFlow.

This saved hours of rework across multiple sessions where the process hung.

---

## Journey of YOLO26n-seg (nano)

### Nano model characteristics

| Property | Value | Comparison with small |
|---|---|---|
| Parameters | 2.7M | ~4× smaller |
| GFLOPs | 9.0 | ~4× smaller |
| Original ONNX | 10.6 MB | ~4× smaller |
| Resolution | 640×640 | equal |

As it is smaller, we expected nano to be easier to compile. In practice, a
different internal architecture created a different problem.

### The critical architectural difference between nano and small

Although both are YOLO26, nano and small have internally different detection
heads. In nano, the `matmul1` node (a matrix multiplication inside the PSA
attention head) has **two consumers** — that is, two different graph nodes
depend on its result.

**What is double-buffering?**
When a node has two consumers that need to use its result independently, the
Hailo compiler needs to maintain **two buffers** for this result in SRAM. Thus,
consumer A can be reading buffer 1 while the result for consumer B is already
being written to buffer 2 — without conflict between them.
[Ref: Hailo DFC — Memory Allocation Strategy, Hailo Developer Zone]

*Analogy:* it's like a printer with two output trays — document A goes to tray 1
while document B goes to tray 2, without mixing.

The problem: with **10 separate outputs** (as in small), the compiler needs to
simultaneously allocate DMA buffers for 10 output tensors *plus* the two buffers
of `matmul1` double-buffering. The sum exceeds available SRAM space. With **4
outputs** (nano cut), there is space left for double-buffering.

---

### Attempt 1 — Use the same approach as small (10 outputs): FAILURE

**Reasoning:** if it worked for small, why not for nano? Nano is smaller, it
should be easier.

```bash
bash cut_onnx_small.sh 640
bash translate.sh yolo26n_seg_640 640
bash compile_hef.sh yolo26n_seg_640 0.6 greedy
```

**Result:**
```
matmul1 Agent infeasible
```

**Why did it fail?**

With 10 separate outputs, the compiler tries to allocate DMA buffers for each
one. `matmul1` with 2 consumers needs double-buffering. The combination of
output buffers (10 tensors) + matmul1 double-buffer exceeds what the compiler
can map in available SRAM.

**Counter-intuitive:** more smaller outputs do not help nano — it hurts. Nano
needs fewer outputs to free up space for matmul1 double-buffering.

---

### Attempt 2 — 4 outputs with greedy 0.6 and 0.8: PrePostAgent

**Reasoning:** use `cut_onnx_nano.sh` (4 outputs) which was the intermediate
cut. With fewer outputs, matmul1 should get its double-buffer.

```bash
bash cut_onnx_nano.sh 640
bash translate.sh yolo26n_seg_640 640
bash compile_hef.sh yolo26n_seg_640 0.6 greedy   # → 5 contexts, PrePostAgent infeasible
bash compile_hef.sh yolo26n_seg_640 0.8 greedy   # → 4 contexts, PrePostAgent infeasible
```

**Result:** `matmul1` was resolved, but `PrePostAgent infeasible` returned.

The problem is the same as for small: the 160×160 proto (~800 KB) is too large
for the `PrePostAgent` buffer in the current context layout.

**Why is 5 contexts worse than 3?**

With more contexts, the model is split into more pieces — and SRAM needs to
accommodate communication buffers between these pieces. Each boundary between
contexts requires input and output buffers. With 5 contexts, SRAM becomes more
**fragmented**: there are many small buffers scattered around, but no large
enough contiguous space left for `PrePostAgent` to allocate the 800 KB proto.

*Analogy:* imagine a shelf where you keep objects of various sizes. With many
small things scattered around (5 contexts → more edge buffers), the shelf might
have 2 meters free in total — but distributed in 10 spaces of 20 cm each. An 80
cm box (the proto) simply doesn't fit in any of the individual spaces, even if
there is enough total space.

With fewer contexts (3), the model is executed in larger blocks. SRAM becomes
more **consolidated** — fewer edge buffers, more contiguous space — and
`PrePostAgent` finds space for the proto at once.

---

### Attempt 3 — 4 outputs with greedy 0.9: SUCCESS

**Reasoning:** `max_utilization=0.9` allows the compiler to use 90% of chip
resources per context (instead of 60% or 80%). With more resources per context,
the model fits in fewer contexts — from 5 to 3. With 3 contexts, the allocation
layout changes enough for `PrePostAgent` to allocate the proto buffer.

```bash
bash cut_onnx_nano.sh 640
bash translate.sh yolo26n_seg_640 640
bash quantize.sh yolo26n_seg_640 640 gpu
bash compile_hef.sh yolo26n_seg_640 0.9 greedy
```

**Result: SUCCESS**

| Metric | Value |
|---|---|
| Contexts | 3 |
| Compilation time | ~13 minutes |
| HEF size | 9.1 MB |
| Date | 04/06/2026 |

### How to understand the max_utilization parameter

```
max_utilization = 0.6  →  uses up to 60% of SRAM per context
                           compiler has more partitioning freedom
                           tends to generate more contexts (4, 5, 6...)
                           useful when there are allocation conflicts

max_utilization = 0.9  →  uses up to 90% of SRAM per context
                           compiler is more aggressive in packaging
                           tends to generate fewer contexts (2, 3, 4...)
                           useful when the problem is precisely having many contexts
```

For nano, the problem was having too many contexts → increasing utilization
resolves. For small, the problem was output tensor too large → dividing the
tensor resolves.

### Nano output format after compilation

`cut_onnx_nano.sh` cuts before `Concat_4` and exposes tensors already processed
by attention (pre-concat), resulting in 4 outputs:

| HEF Tensor | Shape | What it contains |
|---|---|---|
| `ew_mult1` | (1,8400,4) | bbox coordinates (all scales together) |
| `activation3` | (1,8400,1) | confidence scores |
| `concat22` | (1,8400,32) | mask coefficients |
| `conv109` | (160,160,32) | proto — the 32 base masks |

Note that nano already delivers tensors with the 8400 proposals concatenated
(unlike small which delivers per scale). The inference script detects this
automatically via `find_output_keys()` and uses `pre_concat4` mode for nano and
`per_scale` for small.

---

## Deploy on RPi5 and validation

### Transferring HEFs to Raspberry Pi 5

```bash
# From dev host to RPi5 via SSH
scp shared_with_docker/yolo26n_seg_640.hef root@10.21.220.158:~/
scp shared_with_docker/yolo26s_seg_640.hef root@10.21.220.158:~/
```

### Verification with hailortcli parse-hef

Before running any inference, verify HEF structure:

```bash
# On RPi5
hailortcli parse-hef ~/yolo26n_seg_640.hef
```

It should show input and output tensors. If shapes correspond to expected (input
640×640×3, outputs with tensors described above), the HEF is integral.

### Performance benchmark (hailortcli benchmark)

To measure real hardware performance without Python code interference:

```bash
hailortcli benchmark ~/yolo26n_seg_640.hef
hailortcli benchmark ~/yolo26s_seg_640.hef
```

Results measured on 04/07/2026:

| Model | FPS hw_only | HW Latency | Contexts | HEF |
|---|---|---|---|---|
| yolo26n_seg_640 | **68.72 FPS** | 13.45 ms | 3 | 9.1 MB |
| yolo26s_seg_640 | **33.24 FPS** | 28.50 ms | 4 | 21.5 MB |

`hw_only` = Hailo processing in a loop without CPU, without camera. It is the
chip's theoretical maximum throughput for this model. In practice with camera
and CPU, real FPS will be lower.

### Real-time monitoring with HAILO_MONITOR

To see NPU utilization while script runs:

```bash
# Terminal 1: run script with monitoring enabled
HAILO_MONITOR=1 python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef --remote

# Terminal 2: open monitor
hailortcli monitor
```

The monitor shows utilization, temperature, and latency in real-time.

### Developed LKA inference pipeline

After validating that HEFs worked, work continued on developing the complete
inference script for the LKA system:

```
RPi Camera (640×360 @ 30fps)
    ↓  [rpicam-vid — YUV420 capture]
BGR Frame
    ↓  [preprocess — resize + normalize]
Hailo-8 Inference  (yolo26n_seg_640.hef)
    ↓  [~13ms HW latency]
Output tensors (bbox, scores, coefs, proto)
    ↓  [yolo26_to_mask — CPU]
Binary lane mask
    ↓  [morphology — erosion + dilation]
Clean mask
    ↓  [BEV Transform — top-down perspective]
Bird's Eye View of the lane
    ↓  [Sliding Windows + Polyfit]
Left and right polynomials
    ↓  [CTE calculation]
Lateral error in meters (CTE)
    ↓  [Visual overlay + MJPEG encode]
Remote stream via SSH / Local Wayland display
```

Field calibrated parameters:
- **BEV Trapezoid:** `[0.255, 0.44], [0.745, 0.44], [1.17, 1.00], [-0.17, 1.00]`
- **Temporal Smoothing:** `alpha=0.25` (25% current frame, 75% history)
- **Overlay:** `Hailo: Xms | FPS | NPU: X% | Post: Xms | Temp: XC`
- **NPU% Calculation:** `current_fps / 68.72 × 100 × 0.95` (0.95 factor calibrated with hailortcli monitor)

---

## PCIe descriptor page size problem in AGL kernel

After resolving all compilation problems and generating the HEF, when trying to
run the model on RPi5 with AGL (Automotive Grade Linux), an unexpected error
appeared **even before inferring the first frame**:

```
[HailoRT] [error] CHECK failed - max_desc_page_size given 16384 is bigger
                  than hw max desc page size 4096
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_INTERNAL_FAILURE(8)
[HailoRT CLI] [error] Failed configure vdevice from hef
```

### Why does this happen?

Hailo-8 communicates with RPi5 via **PCIe (PCI Express)** — the same bus
standard used by GPUs and NVMe SSDs. To transfer data (camera frames and
detection results) between CPU RAM and the Hailo chip, the system uses **DMA
(Direct Memory Access)**. [Ref: Linux Kernel DMA API Documentation,
kernel.org/doc/Documentation/DMA-API-HOWTO.txt]

**What is DMA?**
DMA is a mechanism that allows hardware to directly access RAM *without* needing
to interrupt the CPU for every byte transferred. Without DMA, the CPU would have
to manually copy each frame to the chip — wasting precious cycles on data
movement instead of processing. With DMA, the chip fetches and delivers data on
its own while the CPU does something else.

*Analogy:* without DMA, the CPU would be like a waiter carrying one plate at a
time between the kitchen and the table. With DMA, there is an automatic
conveyor belt — the waiter only needs to start the delivery and the system
takes care of the rest.

For DMA to work, the driver creates a **descriptor list** — a table in memory
where each entry points to a data block and indicates its size:

```
Descriptor 0 → [16384 byte block] ← part of input frame
Descriptor 1 → [16384 byte block] ← part of input frame
...
```

**HailoRT uses 16384 byte (16 KB) blocks by default**. With larger blocks, fewer
descriptors are needed per frame → less control overhead → higher throughput.
[Ref: HailoRT Driver Source, github.com/hailo-ai/hailort-drivers]

The problem is that the **AGL (Automotive Grade Linux) kernel was compiled with
a conservative restriction** specific to automotive environments, where physical
memory may be fragmented across multiple devices. The kernel's DMA subsystem
(`dma_get_max_seg_size`) returns **4096 bytes (4 KB)** as the maximum supported
size for contiguous mappings.

When the `hailo_pci` driver loads, it consults the kernel:
> "What is the maximum DMA block size you support?"
> AGL Kernel responds: 4096 bytes

The driver then passes this limitation to HailoRT, which tries to create 16384
byte descriptors. The driver detects the incompatibility and refuses to continue
— because trying to map 16 KB when the kernel supports only 4 KB would result in
**memory corruption** (writing outside the allocated region).

### The solution

```bash
# Temporary (for immediate testing):
modprobe -r hailo_pci
modprobe hailo_pci force_desc_page_size=4096

# Permanent (survives reboot):
echo 'options hailo_pci force_desc_page_size=4096' >> /etc/modprobe.d/hailo_pci.conf
reboot
```

The `force_desc_page_size=4096` parameter forces the driver to use 4096 byte
blocks from the start, matching the AGL kernel limit. Hailo-8 hardware accepts
any size — the limitation was exclusively on the kernel side.

### Impact on performance

Despite using 4× more descriptors per frame (75 instead of ~19), the impact is
minimal because the real bottleneck is Hailo-8's internal processing, not PCIe
transfer. With the fix applied:

| Metric | Value |
|---|---|
| hw-only FPS (YOLOv8s) | 398.44 |
| streaming FPS | 381.59 |
| HW Latency | 6.71 ms |
| Extra PCIe overhead | ~4.2% |

For complete documentation of this issue, see
[`11_pcie_desc_page_size.md`](11_pcie_desc_page_size.md).

---

## Decision map — which cut to use for each model

```
New YOLO26-seg model for Hailo-8
    │
    ├─ Is it small (yolo26s)?
    │       │
    │       └─ cut_onnx_small.sh  (exposes 10 tensors: 3 scales × 3 types + proto)
    │          compile_hef.sh <model> 0.6 greedy
    │          → wait ~25 min → 4 contexts → HEF ~21MB ✓
    │
    └─ Is it nano (yolo26n)?
            │
            └─ cut_onnx_nano.sh  (exposes 4 tensors: bbox+score+coef+proto concat)
               compile_hef.sh <model> 0.9 greedy
               → wait ~13 min → 3 contexts → HEF ~9MB ✓
```

**General rule for other models:**
- If receiving `concat24 infeasible` → output tensor too large → divide more
- If receiving `matmul1 infeasible` → double-buffer conflict → reduce outputs
- If receiving `PrePostAgent infeasible` → proto too large → increase
  `max_utilization` (fewer contexts = different layout) or reduce resolution

---

## Lessons Learned — what to know before you start

| # | Lesson | Why it matters |
|---|---|---|
| 1 | Always export with **opset=17** | opset=12 breaks attention Reshape at 640×640 |
| 2 | **Never try to compile original ONNX** | top-k Tiles are not supported — absolute block |
| 3 | Small and nano need **different cuts** | Different internal architecture generates different errors |
| 4 | `matmul1 infeasible` on nano = **fewer outputs**, not more | More outputs worsen matmul1 double-buffering |
| 5 | `PrePostAgent infeasible` = **increase max_utilization** | Fewer contexts → different layout → proto buffer fits |
| 6 | **CUDA 12.3 mandatory** in container with host drivers >= 560 | CUDA 11.8 is incompatible with new drivers |
| 7 | **Do not import TF** before `ClientRunner.optimize()` | Fork inherits corrupted CUDA state → deadlock |
| 8 | **recover_har.sh** exists for a reason | If noise analysis hangs, weights are already saved — don't start from scratch |
| 9 | `strategy=greedy` resolves `PrePostAgent` on **small** | Different allocation algorithm finds viable layout |
| 10 | `max_utilization=0.9` resolves `PrePostAgent` on **nano** | Forces 3 contexts instead of 5 — less DMA fragmentation |
| 11 | **Nano is faster** (68 FPS) but detects **less** (~2% mask coverage) | For LKA with well-marked lane, it may be enough |
| 12 | **hw_only benchmark** is the reference to calculate NPU utilization | `NPU% = real_fps / hw_only_fps × 100 × 0.95` |
| 13 | On **AGL** kernel, always apply `force_desc_page_size=4096` | Kernel limits DMA to 4 KB; default HailoRT tries 16 KB → fails before inferring |

---

## References

### Hailo Hardware and Compiler

- **Hailo-8 Product Brief** — Official chip specifications (26 TOPS, power
  consumption, PCIe interface).
  → https://hailo.ai/product/hailo-8-ai-accelerator/

- **Hailo Dataflow Compiler (DFC) User Guide** — Complete compiler manual:
  HAR/HEF formats, contexts, compilation strategies, `.alls`.
  → Available on Hailo Developer Zone (login required):
  https://hailo.ai/developer-zone/

- **Hailo DFC Supported Operators** — List of supported ONNX operators (confirms
  `Tile`, `Gather`, `GatherElements` are not supported in HW).
  → Hailo Developer Zone → Documentation → Dataflow Compiler

- **HailoRT Driver Source** — `hailo_pci` driver source code, including
  `force_desc_page_size` parameter.
  → https://github.com/hailo-ai/hailort-drivers

- **Hailo Community — PCIe max_desc_page_size issue**
  → https://community.hailo.ai/t/pcie-max-desc-page-size-issue/136

- **Hailo Community — Agent infeasible and compilation strategies**
  → https://community.hailo.ai/

### YOLO26 / YOLOv10 Model

- **Wang et al., "YOLOv10: Real-Time End-to-End Object Detection"** — Original
  paper introducing NMS-free architecture with one2one heads. arXiv:2405.14458,
  2024.
  → https://arxiv.org/abs/2405.14458

- **Ultralytics YOLO Documentation** — Export documentation, opsets, supported
  formats.
  → https://docs.ultralytics.com/

### Quantization and Calibration

- **Jacob et al., "Quantization and Training of Neural Networks for Efficient
  Integer-Arithmetic-Only Inference"** — Reference paper for INT8 quantization
  with calibration by representative images. CVPR 2018.
  → https://arxiv.org/abs/1712.05877

- **CULane Dataset** — Real road lane dataset used for calibration. Pan et al.,
  "Spatial as Deep: Spatial CNN for Traffic Scene Understanding", AAAI 2018.
  → https://xingangpan.github.io/projects/CULane.html

### CUDA and Docker

- **NVIDIA CUDA Compatibility Matrix** — Compatibility table between host driver
  versions and CUDA runtimes in containers.
  → https://docs.nvidia.com/deploy/cuda-compatibility/index.html

- **NVIDIA Container Toolkit** — How Docker manages GPU access.
  → https://github.com/NVIDIA/nvidia-container-toolkit

- **Python Multiprocessing — Caveats with fork** — Official documentation on
  `fork` behavior and resource state inheritance (such as CUDA contexts).
  → https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods

### Linux Kernel and DMA

- **Linux DMA API How-To** — Official kernel documentation on DMA mapping,
  `dma_get_max_seg_size`, and contiguous segment restrictions.
  → https://www.kernel.org/doc/Documentation/DMA-API-HOWTO.txt

- **ONNX Opset Changelog** — Changes between opsets, including improvement in
  dynamic shape representation in opset 13+.
  → https://github.com/onnx/onnx/blob/main/docs/Changelog.md
