# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - System<br>
**Subsystem:** Raspberry Pi5 Automotive Grade Linux<br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** 2026-01-07 <br>
**author:** Vinícius Vaccari<br>
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

| ID | Failure | Autonomous Scenario Consequence | Criticality |
| :--- | :--- | :--- | :---: |
| **H1-SYSTEM-600** | **Cluster initialization fails** | The vehicle is powered on and AGL initiates, but the system fails during the Qt Cluster boot process, preventing the display of critical information | **C1** |
| **H2-SYSTEM-600** | **Lack of Storage** | The system attempts to allocate memory for a critical process, but insufficient memory is available, causing crashes or process termination. | **C3** |
| **H3-SYSTEM-600** | **Raspberry Pi Overheating** | Excessive heating of the Raspberry Pi 5 may cause abrupt shutdowns, potentially corrupting files, altering data, and damaging software, leading to incorrect data being transmitted between components. | **C2** |
| **H4-SYSTEM-600** | **Applications Close Due to Power Loss or Resource Shortage** | Critical applications, including the Instrument Cluster Qt app for example, terminate unexpectedly because of insufficient power (voltage drops, brownouts) or lack of system resources (CPU, RAM, storage). | **C2** |


---

## 3. Safety Goals (SG) / EXPECTATIONS
*What the system **must** do to mitigate the risks above.*

* **EXP-600 (Focus H1):** The system (AGL on Raspberry Pi) automatically start all necessary applications. 
* **EXP-601 (Focus H2):** The system (AGL on Raspberry Pi) must be able to store all the data necessary for its operation without risk of failure due to lack of space.
* **EXP-602 (Focus H3 e H4):** The system (AGL on Raspberry Pi) is capable of monitoring critical data such as temperature and voltage to prevent abrupt shutdowns that could corrupt the file system.

---

## 4. Safe State Strategy
*Automatic action triggered when OTA is not correct*

---
**Additional Notes:**
- 
