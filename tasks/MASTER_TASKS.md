# Master Tasks

Source of truth for every task and its status. This file is an index: one row per task. Scope, acceptance criteria and links live in the task's own file, created under `tasks/<area>/` when the task needs more than one line.

- **Statuses:** `backlog` · `ready` · `in-progress` · `in-review` · `blocked` · `done`. Claude sets `done` only under the closure conditions of ADR-0003. Decisions are Claude's under ADR-0005; tasks whose work is reserved to the owner (ADR-0005 point 3) are closed only after the owner confirms the action in chat.
- **Risk tags** decide the reviewers: `code` · `security` · `architecture` · `docs` (see `CLAUDE.md`), plus the reviewers ADR-0005 point 2.4 always requires. Tags may be added, never removed.
- **IDs** are `T-NNNN`, never reused. A task created from a review finding names the finding ID in the Source column.
- **Next task:** the first `ready` row whose dependencies are all `done`, skipping work reserved to the owner (ADR-0005 point 3).

## Phase 0 — Workflow foundation

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0001 | Establish the workflow foundation (Git, `CLAUDE.md`, reviewers, document skeletons) | done | — | docs | `docs/adr/0001-development-workflow.md` |

## Phase 1 — PRD

### 1a. Completeness

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0011 | PRD v7.1 completeness review: gaps, contradictions and duplication resolved; expansion scope (Syria, Gulf) and market readiness; six new documents; sitemap v3; index updated | done | T-0001 | docs | `docs/prd/00-governance/review-findings.md` §12 |
| T-0016 | PRD v7.2: "Customer" replaces "buyer" everywhere; new section `09-information-architecture` (navigation, labels, components, flows, a specification for each of the 293 pages); sitemap moved into it | done | T-0011 | docs | `docs/prd/00-governance/review-findings.md` §13 |
| T-0012 | Independent documentation review of PRD v7.2 (fresh context, `documentation-reviewer`), including a sample check that page specifications match the rules they cite; report to `docs/reviews/documentation/`; valid findings fixed in PRD v7.3 and re-reviewed | done | T-0011, T-0016 | docs | `docs/reviews/documentation/2026-11-17-T-0012-prd-v7-2.md`; `docs/prd/00-governance/review-findings.md` §14 |

### 1b. Owner review and approval, section by section

A section is binding for implementation once its task is `done`. Findings from T-0012 that touch a section are resolved before that section is approved.

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0002 | Review and approve PRD `00-governance` | done | T-0011 | docs | `docs/prd/00-governance/` |
| T-0003 | Review and approve PRD `01-product` (includes user journeys and market expansion) | done | T-0011 | docs | `docs/prd/01-product/` |
| T-0004 | Review and approve PRD `02-commerce` | done | T-0011 | docs | `docs/prd/02-commerce/` |
| T-0005 | Review and approve PRD `03-sellers` (includes 1P operations) | done | T-0011 | docs | `docs/prd/03-sellers/` |
| T-0006 | Review and approve PRD `04-finance` | done | T-0011 | docs | `docs/prd/04-finance/` |
| T-0007 | Review and approve PRD `05-trust` (includes the Admin Panel) | done | T-0011 | docs | `docs/prd/05-trust/` |
| T-0008 | Review and approve PRD `06-platform` requirements (the stack itself is decided in Phase 2) | done | T-0011 | docs | `docs/prd/06-platform/` |
| T-0009 | Review and approve PRD `07-clients` | done | T-0011 | docs | `docs/prd/07-clients/` |
| T-0010 | Review and approve PRD `08-engineering` | done | T-0011 | docs | `docs/prd/08-engineering/` |
| T-0017 | Review and approve PRD `09-information-architecture` (includes sitemap v3 and decision D-46) | done | T-0016 | docs | `docs/prd/09-information-architecture/` |

### 1c. Owner decisions that shape the next phase

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0013 | Ratify or overrule the assumptions made in the v7.1, v7.2 and v7.3 reviews (D-46, D-47) | done | T-0011, T-0016, T-0012 | docs | `docs/prd/00-governance/review-findings.md` §12.1, §13.1, §14.1 |
| T-0014 | Close the decisions needed before architecture: D-39 (multi-market model), D-06 (hosting and residency), D-09 (funds custody), D-44 (item conditions); confirm D-41 | done | T-0011 | docs | `docs/prd/00-governance/open-decisions.md` |
| T-0015 | (Reserved to the owner, ADR-0005 point 3.) Start the long-lead external workstreams: legal entity and licence (D-14), counsel and accountant engagement (D-37, D-38, D-42), PSP, courier and SMS contacts (D-11, D-28, D-29); with counsel, the legal meaning of "Iraqi data residency" (follow-up of D-06, INF-8) and confirmation of the custody model in use (follow-up of D-09) | blocked | — | docs | `docs/prd/00-governance/release-plan.md` §5 |

### 1d. Parallel track: design

Design runs alongside Phases 2–4 so that P0 page designs exist when UI tasks start ([design-system-ui-workflow](../docs/prd/07-clients/design-system-ui-workflow.md) §6).

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0018 | Claude (ADR-0005), with a designer's input where available: decide D-19 (Arabic typeface, accessible orange, missing tokens, numerals) | ready | — | docs | `docs/prd/07-clients/design-system-ui-workflow.md` §3 |
| T-0019 | Claude: write Stitch design briefs per page group from the page specifications (template, content, states, both languages), as the fixed prompt prefix for the first design pass | backlog | T-0012, T-0018 | docs | `docs/prd/09-information-architecture/` |

### 1e. Follow-ups from the T-0012 review

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0060 | IA consistency pass on the minor findings deferred from T-0012 (template variants and components, priority and reachability mismatches, sitemap admin-role column against the RBAC matrix, `410` wording, seller-dashboard area list, unsupported page assertions) | done | T-0012 | docs | Report F-DOC-088 to F-DOC-096; detail and fixes in `docs/reviews/documentation/2026-11-17-T-0060-ia-detail*.md` (final re-review: approve, 0 findings); open questions moved to T-0061 |
| T-0061 | Decisions raised by T-0060 (18 questions listed in the report's Disposition section: vacation limits, performance overrides, engineer access to system health, admin-reset row in the dual-control table, low-stock threshold, home banner and card limits, currency-table lock, Risk on COD confirmations, Notifications row in the RBAC matrix, COD fee priority, unpublished-product response, delivery phones, seller phone-OTP screen, step-up scope, customer step-up factor, seller areas for KYC, help and referral, store slug, who edits settings) | ready | T-0060 | docs, security, architecture | `docs/reviews/documentation/2026-11-17-T-0060-ia-detail.md` (Disposition, 18 questions); decided by Claude under ADR-0005, except options that loosen access or security rules (questions 3, 14, 15, 18), which are reserved (ADR-0005 point 3.2) and go to the owner; F-DOC-088.2, .3, .5, .7, .10, .12, .13; F-DOC-089.4, .7; F-DOC-090.3; F-DOC-093.3, .4; F-DOC-094.1, .5, .6; F-DOC-095.5, .6, .7; F-DOC-141; F-DOC-143 |
| T-0062 | Align the PRD with ADR-0005: claude-workflow (§1, §2, §4 GRD-1 to GRD-9, §4.4, "proposed stack" wording in line 6 and GRD-7), open-decisions header and Owner column, document-control, PRD README §3, risks R-02 and R-03, security AGT-5 cross-reference | ready | — | docs, security | ADR-0005 "Relation to earlier rules"; F-SEC-003, F-DOC-153, F-DOC-160 |
| T-0063 | Propose technical enforcement of the ADR-0005 bounds: Claude Code permission settings for protected paths and reserved actions; CODEOWNERS and branch protection for when GitHub is used (GitHub parts need the owner) | backlog | T-0062 | security, docs | F-SEC-011 |

## Phase 2 — Architecture

Deliverables, order, gates and exit criteria: [`tasks/02-architecture/README.md`](02-architecture/README.md), structured per ADR-0002. The phase opened on 2026-11-17 when the owner accepted ADR-0004 (D-35 closed).

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0020 | Technology stack ADR `0004` (closes D-35) | done | T-0012, T-0014 | architecture, docs | `docs/adr/0004-technology-stack.md` (accepted by the owner 2026-11-17); reviews in `docs/reviews/architecture/` and `docs/reviews/documentation/` (2026-11-17-T-0020-*) |
| T-0021 | Multi-market model and hosting ADRs `0005`, `0006` (D-39, D-06), if T-0014 left them open | done | T-0014 | architecture, docs | Closed without work, confirmed by the owner on 2026-11-17: T-0014 closed D-39 and D-06. ADR numbers 0005 and 0006 named in its deliverable were not used; the next ADR is 0006 |
| T-0022 | `foundation.md`: system context, repository, shared conventions; includes capacity sizing (F-DOC-055) | ready | T-0020 | architecture, docs | `tasks/02-architecture/README.md`; F-DOC-055; cannot be `done` before T-0032 is `done`; closes ADR-0004 OI-5 to OI-7 and re-checks its secondary-source version facts |
| T-0023 | Module catalogue and build order (in `foundation.md`) | backlog | T-0022 | architecture, docs | `tasks/02-architecture/README.md` |
| T-0028 | Security architecture and threat model (in `foundation.md`) | backlog | T-0022 | architecture, security, docs | `tasks/02-architecture/README.md` |
| T-0029 | Integration architecture (in `foundation.md`), including webhook buffering during an origin outage (F-DOC-056) | backlog | T-0022 | architecture, docs | `tasks/02-architecture/README.md`; F-DOC-056 |
| T-0032 | Phase 2 spikes before `foundation.md` approval (blocked: needs owner-approved paid AWS and Cloudflare accounts, reserved by ADR-0005): RDS Proxy pinning, per-role pools and replica support; Cloudflare R2 lock immutability for the 7-year audit copy; AWS Backup re-encryption of RDS copies; Worker requests through ALB mutual TLS; Cloudflare CNAME setup with Route 53 DNS; an end-to-end test of the CloudFront standby path (listener, security group, pinned certificate). Starts only after the owner approves the AWS and Cloudflare accounts it needs | blocked | T-0020 | architecture, security, docs | ADR-0004 Gaps filled, Backups; F-ARCH-001, F-ARCH-003, F-ARCH-018, F-ARCH-019 |
| T-0024 | Module specifications: identity and commerce core | backlog | T-0023, T-0028, T-0029, T-0004, T-0005, T-0007 | architecture, docs | `tasks/02-architecture/README.md` |
| T-0025 | Module specifications: finance | backlog | T-0023, T-0028, T-0029, T-0006 | architecture, security, docs | `tasks/02-architecture/README.md` |
| T-0026 | Module specifications: operations and platform | backlog | T-0023, T-0028, T-0029, T-0004, T-0007 | architecture, docs | `tasks/02-architecture/README.md` |
| T-0027 | Module specifications: discovery, growth and content | backlog | T-0023, T-0004 | architecture, docs | `tasks/02-architecture/README.md` |
| T-0030 | Client specifications (storefront, seller, admin, mobile readiness) | backlog | T-0024 to T-0027, T-0009, T-0017 | architecture, docs | `tasks/02-architecture/README.md` |
| T-0031 | Architecture and security review; sign-off under ADR-0005 | backlog | T-0020 to T-0030, T-0032 | architecture, security, docs | `tasks/02-architecture/README.md` |

## Phase 3 — Implementation guide

Deliverables: [`tasks/03-implementation-guide/README.md`](03-implementation-guide/README.md).

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0040 | Guide: `standards/` | backlog | T-0031 | docs | `tasks/03-implementation-guide/README.md` |
| T-0041 | Guide: `backend/` | backlog | T-0040 | docs | `tasks/03-implementation-guide/README.md`; ADR-0004 OI-3 |
| T-0042 | Guide: `frontend/` | backlog | T-0040 | docs | `tasks/03-implementation-guide/README.md`; ADR-0004 OI-4 |
| T-0043 | Guide: `testing/` | backlog | T-0041, T-0042 | docs | `tasks/03-implementation-guide/README.md` |
| T-0044 | Guide: `security/` | backlog | T-0041 | docs, security | `tasks/03-implementation-guide/README.md`; ADR-0004 OI-2 |
| T-0045 | Guide: `deployment/` | backlog | T-0040 | docs | `tasks/03-implementation-guide/README.md`; ADR-0004 OI-1 |
| T-0046 | Guide index and reading order | backlog | T-0040 to T-0045 | docs | `tasks/03-implementation-guide/README.md` |
| T-0047 | Documentation review of the guide; acceptance under ADR-0005 | backlog | T-0046 | docs | `tasks/03-implementation-guide/README.md` |

## Phase 4 — Task breakdown

Deliverables: [`tasks/04-task-breakdown/README.md`](04-task-breakdown/README.md). Task files use [`tasks/_TEMPLATE.md`](_TEMPLATE.md).

| ID | Task | Status | Depends on | Risk | Source / file |
|---|---|---|---|---|---|
| T-0050 | Epics and task areas | backlog | T-0047 | docs | `tasks/04-task-breakdown/README.md` |
| T-0051 | Walking-skeleton tasks | backlog | T-0050 | docs | `tasks/04-task-breakdown/README.md` |
| T-0052 | Delivery Phase 1 (Foundation) task files | backlog | T-0051 | docs | `tasks/04-task-breakdown/README.md` |
| T-0053 | Review of the task set; acceptance under ADR-0005 | backlog | T-0052, T-0063 | docs | `tasks/04-task-breakdown/README.md` |

## Phase 5 — Implementation

Starts at kickoff (D-15) with the walking skeleton, then follows the delivery phases in [release-plan](../docs/prd/00-governance/release-plan.md). Implementation tasks are added here by Phase 4.
