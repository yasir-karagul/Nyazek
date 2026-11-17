---
name: nyazek-code-review
description: Checklist and procedure for an independent code review of a Nyazek task. Use when a task tagged `code` reaches `in-review`, or when the owner asks for a code review of specific changes.
---

# Nyazek code review

**Inputs:** the task ID, its row in `tasks/MASTER_TASKS.md`, its task file, and the diff or files in scope. Read the guide files and PRD sections the task links to; nothing more.

**Procedure**

1. Establish scope from the task and the diff. Review what changed and what it directly affects.
2. Work through the checklist. Verify by reading the code and running the project's existing checks; do not assume.
3. Write the report in the format and location defined in `docs/reviews/README.md`.
4. Do not modify the code under review.

**Checklist**

- **Correctness:** meets every acceptance criterion; handles error, empty and boundary cases; no behaviour the PRD does not ask for.
- **Tests:** new behaviour is tested; tests assert outcomes, not implementation; no test weakened, skipped or deleted to pass.
- **Standards:** follows the linked implementation-guide files; naming and structure match the surrounding code.
- **Simplicity:** no dead code, duplication, speculative abstraction or unrequested dependency.
- **Data handling:** money, dates, time zones and Arabic/English text handled as the guide and PRD specify; no silent rounding or truncation.
- **Failure behaviour:** errors are surfaced, not swallowed; operations that can be retried are safe to retry.
- **Scope:** the change stays within the task; unrelated edits are reported.

Security and architecture depth belong to their own reviews. If you notice such an issue, record it as a `note` naming the review that should run.
