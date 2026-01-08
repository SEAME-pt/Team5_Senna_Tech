# Evidence for HARA-200: Justification for the Stale Data Hazard

**ID:** DS-HR200-4
**Date:** 2026-01-08
**Author:** Gemini and Hellom Mendes
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Hazard H4-200 (Stale I²C Data / Latency)

---

## 1. Decision

Hazard `H4-200`, describing system instability caused by **stale data** or **high latency** in sensor readings, is considered a credible and relevant threat to the system's safety analysis.

## 2. Justification and Scenarios

In a real-time control system like the PiRacer, the "age" of sensor data is as important as its correctness. "Stale data" refers to information that, while correct at the moment it was measured, no longer represents the current state of the system when used. Using stale data in a fast control loop leads to decisions based on a past reality, causing instability **[3]**.

### Relevant Scenarios for Hazard Occurrence

*   **I²C Bus Communication Delays:**
    *   **Cause:** The I²C bus can become slow due to high capacitance, or a device may use "clock stretching" to pause communication. If this pause is long, but not long enough to trigger a timeout, data delivery will be delayed **[1]**.
    *   **Effect:** The motor control loop may run several times before receiving a new speed reading, causing it to act based on an old speed.

*   **Low Sensor Sampling Frequency:**
    *   **Cause:** The sensor itself may have an internal limitation on how quickly it can perform a new measurement. If the sensor's sampling frequency is significantly slower than the system's control loop frequency, the data will be inherently stale **[4]**.
    *   **Effect:** The system reads the same speed value repeatedly for several cycles, even if the robot's actual speed has already changed, leading to a delayed control response.

*   **Software Scheduling Delays:**
    *   **Cause:** In a system with an RTOS, the task responsible for reading the sensor may not receive CPU time as often as needed if other higher-priority tasks are occupying the processor **[2]**.
    *   **Effect:** Even if the sensor and I²C bus are fast, software scheduling delays cause the effective reading to be postponed, resulting in stale data being used by the controller.

## 3. Conclusion

Latency is an inevitable factor in any digital system. In the context of an agile robot like the PiRacer, where the system's state changes rapidly, the hazard that latency (whether from hardware or software) becomes large enough to cause control instability (`H4-200`) is **relevant** and **credible**. Therefore, robust mitigations are necessary to detect and react to stale data (to be detailed in a separate document).

---

## Reviewer Note

Please find authoritative external references for the following points. Add the corresponding links in the "4. References" section below.

## 4. References

**[1] (To be filled):** An application note on the **effects of latency and "clock stretching"** on the response time of an I²C bus.

**[2] (To be filled):** An article or textbook on real-time systems that discusses **scheduling delays** as a source of latency in control systems.

**[3] (To be filled):** An article on control theory or robotics that explains how **"stale data" causes instability** in real-time control loops.

**[4] (To be filled):** The **datasheet of the chosen speedometer sensor**, which specifies its maximum sampling frequency or measurement conversion time.
