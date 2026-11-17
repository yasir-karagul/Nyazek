# ADR-0003: Task closure by Claude

- **Status:** Accepted
- **Date:** 2026-11-16
- **Decided by:** Owner
- **Amends:** ADR-0001 decision 3 (only the owner sets `done`) and the matching rules in `CLAUDE.md` (session protocol step 8, rule "Owner decides"). The rest of ADR-0001 stays in force.

## Context

ADR-0001 says only the owner moves a task to `done`. In practice this means the owner edits task files by hand after every task, which adds work and slows the loop. The owner wants Claude to maintain all task statuses, including `done`, and to stay out of the file editing.

Claude writes the work, and the four reviewers are fresh-context Claude subagents. Closure by Claude is therefore only as strong as the closure conditions and the review evidence. This ADR defines both.

## Decision

1. **Claude closes tasks.** Claude sets a task to `done` itself when all of these hold:
   - Every acceptance criterion is met and has been checked one by one.
   - Tests and checks pass. None was weakened, skipped or deleted to make the change pass.
   - Every reviewer required by the task's risk tags has run on the final version and passed.
   - Every valid finding is either fixed and re-reviewed, or tracked as its own task that names the finding ID.
   - Affected documents are updated, with nothing duplicated.
   - Closing evidence is written in the task file: the criteria checklist, links to the review reports, and the commit.

2. **Owner-decision tasks.** A task whose content is an owner decision, or an action outside the repository, is closed by Claude only after the owner states the decision or confirms the action in chat. This covers PRD section approvals, ratifying assumptions, closing open decisions (D-xx) and the external workstreams. Claude records the decision, then sets `done`. Claude never takes these decisions itself.

3. **When closure is not possible.** If a reviewer cannot run, a finding is disputed, or a criterion cannot be met, the task becomes `blocked` and Claude reports why. Claude never closes it.

4. **Other statuses.** Claude maintains all statuses. When a task becomes `done`, Claude sets each dependent task from `backlog` to `ready` once all its dependencies are `done`. The owner still starts every task ("next task" or a task ID); Claude never self-starts, as ADR-0001 decision 3 requires.

5. **Reopening.** The owner can reopen any task at any time. A reopened task returns to `in-progress`, and the reason is recorded in its task file.

6. **Unchanged.** Local only (no push or GitHub change without the owner's approval for that action), no new dependency, tool, service or datastore without owner approval, no invented rules (stop and ask if a document is silent or contradicts itself), and no weakening of tests, lint rules or checks. `IMPLEMENTATION_STATUS.md` is updated by Claude when the high-level picture changes.

## Consequences

- `CLAUDE.md` is updated: session protocol step 8 and the "Owner decides" rule describe closure by Claude, with the owner-decision exception.
- The `MASTER_TASKS.md` header line "Only the owner sets `done`" is replaced by the closure conditions above.
- ADR-0001 is not edited. This ADR amends it, and ADR-0001 gains no new text except an optional one-line pointer.
- The independent human check is now the owner's decisions on owner-decision tasks, plus the owner's right to reopen any task. The owner should read the review reports for high-risk tasks (security, payments, ledger, wallet), because Claude's closing evidence points to them.
- The rows T-0002 to T-0010 currently show `ready` while their dependency T-0011 is not `done`. Under decision 4, Claude corrects such rows to `backlog` until their dependencies are `done`.
