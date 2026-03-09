# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - [Insert Project Name] <br>
**Subsystem:** [Insert Sensor Name, e.g., I2C Encoder] <br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** [Insert Date] <br>
**author:** [Senna Tech member] <br>
**reviewer:** [Reviewer Name] <br>

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
| **H1-XXX** | **[e.g., Total Loss of Comm]** |[e.g., RPi stops receiving data; car maintains last speed.] | **C4** |
| **H2-XXX** | **[e.g., Stale/Frozen Data]** | [e.g., Old speed value causes PID controller to over-accelerate.] | **C4** |
| **H3-XXX** | **[e.g., Bus Congestion]** | [e.g., High latency (>100ms) on steering commands.] | **C3** |
| **H4-XXX** | **[e.g., Data Corruption]** | [e.g., Bit-flip leads to incorrect ID mapping or wrong CRC.] | **C3** |
| **H5-XXX** | **[e.g., OLED Display Glitch]** | [e.g., The onboard status screen flickers or shows corrupted characters. Internal control logic remains 100% nominal.] | **C1** |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-XXX (Focus H1/H2):** [e.g., the system shall invalidate readings if the speed delta violates the motor's physical acceleration limits.]
* **SG-XXX (Focus H1):** [e.g.,The I2C driver shall report communication failure in real-time if the sensor fails to respond within [X] ms.]
* **SG-XXX (Focus H4):** [e.g.,Every data sample shall be accompanied by a hardware timestamp to ensure data freshness.]

---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

* **Primary Action:** Immediate interruption of motor PWM signals (Coast/Brake).
* **Signaling:** Activation of visual warning (Red LED) or critical error logging in the console.

---
**Additional Notes:**
[Space for observations regarding field tests or specific hardware behavior]
