## 🛡️ Cppcheck Linting Workflow

This document outlines the C/C++ code linting workflow using the **Cppcheck** static analysis tool, integrated with GitHub Actions. Cppcheck is a static analysis tool for C/C++ code that detects various kinds of coding errors, potential bugs, and style issues.



---

### ⚙️ Workflow Details (`.github/workflows/lint.yml`)

The workflow is triggered on every code push or pull request (PR) and uses an Ubuntu virtual machine to perform the analysis.

```yaml
jobs:
  #LINTING CHECK
  linting-cpp:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install tools
        run: |
          sudo apt update
          sudo apt install -y cppcheck 

      - name: Run cppcheck
        run: |
          chmod +x ./scripts/ci-cd/cpp_check.sh
          ./scripts/ci-cd/cpp_check.sh
```

### ⚙️ Job Details: `linting-cpp`

| Configuration | Description |
| :--- | :--- |
| `runs-on: ubuntu-latest` | The job runs on the latest available Ubuntu operating system. |

### Steps

| Step Name | Action/Command | Description |
| :--- | :--- | :--- |
| `Checkout code` | `uses: actions/checkout@v4` | Checks out the repository code. |
| `Install tools` | `sudo apt install -y cppcheck` | Installs the `cppcheck` tool on the GitHub Actions runner environment. |
| `Run cppcheck` | `./scripts/ci-cd/cpp_check.sh` | Makes the check script executable and runs it. **This script must contain the logic to call Cppcheck with the desired parameters.** |

> **Note:** The `scripts/ci-cd/cpp_check.sh` below is critical and should be configured to point Cppcheck to the correct files and directories, as well as define the severity levels and rules to be checked.



```
#!/bin/bash
# run cpp_check.sh

# Exit if any command fail
set -e

cppcheck --enable=style,warning \ # Here you can add directories do supress for examples code generated
        --suppress=unknownMacro \
         -isrc/CAN_communication/ \
         -isrc/threadx \
         -isrc/car_cluster/build \
         --error-exitcode=1 \
         src/

echo "Cppcheck lint success."
```

### Examples of Common Errors Detected by Cppcheck

Below are examples of C++ code with issues that Cppcheck is capable of identifying, demonstrating the seven requested error types.

#### 1. Unused Variable (`unusedVariable`)

```cpp
void calculate_area(int length, int width) {
    int area = length * width; // Warning: Variable 'area' is calculated but not used.
    // ...
}
```

#### 2. Null Pointer Dereference (`nullPointerDereference`)

```cpp
#include <iostream>

void unsafe_access() {
    int* ptr = nullptr;
    // ... ptr is not initialized or allocated ...
    *ptr = 10; // Error: Null pointer dereference (accessing memory through nullptr).
}
```

#### 3. Shadowing Variables (`shadowVariables`)

```cpp
class MyClass {
public:
    int count = 0; // Member variable
    void set_count(int count) { // Local 'count' shadows the member 'count'.
        count = count; // Error: Assigning local variable to itself (typo).
    }
};
```

#### 4. Out of Bounds Access (`outOfBounds`)

```cpp
#include <vector>

void access_vector() {
    std::vector<int> data = {1, 2, 3};
    // The vector has indices 0, 1, and 2.
    int value = data[3]; // Error: Out of bounds access.
}
```

#### 5. Always True Condition (`alwaysTrueCondition`)

```cpp
#include <iostream>

void check_value(int val) {
    // Intention: check if 'val' is 10.
    if (val = 10) { // Error: Assignment (val=10) instead of comparison (val==10).
        std::cout << "Condition is always true." << std::endl;
    }
}
```

Aqui está o bloco de código formatado em Markdown puro, incluindo um título descritivo para o erro:

Markdown

#### 6. Boolean Increment (`booleanIncrement`)

```cpp
bool is_valid = false;
is_valid++; // Warning: Incrementing a boolean variable.
```

#### 7. Division by Zero (`divisionByZero`)

```cpp
int main() {
    int numerator = 10;
    int denominator = 0;
    int result = numerator / denominator; // Error: Division by zero.
    return 0;
}

```