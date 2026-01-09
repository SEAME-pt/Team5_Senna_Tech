# Evidence for HARA-200: Mitigation Using Memory Isolation (MPU)

**ID:** DM-HR200-3
**Date:** 2026-01-09
**Author:** Hellom with Gemini
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Safety Goal SG-205

---

## 1. Decision

To mitigate software failure hazards that could impact the speedometer data chain, Safety Goal `SG-205` will be implemented by configuring the **Memory Protection Unit (MPU)** of the STM32U5 microcontroller.

## 2. Mitigation Strategy Justification

The pulse sensor driver, including its interrupt service routines (ISR) and speed calculation logic, is a safety-critical component. A failure in another part of the software (e.g., a buffer overflow in a communication task) must not be able to corrupt the memory, variables, or code of the sensor driver. Memory isolation is a fundamental defense against such failures **[1]**.

### Implementation Strategy

1.  **Memory Region Definition:**
    *   **Description:** A dedicated memory region will be defined to contain:
        *   The pulse sensor driver's code (including the ISR).
        *   The static and global variables used by the driver (e.g., `pulse_count`, calibration constants).
        *   The stack used by the speed calculation task (if applicable).
    *   **Justification:** Grouping these resources into a contiguous memory region allows access rules to be applied to them as a whole.

2.  **MPU Configuration:**
    *   **Description:** The STM32U5's MPU will be configured to create a sandbox for this memory region. The rules will define that:
        *   The driver's code region will be marked as Read-Only and Executable.
        *   The driver's data region will be marked as Read/Write, but access will be restricted to the driver itself (and possibly the RTOS kernel). No other application task (e.g., a logging or communication task) will have write permission to this region.
        *   Any unauthorized access attempt (e.g., a write to the code region or a write from an unprivileged task to the data region) will trigger a hardware fault (e.g., `MemManage fault`) **[2]**.

3.  **MPU Fault Handling:**
    *   **Description:** The system will implement a fault handler (`MemManage_Handler`) that is triggered by an MPU violation.
    *   **Justification:** Instead of allowing memory corruption to go unnoticed, the system can take immediate and safe action. The default action for an MPU violation will be to escalate to the **Fail-Safe State**, as defined in HARA-200.

## 3. Conclusion

The use of the MPU to isolate the pulse sensor driver provides a robust hardware barrier against a wide class of unpredictable software failures. This strategy significantly increases the integrity and reliability of the sensor data chain, directly supporting the mitigation of all identified hazards.

---

## Reviewer Note

Please find references justifying the use of the MPU as a software isolation technique to enhance safety and reliability in embedded systems.

## 4. References

**[1] (To be filled):** A reference on the **importance of memory isolation** (e.g., "freedom from interference") in safety-critical systems.

**[2] (To be filled):** The **STM32U5 reference manual** or an ARM application note detailing the configuration and fault handling of the MPU.
