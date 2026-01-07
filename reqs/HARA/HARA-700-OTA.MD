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
*Technical evaluation of sensor failure modes.*

| ID | Failure | Autonomous Scenario Consequence | Criticality |
| :--- | :--- | :--- | :---: |
| **H1-OTA-700** | **Rollback Mecanism not available or not functional** | The update process fails (e.g., power loss or connectivity failure) and the vehicle is operated without a functional Instrument Cluster, resulting in the absence or corruption of critical driver information | **C2** |
| **H2-OTA-700** | **OTA update during vehicle operation.** | The vehicle is in motion and the system automatically initiates or applies an OTA update, potentially causing the loss of critical vehicle information for a specific period | **C2** |
| **H3-OTA-700** | **New version corrupted or modified** | Software integrity failure in the cluster may result in missing or altered display of critical vehicle data | **C2** |

---

## 3. Safety Goals (SG) / EXPECTATIONS
*What the system **must** do to mitigate the risks above.*

* **EXP-703 (Focus H1/H2):** The instrument cluster shall be be updated at appropriate times and in accordance with security standards, ensuring the integrity of the data displayed in the vehicle.
* **EXP-704 (Focus H3):** All updates must ensure that they are secure and not corrupted or adultered.


---
**Additional Notes:**
- 
