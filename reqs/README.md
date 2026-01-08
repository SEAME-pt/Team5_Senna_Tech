# Requirements and Analysis

This directory serves as the central repository for all project requirements, analysis documents, and supporting evidence, following a structured requirements engineering process.

The goal is to ensure that all aspects of the system are well-defined, traceable, and verifiable.

## Directory Structure and Workflow

The subdirectories are organized to reflect a logical workflow for requirements definition and verification.

**Typical Workflow:**
`Templates` -> `HARA` -> `Expectations` -> `Assertions` / `Assumptions` -> `Tests` -> `Evidences`



-   **[`/templates/`](./templates/)**: Provides standardized templates for creating new requirement and analysis documents, ensuring consistency across the project.

-   **[`/HARA/`](./HARA/)**: The process often begins here with a Hazard Analysis and Risk Assessment to understand the system's safety constraints.

-   **[`/expectations/`](./expectations/)**: Describes high-level expectations of the system's behavior, often derived from initial stakeholder needs and the HARA.

-   **[`/assertions/`](./assertions/)**: Contains formal, verifiable assertions about the system's properties, which are derived from the higher-level expectations.

-   **[`/assumptions/`](./assumptions/)**: Documents all assumptions made during the design and development process.

-   **[`/test/`](./test/)**: Contains requirement-level test cases designed to verify that the defined assertions and expectations are met.

-   **[`/evidences/`](./evidences/)**: Holds the output evidence (e.g., test results, logs) that proves the system complies with its requirements. This closes the verification loop.

---
-   **[`statements-viewer.md`](./statements-viewer.md)**: A document likely related to viewing or interpreting the various requirement statements.
