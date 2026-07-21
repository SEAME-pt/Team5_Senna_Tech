# Installation & Run Guide — PiRacer Autonomous Vehicle

This guide explains how to install and run the **complete Team5 SennaTech system** on a brand‑new car built from the same components as the original prototype. It goes from hardware assembly, through flashing the STM32 firmware and the Raspberry Pi, to launching the autonomous driving pipeline.

---

## Table of Contents

- [System Overview](#system-overview)
- [Bill of Materials](#bill-of-materials)
- [Hardware Assembly](#hardware-assembly)
- [Part A — STM32 Firmware (ThreadX RTOS)](#part-a--stm32-firmware-threadx-rtos)
- [Part B — Raspberry Pi 5: AGL OS & Boot](#part-b--raspberry-pi-5-agl-os--boot)
- [Part C — Hailo‑8, Camera & CAN on the Raspberry Pi](#part-c--hailo8-camera--can-on-the-raspberry-pi)
- [Part D — Cross‑Compiling the Qt Cluster & Gamepad Control (Docker)](#part-d--cross-compiling-the-qt-cluster--gamepad-control-docker)
- [Part E — ADAS Pipeline (Python on the Raspberry Pi)](#part-e--adas-pipeline-python-on-the-raspberry-pi)
- [Part F — Kuksa Middleware (VSS / Databroker)](#part-f--kuksa-middleware-vss--databroker)
- [Part G — Deploying Everything to the Car](#part-g--deploying-everything-to-the-car)
- [Part H — Running the System](#part-h--running-the-system)
- [CAN Signal Reference](#can-signal-reference)
- [File Layout on the Raspberry Pi](#file-layout-on-the-raspberry-pi)
- [Troubleshooting](#troubleshooting)
- [Quick‑Start Checklist](#quick-start-checklist)

---

## System Overview

The PiRacer is an autonomous 1/10‑scale vehicle built around **two compute nodes** that talk over a **CAN bus**:

```
        ┌──────────────────────────────────────────────────────────┐
        │                  Raspberry Pi 5 (AGL)                    │
        │                                                          │
        │  ADAS Pipeline (Python + Hailo‑8 NPU)                    │
        │    camera → lane seg + object det → FSM → PID → CAN      │
        │                                                          │
        │  Gamepad Control (C++)   →  manual override via CAN      │
        │  Qt Instrument Cluster   ←  KUKSA Databroker ← CAN       │
        │  KUKSA Databroker + CAN Provider                         │
        └───────────────▲───────────────────────────▲──────────────┘
                        │ CAN (can0, 500 kbps)      │
        ┌───────────────┴───────────────────────────┴───────────────┐
        │                  STM32U585 (ThreadX)                      │
        │  Reads: speed sensor, battery (INA219), ultrasonic,       │
        │         ambient light, OLED display                       │
        │  Drives: DC motors (PCA9685 0x40), steering servo         │
        │         				                                    │
        │  CAN controller: MCP2515 (SPI1)                           │
        └───────────────────────────────────────────────────────────┘
```

- The **STM32** is the real‑time node: it reads sensors, drives the motors/servo, and reports vehicle data on CAN.
- The **Raspberry Pi 5** is the brain: it runs the AI pipeline (Hailo‑8), the Qt dashboard, the KUKSA middleware, and the gamepad remote control. It sends drive commands (throttle + steering) to the STM32 over CAN.
- The **Hailo‑8** runs two YOLO models compiled to `.hef`: one for lane segmentation, one for object/traffic‑sign detection.
- The **gamepad** can override autonomy at any time (moving the stick instantly switches to MANUAL mode).

---

## Bill of Materials

### Compute & AI

| Component | Notes |
|---|---|
| Raspberry Pi 5 | 8 GB recommended. Booted from NVMe SSD (M.2 HAT+) — see [Part B](#part-b--raspberry-pi-5-agl-os--boot) |
| Hailo‑8 AI Hat | PCIe accelerator for the two YOLO `.hef` models |
| STM32U585 dev board | B‑U585I‑IOT02A (runs ThreadX RTOS) |
| MicroSD / NVMe SSD | OS for the Raspberry Pi (AGL )|

### PiRacer chassis (Waveshare kit)

| Component | Qty |
|---|---|
| Metal chassis | 1 |
| DC gear motors | 2 |
| Rear wheels + couplers | 2 |
| Front wheels + steering knuckles | 2 |
| Servo motor (MG996R) | 1 ( Or more, you will burn some :3 )|
| Expansion board (HAT) with PCA9685 ×2 | 1 |
| Camera module 3 (Wide NoIR, IMX708) + acrylic mount | 1 |
| 18650 battery pack + holder | 1 |

### Sensors, display & comms

| Component | I²C / bus address | Notes |
|---|---|---|
| PCA9685 (steering servo) | `0x40` | PWM @ 50 Hz |
| PCA9685 (DC motors) | `0x60` | PWM @ 50 Hz |
| ADS1115 / INA219 (battery monitor) | `0x48` | Voltage / current / SoC |
| SSD1306 OLED display | `0x3C` | Status display (honestly, just for the shinny eyes... worth it.)|
| LM393 speed sensor | GPIO (PB0 EXTI) | Wheel pulse counter |
| MCP2515 CAN controller (STM32 side) | SPI1 | CAN bridge to the Raspberry Pi |
| Rear display | 1280×400 | Qt instrument cluster |
| ShanWan USB gamepad | — | Manual driving + mode switch |

### Tools / host software

- A Linux host (x86_64, Ubuntu 22.04+) for **Docker cross‑compilation** and **AGL builds**.
- ST‑Link v2/v3 programmer + USB cable for the STM32.
- An SSH connection to the Raspberry Pi (once AGL is running).

---

## Hardware Assembly

### 1. PiRacer chassis

Follow the [PiRacer Assembly Manual by Waveshare](https://www.waveshare.com/wiki/PiRacer_Assembly_Manual) and the condensed guide in [`docs/piracer/piracer_assembly_guide.md`](docs/piracer/piracer_assembly_guide.md). In short:

1. Mount the 2 DC motors to the chassis (M3×6).
2. Attach couplers + rear wheels (M4×8).
3. Install the servo on its bracket and connect the short/long linkage bars to the steering knuckles.
4. Mount the front wheels with locknuts (they must spin freely).
5. Add EVA vibration pads and standoffs.
6. Wire motors + servo to the **Expansion Board (HAT)** respecting polarity:
   - Brown → GND, Red → 5V, Yellow → Signal.
7. Place the HAT on M3×26 standoffs.
8. Mount the Raspberry Pi on top of the HAT and connect the 6‑pin Pi↔HAT cable (enables I²C).

> The HAT's PCA9685 chips are controlled over I²C (`0x40` servo, `0x60` motors). See [`docs/piracer/piracer-cpp.md`](docs/piracer/piracer-cpp.md) for the PWM/I²C theory.

### 2. STM32 ↔ Expansion Board wiring

The STM32 replaces the Raspberry Pi as the **motor/sensor controller**. Wire it to the Expansion Board as described in [`docs/hardware/stm32_motor_wiring.md`](docs/hardware/stm32_motor_wiring.md):

| STM32 pin | Function | Goes to |
|---|---|---|
| 3.3V + GND | Logic power | HAT 3.3V / GND (common ground is mandatory) |
| PB8 (SCL) / PB9 (SDA) | I²C1 | HAT SCL / SDA |
| PE13/PE14/PE15 (SPI1) | MCP2515 CAN controller | CAN module SCK/MISO/MOSI |
| PB0 (EXTI0, falling edge) | LM393 speed sensor | Wheel pulse output |

> **Power:** the STM32 must supply the board's 3.3 V logic (~37 mA total bus load — well within the regulator's capacity). The battery pack still powers the motors through the HAT.

### 3. Camera, Hailo & display

- Connect the **Raspberry Pi Camera Module 3** to the Pi's CSI port (flex cable, contacts toward the board).
- Fit the **Hailo‑8 AI Hat** onto the Pi 5 GPIO header and connect its PCIe ribbon to the Pi's PCIe lane.
- Connect the **rear 1280×400 display** over HDMI.

---

## Part A — STM32 Firmware (ThreadX RTOS)

The STM32 runs the `SennaTech` firmware (ThreadX RTOS): motor/servo PWM, speed sensor, battery, OLED, ultrasonic, parking modes, and CAN. Source lives in [`src/threadx/SennaTech/`](src/threadx/SennaTech/).

### A.1 Install the host toolchain (Linux)

```bash
sudo apt update
sudo apt install -y cmake build-essential \
    gcc-arm-none-eabi libnewlib-arm-none-eabi \
    libstdc++-arm-none-eabi-newlib

# ST‑Link tools (build from source if the apt version is < 1.8 — see troubleshooting)
sudo apt install -y stlink-tools
```

> If `st-flash` is too old ("Unknown chip id 0x482"), build stlink ≥ 1.8 from source as described in [`docs/ThreadX/st-link_compile-flash_threadX.md`](docs/ThreadX/st-link_compile-flash_threadX.md).

### A.2 Build & flash

Connect the ST‑Link to the STM32 board and run the helper script from the project root:

```bash
cd src/threadx/SennaTech
chmod +x compile_flash.sh

# First time: full clean build + flash
./compile_flash.sh slow

# Later: incremental build + flash
./compile_flash.sh fast
```

The script will:
1. Configure CMake with `cmake/gcc-arm-none-eabi.cmake` (Cortex‑M33, hard float).
2. Compile the `SennaTech.elf` executable with `make`.
3. Convert it to `SennaTech.bin` with `arm-none-eabi-objcopy`.
4. Erase flash and write the binary to `0x08000000` via `st-flash`.

### A.3 Verify

- The OLED on the front should light up (cute eyes / sleeping eyes animations).
- UART debug output is available on **USART1 @ 115200 8N1**:

```bash
screen /dev/ttyACM0 115200
# (Ctrl+A then K to exit)
```

At this point the STM32 listens on CAN for drive commands (IDs `0x001`/`0x002`) and publishes sensor data (speed, battery, temperature).

---

## Part B — Raspberry Pi 5: AGL OS & Boot

The Raspberry Pi 5 runs **Automotive Grade Linux (AGL)**. Building AGL is done on the **Linux host** (not the Pi). Full instructions: [`docs/AGL/AGL_install.md`](docs/AGL/AGL_install.md).

### B.1 Host prerequisites (needs ~90 GB free disk)

```bash
sudo apt-get install build-essential chrpath cpio debianutils diffstat file gawk gcc git \
    iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 \
    python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xz-utils zstd

export AGL_TOP=$HOME/AGL
echo 'export AGL_TOP=$HOME/AGL' >> $HOME/.bashrc
mkdir -p $AGL_TOP

# repo tool
mkdir -p $HOME/bin
export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> $HOME/.bashrc
curl https://storage.googleapis.com/git-repo-downloads/repo > $HOME/bin/repo
chmod a+x $HOME/bin/repo
```

### B.2 Download AGL (stable "trout" release)

```bash
cd $AGL_TOP
mkdir trout && cd trout
repo init -b trout -u https://gerrit.automotivelinux.org/gerrit/AGL/AGL-repo
repo sync
```

### B.3 Integrate Hailo + camera + custom layers

Before building, add the project‑specific meta‑layers so the image ships with the Hailo runtime, the rpi‑libcamera fork, and the cluster/services. Follow:

- **Hailo:** [`docs/AGL/AGL_meta-hailo.md`](docs/AGL/AGL_meta-hailo.md)
  - Clone `https://github.com/hailo-ai/meta-hailo.git`, checkout `hailo8-scarthgap`.
  - Add to `conf/local.conf`:
    ```
    IMAGE_INSTALL:append = " libhailort hailortcli hailo-pci pyhailort libgsthailo hailo-firmware"
    ```
  - Add the `linux-raspberrypi_%.bbappend` with `KERNEL_SPLIT_MODULES = "0"` to avoid the hailo‑pci version mismatch.
- **Camera:** [`docs/AGL/AGL_camera-setup.md`](docs/AGL/AGL_camera-setup.md) — install `rpi-libcamera`, `libpisp`, `rpicam-apps`.
- **Custom services & cluster:** [`docs/AGL/AGL_meta-customs.md`](docs/AGL/AGL_meta-customs.md) — add the `meta-services` and `meta-clusterqt` layers to `bblayers.conf`.

### B.4 Build & flash

```bash
source meta-agl/scripts/aglsetup.sh -f -m raspberrypi5 -b raspberrypi5 agl-all-features agl-devel
bitbake agl-image-minimal-crosssdk
```

Flash the resulting `.wic.xz` to a microSD (then clone it to NVMe):

```bash
lsblk
sudo umount /dev/sdX
xzcat tmp/deploy/images/raspberrypi5/agl-image-minimal-crosssdk-raspberrypi5.rootfs.wic.xz \
    | sudo dd of=/dev/sdX bs=4M
sync
```

### B.5 Boot from NVMe (recommended)

Boot once from the microSD, then use **Menu → Accessories → SD Card Copier** to clone the OS to the NVMe SSD, and set the boot order in `sudo raspi-config` → *Advanced Options → Boot Order → NVMe/USB Boot*. Reboot and remove the microSD. See [`docs/raspberry-pi-5/raspberry_Pi_system.md`](docs/raspberry-pi-5/raspberry_Pi_system.md).

### B.6 First boot: Wi‑Fi + SSH

```bash
rfkill unblock all
ip link set up wlan0
connmanctl
# inside connmanctl:
#   scan wifi
#   services
#   agent on
#   connect <network_name>
```

Find the Pi's IP with `ip addr show` and SSH in.

---

## Part C — Hailo‑8, Camera & CAN on the Raspberry Pi

These steps run **on the Raspberry Pi 5** after AGL is booted.

### C.1 Hailo PCIe descriptor fix (mandatory on AGL)

AGL's kernel limits DMA descriptor pages to 4096 bytes, but HailoRT defaults to 16384. Without the fix, inference fails with `CHECK failed - max_desc_page_size`. Apply the permanent fix ([`docs/AGL/AGL_hailo_PCIe_config.md`](docs/AGL/AGL_hailo_PCIe_config.md)):

```bash
echo 'options hailo_pci force_desc_page_size=4096' | sudo tee /etc/modprobe.d/hailo_pci.conf
sudo reboot
```

After reboot, verify the device and run a benchmark:

```bash
hailortcli scan
hailortcli benchmark /home/models/yolo26n_v6.hef   # expect ~380 FPS streaming
```

### C.2 Camera

With `rpicam-apps` installed (from the AGL image), confirm the camera is detected:

```bash
rpicam-hello --list-cameras
# 0 : imx708_wide_noir [4608x2592 10-bit RGGB] ...

rpicam-still -o /tmp/test.jpg   # capture a frame
```

The ADAS pipeline uses `rpicam-vid` streaming YUV420 over a pipe (see `ADAS/pipeline/camera/`).

### C.3 CAN interface (`can0`)

The CAN bus between the Pi and the STM32 (via MCP2515) shows up as `can0`. Bring it up at **500 kbps**:

```bash
sudo ip link set can0 up type can bitrate 500000
```

Verify traffic (with the STM32 powered and sending sensor frames):

```bash
ip -s link show can0
# or, if can-utils is installed:
candump can0
```

Make it persistent across reboots (e.g. a systemd unit or `rc.local`). For **bench testing without a physical CAN bus**, you can use a virtual CAN:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

> The Kuksa `docker-compose.yml` defaults to `vcan0`; switch it to `can0` for the real car (see [Part F](#part-f--kuksa-middleware-vss--databroker)).

---

## Part D — Cross‑Compiling the Qt Cluster & Gamepad Control (Docker)

The **Qt instrument cluster** (`src/car_cluster/`) and the **gamepad manual control** (`src/car-control/joystick-can/`) are C++ programs cross‑compiled for ARM64 (AGL) on an x86_64 host using Docker. The Dockerfile builds Qt 6.7.3 twice (host tools + ARM64 libs), the AGL SDK, gRPC/protobuf, then both projects.

Full explanation: [`docker/README.md`](docker/README.md).

### D.1 Build the Docker image (on the host)

```bash
cd /path/to/Team5_Senna_Tech
docker build -t agl-sdk-container -f docker/Dockerfile .
```

> This is a long build (Qt from source + AGL SDK + gRPC). Expect several hours and ~50 GB.

### D.2 Extract the binaries

```bash
docker run --rm -v "$PWD/out:/out" agl-sdk-container bash -c \
    "cp /root/outputs/appcar_cluster /root/outputs/gamepad_control /out/"
```

You now have two ARM64 binaries:

| Binary | Source | Purpose |
|---|---|---|
| `appcar_cluster` | `src/car_cluster/` | Qt/QML instrument cluster on the rear display |
| `gamepad_control` | `src/car-control/joystick-can/` | Reads the ShanWan gamepad → CAN drive commands + mode switching |

### D.3 (Alternative) Release via OTA

Pushing a tag `clusterqt-v*` triggers the GitHub Actions release workflow that builds and publishes the cluster binary. See [`docs/OTA/InstrumentCluster.md`](docs/OTA/InstrumentCluster.md).

---

## Part E — ADAS Pipeline (Python on the Raspberry Pi)

The autonomous driving pipeline is in [`ADAS/pipeline/`](ADAS/pipeline/) (standard Lane Following Assist) and [`ADAS/Taxi_Robot/`](ADAS/Taxi_Robot/) (Robotaxi variant). It runs **on the Raspberry Pi 5** and uses the Hailo‑8 NPU.

### E.1 Python dependencies

On the Raspberry Pi, install the pipeline's Python dependencies:

```bash
sudo pip install python-can numpy opencv-python
# Hailo Python bindings (pyhailort) — already installed via the AGL image,
# otherwise install from the Hailo Software Suite.
```

> The pipeline imports `can` (python‑can), `numpy`, `cv2` (OpenCV), and `hailo_platform` (HailoRT). The display uses GStreamer (`waylandsink` for local, JPEG for remote).

### E.2 Hailo models (`.hef`)

Two compiled Hailo models are required:

| Model file | Role | Source |
|---|---|---|
| `yolo26n_seg_640.hef` | Lane segmentation (LFA/LKA) | Convert with [`ADAS/convert_hailo/`](ADAS/convert_hailo/) BYOM flow |
| `yolo26n_v6.hef` | Object / traffic‑sign detection (13 classes) | Convert with the Model Zoo or BYOM flow |

If you don't have pre‑compiled `.hef` files, generate them from the trained `.pt` models:

```bash
# On a host with the Hailo Software Suite Docker image:
cd ADAS/convert_hailo
cp .env.hailo.example .env.hailo
# edit .env.hailo: BASE_PROJECT, VENV_NAME, SHARED_DIR, CONTAINER_NAME, DOCKER_IMAGE_NAME, RUNS_BASE, RPI5_HOST

# YOLOv8-seg (Model Zoo flow)
./convert_flow/run_convert.sh

# YOLO26-seg (BYOM flow)
cd yolo26_seg/scripts/conversion
bash pipeline.sh yolov26nseg_cltusm_v yolo26n_seg_640 640 gpu 3outputs
```

See [`ADAS/convert_hailo/README.md`](ADAS/convert_hailo/README.md) and `ADAS/LFA/LKA_trained_models/` for the trained checkpoints. Place the final `.hef` files in `/home/models/` on the Pi (see [Part G](#part-g--deploying-everything-to-the-car)).

### E.3 Pipeline options (important)

`ADAS/pipeline/main.py` accepts:

```
python3 main.py <lane.hef> <object.hef> [options]
  --remote       Stream JPEG frames to stdout (over SSH)
  --no-display   Headless (no rendering, saves CPU)
  --virtual      Compute throttle/steering but DON'T send CAN (safe bench test)
```

Always test with `--virtual --no-display` first when bringing up a new car.

---

## Part F — Kuksa Middleware (VSS / Databroker)

KUKSA converts raw CAN frames into standardized **VSS signals** (e.g. `Vehicle.Speed`) and feeds the Qt cluster. Two containers: a **Databroker** (Rust gRPC server on `localhost:55555`) and a **CAN Provider** (parses CAN via the `.dbc` + mapping `.json`). Config in [`src/Kuksa/`](src/Kuksa/).

### F.1 On the car (real CAN)

Edit `src/Kuksa/docker-compose.yml` and change the CAN interface from `vcan0` to `can0`:

```yaml
command: >
  --dbcfile /data/CAN_decoder.dbc
  --mapping /data/CAN_mapping.json
  --canport can0          # <-- real interface
  --server-type kuksa_databroker
  --use-socketcan
```

Start the middleware:

```bash
cd src/Kuksa
docker compose up -d
docker compose logs -f
```

### F.2 Mapping

- `CAN_decoder.dbc` — defines the CAN frames/signals (IDs `0x001`, `0x010`, `0x100`, `0x110`, `0x200`, `0x210`). See [`src/Kuksa/CAN_decoder.md`](src/Kuksa/CAN_decoder.md).
- `CAN_mapping.json` — maps each DBC signal to a VSS path (`Vehicle.Speed`, `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current`, etc.).

The ADAS pipeline also publishes detected traffic signs to KUKSA via gRPC (`Vehicle.ADAS.SpeedLimitSign`, `Vehicle.ADAS.TrafficSign`) — see [`ADAS/pipeline/kuksa_publish/`](ADAS/pipeline/kuksa_publish/).

---

## Part G — Deploying Everything to the Car

The `run.py` / `run_robotaxi.py` launchers expect a **fixed layout under `/home/`** on the Raspberry Pi. Reproduce it exactly.

### G.1 Target directory layout on the Pi

```
/home/
├── control                 # gamepad_control binary (from Docker, ARM64)
├── run.py                  # launcher (copy from scripts/start_program/)
├── run_robotaxi.py         # robotaxi launcher (copy from scripts/start_program/)
├── models/
│   ├── yolo26n_seg_640.hef # lane segmentation model
│   └── yolo26n_v6.hef      # object detection model
├── pipeline/               # ADAS/pipeline/  (standard LFA)
│   ├── main.py
│   ├── camera/  inference/  post_processing/  object/  LFA/
│   ├── decision/  kuksa_publish/  utils/  core/
│   └── ...
└── pipeline_robotaxi/      # ADAS/Taxi_Robot/ (Robotaxi variant)
    ├── main.py
    └── ... (includes localization/ and map/)
```

### G.2 Transfer from the host

From the repository root on your host (replace `root@<PI_IP>`):

```bash
# 1. Launcher scripts
scp scripts/start_program/run.py          root@<PI_IP>:/home/run.py
scp scripts/start_program/run_robotaxi.py root@<PI_IP>:/home/run_robotaxi.py

# 2. ADAS pipeline (standard)
rsync -avz --exclude='__pycache__' ADAS/pipeline/ root@<PI_IP>:/home/pipeline/

# 3. Robotaxi pipeline (optional)
rsync -avz --exclude='__pycache__' ADAS/Taxi_Robot/ root@<PI_IP>:/home/pipeline_robotaxi/

# 4. Models (place your .hef files here)
scp yolo26n_seg_640.hef root@<PI_IP>:/home/models/
scp yolo26n_v6.hef      root@<PI_IP>:/home/models/

# 5. Cross-compiled binaries
scp out/appcar_cluster   root@<PI_IP>:/home/control_cluster   # cluster binary (e.g. /opt/clusterqt)
scp out/gamepad_control  root@<PI_IP>:/home/control

# 6. Kuksa config (if not baked into the AGL image)
scp -r src/Kuksa/ root@<PI_IP>:/home/Kuksa/
```

> There's also a helper script [`scripts/code_to_rasp.sh`](scripts/code_to_rasp.sh) that rsyncs the Robotaxi pipeline to a fixed Pi address — edit `RASP_IP` / `RASP_USER` / `RASP_DEST` at the top before using it.

### G.3 Permissions & display env

```bash
ssh root@<PI_IP>
chmod +x /home/control /home/run.py /home/run_robotaxi.py

# The Qt cluster & pipeline local display need a Wayland compositor:
export XDG_RUNTIME_DIR=/run/user/200
export WAYLAND_DISPLAY=wayland-1
```

---

## Part H — Running the System

### H.1 Pre‑flight checklist (run every time)

1. **Battery on** — switch on the Expansion Board (so `0x40`/`0x60` are visible on I²C).
2. **STM32 powered** — firmware running, OLED active.
3. **Raspberry Pi booted** into AGL, SSH reachable.
4. **CAN up** — `sudo ip link set can0 up type can bitrate 500000`.
5. **Hailo visible** — `hailortcli scan` finds the device.
6. **Kuksa running** — `docker compose ps` shows `databroker` + `can-provider` up.
7. **Gamepad paired** — ShanWan gamepad connected over USB (`ls /dev/input/js*`).
8. **Models present** — `ls /home/models/*.hef`.

### H.2 Standard autonomous run (Lane Following Assist)

The launcher starts the gamepad control (manual override) **and** the ADAS pipeline together, and guarantees a CAN stop sequence on shutdown (Ctrl+C / SIGTERM):

```bash
python3 /home/run.py --pipeline
```

This is equivalent to, under the hood:

```bash
/home/control                                                # gamepad (manual override)
python3 /home/pipeline/main.py \
    /home/models/yolo26n_seg_640.hef \
    /home/models/yolo26n_v6.hef
```

**Useful flags** (passed straight through to `main.py`):

```bash
# Bench test — no CAN, no display:
python3 /home/run.py --pipeline --virtual --no-display

# Over SSH — stream the annotated view as JPEG to stdout:
python3 /home/run.py --pipeline --virtual --remote | mplayer -demuxer lavf -
```

### H.3 Robotaxi run (pickup → dropoff → parking)

The Robotaxi variant adds ArUco‑based localization and a mission state machine (parking → pickup → dropoff → return). It needs two ArUco IDs (pickup and dropoff):

```bash
python3 /home/run_robotaxi.py --pipeline_robotaxi <pickup_id> <dropoff_id>

# Example (from ADAS/Taxi_Robot/main.py):
python3 /home/run_robotaxi.py --pipeline_robotaxi 0 1
python3 /home/run_robotaxi.py --pipeline_robotaxi 9 8

# With flags:
python3 /home/run_robotaxi.py --pipeline_robotaxi 0 1 --virtual --no-display
```

See [`docs/Robotaxi/robotaxi_readme.md`](docs/Robotaxi/robotaxi_readme.md) for the mission/FSM details and the ArUco↔position map.

### H.4 Qt instrument cluster

In a separate SSH session (or as a systemd service on boot — see [`docs/AGL/AGL_wifi_connect.md`](docs/AGL/AGL_wifi_connect.md) "Autostart QT"):

```bash
export XDG_RUNTIME_DIR=/run/user/200
export WAYLAND_DISPLAY=wayland-1
/opt/clusterqt/appcar_cluster        # standard cluster (Main.qml)
# or, for the Robotaxi cluster UI:
ROBOTAXI_CLUSTER=1 /opt/clusterqt/appcar_cluster
```

The cluster subscribes to KUKSA VSS signals (`Vehicle.Speed`, battery SoC, etc.) and updates the dashboard in real time.

### H.5 Gamepad controls (manual override)

While `gamepad_control` is running, the ShanWan gamepad drives the car:

| Input | Action |
|---|---|
| Left stick Y | Throttle (forward/back) |
| Right stick X | Steering (left/right) |
| **Button A** | Switch to **AUTO** mode (pipeline drives) |
| **Button B** | Switch to **DEBUG** mode |
| **Button L1** | **PARKING** mode |
| Move either stick | Instant override → **MANUAL** (exits AUTO) |

> In AUTO mode the gamepad stays silent and the ADAS pipeline's throttle/steering CAN frames are used. Touching the stick immediately reclaims manual control — a safety feature.

### H.6 Shutdown

Press **Ctrl+C** in the launcher's terminal. `run.py` / `run_robotaxi.py` will:

1. Send a CAN **stop command** (throttle=0, steering=0) three times for reliability.
2. Terminate the Python pipeline and the gamepad process.

Always let the shutdown sequence finish before killing the process manually.

---

## CAN Signal Reference

The Pi and STM32 communicate over `can0` @ 500 kbps. From [`src/Kuksa/CAN_decoder.dbc`](src/Kuksa/CAN_decoder.dbc) / [`src/Kuksa/CAN_decoder.md`](src/Kuksa/CAN_decoder.md):

| CAN ID | Hex | Direction | Message | Key signals |
|---|---|---|---|---|
| 1 | `0x001` | Pi → STM32 | Drive command (gamepad / pipeline) | `throttle int16 LE`, `steering×100 int16 LE` (4 bytes) |
| 2 | `0x002` | Pi → STM32 | Drive command (pipeline `send_drive_command`) | throttle + steering |
| 3 | `0x003` | Pi → STM32 | Enable / mode select | drive enable / mode |
| 4 | `0x004` | Pi → STM32 | Parking command | parking mode |
| 16 | `0x010` | STM32 → Pi | **SPEED** | `Speed_Kmh` (factor 0.01) |
| 256 | `0x100` | Pi → STM32 | MOTOR_PWR (command) | `Throttle_Pos`, `Power_Watts` |
| 272 | `0x110` | Pi → STM32 | STEER (command) | `Steer_Angle` (−45…+45°) |
| 512 | `0x200` | STM32 → Pi | **BATTERY** | `Battery_SoC`, `Battery_Voltage`, `Battery_Current` |
| 528 | `0x210` | STM32 → Pi | **TEMPERATURE** | `Temp_Air`, `Temp_Motor` |
| 544 | `0x220` | STM32 → Pi | **ODOMETER** | distance (2 bytes) — see [`docs/odometer/`](docs/odometer/README.md) |

KUKSA maps these DBC signals to VSS paths via [`src/Kuksa/CAN_mapping.json`](src/Kuksa/CAN_mapping.json) (e.g. `Speed_Kmh` → `Vehicle.Speed`, `Battery_SoC` → `Vehicle.Powertrain.TractionBattery.StateOfCharge.Current`).

---

## File Layout on the Raspberry Pi

Quick reference of where everything lives once deployed (see [Part G](#part-g--deploying-everything-to-the-car)):

```
/home/
├── control                 # gamepad_control (ARM64 binary)
├── run.py                   # LFA launcher
├── run_robotaxi.py          # Robotaxi launcher
├── models/
│   ├── yolo26n_seg_640.hef  # lane model
│   └── yolo26n_v6.hef       # object model
├── pipeline/                # = ADAS/pipeline/
├── pipeline_robotaxi/       # = ADAS/Taxi_Robot/
└── Kuksa/                   # = src/Kuksa/  (docker-compose, dbc, mapping)

/opt/clusterqt/appcar_cluster   # Qt instrument cluster (ARM64 binary)
/etc/xdg/weston/weston.ini.default   # Weston compositor config
/lib/firmware/hailo/              # Hailo firmware (from AGL image)
```

---

## Troubleshooting

### Hailo: `CHECK failed - max_desc_page_size given 16384 is bigger than hw max desc page size 4096`
Apply the `force_desc_page_size=4096` fix — see [Part C.1](#c1-hailo-pcie-descriptor-fix-mandatory-on-agl). [`docs/AGL/AGL_hailo_PCIe_config.md`](docs/AGL/AGL_hailo_PCIe_config.md).

### Camera: `/dev/video*` missing / `rpicam-hello` finds no camera
The standard libcamera on AGL can't drive the Pi 5 ISP. You must use the **rpi‑libcamera** fork + `libpisp` + `rpicam-apps` baked into the AGL image — see [`docs/AGL/AGL_camera-setup.md`](docs/AGL/AGL_camera-setup.md).

### `rpicam-vid` stuck after a crash
```bash
pgrep -f rpicam-vid     # find the PID
kill <PID>
```
The camera module warns about this but won't kill it for you.

### CAN: `CanSender` / `socketcan` errors
Bring the interface up first: `sudo ip link set can0 up type can bitrate 500000`. For bench testing use `vcan0` (see [Part C.3](#c3-can-interface-can0)). [`ADAS/pipeline/utils/README.md`](ADAS/pipeline/utils/README.md).

### AGL build: host runs out of RAM
Yocto is heavy. Lower `BB_NUMBER_THREADS` and `PARALLEL_MAKE` in `conf/local.conf` — see [`docs/AGL/AGL_install.md`](docs/AGL/AGL_install.md) §5.

### AGL boot hangs (no HDMI output)
Comment out `enable_uart=1` in the boot partition's `boot/config.txt`.

### ST‑Link: `unknown chip id! 0x482` / flash erase fails
Your `stlink-tools` is too old (≤1.7.0). Build ≥ 1.8 from source — instructions in [`docs/ThreadX/st-link_compile-flash_threadX.md`](docs/ThreadX/st-link_compile-flash_threadX.md).

### STM32: Hard Fault when accessing GPIOH
On the B‑U585I‑IOT02A, GPIOH (LEDs) is secure‑only. Configure those ports as non‑secure or avoid them from the non‑secure domain — see [`docs/hardware/stm32_motor_wiring.md`](docs/hardware/stm32_motor_wiring.md) §4.2.

### Cluster: blank screen / "no Wayland"
The local display mode needs a running Weston compositor:
```bash
export XDG_RUNTIME_DIR=/run/user/200
export WAYLAND_DISPLAY=wayland-1
```
Or run the cluster headless with the pipeline's `--no-display` flag.

---

## Quick‑Start Checklist

A condensed path from an empty workbench to a driving car:

- [ ] **Hardware**: PiRacer assembled; STM32 wired to the HAT (I²C, SPI CAN, speed sensor); camera + Hailo + display connected to the Pi.
- [ ] **STM32**: `./src/threadx/SennaTech/compile_flash.sh slow` — OLED lights up, UART debug visible.
- [ ] **Pi OS**: AGL image built (with Hailo + rpi‑libcamera + meta‑services/clusterqt), flashed, booted from NVMe, Wi‑Fi/SSH up.
- [ ] **Hailo**: `force_desc_page_size=4096` applied; `hailortcli scan` works.
- [ ] **Camera**: `rpicam-hello --list-cameras` shows the IMX708.
- [ ] **CAN**: `sudo ip link set can0 up type can bitrate 500000`; `candump can0` shows STM32 frames.
- [ ] **Binaries**: `appcar_cluster` + `gamepad_control` cross‑compiled in Docker → copied to the Pi.
- [ ] **Models**: `yolo26n_seg_640.hef` + `yolo26n_v6.hef` in `/home/models/` on the Pi.
- [ ] **Pipeline**: `ADAS/pipeline/` → `/home/pipeline/`; (optional) `ADAS/Taxi_Robot/` → `/home/pipeline_robotaxi/`.
- [ ] **Launchers**: `run.py` + `run_robotaxi.py` in `/home/`; `gamepad_control` at `/home/control`.
- [ ] **Kuksa**: `docker compose up -d` in `src/Kuksa/` (with `--canport can0`).
- [ ] **Bench test**: `python3 /home/run.py --pipeline --virtual --no-display` — no CAN sent, logs show FSM states.
- [ ] **Drive**: `python3 /home/run.py --pipeline` — press **A** on the gamepad for AUTO, move the stick for manual override, **Ctrl+C** to stop.
- [ ] (Optional) **Robotaxi**: `python3 /home/run_robotaxi.py --pipeline_robotaxi 0 1`.

---

## Further Reading

- Project overview & structure: [`README.md`](README.md)
- ADAS pipeline internals: [`ADAS/pipeline/README.md`](ADAS/pipeline/README.md)
- Hailo model conversion: [`ADAS/convert_hailo/README.md`](ADAS/convert_hailo/README.md)
- Qt instrument cluster: [`src/car_cluster/README.md`](src/car_cluster/README.md)
- KUKSA architecture: [`src/Kuksa/kuksa.md`](src/Kuksa/kuksa.md)
- Robotaxi mission logic: [`docs/Robotaxi/robotaxi_readme.md`](docs/Robotaxi/robotaxi_readme.md)
- Cross‑compilation Docker: [`docker/README.md`](docker/README.md)
- All documentation index: [`docs/`](docs/)