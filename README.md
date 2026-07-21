# 🏎️ Team5_Senna_Tech  🏎️

## 📑 Index
- [Context](#-context)
- [Work Overview](#-work-overview)
- [System Objectives](#-system-objectives)
- [Repository Structure](#️-repository-structure)
- [Installation & Run Guide](#-installation--run-guide)
- [Guidelines](#-guidelines)
- [Documentation](#-documentation)
- [Agile & Scrum Workflow](#-agile--scrum-workflow)
- [Sprint Status](#️-sprint-status)

## 🌐 Context

This repository hosts the work of **Team 5 – SennaTech** as part of the **SEA:ME Portugal (Software Engineering in Automotive and Mobility Ecosystems)** program.

Our development focuses on **autonomous driving systems**, **embedded programming** and **reliable software processes** using **agile methodologies**.

## 🎯 Work Overview

### 🚗 Theme
Building a autonomous vehicle (PiRacer) powered by Raspberry Pi 5, STM32 microcontroller, sensors, HAILO AI.

### 🧩 Learning Goals

1. **Hardware Familiarization**
   - Raspberry Pi 5 setup
   - HAILO AI Hat assembly
   - Servo and DC motor configuration
   - Camera and display integration
   - Sensor integration and calibration

2. **Embedded Systems & RTOS**
   - RTOS concepts and multitasking
   - ThreadX development and scheduling
   - CAN communication
   - Embedded real-time software development
   - STM32 microcontroller integration

3. **Autonomous Driving & ADAS**
   - Lane Following Assist (LFA)
   - Lane Keeping Assist (LKA)
   - PID steering control
   - Obstacle avoidance
   - Traffic sign and object detection
   - Decision-making pipelines

4. **Machine Learning & Computer Vision**
   - Training lane detection models
   - Training object detection models
   - YOLO-based perception systems
   - Dataset preparation and validation
   - HAILO model conversion and optimization

5. **Simulation & Validation**
   - CARLA Simulator integration
   - Autonomous driving scenario testing
   - ROI calibration and validation pipelines

6. **Qt GUI Development**
   - Embedded Qt/QML graphical interface
   - Instrument cluster development
   - Vehicle telemetry visualization

7. **Automotive Middleware & Communication**
   - KUKSA integration
   - Vehicle Signal Specification (VSS)
   - uProtocol experimentation

8. **Agile (Scrum) Practices**
   - Sprint planning and retrospectives
   - Backlog management
   - GitHub Projects as Scrum board

9. **Version Control (Git & GitHub)**
   - Branching strategy
   - Pull request workflow
   - Code review & CI/CD pipelines

10. **Trustable Software Framework (TSF)**
   - Requirement definition
   - Architecture Decision Records (ADR)
   - Traceability between requirements, design, and tests

11. **GenAI Pair Programming**
   - Use of generative AI tools for pair programming
   - AI-assisted debugging and documentation

## 📈 System Objectives
- Display a functional Qt-based instrument cluster
- Configure driving systems (Throotle and steering)
- Implement Lane Following Assist (LFA)
- Implement Traffic Sign & Object Detection
- Develop obstacle avoidance strategies
- Integrate PID steering control with perception models
- Enable CAN-based communication between modules
- Support RTOS-based sensor and task management
- Maintain traceable and documented software requirements
- Follow Scrum principles with documented sprints

## 🗂️ Repository Structure
```
├── ADAS/                                # Autonomous driving and AI pipelines
│   ├── CARLA-Simulator/                 # CARLA simulator environment and tests
│   ├── LFA/                             # Lane Following Assist models and datasets
│   ├── Object_Detection/                # Object detection training and inference
│   └── pipeline/                        # Integrated ADAS processing pipeline
│
├── convert_hailo/                       # HAILO model conversion and deployment
│   ├── convert_flow/                    # Automated conversion pipeline
│   ├── docs/                            # Conversion documentation
│   ├── object-detection/                # Object detection conversion flow
│   ├── shared_with_docker/              # Shared Docker resources
│   └── yolo26_seg/                      # YOLO segmentation conversion tools
│
├── docker/                              # Docker environment and cross-compilation
│
├── docs/                                # Project documentation
│   ├── ADAS/                            # ADAS system documentation
│   ├── ADR/                             # Architecture Decision Records
│   ├── AGL/                             # Automotive Grade Linux documentation
│   ├── CARLA-Simulator/                 # CARLA setup and usage
│   ├── car_control/                     # Vehicle control documentation
│   ├── COVESA/                          # VSS and automotive standards
│   ├── cross_compilation/               # Cross-compilation setup
│   ├── energy/                          # Power and energy analysis
│   ├── GITHUB/                          # Git workflow and contribution guides
│   ├── hardware/                        # Hardware integration and wiring
│   ├── KUKSA/                           # KUKSA integration documentation
│   ├── MPC/                             # Model Predictive Control research
│   ├── odometer/                        # Odometer implementation
│   ├── OTA/                             # OTA and cluster documentation
│   ├── Parking/                         # Parking assistance system
│   ├── PID/                             # PID controller documentation
│   ├── pictures/                        # Images and diagrams
│   ├── piracer/                         # PiRacer setup and guides
│   ├── raspberry-pi-5/                  # Raspberry Pi configuration
│   ├── Servo_MG996R/                    # Servo motor documentation
│   ├── sprints/                         # Sprint reports and planning
│   ├── Tests/                           # Testing documentation
│   ├── ThreadX/                         # RTOS and ThreadX documentation
│   ├── trustable/                       # Trustable software reports
│   ├── TSF/                             # Trustable Software Framework
│   ├── uProtocol/                       # uProtocol experiments
│   └── VPN/                             # VPN setup and usage
│
├── scripts/                             # Utility scripts
│   ├── ci-cd/                           # CI/CD scripts
│   └── system/                          # System monitoring scripts
│
├── src/                                 # Main source code
│   ├── car_cluster/                     # Qt/QML instrument cluster
│   ├── car-control/                     # Vehicle control software
│   ├── Kuksa/                           # KUKSA integration and CAN mapping
│   ├── pid_control/                     # PID controller implementation
│   └── threadx/                         # ThreadX RTOS applications
│
├── tests/                               # Unit, integration and system tests
│   ├── integration-tests/
│   ├── unit/
│   └── tests/
```

## 📥 Installation & Run Guide

A complete, step‑by‑step guide to install and run the **entire system on a brand‑new car** with the same components — from hardware assembly and STM32 flashing, through AGL/Hailo setup, to launching the autonomous pipeline — is available in **[INSTALL.md](INSTALL.md)**.

It covers:
- Bill of materials & PiRacer / STM32 hardware assembly
- Building & flashing the STM32 ThreadX firmware
- Building & flashing the AGL image (Raspberry Pi 5) with Hailo + camera + custom layers
- Hailo‑8 PCIe fix, CAN interface, camera setup
- Docker cross‑compilation of the Qt cluster & gamepad control
- ADAS pipeline Python deps, Hailo model conversion, and deployment
- Kuksa middleware (Databroker + CAN Provider)
- Running the standard Lane Following Assist and the Robotaxi mission, with a quick‑start checklist and troubleshooting

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
- **Period**: May 11 to May 22, 2026  [11/05/2026] → [22/11/2026]
- **Current Status**: Finished
- **Goals**: Finish the ADAS Module
