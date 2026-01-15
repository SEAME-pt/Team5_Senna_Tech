from typing import TypeAlias

yaml: TypeAlias = str | int | float | bool | list["yaml"] | dict[str, "yaml"]


def test_log_validator(configuration: dict[str, yaml]) -> tuple[float, list[Exception | Warning]]:
    """
    Validator that scores test evidence logs.

    Rules:
    - Any FAIL -> score = 0.0
    - All PASS -> score = 1.0
    """

    issues: list[Exception | Warning] = []

    log_path = configuration.get("path")

    if not log_path:
        issues.append(ValueError("Missing 'path' in validator configuration"))
        return (0.0, issues)

    try:
        with open(log_path, "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        issues.append(e)
        return (0.0, issues)

    if "FAIL" in content:
        return (0.0, issues)

    if "PASS" in content:
        return (1.0, issues)

    issues.append(Warning("No PASS or FAIL entries found in evidence log"))
    return (0.0, issues)


def reviewer_score(configuration: dict[str, yaml]) -> tuple[float, list[Exception | Warning]]:
    """
    Validator that scores test evidence logs.

    Rules:
    - Any FAIL -> score = 0.0
    - All PASS -> score = 1.0
    """

    issues: list[Exception | Warning] = []

    log_path = configuration.get("url")
    result = configuration.get("result")

    if not log_path:
        issues.append(ValueError("Missing 'url' in validator configuration"))
        return (0.0, issues)
    
    if (result != "PASS"):
        issues.append(ValueError("This evidence is not good"))
        return (0.0, issues)
    return (1.0, issues)


def static_analysis_validator(configuration: dict[str, yaml]) -> tuple[float, list[Exception | Warning]]:
    """
    Validator for static analysis reports (e.g., cppcheck).
    Checks if the report file contains a specific success pattern.
    """
    issues: list[Exception | Warning] = []
    report_path = configuration.get("path")
    # Default pattern for many tools is stating 0 errors found
    success_pattern = configuration.get("success_pattern", "0 errors")

    if not report_path:
        issues.append(ValueError("Missing 'path' in validator configuration"))
        return (0.0, issues)

    try:
        with open(report_path, "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        issues.append(e)
        return (0.0, issues)

    if success_pattern in content:
        return (1.0, issues)

    issues.append(Warning(f"Success pattern '{success_pattern}' not found in report"))
    return (0.0, issues)
