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
