

---

### EVD-100 | Reviewed: ✔ | Score: 1.0 ### {: #evd-100 data-toc-label="EVD-100" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

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
    type: test_log_validator
        configuration:
          path: tests/CAN-EVD-100/TIMEOUT_TEST.log
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
