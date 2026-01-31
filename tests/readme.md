# Testing Documentation

This document outlines the testing strategy, explaining the differences between our test suites and when to use each one. Given the safety-critical nature of the project, we strictly follow the testing pyramid to ensure system reliability.

## Directory Structure

```text
tests/
├── unit/            # Math, logic, and algorithm validation
├── integration/     # Communication between software nodes (e.g., Perception -> Planning)
└── functional/      # High-level behavior and safety scenarios (Simulation/E2E)
```

## 1. Unit Tests (``/unit``)

**Focus:** Mathematical algorithms, sensor data parsing, and pure logic.

**Objective:** To verify that individual functions (like a PID controller or a distance converter) work with 100% accuracy.

**Isolation:** No hardware or simulators involved. We use fixed input data.

**Example:  (C / speed measurement)**
To test if the code correctly converts pulses to km/m.

## 2. Integration Tests (``/integration``)

**Focus:** Testing the "handshake" between different software modules or nodes.

**Objective:** To ensure that the "Perception" module correctly sends detected obstacles to the "Path Planner" in the expected format.

**Environment:** Middleware-based (e.g., ROS2, Cyber RT) using recorded data (rosbags) or virtual bridges.

**Example: (Python / ROS2)**
Checking if the Object Detector node correctly publishes a "Pedestrian" label when processing a specific sensor frame

```bash
def test_perception_to_planning_flow():
    # Setup: Initialize the Perception Node
    # Action: Inject a synthetic camera frame with a pedestrian
    perception_node.feed_frame(pedestrian_image)
    
    # Assert: Verify if the /planning/obstacles topic received the correct data
    msg = wait_for_topic_message('/planning/obstacles')
    assert msg.detected_object == "pedestrian"
    assert msg.confidence > 0.98
```

## 3. Functional Tests (``/functional``)

**Focus**: End-to-End vehicle behavior and safety requirements.

**Objective:** To verify if the vehicle completes a full business or safety requirement (e.g., "The car must stop for a red light").

**Environment:** Full-stack simulation (CARLA, SVL, or Gazebo) or Hardware-in-the-Loop (HiL).

**Example: (Emergency Braking Scenario)**

Testing the Automatic Emergency Braking (AEB) system:

Setup: Vehicle is cruising at 50km/h.

Scenario: A child-sized obstacle enters the lane 20meters ahead.

Success Criteria: The vehicle must apply brakes and come to a full stop without collision.

```bash
# Scenario Definition
test_case: emergency_braking_child_dummy
initial_conditions:
  speed: 50km/h
  weather: clear
trigger:
  obstacle_appearance: 20m
expected_outcome:
  collision: false
  min_distance_to_obstacle: 0.5m
```

## Summary Comparison

| Type | Focus | Key Risk Mitigated |
| :--- | :--- | :--- |
| **Unit** | Algorithms | Mathematical and logical bugs |
| **Integration** | Interfaces | Data loss or format mismatch between nodes |
| **Functional** | Behavior | Real-world safety failures and crashes |