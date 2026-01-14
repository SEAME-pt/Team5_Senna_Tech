# Speed Sensor Verification Suite (Issue 141)

This directory contains the test artifacts, logs, and reports used to validate the safety requirements for the pulse-frequency-based speedometer.

## 📊 Evidence Verification Matrix

The following table maps technical assertions (AST) to their specific validation methods and TSF validators.

| Assertion ID | Technical Title | Test Artifact / Script | Validator Type | Verification Goal |
| :--- | :--- | :--- | :--- | :--- |
| **AST-201** | Pulse Timeout | `logs/timeout_test.log` | `test_log_validator` | Verify system enters error state if pulses stop for >500ms. |
| **AST-202** | Signal Debouncing | `logs/debounce_test.log` | `test_log_validator` | Ensure noise and bouncing pulses are filtered out. |
| **AST-205** | MPU Isolation | `DS-HR200-3_MPU-Isolation.md` | `reviewer_score` | Confirm sensor driver memory is protected via MPU regions. |
| **AST-206** | Counter Overflow | `reports/cppcheck_report.txt` | `static_analysis_validator` | Verify 64-bit logic prevents counter wraparound at high speeds. |
| **AST-207** | Plausibility | `logs/imu_fusion_test.log` | `test_log_validator` | Cross-check speedometer data with IMU-derived velocity. |

## 📂 Directory Structure

- **`/logs/` (Behavioral Evidence)**: Stores results from system execution and hardware tests. These files prove the system *behaves* correctly under specific conditions (e.g., detecting a timeout). Validated by `test_log_validator`.
- **`/reports/` (Structural Evidence)**: Stores results from automated analysis tools (like Cppcheck or Lint). These files prove the system is *designed* correctly and follows safety coding standards. Validated by `static_analysis_validator`.
- **`/scripts/` (Test Tools)**: Local helper scripts used to format or move artifacts into this evidence repository.

## 🧪 Test Architecture & Workflow

To maintain a clean and auditable repository, this project follows a strict separation between **Test Execution** and **Evidence Storage**.

### 1. Test Source Code (`src/`)
All scripts, unit tests, and hardware simulators are located within the `src/` directory, close to the functional code they verify. 
- *Example*: `src/car-control/piracer-cpp/tests/verify_timeout.py`

### 2. Evidence Artifacts (`tests/speed_sensor-200/`)
This directory (where you are now) acts as the **central repository for proof**. It should only contain the *output* of the tests (logs, reports, and screenshots). 
- *Why?* This ensures the **Trustable Software Framework (TSF)** has a stable, centralized path to validate the "Chain of Trust" without being cluttered by source code or build files.

### 🔄 Workflow:
1. **Develop**: Write the test script in the appropriate `src/` subfolder.
2. **Execute**: Run the test on the PiRacer, STM32, or Simulation environment.
3. **Capture**: Redirect the output to a file in `tests/speed_sensor-200/logs/`.
4. **Validate**: Run `trudag score` to let the TSF verify the newly generated logs.
