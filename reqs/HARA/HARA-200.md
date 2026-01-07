# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - Speedometer Sensor Integration <br>
**Subsystem:** Speedometer Data Chain (CAN Sensor -> STM32 -> SPI -> RPi) <br>
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

| ID | Failure Mode | Autonomous Scenario Consequence | Criticality |
| :--- | :--- | :--- | :---: |
| **H1-200** | **Loss of Function (M1)** | System reads 0 km/h and applies maximum motor power to compensate. | **C4** |
| **H2-200** | **Erratic High Value (M2)** | System reads excessive speed and performs emergency braking unexpectedly. | **C4** |
| **H3-200** | **Erratic Low Value (M3)** | Robot operates above the actual allowed speed limit for the environment. | **C3** |
| **H4-200** | **Stale Data / Latency (M4)** | Old data causes oscillations in path tracking (instability). | **C2** |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-200 (Focus H1/H2):** The system shall invalidate readings if the speed delta violates the motor's physical acceleration limits.
* **SG-200 (Focus H1):** The I2C driver shall report communication failure in real-time if the sensor fails to respond within [X] ms.
* **SG-200 (Focus H4):** Every data sample shall be accompanied by a hardware timestamp to ensure data freshness.

---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

* **Primary Action:** Immediate interruption of motor PWM signals (Coast/Brake).
* **Signaling:** Activation of visual warning (Red LED) or critical error logging in the console.

---
**Additional Notes:**
- The core of TSF is Transparency. The research should prioritize methods that allow the sensor status to be exported clearly to the framework.
- Consider leveraging the STM32U5's TrustZone or Hardware CRC engine as primary evidence-generation tools.
