# Evidence for HARA-200: Mitigation Analysis for Communication Failure

**ID:** DS-HR200-7
**Date:** 2026-01-08
**Author:** Gemini and Hellom Mendes
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Safety Goal SG-201 (Focus H1-200)

---

## 1. Decision

To mitigate hazard `H1-200` (I²C Communication Failure), safety goal `SG-201` ("The I2C driver shall report communication failure in real-time (e.g., NACK, Timeout)") will be implemented through a robust I²C driver that detects and reacts to NACK and Timeout failures.

## 2. Mitigation Solution Analysis

The mitigation strategy relies on two fronts: fault detection and a recovery protocol.

### 2.1 NACK Detection (Not Acknowledged)

The I²C driver must monitor the ACK/NACK bit after each transmitted byte.

*   **Implementation:** The STM32U5's I²C peripheral has status flags (e.g., `I2C_FLAG_NACKF`) that are set by hardware when a NACK is received. The driver must check this flag **[1]**.
*   **Handling Logic:**
    1.  Upon detecting an unexpected NACK (e.g., after an address or during a data write), the driver should immediately stop the current transaction by sending a STOP condition on the bus.
    2.  The driver should report the failure to the application layer with a specific error code (e.g., `I2C_ERROR_NACK`).
    3.  The application layer can then decide whether to retry (in case of a busy slave) or enter a safe state (in case of a device not found).

### 2.2 Timeout Detection

The driver must be able to detect if the I²C bus is stalled.

*   **Implementation:** The most robust approach combines hardware and software.
    *   **Hardware Timeout:** The STM32U5's I²C peripheral includes a timeout mechanism that can detect when the SCL line is held low for an excessive time ("indefinite clock stretching"). This feature must be enabled and configured **[2]**.
    *   **Software Timeout (Watchdog):** A software timer can be implemented in the driver layer to monitor the total duration of an I²C transaction. If the complete transaction takes longer than an expected limit, a failure is assumed.
*   **Handling Logic:**
    1.  Upon detecting a timeout (either hardware or software), the first action should be to attempt a reset of the STM32's I²C peripheral to try and release the bus.
    2.  If the peripheral reset does not resolve the issue (the bus remains stalled), the failure must be escalated to a higher system level.
    3.  The application layer, upon receiving a timeout error, should trigger entry into the **Fail-Safe State**, as defined in `HARA-200.md`.

## 3. Conclusion

The combination of NACK detection and multiple timeout mechanisms (hardware and software) provides robust coverage for Safety Goal `SG-201`, ensuring that communication failures are detected and handled in real-time.

---

## Reviewer Note

Please find references in the STM32U5 reference manual to confirm the hardware features mentioned.

## 4. References

**[1] (To be filled):** Look for the **STM32U5 Reference Manual (RM0456)**, in the I²C peripheral section, to find the description of the **NACK status flag (NACKF)**.

**[2] (To be filled):** Look for the **STM32U5 Reference Manual (RM0456)**, in the I²C peripheral section, to find the description of the **hardware timeout configuration registers**.
