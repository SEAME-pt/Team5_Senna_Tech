# Trudag Automation Scripts

This directory contains a suite of shell scripts designed to automate the workflow of the Trustable Software Framework (TSF).

## Script Hierarchy & Dependencies

*   **`preview_site.sh`** (Orchestrator)
    *   Executes: `trudag publish`
    *   Executes: **`fix_markdown_attributes.sh`**
    *   Executes: `mkdocs serve`
*   **`register_reqs.sh`** (Standalone)
    *   Executes: `trudag init`, `trudag add`, `trudag update`
*   **`link_reqs.sh`** (Standalone)
    *   Executes: `trudag link`
*   **`trudag_env.sh`** (Standalone)
    *   Executes: `python3 -m venv`, `pip install`

---

## Detailed Description

### 1. `trudag_env.sh`
**Purpose:** Environment Setup.
**Problem Solved:** Ensures an isolated and reproducible Python environment with the correct dependencies for the safety framework.
**Main Commands:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r trudag_aux_dependences.txt
```
**Note on `trudag_aux_dependences.txt`:** This file contains the exact list of required Python dependencies (such as `trudag`, `mkdocs`, `mkdocs-material`, and security plugins), pinned to specific versions to ensure the evidence system is generated consistently across different machines.

### 2. `register_reqs.sh`
**Purpose:** Requirement Registration.
**Problem Solved:** Automates the ingestion of Markdown requirements into the `.dotstop.dot` Trudag database.
**Main Commands:**
```bash
trudag init  # (If the DB doesn't exist)
trudag add --id <ID> --type <TYPE> ...
trudag update --id <ID> ...
```

### 3. `link_reqs.sh`
**Purpose:** Traceability Linking.
**Problem Solved:** Synchronizes the logical connections (graph edges) defined in the Markdown files with the Trudag database.
**Main Commands:**
```bash
trudag link --from <PARENT_ID> --to <CHILD_ID>
```

### 4. `preview_site.sh`
**Purpose:** Site Generation & Preview.
**Problem Solved:** Compiles the final report, applies visual patches, and starts the local server in a single step.
**Main Commands:**
```bash
trudag publish --output-dir docs/TSF/trustable
bash docs/TSF/scripts/trudag/fix_markdown_attributes.sh
mkdocs serve -f docs/TSF/trustable/mkdocs_trustable.yml
```

### 5. `fix_markdown_attributes.sh`
**Purpose:** Visual Patching.
**Problem Solved:** Fixes line-break artifacts in the generated Markdown that prevent CSS classes and expandable components from rendering correctly.
**Main Commands:**
```bash
perl -0777 -i -pe 's/(\\}[ \t]*)\\n\\n\\s*\{: \.expanded-item-element \}/ .expanded-item-element \1/g' "$file"
```

---

## Recommended Workflow

```bash
# 1. Setup Environment
./docs/TSF/scripts/trudag/trudag_env.sh

# 2. Register Items
./docs/TSF/scripts/trudag/register_reqs.sh

# 3. Create Links
./docs/TSF/scripts/trudag/link_reqs.sh

# 4. Preview Report
./docs/TSF/scripts/trudag/preview_site.sh
```
