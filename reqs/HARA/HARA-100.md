# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** CAN Communication Analysis <br>
**Subsystem:** CAN Bus Interface (STM32 ↔ RPi 5 AGL) <br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** 07/01/2026 <br>
**Author:** Yasmine Macedo <br>
**Reviewer:** [Reviewer Name] <br>

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
| **H1-100** | **Total Loss of Comm (Bus Off)** | RPi 5 stops receiving telemetry or STM32 stops receiving steering/speed commands. If the STM does not have fail-safe, the car maintains the last received speed until collision.| **C4** |
| **H2-100** | **Data Corruption (Payload Error)** | If values are not converted correctly, the read information will be wrong. A float conversion error or an Endianness error between STM32 and RPi can cause a command of "2% power" to be read as "100%", causing sudden acceleration. | **C4** |
| **H3-100** | **High Latency** | Delay in processing brake commands, increasing stopping distance for obstacles. | **C3** |
| **H4-100** | **Stale Data** | The STM32 continues executing an old command from RPi 5 because it did not detect that the message was not updated. | **C3** |
| **H5-100** | **Bus Congestion** | RPi or STM send too many messages, delaying critical braking messages. Vehicle reaction time increases dangerously. | **C3** |
| **H6-100** | **Incorrect ID Mapping** | Misconfigured software on RPi sends speed commands with the CAN ID reserved for steering, or vice versa. STM32 would execute the wrong action (e.g., turns wheels when it should accelerate). | **C4** |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-100 (Focus H1/H4):** The system must ensure that the vehicle enters a safe stopped state if CAN communication is lost or if control data "freezes".
* **SG-101 (Focus H2):** The system must validate the integrity of each control message (steering/speed) before execution to prevent actions caused by data corruption.
* **SG-102 (Focus H3/H5):** The system must guarantee a deterministic response time for braking and steering commands, limiting maximum processing delay.
* **SG-103 (Focus H2):** The system must prevent the execution of commands that violate the physical limits of acceleration and steering of the prototype (Plausibility Check).
* **SG-104 (Focus H6):** The system must validate the origin (CAN ID) and content of each message before execution, ensuring that steering and speed commands are processed only from the correct and expected IDs.


---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

* **Primary Action:** Emergency Stop (E-Stop)
Trigger: Immediate trigger by H1-100, H2-100 (fatal error) and H4-100 (timeout expired).

STM32 side: Immediate PWM signal cut to motors (Coast or Active Braking, depending on ESC hardware configuration) and automatic centering of steering servo (Neutral Position).

RPi 5 side: High-level control software must suspend sending new trajectories and enter diagnostic mode.

* **Secondary Action:** Degraded Mode (Limp Home / Safe Stop)
Trigger: Triggered by H3-100 (High Latency) or H5-100 (Bus Congestion).

Reduced Speed: The system limits maximum speed to 10% of nominal to ensure that reaction time (latency) is sufficient to avoid collisions.

Message Rejection: Corrupted messages (H2-100) or out-of-sequence messages (H4-100) are discarded. The system maintains the last valid command for only 1 cycle. If the error persists in the next cycle, it escalates to Primary Action.

* **Signaling & Logging**
Digital: Immediate recording of an ERROR_LOG in the AGL system containing the failure ID (e.g., CAN_BUS_OFF_ERR) and the last valid timestamp.

---
**Additional Notes:**
[Space for observations regarding field tests or specific hardware behavior]
