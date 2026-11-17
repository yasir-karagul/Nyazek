# ADR-0001: Development workflow and repository foundation

- **Status:** Accepted (owner, 2026-11-15)
- **Date:** 2026-11-15
- **Decided by:** Owner

## Context

Nyazek is built by one AI engineering agent (Claude Code) under owner supervision. The agent needs one unambiguous answer to "what do I do next, and where are my instructions". The PRD draft (`docs/prd/08-engineering/claude-workflow.md`) describes a workflow based on GitHub issues and assumes a finalized stack; the PRD has not yet been reviewed, and the stack is not finalized.

## Decision

1. **Lifecycle:** PRD → Architecture → Implementation Guide → MASTER_TASKS → implementation → risk-based reviews → findings → MASTER_TASKS → fixes → re-review → IMPLEMENTATION_STATUS.
2. **Tasks:** `tasks/MASTER_TASKS.md` is the only source of truth for tasks and statuses. It is an index; detail lives in per-task files. GitHub issues are not used for now.
3. **Instructions chain:** `CLAUDE.md` holds the session protocol; a task links to the guide files, PRD sections and ADRs it needs; Claude reads only those. The owner starts every task and is the only one who sets `done`.
4. **Documents with one job each:** `MASTER_TASKS.md` (tasks), `IMPLEMENTATION_STATUS.md` (high-level progress), `docs/implementation-guide/` (how, one topic per file, indexed by its README), `CLAUDE.md` (concise project-wide rules).
5. **Reviews:** four independent disciplines — code, architecture, security, documentation — each a fresh-context subagent following a checklist skill. Reviews run according to the task's risk tags, not all on every change. Reports go to `docs/reviews/<discipline>/`; valid findings become tasks.
6. **Repository:** folder names under `docs/` are lowercase; the PRD lives in `docs/prd/`. Folders are created when they first hold content.
7. **GitHub:** work stays local; every push or other GitHub change needs separate owner approval.
8. **Graphify:** optional code-navigation aid, generated only when installed and needed; whether its output is committed is deferred until code exists.

## Consequences

- This ADR overrides `docs/prd/08-engineering/claude-workflow.md` where they differ (task tracking in GitHub issues, `docs/tasks/`, the assumed stack and repository layout). That document is aligned during its PRD review (T-0010).
- Task tracking works offline and is versioned with the code; there is no issue-tracker view unless one is added later.
- The task-area folders under `tasks/` and the guide subfolders are named after the architecture phase.
