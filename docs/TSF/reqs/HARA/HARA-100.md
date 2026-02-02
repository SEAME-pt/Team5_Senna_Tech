# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** CAN Communication & Control Bus <br>
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
| **H2-100** | **Data Corruption** | A faulty node sends noise continuously, blocking ESTOP (ID 0x001) from reaching the STM32. Total loss of control. | **C4** |
| **H3-100** | **Frozen Planner (Kernel Panic)** | Rasp5 freezes but CAN controller buffer keeps repeating the last "Accelerate" command. STM32 thinks system is normal and maintains speed. | **C3** |
| **H4-100** | **High Latency** | Receives steering command too late while entering a curve, resulting in path deviation/crash. | **C3** |
| **H5-100** | **Bus Congestion** | RPi or STM send too many messages, delaying critical braking messages. Vehicle reaction time increases dangerously. | **C3** |
| **H6-100** | **Incorrect ID Mapping** | Misconfigured software on RPi sends speed commands with the CAN ID reserved for steering, or vice versa. STM32 would execute the wrong action (e.g., turns wheels when it should accelerate). | **C4** |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-CAN-01 (Focus H-CAN-01/03)**: The STM32 shall implement a Watchdog Timer that triggers the Safe State if the Heartbeat message (ID 0x005) is missing for more than 500ms.

* **SG-CAN-02 (Focus H-CAN-02/05)**: The ESTOP message (ID 0x001) shall always be assigned the lowest CAN ID to guarantee arbitration priority over all other messages.

* **SG-CAN-03 (Focus H-CAN-04)**: The CAN Control Loop (Rasp5 → STM32) shall ensure end-to-end latency is less than 50ms for steering and throttle commands.

* **SG-CAN-04 (Focus H-CAN-03)**: The Rasp5 software shall run the Heartbeat sender in a dedicated thread/process, ensuring it stops transmission immediately upon OS freeze/Kernel Panic.


---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

* **Primary Action (Actuator Cutoff)**: STM32 immediately sets Motor PWM to 0 (Coast/Brake) and Steering Servo to Center/Neutral.

* **Secondary Action (State Lock)**: System enters STATE_ESTOP. Exit from this state requires a manual hardware reset or a specific "Arming Sequence" (no automatic restart).

---
**Additional Notes:**
[Space for observations regarding field tests or specific hardware behavior]
