

---

### EXP-100 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-100 data-toc-label="EXP-100" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The CAN bus shall operate at 500 kbps with a bus load of less than 70%.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-100](AST.md#ast-100) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-101 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-101 data-toc-label="EXP-101" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The dynamic control messages (SPEED, MOTOR_PWR, STEER) shall be transmitted cyclically every 50ms ±10%.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-101](AST.md#ast-101) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-102 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-102 data-toc-label="EXP-102" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  Monitoring messages (BATTERY, TEMPERATURE) should be transmitted every 1000ms ±10%.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-102](AST.md#ast-102) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-103 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-103 data-toc-label="EXP-103" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  The Emergency command (ESTOP - ID 0x001) must be processed and activated on the STM32 in less than 20ms from the request on the Rasp5.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-103](AST.md#ast-103) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### EXP-201 | Reviewed: ⨯ | Score: 0.0 ### {: #exp-201 data-toc-label="EXP-201" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The speed sensor pulse reading logic MUST be reliable and detect timeouts (missing pulses) within a safety-critical window to prevent stale data usage.
{: .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-201](AST.md#ast-201) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the time counter between pulses exceeds the calibrated threshold (e.g., 500ms), the system MUST transition to the "Signal Lost" error state. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

- `docs/TSF/Decision_support/DS-HR200-1_Comm-Failure-Hazard-Justification.md`

	??? "Click to view reference"

		````md
		# Evidence for HARA-200: Justification for the Sensor Connection Failure Hazard
		
		**ID:** DS-HR200-1
		**Date:** 2026-01-08
		**Author:** Hellom with Gemini
		**Reviewer:** Hellom Mendes
		**Relates to:** HARA-200, Hazard H1-200 (Sensor Connection Failure)
		
		---
		
		## 1. Decision
		
		Hazard `H1-200` (Sensor Connection Failure), manifested by events such as a **disconnected or broken sensor cable**, is considered a credible and relevant threat to the system's safety analysis.
		
		## 2. Justification and Scenarios
		
		A physical connection failure of the sensor, such as a disconnected or damaged cable, will prevent sensor pulses from reaching the STM32. This can lead the system to operate without updated speed data, resulting in dangerous behavior **[1]**.
		
		### Relevant Scenarios for Hazard Occurrence
		
		*   **Disconnected/Damaged Sensor Cable:**
		    *   **Description:** The physical conductor transmitting sensor pulses to the STM32 is broken or disconnected. This prevents pulses from reaching the microcontroller, resulting in a 0 km/h speed reading.
		    *   **Common Scenarios:**
		        *   **Vibration/Mechanical Shock:** Vehicle movement or impacts can loosen or physically disconnect the sensor cable.
		        *   **Wear/Material Fatigue:** Over time, the cable may wear out or break due to repeated flexing or stress.
		        *   **Damage During Maintenance/Assembly:** The cable may be accidentally cut or damaged during assembly or repairs.
		
		*   **Short Circuit or Open Circuit on the Pulse Line:**
		    *   **Description:** Electrical problems on the pulse line can prevent the correct transmission of pulses. A short circuit can cause the line to be constantly high or low, while an open circuit prevents any signal **[2]**.
		    *   **Common Scenarios:**
		        *   **Damaged Wiring:** Compromised insulation leading to short circuits with other lines or ground.
		        *   **Faulty Circuit Components:** Pull-up/pull-down resistors or capacitors associated with the pulse line fail, altering signal behavior.
		
		## 3. Conclusion
		
		Considering that physical connection failures and electrical problems are documented and expected failure modes for sensors, hazard `H1-200` is considered **relevant** and **credible**, requiring robust software mitigations to detect the absence of pulses and ensure that the 0 km/h reading is handled safely (to be detailed in a separate document).
		
		---
		
		## Reviewer Note
		
		The references have been validated. ISO 26262 theoretically confirms that the loss of control data is critical, while the GM Recall (NHTSA) proves that this specific failure (speed sensor) has already caused real-world accidents due to involuntary braking, justifying the C4 criticality classification for this hazard.
		
		## 4. References
		
		**[1] ISO 26262-6:2018 - Annex D.2.3 (Freedom from interference by information exchange):** Identifies **"Loss of information"** and **"Blocking of information"** as critical failure modes in the exchange between system elements (e.g., Sensor to Microcontroller). The standard states that the loss of safety-critical feedback, such as vehicle speed, compromises the system's ability to maintain a safe state (e.g., closed-loop control), leading to hazardous behaviors unless detected by specific mechanisms like timeouts or E2E protection.
		
		**[2] NHTSA Safety Recall 19V649000 - General Motors:** This official safety recall documents how wheel speed sensor signal failures (intermittent signal loss or corruption) led to unintended braking activations in over 600,000 vehicles, providing empirical evidence of the hazardous behaviors described in this document.
		
		````



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
