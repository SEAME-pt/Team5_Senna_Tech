# 🏎️ piRacer System Functional Requirements and Assertions

---

## 1. Motor Control

### Expectation (Level 1)

- **FUNC-001:** The piRacer must correctly respond to manual control inputs.

➡️ Failure to move the motors properly may affect the vehicle’s movement and could potentially cause accidents.

**ASIL:** B

#### Assertions (Level 2)

- **ASS-001:** The DC motors and servo must correctly respond to the parameters sent in the code.

---

## 2. Critical Battery and Temperature Information

### Expectation (Level 1)

> **FUNC-002:** The driver must be alerted to critical vehicle conditions (such as low battery or high temperature) through the Qt interface to ensure a safe response.

➡️ Failure to display this information may directly impact safety.

**ASIL:** A

#### Assertions (Level 2)

> **ASS-002:** The display must show a visual alert:  
> “**Critical battery — reduce speed / stop / look for a charging station**” when the level drops below *X%*.
>
> **ASS-003:** The Qt interface must display a visual alert:  
> “**High Temperature**” if the system temperature reaches dangerous levels.

---

## 3. Sensor Reading Failure Information

### Expectation (Level 1)

> **FUNC-003:** The driver must be alerted to any sensor reading failures.

➡️ Failure to display this information may directly impact safety.

**ASIL:** A

#### Assertions (Level 2)

> **ASS-004:** The software must clearly alert when a speed sensor reading error occurs.  
>
> **ASS-005:** The software must clearly alert when a battery sensor reading error occurs.

