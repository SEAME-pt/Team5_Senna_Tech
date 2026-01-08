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
-   **[`statements-viewer.md`](./statements-viewer.md)**: A document likely related to viewing or interpreting the various requirement statements.

### Related Documentation

-   **`docs/Decision_support/`**: While formal evidence resides here in `/evidences`, the `docs/Decision_support/` directory holds detailed engineering-level justifications, research, and rationale for specific design decisions made during analysis (e.g., justifying a specific HARA failure mode).