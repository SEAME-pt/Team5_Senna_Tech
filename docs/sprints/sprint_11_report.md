# 🚀 Sprint 11 Report – Team5: Senna Tech

**Duration:** [13/04/2026] → [24/04/2026]

**Sprint Goal:** Integrate PID (steering) with Lane Detection Model  and perform a live demo

---

## 🎯 Objectives for this Sprint

- Define a communication pipeline between the Lane Detection model, PID and servo motors.
- Improve Lane Detection post processing, focusing on curves and intersections
- Perform initial training of Object Detection Model (YOLOv8/v26)
- Implement Manual/Autonomous driving modes
- Conduct a Spike on Model Predictive Control (MPC)
- Improve the the energy distribution system 

---

**Team Roles:**
| Name            | Responsibilities                          |
|-----------------|-------------------------------------------|
| Hellom          | Energy and Hardware                         |
| Vinicius        | PID + Lane Detection Integration                         |
| Jose            | PID + Lane Detection Integration                                      |
| Yasmine         | Lane Detection Model              |
| Marcelo         | PID + Lane Detection Integration                                      | 

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+10)

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **13/04** | The team planned sprint 11, define the goals and split tasks **Marcelo, Vinicius and José:** Will work together to integrate the PID (steering) with the Lane Detection Model and servo motors **Yasmine:** Will work on the improvement of the Lane Detection Model post processing, focusing on curves and intersections. **Hellom:** Will upgrade the energy distribution system by adding a stepdown to feed the microcontroller and the display. |
| **14/04** | **Hellom**: Changed the energy distribution, adding a new step-down that feeds the microcontroller and the display, as well as heat sinks and coolers for the system. Today is focused on installing monitoring systems on the Raspberry Pi. **José**: Focused on finishing the 42 Common Core. **Yasmine**: Will work on improving the Lane Detection model post-processing, focusing on curves and intersections. **Vinicius**: Helped Hellom install new monitoring libraries into the AGL build, recompiling the entire system and flashing it onto the microSD card. He will also work together with **Marcelo** to integrate the PID class into the Lane Detection pipeline code, sending the steering value to the microcontroller via the CAN protocol. |
| **15/04** | **José**: Will work on the implementation of Manual/Autonomous driving modes by pressing buttons on the joystick. **Yasmine**: Improved the Lane Detection post-processing by creating imaginary lines on the road whenever the model doesn't recognize one of the lines. By implementing this, the detection has improved a lot, especially in curves.  **Vinicius and Marcelo**: Fine-tuning the PID control by calibrating the three PID parameters (Kp, Ki, Kd). **Hellom**: Day off. |


---

## 🧠 Key Achievements
- 
---