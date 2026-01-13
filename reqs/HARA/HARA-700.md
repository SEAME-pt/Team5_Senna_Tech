# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - OTA<br>
**Subsystem:** OTA updates management (instrument cluster, STM32)<br>
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
| **H1-OTA-700** | **OTA update during vehicle operation.** | The vehicle is in motion and the system automatically initiates or applies an OTA update, potentially causing the loss of critical vehicle information for a specific period | **C1** |
| **H2-OTA-700** | **Rollback Mecanism not available or not functional** | The update process fails (e.g., power loss or connectivity failure) and the vehicle is operated without a functional Instrument Cluster, resulting in the absence or corruption of critical driver information | **C1** |
| **H3-OTA-700** | **New version corrupted or modified** | Software integrity failure in the cluster may result in missing or altered display of critical vehicle data | **C1** |

---

## 3. Safety Goals (SG) / EXPECTATIONS
*What the system **must** do to mitigate the risks above.*

* **EXP-700 (Focus H1):** The instrument cluster shall be be updated at appropriate times
* **EXP-701 (Focus H2/H3):** All updates must ensure that they are secure and not corrupted or adultered.
---

## 4. Safe State Strategy
*Automatic action triggered when OTA is not correct*

* **Action:** Do not run the new cluster software while the vehicle is in operation.
* **Action:** Always verify the integrity of the new files installed on the system.
* **Action:** Ensure that rollback mechanisms works in case the new version is not safe or the update process is interrupted.


---
**Additional Notes:**
- 
