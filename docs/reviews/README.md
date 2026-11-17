# Reviews

Reports from the four independent review disciplines. Each discipline has a subagent (`.claude/agents/`) and a checklist skill (`.claude/skills/`). Which reviews run for a change is decided by the task's risk tags (see `CLAUDE.md`).

## Where reports go

`docs/reviews/<discipline>/YYYY-MM-DD-<task-id>-<slug>.md`, with `<discipline>` one of `code`, `architecture`, `security`, `documentation`. The folder is created with its first report. A re-review is a new file that names the report it follows up.

## Report format

```
# <Discipline> review — <task ID>: <title>
Date · Reviewer agent · Scope (files, commits or documents reviewed) · Follows up: <report or —>

## Verdict
approve | approve with findings | changes required

## Findings
| ID | Severity | Location | Finding | Recommended fix |

## Not reviewed
Anything in scope that could not be checked, and why.
```

- **Finding IDs:** `F-CODE-NNN`, `F-ARCH-NNN`, `F-SEC-NNN`, `F-DOC-NNN`, numbered continuously per discipline across all reports.
- **Severity:** `critical` (blocks; unsafe or wrong) · `major` (must fix before `done`) · `minor` (fix or consciously defer) · `note` (no action required).
- A finding states what is wrong, where, and why it matters. Reviewers report; they do not edit the work under review.

## From finding to task

Every valid finding becomes a row in `tasks/MASTER_TASKS.md` with the finding ID in its Source column. A finding judged invalid is marked so in the report with the reason. `critical` and `major` findings must be `done` and re-reviewed before the original task can be `done`. The author never declares invalid, lowers the severity of, or defers a `critical` or `major` security or architecture finding; a disputed one keeps the task `blocked` until the owner rules (ADR-0005 point 2.4).
