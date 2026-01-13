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
    %% Flow 201
    EXP201[EXP-201] --> AST201[AST-201]
    AST201 --> TST201[TST-201]
    TST201 --> E201_1[EVD-201-1]
    TST201 --> E201_2[EVD-201-2]

    %% Flow 202
    EXP202[EXP-202] --> AST202[AST-202]
    AST202 --> TST202[TST-202]
    TST202 --> E202_1[EVD-202-1]

    %% Flow 205
    EXP205[EXP-205] --> AST205[AST-205]
    EXP205 --> ASM205[ASM-205]
    AST205 --> TST205[TST-205]
    TST205 --> E205[EVD-205]
    ASM205 -.-> E205

    %% Flow 206
    EXP206[EXP-206] --> AST206[AST-206]
    AST206 --> TST206[TST-206]
    TST206 --> E206_1[EVD-206-1]
    TST206 --> E206_2[EVD-206-2]

    %% Flow 207
    EXP207[EXP-207] --> AST207[AST-207]
    EXP207 --> ASM207[ASM-207]
    AST207 --> TST207[TST-207]
    TST207 --> E207[EVD-207]
    ASM207 -.-> E207

    %% Links to files
    click EXP201 "./expectations/EXP-201.md"
    click EXP202 "./expectations/EXP-202.md"
    click EXP205 "./expectations/EXP-205.md"
    click EXP206 "./expectations/EXP-206.md"
    click EXP207 "./expectations/EXP-207.md"
    click AST201 "./assertions/AST-201.md"
    click AST202 "./assertions/AST-202.md"
    click AST205 "./assertions/AST-205.md"
    click ASM205 "./assumptions/ASM-205.md"
    click AST206 "./assertions/AST-206.md"
    click AST207 "./assertions/AST-207.md"
    click ASM207 "./assumptions/ASM-207.md"
    click TST201 "./test/"
    click TST202 "./test/"
    click TST205 "./test/"
    click TST206 "./test/"
    click TST207 "./test/"
    click E201_1 "./evidences/EVD-201-1.md"
    click E201_2 "./evidences/EVD-201-2.md"
    click E202_1 "./evidences/EVD-202-1.md"
    click E205 "./evidences/EVD-205.md"
    click E206_1 "./evidences/EVD-206-1.md"
    click E206_2 "./evidences/EVD-206-2.md"
    click E207 "./evidences/EVD-207.md"
``````

---
-   **[`statements-viewer.md`](./statements-viewer.md)**: A document likely related to viewing or interpreting the various requirement statements.

### Related Documentation

-   **`docs/Decision_support/`**: While formal evidence resides here in `/evidences`, the `docs/Decision_support/` directory holds detailed engineering-level justifications, research, and rationale for specific design decisions made during analysis (e.g., justifying a specific HARA failure mode).
