# Evidence for HARA-200: Mitigation for Plausibility Check (SG-207)

**ID:** DM-HR200-5
**Date:** 2026-01-09
**Author:** Hellom with Gemini
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Safety Goal SG-207

---

## 1. Decision

To mitigate the sensor degradation or physical failure hazard (`H6-200`), Safety Goal `SG-207` will be implemented through a **Cross-Plausibility Check** mechanism, comparing pulse sensor data with the speed estimate derived from the **Inertial Measurement Unit (IMU)**.

## 2. Mitigation Strategy Justification

Pulse sensors can suffer failures where they continue to send data, but inaccurately (drift, stuck values, or offset). Without a secondary source, the system would have no way of knowing if the read speed is real. Using redundant information from different sensors (sensor diversity) is a standard technique for detecting common-mode failures and signal degradation **[1]**. The IMU provides an independent source of acceleration data that can be integrated to validate the speed sensor reading **[2]**.

### Implementation Strategy

1.  **IMU-Based Estimation:**
    *   **Description:** The system will use the IMU's longitudinal accelerometer data to calculate an estimate of the speed variation ($\Delta v = a \cdot \Delta t$).
    *   **Justification:** Provides an independent data channel that does not rely on the physical mechanism of the pulse sensor (wheels/axle).

2.  **Comparison Monitor (Discrepancy Monitor):**
    *   **Description:** An algorithm will compare, in real-time, the pulse sensor speed with the IMU estimate. If the difference between the two exceeds a defined error threshold (e.g., > 15%) for a continuous period (e.g., > 300ms), a plausibility fault is signaled.
    *   **Justification:** Model-based consistency algorithms or redundant sensors are required to identify failures that do not generate obvious electrical errors (like short circuits) but rather information content errors **[3]**.

3.  **Safety Action:**
    *   **Description:** Upon detecting a plausibility fault, the system must assume the speed data is no longer reliable and transition to the **Fail-Safe State** or, at a minimum, to a **Degraded Mode** with severely limited speed.

## 3. Conclusion

Cross-plausibility checking between the pulse sensor and the IMU provides essential analytical redundancy. This ensures that gradual failures or physical degradations that do not completely interrupt the signal are still detected before causing dangerous control decisions.

---

## Reviewer Note

Evaluate if error accumulation in IMU integration (drift) can cause false positives on long trips and if a Kalman filter or similar sensor fusion technique should be formally required.

## 4. References

**[1] (To be filled):** Functional safety standard reference (e.g., ISO 26262-6, Table D.1) on the use of "Plausibility Check" or "Sensor Diversity" as a failure detection mechanism.

**[2] (To be filled):** Technical document or Application Note describing the physics of integrating IMU data (accelerometer) for vehicle speed estimation.

**[3] (To be filled):** Academic or industrial reference on fault diagnosis methods in sensors via residual generation/comparison.
