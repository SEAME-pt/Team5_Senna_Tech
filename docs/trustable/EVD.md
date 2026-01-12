

---

### EVD-604 | Reviewed: ✔ | Score: 1.0 ### {: #evd-604 data-toc-label="EVD-604" .item-element .item-section class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-604](AST.md#ast-604) {class="tsf-score" style="background-color:hsl(120.0, 100%, 30%)"} |  | 1.00 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 1.0_

??? "Click to view validator configuration"
    ````yaml
    type: test_validator
        configuration:
          url: docs/AGL/AGL_install.md
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
