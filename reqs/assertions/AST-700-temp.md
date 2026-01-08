---
id: AST-700
related_expectation_id: EXP-700
title: Cluster New Update
statement: 
  The new cluster version shall only start on the next time the vehicle turn on again
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-701
related_expectation_id: EXP-701
title: Package integrity validation
statement: 
  The new package shall be validated using checksum or hash befora installation
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-702
related_expectation_id: EXP-701
title: OTA update fail
statement: 
  If the update fail (wifi, energy drops etc...) the system shall support rollback to the previous versions.
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-703
related_expectation_id: EXP-701
title: OTA integrity fail
statement: 
  If the new package update is not safe the system shall support rollback to the previous versions.
type: assertion
owner: Senna Tech member
date: 2026-01-08
---

---
id: AST-704
related_expectation_id: EXP-701
title: OTA logs
statement: 
  Every OTA update shall be logged with timestamp, version and result (success or fail)
type: assertion
owner: Senna Tech member
date: 2026-01-08
---