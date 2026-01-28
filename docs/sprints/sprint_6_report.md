
# 🚀 Sprint 6 Report – Team5: Senna Tech

**Duration:** [19/01/2026] → [30/01/2026]

**Sprint Goal:** [Motor Control Migration and Communication Refinement.] 

## 🎯 Objectives for this Sprint

#### Goal 1 - Migrate DC and Servo control to STM32 and ThreadX

Currently, the I2C communication reaching the motors is handled by the Raspberry Pi. The goal here is to completely migrate the code that sends the pulses so that it runs inside a thread on the STM32 using an RTOS (ThreadX).

- [Threads Architecture](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6&pane=issue&itemId=150468082&issue=SEAME-pt%7CTeam5_Senna_Tech%7C161)
- [Migrate and adapt code](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6&pane=issue&itemId=150469564&issue=SEAME-pt%7CTeam5_Senna_Tech%7C164)


#### Goal 2 - Implement KUKSA
Implement KUKSA with the goal of centralizing and standardizing data, creating greater scalability for the project.

- [Kuksa Architecture](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6&pane=issue&itemId=150482982&issue=SEAME-pt%7CTeam5_Senna_Tech%7C166)
- [Kuksa Implementation](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6&pane=issue&itemId=150470035&issue=SEAME-pt%7CTeam5_Senna_Tech%7C163)

#### Goal 3 - Instrument Cluster Improvements

Improve desing and prepare for future additions.

- [Instrument Cluster](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6&pane=issue&itemId=150353754&issue=SEAME-pt%7CTeam5_Senna_Tech%7C160)


---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6)

---

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **19/01** | The team better divided the responsibilities, planned the presentation for the planning session, and discussed initial questions.  | - |
| **20/01** | Marcelo and Yasmine have started researching KUKSA, covering how to create and consume the data broker and adding it to the AGL image, while Hellom is studying STM32 pinouts and datasheets, Vinícius is delving into ThreadX. | - |
| **21/01** | Hellom will work through the night modifying the I2C cables from the Raspberry Pi to the STM32 and verifying the feasibility of the I2C addresses, while Vinícius has defined the initial architecture for the RTOS threads and aims to have them created by the end of the day, as Marcelo added KUKSA to the system and transferred the legacy files, Yasmine completed and documented the CAN decoder files and Nicole is searching for image references to improve the IC. | - |
| **22/01** | Hellom connected the cables and successfully identified the I2C addresses between the board and the STM32, while Vinícius managed to migrate the code from C++ to C within the microcontroller threads and validated that the I2C can move the car via the STM, and Yasmine and Marcelo are working on the vehicle's CAN decoder (DBC) to translate CAN bits into readable values such as speed, battery status, motor power, and steering angle. | - |
| **23/01** | Vinicius will handle the joystick code to send commands via CAN to the STM. Hellom will take care of the documentation and VPN adjustments. Marcelo will prepare a new AGL build with the new Kuksa dependencies, and Yasmine will run tests and validate the CAN provider implementation. | - |
| **26/01** | Vinicius will refactor and organize the STM32 code. Hellom continues working on the team’s VPN adjustments. Marcelo transferred the files from the old system to the new one and is starting the process to compile KUKSA in the CI/CD pipeline, while Yasmine will research how we can perform latency tests. | - |
| **27/01** | The team continues with the same tasks as the previous day. | - |
| **28/01** |  | - |
| **29/01** |  | - |
| **30/01** |  | - |

---

## 🧠 Key Achievements

- 
- 
- 
- 
- 
- 

---

## ⚙️ Pending for next sprint

- 
- 