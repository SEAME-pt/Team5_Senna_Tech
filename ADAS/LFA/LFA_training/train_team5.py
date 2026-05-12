from ultralytics import YOLO


DATASET_YAML = "/home/team5/Documents/ADAS/LKA_model/datasets/dataset.yaml"
PROJECT      = "/home/team5/Documents/ADAS/LKA_model/runs"


model = YOLO("yolo26n-seg.pt")

model.train(
   # --- CORE CONFIGURATIONS ---
   data    = DATASET_YAML, # path to images and labels
   epochs  = 160,          # number of times the model sees the entire dataset
   batch   = 16,           # how many images it processes before updating weights
   imgsz   = 640,          # resizes all images to 640x640 pixels
   device  = 0,            # uses GPU 0 (the only one we have)
   project = PROJECT,      # directory where it saves the results
   name    = "yolov26nseg_cltusm_v", # (complet_model_name)_(dataset vl(vill10) cl(CULane) ca(CARLA) tu(TUlane) sm(seame))_v
   save    = True,         # saves the model weights during training
   plots   = True,         # generates plots with the training metrics
  
   # --- HARDWARE and TRAINING OPTIMIZATIONS ---
   workers = 4,            # accelerates image loading using the CPU (4 threads prevent RAM overload)
   amp     = True,         # automatic mixed precision: speeds up training and saves GPU VRAM
   patience = 25,          # stops training if accuracy doesn't improve for 15 consecutive epochs
   cos_lr  = True,         # smoothly adjusts the learning rate at the end of the training
   lr0          = 0.01,    # Initial learning rate
   lrf          = 0.001,   #Final learning rate
   overlap_mask = True,   # Allows segmentation masks to overlap during training
   mask_ratio   = 4,      # Downsample ratio for segmentation masks

   # --- AUGMENTATIONS (SPECIFIC FOR ADAS/LANE KEEPING) ---
   fliplr  = 0.0,          # ZERO probability of horizontal flip, lanes have sides (left is left, right is right)
   hsv_h   = 0.015,        # Slightly varies the color (hue), simulates different times of the day
   hsv_s   = 0.7,          # Greatly varies saturation, simulates cloudy vs. strong sun
   hsv_v   = 0.4,          # Varies brightness, simulates shadows and tunnels
   mosaic  = 0.7,          # Combines 4 images into one, artificially increases dataset variety
   close_mosaic = 10,      # Disables mosaic augmentation in the last 10 epochs for stability
   degrees = 5.0,          # Random rotation up to 5 degrees, simulates a slightly tilted camera
   translate = 0.1,        # Shifts the image up to 10%, simulates car vibrations/bumping (NEW)
   perspective = 0.0001,   # 3D perspective distortion, simulates the car pitching/tilting on the road
   shear       = 2.0,
)


print("Training completed!")
print(f"Best model saved at: {PROJECT}/--name_of_model--/weights/best.pt")


# ==========================================
# TRAINING NOTES & WORKFLOW
# ==========================================
# Augmentation is essential because the model never sees the exact same image twice,
# which drastically improves its ability to generalize in the real world.


# What happens under the hood during training:


# At each epoch, the model does this:
# For each batch of 16 images:
#    1. Forward pass  -> The model predicts lane masks.
#    2. Loss calc     -> Compares the prediction with the ground truth (real label).
#    3. Backward pass -> Calculates gradients (how wrong each weight is).
#    4. Optimizer     -> Adjusts the weights to reduce the error.


# At the end of each epoch:
#    - Evaluates performance on the validation set.
#    - Saves metrics (box_loss, seg_loss, cls_loss).
#    - If it's the best performance so far -> updates and saves 'best.pt'.

