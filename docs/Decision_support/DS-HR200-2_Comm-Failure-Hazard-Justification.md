# Evidence for HARA-200: Justification for the Communication Failure Hazard

**ID:** DS-HR200-2
**Date:** 2026-01-08
**Author:** Gemini and Hellom Mendes
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Hazard H1-200 (I²C Communication Failure)

---

## 1. Decision

Hazard `H1-200` (I²C Communication Failure), manifested by events such as **NACK (Not Acknowledged)** and **Timeout**, is considered a credible and relevant threat to the system's safety analysis.

## 2. Justification and Scenarios

I²C communication can fail in such a way that data transmission is completely interrupted or never successfully completed **[3]**. These events, if not handled, can lead the system to operate without updated speed data, resulting in dangerous behavior.

### Relevant Scenarios for Hazard Occurrence

*   **NACK (Not Acknowledged):**
    *   **Description:** Occurs when the master device (STM32) does not receive an acknowledgment signal from the slave (sensor) after sending an address or a data byte. It is an explicit indication that the slave is not ready, does not exist, or did not understand the communication **[1]**.
    *   **Common Scenarios:**
        *   **Invalid Address:** The master attempts to communicate with an I²C address that does not correspond to any device on the bus.
        *   **Slave Busy:** The sensor is performing an internal operation (e.g., a measurement) and is not yet ready to respond.
        *   **Slave Failure:** The sensor has crashed or is in an error state and cannot respond.

*   **Timeout:**
    *   **Description:** Occurs when the I²C bus remains stuck in a state for a period longer than expected, paralyzing communication **[2]**.
    *   **Common Scenarios:**
        *   **"Clock Stretching" Indefinite:** A slave may hold the clock line (SCL) low to indicate it needs more time. If it never releases the line due to an internal error, the bus hangs, and the master experiences a timeout.
        *   **No Response:** The master waits for a response (a bit, a byte) that never arrives, and a software or hardware watchdog triggers a timeout error.

## 3. Conclusion

Given that NACK and Timeout events are documented and expected failure modes of the I²C protocol, hazard `H1-200` is considered **relevant** and **credible**, requiring robust mitigations in the driver to detect and handle these failures (to be detailed in a separate document).

---

## Reviewer Note

Please find authoritative external references to justify the **NACK** and **Timeout** failure scenarios on the I²C bus, as well as a general reference justifying communication failure as a known risk for the protocol. Add the corresponding links in the "4. References" section below.

## 4. References

**[1] (To be filled):** An I²C protocol specification or application note describing the **conditions that cause a NACK**.

**[2] (To be filled):** An application note or design guide explaining the phenomenon of **"clock stretching" and timeouts** in I²C.

**[3] (To be filled):** A general reference (e.g., textbook) that establishes **communication failure as a known risk** for the I²C protocol.