# 🚀 Sprint 13 Report – Team5: Senna Tech

**Duration:** [11/05/2026] → [22/05/2026]
**Sprint Goal:** Advanced ADAS Features Integration and Pipeline Optimization

**Team Roles:**
| Name            | Responsibilities     |
|-----------------| ---------------------|
| Hellom          | Execution pipeline refactoring |
| Vinicius        | Object detection refinement |
| Jose            | Adaptive Cruise Control (ACC) implementation |
| Yasmine         | Obstacle Avoidance implementation |
| Marcelo         | On vacation |

---

## 🎯 Objectives for this Sprint

- Refine the Object Detection model and its inference efficiency (Vinicius).
- Implement Adaptive Cruise Control (ACC) logic for automatic speed adjustment (Jose).
- Implement detection and maneuvers for Obstacle Avoidance (Yasmine).
- Refactor the main execution pipeline to improve modularity and performance (Hellom).

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83)

---

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **11/05** | Sprint 13 planning and goal definition. | - |
| **12/05** | Team members started working on their respective defined tasks. | - |
| **13/05** | Work has been initiated for everyone across all planned fronts. | - |
| **14/05** | **Jose:** Worked on Adaptive Cruise Control (ACC). The car already recognizes another car and stops at a safe distance. Next, he will advance to the tracking logic so the car can follow the vehicle ahead. **Yasmine:** Ran the first Obstacle Avoidance tests, but without major results so far. **Hellom:** Worked on the study and documentation of the inference part of the pipeline. **Vinicius:** Pending. | Another servo motor burned out. |
| **15/05** | **Hellom:** Tested and studied the Python inference package, integrated lane and object detection post-processing modules, and updated documentation for all execution pipeline modules. Continued with study and refactoring. **Yasmine:** Successfully implemented Obstacle Avoidance but identified trajectory errors in curves. **Jose:** Identified another burned-out servo motor; trained the object detection model with expanded datasets to improve vehicle identification for ACC. **Vinicius:** Day off. | Another burned-out servo motor; Errors in curves. |
| **18/05** | **Hellom:** Converted the object detection model trained by Jose; continued with pipeline packaging and documentation. **Yasmine:** Updated code with Vinicius' object detection adjustments and fixed curve issues; started researching future modules and planning automatic parking implementation using ultrasonic sensors with Jose. Also responsible for cleaning up the code merged into the develop branch (Jose, Yasmine, and Vinicius' implementations). **Jose:** Finished Adaptive Cruise Control (ACC) and updated manual/autonomous mode with manual priority. **Vinicius:** Preparing a before/after video of FPS corrections to justify improved detection reliability. | Jose noted that ACC documentation currently resides only within code comments. |
| **19/05** | **Vinicius:** Retrained and converted the object detection model; completed object detection training documentation; produced a before/after documentary video showcasing the camera frame fix; started studying topics for the next module. **Yasmine:** Refactored the pipeline code and started working on the retrospective presentation. **Jose:** Finished the manual/automatic/parking mode restructuring and plans to open a PR; will mount the ultrasonic sensors on the car and update the electrical system with the connection ports between the STM and the two sensors — no additional sensor documentation planned beyond the electrical wiring update. **Hellom:** Continued pipeline refactoring following documentation standards. | - |
| **20/05** | **Vinicius:** Finished all pending documentation; began studying the next module; discussed with the team the challenge of building a robot taxi; explored microbit-based traffic light communication as a future requirement; plans to assemble a second car for remote control. **Jose:** Got one ultrasonic sensor working and ran first automatic parking tests; will study the viability of using two sensors and continue developing the parking algorithm. **Yasmine:** Worked on the retrospective presentation; assisted Jose with sensor assembly; recorded demonstration videos for the retrospective; started studying topics for the next module. **Hellom:** Finished the pipeline refactoring; plans to advance with testing on the Raspberry Pi, validation with the rest of the team, and updating the branches up to main. | - |
| **21/05** | **Hellom:** Final tests and adjustments on the issue #250 pipeline; adjusted retrospective content; plans to update the daily logs, open the issue PR, and ensure all pending PRs are merged up to main. **Yasmine:** Finished the retrospective content; did a brief study on Brisa Group technologies (next week's topic); started working on an emergency body design for the car; plans to upgrade the obstacle avoidance module. **Vinicius:** Started testing microbits for smart traffic light viability; second car assembly proved unfeasible due to defective parts; advanced with the refactoring of the project's main README for the main branch update. **Jose:** Finished the parking algorithm with a satisfactory success rate; opened a PR with the updated code; plans to open a PR for the additional joystick configuration. | - |
| **22/05** | Team dedicated to repository updates (pending PRs, branch merges up to main) and preparation for the Sprint 13 Retrospective presentation. | - |

---

## 🧠 Key Achievements

- [Summary of what was achieved]

---

## ⚙️ Pending for next sprint

- [Items not completed or blocked]
