# Eclipse Kuksa

## 1. Overview
Eclipse Kuksa is an open-source project (Apache 2.0 license) that provides a software platform for vehicles, enabling applications to access and control vehicle data and functionalities in a standardized way.

The project is based on the COVESA Vehicle Signal Specification (VSS), which defines the names and semantics of a wide variety of data entries that represent the current and/or intended state of a vehicle's sensors and actuators, organized in a tree-like structure (example: Vehicle.Speed).

## 2. System Architecture
The Kuksa system follows a modular architecture with two main interacting components:

        +------------------+
        |   Applications   |
        |     (Clients)    |
        +--------+---------+
                 | (gRPC/WebSocket API)
        +--------+---------+
        |  Kuksa Databroker|
        |   (VSS Server)   |
        +--------+---------+
                 | (gRPC API)
        +--------+---------+
        | Kuksa CAN Provider|
        +--------+---------+
                 | (SocketCAN)
        +--------+---------+
        |    CAN Bus       |
        |      (ECUs)      |
        +------------------+

## 3. Core Components
**3.1 Kuksa Databroker**

The Databroker is the core of the system, implementing a resource-efficient VSS signal tree optimized to run inside a vehicle on a microprocessor-based platform.

Technical Characteristics:
Language: Rust (highly resource-efficient)

Primary Interface: gRPC API

Size: Lightweight (<4 MB when statically compiled)

License: 100% Open Source (Apache 2.0)

Functionalities:
Centralized Storage: Maintains a hierarchical data model of vehicle signals (speed, engine RPM, door status, etc.).

Access API: Provides a uniform, high-level API for in-vehicle applications to query signals, update values, and receive notifications about changes.

**3.2 Kuksa CAN Provider**

The CAN Provider is the connector between the Databroker (high-level VSS world) and the vehicle's CAN network (low-level ECU world). It translates raw CAN frames into VSS signals understandable by the Databroker and vice versa.

Operating Principle:

```markdown
+-------------------+      +---------------------+      +-----------------------+
|     CAN Bus       | CAN  |    CAN Provider     | VSS  |    Kuksa Databroker   |
|  (Real ECUs)      |----->|   (dbc2val-mode)    |----->|                       |
+-------------------+      +---------------------+      +-----------------------+

```

Technical Characteristics:
Language: Python

Input/Output: SocketCAN or dump files for testing

Mapping: Uses DBC (Database CAN) files and a JSON mapping file (vss_dbc.json) to define the relationship between CAN and VSS signals.

Operation Modes:
dbc2val (Enabled by default):

Reads raw CAN data from the SocketCAN interface.

Parses it according to the DBC file.

Uses the mapping to convert CAN signals to VSS signals.

Sends the VSS values to the Databroker.

val2dbc:

Subscribes to VSS signals in the Databroker.

Receives value updates.

Uses the inverse mapping and default values (dbc_default_values.json) to assemble complete CAN frames.

Sends the CAN frames to the bus.

## 4. Typical Data Flow
Reading from a Sensor (e.g., speed):

The speedometer ECU generates a CAN frame containing the value.

The CAN Provider (in dbc2val mode) captures the frame, decodes it using the DBC file, and maps it to the VSS signal Vehicle.Speed.

The CAN Provider sends a publish command to the Databroker via gRPC, updating the value in the VSS tree.

A client application (e.g., digital cluster) subscribed to Vehicle.Speed receives a notification from the Databroker with the new value and updates the display.

Writing to an Actuator (e.g., turn on headlight):

A client application (e.g., voice command) sends an actuate command to the Databroker to change the signal Vehicle.Body.Lights.Beam.Low.IsOn to true.

The CAN Provider (in val2dbc mode), which is subscribed to this signal, receives the notification from the Databroker.

It consults the mapping to find the corresponding CAN signal(s) and frame ID for the low beam.

The Provider assembles the CAN frame, filling unmapped signals with default values, and sends it to the CAN bus via SocketCAN.

The ECU controlling the headlights receives the frame and activates the relay/light.

## 5. Conclusion
Eclipse Kuksa provides a modern, standardized foundation for software development in vehicles. By decoupling applications (which use the rich semantics of VSS) from vehicle network complexity (via protocols like CAN), it promotes:

**Interoperability**: Applications become independent of the vehicle manufacturer or specific ECUs.

**Agile Development**: Developers can focus on application logic without needing to understand low-level vehicle bus details.

**Testability**: Components can be tested in isolation (e.g., using CAN dump files).

**Efficiency**: The Rust-based Databroker ensures high performance and low resource consumption.


