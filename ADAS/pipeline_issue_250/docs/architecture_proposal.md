# Architecture Proposal

## Introduction

The proposed architecture for the ADAS pipeline aims to create a robust, efficient, and modular system that allows for the continuous evolution of the project without compromising code quality or system performance. This proposal defines rules for code organization, separation of responsibilities between modules, the structure of `main`, and how new features should be integrated into the pipeline.

The principles adopted in this proposal are as follows:

1. **Layer Concept:** based on "Software Architecture in Practice" by Len Bass, Paul Clements, and Rick Kazman. The system should be organized into layers with clear responsibilities, where higher layers depend on services or contracts from lower layers, and not vice versa. This promotes separation of responsibilities and reduces coupling.

2. **Pipe-and-Filter Pattern:** also based on "Software Architecture in Practice". Each stage of the pipeline should receive a defined input, process it, and produce an output consumed by the next stage. This facilitates isolated testing, component replacement, and controlled evolution of the flow.

3. **Responsibility and Low Coupling Principles:** the proposal mainly applies the concepts of `Single Responsibility` and `Dependency Inversion` to ensure that each module has a clear responsibility and that dependencies between parts of the system are made through stable contracts rather than internal implementation details.

## 1. General Rules for the ADAS Code Execution Pipeline

Our ADAS pipeline execution code grew organically, focusing on functionality and immediate results. Now, to ensure the sustainability of the project, we need to establish clear architectural rules to guide code organization, interaction between modules, and the implementation of new features.

The main objectives of these rules are:

- **Efficiency:** Since we need to achieve a good FPS, the architecture must be lightweight and optimized, avoiding unnecessary overhead and ensuring each module performs its function efficiently.
- **Modularity:** The code should be divided into independent modules, each with a clear responsibility and well-defined interfaces. This facilitates maintenance, testing, and system evolution.
- **Centralized Orchestration:** `main` should be the control point for execution but should not contain business logic. It should coordinate the execution order of modules, ensure correct data passage, and manage the application lifecycle.
- **Functional Organization:** Modules should be organized based on the function they perform in the system, avoiding unnecessary coupling and promoting internal cohesion of each part of the code.
- **Controlled Evolution:** Every new feature must be implemented respecting the already defined architecture, ensuring that the system evolves consistently and without degrading the existing structure.

These rules serve to transform the pipeline into a predictable, testable, and evolutionary system. By following this architectural base, the project reduces the risk of regression, improves the clarity of the execution flow, and facilitates maintenance over future iterations.

## 2. Modules and Responsibilities

To ensure a clear and functional architecture, system modules should be organized based on their responsibilities. Each package can use an `__init__.py` to expose its public API when appropriate, but the module interface definition should primarily be in the classes, functions, and data contracts it provides. Below is a proposed organization:

- **Camera:** responsible for capturing images and providing frames to the pipeline.
- **Inference:** responsible for executing inference models and returning raw results.
- **Post-Processing:** responsible for translating raw model outputs into structures usable by the domain.
- **LFA:** responsible for lane detection and interpretation logic. Within this module are stages such as `BEV Transform`, `Sliding Windows`, and `CTE` calculation.
- **Object Perception:** responsible for the detection, classification, and interpretation of objects relevant to driving.
- **Decision and Control:** responsible for FSM, PID, and defining the vehicle's response.
- **CAN Bus / External Interfaces:** responsible for sending commands to the vehicle and integrating external interfaces like CAN and Kuksa.
- **Display/Debug:** responsible for visualization, overlays, and validation support during development.

This organization avoids confusing processing stages with architectural boundaries. `BEV`, `Sliding Windows`, and `CTE`, for example, are part of the LFA domain but do not necessarily need to exist as independent first-level modules.

Each module should be designed to be as independent as possible, with clear and well-defined interfaces. This allows each part of the system to evolve in isolation, facilitating maintenance and the addition of new features without impacting other parts of the code.

## 3. `main` Organization and Execution Orchestration

`main` should follow a clear control structure, where each stage of the pipeline is executed in a logical order, ensuring that data flows consistently and predictably. `main` should function as the system orchestrator and not as a concentrator of business rules.

Generally, the execution order can follow this flow:

1. Camera frame capture
2. Inference model execution
3. Post-processing of inference results
4. Transformation to BEV
5. Application of sliding windows
6. CTE calculation
7. Execution of PID controller
8. Sending commands to the vehicle via CAN Bus

Each stage should be clearly separated, with calls to functions or methods of the corresponding modules. `main` should only be responsible for coordinating execution and ensuring correct data passage between modules, without containing business logic, decoder formulas, geometry rules, or hardware-specific processing that can be encapsulated in another component.

This approach makes `main` easier to understand, maintain, and test. The leaner it is, the clearer the system flow becomes, and the lower the risk of turning the central orchestration into a new point of coupling.

## 4. Communication between Modules and Data Contracts

Communication between modules should be done through well-defined interfaces, where each module exposes only the functionality necessary to interact with others. Data contracts must have clear inputs and outputs, ensuring each module knows exactly what it receives and what it should produce.

Example of inputs and outputs along the pipeline:

- **Camera:** no input; output `bgr (H, W, 3) uint8`
- **Inference:** input `bgr`; output `outputs_lane (dict)`, `outputs_obj (dict)`
- **Post-Processing:** input `outputs_lane`; output `binary_mask (H, W) uint8`
- **BEV Transform:** input `binary_mask`; output `bev_mask (H, W) uint8`
- **Sliding Windows:** input `bev_mask`; output `fit_result (LaneFitResult)`
- **CTE:** input `fit_result.cte_norm`; output `cte (float [-1, 1])`
- **PID:** input `cte`, `dt`; output `pid_return (float [-1, 1])`
- **CAN Bus:** input `pid_return`, `current_state`; output CAN command `0x110`, `0x001`

Whenever possible, these contracts should be represented by types, dataclasses, enums, or documented structures. This reduces ambiguity, improves code readability, and facilitates unit and integration testing.

This approach reinforces the separation of responsibilities and improves fault identification because each module has expected behavior and clearer technical boundaries.

## 5. Implementation of New Features and System Evolution

Every new feature must be implemented respecting the already defined architecture, ensuring that the system evolves consistently and without degrading the existing structure. This means any new functionality should be added as a new module or as an extension of an existing module, following the established communication rules and data contracts.

Before implementation, it's important to answer some questions:

- Which layer does the feature belong to?
- What is the expected input?
- What is the expected output?
- Does it add unnecessary coupling to `main`?
- Can it be tested in isolation?

It is also important to ensure that new features are tested with unit and integration tests whenever possible. This helps identify regressions, validate contracts, and reduce the risk of negative impact on global pipeline performance or behavior.

Each module should contain clear documentation about its responsibilities, interfaces, and relationship with the general system architecture. This facilitates code understanding by other developers and improves team collaboration.

## 6. Conclusion

The proposed architecture for the ADAS pipeline is based on principles of separation of responsibilities, modularity, clear data contracts, and centralized orchestration. By following these guidelines, the project gains predictability, improves maintainability, and reduces the cost of evolution over time.

More than just reorganizing files, this proposal defines an implementation rule for the pipeline. The goal is to ensure the system can grow in a controlled manner, maintaining structural clarity, technical consistency, and alignment with current and future project needs.
