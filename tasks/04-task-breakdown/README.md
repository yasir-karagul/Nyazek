# Phase 4: Task Breakdown

**Purpose:** turn the PRD, architecture and guide into implementation tasks that Claude Code can pick from `MASTER_TASKS.md` one at a time, each sized for one focused session and one branch.

**Entry:** T-0047 done.
**Exit (T-0053):** the tasks for delivery Phase 1 (Foundation, [release-plan](../../docs/prd/00-governance/release-plan.md) §2) are written and approved; later delivery phases have epics, and their tasks are written at the start of each phase so they reflect what was learned.

## Deliverables

| Task | Deliverable |
|---|---|
| T-0050 | **Epics and task areas.** Epics per module and page group, each listing its PRD documents, rule prefixes, Page IDs and delivery phase. Task folders under `tasks/` named after the module map (T-0023), replacing the provisional names in the original proposal |
| T-0051 | **Walking skeleton.** The first vertical slice through every layer: repository skeleton, CI, one module end to end (contract → API → persistence → one Storefront page → tests → preview deployment). Its tasks come first so every later task has a working pattern to follow |
| T-0052 | **Delivery Phase 1 tasks.** Every task file written from `tasks/_TEMPLATE.md`: goal, the exact documents to read, acceptance criteria with rule IDs, tests required, risk tags, dependencies. Protected-path tasks marked for plan approval (GRD-1) |
| T-0053 | **Review and approval.** Documentation review of the task set (coverage of P0 rules and pages for the phase, sizing, dependencies); acceptance under ADR-0005. Implementation (Phase 5) starts at kickoff (D-15) |

## Sizing rules

- One task changes one module (or one page group) and is reviewable in one sitting.
- A feature is a short chain: contract and API with tests → UI → follow-ups.
- Every task's acceptance criteria cite rule IDs or Page IDs; a task with neither is not ready.
