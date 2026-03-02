

---

### EVD-100 | Reviewed: ✔ | Score: 1.0 ### {: #evd-100 data-toc-label="EVD-100" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-100](AST.md#ast-100) {class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"} |  | 0.50 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: docs/TSF/tests-log/CAN-EVD-100/CAN_evidence_log.txt
          test: bus load
          result: PASS
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

### EVD-101 | Reviewed: ✔ | Score: 0.33 ### {: #evd-101 data-toc-label="EVD-101" .item-element .item-section class="tsf-score" style="background-color:hsl(39.6, 100%, 53%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-101](AST.md#ast-101) {class="tsf-score" style="background-color:hsl(19.8, 100%, 59%)"} |  | 0.17 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: docs/TSF/tests-log/CAN-EVD-100/CAN_evidence_log.txt
          test: EXP-101
          result: PASS
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

### EVD-102 | Reviewed: ✔ | Score: 1.0 ### {: #evd-102 data-toc-label="EVD-102" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-102](AST.md#ast-102) {class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"} |  | 0.50 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: docs/TSF/tests-log/CAN-EVD-100/CAN_evidence_log.txt
          test: EXP-102
          result: PASS
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

### EVD-103 | Reviewed: ✔ | Score: 0.0 ### {: #evd-103 data-toc-label="EVD-103" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-103](AST.md#ast-103) {class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"} |  | 0.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.0_

??? "Click to view validator configuration"
    ````yaml
    type: system_log_validator
        configuration:
          url: docs/TSF/tests-log/CAN-EVD-100/CAN_evidence_log_103.txt
          test: EXP-103 (ESTOP_LATENCY)
          result: PASS
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
    [Errno 2] No such file or directory: 'docs/TSF/tests-log/CAN-EVD-100/CAN_evidence_log_103.txt'
    ````

{% raw %}

**References:**

_None_

{% endraw %}


---

### EVD-205 | Reviewed: ⨯ | Score: 0.0 ### {: #evd-205 data-toc-label="EVD-205" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
Verification log confirming the correct configuration of the Memory Protection Unit (MPU). The speed sensor driver is isolated in a restricted memory region.
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
          url: docs/TSF/tests/logs/mpu_config_test.log
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

### EVD-207 | Reviewed: ⨯ | Score: 0.0 ### {: #evd-207 data-toc-label="EVD-207" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
Plausibility check evidence comparing wheel speed data with IMU estimation. The cross-reference validates the consistency of the sensor readings.
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
          url: docs/TSF/tests/evidences/imu_cross_check.mp4
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

### EVD-300 | Reviewed: ✔ | Score: 1.0 ### {: #evd-300 data-toc-label="EVD-300" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/threadx/test.log
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

### EVD-301 | Reviewed: ✔ | Score: 1.0 ### {: #evd-301 data-toc-label="EVD-301" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/threadx/test.log
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

### EVD-302 | Reviewed: ✔ | Score: 1.0 ### {: #evd-302 data-toc-label="EVD-302" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/threadx/test.log
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

### EVD-303 | Reviewed: ✔ | Score: 1.0 ### {: #evd-303 data-toc-label="EVD-303" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/threadx/test.log
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

### EVD-304 | Reviewed: ✔ | Score: 1.0 ### {: #evd-304 data-toc-label="EVD-304" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/threadx/test.log
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

### EVD-305 | Reviewed: ✔ | Score: 1.0 ### {: #evd-305 data-toc-label="EVD-305" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/threadx/test.log
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

### EVD-306 | Reviewed: ✔ | Score: 1.0 ### {: #evd-306 data-toc-label="EVD-306" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

**Supported Requests:**

_None_

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: docs/TSF/tests/threadx/test.log
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

### EVD-400 | Reviewed: ✔ | Score: 1.0 ### {: #evd-400 data-toc-label="EVD-400" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/COVESA-EVD-400/version_vss.log
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

### EVD-401 | Reviewed: ✔ | Score: 1.0 ### {: #evd-401 data-toc-label="EVD-401" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/COVESA-EVD-400/version_vss.log
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

### EVD-402 | Reviewed: ✔ | Score: 1.0 ### {: #evd-402 data-toc-label="EVD-402" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests/COVESA-EVD-400/version_vss.log
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

### EVD-501 | Reviewed: ✔ | Score: 0.0 ### {: #evd-501 data-toc-label="EVD-501" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

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
          url: docs/TSF/tests/car_cluster/logs/cluster_refresh_time.log
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

### EVD-502 | Reviewed: ✔ | Score: 0.0 ### {: #evd-502 data-toc-label="EVD-502" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

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
          url: docs/TSF/tests/car_cluster/logs/cluster_limit_refresh_time.log
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

### EVD-503 | Reviewed: ✔ | Score: 0.0 ### {: #evd-503 data-toc-label="EVD-503" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

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
          url: docs/TSF/tests/car_cluster/logs/cluster_unit_tests_log.xml
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

### EVD-504 | Reviewed: ✔ | Score: 0.0 ### {: #evd-504 data-toc-label="EVD-504" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

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
          url: docs/TSF/tests/car_cluster/logs/cluster_warning_on_critical_condition.log
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

### EVD-505 | Reviewed: ✔ | Score: 0.0 ### {: #evd-505 data-toc-label="EVD-505" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

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
          url: docs/TSF/tests/car_cluster/logs/cluster_persistent_warning.log
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

### EVD-506 | Reviewed: ✔ | Score: 1.0 ### {: #evd-506 data-toc-label="EVD-506" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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

### EVD-600 | Reviewed: ✔ | Score: 1.0 ### {: #evd-600 data-toc-label="EVD-600" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests-log/system/system.txt
          test: cluster_auto_start.sh
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

### EVD-601 | Reviewed: ✔ | Score: 1.0 ### {: #evd-601 data-toc-label="EVD-601" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

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
          url: docs/TSF/tests-log/system/system.txt
          test: check_update_started.sh
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

### EVD-602 | Reviewed: ✔ | Score: 0.0 ### {: #evd-602 data-toc-label="EVD-602" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

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

### EVD-603 | Reviewed: ✔ | Score: 0.0 ### {: #evd-603 data-toc-label="EVD-603" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-603](AST.md#ast-603) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new cluster version shall only start on the next time the vehicle turn on again | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

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

### EVD-604 | Reviewed: ✔ | Score: 1.0 ### {: #evd-604 data-toc-label="EVD-604" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)" .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-604](AST.md#ast-604) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | The new package shall be validated using checksum or hash before installation | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: scripts/ci-cd/release/cluster_release.sh
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
