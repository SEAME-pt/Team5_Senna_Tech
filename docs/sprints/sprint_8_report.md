# 🚀 Sprint 8 Report – Team5: Senna Tech

**Duration:** [23/02/2026] → [06/03/2026]

**Sprint Goal:** Define the initial architecture of our ADAS

**Team Roles:**
| Name     | Responsibilities              |
|----------|-------------------------------|
| Hellom   | Scrum Master / Hardware       |
| Vinicius | Camera Software Resources     |
| Jose     | Team Integration              |
| Yasmine  | ADAS Module Research          |
| Marcelo  | ADAS Module Research          |

---

## 🎯 Objectives for this Sprint

- First steps with CARLA and OpenCV to understand how they work
- Understand the different objectives of this module to define and organize task priorities
- Install the ultrasonic sensor and camera, both in hardware and software
- Study the implementation of the PID (Proportional-Integral-Derivative) controller in motors
- Study the implementation and operation of the Hailo-8 AI HAT

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83)

---

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **23/02** | **Hellom:** Will mount and study the ultrasonic sensor and camera, update GitHub and prepare the planning presentation. **Marcelo:** Will document the odometer update, update the retrospective presentation, create an ADAS module study issue and start studying the module's objectives. **Vinicius:** Will explore camera initialization, create a Hailo-8 study/implementation issue, update the AGL layers presentation for Hailo and document the Hailo base setup on AGL. **Jose:** Created a PID study issue and will study the ultrasonic sensor. **Yasmine:** Day off – travelling. | Jose found a bug in the STM files related to an include directive. |
| **24/02** | **Hellom:** Physically mounted the sensor with 5V and GND power (echo and trigg connections pending), planning presentation went positively, performed mechanical adjustments on the car for better stability. Will update GitHub, open bug and sensor issues and review PRs. **Marcelo:** Submitted PR for odometer documentation, updated retrospective presentation, created ADAS study issue. Will continue studying the module topics. **Vinicius:** Created Hailo-8 study/implementation issue, updated AGL layers presentation for Hailo, submitted PR for the Hailo AGL base documentation, and confirmed that the camera is recognised by the system. Will install OpenCV and camera dependencies on AGL. **Jose:** Created PID study issue and began studying the ultrasonic sensor. Focused on 42 exam – no further tasks planned. **Yasmine:** Day off – travelling. | Sensor mounting incomplete – echo and trigg pins not yet connected. |
| **25/02** | **Hellom:** Connectivity issues prevented planned work. Will update GitHub, create bug and sensor issues, confirm the board and open issues, review PRs and attend the standup meeting. **Marcelo:** Personal matters. Will continue studying the module topics. **Vinicius:** Installed OpenCV and camera drivers and ran initial image display tests. Will continue working on camera functionality. **Jose:** Studying for 42 exam. **Yasmine:** Rest day. Will study and prepare the objectives presentation. | Hellom had internet connectivity issues. |
| **26/02** | **Hellom:** PR for Hailo AGL layers installation documentation approved. Deleted unused branches and closed completed PRs. Submitted PR to sync develop with commits incorrectly pushed to main. Researched other teams' camera implementations and attended meeting with SEA:ME's Maria. Updated GitHub, created STM bug issue and ultrasonic sensor issue, attended standup. Will research and contribute to camera implementation, focusing on Raspberry Pi 5 camera integration with AGL/Yocto. **Vinicius:** Modified AGL pipelines for libcamera but camera is still not opening. Will continue resolving camera implementation. **Yasmine:** Continued preparing the general ADAS module concept presentation. Will finish the ADAS general concepts presentation on 27/02. **Jose:** OFF – studying for 42 exam. Will study the ultrasonic sensor. **Marcelo:** Ran initial functionality tests with YOLO-Ultralytics. Will investigate OpenCV for lane detection. | Camera not yet functional after AGL pipeline modifications. Note: TSF presentation to DANA scheduled for 03/03/2026. Idea raised for 2–3 AI models (Track, Object and Road Signs detection). |
| **27/02** | **Hellom:** Researched and shared useful information with Vinicius. Will study AGL architecture and help configure AGL for camera functionality, and discuss with the team the task division and initial ADAS architecture following Yasmine's presentation. **Yasmine:** Finished assembling the presentation. Will present and discuss the initial ADAS architecture and task division with the team. **Vinicius:** Still blocked on the camera issue. Will continue testing, researching and adjusting AGL recipes to get the camera working with libcamera. **Jose:** Took the 42 exam. Will verify STM functionality and related ThreadX code, and study the ultrasonic sensor. **Marcelo:** Started studying car modelling and abstraction inside CARLA. Will begin studying model training. | Vinicius remains blocked on camera implementation. After Yasmine's presentation, the team decided to split: 2 members will study PID or MCP control and 3 members will divide between AI analysis concepts and application. Architectural decision: ultrasonic sensor will not be included in the initial architecture but is not discarded for future updates if needed. |

---

## 🧠 Key Achievements

-

---

## ⚙️ Pending for next sprint

-
