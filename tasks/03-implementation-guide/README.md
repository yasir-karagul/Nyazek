# Phase 3: Implementation Guide

**Purpose:** write the *how*: the conventions and patterns Claude Code follows in every task, so that two tasks written weeks apart produce code that looks like one author wrote it. Output lives in `docs/implementation-guide/`, one topic per file, indexed by its `README.md`.

**Entry:** T-0031 done (architecture accepted, stack decided).
**Exit (T-0047):** documentation review without open critical or major findings; acceptance under ADR-0005.

**Rules for this phase**

- A guide file is short and concrete: the rule, a minimal example in the chosen stack, and the anti-pattern to avoid. It links PRD rules and architecture sections instead of restating them.
- Every convention that CI can enforce names the lint rule or check that enforces it (the check itself is built in implementation).
- Examples are illustrative snippets inside the guide, not application code.

## Deliverables

| Task | Folder | Files (one topic each) |
|---|---|---|
| T-0040 | `standards/` | Code style and naming · error model and error codes · logging, tracing and correlation · money, currency and rounding in code · dates, time zones and markets · internationalisation, copy keys and RTL · configuration and feature flags · Git, branches and commits |
| T-0041 | `backend/` | Module template and boundaries · persistence, schemas and migrations · transactions, outbox and jobs · idempotency · authorisation enforcement · state-machine implementation · ledger postings · provider adapters · audit trail writes · file uploads and media |
| T-0042 | `frontend/` | Application shells and routing · data fetching with the generated client · forms and validation · page templates (`TPL-*`) as components · shared components and tokens · RTL, accessibility and responsive rules · SEO and rendering modes · state, loading, empty and error handling |
| T-0043 | `testing/` | Test layout and naming with rule IDs · factories and seed data · property and model-based tests · contract tests · end-to-end tests by journey · visual and accessibility tests · provider mock servers |
| T-0044 | `security/` | Secure coding checklist · secrets handling · authorisation test generation · personal-data handling and masking · agent guardrails in practice |
| T-0045 | `deployment/` | Local environment · CI pipeline and gates · migrations in deployment · environments and promotion · rollback · observability and alerts |
| T-0046 | `README.md` | Index updated; "start here" reading order for a new task |
| T-0047 | – | Documentation review (`documentation-reviewer`) and acceptance under ADR-0005 |
