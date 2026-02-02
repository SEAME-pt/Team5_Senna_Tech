# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** COVESA <br>
**Subsystem:** VSS (Vehicle Signal Specification) Data Mapping <br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** 12/01/2026 <br>
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
| **H1-400** | **Unit Mismatch (Semantic)** | VSS requires SI Units (m/s). If the software sends in km/h and the driver interprets as m/s, the car will accelerate 3.6x more than expected.| **C2** |
| **H2-400** | **Data Type Overflow** | Assigning a value that exceeds the data type defined in VSS (e.g., sending 400 for a signal that VSS defines as 0-100), causing unpredictable behavior in the parser.| **C2** |

---

## 3. Safety Goals (SG)
*What the system **must** do to mitigate the risks above.*

* **SG-400 (Focus H1):** The system must ensure that all speed and steering signals strictly follow the SI standard units defined by COVESA VSS (m/s for speed, degrees for angles).
* **SG-401 (Focus H2):** Implement plausibility filters based on VSS metadata (Min/Max/Allowed values).

---

## 4. Safe State Strategy
*Automatic action triggered when sensor confidence is lost:*

* **Primary Action:** In case of receiving a signal that violates the limits defined in the VSS contract (e.g., steering angle outside the range defined in .vspec), the command must be discarded (reproduces what a middleware would do).

* **Validation:** Before any maneuver, the system must validate whether the "Target Value" is within the VSS specification.

---
**Additional Notes:**
[Space for observations regarding field tests or specific hardware behavior]
