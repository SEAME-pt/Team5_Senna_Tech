# 🚀 Sprint 2 Report – Team5: Senna Tech

**Duration:** [10/11/2025] → [23/11/2025]

**Sprint Goal:** Complete the installation and migration to AGL, ensuring full integration of all existing project components.

**Team Roles:**
| Name            | Responsibilities     |
|-----------------| ---------------------|
| Hellom        | Hardware Engineer |
| Marcelo       | QT Developer |
| Nicole          | Scrum Master |
| Vinicius       | Software Engineer |
| Yasmine      | Software Engineer |

---

## 🎯 Objectives for this Sprint

- Install and configure AGL.
- Migrate the existing project to the AGL environment.
- Solve the battery drops problem.
- Implement Cross Compilation.
- Set up ThreadX.
- Implement CAN protocol for microcontroller communication.
- Continue the implementation of TSF.

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83)

---

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **10/11** | Helom will assemble the hardware setup to mount and fix the microcontroller. Vinicius will begin the implementation of AGL using Yocto and start building the image to test deployment on the Raspberry Pi. Marcelo will implement the battery level reading feature in Qt. Nicole will study the initial steps for implementing ThreadX. Yasmine will assemble the CAN protocol setup to put the theoretical concepts into practice. | - |
| **11/11** | Helom will create an Excel table to calculate the available and required power levels and will document the process. Nicole will finish installing the IDE and start the ThreadX test project. Vinicius completed the image build of AGL and will transfer it to the Raspberry Pi. Marcelo managed to read the battery level, but the data is unstable, so he will work on fixing this issue. Yasmine will finish the pinout with the STM and check if the information is being transmitted. | - |
| **12/11** | Helom finished issue #75 and submitted a pull request, now will start the power assessment of all components. Nicole will continue learning to use the IDE and will try to create a small test program already using ThreadX. Vinicius will make a new AGL image build to deploy on the Raspberry Pi, since there were issues with the previous one. Yasmine will continue working on the CAN protocol connection and check if there is already a response. | - |
| **13/11** | Nicole will try to implement the LED using ThreadX. Yasmine is working on the CAN response and needs the logic converter to proceed. Vinicius will explore AGL, which is already running on the Raspberry Pi. Marcelo will start working on cross-compilation in AGL. Helom will continue the power assessment. | - |
| **14/11** | Vinicius will try to display AGL on the screen, reassemble the car, and document the process. Marcelo successfully performed cross-compilation of a test file. He will now generate the AGL development kit and configure the Qt IDE for cross-compilation. Yasmine successfully established CAN communication using SPI and confirmed that CAN is working. She will now try connecting all CAN components to the Raspberry Pi. Nicole will study TSF. Helom will continue the power assessment. | - |
| **17/11** | Nicole will continue studying TSF. Marcelo will finish installing the IDE, configure the cross-compilation kit, and integrate Qt into AGL. Vinicius has installed the display configuration on AGL and will complete the remaining setup today. Yasmine will work on establishing the connection between the CAN system and AGL. Helom will continue the power requirements assessment. | - |
| **18/11** | Vinicius will put the car control code in AGL. Marcelo will continue the configuration of cross-compilation. Nicole will implement the LED program using ThreadX. Helom will search for a solution regarding the battery problem. Yasmine will finish the CAN system connection. | - |

---

## 🧠 Key Achievements


---

## ⚙️ Pending for next sprint


