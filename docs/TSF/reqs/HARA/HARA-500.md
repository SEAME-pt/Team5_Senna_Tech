# 📑 HARA: Hazard Analysis and Risk Assessment

**Project:** PiRacer - Instrument Cluster (Qt GUI)<br>
**Scenario:** Fully Autonomous (No Human Driver) <br>
**Date:** 2026-01-07 <br>
**author:** Marcelo Fassbinder <br>
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
*Technical evaluation of instrument cluster failure modes.*

| ID | Failure Mode | Autonomous Scenario Consequence | Criticality |
| :--- | :--- | :--- | :---: |
| **H1-500** | **Incorrect information displayed** | Observers misinterpret vehicle state and system behavior. | **C1** |
| **H2-500** | **Outdated or delayed information displayed** | Observers rely on obsolete data, reducing monitoring reliability. | **C1** |
| **H3-500** | **Missing warning or status indications** | Critical vehicle conditions are not visible to observers. | **C2** |

---

## 3. Safety Goals / Expectations (EXP)
*What the system **must** do to mitigate the risks above.*

* **EXP-501 (Focus H1/H2):** The instrument cluster shall ensure that displayed vehicle information
  represents the current system state within an acceptable time window
  and shall safely handle invalid, missing, or out-of-range data
  without causing application failure or undefined behavior.
* **EXP-502 (Focus H3):** The instrument cluster shall present warning and status indications
  whenever critical vehicle conditions are detected, ensuring observer awareness.

---

**Additional Notes:**
Since the instrument cluster does not influence vehicle actuation and is used only for observation and monitoring, hazards are mainly related to loss of situational awareness and reduced reliability of system validation, rather than direct vehicle control.
