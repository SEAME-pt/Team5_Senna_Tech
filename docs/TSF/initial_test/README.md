# Trustable Software Framework (TSF) — Initial Validator Implementation
## 1. Objective

This document describes the implementation of an initial Trustable Software Framework (TSF) validation workflow using trudag.

The goal of this exercise is to:

* Validate automated test evidence

* Convert test results into a quantified trust score

* Establish traceability between software artifacts, evidence, and trust claims

This serves as a training and proof-of-concept implementation of TSF principles.

## 2. Scope

The implementation covers:

* Automated shell-based tests

* Evidence collection via a log file

* A custom TSF validator that interprets the log

* Scoring and trust evaluation using trudag

This setup is intentionally simple to focus on process correctness, not system complexity.

## 3. Directory Structure
```
docs/TSF/initial_test/
├── speed_reader.c
├── tests/
│   └── run_tests.sh
├── tsf/
│   └── evidence.log
└── SPEED-TEST_EVIDENCE.md
```
At the repository root:
```
.dotstop_extensions/
└── validators.py
.dotstop.dot
```
## 4. Evidence Generation
### 4.1 Test Execution

Automated tests are executed via a shell script:
```
./run_tests.sh
```
The script:

* Executes all test scripts

* Collects results

* Writes outcomes to evidence.log

### 4.2 Evidence Format

The evidence log contains human-readable test results:
```
--- TSF Evidence Report ---
Running tests...
A2.1: PASS
A1.1: PASS
A3.1: PASS
```
## 5. TSF Item Definition

The evidence is represented as a TSF item using a Markdown file.

### 5.1 Item File (SPEED-TEST_EVIDENCE.md)
```
---
level: "1.1"
normative: true
evidence:
  type: test_log_validator
  configuration:
    path: docs/TSF/initial_test/tsf/evidence.log
references:
  - type: "file"
    path: docs/TSF/initial_test/tsf/evidence.log
---

Automated shell-based tests validating speed range handling and robustness.
```
### 5.2 Meaning

* level: Trust hierarchy level

* normative: Marks the claim as mandatory

* evidence.type: Name of the validator function

* configuration: Parameters passed to the validator

* references: Explicit traceability to the evidence artifact

## 6. Validator Implementation
### 6.1 Location

All local TSF validators are implemented in:
```
.dotstop_extensions/validators.py
```
This location is required by trudag for local extensions.

## 7. Scoring Process

From the repository root (where .dotstop.dot is located):
```
trudag score
```
### 7.1 Behavior

* The validator is automatically discovered

* The evidence log is parsed

* A trust score is calculated

### 7.2 Scoring Logic

| Condition                    | Score |
|-----------------------------|-------|
| Any `FAIL` detected          | 0.0   |
| All tests `PASS`             | 1.0   |
| No recognizable output       | 0.0   |

## 8. Key TSF Principles Demonstrated

This implementation demonstrates:

* Separation of concerns

    * Tests generate evidence

    * Validators interpret evidence

    * TSF computes trust

* Traceability

    * Claims → Evidence → Files

* Conservative trust

    * Missing or unclear evidence results in zero trust

* Automation readiness

    * Fully compatible with CI pipelines

## 9. Lessons Learned

* TSF does not assume test correctness — trust must be justified

* Validators are the critical link between artifacts and trust

* Relative paths are evaluated from the .dotstop.dot directory

* A working TSF setup is infrastructure + discipline, not just tooling

## 10. Next Steps

Possible future improvements:

* Partial scoring based on test coverage

* Severity-based failure weighting

* Multiple validators per item

* Integration with static analysis or runtime metrics

## 11. Conclusion

This initial TSF implementation successfully establishes a repeatable, auditable, and automated trust evaluation pipeline.

It provides a solid foundation for scaling TSF usage to more complex software components and safety requirements.