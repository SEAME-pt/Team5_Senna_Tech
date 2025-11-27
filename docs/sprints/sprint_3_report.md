# 🚀 Sprint 3 Report – Team5: Senna Tech

**Duration:** [24/11/2025] → [07/12/2025]

**Sprint Goal:** Integrate speedometer with hardware, processing data through ThreadX  

**Team Roles:** :
| Name            | Responsibilities     |
|-----------------| ---------------------|
| Hellom        | Hardware Engineer |
| Marcelo       | Scrum Master |
| Nicole          | Software Engineer |
| Vinicius       | Software Engineer |
| Yasmine      | Software Engineer |

---

## 🎯 Objectives for this Sprint

- Full hardware integration: microcontroller, CAN, and speedometer
- Process real speed data using ThreadX 
- Develop CI/CD tools (linter, tests…)
- Validate and test solutions for voltage drops
- Automate tasks inside AGL

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83)

---
## 🗣️ Daily Standup Logs

| Date | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **24/11** | Hellom and Yasmine will assemble the hardware, integrating microcontroller, speedometer and CAN transceivers. Vinicius will continue the study and development to automate tasks in AG. Marcelo will study how to implement linter and understand its use inside GitHub Actions. Nicole will study the integration between speedometer and microcontroller. | - |
| **25/11** | Hellom will study how to implement the solution for the battery issues. Vinicius will develop scripts to automate tasks for AGL such as setup wifi and SSH services, and run the control car and instrument cluster programs as the raspberry starts. Nicole will continue the studies to integrate the speed detection code to ThreadX. Marcelo will study about linters and its implementation on CI/CD. | - |
| **26/11** | Hellom will run tests on the battery’s energy level so we can define a solution for the current battery issue. Nicole will continue the studies to integrate the speed detection code to ThreadX. Vinicius and Marcelo will develop a Docker container that simulates the AGL environment using the Raspberry Pi 5 architecture. Yasmine will work on improving the CAN protocol performance. | - |
| **27/11** | Hellom will develop a diagram to illustrate the energy architecture and implement the solution he proposed. Yasmine will work on changing the method the microcontroller uses to read speed data. She will implement interrupt-based reading, improving performance and CPU usage. Vinicius will research how to receive speed data on the Raspberry Pi, in C++, coming from the microcontroller through the SPI protocol. Marcelo will continue developing the Docker container to enable cross-compiling our existing Qt project inside the container. Nicolew ill continue the studies to integrate the speed detection code to ThreadX | Nicole is facing some difficulties debugging the speed-detection code in the STM32 IDE. |

## 🧠 Key Achievements

- [Summary of what was achieved]

---

## ⚙️ Pending for next sprint

- [Items not completed or blocked]

