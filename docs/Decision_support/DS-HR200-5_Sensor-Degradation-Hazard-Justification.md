# Evidence for HARA-200: Justification for the Sensor Degradation/Physical Failure Hazard

**ID:** DS-HR200-5
**Date:** 2026-01-08
**Author:** Hellom Mendes with Gemini
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Hazard H6-200 (Sensor Degradation / Physical Failure)

---

## 1. Decision

Hazard `H6-200`, describing the system operating with physically inaccurate data due to **sensor degradation or physical failure**, is considered a credible and relevant threat to the system's safety analysis.

## 2. Justification and Scenarios

A sensor, like any physical component, is subject to degradation and failure over time or due to environmental stress. Unlike communication failures or data corruption, here the problem lies in the physical measurement itself, resulting in data that is protocol-wise and semantically valid, but physically incorrect **[3]**.

### Relevant Scenarios for Hazard Occurrence

*   **Sensor Drift or Offset:**
    *   **Cause:** Over time, with continuous use, temperature variations, vibration, or aging of components, the sensor's internal calibration can change. This causes the sensor to start reporting values slightly higher or lower than the actual quantity it is measuring **[1]**.
    *   **Effect:** The system receives consistent and CRC-valid data, but it contains a systematic error. If the drift is, for example, 2 m/s, the system will always think it is moving 2 m/s faster or slower than reality, leading to navigation or speed control errors.

*   **Stuck-at-Value Data:**
    *   **Cause:** An internal sensor failure (hardware or firmware) can cause it to stop updating its readings, reporting the last valid value indefinitely or a fixed value (e.g., 0 km/h or 255 km/h) **[2]**.
    *   **Effect:** The control system operates as if the speed is not changing, leading to an inadequate response to the actual conditions of the environment, which can be extremely dangerous.

*   **Increased Reading Noise:**
    *   **Cause:** Internal sensor components can degrade, leading to an increase in the intrinsic noise of the measurement.
    *   **Effect:** The system receives speed readings that fluctuate excessively, making it difficult for the controller to determine the actual speed and causing instability.

## 3. Conclusion

Considering that the physical degradation and failure of sensors are expected events in the life cycle of electronic components in harsh operating environments (like the PiRacer), hazard `H6-200` is considered **relevant** and **credible**. This requires the system to implement plausibility or redundancy checks to validate the physical accuracy of the data (to be detailed in a separate document).

---

## Reviewer Note

Please find authoritative external references to justify the scenarios listed in Section 2. Add the corresponding links in the "4. References" section below.

## 4. References

**[1] (To be filled):** Look for an article or textbook on **sensors and instrumentation** discussing phenomena like **drift**, offset error, and aging in sensors.

**[2] (To be filled):** Look for a reference (e.g., hardware failure analysis, reliability report) on **sensor failure modes** resulting in **stuck-at-value readings**.

**[3] (To be filled):** Look for a general reference (e.g., textbook on sensor reliability, engineering standards) on **sensor degradation and physical failure** as known risks in embedded systems.
