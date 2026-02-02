

---

### EVD-ASM-205 | Reviewed: ⨯ | Score: 0.0 ### {: #evd-asm-205 data-toc-label="EVD-ASM-205" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
Technical evidence based on the STM32U5 datasheet, confirming the presence and capabilities of the Memory Protection Unit (MPU).
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-205](ASM.md#asm-205) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the hardware platform (STM32U5) possesses a functional and configurable Memory Protection Unit (MPU) or TrustZone capability. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: docs/energy/components_datasheet.md
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

### EVD-ASM-207 | Reviewed: ⨯ | Score: 0.0 ### {: #evd-asm-207 data-toc-label="EVD-ASM-207" .item-element .item-section class="tsf-score" style="background-color:hsl(0.0, 100%, 65%)"}
Verification of vehicle specifications, confirming that the IMU hardware is available and functional for secondary speed estimation.
{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [ASM-207](ASM.md#asm-207) {class="tsf-score status-unreviewed" style="background-color:hsl(0.0, 100%, 65%)"} | It is assumed that the vehicle possesses a secondary source for speed estimation (e.g., IMU or motor model) with a known error margin. | 0.00 | ⨯ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: reviewer_score
        configuration:
          url: docs/piracer-cpp.md
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
