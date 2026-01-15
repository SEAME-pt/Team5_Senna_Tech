# Evidence Artifacts Repository (`/tests`)

This directory serves as the centralized **Evidence Artifacts Repository** for the entire project. It is specifically structured to support the **Trustable Software Framework (TSF)** and the automated safety scoring process via **Trudag**.

## 📐 Organizational Standard

Every new feature or issue involving safety verification must create a sub-directory following this naming convention:
`[feature-name]-[HARA-number]` (e.g., `speed_sensor-200` for HARA-200)

### Internal Directory Structure
Each test suite directory MUST be organized as follows to ensure compatibility with project-wide validators:

1. **`/logs/` (Behavioral Evidence)**
   - **Content**: Runtime logs, console outputs, and hardware execution traces.
   - **Validator**: Typically validated by `test_log_validator`.
   - **Goal**: Prove the system *behaves* as expected during execution.

2. **`/reports/` (Structural Evidence)**
   - **Content**: Static analysis reports (Cppcheck, Lint), coverage reports, and architecture reviews.
   - **Validator**: Typically validated by `static_analysis_validator`.
   - **Goal**: Prove the system is *designed* correctly and follows safety standards.

3. **`/scripts/` (Local Helpers)**
   - **Content**: Scripts exclusively dedicated to formatting, filtering, or processing artifacts for this specific test suite (e.g., converting a raw sensor dump to a formatted log).
   - **Distinction**: Unlike the global `/scripts` folder at the project root (which handles project-wide infrastructure like CI/CD or Trudag automation), these local scripts are feature-specific utilities.
   - **Note**: The actual test logic and simulators (the "how to test") must remain in the `/src` directory.

## 🔄 Verification Workflow

1. **Execute** tests located in `src/`.
2. **Export** results (logs/reports) to the corresponding sub-folder in `tests/`.
3. **Commit** the evidence artifacts.
4. **Validate** by running `trudag score` to update the Trust Graph.

---
*Reference: See `.dotstop_extensions/validators.py` for a detailed logic of automated validators.*
