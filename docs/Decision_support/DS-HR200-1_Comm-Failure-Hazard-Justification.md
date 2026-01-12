# Evidence for HARA-200: Justification for the Sensor Connection Failure Hazard

**ID:** DS-HR200-1
**Date:** 2026-01-08
**Author:** Hellom with Gemini
**Reviewer:** Hellom Mendes
**Relates to:** HARA-200, Hazard H1-200 (Sensor Connection Failure)

---

## 1. Decision

Hazard `H1-200` (Sensor Connection Failure), manifested by events such as a **disconnected or broken sensor cable**, is considered a credible and relevant threat to the system's safety analysis.

## 2. Justification and Scenarios

A physical connection failure of the sensor, such as a disconnected or damaged cable, will prevent sensor pulses from reaching the STM32. This can lead the system to operate without updated speed data, resulting in dangerous behavior **[1]**.

### Relevant Scenarios for Hazard Occurrence

*   **Disconnected/Damaged Sensor Cable:**
    *   **Description:** The physical conductor transmitting sensor pulses to the STM32 is broken or disconnected. This prevents pulses from reaching the microcontroller, resulting in a 0 km/h speed reading.
    *   **Common Scenarios:**
        *   **Vibration/Mechanical Shock:** Vehicle movement or impacts can loosen or physically disconnect the sensor cable.
        *   **Wear/Material Fatigue:** Over time, the cable may wear out or break due to repeated flexing or stress.
        *   **Damage During Maintenance/Assembly:** The cable may be accidentally cut or damaged during assembly or repairs.

*   **Short Circuit or Open Circuit on the Pulse Line:**
    *   **Description:** Electrical problems on the pulse line can prevent the correct transmission of pulses. A short circuit can cause the line to be constantly high or low, while an open circuit prevents any signal **[2]**.
    *   **Common Scenarios:**
        *   **Damaged Wiring:** Compromised insulation leading to short circuits with other lines or ground.
        *   **Faulty Circuit Components:** Pull-up/pull-down resistors or capacitors associated with the pulse line fail, altering signal behavior.

## 3. Conclusion

Considering that physical connection failures and electrical problems are documented and expected failure modes for sensors, hazard `H1-200` is considered **relevant** and **credible**, requiring robust software mitigations to detect the absence of pulses and ensure that the 0 km/h reading is handled safely (to be detailed in a separate document).

---

## Reviewer Note

The references have been validated. ISO 26262 theoretically confirms that the loss of control data is critical, while the GM Recall (NHTSA) proves that this specific failure (speed sensor) has already caused real-world accidents due to involuntary braking, justifying the C4 criticality classification for this hazard.

## 4. References

**[1] ISO 26262-6:2018 - Annex D.2.3 (Freedom from interference by information exchange):** Identifies **"Loss of information"** and **"Blocking of information"** as critical failure modes in the exchange between system elements (e.g., Sensor to Microcontroller). The standard states that the loss of safety-critical feedback, such as vehicle speed, compromises the system's ability to maintain a safe state (e.g., closed-loop control), leading to hazardous behaviors unless detected by specific mechanisms like timeouts or E2E protection.

**[2] NHTSA Safety Recall 19V649000 - General Motors:** This official safety recall documents how wheel speed sensor signal failures (intermittent signal loss or corruption) led to unintended braking activations in over 600,000 vehicles, providing empirical evidence of the hazardous behaviors described in this document.
