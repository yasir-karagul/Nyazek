# Phase 2: Architecture

**Purpose:** turn the approved PRD into a technical design concrete enough that the implementation guide and the implementation tasks can be written without design decisions left open. The structure of the output follows ADR-0002 and the stack in ADR-0004: `docs/architecture/foundation.md`, one `docs/architecture/modules/<schema>.md` per module in [architecture](../../docs/prd/06-platform/architecture.md) §3, one `docs/architecture/clients/<app>.md` per client application, and decisions in `docs/adr/`.

**Entry (ADR-0002 §4):** met on 2026-11-17: T-0012 findings fixed, T-0014 decisions closed, and the owner accepted ADR-0004 (D-35 closed).
**Gates:** `foundation.md` is approved before any module specification. A module specification is written only after the PRD sections it implements are approved (T-0002 to T-0010, T-0017 `done`).
**Exit (T-0031):** architecture and security reviews have no open critical or major findings; ADRs, `foundation.md` and every specification accepted under ADR-0005 (protected-path content by the owner, point 3.1); every PRD module, rule group and Page ID is traceable to a module or client specification.

**Rules for this phase**

- A specification links the PRD rules it implements and never restates them (ADR-0002 §2). It records only what the PRD leaves open: schema, interfaces, contracts and technical decisions.
- Each significant choice is an ADR with options, trade-offs and a recommendation, decided under ADR-0005.
- No application code. Small spikes are allowed only to answer a question an ADR raises, kept outside `apps/` and deleted or archived after.
- ADR numbers 0001–0005 are taken (workflow, architecture layer, task closure, technology stack, decision authority); the next ADR is 0006.

## Deliverables

| Task | Deliverable | Location | Acceptance |
|---|---|---|---|
| T-0020 | **Technology stack ADR.** Re-verify the proposed stack in [technology-stack](../../docs/prd/06-platform/technology-stack.md) against current versions and support, the AI-agent workflow, Flutter and the no-PHP mandate; options and recommendation per layer | `docs/adr/0004-technology-stack.md` | Every PRD platform requirement maps to a component; owner decision recorded (closes D-35) |
| T-0021 | *Closed without work, confirmed by the owner on 2026-11-17.* **Market and hosting ADRs** (if T-0014 left them open): multi-market deployment and configuration resolution; hosting regions and the meaning of data residency | `docs/adr/0005-multi-market-model.md`, `docs/adr/0006-hosting-and-residency.md` | Options per [market-expansion](../../docs/prd/01-product/market-expansion.md) §3 and MKT-7; owner decision or recorded deferral |
| T-0032 | **Spikes.** RDS Proxy questions and Cloudflare R2 lock check from ADR-0004 (pinning, per-role pools, replica support, AWS Backup re-encryption, Worker requests through ALB mutual TLS, R2 compliance-mode lock, Cloudflare CNAME setup with Route 53 DNS; an end-to-end test of the CloudFront standby path (listener, security group, pinned certificate)). Needs owner-approved AWS and Cloudflare accounts | Archived notes linked from `foundation.md` | Each question answered; the answers feed T-0022, which closes OI-6 and OI-7 |
| T-0022 | **Foundation.** System context and containers, API and worker roles, datastores, trust boundaries, environments; repository and package structure; conventions shared by all modules for data (keys, money, market and currency columns, audit, retention class), API, events and outbox, jobs, errors | `docs/architecture/README.md`, `docs/architecture/foundation.md` | A new contributor could create the empty repository skeleton from it; every external party in the PRD appears with its integration type and trust boundary |
| T-0023 | **Module catalogue and build order.** Dependency graph of the modules in architecture §3, the shared-transaction exceptions (§3.2), the order in which specifications and code are built | `docs/architecture/foundation.md` (section) | No rule prefix without an owning module; graph acyclic; boundary rules testable |
| T-0024 | **Module specifications: identity and commerce core** — `identity`, `customers`, `sellers`, `catalog`, `inventory`, `checkout`, `orders` | `docs/architecture/modules/<schema>.md` | The eleven sections of ADR-0002 §3; every state machine, timer and page action of these modules covered; acceptance criteria with IDs |
| T-0025 | **Module specifications: finance** — `payments`, `ledger`, `wallet`, `commission`, `invoicing` | as above | Every posting rule (JE-n) mapped to the transition that posts it; ledger invariants mapped to database constraints or jobs |
| T-0026 | **Module specifications: operations and platform** — `logistics`, `returns`, `risk`, `notifications`, `media`, `backoffice`, `audit` | as above | As T-0024 |
| T-0027 | **Module specifications: discovery, growth and content** — `search`, `reviews`, `promotions`, `loyalty`, `ads`, `content`, `support`, `analytics`, `messaging` (P1) | as above | As T-0024 |
| T-0028 | **Security architecture and threat model.** Authentication and sessions per realm, authorisation enforcement, secrets, encryption, uploads, admin access, agent guardrails; STRIDE model of identity, checkout and payments, payouts, admin, uploads | `docs/architecture/foundation.md` (security section) | Every threat has a mitigation linked to a rule or a design element |
| T-0029 | **Integration architecture.** Ports and adapters for PSPs, couriers (API and file-based), SMS, email, push, storage; capability matrices; mock servers; sandbox strategy | `docs/architecture/foundation.md` (integrations section) | Each provider type has a port, a mock and a failure behaviour |
| T-0030 | **Client specifications** — storefront, seller dashboard, admin panel, mobile readiness: routing, data fetching, state, page-to-endpoint map from the page specifications | `docs/architecture/clients/<app>.md` | Every page action in `09-information-architecture` maps to an endpoint in a module specification |
| T-0031 | **Architecture and security review; sign-off under ADR-0005** | `docs/reviews/architecture/`, `docs/reviews/security/` | Exit criteria above met |

## Order

T-0020 (D-35 closed) → T-0032 spikes alongside T-0022 with T-0023, T-0028, T-0029 (all of `foundation.md`) → foundation accepted under ADR-0005 → T-0024, T-0025, T-0026, T-0027 as their PRD sections are approved → T-0030 → T-0031.
