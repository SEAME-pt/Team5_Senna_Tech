
 * SERVO POWER REQUIREMENTS AND BURNOUT ANALYSIS (MG996R):
 * 
 * FROM DATASHEET:
 * - Operating Voltage: 4.8V to 7.2V
 * - Running Current: 500mA (4.8-7.2V range), 900mA (at 6V nominal)
 * - STALL CURRENT: 2.5A (6V) ← THIS IS THE KILLER
 * - Temperature range: 0°C to 55°C
 * 
 * WHY YOUR SERVO BURNED OUT:
 * When servo hits mechanical limits or gets stuck:
 *   1. Servo stalls and draws 2.5A continuously
 *   2. If stalled for even 5 seconds: servo core temp rises to 100°C+
 *   3. Coil insulation melts, then shorted windings → servo dies
 * 
 * ROOT CAUSE: Steering commands were pulling servo to mechanical limits (raw=205 or 410)
 *             causing stall current spikes that rapidly destroyed the servo.
 * 
 * SOLUTIONS IMPLEMENTED:
 * 1. Reduced safe range from 205-410 to 240-375 (prevents mechanical hard-stops)
 * 2. Added stall detection that warns if servo held at limit >5 seconds
 * 3. CRITICAL: Verify power supply can deliver:
 *    - Minimum: 4.8V sustained (even under 2.5A stall events)
 *    - Recommended: 6V with <0.1Ω cable resistance
 *    - Supply must have >3A capacity (even 500mA servo needs headroom)
 * 
 * HARDWARE FIX CHECKLIST:
 * ✓ Use dedicated 6V power supply (NOT shared USB/logic rail)
 * ✓ Add 100μF + 22μF capacitors across servo power for stall current spikes
 * ✓ Use short, thick gauge servo connector cable (<50mm, 16AWG+)
 * ✓ Check servo is authentic MG996R (counterfeits have worse specs)
 * ✓ Verify under-voltage: measure servo voltage during full stall test
 