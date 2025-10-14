
# 🧭 Git Workflow Guide (Team Manual)

This document describes the **branching strategy**, **naming conventions**, and **Pull Request (PR)** workflow for the *Electric Car Project* team.  
Following these standards keeps our repository clean, traceable, and conflict-free.

---

## 🌳 Branch Structure

We use a **simplified Git Flow** model:
```
main
│
└── develop
    ├── feature/motor-control
    ├── feature/gui-qt
    ├── feature/battery-module
    └── fix/sensor-bug
```

###  `main`
- Contains **stable, production-ready code** only.
- Protected branch — no direct commits or merges allowed.

###  `develop`
- The **integration branch** where new features are merged and tested.
- Represents the latest development state.

###  `feature/*`
- Used for new functionality or large improvements.
- Created from `develop`, merged back into `develop`.

###  `fix/*`
- Used for bug fixes during normal development.
- Created from `develop`, merged back after review.

---

## 🧩 Branch Naming Rules

| Type | Example | Description |
|------|----------|-------------|
| `feature/` | `feature/gui-qt` | New functionality |
| `fix/` | `fix/sensor-calibration` | Non-critical bug fix |
| `docs/` | `docs/update-readme` | Documentation update |
| `test/` | `test/simulation-module` | Testing-related changes |

**Rules:**
- Use **lowercase letters** and **hyphens** (`-`) to separate words.
- Keep it descriptive but short.
- One purpose per branch.

---

## ⚙️ Creating and Merging Branches

### 🪴 Create a new feature branch
```
git checkout develop
git pull
git checkout -b feature/gui-qt
```

### 🧑‍💻 Work and commit
```
git add .
git commit -m "Implement basic Qt GUI window"
```

### 🔄 Sync regularly
```
git pull origin develop
```

### 📤 Push branch to GitHub
```
git push -u origin feature/gui-qt
```

### 🔀 Pull Request (PR) Workflow
### 1. **Open a PR**

* Go to GitHub → _Pull Requests_ → _New Pull Request_

* **Base branch:** `develop`

* **Compare branch:** your `feature/...` branch

* Fill title and description clearly:
```
[Feature] Implement Qt GUI base structure
- Added main window and layout
- Connected signals and slots
- Updated CMakeLists.txt
```

### 1. **Code Review**

* Another teammate must review before merging.

* Use GitHub comments to discuss improvements.

### 3. **Merge**

* After approval, merge the PR into develop.

### 4. **Delete Branch**

After merge, delete your branch from GitHub.

---

## 🧭 Summary Diagram
```
main  ←──────────────  release tags
 │
 └── develop  ←─────  integration branch
       ├── feature/gui-qt
       ├── feature/motor-control
       └── fix/sensor-bug
```

## ✅ Best Practices

* Never commit directly to main or develop.

* Keep branches small and focused.

* Always pull the latest changes before merging.

* Reference issues in commits:
    ```
    git commit -m "Add motor temperature monitoring (#42)"
    ```
* Ensure code passes tests before opening a PR.

* Update documentation if behavior or architecture changes.
