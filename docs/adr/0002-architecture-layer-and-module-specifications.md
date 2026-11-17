# ADR-0002: Architecture layer and module specifications

- **Status:** Accepted
- **Date:** 2026-11-16
- **Decided by:** Owner
- **Supplements:** ADR-0001 (adds to decisions 4 and 6; changes nothing else in it)

## Context

ADR-0001 sets the lifecycle PRD → Architecture → Implementation Guide → MASTER_TASKS → implementation, but it does not say what the Architecture phase produces. The implementation guide is organised by technical topic (`standards/`, `backend/`, `frontend/`, `testing/`, `security/`, `deployment/`), so it has no place for the facts that belong to one module: its tables, its public interface, its API endpoints, its events and its acceptance criteria.

The PRD already defines required behaviour, state machines and the content of every page. It also names a proposed stack that stays unconfirmed until the architecture phase (D-35). Technical detail therefore cannot live in the PRD, because requirements must not depend on a stack that is not final. It cannot live in the guide either, because a guide file says how something is done everywhere, not what one module is.

Without a defined architecture layer, each task would decide module-level technical details on its own, and those decisions would conflict across modules.

## Decision

1. **Architecture documents.** The Architecture phase produces documents in `docs/architecture/`, indexed by its `README.md`:
   - `foundation.md`: the confirmed stack (D-35), repository and package structure, and the data, API, event and error conventions shared by all modules.
   - `modules/<schema>.md`: one module specification per module listed in `docs/prd/06-platform/architecture.md` §3, named after the module's schema.
   - `clients/<app>.md`: one technical specification per client application (storefront, seller dashboard, admin panel, mobile).
   - Decisions and their reasons go to `docs/adr/` as usual.

2. **Authority.**
   - The PRD says what must happen and why. A module specification says what the module is technically. A guide file says how it is done everywhere. An ADR records the decision and the reason, and overrides on conflict (as in ADR-0001).
   - A module specification links to the PRD sections it implements and never restates them. It records only what the PRD leaves open: schema, interfaces, contracts and technical decisions.
   - A guide file contains no module-specific facts. A module specification contains no cross-cutting how-to.

3. **Module specification content.** Every module specification has these sections, in this order:
   1. Purpose and linked PRD sections
   2. Tables and schema
   3. Public service interface
   4. API endpoints
   5. Events produced and consumed
   6. State machines (reference the PRD; add technical details only)
   7. Permissions and configuration keys (reference the configuration register)
   8. Errors and edge cases
   9. Acceptance criteria, each with an ID that is unique within the specification and cited by its tests
   10. Dependencies and build order
   11. Open questions

4. **Gates.**
   - The phase opens only when the owner opens it, after the decisions needed before architecture are closed (T-0014: D-39, D-06, D-09, D-44) and the stack is decided (D-35).
   - `foundation.md` is approved before any module specification.
   - A module specification is written only after the PRD sections it implements are approved (their review tasks are `done`).
   - The owner approves `foundation.md` and each specification. A specification is binding for tasks only once its review task is `done`, the same rule as for PRD sections.

5. **Reviews.** Architecture documents carry the risk tags `architecture` and `docs`. Reports go to `docs/reviews/architecture/` and `docs/reviews/documentation/`. Valid findings become tasks, as ADR-0001 decision 5 defines.

6. **Tasks.** Each implementation task links to one module or client specification, the guide topics it needs, and the PRD sections it implements. Claude reads only those.

7. **Change control.** If implementation shows that a specification or the PRD is wrong, the task becomes `blocked`. The owner decides, the document is changed and reviewed, and only then does the code change. Code never moves ahead of the documents.

8. **Repository.** `docs/architecture/` and its subfolders are lowercase and are created when they first hold content (ADR-0001 decision 6). The architecture documents become a document type with one job (ADR-0001 decision 4).

## Alternatives considered

- **A separate functional specification layer.** Rejected: the PRD already defines behaviour, state machines and every page, so a second layer would duplicate it and drift.
- **Module facts inside the implementation guide.** Rejected: it mixes module-specific facts with cross-cutting practice, and a task would have to search several topic files for one module's contract.
- **Technical detail inside the PRD.** Rejected: the PRD's technologies are proposed, and its requirements must not depend on them.

## Consequences

- `CLAUDE.md` gets a row in its "Where things live" table pointing to `docs/architecture/`, added when the first document exists.
- `docs/architecture/README.md` is created with the first document and lists every file, as the guide README does for guide files.
- The `architecture-reviewer` and `documentation-reviewer` skills are extended to check that module specifications link to the PRD instead of restating it, and that every acceptance criterion has an ID.
- `IMPLEMENTATION_STATUS.md` records Phase 2 progress per module once the phase opens.
- Phase 2 and Phase 3 tasks are added to `tasks/MASTER_TASKS.md` only after the owner opens those phases.
- This ADR does not choose any technology. The stack stays proposed until D-35 is closed.
- `docs/prd/08-engineering/claude-workflow.md` is aligned with this ADR during its PRD review (T-0010), as for ADR-0001.
