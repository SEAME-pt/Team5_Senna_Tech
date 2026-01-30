# Evidence for HARA-200: Justification for Incorrect Pulse Reading Hazard

**ID:** DS-HR200-2
**Date:** 2026-01-08
**Author:** Hellom with Gemini
**Reviewer:** Hellom Mendes
**Relates to:** HARA-200, Hazards H2-200 & H3-200 (Incorrect Pulse Reading)

---

## 1. Decision

The hazards `H2-200` (Erratic High Value) and `H3-200` (Erratic Low Value), caused by incorrect pulse readings (e.g., electrical noise or bouncing), are considered credible and relevant threats to the system's safety analysis.

## 2. Justification and Scenarios

Incorrect pulse readings are a known risk in embedded systems, especially when dealing with electromechanical sensors in noisy environments **[4]**. These issues can lead to "false" pulses (erratic high value) or "missing" pulses (erratic low value), resulting in erroneous and potentially dangerous speed calculations.

### Relevant Scenarios for Hazard Occurrence

*   **Electrical Noise / Electromagnetic Interference (EMI):**
    *   **Cause:** Electric motors, power converters, and other high-current components generate electromagnetic fields that can induce spurious electrical signals (noise) on the sensor's pulse line **[1]**.
    *   **Effect:** Noise can be misinterpreted as additional pulses, leading to an artificially high-speed reading (Erratic High Value).

*   **Sensor Bouncing / Multiple Transitions:**
    *   **Cause:** Physical imperfections or vibrations in the sensor mechanism can cause the signal to "bounce" (rapidly switch between high and low multiple times) during a single intended pulse event **[2]**.
    *   **Effect:** A single actual rotation can be registered as multiple pulses, leading to an exaggerated high-speed reading (Erratic High Value).

*   **Signal Integrity Issues (Weak/Degraded Signal):**
    *   **Cause:** The quality of the pulse signal can be degraded by factors such as long or unshielded wires, improper impedance matching, or insufficient voltage levels from the sensor **[3]**.
    *   **Effect:** A weak or distorted pulse might not be reliably detected by the STM32's input, leading to missed pulses and an artificially low-speed reading (Erratic Low Value).

*   **Power Supply Fluctuations (affecting sensor/STM32 input):**
    *   **Cause:** Variations or noise on the power supply voltage for the sensor or the STM32's input pin can affect the threshold at which a pulse is detected.
    *   **Effect:** Fluctuations can cause a single pulse to be missed or incorrectly interpreted, leading to an erratic speed reading.

## 3. Conclusion

Considering that the PiRacer's operating environment includes significant sources of electrical noise and that pulse sensors can exhibit bouncing, the hazard of incorrect pulse readings is considered **relevant** and **credible**, requiring robust signal conditioning and filtering mitigation (to be detailed in a separate document).

---

## Reviewer Note

All references have been validated. The GM and Chrysler recalls provide concrete evidence that both erratic high and low speed signals lead to hazardous safety system failures (unintended braking and disabled stability control) in the field. Combined with the TI technical justification for EMI-induced ghost pulses and the ISO 26262 normative framework for data corruption, the H2 and H3 hazards are confirmed as C4 critical.

## 4. References

**[1] Texas Instruments (TI) Tech Note AN-118:** *"Hall-Effect Sensor Ghost Pulses from PWM Noise"*. This technical reference explains how PWM switching in motors induces electrical noise that can be misinterpreted as valid sensor pulses, specifically in Hall Effect applications.

**[2] NHTSA Safety Recall 05V379000 - General Motors:** This recall documents cases where erratic wheel speed sensor signals (due to corrosion/debris) caused unintended ABS activations at low speeds, increasing stopping distances and demonstrating the danger of corrupted speed data.

**[3] NHTSA Safety Recall 16V913000 - Fiat Chrysler:** This recall highlights how signal degradation and intermittent connectivity in wheel speed sensor circuits can disable critical safety systems (like Electronic Stability Control), proving the danger of "missing" pulses and erratic low-speed readings.

**[4] ISO 26262-6:2018 - Annex D.2.3.2 (Information exchange - Corruption of information):** This international standard explicitly identifies information corruption as a fundamental failure mode in safety-critical systems. It mandates that systems must be designed to detect and mitigate corrupted data to prevent unintended and hazardous behaviors.
