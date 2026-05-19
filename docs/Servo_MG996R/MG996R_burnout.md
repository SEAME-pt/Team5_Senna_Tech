
# MG996R Servo Burnout - Root Cause Analysis & Prevention

## Executive Summary

The MG996R servo has failed repeatedly due to **stall current overheating**. In this system the servo is powered from **5.14V through the expansion board**, and when it reaches a mechanical limit it can still draw up to **about 2.0A** at that voltage. That current is still enough to overheat the internal coil quickly. This document outlines the root cause, implemented solutions, and hardware requirements to prevent future burnouts.

---

## 1. Servo Specifications (Datasheet)

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Operating Voltage** | 4.8V – 7.2V | Datasheet safe operating range |
| **System Voltage** | **5.14V** | Actual voltage supplied by the expansion board |
| **Running Current** | ~500mA | During normal movement at 5.14V |
| **Running Current (Nominal)** | ~750mA @ 5V | Estimated peak running current in this system |
| **Stall Current** | **~2.0A @ 5V** | ⚠️ **Critical – causes burnout even at 5.14V** |
| **Temperature Range** | 0°C – 55°C | Maximum safe operating temp |
| **Stall Torque (6V)** | 11 kgf·cm | Force at mechanical limit |
| **Response Time** | 0.14 s/60° @ 6V | Speed from neutral |

---

## 2. Burnout Mechanism

### Timeline of Servo Failure

| Stage | Current | Duration | Servo State | Temperature |
|-------|---------|----------|-------------|-------------|
| Normal operation | 500 mA | Continuous | Smooth movement | 25–35°C |
| **Stall begins** | **~2.0 A** | 0 sec | Gears locked at limit | **35°C (estimated)** |
| **Early overheating** | ~2.0 A | ~5 sec | Coil resistance heating | **60–75°C (estimated)** |
| **Critical heating** | ~2.0 A | ~10 sec | Insulation degrading | **85–100°C (estimated)** |

### Root Cause

**Steering commands pulled the servo to mechanical hard-stops** (PWM raw values 205 or 410), forcing the servo into continuous stall, causing thermal runaway and coil burnout.

---

## 3. Solutions Implemented

### 3.1 Software: Reduced Safe Operating Range

| Range Type | Raw Values | Movement Range | Status |
|-----------|------------|-----------------|--------|
| Full Mechanical | 205 – 410 | 100% | ❌ Unsafe – causes stall |
| **Safe Operating** | **230 – 385** | **85%** | ✅ **Implemented** |

**Benefit:** The servo now operates at 85% of its mechanical capacity, preventing hard mechanical stops that trigger stall current. This safety margin eliminates the worst-case 2.5A stall scenario while maintaining full steering responsiveness.

### 3.2 Critical: Power Supply Verification & Voltage Stability

The power supply **must** deliver stable 5.14V in this system. The datasheet lists a 6.0V nominal value for best performance, but the current hardware uses a 5V supply from the expansion board.

| Requirement | Value | Justification |
|-------------|-------|----------------|
| **System voltage** | 5.14V | Actual supply voltage from the expansion board |
| **Voltage (minimum)** | 4.8V | Lowest acceptable voltage |
| **Voltage under stall** | >4.8V | Must NOT sag below 4.8V during a 2.0A draw |
| **Current capacity** | ≥2.5A | Headroom above the estimated 2.0A stall current at 5V |
| **Cable impedance** | <0.1Ω | Short, thick-gauge wiring |

#### Measured Voltage Stability (Verified Field Data)

**With Soft Limits (85% range) – Current Configuration:**
- Voltage at neutral position: **5.14V** (stable and consistent)
- Voltage at full deflection: **5.14V** (no sag observed)
- **Even with non-full battery:** Maintains **5.14V** consistency
- Stall event protection: ✅ **Guaranteed** – servo never reaches hard limits

**Without Soft Limits (100% range) – Previous Configuration:**
- Voltage at neutral: 5.5V–6.0V
- Voltage under full deflection: **4.0V** ⚠️ **drops below safe minimum (4.8V)**
- Battery sag events: Servo voltage enters danger zone
- Stall risk: ❌ **High** – servo constantly fighting mechanical limits

**Real-World Impact:** The 85% soft limit prevents voltage collapse and eliminates the previous 4V sag condition, keeping the servo in the safe operating window even with partially depleted battery.

**How the temperature estimate was derived:**
- At 5.14V and an estimated stall current of ~2.0A, the servo dissipates roughly `P = V × I = 5.14 × 2.0 ≈ 10.3W` as heat.
- That is a large amount of heat for a small servo body and internal coil volume.
- In a compact servo with limited airflow, 10W of internal dissipation can plausibly raise the internal temperature tens of degrees above ambient.
- Therefore, the values `60–75°C`, `85–100°C` are theoretical internal heating estimates under sustained stall.

---

## 4. Hardware Fix Checklist

### Power Management
- [ ] **Dedicated stable 5V supply** – Do NOT use shared USB/logic rail
- [ ] **Current rating ≥3A** – Verify power supply spec sheet
- [ ] **Voltage stability test** – Measure voltage during full servo stall (using oscilloscope or multimeter)

### Capacitor Protection
- [ ] **Add 100μF electrolytic capacitor** across servo power pins (low-ESR preferred)
- [ ] **Add 22μF ceramic capacitor** in parallel for high-frequency spikes
- [ ] **Mount near servo connector** – Keep leads <20mm long

### Wiring & Connectors
- [ ] **Use 16AWG or thicker** servo power cable
- [ ] **Keep cable <50mm long** – Minimize voltage drop
- [ ] **Secure connector** – Verify pins cannot slip or corrode
- [ ] **Test resistance** – Measured <100mΩ from supply to servo pins

### Servo Verification
- [ ] **Confirm authentic MG996R** – Counterfeits have worse thermal characteristics
- [ ] **Inspect connector** – No burn marks, corrosion, or loose pins
- [ ] **Visual inspection** – No cracks or damage to servo case

---

## 5. Testing Procedures

### Test 1: Power Supply Voltage Under Load
```
1. Connect multimeter to servo power pins
2. Send servo to 50% position (neutral)
   → Expected: 5.14V ±0.1V
3. Send servo to full deflection (100% steering)
   → Expected: 5.14V ±0.1V
4. Hold servo at full deflection for 10 seconds
   → Expected: Must NOT drop below 4.8V
```

**If voltage drops below 4.8V:** Power supply is inadequate – upgrade required.

---

## 6. References

- **MG996R Datasheet:** [MG996R](./MG996R.PDF)
- **Code Changes:** [car.h](../src/threadx/SennaTech/Core/Inc/car.h) and [car.c](../src/threadx/SennaTech/Core/Src/car.c)
 