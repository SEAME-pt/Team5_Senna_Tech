# Evidence for HARA-200: Justification for Incorrect Pulse Reading Hazard

**ID:** DS-HR200-2
**Date:** 2026-01-08
**Author:** Hellom with Gemini
**Reviewer:** [Pending Human Review]
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

Please find authoritative external references to justify incorrect pulse readings, electrical noise, sensor bouncing, and signal integrity issues as known risks for pulse sensors in embedded systems. Add the corresponding links in the "4. References" section below.

## 4. References

**[1] (To be filled):** A reference on **electrical noise and EMI effects** on digital signals and sensors.

**[2] (To be filled):** A reference explaining **switch bouncing or sensor signal bouncing** and its mitigation.

**[3] (To be filled):** A design guide or application note discussing **signal integrity** for pulse inputs.

**[4] (To be filled):** A general reference (e.g., textbook, industry report) on **known risks of incorrect sensor readings in embedded systems**.
