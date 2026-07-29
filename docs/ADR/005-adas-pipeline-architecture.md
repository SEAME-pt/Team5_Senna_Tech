# [ADR-005] Modular ADAS Pipeline Architecture
Status: Accepted

Date: 21-05-2026

### 1. Context and Problem Statement

The ADAS pipeline grew organically, focused on functionality and immediate results. The initial code concentrated inference, post-processing, decision logic, and display in a single script, creating high coupling, difficult maintenance, and risk of regression with every new feature added.

Current state: modular pipeline implemented in `pipeline/` with modules `camera`, `inference`, `post_processing` (lane decoding), `object` (corridor checking, obstacle tracking, perception contracts), `LFA`, `decision`, `kuksa_publish`, and `utils`, orchestrated by a `main.py` with no business logic.

Driver/Trigger: Need to scale the system with new features (obstacle avoidance, adaptive cruise, lane tracking) without degrading the existing structure or introducing regressions.

### 2. Considered Options

Option A: Monolithic Pipeline — keep all logic in a single script, growing by adding functions and global variables.

Option B: Modular Layered Architecture with Pipe-and-Filter — organise the system into independent modules with clear responsibilities, defined data contracts, and `main` as a pure orchestrator.

Option C: Microservices with IPC/Sockets — isolate each module as an independent process with communication via sockets or message queues.

### 3. Decision Outcome

Chosen Option: Option B — Modular Layered Architecture with Pipe-and-Filter, because it balances separation of concerns with real-time performance on the Raspberry Pi 5 + Hailo-8, without the inter-process communication overhead of Option C.

### 4. Pros and Cons of the Options

**Option A: Monolithic Pipeline**

* Good: Fast to prototype and simple to run.
* Good: No overhead from imports or interfaces between modules.
* Bad: Total coupling — one change can break any part of the system.
* Bad: Impossible to test components in isolation.
* Bad: `main` becomes a concentrator of business logic, hard to read and maintain.

**Option B: Modular Layered Architecture with Pipe-and-Filter**

* Good: Each module has a single responsibility and a clear interface.
* Good: Allows replacing or evolving components without impact on other modules.
* Good: `main` acts as a pure orchestrator — easy to read and audit the full flow.
* Good: Explicit data contracts (`LaneFitResult`, `EnvironmentState`) reduce ambiguity.
* Good: Compatible with the real-time performance requirements of the Raspberry Pi 5 + Hailo-8.
* Bad: Higher initial organisation overhead compared to the monolithic approach.

**Option C: Microservices with IPC/Sockets**

* Good: Maximum isolation — a failure in one process does not bring down others.
* Bad: Inter-process communication latency unacceptable for a real-time pipeline at 15+ FPS.
* Bad: High operational complexity (process management, synchronisation, serialisation).

### 5. Follow-up Tasks

[ None ]
