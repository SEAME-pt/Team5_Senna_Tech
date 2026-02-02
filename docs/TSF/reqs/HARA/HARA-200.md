# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - Speedometer Sensor Integration <br>
**Subsystem:** Speedometer Data Chain (Pulse Sensor -> STM32) <br>
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
| **H1-200** | **Sensor Connection Failure (e.g., disconnected/broken cable)** | System reads 0 km/h and applies maximum motor power to compensate. | **C4** | [DS-HR200-1](../../docs/TSF/Decision_support/DS-HR200-1_Comm-Failure-Hazard-Justification.md) |
| **H2-200** | **Incorrect Pulse Reading (e.g., electrical noise/bouncing) leading to Erratic High Value** | System reads excessive speed and performs emergency braking unexpectedly. | **C4** | [DS-HR200-2](../../docs/TSF/Decision_support/DS-HR200-2_Data-Corruption-Hazard-Justification.md) |
| **H3-200** | **Incorrect Pulse Reading (e.g., electrical noise/bouncing) leading to Erratic Low Value** | Robot operates above the actual allowed speed limit for the environment. | **C4** | [DS-HR200-2](../../docs/TSF/Decision_support/DS-HR200-2_Data-Corruption-Hazard-Justification.md) |
| **H4-200** | **Stale Pulse Data / Latency (e.g., processing delays on STM32)** | Old data causes oscillations in path tracking (instability). | **C2** | [DS-HR200-3](../../docs/TSF/Decision_support/DS-HR200-3_Stale-Data-Hazard-Justification.md) |
| **H5-200** | **Pulse Counting Logic Failure (e.g., counter overflow, calculation error)** | Incorrect speed calculation, leading to dangerous system behavior. | **C4** | [DS-HR200-4](../../docs/TSF/Decision_support/DS-HR200-4_Incorrect-Config-Hazard-Justification.md) |
| **H6-200** | **Sensor Degradation / Physical Failure** | Sensor provides consistently inaccurate data (offset, drift, stuck value), leading to improper control decisions. | **C4** | [DS-HR200-5](../../docs/TSF/Decision_support/DS-HR200-5_Sensor-Degradation-Hazard-Justification.md) |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

| ID | Description | Decision Support |
| :--- | :--- | :--- |
| **SG-201** | (Focus H1) The system shall detect the absence of pulses for a prolonged period (indicating disconnected sensor). | [DM-HR200-1](../../docs/TSF/Decision_support/DM-HR200-1_Comm-Failure-Mitigation.md) |
| **SG-202** | (Focus H2, H3) The software shall filter spurious pulses to ensure the integrity of the count. | [DM-HR200-2](../../docs/TSF/Decision_support/DM-HR200-2_Pulse-Filtering-Mitigation.md) |
| **SG-205** | (Focus: All Hazards) To ensure its integrity and isolation, the pulse sensor driver (interrupt routines and calculation logic) shall operate within a protected memory region configured via MPU (Memory Protection Unit) or a similar hardware mechanism (e.g., TrustZone). | [DM-HR200-3](../../docs/TSF/Decision_support/DM-HR200-3_MPU-Isolation-Mitigation.md) |
| **SG-206** | (Focus H5) The RPM/speed calculation logic shall be protected against pulse counter overflow. | [DM-HR200-4](../../docs/TSF/Decision_support/DM-HR200-4_Counter-Overflow-Mitigation.md) |
| **SG-207** | (Focus H6) The system shall perform a plausibility check on the speedometer data, comparing it against a secondary source (e.g., IMU-derived velocity or a system dynamics model) to detect sensor drift or physical failure. | [DM-HR200-5](../../docs/TSF/Decision_support/DM-HR200-5_Plausibility-Check-Mitigation.md) |

---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

**Fail-Safe State (for C4 Hazards: H1, H2, H3):**
*   **Action:** Immediate interruption of motor PWM signals (Coast/Brake).
*   **Signaling:** Activation of visual warning (Red LED) or critical error logging in the console.

**Degraded Mode (for C2 Hazard: H4):**
*   **Action:** Reduce maximum speed to a safe level (e.g., 20% of normal) and continue attempting to acquire fresh data.
*   **Escalation:** If stale data persists for more than 200ms, escalate to Fail-Safe State.
*   **Signaling:** Activation of specific warning (e.g., Yellow LED) or warning log in the console.

---
**Additional Notes:**
- The core of TSF is Transparency. The research should prioritize methods that allow the sensor status to be exported clearly to the framework.
- Consider leveraging the STM32U5's TrustZone or Hardware CRC engine as primary evidence-generation tools.

---

## 5. Glossary

*   **CRC:** Cyclic Redundancy Check. An error-detecting code used to detect accidental changes to raw data during transmission. When the STM32 receives speedometer data, it calculates a CRC and compares it to a value sent by the sensor.
*   **Checksum Mismatch:** Occurs when a calculated data integrity value (like a CRC) at the receiver (e.g., STM32) does not match the value sent by the transmitter (e.g., speedometer sensor). This indicates that the data was corrupted during transmission.
*   **Timeout:** In communication, a predefined period an initiator (e.g., STM32) waits for a response from a device (e.g., speedometer sensor). If no response is received within this time, a timeout error occurs, indicating a communication failure or stale data.
*   **Latency:** The delay between an event (e.g., actual speed change) and its reflection in the system's data (e.g., new speed reading available to STM32). High latency means the system operates with "stale data," which can lead to control instability.
*   **TrustZone:** A hardware-based security technology by ARM that creates an isolated, secure environment for trusted software, crucial for ensuring the integrity of critical components like the pulse sensor driver.
*   **MPU:** Memory Protection Unit. A hardware unit used to define and protect regions of memory from unauthorized access, enhancing the isolation and integrity of software components.
*   **Pulse Sensor / Encoder:** An electromechanical sensor that converts the angular position or motion of a shaft into a series of electrical pulses.
*   **Debouncing:** A technique used to ensure that a single physical contact or pulse from a sensor is registered as a single event, by filtering out spurious signals caused by mechanical bouncing or electrical noise.
*   **IMU:** Inertial Measurement Unit. An electronic device that measures and reports a body's specific force, angular rate, and sometimes the orientation of the body, using a combination of accelerometers and gyroscopes. It can be used as a secondary source for velocity estimation.