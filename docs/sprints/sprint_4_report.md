# 🚀 Sprint 4 Report – Team5: Senna Tech

**Duration:** [09/12/2025] → [19/12/2025]

**Sprint Goal:** Investigation for OTA update implementation

**Team Roles:**
| Name            | Responsibilities               |
|-----------------| ------------------------------ |
| Hellom          | Scrum Master                   |
| Marcelo         | CI/CD                          |
| Nicole          | TSF                            |
| Vinicius        | OTA                            |
| Yasmine         | COVESA & uProtocol Researcher  |

---

## 🎯 Objectives for this Sprint

- Research and choose an OTA update framework/tool.
- Develop a proof-of-concept for the OTA update mechanism.
- Integrate the OTA solution into the AGL environment.
- Document the OTA update process.

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83)

---

## 🗣️ Daily Standup Logs

| Date | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **09/12** | Nicole: TSF update. Vini: OTA study. Yasmine: uProtocol and COVESA investigation. Marcelo: AGL compilation automation in docker via github action. Hellom: battery energy presentation and TeamViewer viability check. | |
| **10/12** | Nicole: Continues TSF update. Yasmine: Continues uProtocol and COVESA investigation. Marcelo: Continues AGL compilation automation in docker via github action. Hellom: Continues battery energy presentation and TeamViewer viability check. Vini: Study CI/CD implementation in GitHub. | |
| **11/12** | Yasmine will upload her documentation on uProtocol's functioning and start studying COVESA. Marcelo continues his mission to automate docker compilation in GitHub Actions. Vinicius has already implemented a small test on GitHub and plans to do further study to upload documentation on it. Hellom continues studying and creating a presentation on SEAME's electronics and configuring TeamViewer on the school PC. | |
| **12/12** | Nicole continues to study the implementation of TSF with the goal of creating a functional test to generate an initial report. Following his study on Pipelines in GitHub Actions, Vinicius documented the path to performing the first automated test and will now work on implementing Google Tests in GitHub Actions as well. Marcelo remains on the task of automating the system's compilation via Docker. Yasmine continues to study and implement COVESA, uProtocol, and their relationship with the CAN protocol. Hellom is looking for an alternative to TeamViewer to work remotely on the local PC and continues to assemble slides to present the car's energy issue to the group. | |
| **15/12** | Vinicius has successfully implemented an initial test for Google Test in GitHub Actions, updated the documentation, and will now proceed with studying OTA updates to continue the work. Marcelo has successfully automated system compilation in Docker and will move on to creating initial QT system tests for implementation in GitHub Actions. Nicole continues with the creation of the initial program to generate a first TSF test report. Yasmine has gained a solid foundation in COVESA and uProtocol and will proceed with initial study tests for their implementation. Hellom has finalized the creation of the car's energy presentation, will proceed with collecting battery and motor data via the I2C protocol, but first needs to complete the installation of some software that allows remote work on the system; Google Remote is a possibility. | |
| **16/12** | Vinicius: After studying the general concepts of OTA and presenting them to the team, he decided to focus on OTA for the QT part, as it would be a feasible implementation study until the end of the sprint. Marcelo: Started creating tests related to the cluster's functionality for future implementation in the GitHub testing workflow. Yasmine: Finished the initial study of COVESA and uProtocol and will proceed with documentation. Nicole: Continues with the implementation of TSF using Trudag to generate the initial score. Hellom: Focused on finalizing the presentation for the next day and continuing the viability of VPN for remote access to the car's system. | |
| **17/12** | Yasmine: Finished the documentation and will prepare a small presentation for the team to understand her findings and suggestions. Marcelo: Finished the initial tests for QT and will document them. Vinicius: Made progress on automating QT updates remotely and is moving towards a verification script in the car's system (AGL) that checks for updates. Nicole: Managed to generate a script with a score not yet based on real requirements but concluding her objective, which was to do an initial test to enable the requirements workflow. She will proceed with documenting this. Hellom: Made progress on implementing tools for remote access and will proceed with the presentation to the team on this day about the car's energy and how it works. | |
| **18/12** | Yasmine, with help, installed and configured the VPN for remote access to our car system, and presented the conclusion of her studies with COVESA and uProtocol to the team. She is now in charge of uploading the result to a PR to finalize the sprint. Marcelo continues with the documentation of the tests, the study of CI/CD, and the preparation of slides to report his findings in the retrospective. Vini managed to finalize a script for remote QT updates, thus concluding our initial objective of implementing an OTA update in an MMVP concept. Unfortunately, the documentation for this will be left for the next sprint, and he will continue with the preparation of an explanation of the process for the team and for the retrospective, and finalize his modifications by uploading the code to the develop branch. Nicole finished the documentation on her feasibility study for the implementation of TSF and is in charge of uploading it to GitHub with the finalization of the issue for the retrospective. Hellom worked on the car reorganizing cables and implementing the Hailo and SSD hardware in the physical system for a future update. He is also in charge of starting to update the daily documentation, updating GitHub for the retrospective, and preparing the presentation. It was suggested to all members that after finishing their work for the day, they should not have a defined objective for the next day, leaving the day just for the retrospective. | |
| **19/12** | Sprint retrospective day. | |

---

## 🧠 Key Achievements

- [Summary of what was achieved]

---

## ⚙️ Pending for next sprint

- [Items not completed or blocked]
