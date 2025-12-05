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
| **28/11** | Yasmine will work on get the pulses coming from the speedsensor to the Raspberry Pi 4 through CAN protocol. Hellom will work on developing a presentation explaining all his research and solution proposed to the power consumption architecture. Marcelo will continue to implement cross-compilation of Qt projects inside the AGL docker. Vinicius will continue to implement the speed detection code inside teh Raspberry Pi 5 through CAN communication. Nicole overcame her blocker yesterday and now can read the speedometer pulses inside the microcontroller with ThreadX, and today she will document all the process. | - |
| **02/12** | Vinicius and Yasmine will work integrating the CAN protocol communication between microcontroller and Raspberry Pi 5 with AGL. Nicole will work on migrate the CAN protocol code we have to the ThreadX RTOS. Hellom will work on preparing a presentation for the team about the battery issues and potential solutions. Marcelo will work on setting up the Docker environment to support cross-compilation of the Qt instrument cluster. | Marcelo is facing difficulties about the dependencies between host (x_86_64) and target (arm64) architectures inside the docker. |
| **03/12** | Nicole will work on migrate the CAN protocol code we have to the ThreadX RTOS. Vinicius will start a research about unit tests, how to implement it in our project and define which tool we will use for tests. Yasmine will work on documenting the new code for the CAN protocol. Hellom will work on preparing a presentation for the team about the battery issues and potential solutions. Marcelo will work on setting up the Docker environment to support cross-compilation of the Qt instrument cluster. | Marcelo is still facing difficulties about the dependencies between host (x_86_64) and target (arm64) architectures inside the docker. |
| **04/12** | Yasmine will work on documenting the new code for the CAN protocol. Nicole will document her achievement, describing the implementation of CAN communication inside ThreadX. Marcelo will work on documenting the AGL Docker setup for Qt and C++ cross-compiling. Vinicius and Hellom will work on integrating all the hardware components in the car. | - |

## 🧠 Key Achievements

- The speedometer was successfully integrated into the system: the data is processed by the microcontroller running ThreadX and then transmitted to the Raspberry Pi using the CAN protocol over an SPI interface.
- All the software can be cross-compiled inside a docker container that replicates AGL environment.
- The battery issue investigation was validated, and new components were integrated, fixing the problems.
- AGL was fully configured with all the required dependencies to operate our software.

---

## ⚙️ Pending for next sprint

- Development of CI/CD tools
- Unit tests implementation

