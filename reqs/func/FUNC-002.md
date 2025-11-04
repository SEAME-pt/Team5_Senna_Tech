---
id: FUNC-002 
title: The user (driver) must be able to view vehicle information in a cross-compiled Qt graphical interface.
normative: true
level: 1.0
type: expectation
ASIL: A
reviewers:
    - name: "namedoreviewer"
    - email: "email@reviewr.com"
reviewed: ''
owner: Nicole Souza, Marcelo Martins
date: 2025-10-30
---

# Expectation‑ID: FUNC‑002  
**Title**: The user (driver) must be able to view vehicle information in a cross-compiled Qt graphical interface.

**Date**: 2025‑10‑30

**Owner(s)**: Vinícius Vaccari - Senna_Tech

## 1. Description  

The system must provide a graphical interface, developed using Qt and cross-compiled for the target embedded platform, allowing the driver to easily access and visualize key vehicle information.
The interface should present data such as speed, fuel level, temperature, and warnings indicators in a clear, intuitive, and non-distracting manner.
User interaction must be minimal, prioritizing safety and clarity during driving.

## 2. Scope
- Display real-time vehicle information such as speed, battery level, and temperature.
- Indicate warning messages (e.g., low fuel, high temperature).
- Use simple, readable layouts suitable for embedded screens.
- Operate seamlessly on the target embedded hardware using cross-compiled Qt libraries.


## 3. Post‑conditions / Outcomes  
- The driver can read essential vehicle information without confusion or delay.
- All relevant data is displayed correctly and refreshed in real time

## 4. Acceptance criteria  
- [ ] The interface displays key parameters (e.g., speed, battery and temperature).
- [ ] The layout is readable and functional on the target embedded display.
- [ ] The application runs correctly after cross-compilation on the target device.


## 5. Related Assertions  
-   ASS-003
-   ASS-004
-   ASS-005

## 6. log  
| Version | Date       | Author         | Description             |
|---------|------------|----------------|-------------------------|
| 1.0     | 2025‑10‑30 | Vinicius Vaccari | Qt Display requirements |
