# Evidence for HARA-200: Justification for the Incorrect Configuration Hazard

**ID:** DS-HR200-5
**Date:** 2026-01-08
**Author:** Gemini and Hellom Mendes
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Hazard H5-200 (Incorrect Sensor Configuration)

---

## 1. Decision

Hazard `H5-200`, describing system operation with semantically incorrect data due to **incorrect sensor configuration**, is considered a credible and relevant threat to the system's safety analysis.

## 2. Justification and Scenarios

Beyond data integrity and timeliness, **semantic correctness** is crucial. The system needs to not only receive data correctly but also ensure it *means* what is expected. A sensor configuration failure can lead to data that is protocol-valid and timely, but represents a physical quantity different from what was expected **[4]**.

### Relevant Scenarios for Hazard Occurrence

*   **Register Write Failure (Write Failure):**
    *   **Cause:** During initialization, the STM32 driver sends I²C commands to write to internal sensor registers, defining parameters such as measurement scale or resolution. A momentary bus failure or power glitch can cause one of these write commands to fail undetected **[1]**.
    *   **Effect:** The sensor may continue operating with a default or previous configuration. If the default configuration is, for example, "0 to 10 m/s scale" and the system expected "0 to 40 m/s scale," all readings above 10 m/s will be reported incorrectly (e.g., may "saturate" at the maximum value), leading the control system to make dangerous decisions.

*   **Use of Incorrect Default Settings:**
    *   **Cause:** The driver software might assume that the sensor's power-on default configuration state is different from the actual state defined by the manufacturer **[2]**.
    *   **Effect:** The system operates based on a wrong assumption about the data's scale or unit, resulting in incorrect speed calculations.

*   **Sensor Non-Volatile Memory Corruption:**
    *   **Cause:** In some sensors, calibration or configuration settings are stored in internal non-volatile memory (e.g., EEPROM). Electrical stress events or memory end-of-life could corrupt these stored values **[3]**.
    *   **Effect:** The sensor powers on and loads a corrupted configuration, operating in a semantically incorrect way from the start.

## 3. Conclusion

Given that sensor configuration is a prerequisite for the correct interpretation of its data and that register write failures are a known risk in bus communication, hazard `H5-200` is considered **relevant** and **credible**, requiring mitigation that actively verifies successful configuration (to be detailed in a separate document).

---

## Reviewer Note

Please find authoritative external references to justify the scenarios listed in Section 2. Add the corresponding links in the "4. References" section below.

## 4. References

**[1] (To be filled):** Look for an application note or article discussing the importance of **"read-after-write" verification** to ensure correct peripheral configuration over buses like I²C or SPI.

**[2] (To be filled):** Look for an **example datasheet** that highlights default register values that differ from operational values, justifying the need for explicit configuration.

**[3] (To be filled):** Look for a reference (e.g., article on memory reliability) detailing **non-volatile memory (e.g., EEPROM) corruption** as a potential failure mode in embedded sensors.

**[4] (To be filled):** Look for a general reference (e.g., textbook on embedded systems, sensor integration guide) on the **importance of correct sensor configuration** for data interpretation and system safety.
