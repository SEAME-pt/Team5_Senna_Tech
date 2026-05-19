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

---

## 🧠 Key Achievements

- [Summary of what was achieved]

---

## ⚙️ Pending for next sprint

- [Items not completed or blocked]
