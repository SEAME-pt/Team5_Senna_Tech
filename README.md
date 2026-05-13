# 🏎️ Team5_Senna_Tech  🏎️

## 📑 Index
- [Context](#-context)
- [Work Overview](#-work-overview)
- [System Objectives](#-system-objectives)
- [Repository Structure](#️-repository-structure)
- [Guidelines](#-guidelines)
- [Documentation](#-documentation)
- [Agile & Scrum Workflow](#-agile--scrum-workflow)
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
- Display a functional Qt GUI on the onboard screen
- Configure autonomous driving (motors, steering)
- Maintain traceable and documented software requirements
- Follow Scrum principles with documented sprints

## 🗂️ Repository Structure
```
├── .github/                           # Templates for issues and other GitHub configs
├── docker/                            # Docker configuration for cross-compilation
├── docs/                              # Project documentation
│   ├── AGL/                           # AGL documentation
│   ├── cross_compilation/             # Cross-compilation documentation
│   ├── energy/                        # Energy consumption analysis and datasheets
│   ├── pictures/                      # Project images and diagrams
│   ├── sprints/                       # Sprint reports and goals
│   ├── ThreadX/                       # ThreadX related documentation
│   └── TSF/                           # Trustable Software Framework documentation
├── reqs/                              # Requirements and specifications
│   └── templates/
├── scripts/                           # Utility and environment scripts
│   └── trudag/
└── src/                               # Main source code
    ├── car_cluster/                   # Qt-based car cluster GUI
    ├── car-control/                   # C++ source for car control (PiRacer)
    └── threadx/                       # ThreadX examples and source code
```

## 🧭 Guidelines
All guidelines were developed by the entire team to ensure the best standard for work efficiency. All information can be found at [git_guidelines.md](docs/git_guidelines.md)


## 🧾 Documentation
All documentation is kept inside the [docs/](docs/) folder.
## 🧱 Agile & Scrum Workflow
- **Methodology:** Scrum
- **Sprints:** 2-week sprints
- **Tools:** GitHub Projects + Issues

👥 Team
| Name            | Responsibilities                                 |
|-----------------|--------------------------------------------------|
| Hellom          | Execution pipeline refactoring                   |
| Vinicius        | Object detection refinement                      |
| Jose            | Adaptive Cruise Control (ACC) implementation     |
| Yasmine         | Obstacle Avoidance implementation                |
| Marcelo         | ---                                              |

All progress can be seen in [Projects](https://github.com/orgs/SEAME-pt/projects/83)

## 🗓️ Sprint Status
- **Current sprint**: Sprint 13
- **Period**: May 11 to May 22, 2026  [11/05/2026] → [22/05/2026]
- **Current Status**: In Progress
- **Goals**: Refine object detection, implement ACC and Obstacle Avoidance, and refactor the execution pipeline.
