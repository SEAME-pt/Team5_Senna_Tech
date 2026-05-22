# Object Detection Training Documentation — SEA:ME (SennaTech)

---

# Summary

1. [Introduction](#1-introduction)  
2. [Environment](#2-environment)  
3. [Datasets](#3-datasets)  
4. [Trained Models](#4-trained-models)  
5. [How to Train and Run Scripts](#5-how-to-train-and-run-scripts)  

---

# 1. Introduction

## Overview

This repository contains the complete training pipeline for the object detection system used by the SennaTech team on the SEA:ME 8 PC.

The project is based on the **Ultralytics YOLO framework** and supports:

- Training custom object detection models
- Fine-tuning pretrained YOLO models
- Advanced augmentations using Albumentations
- Dataset merging and organization
- Experiment tracking and model versioning

---

## Repository Structure

```bash
Object-Detection/
│
├── custom_train.py
├── train_objects.py
├── train_albumentations.py
├── test_model_prediction.py
│
├── datasets/
├── raw_models/
├── trained_models/
├── trainings/
├── test_videos/
│
├── runs/
├── venv/
└── __pycache__/
```

---

# 2. Environment

## Installation and Environment Setup

### 2.1 Activate Environment

```bash
source venv/bin/activate
```

---

### 2.2 Create Python Virtual Environment

Create the environment if it does not exist yet:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

### 2.3 Install Dependencies

```bash
pip install ultralytics opencv-python albumentations
```

---

## Dataset Structure

YOLO datasets must follow this structure:

```bash
dataset/
│
├── images/
│   ├── train/
│   └── val/
│
├── labels/
│   ├── train/
│   └── val/
│
└── data.yaml
```

---

## data.yaml Example

```yaml
path: /home/seame/ADAS/Object-Detection/datasets/full_dataset

train: images/train
val: images/val
```

---

# 3. Datasets

## datasets/

Contains all datasets used for training and experimentation.

```bash
datasets/
```

---

## Main Datasets

| Folder | Description |
|---|---|
| `50-sign` | Dataset containing only 50 km/h traffic signs |
| `80-sign` | Dataset containing only 80 km/h traffic signs |
| `50-80-signs-seame-lane` | Combined dataset with lane + speed signs |
| `KITTI-Dataset` | External dataset used for experimentation |
| `SEA:ME-2026_objects` | SEA:ME 2026 Dataset |
| `seame-lane-objects` | SEA:ME 2025 Dataset |
| `full_dataset` | All datasets merged |

---

## Dataset Merge Scripts

| Script | Purpose |
|---|---|
| `merge_all_datasets.py` | Merges all datasets into one |
| `merge_datasets.py` | Merges 2 specific datasets into one |

These scripts are used to consolidate multiple datasets into a unified training dataset.

---

# 4. Trained Models

## raw_models/

Contains original pretrained YOLO models downloaded from Ultralytics.

```bash
raw_models/
```

---

## Available Models

| Model | Description |
|---|---|
| `yolo26n.pt` | YOLO26 nano model |
| `yolov8n.pt` | YOLOv8 nano model |
| `yolov8s.pt` | YOLOv8 small model |

These models are used as the initial weights for transfer learning.

---

## trained_models/

Contains the best exported models from completed trainings.

```bash
trained_models/
```

---

## Available Models

| File | Description |
|---|---|
| `best.pt` | Current best global model |
| `yolov26n_sm.pt` | Base YOLO26 trained model |
| `yolov26n_sm_50_80_v1.pt` | Version 1 |
| `yolov26n_sm_50_80_v2.pt` | Version 2 |
| `yolov8n_sm_v1.pt` | YOLOv8 nano trained model |
| `yolov8s_sm_v1.pt` | YOLOv8 small trained model |

This folder stores only the final selected models.

---

## trainings/

Contains full training logs and experiment outputs.

```bash
trainings/
```

---

## Each Training Folder Contains

```bash
weights/
results.csv
results.png
confusion_matrix.png
F1_curve.png
PR_curve.png
```

---

## Training Folder Example

```bash
trainings/yolov26n_sm_50_80_v6/
```

---

## Contents

| File | Description |
|---|---|
| `weights/best.pt` | Best model during training |
| `weights/last.pt` | Last epoch checkpoint |
| `results.csv` | Metrics per epoch |
| `confusion_matrix.png` | Classification confusion matrix |
| `PR_curve.png` | Precision-Recall curve |
| `F1_curve.png` | F1 score curve |

---

## test_videos/

Contains videos used for inference testing.

```bash
test_videos/
```

---

## Available Test Videos

| File | Description |
|---|---|
| `pista01.avi` | Track test video |
| `pista02.avi` | Track test video |
| `pista_semaforo.avi` | Traffic light test |
| `test_object_detection.webm` | Generic detection test |
| `video_final_165502.avi` | Final run recording |
| `video_final_165718.avi` | Final run recording |

---

# 5. How to Train and Run Scripts

# 5.1 `test_model_prediction.py`

## Purpose

Runs inference using a trained YOLO model on:

- Images
- Videos
- Webcam streams

---

## Usage

### Image Prediction

```bash
python test_model_prediction.py \
--image image.jpg \
--model trained_models/best.pt
```

---

### Video Prediction

```bash
python test_model_prediction.py \
--video test_videos/pista01.avi \
--model trained_models/best.pt
```

---

### Webcam Prediction

```bash
python test_model_prediction.py \
--webcam /dev/video0 \
--model trained_models/best.pt
```

---

## Parameters

| Parameter | Description |
|---|---|
| `--image` | Path to input image |
| `--video` | Path to video |
| `--webcam` | Webcam device |
| `--model` | YOLO model path |
| `--conf` | Confidence threshold |

---

## Internal Functions

| Function | Description |
|---|---|
| `run_image()` | Runs inference on images |
| `run_video()` | Runs inference on videos |
| `run_webcam()` | Real-time webcam inference |

---

# 5.2 `custom_train.py`

## Purpose

Defines a custom YOLO trainer with advanced Albumentations augmentations.

The script extends:

```python
DetectionTrainer
```

from Ultralytics.

---

## Applied Augmentations

| Augmentation | Purpose |
|---|---|
| `MotionBlur` | Simulates vehicle movement |
| `GaussianBlur` | Simulates focus issues |
| `ImageCompression` | Simulates camera compression |
| `RandomBrightnessContrast` | Lighting variations |
| `RandomShadow` | Simulates road shadows |

---

## Why Albumentations?

Albumentations provides more realistic augmentations than native YOLO augmentations.

This improves:

- Generalization
- Robustness
- Real-world performance

---

# 5.3 `train_albumentations.py`

## Purpose

Trains a YOLO model using:

- `CustomTrainer`
- Albumentations
- Advanced hyperparameter tuning

---

## Training Workflow

```text
Dataset
   ↓
Augmentations
   ↓
Forward Pass
   ↓
Loss Calculation
   ↓
Backpropagation
   ↓
Optimizer Update
   ↓
Validation
   ↓
Save best.pt
```

---

## Core Training Parameters

| Parameter | Description |
|---|---|
| `data` | Dataset YAML |
| `epochs` | Number of training epochs |
| `batch` | Batch size |
| `imgsz` | Image resolution |
| `device` | GPU device |
| `project` | Output directory |
| `name` | Training name |

---

## Optimization Parameters

| Parameter | Description |
|---|---|
| `optimizer="AdamW"` | Weight optimization algorithm |
| `lr0` | Initial learning rate |
| `lrf` | Final learning rate |
| `weight_decay` | Reduces overfitting |
| `warmup_epochs` | Gradual LR warmup |
| `cos_lr=True` | Cosine LR scheduler |
| `amp=True` | Mixed precision training |
| `patience` | Early stopping |

---

## Loss Parameters

| Parameter | Description |
|---|---|
| `box` | Bounding box loss weight |
| `cls` | Classification loss weight |
| `dfl` | Distribution focal loss |

---

## Augmentation Parameters

| Parameter | Description |
|---|---|
| `fliplr` | Horizontal flip |
| `flipud` | Vertical flip |
| `hsv_h` | Hue variation |
| `hsv_s` | Saturation variation |
| `hsv_v` | Brightness variation |
| `mosaic` | Mosaic augmentation |
| `degrees` | Random rotation |
| `translate` | Random translation |
| `perspective` | Perspective distortion |
| `shear` | Shear transformation |
| `scale` | Random zoom |
| `copy_paste` | Object copy-paste |
| `mixup` | Image blending |
| `erasing` | Random occlusion |

---

## Example Training Command

```bash
python train_albumentations.py
```

---

# 5.4 `train_objects.py`

## Purpose

Standard YOLO training script without custom Albumentations trainer.

Used for:

- Baseline experiments
- Faster training
- Simpler debugging

---

## Main Difference

| Script | Description |
|---|---|
| `train_objects.py` | Native YOLO augmentations |
| `train_albumentations.py` | YOLO + Albumentations |

---

## Training Lifecycle

During each epoch:

```text
1. Forward Pass
2. Loss Calculation
3. Backpropagation
4. Weight Update
5. Validation
6. Metrics Logging
```

---

## Output Files

After training:

```bash
trainings/model_name/
```

You will find:

```bash
weights/best.pt
weights/last.pt
results.png
PR_curve.png
confusion_matrix.png
```

---

## Recommended Training Strategy

### Small Dataset

```python
epochs = 50
batch = 16
imgsz = 640
```

---

### Medium Dataset

```python
epochs = 80
batch = 16
imgsz = 640
```

---

### Large Dataset

```python
epochs = 100+
batch = 32
imgsz = 1280
```

---

## GPU Recommendations

| GPU | Recommended Batch |
|---|---|
| RTX 3050 | 8 |
| RTX 3060 | 16 |
| RTX 4070 | 32 |
| Jetson Orin | 4–8 |

---

## Best Practices

### 1. Always Start from Pretrained Models

Example:

```python
YOLO("yolov8n.pt")
```

Transfer learning drastically improves convergence speed.

---

### 2. Use Strong Augmentations

Especially for autonomous driving scenarios:

- Motion blur
- Shadows
- Brightness changes
- Perspective distortions

---

### 3. Monitor Overfitting

Watch:

- Validation loss
- mAP
- Precision
- Recall

---

### 4. Keep Dataset Balanced

Avoid excessive class imbalance.

---

## Model Evaluation Metrics

| Metric | Meaning |
|---|---|
| `Precision` | Correct positive predictions |
| `Recall` | Detection coverage |
| `mAP50` | Detection quality at IoU 0.5 |
| `mAP50-95` | General detection performance |
| `F1-score` | Precision/Recall balance |

---

## Inference Example

```python
from ultralytics import YOLO

model = YOLO("trained_models/best.pt")

results = model.predict("image.jpg")

results[0].show()
```

---

## Real-Time Webcam Example

```bash
python test_model_prediction.py \
--webcam /dev/video0 \
--model trained_models/best.pt
```

Press:

```text
q
```

to exit.

---

## Recommended Workflow

```text
1. Prepare dataset
2. Merge datasets
3. Configure data.yaml
4. Select base model
5. Train model
6. Evaluate metrics
7. Export best.pt
8. Test inference
9. Deploy to ADAS system
```

---

# Final Notes

This repository was designed for:

- Autonomous driving research
- Traffic sign detection
- Lane object detection
- Real-time embedded AI systems

The combination of:

- YOLO
- Transfer Learning
- Albumentations
- Dataset merging
- Advanced augmentation

provides a robust object detection pipeline optimized for the SEA:ME autonomous driving platform.