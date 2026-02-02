# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - Autonomous Control Stack <br>
**Subsystem:** RTOS Scheduling, Inter-task Communication, Timing <br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** 2026-01-07 <br>
**author:** Nicole Oliveira <br>
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

| ID            | Failure Mode       | RTOS Failure Description                                              | Autonomous Scenario Consequence                   | Criticality |
| :------------ | :----------------- | :-------------------------------------------------------------------- | :------------------------------------------------ | :---------: |
| **H1-300** | Task Starvation    | Speed sensor task not scheduled due to priority misconfiguration      | Speed defaults to 0 km/h → motor overcompensation |    **C4**   |
| **H2-300** | Priority Inversion | High-priority control task blocked by low-priority task holding mutex | Delayed braking or steering response              |    **C4**   |
| **H3-300** | Missed Deadline    | Sensor task executes too late due to CPU overload                     | Stale speed data used for control decisions       |    **C3**   |
| **H4-300** | Queue Overrun      | Speed samples overwritten before consumption                          | Erratic or inconsistent speed readings            |    **C3**   |
| **H5-300** | Race Condition     | Unsynchronized access to shared speed buffer                          | Sporadic high or low speed spikes                 |    **C4**   |
| **H6-300** | Time Base Drift    | RTOS tick misconfiguration                                            | Invalid timestamping → data freshness lost        |    **C2**   |


---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-300 (Focus H1/H3):** The RTOS shall guarantee periodic execution of the speed sensor task within its defined deadline.
* **SG-301 (Focus H3/H6):** The RTOS shall ensure that every speed sample includes a monotonic timestamp and is invalidated if stale.
* **SG-302 (Focus H5):** The RTOS shall enforce exclusive access to shared speed data using deterministic synchronization primitives.
* **SG-303 (Focus H4):** The RTOS shall detect and report queue overflows and lost messages in inter-task communication.
* **SG-304 (Focus H2):** The RTOS configuration shall prevent unbounded priority inversion for safety-critical tasks.
---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

* **Primary Action:** Immediate interruption of motor PWM signals (Coast/Brake).
* **Signaling:** Activation of visual warning (Red LED) or critical error logging in the console.

---
**Additional Notes:**
In an autonomous system, the RTOS is part of the safety boundary.
A correctly implemented algorithm running on an unreliable scheduler is not safe.