

---

### EVD-100 | Reviewed: ✔ | Score: 0.7 ### {: #evd-100 data-toc-label="EVD-100" .item-element .item-section class="tsf-score" style="background-color:hsl(84.0, 100%, 40%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-100](AST.md#ast-100) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the CAN bus is disconnected or the RPi stops transmitting, the PWM output pins of the STM32 should be brought to 0% within a time interval such that t < 110ms. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-101 | Reviewed: ✔ | Score: 0.5 ### {: #evd-101 data-toc-label="EVD-101" .item-element .item-section class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-101](AST.md#ast-101) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Whenever the STM32 receives a CAN message with a 'Speed' value > 100 or 'Steer' > 30 (e.g., 'Steer' not in [-30, 30]'), respecting the physical limits, the message should be discarded and the previous state of the actuators should be maintained unchanged. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-102 | Reviewed: ✔ | Score: 0.3 ### {: #evd-102 data-toc-label="EVD-102" .item-element .item-section class="tsf-score" style="background-color:hsl(36.0, 100%, 54%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-102](AST.md#ast-102) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If three consecutive CAN frames are received with the same Rolling Counter value, the can_data_fresh flag should be set to false and the Safe State should be triggered. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-103 | Reviewed: ✔ | Score: 1.0 ### {: #evd-103 data-toc-label="EVD-103" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-103](AST.md#ast-103) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the CRC calculated on the 7-byte payload of the CAN message does not match the 8th byte (checksum) sent by the RPi, the STM32 should increment the error counter can_crc_errors and ignore the current frame. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-104 | Reviewed: ✔ | Score: 0.0 ### {: #evd-104 data-toc-label="EVD-104" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-501](ASM.md#asm-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Communication latency remains within the limits defined by the system architecture. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |
| [AST-104](AST.md#ast-104) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The nominal interval between control messages should be 2 ms. The assertion is true if the measured interval T is within the range 1.8 ms <= T >= 2.2 ms. Furthermore, there should be no loss of more than 2 consecutive frames in a 1-second period. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-105 | Reviewed: ✔ | Score: 0.8 ### {: #evd-105 data-toc-label="EVD-105" .item-element .item-section class="tsf-score" style="background-color:hsl(96.0, 100%, 37%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-105](AST.md#ast-105) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | During a 5-minute test, 100% of the frames transmitted by the RPi for control must use the CAN IDs predefined in the protocol specification document (e.g., Speed=0x100, Steer=0x101). | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-106 | Reviewed: ✔ | Score: 0.7 ### {: #evd-106 data-toc-label="EVD-106" .item-element .item-section class="tsf-score" style="background-color:hsl(84.0, 100%, 40%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-100](ASM.md#asm-100) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the actuators (ESC, Servo) have their own internal fail-safe behavior (e.g., PWM signal = 0% results in safe stop) that will be executed if the STM32 stops transmitting PWM due to a fault. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-107 | Reviewed: ✔ | Score: 0.6 ### {: #evd-107 data-toc-label="EVD-107" .item-element .item-section class="tsf-score" style="background-color:hsl(72.0, 100%, 44%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-101](ASM.md#asm-101) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the CAN network is physically terminated with 1200Ω resistors at both ends, minimizing signal reflections that could cause errors at high frequencies such as 500kbps. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/CAN-EVD-100/TIMEOUT_TEST.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-205 | Reviewed: ✔ | Score: 1.0 ### {: #evd-205 data-toc-label="EVD-205" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-205](AST.md#ast-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The firmware MUST configure the Memory Protection Unit (MPU) to enforce read-only access to the sensor driver code and restricted read/write access to its data structures, triggering a fault on unauthorized access. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/logs/mpu_config_test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-207 | Reviewed: ✔ | Score: 1.0 ### {: #evd-207 data-toc-label="EVD-207" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-207](AST.md#ast-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system MUST compare the calculated wheel speed against a secondary estimation source (e.g., IMU) and invalidate the reading if the deviation exceeds the defined error margin. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/reports/plausibility_test_results.pdf
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-300 | Reviewed: ✔ | Score: 1.0 ### {: #evd-300 data-toc-label="EVD-300" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-300](AST.md#ast-300) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The speed sensor task executes periodically within its configured period and   completes execution before its defined deadline on every activation under   normal operating conditions. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-301 | Reviewed: ✔ | Score: 1.0 ### {: #evd-301 data-toc-label="EVD-301" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-301](AST.md#ast-301) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Every speed sample produced by the system includes a monotonic timestamp, and   samples older than the configured freshness threshold are automatically   invalidated and not used by downstream control logic. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-302 | Reviewed: ✔ | Score: 1.0 ### {: #evd-302 data-toc-label="EVD-302" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-302](AST.md#ast-302) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Concurrent tasks accessing shared speed data are synchronized using RTOS   primitives such that no data races, partial writes, or inconsistent reads   occur during execution. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-303 | Reviewed: ✔ | Score: 1.0 ### {: #evd-303 data-toc-label="EVD-303" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-303](AST.md#ast-303) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system detects queue overflows and lost messages in inter-task   communication and reports these events through logs or diagnostic counters   at runtime. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-304 | Reviewed: ✔ | Score: 1.0 ### {: #evd-304 data-toc-label="EVD-304" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-304](AST.md#ast-304) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The RTOS configuration prevents unbounded priority inversion by ensuring that   safety-critical tasks are protected by priority inheritance or equivalent   mechanisms, maintaining bounded execution latency. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-305 | Reviewed: ✔ | Score: 1.0 ### {: #evd-305 data-toc-label="EVD-305" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-300](ASM.md#asm-300) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | All tasks accessing shared speed data use the designated RTOS synchronization   primitives and do not bypass them through direct or unsafe memory access. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-306 | Reviewed: ✔ | Score: 1.0 ### {: #evd-306 data-toc-label="EVD-306" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-301](ASM.md#asm-301) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The RTOS is correctly configured and supports priority inheritance or an   equivalent mechanism for managing priority inversion. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/threadx/test.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-400 | Reviewed: ✔ | Score: 1.0 ### {: #evd-400 data-toc-label="EVD-400" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-400](AST.md#ast-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Not only should the variables be conventionally aligned with the VSS standard, but the units of measurement should also be. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/COVESA-EVD-400/version_vss.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-401 | Reviewed: ✔ | Score: 1.0 ### {: #evd-401 data-toc-label="EVD-401" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-401](AST.md#ast-401) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The code must have a data range validator, if the information sent has a value beyond the max, or less than the min of the range it must be discarded. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/COVESA-EVD-400/version_vss.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-402 | Reviewed: ✔ | Score: 1.0 ### {: #evd-402 data-toc-label="EVD-402" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-400](ASM.md#asm-400) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that both ends of the communication (RPi and STM32) use the same version of the VSS specification file (.vspec) to avoid mapping conflicts. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/COVESA-EVD-400/version_vss.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-501 | Reviewed: ✔ | Score: 0.0 ### {: #evd-501 data-toc-label="EVD-501" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-501](AST.md#ast-501) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall refresh each displayed vehicle parameter at least once every 300 ms. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/car_cluster/logs/cluster_refresh_time.log
          result: PENDING
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-502 | Reviewed: ✔ | Score: 0.0 ### {: #evd-502 data-toc-label="EVD-502" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-502](AST.md#ast-502) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall detect and flag any vehicle parameter that is not updated within the defined freshness time limit (300ms). | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/car_cluster/logs/cluster_limit_refresh_time.log
          result: PENDING
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-503 | Reviewed: ✔ | Score: 0.0 ### {: #evd-503 data-toc-label="EVD-503" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-503](AST.md#ast-503) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall not crash, freeze, or display undefined behavior when receiving invalid, missing, or out-of-range vehicle data. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/car_cluster/logs/cluster_unit_tests_log.xml
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-504 | Reviewed: ✔ | Score: 0.0 ### {: #evd-504 data-toc-label="EVD-504" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-504](AST.md#ast-504) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall display a visible warning indication whenever a critical vehicle condition is reported by the system. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/car_cluster/logs/cluster_warning_on_critical_condition.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-505 | Reviewed: ✔ | Score: 0.0 ### {: #evd-505 data-toc-label="EVD-505" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-505](AST.md#ast-505) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster shall keep the warning indication visible for the entire duration of the critical condition. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: tests/car_cluster/logs/cluster_persistent_warning.log
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-506 | Reviewed: ✔ | Score: 1.0 ### {: #evd-506 data-toc-label="EVD-506" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-504](ASM.md#asm-504) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The instrument cluster hardware is powered continuously since the start of the vehicle operation. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: https://github.com/SEAME-pt/Team5_Senna_Tech/blob/docs/TSF-reqs-Hellom-200/docs/energy/README.md
          result: PASS
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-600 | Reviewed: ✔ | Score: 1.0 ### {: #evd-600 data-toc-label="EVD-600" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-600](AST.md#ast-600) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall immediately start Instrument Cluster using systemd maximum 10 seconds after boot. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: tests/system/logs/system.txt
          test: cluster_auto_start.sh
          result: waiting review
    ````

??? "Click to view validator documentation"
    ````md
    Validator for tests/system
        Checks the system.txt file containing test results
    
        Rules:
        - FAIL -&gt; score = 0.0
        - PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-601 | Reviewed: ✔ | Score: 1.0 ### {: #evd-601 data-toc-label="EVD-601" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-601](AST.md#ast-601) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system shall immediately start a script to verify OTA updates after connected to the internet | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: tests/system/logs/system.txt
          test: check_update_started.sh
          result: waiting review
    ````

??? "Click to view validator documentation"
    ````md
    Validator for tests/system
        Checks the system.txt file containing test results
    
        Rules:
        - FAIL -&gt; score = 0.0
        - PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-602 | Reviewed: ✔ | Score: 0.0 ### {: #evd-602 data-toc-label="EVD-602" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-602](AST.md#ast-602) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If for any reason the auto-start of an application fails, the system should attempt to run it again at least 10 more times. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: pending
          test: pending
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator for tests/system
        Checks the system.txt file containing test results
    
        Rules:
        - FAIL -&gt; score = 0.0
        - PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    [Errno 2] No such file or directory: 'pending'
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-603 | Reviewed: ✔ | Score: 0.0 ### {: #evd-603 data-toc-label="EVD-603" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-603](AST.md#ast-603) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The AGL on the Raspberry Pi 5 must support the entire structure of this project and its features. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: docs/AGL/AGL_support.md
          result: waiting reviewer
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-604 | Reviewed: ✔ | Score: 1.0 ### {: #evd-604 data-toc-label="EVD-604" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-604](AST.md#ast-604) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must include a storage monitoring program. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: tests/system/logs/system.txt
          test: cluster_monitoring_running.sh
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator for tests/system
        Checks the system.txt file containing test results
    
        Rules:
        - FAIL -&gt; score = 0.0
        - PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-605 | Reviewed: ✔ | Score: 0.0 ### {: #evd-605 data-toc-label="EVD-605" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-605](AST.md#ast-605) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The system must include a temperature monitoring program. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: tests/system/logs/system.txt
          test: cluster_monitoring_running.sh
          result: waiting review
    ````

??? "Click to view validator documentation"
    ````md
    Validator for tests/system
        Checks the system.txt file containing test results
    
        Rules:
        - FAIL -&gt; score = 0.0
        - PASS -&gt; score = 1.0
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-700 | Reviewed: ✔ | Score: 0.0 ### {: #evd-700 data-toc-label="EVD-700" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-700](AST.md#ast-700) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new cluster version shall only start on the next time the vehicle turn on again | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: pending
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-701 | Reviewed: ✔ | Score: 0.0 ### {: #evd-701 data-toc-label="EVD-701" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-701](AST.md#ast-701) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new package shall be validated using checksum or hash before installation | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: pending
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-702 | Reviewed: ✔ | Score: 0.0 ### {: #evd-702 data-toc-label="EVD-702" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-702](AST.md#ast-702) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the update fail (wifi, energy drops etc...) the system shall support rollback to the previous versions. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: pending
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-703 | Reviewed: ✔ | Score: 0.0 ### {: #evd-703 data-toc-label="EVD-703" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-703](AST.md#ast-703) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | If the new package update is not safe the system shall support rollback to the previous versions. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: pending
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-704 | Reviewed: ✔ | Score: 0.0 ### {: #evd-704 data-toc-label="EVD-704" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-704](AST.md#ast-704) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | Every OTA update shall be logged with timestamp, version and result (success or fail) | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: pending
          result: pending
    ````

??? "Click to view validator documentation"
    ````md
    Validator that scores test evidence logs.
    
        Rules:
        - Any FAIL -&gt; score = 0.0
        - All PASS -&gt; score = 1.0
    ````

??? "Click to view validator logs"
    ````md
    This evidence is not good
    ````

{% raw %}

**References:**

_None_

{% endraw %}
