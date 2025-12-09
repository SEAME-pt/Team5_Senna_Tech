
# Pull Request Guidelines


1. [Creating Pull Request](#creating-pull-request)
2. [Reviewing Pull Request](#reviewing-pull-request)

## Creating Pull Request

1. Go to the **Pull Requests → New Pull Request** tab.

2. Select the source branch (your branch) and the target branch (e.g., `develop`).

### PR Title
- Keep it short and clear, similar to the main commit:
  - `Fix login validation error`
  - `Add support for dark mode`

### PR Description
- Explain **what**, **why**, and **how** you made the changes.
- Include references to issues, if any:
  ```markdown
  Closes #42
  Fixes #35

In the PR body, use keywords to link issues:

```Closes #number``` → closes the issue when merged.

```Related to #number``` → only references the issue.

### Select Reviewers and Assignees

In the PR sidebar:

- **Reviewers**: choose teammates who should review the code.  

- **Assignees**: the person responsible for the PR.


### Add Labels

Labels help organize and filter PRs:

- `bug`, `feature`, `enhancement`, `documentation`, `chore`

Set them in the **Labels** panel on the right side of the PR.

---

## Reviewing Pull Request

### Open the Pull Request
    1. Go to the repository on GitHub.
    2. Click on the **Pull Requests** tab.
    3. Select the PR you want to review.

### Check the Files Changed
    1. Click on the **Files changed** tab.
    2. Review and verify every files changed.
    3. Use Add a comment to leave inline feedback on specific lines of code.


### Assingnes, labels, reviewers, issues

If the PR author hasn’t properly set any of these fields, you should set them yourself to ensure better PR organization.

### Leave a Review
    1. Click the green **Review changes** button at the top-right of the **Files changed** tab.
    2. Choose one of the options:
      - **Comment** → leave feedback without approving or requesting changes.
      - **Approve** → the PR is good to merge.
      - **Request changes** → the PR needs changes before it can be merged.
    3. Write a summary message in the text box and click **Submit review**.