# 🏎️ Team5_Senna_Tech  🏎️

## 📑 Index
- [Context](#-Context)
- [Work Overview](#-Work-Overview)
- [Repository Structure](#️-repository-structure)
- [Guidelines]( #-Guidelines)
- [How to Execute](#️-how-to-execute)
- [Documentation](#-documentation)
- [Agile & Scrum Workflow](#-Agile-&-Scrum-Workflow)
- [Sprint Status](#️-sprint-status)

## 🌐 Context

This repository hosts the work of **Team 5 – SennaTech** as part of the **SEA:ME Portugal (Software Engineering in Automotive and Mobility Ecosystems)** program.

Our development focuses on **autonomous driving systems**, **embedded programming** and **reliable software processes** using **agile methodologies**.

## 🎯 Work Overview

### 🚗 Theme
Building a miniature autonomous vehicle (PiRacer) powered by Raspberry Pi 5 and HAILO AI.

### 🧩 Learning Goals
1. **Hardware Familiarization**
   - Raspberry Pi 5 setup  
   - HAILO AI Hat assembly  
   - Servo and DC motor configuration  
   - Display integration  
2. **Qt GUI Development**
   - Design and implementation of an embedded graphical interface  
3. **Agile (Scrum) Practices**
   - Sprints, backlogs, retrospectives  
   - GitHub Projects as Scrum board  
4. **Version Control (Git & GitHub)**
   - Branching strategy  
   - Code review & CI/CD  
5. **Trustable Software Framework (TSF)**
   - Requirement definition  
   - Traceability between requirements, design, and tests  
6. **GenAI Pair Programming**
   - Use of generative AI tools for pair programming and code assistance  

## 📈 System Objectives
- Assemble and configure the PiRacer hardware  
- Display a functional Qt GUI on the onboard screen  
- Enable remote control of the PiRacer (motors, steering)  
- Maintain traceable and documented software requirements  
- Follow Scrum principles with documented sprints  

## 🗂️ Repository Structure
```
├── .github/                           # templates
├── docs/                              # Project documentation
├── src/                               # Main source code
│   ├── feature_[feature-name]/        # Specifc feature code
└── README.md                          # This file
```
See detals in [git_workflow_guide.md](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/git_workflow_guide.md)

## 🧭 Guidelines
All guidelines were developed by the entire team to ensure the best standard for work efficiency. All information can be found at [git_guidelines.md](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/git_guidelines.md)


## 🧾 Documentation
- All documentation will be kept inside the docs/ folder.
- During this sprint, files will be created explaining:
  - How car control was implemented
  - How to set up the development environment
  - Code structure and adopted standards

####  Table of Contents
- [Rules and Best Practices for Git](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/git_guidelines.md)
- [Git Workflow Guide](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/git_workflow_guide.md)
- [PiRacer Assembly Guide](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/piracer_assembly_guide.md)
- [Raspberry Pi OS Installation in SSD NVMe](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/raspberry_Pi_system.md)
- [Initial Program Installation](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/install_initial_program.md)
- [Joystick Car Control - Python](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/joystick_control_python.md)
- [Joystick Car Control - C++](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/piracer-cpp.md)
- [GitHub Actions Overview](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/git_actions_overview.md)
- [VPN and Remote Server Access Guide via NetBird + TigerVNC](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/vpn_install_usage.md)
- [Sprints](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/sprints/README.md)
  - [Sprint Goals](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/sprints/Sprint_Goals.md)
  - [Sprint 0 Report](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/sprints/sprint_0_report.md)
  - [Sprint 1 Report](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/sprints/sprint_1_report.md)
  - [Sprint Template](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/sprints/sprint_template.md)
- [TSF (Trustable Software Framework)](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/TSF/README.md)
  - [ISO 26262:2018 — Functional Safety for Road Vehicles](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/TSF/ISO26262-structure-and-concepts.md)
  - [Applying TSF to Automotive Projects](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/TSF/TSF-applying.md)
  - [TSF Learning Guide](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/docs/TSF/TSF-concepts.md)
## 🧱 Agile & Scrum Workflow
- **Methodology:** Scrum  
- **Sprints:** 2-week sprints  
- **Tools:** GitHub Projects + Issues  

👥 Team
| Name            | Responsibilities     |
|-----------------| ---------------------|
| Hellom          | Hardware Engineer    |
| Marcelo         | Scrum Master    |
| Nicole          |  Software Engineer        |
| Vinicius        |  Software Engineer  |
| Yasmine         | Software Engineer        |

All progress can be seen in [Projects](https://github.com/orgs/SEAME-pt/projects/83)

## 🗓️ Sprint Status
- **Current sprint**: Sprint 3
- **Period**: November 24 to December 07, 2025
- **Current Status**: 🟡 In Progress
- **Goals**: Integrate speedometer with hardware, processing data through ThreadX
