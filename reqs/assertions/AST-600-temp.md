---
id: AST-600
related_expectation_id: EXP-600
title: Instrument Cluster Auto Start
statement:
  The system shall immediately start Instrument Cluster using systemd maximum 15 seconds after boot.
type: assertion
owner: Senna Tech member
date: 2026-01-08
---


---
id: AST-601
related_expectation_id: EXP-600
title: Check software updates
statement:
  The system shall immediately start a script to verify OTA updates after connected to the internet
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-602
related_expectation_id: EXP-600
title: Auto Start Fail
statement:
  If for any reason the auto-start of an application fails, the system should attempt to run it again at least 10 more times.
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-603
related_expectation_id: EXP-601
title: AGL Support on Raspberry Pi 5
statement: 
  The AGL on the Raspberry Pi 5 must support the entire structure of this project and its features.
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-604
related_expectation_id: EXP-602
title: Storage Monitoring
statement: 
  The system must include a storage monitoring program. 
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-605
related_expectation_id: EXP-602
title: Voltage Monitoring
statement: 
  The system must include a voltage monitoring program.
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-606
related_expectation_id: EXP-602
title: Temperature Monitoring
statement: 
  The system must include a temperature monitoring program and turn off safelly at 85ºC
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

