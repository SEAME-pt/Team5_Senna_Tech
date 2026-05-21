# 📄 Project Documentation

This directory contains all the technical and process-related documentation for the project. Below is a table of contents to help you navigate through the different documents.

---

## 📚 Table of Contents

---

### 🔧 Git & Workflow
- [Git Guidelines](GITHUB/git_guidelines.md) - Standards for commit messages, branching strategy, and pull requests.
- [Git Workflow Guide](GITHUB/git_workflow_guide.md) - Detailed feature branching and release workflow.
- [GitHub Actions Overview](GITHUB/git_actions_overview.md) - CI/CD pipelines and automation overview.
- [Pull Request Guide](GITHUB/pull_request_guide.md) - Best practices for PR creation and review process.

---

### 🧠 Hardware & Setup
- [PiRacer Assembly Guide](piracer/piracer_assembly_guide.md) - Step-by-step guide to assemble the PiRacer vehicle.
- [Initial Program Installation](piracer/install_initial_program.md) - Setup instructions for required software stack.
- [Raspberry Pi System Setup](raspberry-pi-5/raspberry_Pi_system.md) - Configuration of Raspberry Pi OS and NVMe SSD setup.
- [STM32 Motor Wiring](hardware/stm32_motor_wiring.md) - Wiring and hardware integration for motor control.
- [VPN & Remote Access Guide](VPN/vpn_install_usage.md) - Remote access using NetBird and TigerVNC.

---

### 🎮 Car Control
- [Joystick Control - Python](car_control/joystick_control_python.md) - Python-based joystick control implementation.
- [Joystick Control - C++](piracer/piracer-cpp.md) - C++ implementation for vehicle control logic.
- [Car Control Instructions](car_control/car_control_instructions.md) - General car control setup and usage guide.

---

### 🏁 ADR (ADAS & Autonomous Systems)
- [Lane Detection Model ADR](ADR/001-model-lane-detection.md)
- [Object Detection Model ADR](ADR/002-model-object-detection.md)
- [FSM Design (Decision System)](ADR/003-FSM.md)
- [Obstacle Avoidance ADR](ADR/004-obstacle-avoidence.md)
- [Lane Following Assist (LFA)](ADAS/LFA.md)
- [Obstacle Avoidance System](ADAS/obstacle_avoidence.md)

---

### 🏗️ Software Architecture & Frameworks
- [AGL (Automotive Grade Linux)](AGL/readme.md) - Embedded Linux platform integration and setup.
- [Cross Compilation](cross_compilation/README.md) - Toolchain and cross-build environment.
- [Energy Management](energy/README.md) - Energy analysis, consumption modeling and optimization.
- [KUKSA](KUKSA/README.md) - Vehicle signal and middleware integration.
- [COVESA / VSS](COVESA/COVESA.md) - Vehicle Signal Specification and conventions.
- [uProtocol](uProtocol/uProtocol.md) - Communication framework exploration.
- [ThreadX RTOS](ThreadX/system_setup_and_LED_priority_demonstration.md) - Real-time operating system documentation.
- [Odometer System](odometer/README.md) - Vehicle distance tracking system.
- [Parking System](Parking/parking_system.md) - Autonomous parking logic and design.
- [OTA / Instrument Cluster](OTA/InstrumentCluster.md) - Cluster and OTA-related systems.

---

### 🤖 AI / Simulation / ADAS Pipeline
- [CARLA Simulator Setup](CARLA-Simulator/carla_initial_setup.md) - Setup and integration with CARLA simulator.

---

### 🧪 Testing & Validation
- [C++ Linting Guide](Tests/cpp_linting.md) - Code quality and linting rules.
- [C++ Tests](Tests/cpp_tests.md) - Unit and system testing guidelines.

---

### 📊 Trustable Software Framework (TSF)
- [TSF Overview](TSF/README.md) - Introduction to TSF methodology.
- [TSF Concepts](TSF/tutorials/TSF-concepts.md) - Core TSF concepts.
- [TSF Applied Guide](TSF/tutorials/TSF-applying.md) - Practical application of TSF.
- [ISO 26262 Structure](TSF/tutorials/ISO26262-structure-and-concepts.md) - Functional safety foundation.
- [Requirements & Assumptions](TSF/reqs/) - System requirements
- [Decision Support](TSF/Decision_support/) - Engineering decisions and hazard analysis.


---

### 🧱 Sprint & Agile Management
- [Sprint Overview](sprints/README.md) - Agile sprint structure and tracking.
- [Sprint Reports](sprints/) - Detailed reports for each sprint iteration.

---

### ⚡ Energy & Hardware Analysis
- [Energy Consumption Analysis](energy/energy_consumption_analysis.md)
- [Power Architecture Solution](energy/power_architecture_solution.md)
- [Component Datasheets](energy/components_datasheet.md)
- [Spreadsheet Guide](energy/spreadsheet_guide.md)


**Sprints & Process**
- [Sprints](./sprints/README.md) - Contains all sprint reports and goals.
  - [Sprint Goals](./sprints/Sprint_Goals.md)
  - [Sprint 0 Report](./sprints/sprint_0_report.md)
  - [Sprint 1 Report](./sprints/sprint_1_report.md)
  - [Sprint 2 Report](./sprints/sprint_2_report.md)
  - [Sprint 3 Report](./sprints/sprint_3_report.md)
  - [Sprint 4 Report](./sprints/sprint_4_report.md)
  - [Sprint 5 Report](./sprints/sprint_5_report.md)
  - [Sprint 6 Report](./sprints/sprint_6_report.md)
  - [Sprint 7 Report](./sprints/sprint_7_report.md)
  - [Sprint 8 Report](./sprints/sprint_8_report.md)
  - [Sprint 9 Report](./sprints/sprint_9_report.md)
  - [Sprint 10 Report](./sprints/sprint_10_report.md)
  - [Sprint 11 Report](./sprints/sprint_11_report.md)
  - [Sprint 12 Report](./sprints/sprint_12_report.md)
  - [Sprint 13 Report](./sprints/sprint_13_report.md)
  - [Sprint Template](./sprints/sprint_template.md)
