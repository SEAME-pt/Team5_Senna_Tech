
# Instrument Cluster - Senna Tech 🚗 

A **Qt-based car dashboard** that displays (simulated) vehicle data such as speed, battery level, and temperature through an elegant, animated QML interface.

This project demonstrates how **C++ (Qt backend)** and **QML (frontend)** can interact seamlessly to create modern, responsive automotive interfaces — a key concept behind **Software-Defined Vehicles (SDV)**.

The interface was specifically developed for the rear display of the **PiRacer** prototype, optimized for a wide **1280×400-pixel** screen configuration.

![screenshot](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/qt/src/car_cluster/cluster_v2_light.png)
![screenshot](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/qt/src/car_cluster/cluster_v2_dark.png)
---

## 📸 Overview

The project simulates:

- Vehicle **speed** changes (animated speedometer)
- **Battery level** decreasing over time
- A **temperature and autonomy** display
- A central **car view** with gear selector and dynamic road animation  

> ⚠️ All vehicle data is **fake/simulated** — the system currently does not connect to real hardware.  
> However, it is structured to easily integrate with real vehicle sensors in the future.

---

## 🧠 Architecture

| Layer | Language | Description |
|-------|-----------|-------------|
| **Backend (Logic)** | C++ | The `vehicleData` class simulates vehicle metrics using Qt timers and exposes them to QML via `Q_PROPERTY`. |
| **Frontend (UI)** | QML | The dashboard visual interface displays the simulated values and animations. |
| **Build System** | CMake | Defines project structure, compiles code, and manages Qt dependencies. |

---

## 🗂️ Project Structure

```
car_cluster/
├── CMakeLists.txt  # CMake configuration
├── main.cpp        # Application entry point
├── vehicleData.hpp # Vehicle data class (header)
├── vehicleData.cpp # Vehicle data class (implementation)
├── Main.qml        # Dashboard UI
├── mclaren.png     # Center car image
└── resources.qrc   # QML and image resources
```

---

## ⚙️ How It Works

1. The app starts and initializes Qt Quick style (`Basic`).
2. The singleton `vehicleData` object is created and exposed to QML as `vehicle`.
3. QML accesses vehicle data attributes directly through bindings like:

   ```qml
   property real currentSpeed: vehicle.speed
   property int batteryLevel: vehicle.battery
   ```
4. C++ periodically updates these values via simulation functions:

```cpp
vehicle->startSpeedSimulation();
vehicle->startBatterySimulation();
```
5. The QML interface reacts automatically, animating the dashboard instantly.



## 🧩 Main Components

### 🔹 ``vehicleData.hpp`` / ``vehicleData.cpp``

- Defines a singleton class responsible for:

- Holding vehicle attributes (``speed``, ``battery``, ``temperature``, ``isCharging``)

- Emitting signals when data changes

- Simulating dynamic values using ``QTimer``

### 🔹 ``main.cpp``
Application entry point, responsible for:

- Setting QML style (```QQuickStyle::setStyle("Basic")```)

- Initializing ``QQmlApplicationEngine``

- Registering the ``vehicleData`` singleton with QML

- Loading the ``Main.qml`` interface

- Starting data simulation

### 🔹 ``Main.qml``

Defines the entire dashboard layout and animation:

- Speedometer with animated gradient arc

- Gear selector (``P``, ``R``, ``N``, ``D``, ``S``)

- Battery, temperature, and autonomy indicators

- Central 3D-like car view


## 🧱 Build Instructions

### 🔧 Requirements

- **Qt 6.5+** (with Qt Quick and Qt Quick Controls 2)

- **CMake 3.16+**

- **C++17 or later**

- (Optional) **Qt Creator** for easier configuration

### 💻 Building from the terminal

```
# Create build directory
mkdir build && cd build

# Configure the project
cmake ..

# Build
cmake --build .

# Run
./appcar_cluster
```

## 🚀 Future Improvements

- Integration with real hardware sensors (e.g., CAN bus data)

- Additional dashboard elements (e.g., RPM, turn signals, time)

- Vehicle diagnostics page



