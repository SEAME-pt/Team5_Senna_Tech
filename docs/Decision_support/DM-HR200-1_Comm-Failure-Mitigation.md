# Evidence for HARA-200: Mitigation for Sensor Connection Failure (SG-201)

**ID:** DM-HR200-1
**Date:** 2026-01-09
**Author:** Hellom with Gemini
**Reviewer:** [Pending Human Review]
**Relates to:** HARA-200, Safety Goal SG-201

---

## 1. Decision

To mitigate the sensor connection failure hazard (`H1-200`), Safety Goal `SG-201` will be implemented through a **pulse timeout detection** mechanism in the sensor driver logic.

## 2. Mitigation Strategy Justification

When the sensor is disconnected or the cable is broken, the STM32 stops receiving pulses. If the vehicle is in motion, the absence of pulses will result in a 0 km/h reading, which may lead the controller to apply maximum power to compensate for the perceived lack of speed. Proactively detecting this absence is crucial for safety.

### Implementation Strategy

1.  **Timeout Monitoring:**
    *   **Description:** The system will maintain a timer that is reset with each pulse received from the sensor. If the time since the last pulse exceeds a predefined limit while the motor is receiving a movement command, a communication failure is detected.
    *   **Justification:** This differentiates a stopped vehicle (where the absence of pulses is normal) from a connection failure while in motion.

2.  **Dynamic Timeout Limit:**
    *   **Description:** The timeout limit will be inversely proportional to the minimum expected speed under command. For the PiRacer, a fixed timeout of **500ms** will initially be adopted as a safe upper limit.
    *   **Justification:** 500ms is sufficient time to cover low speeds without triggering false positives, but fast enough to prevent dangerous acceleration in case of failure.

3.  **Safety Action:**
    *   **Description:** Once the timeout is detected, the system will immediately transition to the **Fail-Safe State**.
    *   **Action:** Total interruption of motor PWM and critical error signaling.

## 3. Conclusion

The implementation of a timeout detection linked to the motor command ensures that the system quickly identifies physical connection failures, preventing dangerous control reactions and ensuring the transition to a safe state.

---

## Reviewer Note

Please validate if the 500ms timeout value is appropriate for the PiRacer dynamics or if it should be adjusted based on practical stable minimum speed tests.

## 4. References

**[1] (To be filled):** Technical documentation or standards on **timeout detection strategies in speed sensors/encoders**.
