# 🏎️ piRacer System Functional Requirements and Assertions

---

## 1️⃣ Motor Control (via joystick or code)

### **Expectation (Level 1)**  
**FUNC-001:** The piRacer must be controllable both via joystick and programmatically.

### **Assertions (Level 2)**  
- **ASS-001:** Joystick commands must be correctly mapped to the motors (forward, reverse, left, right).  
- **ASS-002:** Commands sent via code (API or scripts) must trigger the motors consistently and predictably.  
- **ASS-003:** The response time between a command (joystick or code) and motor movement must be less than **X ms**.

---

## 2️⃣ Qt Application for the Driver

### **Expectation (Level 1)**  
**FUNC-002:** The driver must be able to view vehicle information through a Qt graphical interface (cross-compiled).

### **Assertions (Level 2)**  
- **ASS-004:** The Qt interface must display real-time battery percentage.  
- **ASS-005:** The Qt interface must display the vehicle’s speed.  
- **ASS-006:** The application must be cross-compilable for the piRacer hardware without errors.  
- **ASS-007:** The interface data must refresh at a minimum frequency of **X Hz** (responsiveness).

---

## 3️⃣ Sensor Reading (e.g., speed sensor)

### **Expectation (Level 1)**  
**FUNC-003:** The system must correctly read data from the piRacer sensors.

### **Assertions (Level 2)**  
- **ASS-008:** The speed sensor must provide accurate readings relative to the vehicle’s actual speed.  
- **ASS-009:** The battery level sensor must provide accurate readings relative to the piRacer’s remaining battery.
