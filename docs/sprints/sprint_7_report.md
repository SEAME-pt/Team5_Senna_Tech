
# 🚀 Sprint 7 Report – Team5: Senna Tech

**Duration:** [31/01/2026] → [13/02/2026]

**Sprint Goal:** Development of unit and integration tests, modernization of the instrument cluster UI

## 🎯 Objectives for this Sprint

- Develop unit and integration tests, to validate requirements
- Modernize Qt instrument cluster interface by improving its visual design, code structure, and overall maintainability
- Reorganize the repository architecture
- Implement new CAN messages ID’s (Emergency Stop, Heartbeat)
- Refactor TSF Requirements
- Integration of tests into GitHub Actions workflows
- Investigate and fix the speed capture bug

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+6)

---

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **02/02** | The team better discussed initial questions, helping with the development of tha planning presentation. Yasmine will work on the refactoring of the repository structure, Vinicius will investigate the speed capture bug, Hellom will refactor the speedsensor requirements and Marcelo will start searching about the improvement of cluster UI | - |
| **03/02** | Hellom will investigate EXP-202 to mitigate errors on capturing speed signals. Vinicius will continue refactoring TSF requirements related to the system and start the development of unit tests for ThreadX. Marcelo will continue the design of the new cluster version. Yasmine will implement the new CAN IDs and link the CAN tests to TSF structure. | - |
| **04/02** | Hellom will adjust the hardware to mitigate errors on capturing speed signals. Vinicius will continue the development of unit tests for ThreadX. Marcelo will continue the design of the new cluster version. Yasmine will evidence the CAN communication and link the tests to TSF structure. | - |
| **05/02** | Hellom repaired the speed sensor hardware and verified signal capture using an oscilloscope. Today, he will document the process as evidence for requirement. Vinicius developed unit tests for ThreadX, identifying minor issues and optimizing the code. He will document the process and automate the process by adding it to the GitHub Actions workflow. Marcelo will continue the design of the new cluster version, by working on the development of the display components. Yasmine validated CAN communication, securing evidence for latency and data integrity in alignment with the TSF structure. She will design a base image for the cluster new version. | A servo motor was damaged. The team is investigating the cause and suspects it happened due to a data overflow.|
| **06/02** | Hellom created an evidence for EXP-202 requirement, linking it into TSF structure, today he will work on reviewing all the work made in this module, to prepare the Retrospective presentation. Vinicius added unit tests to GitHub Actions workflow and will work on the development of evidences for TSF requirements. Marcelo will continue the design of the new cluster version, by working on the development of the display components. Yasmine will design a base image for the cluster new version.
| **09/02** | Hellom is going to replace the servo motor with a brand-new one and reorganize the hardware, shortening any unnecessary wiring to improve the vehicle's organization Vinicius is finishing the integration tests related to the system requirements and will fix the battery inconsistent values bug. Marcelo and Yasmine will continue the design of the new cluster version.
| **10/02** | Hellom will continue to improve the vehicle hardware organization Vinicius will develop a method to calculate the vehicle's range. Marcelo and Yasmine will continue the design of the new cluster version, by adding new assets such as buttons, traffic signs, warnings, battery and autonomy figures.

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