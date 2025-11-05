---
id: FUNC-003
title: PiRacer shall correctly read system data
normative: true
level: 1.0
type: requirement
ASIL: B
reviewers:
    - name: "namedoreviewer"
    - email: "email@reviewer.com"
reviewed: ''
owner: Vinicius Vaccari, Yasmine Fontenele, Nicole Souza
date: 2025-10-30
---

# Expectation‑ID: FUNC‑003  
**Title**: PiRacer shall correctly read system data

**Date**: 2025‑10‑30

**Owner(s)**: Vinícius Vaccari, Yasmine Fontenele, Nicole Souza - Senna_Tech

## 1. Description  

The system shall be capable of correctly reading and processing all relevant system data from the PiRacer platform.

## 2. Scope
- Accessing system sensors and status data (temperature, battery level, speed sensor, etc.)
- Ensuring data integrity and accuracy of readings


## 3. Post‑conditions / Outcomes  
- System retrieves and updates CPU temperature correctly
- Data must be available to other modules (example: QT Display)

## 4. Acceptance criteria  
- [ ] The interface displays key parameters (e.g., speed, battery and temperature).
- [ ] The extracted datas corresponds to the operation of the expansion board / Raspberry5 etc...


## 5. Related Assertions  
-   ASS-006
-   ASS-007
-   ASS-008

## 6. log  
| Version | Date       | Author         | Description             |
|---------|------------|----------------|-------------------------|
| 1.0     | 2025‑10‑30 | Vinicius Vaccari | System data requirements |
