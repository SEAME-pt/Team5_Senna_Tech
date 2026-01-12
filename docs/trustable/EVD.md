

---

### EVD-600 | Reviewed: ✔ | Score: 0.5 ### {: #evd-600 data-toc-label="EVD-600" .item-element .item-section class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-600](AST.md#ast-600) {class="tsf-score" style="background-color:hsl(60.0, 100%, 47%)"} |  | 0.50 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.5_

??? "Click to view validator configuration"
    ````yaml
    type: test_validator
        configuration:
          url: docs/AGL/AGL_setup.md
          score: 0.5
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

### EVD-604 | Reviewed: ✔ | Score: 0.8 ### {: #evd-604 data-toc-label="EVD-604" .item-element .item-section class="tsf-score" style="background-color:hsl(96.0, 100%, 37%)"}

{: .expanded-item-element }

**Supported Requests:**

| Item {style="width:25%"} | Summary {style="width:50%"} | Score {style="width:0%"} | Status {style="width:25%"} |
| --- | --- | --- | --- |
| [AST-604](AST.md#ast-604) {class="tsf-score" style="background-color:hsl(96.0, 100%, 37%)"} |  | 0.80 | ✔ Item Reviewed<br>✔ Link Reviewed |

**Supporting Items:**

_None_

**Validator:**

_Validator Score: 0.8_

??? "Click to view validator configuration"
    ````yaml
    type: test_validator
        configuration:
          url: docs/AGL/AGL_install.md
          score: 0.8
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
