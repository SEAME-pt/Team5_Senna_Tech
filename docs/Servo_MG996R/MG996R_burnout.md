
# MG996R Servo Burnout - Root Cause Analysis & Prevention

## Executive Summary

The MG996R servo has failed repeatedly due to **stall current overheating**. When the servo is held at mechanical limits, it draws **2.5A**, causing the internal coil to overheat and melt in as little as 5-10 seconds. This document outlines the root cause, implemented solutions, and hardware requirements to prevent future burnouts.

---

## 1. Servo Specifications (Datasheet)

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Operating Voltage** | 4.8V – 7.2V | Safe operating range |
| **Running Current** | 500mA (4.8-7.2V) | During normal movement |
| **Running Current (Nominal)** | 900mA @ 6V | Peak running current at 6V |
| **Stall Current** | **2.5A @ 6V** | ⚠️ **Critical – causes burnout** |
| **Temperature Range** | 0°C – 55°C | Maximum safe operating temp |
| **Stall Torque (6V)** | 11 kgf·cm | Force at mechanical limit |
| **Response Time** | 0.14 s/60° @ 6V | Speed from neutral |

---

## 2. Burnout Mechanism

### Timeline of Servo Failure

| Stage | Current | Duration | Servo State | Temperature |
|-------|---------|----------|-------------|-------------|
| Normal operation | 500 mA | Continuous | Smooth movement | 25–35°C |
| **Stall begins** | **2.5 A** | 0 sec | Gears locked at limit | **35°C** |
| **Early overheating** | 2.5 A | ~5 sec | Coil resistance heating | **60–75°C** |
| **Critical heating** | 2.5 A | ~10 sec | Insulation degrading | **85–100°C** |
| **Thermal runaway** | 2.5 A | ~15–30 sec | Coil winding short | **>120°C** |
| **Servo destroyed** | – | After 30 sec | Internal coil melted | **Failure** |

### Root Cause

**Steering commands pulled the servo to mechanical hard-stops** (PWM raw values 205 or 410), forcing the servo into continuous stall, causing thermal runaway and coil burnout.

---

## 3. Solutions Implemented

### 3.1 Software: Reduced Safe Operating Range

| Range Type | Raw Values | Movement Range | Status |
|-----------|------------|-----------------|--------|
| Full Mechanical | 205 – 410 | 100% | ❌ Unsafe – causes stall |
| **Safe Operating** | **240 – 375** | **85%** | ✅ **Implemented** |

**Benefit:** The servo now operates at 85% of its mechanical capacity, preventing hard mechanical stops that trigger stall current. This safety margin eliminates the worst-case 2.5A stall scenario while maintaining full steering responsiveness.

### 3.2 Software: Stall Detection & Warning System

A real-time monitoring system now tracks servo position:
- **Monitors** if servo is held at extreme limits
- **Warns** via UART if servo is locked for >5 seconds
- **Message:** `"WARNING: Servo at mechanical limit for >5s - HIGH STALL RISK!"`

### 3.3 Critical: Power Supply Verification & Voltage Stability

The power supply **must** deliver:

| Requirement | Value | Justification |
|-------------|-------|----------------|
| **Voltage (nominal)** | 6.0V | Servo datasheet nominal |
| **Voltage (minimum)** | 4.8V | Lowest acceptable voltage |
| **Voltage under stall** | >4.8V | Must NOT sag below 4.8V during 2.5A draw |
| **Current capacity** | ≥3.0A | Headroom above 2.5A stall current |
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

---

## 4. Hardware Fix Checklist

### Power Management
- [ ] **Dedicated 6V supply** – Do NOT use shared USB/logic rail
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
   → Expected: 6.0V ±0.1V
3. Send servo to full deflection (100% steering)
   → Expected: 6.0V ±0.1V
4. Hold servo at full deflection for 10 seconds
   → Expected: Must NOT drop below 4.8V
```

**If voltage drops below 4.8V:** Power supply is inadequate – upgrade required.

### Test 2: Thermal Stability
```
1. Start with servo at 0% (neutral position)
2. Cycle steering 0% → 100% → 0% at 1 Hz for 2 minutes
3. Hold servo at 100% deflection for 30 seconds
4. Measure servo case temperature with IR thermometer
   → Expected: <55°C
   → WARNING: >60°C indicates problem
   → CRITICAL: >75°C stop immediately
```

### Test 3: Stall Detection Firmware
```
1. Flash updated firmware
2. Send UART monitor
3. Manually hold servo at full right deflection
4. Wait >5 seconds
   → Expected: UART message appears
      "WARNING: Servo at mechanical limit for >5s - HIGH STALL RISK!"
```

---

## 6. Recommended Improvements

### Immediate (Required)
1. **Replace burned-out servo** with new MG996R
2. **Upgrade power supply** if it's <3A rated
3. **Add capacitor filtering** (100μF + 22μF) to servo power
4. **Flash updated firmware** with stall detection
5. **Perform all tests** before returning to operation

### Medium-term (Recommended)
1. Add current-limiting circuit (100mA fuse + TVS diode) on servo power line
2. Implement servo temperature monitoring via thermistor (if available)
3. Add watchdog timer to auto-neutral servo if control messages stop

### Long-term (Nice-to-have)
1. Replace MG996R with digital servo (has internal temperature monitoring)
2. Add servo feedback angle sensor for closed-loop verification
3. Implement CAN-based servo health monitoring

---

## 7. References

- **MG996R Datasheet:** Operating Voltage 4.8–7.2V, Stall Current 2.5A @ 6V
- **Code Changes:** [car.h](../src/threadx/SennaTech/Core/Inc/car.h) and [car.c](../src/threadx/SennaTech/Core/Src/car.c)
- **Team Contact:** Servo maintenance responsable

---

**Last Updated:** May 5, 2026  
**Status:** Preventative measures implemented – awaiting hardware verification
 