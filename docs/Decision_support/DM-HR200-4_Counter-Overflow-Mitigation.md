# Evidence for HARA-200: Mitigation for Pulse Counter Overflow (SG-206)

**ID:** DM-HR200-4
**Date:** 2026-01-09
**Author:** Hellom with Gemini
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Safety Goal SG-206

---

## 1. Decision

To mitigate the counting logic failure hazard (`H5-200`), specifically variable overflow, Safety Goal `SG-206` will be implemented using **64-bit** variable types for accumulation and hardware wrap-around handling logic.

## 2. Mitigation Strategy Justification

Counter variable overflow is a latent risk in odometry systems. If a 16 or 32-bit counter reaches its maximum value and rolls over to zero, the pulse difference calculation can result in erroneous values, leading to incorrect speed calculations and dangerous motor behavior. Critical software standards explicitly require preventing wraparound errors in safety-related calculations to ensure predictable behavior **[1]**.

### Implementation Strategy

1.  **Use of uint64_t for Long-Term Accumulation:**
    *   **Description:** The global variable storing the total pulses since initialization will be a `uint64_t`.
    *   **Justification:** Practically impossible to overflow under normal operating conditions (would take centuries even at MHz frequencies). Using adequate data types to prevent overflow is a primary defensive programming technique **[2]**.

2.  **Hardware Timer Overflow Handling:**
    *   **Description:** If the STM32 hardware uses a 16/32-bit counter, the driver logic will detect when the current value is smaller than the previous one (indicating a wrap-around) and compensate for the difference by adding the counter's maximum value.
    *   **Justification:** Ensures that the instantaneous speed calculation remains accurate in every reading cycle, regardless of the hardware register state.

3.  **Output Data Sanity:**
    *   **Description:** The final calculated speed value will be software-limited to a plausible "Physical Maximum" for the PiRacer.
    *   **Justification:** Serves as a last line of defense in case of any unforeseen calculation error.

## 3. Conclusion

The combination of high-capacity variables (64-bit) with hardware compensation logic eliminates the risk of overflow errors, ensuring the integrity of speed data provided to the control system.

---

## Reviewer Note

Verify if the STM32U5 ARM Cortex-M33 architecture handles 64-bit operations natively or if the software overhead for these operations is acceptable at the defined sampling frequency.

## 4. References

**[1] (To be filled):** Coding standard guideline (e.g., MISRA C:2012, Rule 10.x or CERT C INT30-C) stating that unsigned integer wraparound should be avoided or explicitly handled in critical logic.

**[2] (To be filled):** Reference regarding defensive programming best practices for variable sizing in long-running embedded systems.
