
# Creating statements with TruDag


### 1. Create statement file

```bash
trudag manage create-item FUNC 000 reqs/func
```
This will create the FUNC-000.md file inside the reqs/func directory

### 2. Edit the FUNC-000.md file
Open reqs/func/FUNC-000.md in your preference editor and add the statement.

```
---
id: FUNC-xxx or SAF-xxx or NFR-xxx or PERF-xxx or SEC-xxx  
title: add title
normative: true
level: 1.0
type: expectation
ASIL: A, B, C, D or QM
reviewers:
    - name: "namedoreviewer"
    - email: "email@reviewr.com"
reviewed: ''
owner: nameoftheowner
date: 2025-10-30
---

# Expectation‑ID: FUNC‑001  
**Title**: ADD TITLE

**Date**: YYYY‑MM‑DD

**Owner(s)**: nameoftheowner - Senna_Tech

## 1. Description  
EXAMPLE
The system shall allow the piRacer vehicle to be controlled using a joystick interface.  
This expectation covers the interaction between the human operator (via joystick) and the vehicle control logic, ensuring direct and real‑time control of vehicle movement.


## 2. Scope
- Connecting joystick hardware  
- Reading joystick inputs (axis movements)  
- Mapping joystick input to vehicle control commands (steer, accelerate)  


## 3. Post‑conditions / Outcomes  
EXAMPLE When the joystick is operated, the vehicle control logic receives the input and actuates the vehicle accordingly (steer/accelerate/brake) in real-time.

## 4. Acceptance criteria  
- [ ] x
- [ ] x  
- [ ] x  


## 5. Related Assertions  
-   ASS-xxx

## 6. log  
| Version | Date       | Author         | Description             |
|---------|------------|----------------|-------------------------|
| 1.0     | 2025‑10‑30 | name | description |
```

- You can use the templates located in reqs/templates to start your requirement!

### 3. Validate syntax according with trudag
```bash
trudag manage lint
```

# Creating link between statements with TruDag

### 1. You can create a link between 2 statemets using:

```bash
trudag manage create-link FUNC-000 ASS-000
```
This will update the .dotstop.dot file. You can see the new link there!

