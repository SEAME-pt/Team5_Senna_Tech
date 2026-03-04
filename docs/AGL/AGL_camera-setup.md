# Setting up rpi-libcamera on Raspberry Pi 5 with AGL

## Table of Contents

1. [Problem Overview](#problem-overview)  
2. [Solution: Using the rpi-libcamera Fork](#solution-using-the-rpi-libcamera-fork)  
3. [Implementation Structure](#implementation-structure)  
   1. [Install rpi-libcamera and Dependencies](#install-rpi-libcamera-and-dependencies)  
   2. [Verify Installation Files](#verify-installation-files)  
   3. [Test the Camera](#test-the-camera)   
5. [References](#References)  

---

## Problem Overview

Automotive Grade Linux (AGL) **does not include Raspberry Pi 5 proprietary pipelines** by default, such as `libpisp`.  

Without these pipelines:

- The sensor and ISP (Image Signal Processor) pipeline is missing  
- IPAs (Image Processing Algorithms) like are unavailable  
- Applications like OpenCV or any V4L2-based software cannot access `/dev/video*`  

As a result, standard libcamera on AGL **cannot capture frames from Raspberry Pi cameras**.

---

## Solution: Using the rpi-libcamera Fork

The **rpi-libcamera fork** provides:

- Raspberry Pi-specific pipelines (rpi/pisp)  
- Precompiled IPAs for official sensors (IMX219, IMX708, IMX477, etc.)  

By installing `rpi-libcamera` along with its dependencies, AGL can fully support Raspberry Pi cameras.

---

## Implementation Structure

The implementation consists of three main components:

1. **rpi-camera Recipe (recipes-multimedia/rpi-libcamera/rpi-libcamera_0.5.2bb)**  
   - Tracks the Raspberry Pi fork of libcamera  
   - Ensures that using RPi Linux requires `rpi-libcamera`  
   - Sets `rpi-libcamera` as the preferred provider in AGL builds  

2. **libpisp Recipe (recipes-multimedia/rpi-libcamera/libpisp_1.3.0.bb)**  
   - Provides the **PISP pipeline handler** for Raspberry Pi5 
   - Includes prebuilt IPAs for official cameras  

3. **rpicam-apps Recipe (recipes-multimedia/rpicam-apps/rpicam-apps_1.9.1.bb)**  
   - Replaces standard `libcamera-apps` in the Yocto build for Raspberry Pi  
   - Utilities provided:
     - `rpicam-hello` – camera detection and info  
     - `rpicam-jpeg` – capture JPEG images  
     - `rpicam-still` – capture raw stills  
     - `rpicam-vid` – record video  

**Additional Notes on Implementation:**

- Dynamic layers were cleaned:
  - `libcamera-apps` removed from `dynamic-layers`  
  - `libcamera_%.bbappend` removed  
- Preferred provider for `libcamera` is explicitly set to `rpi-libcamera` in `conf/local.conf`  


---



### Install rpi-libcamera and Dependencies into yout build

In the AGL environment:

Add the following recipes to your build in `conf/local.conf`:  
   - `rpi-camera`  
   - `libpisp`  
   - `rpicam-apps` 

### Verify Installation Files after new AGL image builded

Confirm that:

- `rpi-libcamera` contains the `rpi/pisp` pipeline and IPAs  
- `libpisp` provides the PISP library for Raspberry Pi sensors  
- `rpicam-apps` provides the camera utilities and assets  

---

### Test the Camera

List available cameras:

```bash
rpicam-hello --list-cameras

Example output:

0 : imx708_wide_noir [4608x2592 10-bit RGGB]
    Modes: 'SRGGB10_CSI2P' : 1536x864 [120.13 fps]
                             2304x1296 [56.03 fps]
                             4608x2592 [14.35 fps]
```

                            

Confirms that the pipeline is loaded and the camera is detected



#### Capture a Frame

Use rpicam-still to capture a single frame:

```
rpicam-still -o capture.jpg
```

-o capture.jpg → save captured image to capture.jpg

**This works with the RPi pipeline and IPAs enabled by rpi-libcamera**


## References

- Raspberry Pi libcamera fork and PISP pipeline discussion: [meta-raspberrypi PR #1517](https://github.com/agherzan/meta-raspberrypi/pull/1517)  