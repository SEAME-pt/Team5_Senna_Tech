# Instrument Cluster - Senna Tech 🚗 

A **Qt-based car dashboard** that displays real vehicle data such as speed, battery level, and temperature through an elegant, animated QML interface.

This project demonstrates how **C++ (Qt backend)** and **QML (frontend)** can interact seamlessly to create modern, responsive automotive interfaces — a key concept behind **Software-Defined Vehicles (SDV)**.

The interface was specifically developed for the rear display of the **PiRacer** prototype, optimized for a wide **1280×400-pixel** screen configuration.

![screenshot](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/qt/src/car_cluster/assets/cluster_v2_light.png)
![screenshot](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/qt/src/car_cluster/assets/cluster_v2_dark.png)

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Data Flow](#-data-flow)
  - [Speed Signal Pipeline](#-speed-signal-pipeline)
  - [Battery Signal Pipeline](#-battery-signal-pipeline)
  - [Temperature Flow](#️-temperature-flow)
  - [Autonomy (Range) Calculation](#-autonomy-range-calculation)
- [Project Structure](#️-project-structure)
- [Main Components](#-main-components)
- [Features](#️-features)
  - [Theme Switching](#-theme-switching)
  - [Unit Switching](#-unit-switching)
  - [Warning System](#️-warning-system)
  - [Traffic Sign Integration](#-traffic-sign-integration-future-ready)
- [Build Instructions](#-build-instructions)
  - [Requirements](#-requirements)
  - [Cross-Compilation with Docker](#-cross-compilation-with-docker)
- [Runtime Requirements](#-runtime-requirements)
- [Project Goals](#-project-goals)
- [Future Improvements](#-future-improvements)
---

## 📸 Overview


The cluster consumes real vehicle data and provides:

- 🚗 **Real-time speed** (wheel sensor → CAN → KUKSA → Qt)
- 🔋 **Real battery level** (via CAN + KUKSA Databroker)
- 🌡️ **Temperature** from Raspberry Pi onboard sensor
- 📏 **Autonomy (range)** calculation based on battery level
- ⚙️ **Automatic Gear Selector**
  - `N` → vehicle stopped
  - `D` → moving forward
  - `R` → moving backward
- 🕒 **Live clock display**
- 🎨 **User customization**
  - Toggle between km/h and dm/h
  - Toggle between Light and Dark mode
- 🚦 **Traffic sign display** (currently simulated)
  - Designed for future camera-based detection integration
- ⚠️ **Dynamic warning system**
  - High temperature
  - Rising temperature
  - Low battery
  - Emergency stop

---

## 🧠 Architecture

| Layer | Technology | Description |
|-------|-----------|-------------|
| **Sensor Layer** | Wheel speed sensor | Captures wheel rotation pulses |
| **Control Layer** | Microcontroller | Calculates speed and sends CAN frames |
| **Communication** | CAN Bus | Transmits vehicle signals |
| **Middleware** | KUKSA CAN Provider + KUKSA Databroker | Converts CAN → VSS and stores signals |
| **Backend** | C++ (Qt 6) | Subscribes to vehicle signals and processes logic |
| **Frontend** | QML (Qt Quick) | Modular UI components and animations |
| **Hardware** | Raspberry Pi | Runs cluster and provides temperature data |
| **Build System** | CMake | Manages build configuration |

---

## 🔄 Data Flow

The instrument cluster receives real vehicle data through a complete embedded automotive pipeline.

### 🚗 Speed Signal Pipeline

1. **Wheel Speed Sensor (Speedometer)**  
   A physical sensor attached to the wheel captures rotation pulses.

2. **Microcontroller Processing**  
   The microcontroller:
   - Reads raw pulse signals
   - Calculates vehicle speed
   - Encapsulates the computed speed into CAN frames

3. **CAN Bus Transmission**  
   Speed data is transmitted over the CAN bus to the Raspberry Pi.

4. **KUKSA CAN Provider (Raspberry Pi)**
   - Listens to CAN frames
   - Parses incoming CAN messages
   - Converts signals into the VSS (Vehicle Signal Specification) format

5. **KUKSA Databroker**
   - Stores standardized signals (e.g., `Vehicle.Speed`)
   - Provides subscription-based access to applications

6. **Qt Backend (`vehicleData` class)**
   - Subscribes to VSS signals
   - Receives real-time updates
   - Exposes them to QML via `Q_PROPERTY`

7. **QML Frontend**
   - Reacts automatically through property bindings
   - Updates animations and UI elements in real time

### 🔋 Battery Signal Pipeline

Battery data follows the same structured path:

**Microcontroller → CAN Bus → KUKSA CAN Provider → VSS Conversion → KUKSA Databroker → Qt Backend → QML UI**

### 🌡️ Temperature Flow

Temperature is read directly from the Raspberry Pi onboard sensor.

The Qt backend:
- Periodically reads system temperature
- Updates QML bindings
- Triggers warning states when thresholds are exceeded

### 📏 Autonomy (Range) Calculation

Calculated inside the Qt backend based on:
- Current battery level
- Predefined consumption model
- Updated dynamically and exposed to QML

**This architecture ensures:**
- Clear hardware abstraction
- Middleware decoupling
- VSS standardization
- Real-time responsiveness
- Scalability for future vehicle signals

---

## 🗂️ Project Structure
```
.
├── CMakeLists.txt
├── Main.qml
├── README.md
├── main.cpp
├── vehicleData.hpp
├── vehicleData.cpp
├── components/
│   ├── BatteryPanel.qml
│   ├── Footer.qml
│   ├── GearSelector.qml
│   ├── Header.qml
│   ├── SpeedPanel.qml
│   ├── TrafficSign.qml
│   └── Warning.qml
├── assets/
│   ├── cluster/
│   ├── battery/
│   ├── traffic/
│   ├── warnings/
│   └── fonts/
├── protos/
│   └── kuksa/val/v2/
└── resources.qrc
```

The UI is fully modularized using reusable QML components.

---

## 🧩 Main Components

### 🔹 `vehicleData.hpp` / `vehicleData.cpp`

Responsible for:
- Subscribing to KUKSA Databroker signals
- Handling real-time vehicle updates
- Reading Raspberry Pi temperature
- Exposing properties to QML

### 🔹 `Main.qml`

Main dashboard layout integrating:
- Speed panel
- Battery panel
- Gear selector
- Traffic sign display
- Warning overlays
- Header (unit + theme toggles)
- Footer (clock + temperature)

### 🔹 `components/`

Modular UI structure:
- `SpeedPanel.qml` → Speed visualization
- `BatteryPanel.qml` → Battery + range
- `GearSelector.qml` → Automatic gear indicator
- `TrafficSign.qml` → Central traffic sign
- `Warning.qml` → Alert overlays
- `Header.qml` → Customization controls
- `Footer.qml` → Clock and temperature displays

---

## ⚙️ Features

### 🎨 Theme Switching

Users can toggle between:
- **Light Mode**
- **Dark Mode**

Assets and UI elements adapt dynamically.

### 📏 Unit Switching

Speed display supports:
- `km/h`
- `dm/h`

### ⚠️ Warning System

Warnings are triggered automatically when:
- Battery level is critically low
- Temperature exceeds safe limits
- Temperature is rapidly increasing
- Emergency stop condition is detected

Warnings are displayed visually in the cluster center.

### 🚦 Traffic Sign Integration (Future-Ready)

Currently simulated traffic signs are displayed in the center of the cluster.

The architecture is prepared to receive:
- Camera-detected traffic signs
- AI-based recognition results
- External vehicle signals

---

## 🧱 Build Instructions

### 🔧 Requirements

- Qt 6.5+ (Qt Quick + Qt Quick Controls 2)
- CMake 3.16+
- C++17 or later
- KUKSA Databroker running
- KUKSA CAN Provider running
- Raspberry Pi 
- Active CAN interface

### 🐳 Cross-Compilation with Docker

This project is designed to run on a **Raspberry Pi 5** with **ARM64 architecture**. The application is cross-compiled within a specialized Docker environment to ensure compatibility and reproducibility. All the process is detailed in this documentation: [AGL Cross-Compilation Development Environment](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/qt/docker/README.md)

The build process is integrated into an **OTA (Over-The-Air) update pipeline**, enabling seamless deployment and updates to the target device. Further details on the implementation and update protocols can be found here: [How to release a new version (Instrument Cluster)](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/qt/docs/OTA/InstrumentCluster.md)

---

## 🚀 Runtime Requirements

Before launching the cluster, ensure:
- CAN interface is active
- Microcontroller is transmitting CAN frames
- `kuksa-can-provider` is running
- `kuksa-databroker` is running
- VSS signals are properly mapped

---

## 🎯 Project Goals

This project demonstrates a complete **Software-Defined Vehicle (SDV)** development workflow:

- **End-to-end automotive data integration** – From physical sensors to UI visualization
- **Industry-standard signal processing** – CAN Bus to VSS (Vehicle Signal Specification) conversion
- **Middleware architecture** – Decoupled layers using KUKSA Databroker
- **Real-time embedded UI** – Qt/QML dashboard optimized for automotive displays
- **Production-ready deployment** – Cross-compilation, containerization, and OTA updates
- **Scalable design** – Modular architecture ready for additional vehicle signals and features

---

## 📌 Future Improvements

- Full camera-based traffic sign recognition integration
- Advanced vehicle diagnostics page
- Performance optimizations for embedded deployment

---