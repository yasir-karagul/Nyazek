# T-NNNN: <imperative title>

| Field | Value |
|---|---|
| Status | Mirrors `MASTER_TASKS.md` (the index is the source of truth) |
| Phase / epic | <phase> / <epic ID> |
| Risk tags | `code` · `security` · `architecture` · `docs` (decide the reviewers; see `CLAUDE.md`) |
| Depends on | T-…, decisions D-… that must be closed |
| Page IDs | `SF-…`, `SL-…`, `AD-…` (UI tasks only) |

## Goal

One or two sentences: what exists when this task is done, and why.

## Read before starting

Only these; nothing else from the PRD or the guide.

- PRD: `docs/prd/<file>.md` §… (rule IDs …)
- Page specifications: `docs/prd/09-information-architecture/<file>.md` (Page IDs …)
- Architecture: `docs/architecture/<file>.md` §…
- Guide: `docs/implementation-guide/<folder>/<file>.md`
- ADRs: `docs/adr/NNNN-….md`
- Design reference: `docs/design/<PAGE-ID>/` (UI tasks)

## Scope

- In: …
- Out: … (and which task covers it)

## Acceptance criteria

Each is testable and names the rule ID it proves.

1. Given … when … then … (RULE-ID)
2. …

## Tests required

- Unit / property / model / integration / contract / end-to-end / visual: what each must cover.
- Rule IDs that must appear in test names.

## Plan (written by Claude before coding; the owner approves it for protected paths, ADR-0005 point 3.1)

Approach, files and modules touched, contract and schema changes, migrations, risks.

## Definition of done

The project definition of done (`docs/prd/08-engineering/claude-workflow.md` §7) plus:

- [ ] Every acceptance criterion has a passing test
- [ ] Required reviews run and saved under `docs/reviews/`; valid findings added to `MASTER_TASKS.md`
- [ ] PRD, architecture or guide updated if behaviour or structure changed
- [ ] Owner approval recorded (protected paths and reserved items only, ADR-0005 point 3)

## Notes and assumptions

Decisions made under ADR-0005 point 2, each with its record.
