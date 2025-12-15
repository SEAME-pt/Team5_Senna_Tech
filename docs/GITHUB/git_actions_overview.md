# GitHub Actions Overview

**GitHub Actions** is a CI/CD (Continuous Integration and Continuous Deployment) system built directly into GitHub.  
It allows you to **automate tasks** such as testing, building, analyzing, and deploying software whenever changes occur in your repository.

A **GitHub Actions pipeline** is defined using **YAML** files stored in the `.github/workflows/` directory of your repository.

## Table of contents

- [Events](#events)
- [Jobs](#jobs)
- [Workflows](#workflows)
- [Actions](#actions)
- [Runners](#runners)
- [Understanding the Execution Flow](#understanding-the-execution-flow)
- [Best Practices](#best-practices)
- [Reference](#reference)

---

## Events

An **event** is a specific activity that triggers a workflow.  
Events can be internal to GitHub (e.g., `push`, `pull_request`, `issues`) or external (via `repository_dispatch` or manual triggers like `workflow_dispatch`).

#### Common Event Types

| Event | Description |
|--------|-------------|
| `push` | Triggered when commits are pushed to a branch. |
| `pull_request` | Triggered when a pull request is opened, synchronized, or merged. |
| `workflow_dispatch` | Allows manual execution of workflows from the GitHub UI. |
| `schedule` | Runs workflows based on a cron expression. |
| `repository_dispatch` | Triggers workflows from external systems or other repositories. |
| `issue_comment` | Triggered when someone comments on an issue or PR. |

#### Example

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
  ```
This workflow triggers on:
- Every push to the main branch
- Every PR targeting main
- Manual runs via the GitHub UI

## Jobs
A **job** is a group of **steps** executed on the **same runner** within a workflow.  
Each step can be:

- A **shell command** (using `run:`)  
- An **action** (using `uses:`)

Steps run **in sequence** and can **share data** since they execute in the same environment.

#### Example

```yaml
jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build application
        run: make build

      - name: Test application
        run: make test
  ```

Jobs run **in parallel by default**, but you can define dependencies using `needs:`.
A dependent job will only start after its prerequisite jobs complete successfully.
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: make build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: make test
```
#### Matrix Strategy
You can run the same job multiple times with different variables (e.g., OS, Python version, or architecture) using a **matrix**.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m build
```
In this example:
- The job will be replicated **9 times** (1 per combination Python-version x OS)
- GitHub Actions creates multiple builds for each **OS and Python version combination**.
- All build jobs run **in parallel**.


## Workflows

A **workflow** is an automated process defined in a YAML file under **.github/workflows/.**

Each workflow is composed of:
- One or more jobs
- Each job containing one or more steps
- Each step using actions or custom scripts

#### Basic Workflow Structure
```yaml
name: CI Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4 #uses a specific pre existing action 

      - name: Run build
        run: make build #run a custom script
```

## Actions

**Actions** are reusable units of logic that can be executed in steps.
They can be:
- Official GitHub Actions (e.g., actions/checkout, actions/setup-python)
- Custom actions (defined in your repo or imported from others
- Composite actions (a combination of multiple smaller actions
#### Example
``` yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"

```

## Runners

#### What Is a Runner?

A **runner** is a virtual machine (VM) or physical machine that executes the jobs defined in your workflow. Each job runs in a clean, isolated environment — ensuring consistency and reproducibility across builds.

When you define a job with:

``` yaml
runs-on: ubuntu-latest

```
GitHub automatically assigns a hosted runner (from GitHub's infrastructure) that provides the specified operating system image.

#### Runner Types

| Runner Type | Description |
|-------------|-------------|
| GitHub-Hosted Runners | Managed by GitHub. Automatically created and destroyed for each job. Supports Ubuntu, Windows, and macOS. |
| Self-Hosted Runners | Managed by you. Runs on your own machine or cloud server. Useful for private environments, special dependencies, or hardware access. |

#### Example: GitHub-Hosted Runner
```yaml
jobs:
  tsf_analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Analysis
        run: trudag run structure_analysis --config .trustable-config.yaml
```
In this case:

- GitHub automatically starts a temporary **Ubuntu VM**
- Installs all dependencies
- Runs the defined steps
- Deletes the environment after completion

#### Example: Self-Hosted Runner
```yaml
jobs:
  custom_analysis:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Execute Custom TSF Step
        run: trudag run generate_report

```
In this setup:

- You register your own machine as a self-hosted runner
- Jobs run directly on that machine
- It remains persistent between runs (allowing caching or heavy dependencies)

## Understanding the Execution Flow

1. An **event** occurs (e.g., `push` to main)
2. GitHub reads the corresponding **workflow** YAML
3. The workflow runs its defined **jobs**
4. Each job is assigned to a **runner**
5. The runner executes **steps** (actions or commands)
6. Logs, statuses, and artifacts are uploaded to GitHub

## Best Practices

✅ Use separate jobs for independent stages (build, test, analysis)  
✅ Cache dependencies to speed up workflows (actions/cache@v4)  
✅ Use secrets for API keys and sensitive data (`${{ secrets.TOKEN }}`)  
✅ Keep workflow files readable and modular


## Reference
This document was based in the official documentation from [GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions)
