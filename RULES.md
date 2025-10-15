
# 🧭 Rules and Best Practices

This document defines the **rules and best practices** for contributing to this project.  
It ensures that all commits, reviews, and documentation remain **consistent, clear, and maintainable** for the entire team.

## 📑 Index
1. [Commit Message Format](#1️⃣-commit-message-format)
2. [Review and Merge](#2️⃣-review-and-merge)
3. [Repository Documentation](#3️⃣-repository-documentation)
4. [Issues](#4️⃣-Issues)


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

## 2️⃣ Review and Merge

- Always create **Pull Requests / Merge Requests** before merging.  
- Request a review from **at least one teammate**.  
- Use **squash merge** to keep the commit history clean and organized.

### ✅ Review Checklist
- [ ] Does the code follow project standards?  
- [ ] Are there sufficient tests?  
- [ ] Is the functionality complete?  
- [ ] Is there duplicated code?  
- [ ] Was the documentation updated?  
- [ ] Are there any security concerns?

---

## 3️⃣ Documentation

Always document everything **clearly** — any reader should be able to understand what has been developed and how it works.

### Recommended Structure
```bash
README.md                         # Project overview
DOC_[object_name].md              # Detailed documentation of a specific module or feature
```

## 4️⃣ Issues

Issues should be separated by **type** (`bug`, `feature`, `documentation`, etc.), according to the established template.  
The **title** must be **short, direct, and describe an action**.

In description, clearly state **what** needs to be done.

In Objective, explain **why** this task is necessary.

In dependencies, if there are other **tasks required** for its completion, they must be listed here.

In details, add relevant information, **technical considerations**, or **context** related to the issue.

Completion conditions, when creating issues, make sure to list the **completion criteria** so they can be reviewed before closing the issue.


