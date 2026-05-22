# Lane Following Assistance (LFA) - Model Training

This repository contains the documentation and training configuration for a **Lane Following Assistance (LFA)** model based on the YOLO segmentation architecture. The goal of this project is to provide a robust lane detection system for autonomous driving tasks.

## 🚀 Model Overview

- **Base Model:** `yolo26n-seg.pt`
- **Task:** Instance Segmentation (Lane Marking Detection)
- **Framework:** [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)

The choice of a segmentation model allows the system to not only detect lanes but to precisely mask the drivable area and lane boundaries, which is critical for steering control logic.

## 📊 Dataset Composition

A massive effort was put into data preparation. We combined large-scale public datasets with proprietary data collected from the **SEA:ME** tracks. 

| Dataset Source | Image Count | Type | Status |
| :--- | :--- | :--- | :--- |
| **CULane** | 78,421 | Public | Checked & Converted |
| **Tusimple** | 3,626 | Public | Checked & Converted |
| **SEA:ME Track (2024/2025)** | 1,366 | Private | Custom Labeled |
| **SEA:ME Track (2025/2026)** | 380 | Private | Custom Labeled |
| **Total** | **83,793** | -- | -- |

> **Note:** All public datasets were manually verified and converted to match our model's specific label requirements, ensuring consistency across the training pipeline.

## ⚙️ Training Configuration

The model was trained using the following hyperparameters to ensure high generalization in real-world scenarios:

- **Epochs:** 160 (with Early Stopping)
- **Batch Size:** 16
- **Image Size:** 640x640 pixels
- **Optimization:** Automatic Mixed Precision (AMP) enabled for faster VRAM efficiency.
- **Learning Rate:** Initial lr_0 = 0.01 with a Cosine Scheduler (lr_f = 0.001).
- **Patience:** 25 epochs (stops training if no improvement is detected).

### Specific Augmentations for ADAS
Unlike standard object detection, lane keeping requires specific spatial logic. Our augmentation strategy reflects this:

- **`fliplr = 0.0` (Critical):** Horizontal flipping is disabled. In LFA, the spatial distinction between left and right lanes is vital, flipping could confuse the model regarding lane orientation.
- **`translate = 0.1`:** Simulates vehicle vibrations and bumping on uneven roads.
- **`perspective = 0.0001`:** Mimics the car pitching/tilting during acceleration or braking.
- **`hsv_h/s/v`:** Significant variations in saturation and value to simulate shadows, tunnels, and different sunlight intensities (cloudy vs. strong sun).
- **`mosaic = 0.7`:** Combines images to force the model to detect lanes in complex, crowded contexts.

## 🛠️ Training Workflow

The training process follows a standard deep learning pipeline optimized for performance:

1. **Forward Pass:** The model predicts lane masks.
2. **Loss Calculation:** A combination of `box_loss`, `seg_loss`, and `cls_loss` compares predictions against ground truth.
3. **Backward Pass:** Gradients are calculated to identify weight errors.
4. **Optimizer:** Weights are adjusted to minimize error.
5. **Validation:** At the end of each epoch, the model is tested against a validation set. The `best.pt` weight is updated only if performance improves.

## 📈 Results

The training results, including metrics and weights graphs, are saved in our directory so we can analyze them and see which parameters can be improved.

---
*Developed for ADAS applications - Team 5*
