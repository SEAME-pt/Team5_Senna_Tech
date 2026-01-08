# Evidence for HARA-200: Justification for the Data Corruption Hazard

**ID:** DS-HR200-3
**Date:** 2026-01-08
**Author:** Gemini and Hellom Mendes
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Hazards H2-200 & H3-200 (Corrupted I²C Data)

---

## 1. Decision

The hazards `H2-200` (Erratic High Value) and `H3-200` (Erratic Low Value), caused by corrupted data during I²C transmission, are considered credible and relevant threats to the system's safety analysis.

## 2. Justification and Scenarios

Data corruption on an I²C bus is a known risk in embedded systems **[4]**. Data transmission can be affected by various factors, resulting in "bit-flips" that alter the information without necessarily halting communication. If undetected, this corrupted data is accepted by the microcontroller as valid, leading to erroneous and potentially dangerous speed readings.

### Relevant Scenarios for Hazard Occurrence

*   **Electromagnetic Interference (EMI):** This is the most likely scenario on the PiRacer.
    *   **Cause:** Electric motors, power converters, and other high-current components generate electromagnetic fields that can induce noise and glitches on the I²C bus data (SDA) and clock (SCL) lines **[1]**.
    *   **Effect:** A glitch can cause a `0` bit to be read as a `1` or vice-versa, corrupting the speed value (e.g., `0x0A` (10) becomes `0x8A` (138)).

*   **Bus Signal Integrity Issues:**
    *   **Cause:** The quality of the electrical signal on the bus can be degraded by physical characteristics such as long PCB traces, improper pull-up resistor values, or excessive bus capacitance **[2]**.
    *   **Effect:** Degraded signals (with slow rise/fall times) are more susceptible to misinterpretation by devices, resulting in incorrect bit readings.

*   **Power Supply Fluctuations:**
    *   **Cause:** Variations or noise on the power supply voltage for the sensor or microcontroller can affect the logic level references (what is considered a `0` and a `1`), leading to misinterpretation of data **[3]**.
    *   **Effect:** A bit can be read incorrectly due to instability in the voltage reference.

## 3. Conclusion

Given that the PiRacer's operating environment includes significant sources of EMI and that the physical integrity of the bus cannot be guaranteed to be perfect, the hazard of data corruption is considered **relevant** and **credible**, requiring robust error detection mitigation (to be detailed in a separate document).

---

## Reviewer Note

Please review Section "2. Justification and Scenarios" and find authoritative external references for the causes of I²C data corruption. Add the links corresponding to the descriptions in the "4. References" section below.

## 4. References

**[1] (To be filled):** An application note or technical article explaining the effect of **EMI from motors** on signal buses like I²C.

**[2] (To be filled):** A design guide or application note discussing **I²C signal integrity**, pull-up resistors, and bus capacitance.

**[3] (To be filled):** A technical document explaining the impact of **power supply noise** on digital communication logic levels.

**[4] (To be filled):** A general reference (e.g., textbook, industry report) on **known risks of data corruption in embedded systems on I²C bus**.