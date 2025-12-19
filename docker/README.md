

# AGL Cross-Compilation Development Environment 

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Dockerfile - Detailed Explanation](#3-dockerfile---detailed-explanation)
4. [CMake toolchain file - Detailed Explanation](#4-cmake-toolchain-file---detailed-explanation)
5. [Final Container Structure](#5-final-container-structure)
6. [Recommended Workflow](#6-recommended-workflow)
7. [Conclusion](#7-conclusion)

## 1. Introduction

This repository provides a fully containerized development environment designed for building C++ and Qt/QML applications targeting Automotive Grade Linux (AGL) running on a Raspberry Pi 5 (ARM64). 

### Goals of the container

- **Accelerated development and testing**: Developers can build and test applications without relying on the physical Raspberry Pi hardware.
- **Reproducible builds**: The container defines a stable, isolated, and predictable environment.
- **Cross‑compilation**: Applications are compiled on an x86_64 host system but generate binaries for aarch64/ARM64.
- **CI/CD readiness**: The entire environment is portable and automated, enabling future integration with build and deployment pipelines.

Originally, the projects were compiled directly inside the Raspberry Pi running AGL. This approach was slow, hardware-dependent, and difficult to automate.

This container solves these issues by encapsulating:

- A controlled **x86_64 host environment**.
- An **AGL cross-compiler + sysroot**.
- A fully functional **Qt host build** + **Qt ARM64 build**.
- Ability to run **ARM binaries** using **QEMU**.

## 2. Architecture Overview

### Host / Target Architecture

- The Docker host is: **x86_64**
-   The compiled binaries target: **ARM64 (aarch64)**
    → These binaries run on Raspberry Pi 5 under AGL.

### Cross-compilation workflow
``` java
 Qt Host Tools        Qt ARM Build        AGL SDK
(moc, rcc, uic)     (target ARM64)      (sysroot + gcc)
       │                    │                 │
       └───────────► CMake/Ninja ◄────────────┘
                         │
                       Output
                  ARM64 Qt Application
```

### Why Qt Is Built Twice?

Qt requires:

1. **Host build (x86_64)** → provides tools like:

- ``moc``, ``rcc``, ``uic``, ``qmlcachegen`` and many other generators.


2. **Cross build (ARM64)** → actual Qt libs that run on the Raspberry Pi.

Without the host build, the cross build is impossible.

## 3. Dockerfile - Detailed Explanation

### 3.1 Base Image and Environment Variables
```dockerfile
FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
```
#### Why AMD64?

Even though the target is ARM64, we build on an x86_64 machine using:

- Qt host tools (which must run on the host)
- AGL’s cross-compiler (runs on x86_64)
- QEMU (to emulate ARM binaries)

#### Why configure locale and DEBIAN_FRONTEND?

- Prevents interactive prompts during installation.
- Ensures UTF-8 support, required by Qt build scripts.

### 3.2 Installing System Dependencies

Includes:
- ``build-essential``, ``cmake``, ``ninja-build`` → base tools for building Qt and CMake projects.
- ``libxkbcommon-dev``, ``libwayland-dev``, ``libxcb*`` → required to compile Qt with Wayland/EGL/XCB support. 
- ``qemu-user-static`` → executes ARM binaries inside the container. 
- ``locales`` → ensures Qt can configure environment correctly.

### 3.3 Downloading the Qt Source
``` bash
wget https://download.qt.io/.../qt-everywhere-src-6.7.3.tar.xz
```

Qt must be compiled from source because:
- Precompiled Qt binaries cannot be used for ARM cross‑compilation.
- Version **6.7.3** provides stable QtWayland and OpenGL ES support.

### 3.4 Installing the AGL SDK

The script:

```bash
./agl-sdk.sh
```
Installs:

- Cross-compiler (``aarch64-agl-linux-gcc``)
- ARM sysroots
- Environment setup script: ``environment-setup-aarch64-agl-linux``

Acrivating this environment script, this configures:

- PATH

- CC, CXX
- SYSROOT
- PKG_CONFIG paths

### 3.5 Building Qt for the HOST (x86_64)

Qt first compiles natively to generate host tools:

These tools are mandatory before cross‑compiling. Qt fails to cross‑compile if it does not detect a host build.

This build is installed under:

```bash
/opt/qt-host-build
```

### 3.6 Building Qt for ARM64 (Cross Build)

This stage uses:

- ``toolchain-agl-aarch64.cmake``
- Direct reference to host Qt tools via ``-DQT_HOST_PATH=/opt/qt-host-build``

Wayland and EGL are explicitly enabled:

- ``-DQT_FEATURE_wayland=ON``
- ``-DQT_FEATURE_opengl_es2=ON``

The resulting Qt installation is suitable for running natively on AGL, and is installed at the location:
```bash
/opt/qt-cross-build
```
### 3.7 Copying the ``car_cluster`` and ``car_control`` software into the Container

The projects directories is copied into:
```bash 
/root/car_cluster 
/root/car_control
```

This allows:

- Building directly inside the container
- CI/CD integration
- Running CMake without touching the host filesystem

### 3.8 Environment Adjustments

``/etc/bash.bashrc`` contains:

```bash
source /opt/agl-sdk/environment-setup-aarch64-agl-linux
```

This auto-activates the AGL environment through SDK when the container starts.

### 3.9 Cross compilation inside the Container

```dockerfile
RUN mkdir /root/car_cluster/build && cd /root/car_cluster/build && cmake .. -GNinja  -DQT_HOST_PATH=/opt/qt-host-build/ && ninja
```

This step is replicated for `car_cluster` and `car_control` projects and: 
- Creates a build directory
- Configure the project for `CMake` build system
- Compiles the code with `Ninja` using AGL sysroot
- Generates executable files compatible with the Raspberry Pi (ARM64)

### 3.10 Binaries location

The final cross-compiled binaries will be located in:
```bash 
/root/outputs
```

## 4. CMake toolchain file - detailed explanation

### 4.1 Target System Definition
```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
```

Tells CMake:

- We are cross-compiling from x86_64 → ARM64
- The target OS is Linux
- The processor architecture is ARM64

### 4.2 Sysroot Configuration

```cmake
set(CMAKE_SYSROOT /opt/agl-sdk/sysroots/aarch64-agl-linux)
```

Points to the AGL-provided root filesystem containing:

- Target headers
- Target libraries
- AGL-specific dependencies

This ensures CMake can correctly link against AGL libraries.

### 4.3 Cross Compilers

```cmake
set(CMAKE_C_COMPILER .../aarch64-agl-linux-gcc)
set(CMAKE_CXX_COMPILER .../aarch64-agl-linux-g++)
```

These compilers:

- Run on x86_64
- Produce ARM64 binaries 

### 4.4 Qt Integration
```cmake
set(QT_HOST_PATH /opt/qt-host-build)
set(Qt6_DIR /opt/qt-cross-build/lib/cmake/Qt6)
```

Qt requires:

- A host build (for tools)
- A target build (ARM libraries)

This toolchain file makes it explicit.

### 4.5 Find Root Path Logic
```cmake
set(CMAKE_FIND_ROOT_PATH ...)
```

This determines the search order for dependencies.

```cmake
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
```

Programs (like ``bash``, ``sh``) are searched on the host.

```cmake
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
```

Libraries, includes, and packages are searched only inside the sysroot.
This prevents accidental linkage to host libraries.

## 5. Final Container Structure

```bash
/opt
 ├── agl-sdk/               # AGL cross compiler + sysroots
 ├── qt-host-build/         # Qt tools built for x86_64
 └── qt-cross-build/        # Qt libraries built for ARM64
/root
 ├── car_control/           # Car control program (C++)
 ├── car_cluster/           # Car cluster project (Qt/QML)
 ├── outputs/               # Cross-compiled binaries
```

## 6. Recommended Workflow

### 6.1 Build the image

Assuming you are in the root of the ``Team5_Senna_Tech`` repository:
```bash
docker build -t agl-sdk-container -f docker/Dockerfile .
```

### 6.2 Start the container
```bash
docker run -it agl-sdk-container
```

### 6.3 Navigate to the outputs directory
```bash
cd /root/outputs
```

### 6.4 Deploy to Raspberry Pi

```bash
scp your_app root@raspberrypi:/path_to_executable
```

## 7. Conclusion

This containerized development environment provides a powerful, scalable, and automated solution for building applications for Automotive Grade Linux:

- Eliminates dependency on Raspberry Pi hardware

- Enables reproducible builds

- Ideal for CI/CD pipelines

- Fully supports Qt 6 + Wayland on ARM64

- Future-proof for automation and integration
