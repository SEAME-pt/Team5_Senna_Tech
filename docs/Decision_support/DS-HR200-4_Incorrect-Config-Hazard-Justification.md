# Evidence for HARA-200: Justification for Pulse Counting Logic Failure Hazard

**ID:** DS-HR200-4
**Date:** 2026-01-08
**Author:** Hellom with Gemini
**Reviewer:** Hellom Mendes
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

All references have been validated. The Ariane 5 case proves the catastrophic danger of overflow in velocity-related calculations, while the Mars Climate Orbiter case perfectly illustrates how unit conversion/constant errors can lead to total mission loss. MISRA and ISO guidelines provide the necessary normative support for ensuring arithmetic integrity.

## 4. References

**[1] ESA Ariane 5 Flight 501 Inquiry Board Report (1996):** This classic failure analysis documents how an unhandled integer overflow in the navigation system's velocity calculation led to the destruction of the rocket, providing definitive proof of the danger of H5-200.

**[2] NASA Mars Climate Orbiter Mishap Investigation Board Report (1999):** This report details how a failure to use consistent conversion constants (metric vs. English units) led to the loss of the spacecraft, validating the criticality of semantic and mathematical correctness in sensor data.

**[3] MISRA C:2012 - Guidelines for the Use of Floating-Point Types:** Provides essential technical rules for handling non-integer arithmetic in critical systems, highlighting the risks of precision loss and comparison errors in embedded environments.

**[4] ISO 26262-6:2018 - Annex D.2.3 (Information exchange - Integrity):** This international standard defines the normative requirements for ensuring that information remains semantically correct and unaltered during system processing and exchange.