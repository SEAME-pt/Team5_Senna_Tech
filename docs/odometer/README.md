# Odometer System Implementation

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [3. Persistent Storage Strategy](#3-persistent-storage-strategy)
  - [3.1 Why a Dedicated Partition?](#31-why-a-dedicated-partition)
  - [3.2 Resizing Root Partition (sda2)](#32-resizing-root-partition-sda2)
  - [3.3 Create New Partition (sda3)](#33-create-new-partition-sda3)
  - [3.4 Format Partition](#34-format-partition)
  - [3.5 Mount Point](#35-mount-point)
  - [3.6 Persistent Mount](#36-persistent-mount)
- [4. STM32 Odometer Logic (ThreadX)](#4-stm32-odometer-logic-threadx)
  - [4.1 Pulse-Based Distance Calculation](#41-pulse-based-distance-calculation)
  - [4.2 Thread Implementation](#42-thread-implementation)
  - [4.3 CAN Transmission](#43-can-transmission)
  - [4.4 Thread Behavior](#44-thread-behavior)
- [5. Raspberry Pi Odometer Service (SocketCAN)](#5-raspberry-pi-odometer-service-socketcan)
  - [5.1 Socket Initialization](#51-socket-initialization)
  - [5.2 Frame Handling](#52-frame-handling)
  - [5.3 Current Behavior](#53-current-behavior)
- [6. Odometer File Format](#6-odometer-file-format)
  - [6.1 Reading Initial Value](#61-reading-initial-value)
- [7. Qt Backend Integration](#7-qt-backend-integration)
  - [7.1 File Read](#71-file-read)
  - [7.2 Update UI](#72-update-ui)
- [Conclusion](#conclusion)

---

## Overview

This document describes the complete implementation of the odometer system in the SEA:ME autonomous vehicle prototype.

The odometer system:

- Calculates travelled distance on the STM32 (ThreadX)
- Sends odometer updates via CAN (ID 0x220)
- Receives frames on the Raspberry Pi using SocketCAN
- Persists the value in a dedicated SSD partition
- Provides the value to the Qt backend
- Displays it on the Instrument Cluster (QML)

---

## 2. System Architecture

### Hardware

- **MCU:** STM32U585 (ThreadX RTOS)
- **MPU:** Raspberry Pi 5 (AGL)
- **Communication:** CAN Bus (MCP2515)
- **Sensor:** Rear wheel speed sensor (18 pulses per revolution)
- **Storage:** SSD card with dedicated `/odometer` partition

### Data Flow
```
Speed Sensor
↓
Interrupt (pulse_count++)
↓
STM32 Odometer Thread (ThreadX)
↓
CAN Frame (ID 0x220, 2 bytes)
↓
Raspberry Pi (SocketCAN - can0)
↓
/odometer/odometer.bin
↓
Qt Backend (C++)
↓
QML Instrument Cluster
```

---

## 3. Persistent Storage Strategy

### 3.1 Why a Dedicated Partition?

The odometer must:

- Survive reboot
- Survive power loss
- Survive new image flashes (Yocto Project)
- Be independent from rootfs updates

For this reason, a dedicated SSD partition was created.

### 3.2 Resizing Root Partition (sda2)

Before creating the new partition, the root filesystem (`/dev/sda2`) had to be reduced to free space.

**1️⃣ Identify partitions**
```bash
lsblk
```

Example:
```
sda
├─ sda1
├─ sda2 (rootfs)
```

**2️⃣ Resize filesystem**

First shrink filesystem:
```bash
resize2fs /dev/sda2 NEW_SIZE
```

Then adjust partition size using:
```bash
fdisk /dev/sda
```

> ⚠️ This is a critical operation and must be done carefully to avoid system corruption.

### 3.3 Create New Partition (sda3)

After freeing space:
```bash
fdisk /dev/sda
```

Create:
```
/dev/sda3
```

### 3.4 Format Partition
```bash
mkfs.ext4 /dev/sda3
```

### 3.5 Mount Point
```bash
mkdir /odometer
mount /dev/sda3 /odometer
```

### 3.6 Persistent Mount

Add to `/etc/fstab`:
```
/dev/sda3 /odometer ext4 defaults 0 2
```

---

## 4. STM32 Odometer Logic (ThreadX)

**File:** `odometer_thread_entry`

### 4.1 Pulse-Based Distance Calculation

Speed sensor characteristics:

- 18 pulses = 1 wheel rotation
- 1 rotation = `WHEEL_CIRCUMFERENCE_MM`

Formula:
```
Distance_mm = total_pulses * (WHEEL_CIRCUMFERENCE_MM / 18)
Distance_m  = Distance_mm / 1000
```

### 4.2 Thread Implementation

Key variables:
```c
extern volatile uint32_t pulse_count;
```

Main logic:
```c
delta = pulse_count - last_pulse_count;
total_pulses_accum += delta;

total_distance_mm = total_pulses_accum * (WHEEL_CIRCUMFERENCE_MM / 18);
total_distance_m  = total_distance_mm / 1000;
```

The value is stored as:
```c
uint16_t total_distance_m;
```

**Unit:** meters

### 4.3 CAN Transmission

- **CAN ID:** `0x220`
- **DLC:** 2 bytes

Frame packing (Big Endian):
```c
odometer_frame.data[0] = total_distance_m >> 8 & 0xFF;
odometer_frame.data[1] = total_distance_m & 0xFF;
```

Transmission only occurs when:
```
total_distance_m > last_sent_distance_m
```

So the MCU sends only when a new meter is reached.

### 4.4 Thread Behavior

- Runs continuously
- Sleeps using:
```c
tx_thread_sleep(1);
```

- Updates shared vehicle state using mutex

---

## 5. Raspberry Pi Odometer Service (SocketCAN)

The Raspberry runs a dedicated C++ user-space service.

It:

- Opens CAN raw socket
- Binds to `can0`
- Listens for CAN ID `0x220`
- Updates odometer file

### 5.1 Socket Initialization
```c
int sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
```

**Interface:** `can0`

### 5.2 Frame Handling

When receiving frame:
```c
uint16_t received_m = (frame.data[0] << 8) | frame.data[1];
```

> ⚠️ Endianness: Big Endian (network order)

### 5.3 Current Behavior

After receiving:
```c
odometer_value++;
write_odometer_to_file(odometer_value);
```

Important:

- The service increments the stored value by 1
- It does NOT directly trust `received_m`
- The file acts as the persistent accumulator

---

## 6. Odometer File Format

**File:** `/odometer/odometer.bin`

**Format:**
- Binary
- 2 bytes
- `uint16_t`
- Little-endian (native host order)

Example write:
```cpp
outfile.write(reinterpret_cast<const char*>(&odometer), sizeof(odometer));
```

### 6.1 Reading Initial Value

At startup:
```cpp
uint16_t odometer_value = read_odometer_from_file();
```

If file exists → continue from previous value.

---

## 7. Qt Backend Integration

The Qt backend reads the binary file every 500ms.

**Function:** `void vehicleData::updateOdometer()`

### 7.1 File Read
```cpp
QFile odometerFile("/odometer/odometer.bin");
```

Read operation:
```cpp
odometerFile.read(reinterpret_cast<char*>(&odometer_read), sizeof(odometer_read));
```

### 7.2 Update UI

After reading:
```cpp
setOdometer(odometer_read);
```

The value is exposed to QML via property binding.

---

## 8. Conclusion

The odometer system provides:

- Real-time deterministic distance calculation (STM32 + ThreadX)
- Efficient CAN communication
- Persistent storage using dedicated SSD partition
- Clean integration with Qt HMI