---
id: FUNC-001
title: PiRacer shall be controled by JoyStick
normative: true
level: 1.0
type: expectation
status: draft
linked_expectations: []
owner: Vinicius Vaccari
date: 2025-10-30
---

# Expectation‑ID: FUNC‑001  
**Title**: PiRacer shall be controled via JoyStick

**Date**: 2025‑10‑30

**Owner(s)**: Vinícius Vaccari - Senna_Tech

## 1. Description  
The system shall allow the piRacer vehicle to be controlled using a joystick interface.  
This expectation covers the interaction between the human operator (via joystick) and the vehicle control logic, ensuring direct and real‑time control of vehicle movement.


## 2. Scope
- Connecting joystick hardware  
- Reading joystick inputs (axis movements)  
- Mapping joystick input to vehicle control commands (steer, accelerate)  


## 3. Post‑conditions / Outcomes  
When the joystick is operated, the vehicle control logic receives the input and actuates the vehicle accordingly (steer/accelerate/brake) in real-time.

## 4. Acceptance criteria  
- [ ] When user moves joystick right axis left/right, the vehicle steers left/right accordingly.
- [ ] When user moves left axis forward or back, the vehicle accelerate in the right direction.  
- [ ] System logs joystick input events and maps to commands for traceability  


## 5. Related Assertions  
-   ASS-001
-   ASS-002

## 6. Change log  
| Version | Date       | Author         | Description             |
|---------|------------|----------------|-------------------------|
| 1.0     | 2025‑10‑30 | ViniciusVaccari | Initial expectation car control |
