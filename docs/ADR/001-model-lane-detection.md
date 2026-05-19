# [ADR-001] Selection of YOLO-v26n-seg for Lane Detection
Status: Accepted

Date: 03/03/2026

### 1. Context and Problem Statement
The autonomous driving prototype requires a robust, accurate, and real-time lane detection model capable of running on edge hardware (Raspberry Pi 5 paired with a Hailo NPU accelerator). The model must process incoming camera frames, output precise lane segmentations to compute the Cross-Track Error (CTE), and coexist efficiently alongside a separate object detection model on the same NPU without triggering hardware bottlenecks or unacceptable processing latencies.

### 2. Considered Options

Option A: YOLO-v26n-seg (YOLOv26 Nano Segmentation)

Option B: YOLO-v8n-seg / YOLO-v8s-seg (YOLOv8 Nano/Small Segmentation)

Option C: Ultra Fast Lane Detection (UFLD)

Option D: Reinforcement Learning (RL-based continuous control agent)

### 3. Decision Outcome
Chosen Option: **Option A (YOLO-v26n-seg)**, because it delivered the optimal balance between inference accuracy and deployment efficiency.

Most notably, evaluating the YOLOv26 architecture revealed that it drastically reduces post-processing latency on the host CPU. Unlike older versions, we do not have to implement or run a heavy Non-Maximum Suppression (NMS) layer in our custom Python decoder loop, making the lane pipeline significantly faster and preventing host-side CPU bottlenecks.

### 4.Pros and Cons of the Options
**Option A:** YOLO-v26n-seg
* Good: Eliminates NMS (Non-Maximum Suppression) overhead in Python post-processing, dramatically speeding up the mask-generation loop.

* Good: Compatibility with the Hailo-8 compiler toolchain.

* Good: Lightweight footprint (Nano variant) ideal for dual-model NPU deployment.

* Good: Fast training

**Option B:** YOLO-v8n-seg / YOLO-v8s-seg
* Good: Highly documented, mature ecosystem with plenty of pre-trained weights available for transfer learning.

* Bad: Requires handling explicit NMS bounding box/mask overlaps during post-processing, adding precious milliseconds to the host CPU cycle.

**Option C:** Ultra Fast Lane Detection (UFLD)
* Good: Extremely fast row-based classification anchor structure on vanilla GPU hardware.

* Bad: High conversion complexity. Adapting custom row-selection layers and multi-lane anchor structures to work natively with the Hailo SDK/HEF format presents an unacceptable architectural risk.

**Option D:** Reinforcement Learning (RL)
* Good: Potential for highly dynamic, end-to-end adaptive driving policies.

* Bad: Unacceptable development time. Training a stable RL agent from scratch or within a simulation environment exceeds our available schedule.

* Bad: High uncertainty regarding runtime behavior, hardware allocation, and software coexistence when sharing NPU memory with an independent object detection model.

### 5. Follow-up Tasks
None