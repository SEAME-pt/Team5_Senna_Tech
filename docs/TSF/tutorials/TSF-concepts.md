# Trustable Software Framework (TSF) — Learning Guide

## Index
## Index
1. [What is TSF?](#1-what-is-tsf)
2. [Fundamental Principles of TSF](#2-fundamental-principles-of-tsf)
3. [Trustable Tenets and Assertions](#3-trustable-tenets-and-trustable-assertions)
4. [TSF Structure](#4-tsf-structure)
5. [Practical Example — PiRacer Project](#5-practical-example--piracer-project)
6. [Benefits of TSF](#6-benefits-of-tsf)
7. [References](#7-references)


---

## 1. What is TSF?
The **Trustable Software Framework (TSF)** is a theoretical model for reasoning about trustable software — a methodology for managing evidence that supports claims about it, and a structure for evaluating risks in the continuous delivery of safety-critical software.  
Its focus is to provide **processes, tools, and evidence** that demonstrate that the software is **trustable, verifiable, and traceable** — essential qualities to meet standards such as **ISO 26262**.

TSF helps teams connect **requirements → architecture → implementation → testing → safety evidence**.

---

## 2. Fundamental Principles of TSF

| Principle | Description | Practical Example |
|------------|-------------|-------------------|
| **Transparency** | Every technical decision must be traceable and documented. | Use GitHub Issues to justify design changes. |
| **Reproducibility** | Results must be reproducible across environments. | Automated build scripts and CI/CD with GitHub Actions. |
| **Traceability** | Each requirement must be linked to the code and tests that validate it. | Map requirements in a `requirements.yml` file linked to commits. |
| **Verifiability** | All artifacts must be testable and auditable. | Automated unit tests for every critical module. |
| **Justifiability** | Every design decision must have a technical justification. | Document design choices in a “Design Decision Record (DDR)”. |

---

## 3. Trustable Tenets and Trustable Assertions

### Trustable Tenets
**Trustable Tenets** are the **core principles** that define what it means for software to be “trustable” within the TSF.  
They represent **universal values** of confidence, safety, and verifiability throughout the software lifecycle.

Examples of Tenets include:
- Software is **comprehensible**: its functions and behavior are clear.  
- Software is **controllable**: its behavior can be managed and limited.  
- Software is **verifiable**: there is evidence supporting its correctness.  
- Software is **reproducible**: results can be repeated under the same conditions.  

Each Tenet is supported by **Assertions** — verifiable statements that provide concrete evidence.

---

### Trustable Assertions
A **Trustable Assertion** is a **verifiable statement** supporting a Tenet.  
It describes **what must be true** about the system or process and can be tested, inspected, or analyzed.

An **Evidence** is an objective, verifiable artifact proving that an **Assertion** is true — meaning that what is claimed about the system actually happens in practice, in a traceable and auditable way.

For example, for the Tenet “Software is traceable.”:
- **Assertion:** “Each functional and safety requirement is linked to at least one automated test and one identifiable implementation commit.”  
- **Evidence:** “Traceability matrix (`traceability-matrix.xlsx`) showing the links between requirements, code, and tests, automatically updated via GitHub Actions.”

The **Assertion** is what you *say* the system does.  
The **Evidence** is the *proof* that it indeed does it safely and reliably.

Assertions can be classified according to their **Statement** type.

---

### Classification of Statements
Statements in a trustable reasoning graph can be naturally classified into overlapping categories:

A **Request** is a Statement that has one or more children. It is a declaration of need or intent, typically from a stakeholder (safety engineer, OEM, auditor, etc.).  
It expresses what needs to be demonstrated.

A **Claim** is a Statement that has one or more parents. It is an assertion supported by evidence that responds to a Request.

These definitions allow us to define three additional and distinct types of Statements:

- An **Expectation** is a Statement that is a Request but not a Claim.  
- An **Assertion** is a Statement that is both a Request and a Claim.  
- A **Premise** is a Statement that is a Claim but not a Request.  

| Type | Description | Example | Purpose |
|------|--------------|----------|----------|
| **Expectation** | A qualitative goal or intent of trust, not necessarily verifiable. | “Software should be continuously validated to avoid regressions.” | Defines intentions or objectives. |
| **Assertion** | A verifiable, objective statement about the system. | “Each commit in the repository automatically triggers the full unit test suite.” | Provides a concrete basis for trust. |
| **Premise** | A condition assumed to be true, used to support Assertions. | “The CI server maintains complete and immutable logs of all test executions.” | Defines assumptions for reasoning. |

How they connect: the **Premise** ensures confidence in the results, the **Assertion** is testable, and the **Expectation** expresses the goal of continuous quality.  
These three categories help organize reasoning about software **trustworthiness**.

Flow of trust between intent → declaration → verification → proof:

| **Concept** | **Question it answers** | **Nature** | **Simple Example** |
|--------------|--------------------------|-------------|--------------------|
| **Request** | “What do we need to prove?” | Intent / requirement | “Prove that the automatic brake is safe.” |
| **Claim** | “What do we assert to be true?” | Main declaration | “The automatic brake is safe.” |
| **Assertion** | “How do we support this?” | Verifiable statement | “The brake responds in <100 ms.” |
| **Evidence** | “What proves this?” | Concrete data | Test logs and reports. |

---

## 4. TSF Structure

TSF is typically divided into **six main areas**:

1. **Requirements Definition**
2. **Architecture and Design**
3. **Implementation**
4. **Verification and Validation**
5. **Safety Argumentation (Safety Case)**
6. **Toolchain Confidence**

---

## 5. Practical Example — PiRacer Project

### Scenario
You are developing the software for **PiRacer**, an educational autonomous vehicle based on **Raspberry Pi 5** with a **Hailo AI Hat**.

### Applying TSF:
- **Tenet:** The system is controllable.  
- **Assertion:** The motor must stop if an obstacle is detected within 50 cm.  
- **Premise:** The ultrasonic sensor provides reliable readings.  
- **Evidence:** Automated testing confirms that the `check_obstacle_distance()` function stops the motor.  

---

Therefore, for a safety-critical software system to be considered "trustable", it should meet the following constraints:

- Risks and hazards associated with its intended use are analyzed.  
- Expected behaviors are explicitly documented.  
- Prohibited or unsafe behaviors are explicitly documented.  
- Expected behaviors are demonstrated through testing.  
- Test procedures and results are verified.  
- Prohibited behaviors are shown to be absent, mitigated, or corrected.  
- Process artifacts and test results are captured as evidence.  
- Evidence is analyzed, distilled, and presented with confidence values for each release.

---

## 6. Benefits of TSF

- Facilitates ISO 26262 certification.  
- Reduces failures and increases confidence.  
- Enables audits with living documentation.  

---

## 7. References

- [ELISA Project – Trustable Software Framework](https://directory.elisa.tech/workshops/2025-05-Lund/3-1_Trustable_Software_Framework.pdf)  
- [Codethink Trustable Framework](https://gitlab.com/CodethinkLabs/trustable/trustable)  
- ISO 26262:2018 — Road Vehicles – Functional Safety
