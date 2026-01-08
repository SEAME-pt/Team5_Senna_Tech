# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - Speedometer Sensor Integration <br>
**Subsystem:** Speedometer Data Chain (I²C Speed Sensor -> STM32) <br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** 2026-01-07 <br>
**author:** Hellom Mendes <br>
**reviewer:** [Pending Review] <br>

---

## 1. Criticality Reference Scale
*Criteria used for hazard evaluation:*

| Level | Category | Description |
| :--- | :--- | :--- |
| **C4** | **Critical** | Failure causes physical damage to the prototype or immediate risk to the operator. |
| **C3** | **High** | Prototype stops working or loses its primary function, but no physical damage occurs. |
| **C2** | **Medium** | Loss of secondary functions; prototype continues to operate with limitations. |
| **C1** | **Low** | Inconvenience or aesthetic/log error that does not affect operation. |

---

## 2. Hazard Analysis
*Technical evaluation of sensor failure modes.*

| ID | Failure Mode | Autonomous Scenario Consequence | Criticality | Decision Support |
| :--- | :--- | :--- | :---: | :--- |
| **H1-200** | **I²C Communication Failure (e.g., NACK, Timeout)** | System reads 0 km/h and applies maximum motor power to compensate. | **C4** | [DS-HR200-2](./Decision_support/DS-HR200-2_I2C-Communication-Failure-Evidence.md) |
| **H2-200** | **Corrupted I²C Data (e.g., CRC/Checksum Mismatch) leading to Erratic High Value** | System reads excessive speed and performs emergency braking unexpectedly. | **C4** |
| **H3-200** | **Corrupted I²C Data (e.g., CRC/Checksum Mismatch) leading to Erratic Low Value** | Robot operates above the actual allowed speed limit for the environment. | **C4** |
| **H4-200** | **Stale I²C Data / Latency (e.g., Read Timeout)** | Old data causes oscillations in path tracking (instability). | **C2** |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-201 (Focus H1):** The I2C driver shall report communication failure in real-time (e.g., NACK, Timeout).
* **SG-202 (Focus H2, H3):** The I2C driver shall validate the integrity of every data payload from the sensor using a CRC or checksum mechanism.
* **SG-203 (Focus H4):** Every data sample shall be accompanied by a hardware timestamp to ensure data freshness.
* **SG-204 (Focus H1, H2, H3):** The system shall invalidate readings if the speed delta violates the motor's physical acceleration limits.
* **SG-205 (Focus: All Hazards):** To ensure its integrity and isolation, the I2C driver shall operate within a protected memory region configured via MPU (Memory Protection Unit) or a similar hardware mechanism (e.g., TrustZone).

---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

**Fail-Safe State (for C4 Hazards: H1, H2, H3):**
*   **Action:** Immediate interruption of motor PWM signals (Coast/Brake).
*   **Signaling:** Activation of visual warning (Red LED) or critical error logging in the console.

**Degraded Mode (for C2 Hazard: H4):**
*   **Action:** Reduce maximum speed to a safe level (e.g., 20% of normal) and continue attempting to acquire fresh data.
*   **Escalation:** If stale data persists for more than [200ms](./Decision_support/DS-HR200-1_Degraded-Mode-Timeout.md), escalate to Fail-Safe State.
*   **Signaling:** Activation of specific warning (e.g., Yellow LED) or warning log in the console.

---
**Additional Notes:**
- The core of TSF is Transparency. The research should prioritize methods that allow the sensor status to be exported clearly to the framework.
- Consider leveraging the STM32U5's TrustZone or Hardware CRC engine as primary evidence-generation tools.

---

## 5. Glossary
*   **I²C:** Inter-Integrated Circuit. A serial communication protocol used for short-distance communication between integrated circuits, often employed for sensors like the speedometer.
*   **NACK:** Not Acknowledged. In I²C communication, a signal from the slave (e.g., speedometer sensor) indicating it did not receive or process data correctly from the master (e.g., STM32). This is a type of communication failure.
*   **CRC:** Cyclic Redundancy Check. An error-detecting code used to detect accidental changes to raw data during transmission. When the STM32 receives speedometer data, it calculates a CRC and compares it to a value sent by the sensor.
*   **Checksum Mismatch:** Occurs when a calculated data integrity value (like a CRC) at the receiver (e.g., STM32) does not match the value sent by the transmitter (e.g., speedometer sensor). This indicates that the data was corrupted during transmission.
*   **Timeout:** In communication, a predefined period an initiator (e.g., STM32) waits for a response from a device (e.g., speedometer sensor). If no response is received within this time, a timeout error occurs, indicating a communication failure or stale data.
*   **Latency:** The delay between an event (e.g., actual speed change) and its reflection in the system's data (e.g., new speed reading available to STM32). High latency means the system operates with "stale data," which can lead to control instability.
*   **TrustZone:** A hardware-based security technology by ARM that creates an isolated, secure environment for trusted software, crucial for ensuring the integrity of critical components like the I²C driver.
*   **MPU:** Memory Protection Unit. A hardware unit used to define and protect regions of memory from unauthorized access, enhancing the isolation and integrity of software components.
*   **PWM:** Pulse-Width Modulation. A technique used to control the power delivered to electrical devices, such as motors, often used for speed control in autonomous vehicles.