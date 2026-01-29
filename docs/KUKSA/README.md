# Eclipse Kuksa Services Setup and Implementation on Raspberry Pi 5 (AGL)

---

## 1. Overview

Eclipse Kuksa is an open-source project (Apache 2.0 license) that provides a software platform for vehicles, enabling applications to access and control vehicle data and functionalities in a standardized way.

The project is based on the **COVESA Vehicle Signal Specification (VSS)**, which defines the names and semantics of a wide variety of data entries that represent the current and/or intended state of a vehicle's sensors and actuators, organized in a tree-like structure (example: `Vehicle.Speed`).

In this project, Eclipse Kuksa is deployed on a **Raspberry Pi 5 running Automotive Grade Linux (AGL)** to act as a **central vehicle data gateway**. All CAN data is received, parsed, and centralized inside the **Kuksa Databroker**, and then consumed by our **Qt-based Instrument Cluster application**, which displays:

* Vehicle speed
* Battery level
* Temperature

This document explains both:

* How Eclipse Kuksa works conceptually
* How the services were practically implemented and configured on the target system

---

## 2. System Architecture (Conceptual)

The Kuksa system follows a modular architecture with two main interacting components:

```
+------------------+
|   Applications   |
|     (Clients)    |
+--------+---------+
         | (gRPC/WebSocket API)
+--------+---------+
|  Kuksa Databroker|
|   (VSS Server)   |
+--------+---------+
         | (gRPC API)
+--------+---------+
| Kuksa CAN Provider|
+--------+---------+
         | (SocketCAN)
+--------+---------+
|    CAN Bus       |
|      (ECUs)      |
+------------------+
```

---

## 3. Architecture in This Project (Practical View)

```
CAN Bus
   ↓
Kuksa CAN Provider (dbcfeeder.py)
   ↓
Kuksa Databroker
   ↓
Qt Instrument Cluster Application
```

The Raspberry Pi 5 hosts:

* Kuksa Databroker
* Kuksa CAN Provider
* Custom VSS file
* Custom DBC file

The Qt application runs as a client and subscribes to VSS signals.

---

## 4. Core Components

### 4.1 Kuksa Databroker

The Databroker is the core of the system, implementing a resource-efficient VSS signal tree optimized to run inside a vehicle on a microprocessor-based platform.

**Technical Characteristics**

* Language: Rust
* Interface: gRPC API
* Lightweight (<4 MB static build)
* License: Apache 2.0

**Responsibilities**

* Stores all vehicle signals
* Maintains hierarchical VSS tree
* Provides API for:

  * Reading values
  * Writing values
  * Subscribing to changes

---

### 4.2 Kuksa CAN Provider

The CAN Provider is the bridge between:

* Low-level CAN frames
* High-level VSS signals

**Technical Characteristics**

* Language: Python
* Input: SocketCAN
* Mapping: DBC file + mapping logic

**Operating Modes**

* `dbc2val` (used in this project)
* `val2dbc` (not used)

---

## 5. Typical Data Flow

### Reading (Speed Example)

1. ECU sends CAN frame with speed
2. CAN Provider captures frame
3. Frame decoded using DBC
4. Signal mapped to `Vehicle.Speed`
5. Databroker updated
6. Qt cluster receives update
7. Speed gauge refreshed

---

## 6. Building the Custom AGL Image

Kuksa support is not enabled by default in all AGL images. Therefore, a custom image was built.

### 6.1 Adding Kuksa Layer

Only one layer was required. In `bblayers.conf`:

```
${METADIR}/meta-agl/meta-agl-kuksa-val
```

### 6.2 Include New Packages at Image

In file ``local.conf``, new packages were added:
```
IMAGE_INSTALL:append = " \
  kuksa-databroker \
  kuksa-can-provider \
  grpc \
  protobuf \
"
```
The compilation and flashing process of the custom AGL image for the Raspberry Pi followed the step-by-step instructions available in the project documentation: [AGL_INSTALL](http://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/kuksa-CAN-provider/docs/AGL/AGL_install.md)

---

## 7. Creating Systemd Services

Both Kuksa services must start automatically at boot.

---

### 7.1 Kuksa Databroker Service

File:

```
/etc/systemd/system/kuksa-databroker.service
```

```
[Unit]
Description=Kuksa Databroker
After=network.target

[Service]
ExecStart=/usr/bin/databroker --vss /home/Kuksa/custom_vss.json
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### 7.2 Kuksa CAN Provider Service

File:

```
/etc/systemd/system/kuksa-can-provider.service
```

```
[Unit]
Description=Kuksa CAN Provider
After=kuksa-databroker.service

[Service]
ExecStart=/usr/bin/dbcfeeder.py $EXTRA_ARGS
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### 7.3 Enable Services

```
systemctl daemon-reload
systemctl enable kuksa-databroker
systemctl enable kuksa-can-provider
systemctl start kuksa-databroker
systemctl start kuksa-can-provider
```

---

## 8. VSS Configuration (custom_vss.json)

Location:

```
/home/Kuksa/custom_vss.json
```

Defines all signals available to applications.

Example:

```
{
  "Vehicle": {
    "Speed": {
      "type": "float",
      "unit": "km/h"
    }
  }
}
```

This file determines what the Qt application can subscribe to.

---

## 9. CAN Parsing – CAN_decoder.dbc

The file `CAN_decoder.dbc` is the **CAN parser**.

It defines:

* Frame IDs
* Signals
* Bit positions
* Scaling

It is responsible for transforming raw CAN bytes into physical values.

Detailed documentation for our custom dbc file is provided here: [CAN_decoder](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/kuksa-CAN-provider/src/Kuksa/CAN_decoder.md](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/kuksa-CAN-provider/src/Kuksa/CAN_decoder.md))

---

## 10. CAN Provider Parsing Flow

```
CAN Frame
   ↓
CAN_decoder.dbc
   ↓
Physical Signal
   ↓
Mapping Logic
   ↓
VSS Path (Vehicle.Speed)
   ↓
Databroker
```

The dbcfeeder script:

* Reads CAN frames
* Uses `CAN_decoder.dbc`
* Converts to physical values
* Publishes values to Databroker

---

## 12. Service Validation

Check status:

```
systemctl status kuksa-databroker
systemctl status kuksa-can-provider
```

Expected state:

```
active (running)
```

---

## 13. Conclusion

This implementation combines the conceptual architecture of Eclipse Kuksa with a concrete embedded deployment on Raspberry Pi 5 using AGL. The platform acts as a robust automotive data gateway, transforming raw CAN traffic into standardized VSS signals and making them available to the Qt Instrument Cluster in a clean, modular, and scalable way.
