# Using the Trudag tool with scripts

This is a step-by-step guide to facilitate the use of the Trustable Software Framework (TSF) using Trudag with the aid of custom scripts. Trudag enables the systematic management of software requirements through a Directed Acyclic Graph (DAG), connecting high-level expectations to technical evidence with automated scoring and validation.

---

## 📋 Table of Contents

- [Using the Trudag tool with scripts](#using-the-trudag-tool-with-scripts)
  - [📋 Table of Contents](#-table-of-contents)
  - [🛠 Prerequisites](#-prerequisites)
  - [⚙️ Environment Setup](#️-environment-setup)
  - [📂 Project Structure](#-project-structure)
  - [🚀 The Requirements Workflow](#-the-requirements-workflow)
  - [🎨 Visualizing the Graph (Plotting)](#-visualizing-the-graph-plotting)
  - [🌐 Publishing Documentation](#-publishing-documentation)

---

## 🛠 Prerequisites
- **Python 3.12+**
- **Graphviz** (Required for generating visual graphs):
```bash
sudo apt install graphviz
```

---

## ⚙️ Environment Setup
We use a virtual environment to isolate dependencies.

1. Initialize the environment:
Run the provided setup script to install trustable (Trudag) and its dependencies.
```bash
chmod +x docs/TSFscripts/trudag/trudag_env.sh
.docs/TSF/scripts/trudag/trudag_env.sh
```

2. Activate the Environment:
Note: You must run this command in every new terminal session.
```bash
source venv/bin/activate
```

---

## 📂 Project Structure
The tools expect the following directory organization:
```bash
Team5_Senna_Tech/
├── docs/
│   └── TSF/
│       ├── reqs/               # Requirements source files (.md)
│       ├── scripts/trudag/     # Automation scripts
│       ├── docs/TSF/tests/              # Test files and logs
│       ├── trustable/          # MkDocs generated site source
│       └── graph/              # Generated DAG images
├── venv/                       # Virtual environment
├── .dotstop.dot                # Local database
└── mkdocs.yml                  # Global documentation config
```

---

## 🚀 The Requirements Workflow
1. Write Requirements
The templates contain all the material that needs to be filled in (expectations, assertions, assumptions, and evidence).

2. Register and Link
Use the automated script to validate files, register them into the database, and establish relationships (links):
```bash
.docs/TSF/scripts/trudag/register_reqs.sh
```
When prompted, choose y to rebuild the database if you have changed links or IDs.

3. Calculate Scores
Propagate trust scores from evidence up to expectations:
```bash
trudag score
``` 

---

## 🎨 Visualizing the Graph (Plotting)

Before or after scoring, you can generate a visual map of your requirements to check for logical errors or missing links.

Generate a vector graph (Recommended):
```bash
trudag plot --output docs/TSF/graph/graph.png
```
How to interpret the graph:

Nodes: Represent your requirements (EXP, AST, ASM, EVD).

Edges (Arrows): Represent the "Trust Flow". An arrow from EVD to AST means "this evidence supports this assertion".

---

## 🌐 Publishing Documentation

To turn your Markdown requirements into a professional, searchable website:

1. Install MkDocs Material:
(Ensure venv is active)
```bash
pip install mkdocs-material
```

2. Generate the Report Content:
```bash
trudag publish --output-directory-path ./relatorio_final
```

3. Serve the Website:
```bash
mkdocs serve -f docs/TSF/trustable/mkdocs_trustable.yml
```
Access the report at http://127.0.0.1:8000 (clickable link in the terminal).

💡 Quick Preview: To automate the publishing process (generate graph + fix attributes + start server), simply run:

```bash
./docs/TSF/scripts/trudag/preview_site.sh
```


