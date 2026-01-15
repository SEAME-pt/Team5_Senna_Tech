# Trustable Compliance Report



## Item status guide ## { .subsection }

Each item in a Trustable Graph is scored with a number between 0 and 1.
The score represents aggregated organizational confidence in a given Statement, with larger numbers corresponding to higher confidence.
Scores in the report are indicated by both a numerical score and the colormap below:
<div class="br" style="height: 26px; width: 80%;background: linear-gradient(to right in hsl, hsl(0.0, 100%, 65%) 0%, hsl(120.0, 100%, 30%) 100%);">
<span style="float:right;">1.00&nbsp</span>
<span style="float:left;">&nbsp0.00</span>
</div>


The status of an item and its links also affect the score.

Unreviewed items are indicated by a cross in the status column.
The score of unreviewed items is always set to zero.


Suspect links are indicated by a cross in the status column.
The contribution to the score of a parent item by a suspiciously linked child is always zero, regardless of the child's own score.
## Compliance for ASM ## {: data-toc-label="ASM"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [ASM-100](ASM.md#asm-100) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the actuators (ESC, Servo) have their own internal fail-safe behavior (e.g., PWM signal = 0% results in safe stop) that will be executed if the STM32 stops transmitting PWM due to a fault. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-101](ASM.md#asm-101) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the CAN network is physically terminated with 1200Ω resistors at both ends, minimizing signal reflections that could cause errors at high frequencies such as 500kbps. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-205](ASM.md#asm-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-207](ASM.md#asm-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the vehicle possesses a secondary source for speed estimation (e.g., IMU or motor model) with a known error margin. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-300](ASM.md#asm-300) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | All tasks accessing shared speed data use the designated RTOS synchronization   primitives and do not bypass them through direct or unsafe memory access. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-301](ASM.md#asm-301) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The RTOS is correctly configured and supports priority inheritance or an   equivalent mechanism for managing priority inversion. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-400](ASM.md#asm-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that both ends of the communication (RPi and STM32) use the same version of the VSS specification file (.vspec) to avoid mapping conflicts. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-501](ASM.md#asm-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Communication latency remains within the limits defined by the system architecture. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [ASM-504](ASM.md#asm-504) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster hardware is powered continuously since the start of the vehicle operation. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |

## Compliance for AST ## {: data-toc-label="AST"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [AST-100](AST.md#ast-100) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the CAN bus is disconnected or the RPi stops transmitting, the PWM output pins of the STM32 should be brought to 0% within a time interval such that t < 110ms. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-101](AST.md#ast-101) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Whenever the STM32 receives a CAN message with a 'Speed' value > 100 or 'Steer' > 30 (e.g., 'Steer' not in [-30, 30]'), respecting the physical limits, the message should be discarded and the previous state of the actuators should be maintained unchanged. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-102](AST.md#ast-102) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If three consecutive CAN frames are received with the same Rolling Counter value, the can_data_fresh flag should be set to false and the Safe State should be triggered. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-103](AST.md#ast-103) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the CRC calculated on the 7-byte payload of the CAN message does not match the 8th byte (checksum) sent by the RPi, the STM32 should increment the error counter can_crc_errors and ignore the current frame. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-104](AST.md#ast-104) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The nominal interval between control messages should be 2 ms. The assertion is true if the measured interval T is within the range 1.8 ms <= T >= 2.2 ms. Furthermore, there should be no loss of more than 2 consecutive frames in a 1-second period. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-105](AST.md#ast-105) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | During a 5-minute test, 100% of the frames transmitted by the RPi for control must use the CAN IDs predefined in the protocol specification document (e.g., Speed=0x100, Steer=0x101). | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-201](AST.md#ast-201) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the time counter between pulses exceeds the calibrated threshold (e.g., 500ms), the system MUST transition to the "Signal Lost" error state. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-202](AST.md#ast-202) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Pulses with a width smaller than the configured debouncing minimum time MUST be ignored by the speed counter. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-205](AST.md#ast-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The firmware MUST configure the Memory Protection Unit (MPU) to enforce read-only access to the sensor driver code and restricted read/write access to its data structures, triggering a fault on unauthorized access. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-206](AST.md#ast-206) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the capture timer overflows, the calculation logic MUST handle the event to prevent the speed from being calculated as zero or an incorrect momentary value. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-207](AST.md#ast-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system MUST compare the calculated wheel speed against a secondary estimation source (e.g., IMU) and invalidate the reading if the deviation exceeds the defined error margin. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-300](AST.md#ast-300) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The speed sensor task executes periodically within its configured period and   completes execution before its defined deadline on every activation under   normal operating conditions. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-301](AST.md#ast-301) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Every speed sample produced by the system includes a monotonic timestamp, and   samples older than the configured freshness threshold are automatically   invalidated and not used by downstream control logic. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-302](AST.md#ast-302) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Concurrent tasks accessing shared speed data are synchronized using RTOS   primitives such that no data races, partial writes, or inconsistent reads   occur during execution. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-303](AST.md#ast-303) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system detects queue overflows and lost messages in inter-task   communication and reports these events through logs or diagnostic counters   at runtime. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-304](AST.md#ast-304) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The RTOS configuration prevents unbounded priority inversion by ensuring that   safety-critical tasks are protected by priority inheritance or equivalent   mechanisms, maintaining bounded execution latency. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-400](AST.md#ast-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Not only should the variables be conventionally aligned with the VSS standard, but the units of measurement should also be. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-401](AST.md#ast-401) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The code must have a data range validator, if the information sent has a value beyond the max, or less than the min of the range it must be discarded. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-501](AST.md#ast-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall refresh each displayed vehicle parameter at least once every 300 ms. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-502](AST.md#ast-502) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall detect and flag any vehicle parameter that is not updated within the defined freshness time limit (300ms). | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-503](AST.md#ast-503) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall not crash, freeze, or display undefined behavior when receiving invalid, missing, or out-of-range vehicle data. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-504](AST.md#ast-504) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall display a visible warning indication whenever a critical vehicle condition is reported by the system. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-505](AST.md#ast-505) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall keep the warning indication visible for the entire duration of the critical condition. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-600](AST.md#ast-600) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall immediately start Instrument Cluster using systemd maximum 10 seconds after boot. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-601](AST.md#ast-601) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall immediately start a script to verify OTA updates after connected to the internet | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-602](AST.md#ast-602) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If for any reason the auto-start of an application fails, the system should attempt to run it again at least 10 more times. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-603](AST.md#ast-603) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The AGL on the Raspberry Pi 5 must support the entire structure of this project and its features. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-604](AST.md#ast-604) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must include a storage monitoring program. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-605](AST.md#ast-605) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must include a temperature monitoring program. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-700](AST.md#ast-700) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new cluster version shall only start on the next time the vehicle turn on again | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-701](AST.md#ast-701) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new package shall be validated using checksum or hash before installation | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-702](AST.md#ast-702) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the update fail (wifi, energy drops etc...) the system shall support rollback to the previous versions. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-703](AST.md#ast-703) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the new package update is not safe the system shall support rollback to the previous versions. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [AST-704](AST.md#ast-704) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Every OTA update shall be logged with timestamp, version and result (success or fail) | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |

## Compliance for EVD ## {: data-toc-label="EVD"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [EVD-100](EVD.md#evd-100) {class="tsf-score" style="background-color:hsl(84.0, 100%, 40%)"} |  | 0.70 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-101](EVD.md#evd-101) {class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"} |  | 0.50 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-102](EVD.md#evd-102) {class="tsf-score" style="background-color:hsl(36.0, 100%, 54%)"} |  | 0.30 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-103](EVD.md#evd-103) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-104](EVD.md#evd-104) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-105](EVD.md#evd-105) {class="tsf-score" style="background-color:hsl(96.0, 100%, 37%)"} |  | 0.80 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-106](EVD.md#evd-106) {class="tsf-score" style="background-color:hsl(84.0, 100%, 40%)"} |  | 0.70 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-107](EVD.md#evd-107) {class="tsf-score" style="background-color:hsl(72.0, 100%, 44%)"} |  | 0.60 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-205](EVD.md#evd-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-207](EVD.md#evd-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-300](EVD.md#evd-300) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-301](EVD.md#evd-301) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-302](EVD.md#evd-302) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-303](EVD.md#evd-303) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-304](EVD.md#evd-304) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-305](EVD.md#evd-305) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-306](EVD.md#evd-306) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-400](EVD.md#evd-400) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-401](EVD.md#evd-401) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-402](EVD.md#evd-402) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-501](EVD.md#evd-501) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-502](EVD.md#evd-502) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-503](EVD.md#evd-503) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-504](EVD.md#evd-504) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-505](EVD.md#evd-505) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-506](EVD.md#evd-506) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-600](EVD.md#evd-600) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-601](EVD.md#evd-601) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-602](EVD.md#evd-602) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-603](EVD.md#evd-603) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-604](EVD.md#evd-604) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-605](EVD.md#evd-605) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-700](EVD.md#evd-700) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-701](EVD.md#evd-701) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-702](EVD.md#evd-702) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-703](EVD.md#evd-703) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-704](EVD.md#evd-704) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |

## Compliance for EVD-201 ## {: data-toc-label="EVD-201"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [EVD-201-1](EVD-201.md#evd-201-1) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-201-2](EVD-201.md#evd-201-2) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |

## Compliance for EVD-202 ## {: data-toc-label="EVD-202"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [EVD-202-1](EVD-202.md#evd-202-1) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |

## Compliance for EVD-206 ## {: data-toc-label="EVD-206"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [EVD-206-1](EVD-206.md#evd-206-1) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-206-2](EVD-206.md#evd-206-2) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |

## Compliance for EVD-ASM ## {: data-toc-label="EVD-ASM"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [EVD-ASM-205](EVD-ASM.md#evd-asm-205) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |
| [EVD-ASM-207](EVD-ASM.md#evd-asm-207) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | Validator | ✔ Item Reviewed<br>✔ All Children Linked |

## Compliance for EXP ## {: data-toc-label="EXP"}

| Item {style="width:15%"} | Summary {style="width:55%"} | Score {style="width:0%"} | Score Origin {style="width:5%"} | Status {style="width:25%"} |
| --- | --- | --- | --- | --- |
| [EXP-100](EXP.md#exp-100) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The STM32 firmware shall monitor the arrival of control messages from the RPi 5. If the interval between two consecutive control messages exceeds 100ms, the system shall enter Safe State (motors at 0 and steering centered). H1-100 | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-101](EXP.md#exp-101) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | To avoid misinterpretations of commands (H2-100), all control messages must follow a strict serialization protocol. Values ​​received outside the physical limits of the actuators (e.g., PWM > 100% or steering angle > 30°) sahll be discarded, and the last valid message must be retained for a maximum of 1 cycle. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-102](EXP.md#exp-102) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Each CAN control frame shall contain a 4-bit field for a Rolling Counter. The STM32 must validate if the counter of the new message is different from the previous one (H4-100). If the counter remains static for 3 consecutive cycles, the message will be considered "stale data" and a warning must be issued. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-103](EXP.md#exp-103) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The Raspberry Pi shall transmit control messages at a constant frequency of 500 Hz. Given the short interval between messages (2ms), any delay in scheduling tasks in the AGL can cause packet loss, impacting the stability of high-speed control. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-104](EXP.md#exp-104) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The mapping between CAN IDs and control variables (speed, steer) shall be validated at system initialization. Any frame received with an unexpected ID should be silently discarded. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-201](EXP.md#exp-201) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall be able to detect the absence of pulses for a prolonged period, indicating a possible disconnection or physical failure of the sensor cable. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-202](EXP.md#exp-202) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The software shall apply filtering mechanisms (such as debouncing) to reject spurious pulses and ensure that only valid signals are counted. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-205](EXP.md#exp-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The sensor driver interrupt and processing logic shall execute in an isolated memory region (MPU or TrustZone) to prevent external interference. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-206](EXP.md#exp-206) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The speed calculation algorithm shall correctly handle hardware counter overflow to maintain speed accuracy. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-207](EXP.md#exp-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall cross-reference speedometer data with a secondary speed estimate (such as IMU derivative) to identify inconsistencies. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-300](EXP.md#exp-300) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall guarantee that the task responsible for reading the speed   sensor is executed periodically within its defined deadline, ensuring temporal   predictability in the ThreadX environment and preventing delays that could   compromise vehicle control. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-301](EXP.md#exp-301) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall ensure that every speed sample includes an associated   monotonic timestamp and that stale data is automatically invalidated when it   exceeds the maximum allowed age, preventing the use of outdated information   in vehicle control. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-302](EXP.md#exp-302) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall guarantee exclusive and deterministic access to speed data   shared between concurrent tasks, using RTOS synchronization primitives to   prevent race conditions and data corruption. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-303](EXP.md#exp-303) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall detect and report queue overflows and lost messages in   inter-task communication, ensuring visibility of communication failures that   could compromise the integrity of speed data. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-304](EXP.md#exp-304) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall prevent unbounded priority inversion in safety-critical   tasks by ensuring that RTOS priority inheritance mechanisms are correctly   used to maintain predictable latency in the execution of speed-related   tasks. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-400](EXP.md#exp-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | All software components shall perform data transmission with unit conversion according to the VSS standard. Example: speed should be treated as m/s. H1-400 | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-401](EXP.md#exp-401) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The control system shall consult VSS metadata (min/max) for each actuator signal. Commands that exceed these limits must trigger an integrity error. H2-400 | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-501](EXP.md#exp-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall ensure that displayed vehicle information represents the current system state within an acceptable time window and shall safely handle invalid, missing, or out-of-range data without causing application failure or undefined behavior. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-502](EXP.md#exp-502) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall present warning and status indications whenever critical vehicle conditions are detected, ensuring observer awareness. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-600](EXP.md#exp-600) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must automatically launch all applications necessary for the project to function properly during boot. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-601](EXP.md#exp-601) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system (AGL on Raspberry Pi) has conditions to store all the data necessary for its operation without risk of failure due to lack of space. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-602](EXP.md#exp-602) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The AGL system on Raspberry Pi continuously monitors key parameters such as temperature and voltage to prevent abrupt shutdowns and protect the file system from corruption. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-700](EXP.md#exp-700) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall be be updated at appropriate times and in a security way, ensuring the integrity of the data displayed in the vehicle. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |
| [EXP-701](EXP.md#exp-701) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | All over-the-air (OTA) updates are performed securely, ensuring data integrity and preventing any corruption or tampering that could affect system functionality. | 0.00 | Missing | ⨯ Item Reviewed<br>✔ All Children Linked |


---

_Generated for: Software_

* _Repository root: /home/bruno/Desktop/SEA_ME/Team5_Senna_Tech_
* _Commit SHA: e2206f6429e723bc4f01621d0017d90b3f2cd406_
* _Commit date/time: 2026-01-15 18:57:13 UTC_
* _Commit tag: e2206f6_
