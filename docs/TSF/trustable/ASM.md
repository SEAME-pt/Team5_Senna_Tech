

---

### ASM-100 | Reviewed: ✔ | Score: 0.0 ### {: #asm-100 data-toc-label="ASM-100" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-100](AST.md#ast-100) {class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"} |  | 0.50 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-101 | Reviewed: ✔ | Score: 0.0 ### {: #asm-101 data-toc-label="ASM-101" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-101](AST.md#ast-101) {class="tsf-score" style="background-color:hsl(19.8, 100%, 59%)"} |  | 0.17 | ✔ Item Reviewed<br>✔ Link Reviewed |
| [AST-102](AST.md#ast-102) {class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"} |  | 0.50 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-102 | Reviewed: ✔ | Score: 0.0 ### {: #asm-102 data-toc-label="ASM-102" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-103](AST.md#ast-103) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-205 | Reviewed: ⨯ | Score: 0.0 ### {: #asm-205 data-toc-label="ASM-205" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-201](AST.md#ast-201) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the time counter between pulses exceeds the calibrated threshold (e.g., 500ms), the system MUST transition to the "Signal Lost" error state. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-205](AST.md#ast-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The firmware MUST configure the Memory Protection Unit (MPU) to enforce read-only access to the sensor driver code and restricted read/write access to its data structures, triggering a fault on unauthorized access. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-206](AST.md#ast-206) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the capture timer overflows, the calculation logic MUST handle the event to prevent the speed from being calculated as zero or an incorrect momentary value. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-207](AST.md#ast-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system MUST compare the calculated wheel speed against a secondary estimation source (e.g., IMU) and invalidate the reading if the deviation exceeds the defined error margin. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-ASM-205](EVD-ASM.md#evd-asm-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Technical evidence based on the STM32U5 datasheet, confirming the presence and capabilities of the Memory Protection Unit (MPU). | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-207 | Reviewed: ⨯ | Score: 0.0 ### {: #asm-207 data-toc-label="ASM-207" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
It is assumed that the vehicle possesses a secondary source for speed estimation (e.g., IMU or motor model) with a known error margin.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-201](AST.md#ast-201) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the time counter between pulses exceeds the calibrated threshold (e.g., 500ms), the system MUST transition to the "Signal Lost" error state. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-207](AST.md#ast-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system MUST compare the calculated wheel speed against a secondary estimation source (e.g., IMU) and invalidate the reading if the deviation exceeds the defined error margin. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-ASM-207](EVD-ASM.md#evd-asm-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Verification of vehicle specifications, confirming that the IMU hardware is available and functional for secondary speed estimation. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-300 | Reviewed: ⨯ | Score: 0.0 ### {: #asm-300 data-toc-label="ASM-300" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  All tasks accessing shared speed data use the designated RTOS synchronization
  primitives and do not bypass them through direct or unsafe memory access.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-302](AST.md#ast-302) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Concurrent tasks accessing shared speed data are synchronized using RTOS   primitives such that no data races, partial writes, or inconsistent reads   occur during execution. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-305](EVD.md#evd-305) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-400 | Reviewed: ⨯ | Score: 0.0 ### {: #asm-400 data-toc-label="ASM-400" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
  It is assumed that both ends of the communication (RPi and STM32) use the same version of the VSS specification file (.vspec) to avoid mapping conflicts.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-400](AST.md#ast-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Not only should the variables be conventionally aligned with the VSS standard, but the units of measurement should also be. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-401](AST.md#ast-401) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The code must have a data range validator, if the information sent has a value beyond the max, or less than the min of the range it must be discarded. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-402](EVD.md#evd-402) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-501 | Reviewed: ⨯ | Score: 0.0 ### {: #asm-501 data-toc-label="ASM-501" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
Communication latency remains within the limits defined by the system architecture.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-501](AST.md#ast-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall refresh each displayed vehicle parameter at least once every 300 ms. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

{% raw %}

**References:**

_None_

{% endraw %}


---

### ASM-504 | Reviewed: ⨯ | Score: 0.0 ### {: #asm-504 data-toc-label="ASM-504" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
The instrument cluster hardware is powered continuously since the start of the vehicle operation.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-504](AST.md#ast-504) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall display a visible warning indication whenever a critical vehicle condition is reported by the system. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [EVD-506](EVD.md#evd-506) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

{% raw %}

**References:**

_None_

{% endraw %}
