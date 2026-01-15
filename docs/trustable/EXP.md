

---

### EXP-100 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-100 data-toc-label="EXP-100" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The STM32 firmware shall monitor the arrival of control messages from the RPi 5. If the interval between two consecutive control messages exceeds 100ms, the system shall enter Safe State (motors at 0 and steering centered). H1-100
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-100](AST.md#ast-100) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the CAN bus is disconnected or the RPi stops transmitting, the PWM output pins of the STM32 should be brought to 0% within a time interval such that t < 110ms. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-101 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-101 data-toc-label="EXP-101" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  To avoid misinterpretations of commands (H2-100), all control messages must follow a strict serialization protocol. Values ​​received outside the physical limits of the actuators (e.g., PWM > 100% or steering angle > 30°) sahll be discarded, and the last valid message must be retained for a maximum of 1 cycle.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-101](AST.md#ast-101) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Whenever the STM32 receives a CAN message with a 'Speed' value > 100 or 'Steer' > 30 (e.g., 'Steer' not in [-30, 30]'), respecting the physical limits, the message should be discarded and the previous state of the actuators should be maintained unchanged. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-103](AST.md#ast-103) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the CRC calculated on the 7-byte payload of the CAN message does not match the 8th byte (checksum) sent by the RPi, the STM32 should increment the error counter can_crc_errors and ignore the current frame. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-102 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-102 data-toc-label="EXP-102" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  Each CAN control frame shall contain a 4-bit field for a Rolling Counter. The STM32 must validate if the counter of the new message is different from the previous one (H4-100). If the counter remains static for 3 consecutive cycles, the message will be considered "stale data" and a warning must be issued.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-102](AST.md#ast-102) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If three consecutive CAN frames are received with the same Rolling Counter value, the can_data_fresh flag should be set to false and the Safe State should be triggered. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-103 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-103 data-toc-label="EXP-103" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The Raspberry Pi shall transmit control messages at a constant frequency of 500 Hz. Given the short interval between messages (2ms), any delay in scheduling tasks in the AGL can cause packet loss, impacting the stability of high-speed control.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-104](AST.md#ast-104) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The nominal interval between control messages should be 2 ms. The assertion is true if the measured interval T is within the range 1.8 ms <= T >= 2.2 ms. Furthermore, there should be no loss of more than 2 consecutive frames in a 1-second period. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-104 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-104 data-toc-label="EXP-104" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The mapping between CAN IDs and control variables (speed, steer) shall be validated at system initialization. Any frame received with an unexpected ID should be silently discarded.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-105](AST.md#ast-105) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | During a 5-minute test, 100% of the frames transmitted by the RPi for control must use the CAN IDs predefined in the protocol specification document (e.g., Speed=0x100, Steer=0x101). | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-201 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-201 data-toc-label="EXP-201" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall be able to detect the absence of pulses for a prolonged period, indicating a possible disconnection or physical failure of the sensor cable.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-201](AST.md#ast-201) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the time counter between pulses exceeds the calibrated threshold (e.g., 500ms), the system MUST transition to the "Signal Lost" error state. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-202 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-202 data-toc-label="EXP-202" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The software shall apply filtering mechanisms (such as debouncing) to reject spurious pulses and ensure that only valid signals are counted.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-202](AST.md#ast-202) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Pulses with a width smaller than the configured debouncing minimum time MUST be ignored by the speed counter. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-205 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-205 data-toc-label="EXP-205" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The sensor driver interrupt and processing logic shall execute in an isolated memory region (MPU or TrustZone) to prevent external interference.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-205](AST.md#ast-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The firmware MUST configure the Memory Protection Unit (MPU) to enforce read-only access to the sensor driver code and restricted read/write access to its data structures, triggering a fault on unauthorized access. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-206 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-206 data-toc-label="EXP-206" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The speed calculation algorithm shall correctly handle hardware counter overflow to maintain speed accuracy.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-206](AST.md#ast-206) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the capture timer overflows, the calculation logic MUST handle the event to prevent the speed from being calculated as zero or an incorrect momentary value. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-207 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-207 data-toc-label="EXP-207" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall cross-reference speedometer data with a secondary speed estimate (such as IMU derivative) to identify inconsistencies.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-207](AST.md#ast-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system MUST compare the calculated wheel speed against a secondary estimation source (e.g., IMU) and invalidate the reading if the deviation exceeds the defined error margin. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-300 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-300 data-toc-label="EXP-300" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall guarantee that the task responsible for reading the speed
  sensor is executed periodically within its defined deadline, ensuring temporal
  predictability in the ThreadX environment and preventing delays that could
  compromise vehicle control.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-300](AST.md#ast-300) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The speed sensor task executes periodically within its configured period and   completes execution before its defined deadline on every activation under   normal operating conditions. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-301 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-301 data-toc-label="EXP-301" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall ensure that every speed sample includes an associated
  monotonic timestamp and that stale data is automatically invalidated when it
  exceeds the maximum allowed age, preventing the use of outdated information
  in vehicle control.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-301](AST.md#ast-301) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Every speed sample produced by the system includes a monotonic timestamp, and   samples older than the configured freshness threshold are automatically   invalidated and not used by downstream control logic. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-302 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-302 data-toc-label="EXP-302" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall guarantee exclusive and deterministic access to speed data
  shared between concurrent tasks, using RTOS synchronization primitives to
  prevent race conditions and data corruption.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-302](AST.md#ast-302) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Concurrent tasks accessing shared speed data are synchronized using RTOS   primitives such that no data races, partial writes, or inconsistent reads   occur during execution. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-303 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-303 data-toc-label="EXP-303" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall detect and report queue overflows and lost messages in
  inter-task communication, ensuring visibility of communication failures that
  could compromise the integrity of speed data.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-303](AST.md#ast-303) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system detects queue overflows and lost messages in inter-task   communication and reports these events through logs or diagnostic counters   at runtime. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-304 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-304 data-toc-label="EXP-304" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The system shall prevent unbounded priority inversion in safety-critical
  tasks by ensuring that RTOS priority inheritance mechanisms are correctly
  used to maintain predictable latency in the execution of speed-related
  tasks.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-304](AST.md#ast-304) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The RTOS configuration prevents unbounded priority inversion by ensuring that   safety-critical tasks are protected by priority inheritance or equivalent   mechanisms, maintaining bounded execution latency. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-400 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-400 data-toc-label="EXP-400" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  All software components shall perform data transmission with unit conversion according to the VSS standard. Example: speed should be treated as m/s. H1-400
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-400](AST.md#ast-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Not only should the variables be conventionally aligned with the VSS standard, but the units of measurement should also be. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-401 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-401 data-toc-label="EXP-401" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The control system shall consult VSS metadata (min/max) for each actuator signal. Commands that exceed these limits must trigger an integrity error. H2-400
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-401](AST.md#ast-401) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The code must have a data range validator, if the information sent has a value beyond the max, or less than the min of the range it must be discarded. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-501 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-501 data-toc-label="EXP-501" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall ensure that displayed vehicle information represents the current system state within an acceptable time window and shall safely handle invalid, missing, or out-of-range data without causing application failure or undefined behavior.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-501](AST.md#ast-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall refresh each displayed vehicle parameter at least once every 300 ms. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-503](AST.md#ast-503) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall not crash, freeze, or display undefined behavior when receiving invalid, missing, or out-of-range vehicle data. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-502](AST.md#ast-502) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall detect and flag any vehicle parameter that is not updated within the defined freshness time limit (300ms). | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-502 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-502 data-toc-label="EXP-502" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall present warning and status indications whenever critical vehicle conditions are detected, ensuring observer awareness.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-505](AST.md#ast-505) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall keep the warning indication visible for the entire duration of the critical condition. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-504](AST.md#ast-504) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall display a visible warning indication whenever a critical vehicle condition is reported by the system. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-600 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-600 data-toc-label="EXP-600" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The system must automatically launch all applications necessary for the project to function properly during boot.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-601](AST.md#ast-601) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall immediately start a script to verify OTA updates after connected to the internet | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-602](AST.md#ast-602) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If for any reason the auto-start of an application fails, the system should attempt to run it again at least 10 more times. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-600](AST.md#ast-600) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall immediately start Instrument Cluster using systemd maximum 10 seconds after boot. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-601 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-601 data-toc-label="EXP-601" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The system (AGL on Raspberry Pi) has conditions to store all the data necessary for its operation without risk of failure due to lack of space.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-603](AST.md#ast-603) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The AGL on the Raspberry Pi 5 must support the entire structure of this project and its features. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-602 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-602 data-toc-label="EXP-602" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The AGL system on Raspberry Pi continuously monitors key parameters such as temperature and voltage to prevent abrupt shutdowns and protect the file system from corruption.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-604](AST.md#ast-604) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must include a storage monitoring program. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-605](AST.md#ast-605) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must include a temperature monitoring program. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-700 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-700 data-toc-label="EXP-700" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster shall be be updated at appropriate times and in a security way, ensuring the integrity of the data displayed in the vehicle.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-700](AST.md#ast-700) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new cluster version shall only start on the next time the vehicle turn on again | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-701 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-701 data-toc-label="EXP-701" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
All over-the-air (OTA) updates are performed securely, ensuring data integrity and preventing any corruption or tampering that could affect system functionality.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-701](AST.md#ast-701) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new package shall be validated using checksum or hash before installation | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-703](AST.md#ast-703) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the new package update is not safe the system shall support rollback to the previous versions. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-704](AST.md#ast-704) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Every OTA update shall be logged with timestamp, version and result (success or fail) | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-702](AST.md#ast-702) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the update fail (wifi, energy drops etc...) the system shall support rollback to the previous versions. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}
