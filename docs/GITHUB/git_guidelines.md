
# 🧭 Rules and Best Practices

This document defines the **rules and best practices** for contributing to this project.  
It ensures that all commits, reviews, and documentation remain **consistent, clear, and maintainable** for the entire team.

## 📑 Table of Contents
1. [Commit Message Format](#1️⃣-commit-message-format)
2. [Pull Requests](#2️⃣-Pull-Requests)
3. [Documentation](#3️⃣-Documentation)
4. [Issues](#4️⃣-Issues)
5. [Directorys and branchs Structure](#5️⃣-Directorys-Structure)


## 1️⃣ Commit Message Format

| Symbol | Meaning |
|:------:|:---------|
| `-` | Deleted something |
| `+` | Added something |
| `~` | Modified something |
| `=` | Refactored something |

### Guidelines
- Each commit must represent **a single logical change**.  
- Avoid commits that include **multiple features or unrelated changes**.  
- **Never commit code that doesn’t compile** (if absolutely necessary, clearly state the reason in the commit description).  
- Commit messages should be **clear and descriptive**.

#### Examples
```bash
# ❌ Bad
git commit -m "update 2FA"

# ✅ Good
git commit -m "+ | added 2FA implementation from SMS"
```

---

## 2️⃣ Pull Requests

- Always create pull requests before merging in the branchs develop or main.  
- In case of a Pull Request for the develop branch, at least 1 other team member must approve it. In case of a merge with the main branch, 2 other members must approve it.
- **NEVER** do git push --force 
- Use **squash merge** to keep the commit history clean and organized.

### ✅ Checklist before pr
- [ ] Does the code follow project standards?  
- [ ] Are there sufficient tests?  
- [ ] Is the functionality complete?  
- [ ] Is there duplicated code?  
- [ ] Was the documentation updated?  
- [ ] Are there any security concerns?

---

## 3️⃣ Documentation
All documentation must be **clear, self-contained, and reproducible**, allowing any team member to understand, continue, or rebuild the work without external guidance.

### Feature Documentation

* Each feature must include its own main documentation file, named README.md, located in the same directory as its code.

* This file should explain:

    * The purpose of the feature.

    * How it works (architecture, logic, data flow, etc.).

    * How to build, test, or run it.

* Any relevant dependencies or configurations.

* The goal is for anyone reading the feature folder to immediately understand and execute it without referring elsewhere.

### General Documentation

The /docs directory (in the project root) is reserved for global or non-feature-specific documentation, such as:

* Project overview and architecture.

* Setup and environment configuration.

* Contribution guidelines.

* Design documents, research, or technical notes.

### Indexing

When multiple topics are covered in a single document, include an index or table of contents at the top to make navigation easier.

## 4️⃣ Issues

Issues should be separated by **type** (`bug`, `feature`, `documentation`, etc.), according to the established template.  

The **title** must be **short, direct, and describe an action**.

In description, clearly state **what** needs to be done.

In objective, explain **why** this task is necessary.

In dependencies, if there are other **tasks required** for its completion, they must be listed here.

In details, add relevant information, **technical considerations**, or **context** related to the issue.

Completion conditions, when creating issues, make sure to list the **completion criteria** so they can be reviewed before closing the issue.

Remember: the issue is only considered completed after complete documentation.

## 5️⃣ Directorys and Branchs Structure
All rules, hierarchies and commands are in the documentation [git_workflow_guide.md](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/documentation/docs/git_workflow_guide.md)

---

## 6️⃣ Project Specifics: STM32 (CubeIDE)

To ensure repository hygiene and avoid "it works on my machine" issues, we adopt the following strategy for STM32CubeIDE generated files.

### 6.1 Files to Track (Commit)
These files are essential for building the project and understanding the configuration.

| Path/Extension | Description | Why Track? |
| :--- | :--- | :--- |
| **`*.ioc`** | STM32CubeMX Configuration File. | **Critical.** Contains the definition of all pins, clocks, and peripherals. Used to regenerate the code structure. |
| **`Core/Src/` & `Core/Inc/`** | Application Source Code. | Contains `main.c`, `stm32u5xx_it.c`, and user logic. This is where the development happens. |
| **`Drivers/`** | HAL & CMSIS Libraries. | Although auto-generated, tracking them ensures **CI/CD pipelines** can build the code without needing STM32CubeMX installed. It also guarantees all developers use the exact same library version. |
| **`*.ld`** | Linker Script (e.g., `STM32U585xx_FLASH.ld`). | Defines memory layout (Flash/RAM addresses). Essential for compilation. |
| **`startup_*.s`** | Assembly Startup Code. | Handles the reset vector and system initialization. |

### 6.2 Files to Ignore (.gitignore)
These files are machine-specific, build artifacts, or personal preferences.

| Path/Extension | Description | Why Ignore? |
| :--- | :--- | :--- |
| **`Debug/` & `Release/`** | Build Output Directories. | Contains binaries (`.elf`, `.bin`, `.hex`) and object files (`.o`). They cause merge conflicts and bloat the repo. |
| **`.settings/`** | Eclipse/IDE Settings Folder. | Often contains absolute paths specific to the user's computer, causing errors for others. |
| **`.mxproject`** | CubeMX Metadata. | Redundant. The IDE regenerates this file from the `.ioc` file automatically. |
| **`*.launch`** | Debug Launch Configurations. | Stores personal debugger settings (like specific probe serial numbers). |



