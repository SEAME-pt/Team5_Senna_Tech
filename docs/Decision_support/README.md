# Decision Support Documentation

## Purpose

This directory contains all documents that provide evidence, justification, and rationale for decisions made during the requirements and safety analysis process.

The goal is to ensure that every requirement, value, and strategic choice is traceable to a well-reasoned analysis, in accordance with the principles of the Trustable Software Framework (TSF). Each document is linked from the specific requirement or analysis document it supports.

## File Naming Convention

Files in this directory follow a standardized naming convention to ensure clarity and traceability.

**Format:** `[TYPE]-[HARA_ID]-[SEQ_NUM]_[Description].md`

**Example:** `DS-HR200-1_Degraded-Mode-Timeout.md`

### Components

-   **`[TYPE]`**: A prefix indicating the type of support document. Examples:
    -   `DS`: Decision Support (a record of a decision and its justification, e.g., why a hazard is considered credible).
    -   `DM`: Decision Mitigation (a record of a decision on *how* a hazard will be mitigated, supporting a Safety Goal).
    -   `TEST`: Test Report (results of a verification activity).
    -   `ANLS`: Analysis (a detailed technical analysis of a component or problem).

-   **`[HARA_ID]`**: An identifier that links the document to the specific HARA it supports.
    -   Example: `HR200` refers to `HARA-200`. The 'R' is added to distinguish it from Hazard IDs (e.g., `H1-200`).

-   **`[SEQ_NUM]`**: A sequential number for documents of the same type supporting the same HARA.

-   **`[Description]`**: A brief, human-readable description of the document's content.
