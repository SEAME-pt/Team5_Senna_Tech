# Requirements and Analysis

This directory serves as the central repository for all project requirements, analysis documents, and supporting evidence, following a structured requirements engineering process.

The goal is to ensure that all aspects of the system are well-defined, traceable, and verifiable.

## Directory Structure and Workflow

The subdirectories are organized to reflect a logical workflow for requirements definition and verification.

**Typical Workflow:**
`Templates` -> `HARA` -> `Expectations` -> `Assertions` / `Assumptions` -> `Tests` -> `Evidences`

-   **[`/templates/`](./templates/)**: Provides standardized templates for creating new requirement and analysis documents.

-   **[`/HARA/`](./HARA/)**: Contains all Hazard Analysis and Risk Assessment (HARA) documents for the project.

-   **[`/expectations/`](./expectations/)**: Describes high-level expectations of the system's behavior from a user or stakeholder perspective.

-   **[`/assertions/`](./assertions/)**: Contains formal, verifiable assertions about the system's properties, which are derived from the higher-level expectations.

-   **[`/assumptions/`](./assumptions/)**: Documents all assumptions made during the design and development process.

-   **[`/test/`](./test/)**: Contains requirement-level test cases designed to verify that the defined assertions and expectations are met.

-   **[`/evidences/`](./evidences/)**: Holds formal evidence artifacts (e.g., final test reports, validation documents) that prove high-level requirements are met. This closes the verification loop.

---

## 🗺️ Traceability Maps

### Speedometer Integration
The diagram below illustrates the full traceability from expectations to final evidence for [Goal 1 of Module 01 - SEAME 2025](https://github.com/SEAME-pt/contents-2025/tree/main/01_SwArchitecture4Automotive).

```mermaid
graph TD
    %% Styles Definition
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef assumption fill:#e2e3e5,stroke:#383d41,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    %% Functional Requirements Layer
    subgraph F201 [201: Timeout]
        EXP201[EXP-201] --> AST201[AST-201]
        AST201 --> E201_1[EVD-201-1]
        AST201 --> E201_2[EVD-201-2]
    end

    subgraph F202 [202: Noise]
        EXP202[EXP-202] --> AST202[AST-202]
        AST202 --> E202_1[EVD-202-1]
    end

    subgraph F205 [205: MPU]
        EXP205[EXP-205] --> AST205[AST-205]
        AST205 --> E205[EVD-205]
    end

    subgraph F206 [206: Overflow]
        EXP206[EXP-206] --> AST206[AST-206]
        AST206 --> E206_1[EVD-206-1]
        AST206 --> E206_2[EVD-206-2]
    end

    subgraph F207 [207: Plausibility]
        EXP207[EXP-207] --> AST207[AST-207]
        AST207 --> E207[EVD-207]
    end

    %% Invisible Spacers to push foundation down
    E201_1 ~~~ ASM205
    E202_1 ~~~ ASM205
    E205 ~~~ ASM205
    E206_1 ~~~ ASM207
    E207 ~~~ ASM207

    %% Foundation Layer (Absolute Bottom)
    subgraph Foundation [Platform Foundation]
        direction LR
        ASM205[ASM-205: MPU Support] -.-> E205_H[EVD-ASM-205]
        
        ASM207[ASM-207: IMU Presence] -.-> E207_H[EVD-ASM-207]
    end

    %% Infrastructure Support Links
    AST201 -.-> ASM205
    AST201 -.-> ASM207
    AST202 -.-> ASM205
    AST202 -.-> ASM207
    AST205 -.-> ASM205
    AST206 -.-> ASM205
    AST207 -.-> ASM205
    AST207 -.-> ASM207

    %% Applying Classes
    class EXP201,EXP202,EXP205,EXP206,EXP207 expectation;
    class AST201,AST202,AST205,AST206,AST207 assertion;
    class E201_1,E201_2,E202_1,E205,E206_1,E206_2,E207,E205_H,E207_H evidence;
    class ASM205,ASM207 assumption;

    %% Links to files
    click EXP201 "./expectations/EXP-201.md"
    click EXP202 "./expectations/EXP-202.md"
    click EXP205 "./expectations/EXP-205.md"
    click EXP206 "./expectations/EXP-206.md"
    click EXP207 "./expectations/EXP-207.md"
    click AST201 "./assertions/AST-201.md"
    click AST202 "./assertions/AST-202.md"
    click AST205 "./assertions/AST-205.md"
    click AST206 "./assertions/AST-206.md"
    click AST207 "./assertions/AST-207.md"
    click ASM205 "./assumptions/ASM-205.md"
    click ASM207 "./assumptions/ASM-207.md"
    click E201_1 "./evidences/EVD-201-1.md"
    click E201_2 "./evidences/EVD-201-2.md"
    click E202_1 "./evidences/EVD-202-1.md"
    click E205 "./evidences/EVD-205.md"
    click E206_1 "./evidences/EVD-206-1.md"
    click E206_2 "./evidences/EVD-206-2.md"
    click E207 "./evidences/EVD-207.md"
    click E205_H "./evidences/EVD-ASM-205.md"
    click E207_H "./evidences/EVD-ASM-207.md"
```

---

## 🛡️ Trustable Framework (TSF) Validators

The project uses the **Eclipse Trustable Software Framework (TSF)** to automatically calculate confidence scores. The following custom validators are implemented in `.dotstop_extensions/validators.py`:

### 1. `test_log_validator` (Runtime Evidence)
Used for technical proofs generated by scripts or system execution.
- **Logic**: Returns **1.0** if it finds the keyword `PASS` in the log, and **0.0** if it finds `FAIL`.
- **Usage**: Validating time-sensitive behaviors like sensor timeouts.

### 2. `static_analysis_validator` (Code Quality Evidence)
Used to verify reports from static analysis tools like `cppcheck` or `lint`.
- **Logic**: Returns **1.0** if it finds a success pattern (default: `0 errors`) in the report file.
- **Usage**: Validating safety-critical code patterns and overflow prevention.

### 3. `reviewer_score` (Process Evidence)
Used for manual gates, such as peer reviews or datasheet inspections.
- **Logic**: Returns **1.0** if the metadata field `result` is explicitly set to `PASS` in the YAML configuration.
- **Usage**: Validating hardware specifications and manual design reviews.

---
-   **[`statements-viewer.md`](./statements-viewer.md)**: A document likely related to viewing or interpreting the various requirement statements.

### Related Documentation

-   **`docs/Decision_support/`**: While formal evidence resides here in `/evidences`, the `docs/Decision_support/` directory holds detailed engineering-level justifications, research, and rationale for specific design decisions made during analysis (e.g., justifying a specific HARA failure mode).
