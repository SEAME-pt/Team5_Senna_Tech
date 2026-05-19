# [ADR-002] Selection of YOLOv26n for Object Detection
Status: Accepted

Date: 03/04/2026

### 1. Context and Problem Statement
The model must detect multiple object classes (such as cars, obstacles, traffic lights, and traffic signs).

Because this model runs concurrently with the lane detection model on the Hailo NPU, it must have a small footprint, fast training convergence, and superior inference performance to ensure the host CPU loop latency remains low.

### 2. Considered Options
Option A: YOLOv26n

Option B: YOLOv8n

### 3. Decision Outcome
Chosen Option: **Option A (YOLOv26n)**, because empirical testing demonstrated both a faster training convergence rate and significantly better precision/recall metrics on our custom dataset compared to YOLOv8n.

### 4.Pros and Cons of the Options
**Option A:** YOLO-v26n-seg
* Good: Faster Training: Reached optimal validation loss and mAP convergence in fewer epochs, saving critical GPU compute time during our development iterations.

* Good: Superior Detection Results: Better bounding box precision, especially on critical classes like traffic signs and lights where early detection (smaller bounding box areas) is required by our FSM thresholds.

* Good: Streamlines hardware deployment by matching the core architecture of our lane segmentation model.

* Bad: Slightly newer codebase, meaning fewer open-source community benchmarks are available compared to older legacy versions.

**Option B:** YOLO-v8n-seg / YOLO-v8s-seg
* Good: Highly stable, mature ecosystem with widely available pre-trained weights for transfer learning.

* Bad: Exhibited lower overall mAP scores on our custom dataset during comparative testing.

* Bad: Slower training convergence, requiring more epochs to achieve stable weights, which introduces an efficiency penalty given our strict timeline.

### 5. Follow-up Tasks
None