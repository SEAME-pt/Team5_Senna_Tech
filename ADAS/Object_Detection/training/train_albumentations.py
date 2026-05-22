from ultralytics import YOLO
from custom_train import CustomTrainer


model = YOLO("/home/seame/ADAS/Object-Detection/trainings/yolov26n_sm_50_80_v5/weights/best.pt")
DATASET_YAML = "/home/seame/ADAS/Object-Detection/datasets/full_dataset/data.yaml"
PROJECT      = "/home/seame/ADAS/Object-Detection/trainings"

model.train(
   trainer = CustomTrainer,

   # --- CORE CONFIGURATIONS ---
   data    = DATASET_YAML,      # path to images and labels
   epochs  = 35,             # number of times the model sees the entire dataset
   batch   = 16,                # how many images it processes before updating weights
   imgsz   = 640,              # resizes all images to 1280x1280 pixels
   device  = 0,                 # uses GPU 0 (the only one we have)
   project = PROJECT,           # directory where it saves the results
   name    = "yolov26n_sm_50_80_v6", # (complet_model_name)_(dataset)_v(version)
   save    = True,              # saves the model weights during training
   plots   = True,              # generates plots with the training metrics

   # --- HARDWARE and TRAINING OPTIMIZATIONS ---
   workers = 4,              # accelerates image loading using the CPU (4 threads prevent RAM overload)
   amp     = True,           # automatic mixed precision: speeds up training and saves GPU VRAM
   patience = 20,            # stops training if accuracy doesn't improve for 50 consecutive epochs
   cos_lr  = True,           # smoothly adjusts the learning rate at the end of the training
   lr0          = 0.0005,     # Initial learning rate
   lrf          = 0.01,      # Final learning rate
   optimizer    = "AdamW",   # AdamW optimizer is often better for medium-sized datasets and can lead to faster convergence compared to SGD.
   weight_decay   = 0.0005,  # Penalizes large weights to reduce overfitting
   warmup_epochs  = 5.0,     # Gradually increases the learning rate during the first 5 epochs to stabilize training
   label_smoothing = 0.05,    # Smooths the labels, reduces overconfidence and helps with similar classes (e.g., sign_50 vs sign_80)

    # --- LOSS WEIGHTS ---
    # Control how much each component of the loss contributes to the total loss.
    box       = 7.5,    # Loss weight for bounding box regression (localization)
    cls       = 1.2,    # Loss weight for classification (object class prediction)
    dfl       = 1.5,    # Loss weight for distribution focal loss (refines bounding box predictions)

   # --- AUGMENTATIONS ---
   fliplr  = 0.2,          # Probability of horizontal flip, lanes have sides (left is left, right is right)
   flipud  = 0.0,          # No vertical flip, it would create unrealistic scenarios (upside down roads)
   hsv_h   = 0.015,        # Slightly varies the color (hue), simulates different times of the day
   hsv_s   = 0.7,          # Greatly varies saturation, simulates cloudy vs. strong sun
   hsv_v   = 0.4,          # Varies brightness, simulates shadows and tunnels
   mosaic  = 0.3,          # Combines 4 images into one, artificially increases dataset variety
   close_mosaic = 15,      # Disables mosaic augmentation in the last 10 epochs for stability
   degrees = 3.5,          # Random rotation up to 3.5 degrees, simulates a slightly tilted camera
   translate = 0.1,        # Shifts the image up to 10%, simulates car vibrations/bumping (NEW)
   perspective = 0.0001,   # 3D perspective distortion, simulates the car pitching/tilting on the road
   shear       = 2.0,      # Shear transformation, simulates the effect of the car leaning during turns
   scale       = 0.2,      # Randomly zooms in/out up to 50%, simulates different distances to the lane markings
   copy_paste   = 0.0,     # Copies and pastes objects within the image, simulates occlusions (e.g., other cars blocking the lane)
   mixup        = 0.05,    # Blends two images together, simulates complex scenarios with multiple lanes and vehicles
   erasing       = 0.4,    # Randomly erases parts of the image, simulates dirt on the camera lens or occlusions
   multi_scale   = False,   # Randomly scales the image by these factors, simulates different distances and zoom levels
   save_period   = 10,     # Saves a checkpoint every 10 epochs, allows us to review intermediate models and metrics
   seed        = 42,       # Ensures reproducibility of the training process (same random augmentations each time)
)


print("Training completed!")
print(f"Best model saved at: {PROJECT}/--name_of_model--/weights/best.pt")
