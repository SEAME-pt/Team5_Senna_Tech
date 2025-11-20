# **Cross Compilation for Raspberry Pi 5 with Automotive Grade Linux (AGL)**

## 📘 **Table of Contents**
1. [Introduction](#introduction)
2. [Preparing the AGL SDK Environment](#preparing-the-agl-sdk-environment)
3. [Cross Compiling the Car Control Program(C++)](#cross-compiling-the-car-control-programc)
6. [Cross Compiling the Instrument Cluster (Qt)](#cross-compiling-the-instrument-cluster-qt)
7. [Transferring the Binaries to the Raspberry Pi](#transferring-the-binaries-to-the-raspberry-pi)
8. [Important Notes](#important-notes)

---

## **Introduction**

This document describes the full **cross compilation workflow** used during the development of our embedded system, which consists of:

- A C++ program responsible for car control  
- A Qt-based **Instrument Cluster**

The target platform is a **Raspberry Pi 5**, running **Automotive Grade Linux (AGL)** on an **ARM64 (aarch64)** architecture.

Because this Raspberry Pi image is minimal and designed for embedded systems, it presents several limitations:

- It does **not** include compilers  
- It has only essential runtime dependencies  
- Its processing power should be preserved for running the system, not compiling large applications  

For these reasons, all compilation is performed on a **Ubuntu x86_64 host machine**, and only the final binaries are transferred to the Raspberry Pi.

---

## **Preparing the AGL SDK Environment**

Before compiling any application, you must extract the **AGL SDK** generated when building the AGL image via Yocto.

The SDK provides:

- Toolchain (set of tools used to compile and build software for a specific target system) for **aarch64** 
- Cross-compilers (`aarch64-agl-linux-gcc/g++`)
- Environment variables
- Complete sysroot for the target filesystem
- Setup scripts

After extracting the SDK, activate its environment with:

```bash
source <SDK>/environment-setup-aarch64-agl-linux
```

This command configures your shell session with:

- Cross-toolchain PATH
- Correct C and C++ compilers
- Variables such as PKG_CONFIG_SYSROOT_DIR, CC, CXX, etc.
- Access to the AGL sysroot

From this point on, all compilation is automatically targeted to ARM64.

## **Cross Compiling the Car Control Program(C++)**

The car_control project is a simple C++ application, and its cross-compilation process is straightforward.

### ✅ Step 1: Activate the SDK environment
```bash
source <SDK>/environment-setup-aarch64-agl-linux
```

### ✅ Step 2: Compile using the cross-compiler

Example:
```bash 
aarch64-agl-linux-g++ main.cpp piracer.cpp gamepad_controls.cpp -o car_control
```

The output will be an ARM64 executable suitable for AGL on the Raspberry Pi 5.

### 📦 Expected result
``car_control``  (ARM64 executable)


You can now transfer this binary to the target device.

## **Cross Compiling the Instrument Cluster (Qt)**

Qt applications require a more complex setup, especially when we want to integrate the process into **Qt Creator**, enabling automated builds and future deployment.

Below is the full configuration required to create a custom Build Kit for AGL inside Qt Creator.

### 🔧 Configuring the Kit in Qt Creator
#### 1. Select the correct C/C++ compiler

Choose the cross-compilers provided by the AGL SDK:

- ``aarch64-agl-linux-gcc``

- ``aarch64-agl-linux-g++``

These tools usually reside inside the SDK’s ``/usr/bin/`` folder.

#### 2. Build Environment

The build environment must inherit all variables defined by the SDK.

This is achieved by:

- Exporting the variables exposed by the ``environment-setup`` script

- Or configuring Qt Creator to load the environment script before building

#### 3. Sysroot

Set the sysroot to:

```bash
<SDK>/sysroots/aarch64-agl-linux
```

This ensures that:

- Include files

- Headers

- Libraries

- Qt dependencies

match the exact system that will run on the Raspberry Pi.

#### 4. Qt Version

Point Qt Creator to the **Qt version built inside the AGL SDK**.

This includes:

- The ``qmake`` binary

- Qt libraries compiled for **ARM64**

Example path:

```bash
<SDK>/sysroots/x86_64-agl-linux/usr/bin/qmake
```

#### 5. CMake Version (optional)

If your project uses CMake, select the version that matches or is included in the SDK.

#### 6. Build Directory

Set a dedicated build folder, such as:

```bash 
build-agl/
```


### ▶️ Building inside Qt Creator

Once the Kit is configured:

1. Open the project (CMake or .pro file)

2. Select the AGL Kit

3. Press **Build**

4. The ARM64 binary will appear in the designated build folder

The final binary is now ready for deployment.

## **Transferring the Binaries to the Raspberry Pi)**

To send a compiled binary to the device, use:

```bash
scp <file> root@<raspberry_ip>:/<path_to_executable_inside_raspberry>
```

### Important Notes

- Always run ``source environment-setup-aarch64-agl-linux `` before compiling.

- Qt Creator does not automatically detect the environment — everything must be configured in the Kit.

- Rebuilding the AGL SDK may change paths or toolchain details.

- Ensure that the Qt runtime version on the Raspberry Pi matches the Qt SDK version.

- Absolute paths reduce the chance of build errors.
