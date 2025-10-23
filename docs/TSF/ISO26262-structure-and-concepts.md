ac# ISO 26262:2018 — Functional Safety for Road Vehicles

## 🧾 Index
1. [Overview](#1-overview)
2. [The Structure](#2-the-structure)
3. [Fundamental Concepts](#3-fundamental-concepts)
4. [ASIL — Automotive Safety Integrity Level](#4-asil--automotive-safety-integrity-level)
5. [Key Artifacts and Documents](#5-key-artifacts-and-documents)
6. [Goal Structuring Notation (GSN)](#6-goal-structuring-notation-gsn)
7. [Safety Lifecycle](#7-safety-lifecycle)
8. [Part 6 – Software Development](#8-part-6--software-development)
9. [Part 10 – Guidelines](#9-part-10--guidelines)
10. [Documentation and Evidence](#10-documentation-and-evidence)
11. [Relation to Other Standards](#11-relation-to-other-standards)
12. [Core Philosophy](#12-core-philosophy)
13. [References](#13-references)

---

## 🧭 1. Overview

**ISO 26262** is the international standard for **functional safety of electrical and electronic (E/E) systems** in production road vehicles.  
It is derived from **IEC 61508** (generic functional safety) and adapts its principles to the automotive context.

The standard covers the **entire safety lifecycle**, from concept to vehicle decommissioning.

---

## ⚙️ 2. The structure

| Part | Title | Description |
|------|--------|-------------|
| **Part 1** | **Vocabulary** | Defines terminology and fundamental concepts. |
| **Part 2** | **Management of Functional Safety** | Defines responsibilities, safety planning, and governance. |
| **Part 3** | **Concept Phase** | Introduces hazard analysis (HARA) and ASIL determination. |
| **Part 4** | **System Development** | Specifies safety requirements at the system level. |
| **Part 5** | **Hardware Development** | Establishes metrics for hardware faults and safety architecture. |
| **Part 6** | **Software Development** | Defines software design, testing, and verification requirements. |
| **Part 7** | **Production and Operation** | Ensures safety during manufacturing and operation. |
| **Part 8** | **Supporting Processes** | Configuration, documentation, verification, and tool qualification. |
| **Part 9** | **ASIL-Oriented and Safety Analysis** | Methods for ASIL decomposition and dependency analysis. |
| **Part 10** | **Guidelines** | Interpretative guidance and best practices. |
| **Part 11** | **Application to Electric Propulsion Systems** | Extension for hybrid and electric vehicles. |
| **Part 12** | **Application to Trucks, Buses, and Motorcycles** | Expansion to heavy-duty and two-wheeled vehicles. |

---

## 🧩 3. Fundamental Concepts

### 🔸 Functional Safety
Absence of unreasonable risk caused by malfunctioning E/E systems.

### 🔸 Item
A system or subsystem under safety analysis (e.g., ABS brake control).

### 🔸 Safety Goal
A high-level safety requirement derived from risk assessment.

### 🔸 Safe State
A condition in which risk is controlled (e.g., brakes applied, engine off).

---

## 🚦 4. ASIL — Automotive Safety Integrity Level

**ASIL** (Automotive Safety Integrity Level) defines the **degree of rigor required** in processes, testing, and documentation according to the **risk of an identified hazard**.

### 🔹 ASIL Scale

| Level | Meaning | Requirement |
|--------|----------|-------------|
| **QM** | Quality Managed (non-safety critical) | Standard quality process. |
| **ASIL A** | Low risk | Basic safety requirements. |
| **ASIL B** | Moderate risk | Increased control and verification. |
| **ASIL C** | High risk | Redundancy and rigorous validation. |
| **ASIL D** | Very high risk | Maximum rigor in design, validation, and independence. |

### 🔹 ASIL Determination Factors

1. **Severity (S)** – The potential severity of harm.  
   - S1: Light injury  
   - S2: Serious injury  
   - S3: Fatal injury or life-threatening damage

2. **Exposure (E)** – The probability of occurrence of the hazardous event.  
   - E1: Rare  
   - E2: Occasional  
   - E3: Frequent  
   - E4: Very frequent

3. **Controllability (C)** – The ability of the driver to avoid harm.  
   - C1: Easily controllable  
   - C2: Difficult to control  
   - C3: Uncontrollable

The combination of these dimensions defines the **ASIL**, typically using a matrix (defined in Part 3).  
Example: S3 + E4 + C3 → **ASIL D**.

### 🔹 Role of ASIL
- Defines **process rigor** for development and verification.  
- Determines **analysis depth** (FMEA, FTA, etc.).  
- Specifies **independence levels** between development and validation.

### 🔹 ASIL Decomposition
When redundancy or complementary safety architectures exist, the ASIL can be **decomposed** into lower levels, provided **independence** between elements is demonstrated.

Example: ASIL D → two independent ASIL B components (B + B).

---

## 📄 5. Key Artifacts and Documents

| Document | Description | Related Parts |
|-----------|--------------|----------------|
| **Safety Plan** | Defines safety responsibilities and planning. | Part 2 |
| **HARA** | Hazard Analysis and Risk Assessment. | Part 3 |
| **ASIL Decomposition** | Breakdown of safety responsibilities. | Part 9 |
| **Safety Requirements** | Traceable safety requirements. | Parts 4–6 |
| **Verification & Validation Plan** | Defines test strategy and acceptance criteria. | Parts 4, 6, 7 |
| **Safety Case (GSN)** | Argument-based evidence of system safety. | Part 10 |

---

## 🧠 6. Goal Structuring Notation (GSN)

**GSN** structures safety reasoning in a traceable logic chain.

```
Goal: The system is safe during normal operation and controlled failure.
│
├── Strategy: Safety is ensured through risk analysis and fault mitigation.
│   ├── Goal: All ASIL C/D hazards have been identified and mitigated.
│   │   └── Evidence: HARA + FMEA reports.
│   ├── Goal: Software complies with ASIL D requirements.
│   │   └── Evidence: MC/DC tests + independent audits.
│   └── Goal: Architecture prevents single-point failures.
│       └── Evidence: FTA results + common cause analysis.
│
└── Context: Category M1 vehicle with redundant electric steering.
```

---

## 🔄 7. Safety Lifecycle

1. Concept and hazard analysis (Part 3)  
2. System development (Part 4)  
3. Hardware and software development (Parts 5 and 6)  
4. Integration and testing  
5. Production and operation (Part 7)  
6. Decommissioning  

---

## 💻 8. Part 6 – Software Development

Defines secure software development practices:
- Safe coding (MISRA-C, AUTOSAR)
- Static and dynamic testing
- Code coverage according to ASIL (MC/DC for D)
- Software tool qualification
- Independence between development and verification teams

---

## 📘 9. Part 10 – Guidelines

Interpretative guide with best practices:
- Practical examples and document templates
- Component reuse strategies
- Integration with ISO 9001 and ASPICE
- ASIL decomposition examples
- Recommendations on safety culture and organizational processes

---

## 🧾 10. Documentation and Evidence

| Evidence | Source | Purpose |
|-----------|---------|----------|
| **Safety requirements** | Parts 3–6 | Define what must be guaranteed. |
| **ASIL assessment** | Part 3 | Establishes required rigor. |
| **Verification and validation** | Parts 4, 6, 7 | Confirms compliance and safe operation. |
| **Safety Case (GSN)** | Part 10 | Demonstrates, with evidence, that the system is safe. |

---

## 🔗 11. Relation to Other Standards

| Standard | Focus | Relationship |
|-----------|--------|---------------|
| **ISO 61508** | Generic functional safety | Conceptual foundation of ISO 26262 |
| **ISO/PAS 21448 (SOTIF)** | Safety Of The Intended Functionality | Covers non-malfunction-based risks |
| **ISO 9001** | Quality management | Organizational alignment |
| **ASPICE** | Automotive process improvement | Complements ISO 26262 development process |

---

## 🧩 12. Core Philosophy

> “Functional safety is an emergent property of systems that are well designed, verified, and managed throughout their lifecycle.”

---

## 📚 13. References

- ISO 26262:2018 — *Road Vehicles – Functional Safety*  
- ISO/PAS 21448 — *Safety of the Intended Functionality (SOTIF)*  
- MISRA-C:2012 — *Guidelines for Safe Coding in C*
