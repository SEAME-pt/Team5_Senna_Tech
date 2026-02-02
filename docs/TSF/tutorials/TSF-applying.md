# Applying the Trustable Software Framework (TSF) to Automotive Projects

## Index
1. [Objective](#1-objective)
2. [Recommended Project Structure](#2-recommended-project-structure)
3. [Requirements Template](#3-requirements-template-requirementsmd)
4. [Trustable Tenets Template](#4-trustable-tenets-tenetsmd)
5. [Trustable Assertions Template](#5-trustable-assertions-assertionsmd)
6. [Evidence Template](#6-evidences-evidencesmd)
7. [Safety Argumentation Chain](#7-safety-argumentation-chain-request--claim--assertion--evidence-readmemd)
8. [Traceability Matrix](#8-traceability-matrix)
9. [Integration with ISO 26262](#9-integration-with-iso-26262)
10. [Automation with GitHub Actions](#10-automation-with-github-actions)
11. [Conclusion](#11-conclusion)

---

## 1. Objective
This guide explains **how to apply the TSF** in automotive projects.  
The goal is to structure **requirements, evidence, tenets, and assertions** in an auditable and traceable way.

---

## 2. Recommended Project Structure
```
/project-root
├── docs/
│   ├── requirements.md
│   ├── tenets.md
│   ├── safety-case.md
│   └── traceability-matrix.xlsx
├── src/
├── tests/
└── .github/workflows/ci.yml
```

### Requirement Identification Convention

| Prefix | Requirement Type | Description | Example |
|---------|------------------|-------------|----------|
| **SAF-** | Safety | Related to functional safety. | SAF-001 — Emergency Stop |
| **FUNC-** | Functional | Defines expected system behavior. | FUNC-005 — Process camera input |
| **NFR-** | Non-Functional | Defines performance, timing, or reliability requirements. | NFR-002 — Response time < 100 ms |
| **PERF-** | Performance | Related to hardware or software performance. | PERF-003 — Inference rate ≥ 30 FPS |
| **SEC-** | Security | Related to cybersecurity and data protection. | SEC-004 — Encrypt logs in transit |

This standardization facilitates traceability between requirements, code, and tests, ensuring clarity during audits or ISO 26262 certifications.

---

## 3. Requirements Template (requirements.md)

```markdown
# Software Requirements Specification (SRS) Template

## Project:
<e.g., PiRacer Autonomous Control System>

## Version:
<e.g., 1.0.0>

## Date:
<YYYY-MM-DD>

## Prepared By:
<Your Name / Team / Department>

---

## 1. Purpose
<Briefly describe the purpose of this software and the scope of these requirements.>

Example:
> This document defines the functional and non-functional software requirements for the PiRacer autonomous vehicle control system.

---

## 2. Definitions and Abbreviations
| Term | Definition |
|------|-------------|
| ASIL | Automotive Safety Integrity Level |
| TSF | Trustable Software Framework |
| CI | Continuous Integration |
| SUT | System Under Test |

---

## 3. Functional Requirements

| ID | Requirement | Description | ASIL | Verification Method | Related Tenet | Status |
|----|--------------|-------------|------|----------------------|---------------|--------|
| <FUNC-001> | <Short Title> | <Detailed description of the function> | <QM / A / B / C / D> | <Unit Test / Simulation / Review> | <TNT-001> | <Draft / Verified / Rejected> |
| <FUNC-002> | <Short Title> | <Detailed description of the function> | <ASIL> | <Method> | <TNT-002> | <Status> |

Example:
| ID | Requirement | Description | ASIL | Verification Method | Related Tenet | Status |
|----|--------------|-------------|------|----------------------|---------------|--------|
| SAF-001 | Emergency Stop | The motor must stop when an obstacle < 50 cm is detected. | B | Unit Test + Simulation | Control | Verified |

---

## 4. Non-Functional Requirements

| ID | Requirement | Description | Verification Method | Target Metric | Status |
|----|--------------|-------------|----------------------|----------------|--------|
| <NFR-001> | <Performance> | <e.g., System latency must be below 100 ms> | <Stress Test> | <100 ms> | <Draft> |
| <NFR-002> | <Reliability> | <System uptime must exceed 99.5%> | <Long-run Test> | <99.5%> | <Verified> |

---

## 5. Safety and Security Requirements

| ID | Requirement | Description | ASIL | Verification Method | Related Standard | Status |
|----|--------------|-------------|------|----------------------|------------------|--------|
| <SAF-001> | <Functional Safety> | <Describe safety-critical behavior> | <ASIL Level> | <Test / Analysis> | <ISO 26262 Part 6> | <Status> |
| <SEC-001> | <Cybersecurity> | <e.g., Logs must be encrypted in transit> | <QM> | <Pen Test> | <ISO/SAE 21434> | <Draft> |

---

## 6. Traceability

| Requirement ID | Code Module | Test Case | Assertion | Evidence | Status |
|----------------|--------------|------------|------------|-----------|--------|
| <FUNC-001> | `path/to/module.py` | `tests/test_module.py` | <ASS-001> | <EVD-001> | <Pass/Fail> |
| <SAF-001> | `src/safety_controller.py` | `tests/test_safety_controller_

```

---

## 4. Trustable Tenets (tenets.md)

```markdown
# Trustable Tenets and Assertions — PiRacer

# Trustable Tenet Template

## Tenet ID:
<TNT-001>

## Tenet Name:
<e.g., The software is verifiable>

## Description:
<Briefly describe the guiding principle of trust this tenet represents.>

Example:
> This tenet ensures that all critical parts of the system can be tested and verified to guarantee correctness and reliability.

---

## Supported Assertions
| ID | Statement | Type | Linked Evidence | Status |
|----|------------|------|------------------|--------|
| <ASS-001> | <Write the assertion text here> | <Assertion / Expectation / Premise> | <Link or file name> | <Draft / Verified / Rejected> |

---

## Notes:
<Add any contextual information, such as the standard (e.g., ISO 26262 Part 6) or reasoning behind adopting this tenet.>

```
---

## 5. Trustable Assertions (assertions.md)

```markdown
# Trustable Assertion Template

## Assertion ID:
<ASS-001>

## Title:
<e.g., All critical modules are covered by automated tests>

## Related Tenet(s):
<Reference to related Tenet IDs, e.g., TNT-001 (Verifiability)>

## Description:
<What is being asserted about the system or process?>

Example:
> Each commit in the repository automatically runs the complete test suite to verify critical functions.

---

## Verification Method:
<e.g., Unit testing, Integration testing, Static analysis, Peer review>

## Evidence Required:
<List the artifacts that prove this assertion is true.>

Example:
> - CI/CD test logs  
> - Coverage report (`coverage.xml`)  
> - Test summary dashboard

---

## Verification Frequency:
<e.g., On every commit / On each release / Periodically>

## Result Summary:
<Optional: status, metrics, or pass/fail record>

| Date | Verified By | Result | Evidence Reference |
|------|--------------|---------|--------------------|
| <YYYY-MM-DD> | <Reviewer Name> | <Pass/Fail> | <Link or file> |

---

```
---

## 6. Evidences (evidences.md)

```markdown
# Trustable Evidence Template

## Evidence ID:
<EVD-001>

## Evidence Name:
<e.g., Test report: Safety controller module>

## Associated Assertion(s):
<List all related assertions, e.g., ASS-001, ASS-002>

## Description:
<Brief summary of what this evidence demonstrates.>

Example:
> This report provides results from automated unit tests verifying obstacle detection and emergency stop functionality.

---

## Source:
<Where the evidence was generated — e.g., CI pipeline, static analysis tool, test lab>

## Artifact Path:
<e.g., /artifacts/test-reports/test_safety_controller.xml>

## Verification Date:
<YYYY-MM-DD>

## Confidence Level:
<Low / Medium / High> — describe any uncertainties or limitations.

---

## Reviewer Notes:
<Comments, observations, or links to issue tracking.>

```
---

## 7. Safety Argumentation Chain (Request → Claim → Assertion → Evidence)

```markdown
# Safety Argumentation Chain

## Request
**ID:** <REQ-001>  
**Question:** <What needs to be proven?>  
**Example:** "Demonstrate that the automatic braking system is safe."

---

## Claim
**ID:** <CLM-001>  
**Answer to Request:** <What is asserted to be true?>  
**Example:** "The braking system is safe during normal operation."

---

## Supporting Assertions
| ID | Statement | Verification Method | Evidence |
|----|------------|---------------------|-----------|
| <ASS-001> | <e.g., The brake responds in less than 100 ms> | <Automated test> | <EVD-001> |
| <ASS-002> | <e.g., The software disables propulsion after obstacle detection> | <Integration test> | <EVD-002> |

---

## Supporting Premises
| ID | Statement | Source |
|----|------------|--------|
| <PRE-001> | <e.g., Ultrasonic sensor accuracy ±2 cm validated> | <Calibration Report 2025-03> |

---

## Conclusion
<Briefly describe how the evidence supports the claim and fulfills the request.>

Example:
> The presented evidence confirms that all safety-critical timing and detection requirements were met. Therefore, the system satisfies REQ-001 with high confidence.

```

---

## 8. Traceability Matrix

```markdown
| Requirement | Tenet | Assertion | Code | Test | CI Evidence |
|--------------|--------|------------|------|------|--------------|
| SAF-001 | Controllability | ASS-002 | `safety_controller.py` | `test_safety_controller.py` | `actions/test-report.xml` |
| SAF-002 | Verifiability | ASS-001 | `gui_display.py` | `test_gui_display.py` | `actions/ui-test.yml` |
```
---

## 9. Integration with ISO 26262

| TSF Element | ISO 26262 Mapping |
|--------------|------------------|
| Tenets & Assertions | Part 10 – Guidelines |
| Requirements | Part 6 – SW Development |
| Verification | Part 6 – Testing |
| Traceability | Part 8 – Supporting Processes |

---

## 10. Automation with GitHub Actions

```yaml
name: TSF Verification
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest --junitxml=actions/test-report.xml
      - uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: actions/test-report.xml
```
---

## 11. Conclusion
By applying **Trustable Tenets and Assertions**, automotive software development becomes more **transparent, auditable, and safe**, ensuring the confidence required in modern automotive systems.
