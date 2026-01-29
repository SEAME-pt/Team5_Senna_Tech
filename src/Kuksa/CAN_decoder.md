# CAN_decoder.dbc Documentation
**Project:** Kuksa (CAN-provider)

**File:** `CAN_decoder.dbc`

## 1. Overview
This file represents the **CAN Database (DBC)**. It acts as a "decoder ring" for the vehicle's network communication.

On the CAN bus, data travels as raw streams of zeros and ones (bits). This file instructs both the software and the engineers on how to translate those bits into human-readable physical values like "Speed in km/h" or "Battery %".

### Key Functions:
1.  **Decoding:** Translates raw Hex values (e.g., `0x09C4`) into physical values (e.g., `25.0 km/h`).
2.  **Validation:** Defines Minimum/Maximum ranges to detect sensor faults.
3.  **Topology:** Defines who sends the message (STM32 or PiRacer) and the data format.

---

## 2. Legend (The Basics)
To understand the file, you need to know these three key tags:

| Tag | Name | Description | Example |
| :--- | :--- | :--- | :--- |
| **BU_** | **Bus Unit** | The network nodes (ECUs/Computers). | `PiRacer`, `STM32` |
| **BO_** | **Build Object** | Defines a **Message** (A data packet). | `SPEED`, `BATTERY` |
| **SG_** | **Signal** | Defines a **Variable** inside the message. | `Speed_Kmh`, `Battery_SoC` |

---

## 3. How to Read a Signal (SG_)
The `SG_` line contains the logic to convert raw bits into real numbers.

**Syntax:**
`SG_ [Name] : [StartBit]|[Length]@[Endian][Sign] ([Factor],[Offset]) [Min|Max] "[Unit]"`

**Example from our file:**
```text
SG_ Speed_Kmh : 7|16@0+ (0.01,0) [0|250] "km/h" Vector__XXX
```

Decoding Steps:

A. Location (7|16)7:

The data starts at Bit 7.16: The data length is 16 bits (2 bytes).

B. Format (@0+)@0:

Indicates Big Endian (Most Significant Byte first).

+: Indicates Unsigned (Positive numbers only).

Note: If it were -, it would support negative numbers (Signed).

C. The Math ((0.01,0))

This is the conversion formula: `Formula: Physical_Value = (Raw_Value * Factor) + Offset`

0.01 (Factor): The multiplier (scaling).

0 (Offset): The value to add (usually zero).Practical

Example: If the CAN bus reads the raw integer 2500: 2500 x 0.01 + 0 = 25.0 km/h

## 4. Message Dictionary

🔴 **ID 1 (0x001) - E_STOP**

Description: Emergency Stop status.

Sender: STM32

Signals:E_Stop_Active (1 bit):

0 = System OK.

1 = EMERGENCY STOP ACTIVE.

🔵 **ID 16 (0x010) - SPEED**

Description: Vehicle speed measured by sensors (Hall effect).Sender: STM32Signals:Speed_Kmh: Range 0-250. Factor 0.01.

🟡 **ID 256 (0x100) - MOTOR_PWR (Commands)**

Description: Drive commands sent from the computer to the microcontroller.Sender: PiRacerSignals:Throttle_Pos: Accelerator position (0 to 100%). Factor 1.Power_Watts: Estimated power (-1000 to 1000 W).Signed Integer: Negative values indicate regenerative braking.

🟡 **ID 272 (0x110) - STEER (Commands)**

Description: Steering servo control.Sender: PiRacerSignals:Steer_Angle: Range -45 to +45 degrees. Factor 1.Negative (-) = Left turn.Positive (+) = Right turn.

🟢 **ID 512 (0x200) - BATTERY**

Description: High Voltage Battery Management System data.Sender: STM32Signals:Battery_SoC: State of Charge (0 to 100%).Battery_Voltage: Voltage. Factor 0.01.Example: Raw 1200 = 12.00 VBattery_Current: Current flow. Factor 0.01 (Signed).Example: Raw -500 = -5.00 A

🟠 **ID 528 (0x210) - TEMPERATURE**

Description: Thermal monitoring.Sender: STM32Signals:Temp_Air: Ambient temperature. Factor 0.1.Example: Raw 255 = 25.5 °CTemp_Motor: Motor temperature. Factor 1 (Integer).

## 5. Manual Decoding

Example: 
Imagine capturing this frame on the terminal:
```text
vcan0  512   [8]  55 04 B0 00 00 00 00 00
```
**Identify ID**: 512 corresponds to the BATTERY message.

**Byte 0 (SoC)**: Hex 0x55 -> Decimal 85.

Result: Battery at 85%.

**Bytes 1-2 (Voltage)**: Hex 0x04B0 -> Decimal 1200.

Math: 1200 x 0.01 = 12.

Result: Voltage is 12.00 V.
```