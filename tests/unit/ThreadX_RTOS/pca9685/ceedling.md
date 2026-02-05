# Ceedling Guide

## ⚠️ What is Ceedling?

**Ceedling** is a build management system for C projects, specifically designed for **Unit Testing**. Instead of manually compiling test files, Ceedling acts as a "master controller" that integrates three essential tools:

* **Unity:** The unit testing framework (where you write your `TEST_ASSERT` statements).
* **CMock:** A tool that automatically creates "mock" functions (simulators) from your header files.
* **Rake:** The build engine (based on Ruby) that handles compilation and execution.

It allows you to verify your logic on your development machine (**Host**) rather than waiting to flash it onto a microcontroller (**Target**).

---

## ⚙️ GUIDE

Ceedling is distributed as a **Ruby Gem**, so you need to have Ruby installed first.

### Install Ruby
* **macOS:** Usually pre-installed, but it is recommended to use [Homebrew](https://brew.sh/): `brew install ruby`.
* **Linux (Ubuntu/Debian):** Run `sudo apt install ruby-full build-essential`.

Verify the installation by running:
```bash
ruby -v
```

### Install Ceedling
Once Ruby is ready, install the Ceedling gem via your terminal:

```bash
gem install ceedling
```

## 🚀 Working with Projects

### Create a New Project
To generate a default folder structure and configuration files, run:

```bash
ceedling new my_project
cd my_project
```

### 📂 Project Structure

**A standard Ceedling project looks like this:**

- src/: Your production code (.c and .h).

- test/: Your test files (must start with test_).

- build/: Temporary files generated during testing (safe to delete).

- project.yml: The main configuration file.

### Basic Commands
Run these commands from the root of your project folder:

| Command | Description |
| :--- | :--- |
| **`ceedling test:all`** | Compiles and runs all unit tests. Provides a detailed pass/fail summary. |
| **`ceedling clean`** | Deletes temporary object files and executables. Useful for a quick "refresh". |
| **`ceedling clobber`** | Performs a deep clean. Deletes the entire `build` folder and all generated mocks. |