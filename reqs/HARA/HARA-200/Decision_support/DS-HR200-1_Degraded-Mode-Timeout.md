# Evidence for HARA-200: Degraded Mode Escalation Timeout

**ID:** EVD-H200-1  
**Date:** 2026-01-08  
**Author:** Gemini  
**Relates to:** HARA-200, Hazard H4-200 (Stale Data / Latency)

---

## 1. Decision

The escalation timeout for the "Degraded Mode" (triggered by Hazard H4-200) is set to **200ms**.

If the system detects stale data from the I²C speedometer and enters Degraded Mode, it will escalate to the full Fail-Safe State (immediate motor interruption) if the condition persists for more than 200ms.

## 2. Justification

The 200ms value was chosen as a balance between system stability and responsiveness, based on the following factors:

*   **Assumed Sensor Update Rate:** The system design assumes a target speed sensor update rate of 50 Hz, meaning a new data sample is expected every **20ms**.

*   **Tolerance for Transient Failures:** A short timeout (e.g., 40-60ms) could trigger a full system shutdown from very brief, recoverable I²C bus glitches. A longer timeout allows the system to ride out these transient issues.

*   **System Agility and Instability Risk:** The PiRacer is a small, agile platform. Operating with stale data can lead to control loop oscillations and instability. A timeout longer than a few hundred milliseconds would create an unacceptable risk of the system becoming dangerously unstable before a safe state is triggered.

*   **Calculation:** A timeout of **200ms** corresponds to **10 consecutive missed sensor readings** (10 * 20ms). This value is considered a robust starting point, as it is long enough to prevent premature escalation from transient bus errors but short enough to mitigate prolonged, dangerous instability.

## 3. Assumptions

*   The primary control loop runs at a frequency that can reliably detect this timeout (e.g., >= 50 Hz).
*   The I²C driver can reliably signal a "stale data" condition to the control loop.
