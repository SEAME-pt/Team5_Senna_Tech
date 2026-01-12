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
    subgraph "Expectations (EXP)"
        EXP201[EXP-201]
        EXP202[EXP-202]
        EXP206[EXP-206]
    end

    

    subgraph "Assertions / Assumptions"
        direction LR
        
        %% Assumptions
        ASM201[ASM-201: HW Protection]
        ASM202[ASM-202: Secondary Src]

        %% Assertions
        AST201[AST-201]
        AST202[AST-202]
        AST206[AST-206]

        %% Horizontal Links
        ASM201 -.-> AST201
        ASM202 -.-> AST202
    end

    subgraph "Tests (TST)"
        TST201_1[TST-201-1: Unit Script]
        TST201_2[TST-201-2: Physical Proc]
        TST202[TST-202: Noise Script]
        TST206_1[TST-206-1: Overflow Script]
        TST206_2[TST-206-2: Static Analysis]
    end

    subgraph "Evidences (EVD)"
        E201_1[EVD-201-1: Log]
        E201_2[EVD-201-2: Video]
        E202_1[EVD-202-1: Log]
        E206_1[EVD-206-1: Log]
        E206_2[EVD-206-2: Report]
    end

    %% Relationships
    EXP201 --> AST201
    EXP202 --> AST202
    EXP206 --> AST206

    %% Invisible links to anchor ASM below EXP
    EXP201 ~~~ ASM201
    EXP202 ~~~ ASM202

    AST201 --> TST201_1 & TST201_2
    AST202 --> TST202
    AST206 --> TST206_1 & TST206_2

    TST201_1 --> E201_1
    TST201_2 --> E201_2
    TST202 --> E202_1
    TST206_1 --> E206_1
    TST206_2 --> E206_2

    %% Links to files
    click EXP201 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/expectations/EXP-201.md"
    click EXP202 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/expectations/EXP-202.md"
    click EXP206 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/expectations/EXP-206.md"
    click ASM201 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/assumptions/ASM-201.md"
    click ASM202 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/assumptions/ASM-202.md"
    click AST201 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/assertions/AST-201.md"
    click AST202 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/assertions/AST-202.md"
    click AST206 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/assertions/AST-206.md"
    click E201_1 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/evidences/EVD-201-1.md"
    click E201_2 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/evidences/EVD-201-2.md"
    click E202_1 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/evidences/EVD-202-1.md"
    click E206_1 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/evidences/EVD-206-1.md"
    click E206_2 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/reqs/evidences/EVD-206-2.md"
```

---
-   **[`statements-viewer.md`](./statements-viewer.md)**: A document likely related to viewing or interpreting the various requirement statements.

### Related Documentation

-   **`docs/Decision_support/`**: While formal evidence resides here in `/evidences`, the `docs/Decision_support/` directory holds detailed engineering-level justifications, research, and rationale for specific design decisions made during analysis (e.g., justifying a specific HARA failure mode).
