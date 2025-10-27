# 🧠 Automotive Functional Safety & Trustable Software Framework

This repository gathers structured documentation related to **ISO 26262** and the **Trustable Software Framework (TSF)**.  
It is designed for engineers, researchers, and practitioners working with **functional safety**, **software assurance**, and **automotive compliance**.

---

## 📂 Repository Structure

| File | Description |
|------|--------------|
|[ISO 26262 – Structure and Concepts](./ISO26262-structure-and-concepts.md)  | Conceptual and structural overview of ISO 26262:2018 (Functional Safety for Road Vehicles). Includes ASIL classification, lifecycle, documentation, and core philosophy. |
| [TSF – Learning Concepts](./TSF-concepts.md)  | Conceptual explanation of the Trustable Software Framework (TSF): core principles, trustable tenets, trustable assertions, and statement classifications. |
| [TSF – Applying in Practice](./TSF-applying.md)| Practical guidance for applying TSF in automotive software projects. Includes examples of traceability matrices, expectations, assertions, and CI evidence mapping. |

---

## 🧾 Quick Overview

### 🚗 **ISO 26262**
Focuses on ensuring **functional safety** of electrical and electronic systems in automotive environments.  
Defines the **ASIL (Automotive Safety Integrity Level)** methodology, **safety lifecycle**, and **documentation artifacts** required to demonstrate compliance.

### 🔒 **Trustable Software Framework (TSF)**
TSF provides a structured methodology for **establishing and demonstrating software trustworthiness**.  
It defines:
- **Trustable Tenets** — Core principles of software trust.  
- **Trustable Assertions** — Statements proving conformance to the tenets.  
- **Expectations / Premises / Assertions** — Logical structure for reasoning about system assurance.

### ⚙️ **Practical Integration**
Combining **ISO 26262** and **TSF** enables:
- Traceable safety requirements and verification evidence.  
- Assurance arguments (*Safety Case*) based on logical structure (e.g., GSN).  
- Reusable frameworks for continuous safety validation in CI/CD environments.

---

## 📚 References

- **ISO 26262:2018** – *Road Vehicles – Functional Safety*  
- **Trustable Project (ELISA / Codethink Labs)** – [https://gitlab.com/CodethinkLabs/trustable/trustable](https://gitlab.com/CodethinkLabs/trustable/trustable)  

---

> *“Trust and safety in software are not abstract ideals — they are measurable, demonstrable, and built into every design decision.”*

