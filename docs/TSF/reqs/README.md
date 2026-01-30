# Requirements and Analysis

This directory serves as the central repository for all project requirements, analysis documents, and supporting evidence, following a structured requirements engineering process.

The goal is to ensure that all aspects of the system are well-defined, traceable, and verifiable.

## Directory Structure and Workflow

The subdirectories are organized to reflect a logical workflow for requirements definition and verification.

**Typical Workflow:**
`Templates` -> `HARA` -> `Expectations` -> `Assertions` / `Assumptions` -> `Tests` -> `Evidences`

-   **[`/templates/`](./templates/)**: Provides standardized templates for creating new requirement and analysis documents.

-   **[`/HARA/`](./HARA/)**: Contains all Hazard Analysis and Risk Assessment (HARA) documents for the project.

-   **[`/expectations/`](./expectations/)**: Describes high-level expectations of the system's behavior from a user or stakeholder perspective.

-   **[`/assertions/`](./assertions/)**: Contains formal, verifiable assertions about the system's properties, which are derived from the higher-level expectations.

-   **[`/assumptions/`](./assumptions/)**: Documents all assumptions made during the design and development process.

-   **[`/test/`](./test/)**: Contains requirement-level test cases designed to verify that the defined assertions and expectations are met.

-   **[`/evidences/`](./evidences/)**: Holds formal evidence artifacts (e.g., final test reports, validation documents) that prove high-level requirements are met. This closes the verification loop.

---

## 🗺️ Traceability Maps

### Speedometer Integration
The diagram below illustrates the full traceability from expectations to final evidence for [Goal 1 of Module 01 - SEAME 2025](https://github.com/SEAME-pt/contents-2025/tree/main/01_SwArchitecture4Automotive).

```mermaid
graph TD
    %% Styles Definition
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef assumption fill:#e2e3e5,stroke:#383d41,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    %% Functional Requirements Layer
    subgraph F201 [201: Timeout]
        EXP201[EXP-201] --> AST201[AST-201]
        AST201 --> E201_1[EVD-201-1]
        AST201 --> E201_2[EVD-201-2]
    end

    subgraph F202 [202: Noise]
        EXP202[EXP-202] --> AST202[AST-202]
        AST202 --> E202_1[EVD-202-1]
    end

    subgraph F205 [205: MPU]
        EXP205[EXP-205] --> AST205[AST-205]
        AST205 --> E205[EVD-205]
    end

    subgraph F206 [206: Overflow]
        EXP206[EXP-206] --> AST206[AST-206]
        AST206 --> E206_1[EVD-206-1]
        AST206 --> E206_2[EVD-206-2]
    end

    subgraph F207 [207: Plausibility]
        EXP207[EXP-207] --> AST207[AST-207]
        AST207 --> E207[EVD-207]
    end

    %% Invisible Spacers to push foundation down
    E201_1 ~~~ ASM205
    E202_1 ~~~ ASM205
    E205 ~~~ ASM205
    E206_1 ~~~ ASM207
    E207 ~~~ ASM207

    %% Foundation Layer (Absolute Bottom)
    subgraph Foundation [Platform Foundation]
        direction LR
        ASM205[ASM-205: MPU Support] -.-> E205_H[EVD-ASM-205]
        
        ASM207[ASM-207: IMU Presence] -.-> E207_H[EVD-ASM-207]
    end

    %% Infrastructure Support Links
    AST201 -.-> ASM205
    AST201 -.-> ASM207
    AST202 -.-> ASM205
    AST202 -.-> ASM207
    AST205 -.-> ASM205
    AST206 -.-> ASM205
    AST207 -.-> ASM205
    AST207 -.-> ASM207

    %% Applying Classes
    class EXP201,EXP202,EXP205,EXP206,EXP207 expectation;
    class AST201,AST202,AST205,AST206,AST207 assertion;
    class E201_1,E201_2,E202_1,E205,E206_1,E206_2,E207,E205_H,E207_H evidence;
    class ASM205,ASM207 assumption;

    %% Links to files
    click EXP201 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-201.md"
    click EXP202 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-202.md"
    click EXP205 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-205.md"
    click EXP206 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-206.md"
    click EXP207 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-207.md"
    click AST201 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-201.md"
    click AST202 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-202.md"
    click AST205 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-205.md"
    click AST206 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-206.md"
    click AST207 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-207.md"
    click ASM205 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-205.md"
    click ASM207 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-207.md"
    click E201_1 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-201-1.md"
    click E201_2 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-201-2.md"
    click E202_1 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-202-1.md"
    click E205 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-205.md"
    click E206_1 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-206-1.md"
    click E206_2 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-206-2.md"
    click E207 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-207.md"
    click E205_H "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-ASM-205.md"
    click E207_H "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-ASM-207.md"
```

### CAN Communication (Case 100)
Traceability for CAN Bus Interface and Communication.

```mermaid
graph TD
    %% Styles Definition
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef assumption fill:#e2e3e5,stroke:#383d41,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    subgraph F100 [100: CAN Timeout]
        EXP100[EXP-100] --> AST100[AST-100]
        AST100 --> E100[EVD-100]
    end

    subgraph F101 [101: Message Integrity]
        EXP101[EXP-101] --> AST101[AST-101]
        EXP101 --> AST103[AST-103]
        AST101 --> E101[EVD-101]
        AST103 --> E103[EVD-103]
    end

    subgraph F102 [102: Bus Load]
        EXP102[EXP-102] --> AST102[AST-102]
        AST102 --> E102[EVD-102]
    end
    
    subgraph F103 [103: Error Handling]
        EXP103[EXP-103] --> AST104[AST-104]
        AST104 --> E104[EVD-104]
    end

    subgraph F104 [104: Secure Boot]
        EXP104[EXP-104] --> AST105[AST-105]
        AST105 --> E105[EVD-105]
    end

    %% Invisible Spacers to push foundation down
    E100 ~~~ ASM100
    E103 ~~~ ASM100
    E102 ~~~ ASM100
    E104 ~~~ ASM100
    E105 ~~~ ASM100

    %% Foundation Layer
    subgraph Foundation [Platform Foundation]
        direction LR
        ASM100[ASM-100] -.-> E106[EVD-106]
        ASM101[ASM-101] -.-> E107[EVD-107]
    end

    %% Infrastructure Support Links
    AST100 -.-> ASM100
    AST103 -.-> ASM101

    %% Applying Classes
    class EXP100,EXP101,EXP102,EXP103,EXP104 expectation;
    class AST100,AST101,AST102,AST103,AST104,AST105 assertion;
    class E100,E101,E102,E103,E104,E105,E106,E107 evidence;
    class ASM100,ASM101, assumption;

    %% Links
    click EXP100 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-100.md"
    click EXP101 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-101.md"
    click EXP102 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-102.md"
    click EXP103 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-103.md"
    click EXP104 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-104.md"

    click AST100 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-100.md"
    click AST101 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-101.md"
    click AST102 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-102.md"
    click AST103 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-103.md"
    click AST104 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-104.md"
    click AST105 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-105.md"

    click E100 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-100.md"
    click E101 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-101.md"
    click E102 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-102.md"
    click E103 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-103.md"
    click E104 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-104.md"
    click E105 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-105.md"
    click E106 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-106.md"
    click E107 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-107.md"

    click ASM100 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-100.md"
    click ASM101 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-101.md"
```

### RTOS Scheduling (Case 300)
Traceability for Real-Time Operating System tasks.

```mermaid
graph TD
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef assumption fill:#e2e3e5,stroke:#383d41,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    subgraph F300 [300: Task Priority]
        EXP300[EXP-300] --> AST300[AST-300]
        AST300 --> E300[EVD-300]
    end

    subgraph F301 [301: Context Switch]
        EXP301[EXP-301] --> AST301[AST-301]
        AST301 --> E301[EVD-301]
    end

    subgraph F302 [302: Deadline Mon]
        EXP302[EXP-302] --> AST302[AST-302]
        AST302 --> E302[EVD-302]
    end
    
    subgraph F303 [303: Stack Usage]
        EXP303[EXP-303] --> AST303[AST-303]
        AST303 --> E303[EVD-303]
    end

    subgraph F304 [304: Resource Lock]
        EXP304[EXP-304] --> AST304[AST-304]
        AST304 --> E304[EVD-304]
    end

    %% Invisible Spacers to push foundation down
    E300 ~~~ ASM300
    E301 ~~~ ASM300
    E302 ~~~ ASM300
    E303 ~~~ ASM300
    E304 ~~~ ASM300

    subgraph Foundation
        direction LR
        ASM300[ASM-300] -.-> E305[EVD-305]
        ASM301[ASM-301] -.-> E306[EVD-306]
    end

    %% Infrastructure Support Links
    AST302 -.-> ASM300
    AST304 -.-> ASM301

    class EXP300,EXP301,EXP302,EXP303,EXP304 expectation;
    class AST300,AST301,AST302,AST303,AST304 assertion;
    class E300,E301,E302,E303,E304,E305,E306 evidence;
    class ASM300,ASM301 assumption;

    click EXP300 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-300.md"
    click EXP301 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-301.md"
    click EXP302 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-302.md"
    click EXP303 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-303.md"
    click EXP304 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-304.md"
    
    click AST300 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-300.md"
    click AST301 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-301.md"
    click AST302 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-302.md"
    click AST303 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-303.md"
    click AST304 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-304.md"
    
    click E300 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-300.md"
    click E301 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-301.md"
    click E302 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-302.md"
    click E303 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-303.md"
    click E304 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-304.md"
    click E305 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-305.md"
    click E306 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-306.md"
    
    click ASM300 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-300.md"
    click ASM301 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-301.md"
```

### COVESA Data Mapping (Case 400)
Traceability for VSS Data Mapping.

```mermaid
graph TD
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef assumption fill:#e2e3e5,stroke:#383d41,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    subgraph F400 [400: Signal Map]
        EXP400[EXP-400] --> AST400[AST-400]
        AST400 --> E400[EVD-400]
    end

    subgraph F401 [401: Data Fmt]
        EXP401[EXP-401] --> AST401[AST-401]
        AST401 --> E401[EVD-401]
    end

    %% Invisible Spacers to push foundation down
    E400 ~~~ ASM400
    E401 ~~~ ASM400

    subgraph Foundation
        direction LR
        ASM400[ASM-400] -.-> E402[EVD-402]
    end

    %% Infrastructure Support Links
    AST400 -.-> ASM400
    AST401 -.-> ASM400

    class EXP400,EXP401 expectation;
    class AST400,AST401 assertion;
    class E400,E401,E402 evidence;
    class ASM400 assumption;

    click EXP400 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-400.md"
    click EXP401 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-401.md"
    click AST400 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-400.md"
    click AST401 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-401.md"
    click E400 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-400.md"
    click E401 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-401.md"
    click E402 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-402.md"
    click ASM400 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-400.md"
```

### Instrument Cluster (Case 500)
Traceability for Qt GUI and Display logic.

```mermaid
graph TD
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef assumption fill:#e2e3e5,stroke:#383d41,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    subgraph F501 [501: GUI Update]
        EXP501[EXP-501] --> AST501[AST-501]
        EXP501 --> AST502[AST-502]
        EXP501 --> AST503[AST-503]
        AST501 --> E501[EVD-501]
        AST502 --> E502[EVD-502]
        AST503 --> E503[EVD-503]
    end

    subgraph F502 [502: Latency]
        EXP502[EXP-502] --> AST504[AST-504]
        EXP502 --> AST505[AST-505]
        AST504 --> E504[EVD-504]
        AST505 --> E505[EVD-505]
    end

    %% Invisible Spacers to push foundation down
    E501 ~~~ ASM501
    E503 ~~~ ASM501
    E504 ~~~ ASM504
    E505 ~~~ ASM504

    subgraph Foundation
        direction LR
        ASM501[ASM-501] -.-> E104[EVD-104]
        ASM504[ASM-504] -.-> E506[EVD-506]
    end

    %% Infrastructure Support Links
    AST501 -.-> ASM501
    AST502 -.-> ASM501
    AST503 -.-> ASM501
    AST504 -.-> ASM504
    AST505 -.-> ASM504

    class EXP501,EXP502 expectation;
    class AST501,AST502,AST503,AST504,AST505 assertion;
    class E501,E502,E503,E504,E505,E506,E104 evidence;
    class ASM501,ASM504 assumption;

    click EXP501 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-501.md"
    click EXP502 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-502.md"
    
    click AST501 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-501.md"
    click AST502 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-502.md"
    click AST503 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-503.md"
    click AST504 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-504.md"
    click AST505 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-505.md"
    
    click E501 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-501.md"
    click E502 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-502.md"
    click E503 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-503.md"
    click E504 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-504.md"
    click E505 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-505.md"
    click E506 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-506.md"
    click E104 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-104.md"
    
    click ASM501 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-501.md"
    click ASM504 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assumptions/ASM-504.md"
```

### System RPi5 (Case 600)
Traceability for AGL System on Raspberry Pi 5.

```mermaid
graph TD
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef hidden display:none;

    %% Invisible Root to force tree layout
    ROOT600:::hidden
    ROOT600 ~~~ EXP600
    ROOT600 ~~~ EXP601
    ROOT600 ~~~ EXP602

    subgraph F600 [600: OS Stability]
        EXP600[EXP-600] --> AST600[AST-600]
        EXP600 --> AST601[AST-601]
        EXP600 --> AST602[AST-602]
        AST600 --> E600[EVD-600]
        AST601 --> E601[EVD-601]
        AST602 --> E602[EVD-602]
    end

    subgraph F601 [601: Boot Time]
        EXP601[EXP-601] --> AST603[AST-603]
        AST603 --> E603[EVD-603]
    end

    subgraph F602 [602: Resource Mgmt]
        EXP602[EXP-602] --> AST604[AST-604]
        EXP602 --> AST605[AST-605]
        AST604 --> E604[EVD-604]
        AST605 --> E605[EVD-605]
    end

    class EXP600,EXP601,EXP602 expectation;
    class AST600,AST601,AST602,AST603,AST604,AST605 assertion;
    class E600,E601,E602,E603,E604,E605 evidence;

    click EXP600 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-600.md"
    click EXP601 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-601.md"
    click EXP602 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-602.md"
    
    click AST600 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-600.md"
    click AST601 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-601.md"
    click AST602 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-602.md"
    click AST603 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-603.md"
    click AST604 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-604.md"
    click AST605 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-605.md"
    
    click E600 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-600.md"
    click E601 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-601.md"
    click E602 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-602.md"
    click E603 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-603.md"
    click E604 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-604.md"
    click E605 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-605.md"
```

### OTA Updates (Case 700)
Traceability for Over-the-Air update mechanisms.

```mermaid
graph TD
    classDef expectation fill:#d1eaf0,stroke:#31708f,stroke-width:2px,color:#000;
    classDef assertion fill:#fff4dd,stroke:#856404,stroke-width:2px,color:#000;
    classDef evidence fill:#d4edda,stroke:#155724,stroke-width:2px,color:#000;
    classDef hidden display:none;

    %% Invisible Root to force tree layout
    ROOT700:::hidden
    ROOT700 ~~~ EXP700
    ROOT700 ~~~ EXP701

    subgraph F700 [700: Update Auth]
        EXP700[EXP-700] --> AST700[AST-700]
        AST700 --> E700[EVD-700]
    end

    subgraph F701 [701: Rollback]
        EXP701[EXP-701] --> AST701[AST-701]
        EXP701 --> AST702[AST-702]
        EXP701 --> AST703[AST-703]
        EXP701 --> AST704[AST-704]
        AST701 --> E701[EVD-701]
        AST702 --> E702[EVD-702]
        AST703 --> E703[EVD-703]
        AST704 --> E704[EVD-704]
    end

    class EXP700,EXP701 expectation;
    class AST700,AST701,AST702,AST703,AST704 assertion;
    class E700,E701,E702,E703,E704 evidence;

    click EXP700 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-700.md"
    click EXP701 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/expectations/EXP-701.md"
    
    click AST700 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-700.md"
    click AST701 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-701.md"
    click AST702 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-702.md"
    click AST703 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-703.md"
    click AST704 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/assertions/AST-704.md"
    
    click E700 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-700.md"
    click E701 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-701.md"
    click E702 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-702.md"
    click E703 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-703.md"
    click E704 "https://github.com/SEAME-pt/Team5_Senna_Tech/blob/main/reqs/evidences/EVD-704.md"
```

---

## 🛡️ Trustable Framework (TSF) Validators

The project uses the **Eclipse Trustable Software Framework (TSF)** to automatically calculate confidence scores. The following custom validators are implemented in `.dotstop_extensions/validators.py`:

### 1. `test_log_validator` (Runtime Evidence)
Used for technical proofs generated by scripts or system execution.
- **Logic**: Returns **1.0** if it finds the keyword `PASS` in the log, and **0.0** if it finds `FAIL`.
- **Usage**: Validating time-sensitive behaviors like sensor timeouts.

### 2. `static_analysis_validator` (Code Quality Evidence)
Used to verify reports from static analysis tools like `cppcheck` or `lint`.
- **Logic**: Returns **1.0** if it finds a success pattern (default: `0 errors`) in the report file.
- **Usage**: Validating safety-critical code patterns and overflow prevention.

### 3. `reviewer_score` (Process Evidence)
Used for manual gates, such as peer reviews or datasheet inspections.
- **Logic**: Returns **1.0** if the metadata field `result` is explicitly set to `PASS` in the YAML configuration.
- **Usage**: Validating hardware specifications and manual design reviews.

---
-   **[`statements-viewer.md`](./statements-viewer.md)**: A document likely related to viewing or interpreting the various requirement statements.

### Related Documentation

-   **`docs/TSF/Decision_support/`**: While formal evidence resides here in `/evidences`, the `docs/TSF/Decision_support/` directory holds detailed engineering-level justifications, research, and rationale for specific design decisions made during analysis (e.g., justifying a specific HARA failure mode).
