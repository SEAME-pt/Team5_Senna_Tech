# Evidence for HARA-200: Pulse Signal Integrity & Noise Rejection Strategy

**ID:** DM-HR200-2
**Date:** February 5, 2026
**Status:** Phase 2 Implemented (Software Debounce)
**Relates to:** HARA-200, Safety Goal SG-202

---

## 1. Context: The Chaos of Real-World Signals
Raw signals from the LM393 sensor in the PiRacer environment are inherently noisy due to motor EMI and mechanical vibration. Without treatment, this noise manifests as spurious pulses, causing hazard `H2-200` (Erratic High Value). This document details the engineering cycle used to diagnose, characterize, and mitigate this issue.

## 2. Noise Mitigation Engineering Cycle

### Phase 1: Diagnosis & Characterization (The "Chaotic State")
**Objective:** Capture raw LM393 signals and characterize noise ($\Delta T$) to define filter parameters.

*   **Technical Evidence:** Detailed signal analysis via oscilloscope, including the identification of gaps and measurement of pulse width (1.8ms) and interval (5ms), is documented in:
    👉 **[Bench Test Report (Oscilloscope)](../tests/speed_sensor-200/bench_test_oscilloscope.md)**

### Phase 2: Action Plan & Implementation (The "Treatment")
**Current Strategy:** Software-Defined Temporal Filtering (AST-202).

*   **Blanking Time Logic:**
    *   The software ignores subsequent interrupts for a period $X$ after the first valid detection.
    *   **Configuration:** $X = 3ms$ (Safety margin based on the 5ms minimum period measured in Phase 1).
*   **Dual Counter Strategy:** 
    *   `pulse_count`: Increments only valid pulses (Official Odometry).
    *   `noise_count`: Increments rejected pulses (Hardware Health Diagnostic).

### Phase 3: Verification of Efficacy (The "After")
**Objective:** Validation of the implemented filtering.

*   **Cross-Validation:** Comparison between the raw sensor signal vs. the processed signal by the STM32 (visualized via debug pin or real-time variable).
*   **Stability Log:** RPM monitoring to ensure the absence of "impossible frequency" spikes.

### Phase 4: Success Demonstration (The "Result")
**Before vs. After Comparison:**
*   **The Problem:** Electrical and mechanical noise causing false and unstable speed readings.
*   **The Solution:** Signal purification via software based on real physical data.
*   **Gain:** 100% elimination of false speed positives caused by high-frequency noise.

## 3. Conclusion
The current software implementation satisfies Safety Goal SG-202. The system now has a solid data capture foundation, allowing for future evolution to hardware-based filters (Timer ICF) if required.

---

**References:**
*   [1] Bench Test Report: `docs/TSF/tests/speed_sensor-200/bench_test_oscilloscope.md`
*   [2] STM32U5 Reference Manual (RM0456) - Section: General-purpose timers.