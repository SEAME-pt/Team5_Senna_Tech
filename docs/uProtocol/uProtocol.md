# README — uProtocol Integration in SEA:ME (CAN → AGL → Qt)

## 📚 Index
1. [Introduction](#1-introduction)
2. [What uProtocol Is (and Is Not)](#2-what-uprotocol-is-and-is-not)
3. [Why uProtocol Matters in SDV Architectures](#3-why-uprotocol-matters-in-sdv-architectures)
4. [Message Semantics vs Transport Medium](#4-message-semantics-vs-transport-medium)
5. [uProtocol Message Model](#5-uprotocol-message-model)
6. [Why uProtocol Cannot Be Sent Directly Over CAN 2.0](#6-why-uprotocol-cannot-be-sent-directly-over-can-20)
7. [Correct Integration Pattern: Uplift on the Raspberry Pi](#7-correct-integration-pattern-uplift-on-the-raspberry-pi)
8. [System Architecture Overview](#8-system-architecture-overview)
9. [End-to-End Example: Speed Sensor → STM32 → CAN → AGL → Qt](#9-end-to-end-example-speed-sensor--stm32--can--agl--qt)
10. [Code Examples](#10-code-examples)
11. [Conclusion](#11-conclusion) 



# 1. Introduction
uProtocol is an abstraction layer designed for Software-Defined Vehicles (SDVs) to unify communications across embedded ECUs, high-performance compute units, infotainment systems, cloud services, and mobile applications.  
This document explains:

- How uProtocol works  
- How message semantics differ from transport  
- Why CAN cannot carry native uProtocol messages  
- How to correctly apply a semantic uplift on the Raspberry Pi  
- How to integrate uProtocol with Qt for an instrument cluster UI  
- A complete end‑to‑end example (sensor → MCU → CAN → Raspberry Pi → Qt)



# 2. What uProtocol Is (and Is Not)
uProtocol **is not**:

- a transport protocol  
- a replacement for CAN, SOME/IP, MQTT, Binder, or Zenoh  
- a serialization format  

uProtocol **is**:

- a standard way to define messages, resources, services, semantics  
- an abstraction layer enabling cross-domain, transport‑agnostic communication  
- a library and API allowing developers to write applications independent of transport mechanics  

It sits conceptually *above* transport layers and focuses on **semantics**.


# 3. Why uProtocol Matters in SDV Architectures
Modern vehicles contain multiple technological domains:

- **ECUs (CAN, LIN, FlexRay, SOME/IP)**  
- **Infotainment (Binder / Android Automotive)**  
- **IoT gateways (MQTT, Zenoh, DDS)**  
- **Cloud (REST, WebSockets, Kafka)**  

OEMs need a **unified way to describe and consume services**, regardless of where they run.

uProtocol provides:

- global addressing  
- consistent API usage  
- unified service discovery  
- shared programming model  
- cross-platform message semantics  

This reduces development and integration complexity.

---

# 4. Message Semantics vs Transport Medium
uProtocol stresses a fundamental architectural separation:

Semantics = WHAT is being communicated  
(COVESA VSS resources, message meaning, structure)

Transport = HOW bytes move between components  
(CAN, TCP, SOME/IP, MQTT, Zenoh, Binder…)

Example:  
`vehicle.speed` is meaningful no matter if the signal came from CAN, MQTT, or Binder.

This separation enables SDV modularity.

# 5. uProtocol Message Model
A uProtocol message consists of:

```
uMessage:
  header:
  resource:
  payload:
```

Header  
Metadata describing the message.

| Field | Description |
|-------|-------------|
| `source` | service sending the message |
| `timestamp` | epoch time |
| `uEID` | endpoint identifier |
| `qos` | best-effort, reliable, etc. |

Example:

```
header:
  source: stm32.speed.service
  timestamp: 1712605512
  qos: best_effort
```

Resource Namespace  
Based on **COVESA Vehicle Signal Specification (VSS)**.

Examples:

```
vehicle.speed
vehicle.powertrain.combustion.engineSpeed
vehicle.cabin.temperature
```

Payload  
Actual value, encoded in JSON/CBOR/Protobuf depending on platform.

Example:

```json
{ "value": 31.4 }
```


# 6. Why uProtocol Cannot Be Sent Directly Over CAN 2.0
CAN 2.0 payload = **8 bytes maximum**.

Typical uProtocol metadata exceeds **40–300 bytes**.

Therefore:

- ❌ Impossible to transport native uMessages over CAN  
- ❌ Fragmentation possible but inefficient  
- ✔ Correct: **transport raw values over CAN**  

OEMs also use this method.

# 7. Correct Integration Pattern: Uplift on the Raspberry Pi
**Semantic uplift** = reconstructing a full uMessage after receiving its raw transport version.

Process:

1. STM32 sends raw bytes over CAN  
2. Raspberry Pi (AGL) receives CAN frame  
3. Raspberry Pi converts it to a structured uProtocol message  
4. Qt UI consumes the clean semantic message  

This is the correct and expected pattern in SEA:ME.

# 8. System Architecture Overview

```
+--------------------+        +---------------------------+        +---------------------------+
| Speed Sensor       |        | STM32 (ThreadX RTOS)     |        | Raspberry Pi (AGL Linux)  |
| (I2C)              | -----> | - Reads sensor           | -----> | - Receives CAN            |
+--------------------+        | - Encodes raw bytes      |  CAN   | - Performs uProtocol      |
                              +---------------------------+        |   uplift                  |
                                                                    | - Publishes to Qt UI      |
                                                                    +---------------------------+
```

Qt UI then displays `vehicle.speed` from the uMessage.


# 9. End-to-End Example: Speed Sensor → STM32 → CAN → AGL → Qt

## 9.1 STM32 ThreadX reads speed
Speed is sampled via I²C or internal capture hardware.

Example raw value:
```
31.4 km/h
```

## 9.2 STM32 sends compact CAN payload
Convert speed to integer:

```
speed_raw = 31
```

Send over CAN:

```
data[0] = 0x00
data[1] = 0x1F
```

CAN frame example:

```
ID = 0x100
Payload = 00 1F
```

## 9.3 Raspberry Pi receives CAN via SocketCAN

```
can0: ID=0x100 DATA=00 1F
```

Convert back to km/h:

```
speed = 31
```

## 9.4 Raspberry Pi constructs uProtocol message (uplift)

```json
{
  "header": {
    "source": "stm32.speed.service",
    "timestamp": 1712605512
  },
  "resource": "vehicle.speed",
  "payload": { "value": 31.0 }
}
```

## 9.5 Qt UI consumes uProtocol message
Qt subscribes to the message and updates the speedometer.


# 10. Code Examples

10.1 STM32 ThreadX sending CAN frame

```c
uint16_t speed = (uint16_t)(current_speed_kmh);

CAN_TxHeaderTypeDef header;
header.StdId = 0x100;
header.DLC = 2;

uint8_t data[2];
data[0] = (speed >> 8) & 0xFF;
data[1] = speed & 0xFF;

HAL_CAN_AddTxMessage(&hcan, &header, data, &mailbox);
```

10.2 Python reading CAN on AGL

```python
import can

bus = can.interface.Bus('can0', bustype='socketcan')

msg = bus.recv()
speed_raw = (msg.data[0] << 8) | msg.data[1]
speed_kmh = float(speed_raw)
```

10.3 Constructing a uProtocol message (pseudo-Python)

```python
from uprotocol import Message, Header, Timestamp

u_msg = Message(
    header=Header(
        source="stm32.speed.service",
        timestamp=Timestamp.now()
    ),
    resource="vehicle.speed",
    payload={"value": speed_kmh}
)
```

Qt then receives and displays the message.

# 11. Conclusion
This document clarified:

- uProtocol provides **semantics**, not transport  
- CAN should carry only **raw values**  
- Raspberry Pi should perform **semantic uplift**  
- Qt UI consumes uProtocol messages cleanly  
