

---

### AST-100 | Reviewed: ✔ | Score: 0.0 ### {: #ast-100 data-toc-label="AST-100" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-100](EXP.md#exp-100) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The CAN bus shall operate at 500 kbps with a bus load of less than 70%. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-100](ASM.md#asm-100) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-100](EVD.md#evd-100) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-101 | Reviewed: ✔ | Score: 0.0 ### {: #ast-101 data-toc-label="AST-101" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-101](EXP.md#exp-101) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The dynamic control messages (SPEED, MOTOR_PWR, STEER) shall be transmitted cyclically every 50ms ±10%. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-101](ASM.md#asm-101) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-101](EVD.md#evd-101) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-102 | Reviewed: ✔ | Score: 0.0 ### {: #ast-102 data-toc-label="AST-102" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-102](EXP.md#exp-102) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | Monitoring messages (BATTERY, TEMPERATURE) should be transmitted every 1000ms ±10%. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-101](ASM.md#asm-101) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-102](EVD.md#evd-102) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-103 | Reviewed: ✔ | Score: 0.0 ### {: #ast-103 data-toc-label="AST-103" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-103](EXP.md#exp-103) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The Emergency command (ESTOP - ID 0x001) must be processed and activated on the STM32 in less than 20ms from the request on the Rasp5. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-102](ASM.md#asm-102) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-103](EVD.md#evd-103) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-201 | Reviewed: ✔ | Score: 0.75 ### {: #ast-201 data-toc-label="AST-201" .item-element .item-section class="tsf-score" style="background-color:hsl(90.0, 100%, 38%)"}
If the time counter between pulses exceeds the calibrated threshold (e.g., 500ms), the system MUST transition to the "Signal Lost" error state.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-201](EXP.md#exp-201) {class="tsf-score" style="background-color:hsl(90.0, 100%, 38%)"} | The speed sensor pulse reading logic MUST be reliable and detect timeouts (missing pulses) within a safety-critical window to prevent stale data usage. | 0.75 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-207](ASM.md#asm-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the vehicle possesses a secondary source for speed estimation (e.g., IMU or motor model) with a known error margin. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [ASM-205](ASM.md#asm-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-201-1](EVD-201.md#evd-201-1) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | Test log evidence confirming that the system correctly detects a pulse timeout and transitions to the "Signal Lost" state when pulses stop for more than 500ms. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-201-2](EVD-201.md#evd-201-2) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | Video demonstration showing the physical disconnection of the sensor cable and the subsequent system reaction, validating the failure mode handling. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-202 | Reviewed: ✔ | Score: 0.66667 ### {: #ast-202 data-toc-label="AST-202" .item-element .item-section class="tsf-score" style="background-color:hsl(80.0004, 100%, 41%)"}
Pulses with a width smaller than the configured debouncing minimum time MUST be ignored by the speed counter.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-202](EXP.md#exp-202) {class="tsf-score" style="background-color:hsl(80.0004, 100%, 41%)"} | The software shall apply filtering mechanisms (such as debouncing) to reject spurious pulses and ensure that only valid signals are counted. | 0.67 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-207](ASM.md#asm-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the vehicle possesses a secondary source for speed estimation (e.g., IMU or motor model) with a known error margin. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [ASM-205](ASM.md#asm-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-202-1](EVD-202.md#evd-202-1) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Physical signal validation and noise characterization using a digital oscilloscope. This evidence confirms the hardware baseline and defines the required filtering parameters to satisfy AST-202. | 0.00 | ⨯ Item Reviewed<br>⨯ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-205 | Reviewed: ✔ | Score: 1.0 ### {: #ast-205 data-toc-label="AST-205" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
The firmware MUST configure the Memory Protection Unit (MPU) to enforce read-only access to the sensor driver code and restricted read/write access to its data structures, triggering a fault on unauthorized access.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-205](EXP.md#exp-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The sensor driver interrupt and processing logic shall execute in an isolated memory region (MPU or TrustZone) to prevent external interference. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-205](ASM.md#asm-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-205](EVD.md#evd-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | Verification log confirming the correct configuration of the Memory Protection Unit (MPU). The speed sensor driver is isolated in a restricted memory region. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-206 | Reviewed: ✔ | Score: 0.66667 ### {: #ast-206 data-toc-label="AST-206" .item-element .item-section class="tsf-score" style="background-color:hsl(80.0004, 100%, 41%)"}
If the capture timer overflows, the calculation logic MUST handle the event to prevent the speed from being calculated as zero or an incorrect momentary value.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-206](EXP.md#exp-206) {class="tsf-score" style="background-color:hsl(80.0004, 100%, 41%)"} | The speed calculation algorithm shall correctly handle hardware counter overflow to maintain speed accuracy. | 0.67 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-205](ASM.md#asm-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-206-2](EVD-206.md#evd-206-2) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | Manual test report validating the hardware counter overflow management. The system maintains accuracy even during long periods of continuous operation. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-206-1](EVD-206.md#evd-206-1) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | Static analysis report (Cppcheck) verifying that the timer overflow handling logic is free of arithmetic errors and undefined behaviors. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-207 | Reviewed: ✔ | Score: 1.0 ### {: #ast-207 data-toc-label="AST-207" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
The system MUST compare the calculated wheel speed against a secondary estimation source (e.g., IMU) and invalidate the reading if the deviation exceeds the defined error margin.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-207](EXP.md#exp-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The system shall cross-reference speedometer data with a secondary speed estimate (such as IMU derivative) to identify inconsistencies. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-207](ASM.md#asm-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the vehicle possesses a secondary source for speed estimation (e.g., IMU or motor model) with a known error margin. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [ASM-205](ASM.md#asm-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-207](EVD.md#evd-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | Plausibility check evidence comparing wheel speed data with IMU estimation. The cross-reference validates the consistency of the sensor readings. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-300 | Reviewed: ✔ | Score: 1.0 ### {: #ast-300 data-toc-label="AST-300" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  The speed sensor task executes periodically within its configured period and
  completes execution before its defined deadline on every activation under
  normal operating conditions.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-300](EXP.md#exp-300) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The system shall guarantee that the task responsible for reading the speed   sensor is executed periodically within its defined deadline, ensuring temporal   predictability in the ThreadX environment and preventing delays that could   compromise vehicle control. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-300](EVD.md#evd-300) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-301 | Reviewed: ✔ | Score: 1.0 ### {: #ast-301 data-toc-label="AST-301" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  Every speed sample produced by the system includes a monotonic timestamp, and
  samples older than the configured freshness threshold are automatically
  invalidated and not used by downstream control logic.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-301](EXP.md#exp-301) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The system shall ensure that every speed sample includes an associated   monotonic timestamp and that stale data is automatically invalidated when it   exceeds the maximum allowed age, preventing the use of outdated information   in vehicle control. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-301](EVD.md#evd-301) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-302 | Reviewed: ✔ | Score: 1.0 ### {: #ast-302 data-toc-label="AST-302" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  Concurrent tasks accessing shared speed data are synchronized using RTOS
  primitives such that no data races, partial writes, or inconsistent reads
  occur during execution.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-302](EXP.md#exp-302) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The system shall guarantee exclusive and deterministic access to speed data   shared between concurrent tasks, using RTOS synchronization primitives to   prevent race conditions and data corruption. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-300](ASM.md#asm-300) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | All tasks accessing shared speed data use the designated RTOS synchronization   primitives and do not bypass them through direct or unsafe memory access. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-302](EVD.md#evd-302) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-303 | Reviewed: ✔ | Score: 1.0 ### {: #ast-303 data-toc-label="AST-303" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  The system detects queue overflows and lost messages in inter-task
  communication and reports these events through logs or diagnostic counters
  at runtime.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-303](EXP.md#exp-303) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The system shall detect and report queue overflows and lost messages in   inter-task communication, ensuring visibility of communication failures that   could compromise the integrity of speed data. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-303](EVD.md#evd-303) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-304 | Reviewed: ✔ | Score: 1.0 ### {: #ast-304 data-toc-label="AST-304" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  The RTOS configuration prevents unbounded priority inversion by ensuring that
  safety-critical tasks are protected by priority inheritance or equivalent
  mechanisms, maintaining bounded execution latency.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-304](EXP.md#exp-304) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The system shall prevent unbounded priority inversion in safety-critical   tasks by ensuring that RTOS priority inheritance mechanisms are correctly   used to maintain predictable latency in the execution of speed-related   tasks. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-301](ASM.md#asm-301) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The RTOS is correctly configured and supports priority inheritance or an   equivalent mechanism for managing priority inversion. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-304](EVD.md#evd-304) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-400 | Reviewed: ✔ | Score: 1.0 ### {: #ast-400 data-toc-label="AST-400" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  Not only should the variables be conventionally aligned with the VSS standard, but the units of measurement should also be.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-400](EXP.md#exp-400) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | All software components shall perform data transmission with unit conversion according to the VSS standard. Example: speed should be treated as m/s. H1-400 | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-400](ASM.md#asm-400) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that both ends of the communication (RPi and STM32) use the same version of the VSS specification file (.vspec) to avoid mapping conflicts. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-400](EVD.md#evd-400) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-401 | Reviewed: ✔ | Score: 1.0 ### {: #ast-401 data-toc-label="AST-401" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}
  The code must have a data range validator, if the information sent has a value beyond the max, or less than the min of the range it must be discarded.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-401](EXP.md#exp-401) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The control system shall consult VSS metadata (min/max) for each actuator signal. Commands that exceed these limits must trigger an integrity error. H2-400 | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-400](ASM.md#asm-400) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | It is assumed that both ends of the communication (RPi and STM32) use the same version of the VSS specification file (.vspec) to avoid mapping conflicts. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-401](EVD.md#evd-401) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-501 | Reviewed: ✔ | Score: 0.0 ### {: #ast-501 data-toc-label="AST-501" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall refresh each displayed vehicle parameter at least once every 300 ms.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-501](EXP.md#exp-501) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall ensure that displayed vehicle information represents the current system state within an acceptable time window and shall safely handle invalid, missing, or out-of-range data without causing application failure or undefined behavior. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-501](ASM.md#asm-501) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | Communication latency remains within the limits defined by the system architecture. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-501](EVD.md#evd-501) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-502 | Reviewed: ✔ | Score: 0.0 ### {: #ast-502 data-toc-label="AST-502" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall detect and flag any vehicle parameter that is not updated within the defined freshness time limit (300ms).
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-501](EXP.md#exp-501) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall ensure that displayed vehicle information represents the current system state within an acceptable time window and shall safely handle invalid, missing, or out-of-range data without causing application failure or undefined behavior. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-502](EVD.md#evd-502) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-503 | Reviewed: ✔ | Score: 0.0 ### {: #ast-503 data-toc-label="AST-503" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall not crash, freeze, or display undefined behavior when receiving invalid, missing, or out-of-range vehicle data.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-501](EXP.md#exp-501) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall ensure that displayed vehicle information represents the current system state within an acceptable time window and shall safely handle invalid, missing, or out-of-range data without causing application failure or undefined behavior. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-503](EVD.md#evd-503) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-504 | Reviewed: ✔ | Score: 0.5 ### {: #ast-504 data-toc-label="AST-504" .item-element .item-section class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"}
The instrument cluster shall display a visible warning indication whenever a critical vehicle condition is reported by the system.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-502](EXP.md#exp-502) {class="tsf-score" style="background-color:hsl(30.0, 100%, 56%)"} | The instrument cluster shall present warning and status indications whenever critical vehicle conditions are detected, ensuring observer awareness. | 0.25 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-504](ASM.md#asm-504) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} | The instrument cluster hardware is powered continuously since the start of the vehicle operation. | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [EVD-504](EVD.md#evd-504) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-505 | Reviewed: ✔ | Score: 0.0 ### {: #ast-505 data-toc-label="AST-505" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall keep the warning indication visible for the entire duration of the critical condition.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-502](EXP.md#exp-502) {class="tsf-score" style="background-color:hsl(30.0, 100%, 56%)"} | The instrument cluster shall present warning and status indications whenever critical vehicle conditions are detected, ensuring observer awareness. | 0.25 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-505](EVD.md#evd-505) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-600 | Reviewed: ✔ | Score: 0.0 ### {: #ast-600 data-toc-label="AST-600" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The system shall immediately start Instrument Cluster using systemd maximum 10 seconds after boot.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-600](EXP.md#exp-600) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The system must automatically launch all applications necessary for the project to function properly during boot. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-600](EVD.md#evd-600) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-601 | Reviewed: ✔ | Score: 0.0 ### {: #ast-601 data-toc-label="AST-601" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The system shall immediately start a script to verify OTA updates after connected to the internet
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-600](EXP.md#exp-600) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The system must automatically launch all applications necessary for the project to function properly during boot. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-601](EVD.md#evd-601) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-602 | Reviewed: ✔ | Score: 0.0 ### {: #ast-602 data-toc-label="AST-602" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
If for any reason the auto-start of an application fails, the system should attempt to run it again at least 10 more times.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-600](EXP.md#exp-600) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The system must automatically launch all applications necessary for the project to function properly during boot. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-602](EVD.md#evd-602) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-603 | Reviewed: ✔ | Score: 0.0 ### {: #ast-603 data-toc-label="AST-603" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The AGL on the Raspberry Pi 5 must support the entire structure of this project and its features.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-601](EXP.md#exp-601) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The system (AGL on Raspberry Pi) has conditions to store all the data necessary for its operation without risk of failure due to lack of space. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-603](EVD.md#evd-603) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-604 | Reviewed: ✔ | Score: 0.0 ### {: #ast-604 data-toc-label="AST-604" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The system must include a storage monitoring program.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-602](EXP.md#exp-602) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The AGL system on Raspberry Pi continuously monitors key parameters such as temperature and voltage to prevent abrupt shutdowns and protect the file system from corruption. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-604](EVD.md#evd-604) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-605 | Reviewed: ✔ | Score: 0.0 ### {: #ast-605 data-toc-label="AST-605" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The system must include a temperature monitoring program.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-602](EXP.md#exp-602) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The AGL system on Raspberry Pi continuously monitors key parameters such as temperature and voltage to prevent abrupt shutdowns and protect the file system from corruption. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-605](EVD.md#evd-605) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-700 | Reviewed: ✔ | Score: 0.0 ### {: #ast-700 data-toc-label="AST-700" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The new cluster version shall only start on the next time the vehicle turn on again
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-700](EXP.md#exp-700) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall be be updated at appropriate times and in a security way, ensuring the integrity of the data displayed in the vehicle. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-700](EVD.md#evd-700) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-701 | Reviewed: ✔ | Score: 0.0 ### {: #ast-701 data-toc-label="AST-701" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The new package shall be validated using checksum or hash before installation
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-701](EXP.md#exp-701) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | All over-the-air (OTA) updates are performed securely, ensuring data integrity and preventing any corruption or tampering that could affect system functionality. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-701](EVD.md#evd-701) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-702 | Reviewed: ✔ | Score: 0.0 ### {: #ast-702 data-toc-label="AST-702" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
If the update fail (wifi, energy drops etc...) the system shall support rollback to the previous versions.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-701](EXP.md#exp-701) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | All over-the-air (OTA) updates are performed securely, ensuring data integrity and preventing any corruption or tampering that could affect system functionality. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-702](EVD.md#evd-702) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-703 | Reviewed: ✔ | Score: 0.0 ### {: #ast-703 data-toc-label="AST-703" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
If the new package update is not safe the system shall support rollback to the previous versions.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-701](EXP.md#exp-701) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | All over-the-air (OTA) updates are performed securely, ensuring data integrity and preventing any corruption or tampering that could affect system functionality. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-703](EVD.md#evd-703) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### AST-704 | Reviewed: ✔ | Score: 0.0 ### {: #ast-704 data-toc-label="AST-704" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
Every OTA update shall be logged with timestamp, version and result (success or fail)
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EXP-701](EXP.md#exp-701) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} | All over-the-air (OTA) updates are performed securely, ensuring data integrity and preventing any corruption or tampering that could affect system functionality. | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-704](EVD.md#evd-704) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}
