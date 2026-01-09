# Evidence for HARA-200: Justification for Pulse Counting Logic Failure Hazard

**ID:** DS-HR200-4
**Date:** 2026-01-08
**Author:** Hellom with Gemini
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Hazard H5-200 (Pulse Counting Logic Failure)

---

## 1. Decision

Hazard `H5-200`, describing system operation with semantically or mathematically incorrect data due to **pulse counting and calculation logic failures**, is considered a credible and relevant threat to the system's safety analysis.

## 2. Justification and Scenarios

Beyond data integrity and timeliness, **semantic and mathematical correctness** is crucial. The system needs to not only correctly receive pulses but also ensure that their interpretation and calculation result in the expected speed. A failure in the counting/calculation logic can lead to data that is protocol-valid and timely, but represents an incorrect physical quantity, leading to dangerous decisions **[4]**.

### Relevant Scenarios for Hazard Occurrence

*   **Pulse Counter Overflow:**
    *   **Cause:** If the STM32's pulse counter (typically an integer variable) is not designed to handle the maximum number of pulses that can be generated (e.g., at high speed for a prolonged period), it may reach its maximum value and "wrap around" (overflow), reverting to zero or a negative value **[1]**.
    *   **Effect:** Speed calculation will be based on an incorrect pulse `delta` (due to overflow), resulting in erratic speed readings (too high or too low), leading the control system to make dangerous decisions.

*   **Incorrect Conversion Constant (Pulses to Speed):**
    *   **Cause:** A software error (e.g., an incorrectly programmed value) in the constant that converts pulse count per unit time to RPM or km/h. For instance, the "pulses per revolution" constant might be wrong **[2]**.
    *   **Effect:** The system operates based on a wrong assumption about the measurement scale, resulting in consistently incorrect speed calculations (e.g., always double or half the actual speed), leading to inadequate control.

*   **Rounding or Precision Error in Floating-Point Calculations:**
    *   **Cause:** In resource-limited embedded environments, complex floating-point calculations can introduce rounding errors if not handled carefully, especially when converting between different units or integrating over time **[3]**.
    *   **Effect:** Small precision errors can accumulate over time or at certain speed ranges, resulting in subtle but persistent deviations in speed readings that can lead to degraded or unstable control performance.

## 3. Conclusion

Considering that the correct functioning of pulse counting logic and speed calculation is a prerequisite for the accurate interpretation of its data, hazard `H5-200` is considered **relevant** and **credible**, requiring mitigation that ensures the robustness and accuracy of these calculations (to be detailed in a separate document).

---

## Reviewer Note

Please find authoritative external references to justify the scenarios listed in Section 2. Add the corresponding links in the "4. References" section below.

## 4. References

**[1] (To be filled):** A reference on **integer overflow** in embedded programming and its consequences.

**[2] (To be filled):** A design guide or application note on **calibration and conversion constants** for pulse sensors/encoders.

**[3] (To be filled):** An article or textbook on **rounding and floating-point precision** in embedded systems.

**[4] (To be filled):** A general reference (e.g., textbook, industry report) on **importance of semantic/mathematical correctness** in sensor data.