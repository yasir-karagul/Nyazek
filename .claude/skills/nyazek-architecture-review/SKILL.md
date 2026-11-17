---
name: nyazek-architecture-review
description: Checklist and procedure for an independent architecture review of a Nyazek task or design. Use when a task tagged `architecture` reaches `in-review`, when a new module, schema, API or event contract is introduced, or before an ADR is accepted.
---

# Nyazek architecture review

**Inputs:** the task ID and file, the change or design in scope, the relevant files in `docs/adr/`, `docs/prd/06-platform/` and any architecture documents the task links to.

**Procedure**

1. Identify which modules, data and contracts the change touches.
2. Work through the checklist against the approved architecture and ADRs.
3. Write the report in the format and location defined in `docs/reviews/README.md`.
4. Do not modify the work under review.

**Checklist**

- **Standing decisions:** modular monolith, API-first, client-agnostic; no PHP; Flutter for mobile.
- **Boundaries:** each module owns its data; no reaching into another module's internals or tables; dependencies point in the allowed direction; no cycles.
- **Contracts:** API and event contracts are explicit, versioned as the guide requires, and serve every client equally (web, mobile, third parties).
- **Data model:** schema changes are consistent with the domain; migrations are reversible or the risk is stated; financial records are never destructively changed.
- **Consistency with decisions:** conforms to accepted ADRs; a deviation or a new significant decision has its own ADR.
- **Operational fit:** failure modes, idempotency and load were considered where relevant to the change.
- **Proportion:** no component, service, datastore or abstraction beyond what the requirement needs.
- **Traceability:** the design maps to PRD requirements; nothing is built that the PRD does not ask for.
