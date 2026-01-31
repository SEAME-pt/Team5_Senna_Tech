## 🧠 Trustable Software Framework (TSF) & Traceability

This directory is the central hub for the Trustable Software Framework (TSF) implementation within the Senna Tech project. It integrates ISO 26262 functional safety concepts with the Trudag tool to create a mathematically verifiable traceability chain.

# 📁 Directory Structure

| Folder | Description | Primary Usage |
|--------|-------------|---------------|
| **reqs/** | **The Core.** Contains formal safety definitions (EXP, AST, ASM, EVD). | Edit/Create `.md` files here to modify the safety logic. |
| **scripts/** | **Automation.** Python and Bash scripts to manage the TSF database. | Run these to register requirements or generate the site. |
| **trustable/** | **Generated Output.** The MkDocs source for the safety website. | **Do not edit manually.** This is updated by `preview_site.sh`. |
| **decision_support/** | **Justifications.** In-depth mitigation and hazard analysis. | Link these files in your requirements as supporting evidence. |
| **tutorials/** | **Knowledge Base.** ISO 26262 theory and TSF learning concepts. | Onboarding for new members to understand the methodology. |
| **initial_test/** | **Prototyping.** Early-stage tests and reference C implementations. | Reference for algorithm validation before final integration. |
| **tests_log/** | **Evidence Source.** Physical test logs and static analysis reports. | Store `.txt` or `.log` files here to be validated by Trudag. |
| **practice/** | **Cheat Sheets.** Quick guides for Trudag syntax and commands. | Quick lookup for writing new statements. |

## 🚀 The Requirements Workflow

To maintain a valid safety case, follow this "Trust Flow":

### 1. **Define** (`reqs/`)
   - Write **Expectations (EXP)** based on the HARA
   - Create **Assertions (AST)** detailing specific system behaviors

### 2. **Execute & Log**
   - Develop your code and run tests
   - Save the resulting logs in `tests-log/`

### 3. **Register** (`scripts/trudag`)
   - Run the `register_reqs.sh` script to register in the database and link EXP, AST, ASM, and EVD.
   - If this is the first time you are running the script, first run `trudag_env.sh` to install all the necessary dependencies.

### 4. **Publish**
   - Use the `preview_site.sh` script to generate the final documentation
   - Generate the traceability graph for visualization

# 🛠️ Essential Commands

Always run these commands from the root of the repository with your virtual environment active:

### 1. **Setup Environment**
```bash
# Prepare the TSF environment and install dependencies
./docs/TSF/scripts/trudag/trudag_env.sh
source venv/bin/activate
```

### 2. Synchronize Database
```bash
# Run this whenever you create or modify a requirement in /reqs
./docs/TSF/scripts/trudag/register_reqs.sh
```

### 3. Visualize & Serve
```bash
# Generates the DAG graph and starts the local documentation server
./docs/TSF/scripts/trudag/preview_site.sh
```

## 📊 Statement Hierarchy (Nomenclature)
We use a standardized ID system to ensure the graph maps correctly:

HARA-XXX: Hazard Analysis and Risk Assessment.

EXP-XXX: High-level goals (e.g., "The vehicle must maintain lateral stability").

AST-XXX: Technical claims (e.g., "The steering motor must respond within 10ms").

ASM-XXX: Accepted truths or external dependencies (e.g., "Hardware is calibrated").

EVD-XXX: Proof of fulfillment (e.g., unit test logs or code reviews).