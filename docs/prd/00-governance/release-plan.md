# Release Plan

**Authoritative for:** phases, deliverables and exit criteria, launch gates, long-lead external dependencies, operating readiness, post-launch roadmap.
**Related:** [scope-priorities](../01-product/scope-priorities.md) · [open-decisions](open-decisions.md) · [risks](risks.md) · [testing-quality](../08-engineering/testing-quality.md) §6.1

---

## 1. Shape of the plan

The plan below is the **delivery** plan. It begins at kickoff, which follows the documentation phases of the approved workflow (PRD review, architecture, implementation guide: `docs/adr/0001-development-workflow.md`; progress in `docs/implementation-guide/IMPLEMENTATION_STATUS.md`). Stack names in the deliverables are the stack decided by ADR-0004 (D-35 closed).

Four phases over six months from kickoff (kickoff date: D-15). All P0 features and all launch gates must be complete before public launch. P1 features target launch and may ship within 30 days after it.

Work is delivered as vertical slices (contract → API → client → tests) by Claude under the workflow in [claude-workflow](../08-engineering/claude-workflow.md). Each phase ends with an exit review by the owner.

## 2. Phases

### Phase 1: Foundation (months 1–2)

| Stream | Deliverables |
|---|---|
| Decisions | D-01, D-04, D-06, D-07, D-08, D-09, D-11, D-12, D-14 (started), D-15, D-19, D-23, D-24, D-27, D-28, D-29, D-32, D-33, D-37, D-39, D-42, D-44 closed (D-35 is closed earlier, in the architecture phase) or explicitly deferred with the default in force |
| Environment | Monorepo, Dev Container and local stack, CI pipeline with all gates, preview deployments, `CLAUDE.md` and repository rules, protected paths |
| Infrastructure | Accounts and environments from code, edge configuration, region latency measurements from Iraqi networks, staging live, observability baseline, backups and first restore test |
| Architecture skeleton | NestJS module structure with per-module schemas and roles, boundary checks, outbox and job queue, event envelope, audit trail, configuration store and feature flags, error model, idempotency layer |
| Contracts | Zod schemas → OpenAPI → generated TypeScript and Dart clients; tokens and i18n generators |
| Identity | Identity claims, three realms, OTP, sessions and tokens, 2FA, origin isolation, account lifecycle |
| Ledger | Chart of accounts and posting rules validated by the accountant; journal, balances, invariants; Money library with property tests |
| Sellers | Registration, onboarding wizard, KYC queue and review, seller states, Seller Dashboard shell |
| Catalogue | Categories, attribute schemas, brands, products, variants, offers, listing types, media pipeline, admin catalogue queues |
| Admin | Admin shell, roles and permissions, dual-control framework, audit viewer |
| Design system | D-19 applied; token file; core components in Storybook in Arabic and English |
| Mobile readiness | Flutter spike app building in CI for Android and iOS with generated client, tokens and catalogues |
| External | PSP or aggregator, courier, SMS contracts in progress; legal entity and licence workstream; contribution-margin model started |

**Exit criteria:** a seller can register, pass KYC and create an offer on staging; boundary, authorisation and ledger invariant suites run in CI; the Flutter spike passes; the region is chosen.

### Phase 2: Core commerce (months 2–4)

| Stream | Deliverables |
|---|---|
| Decisions | D-02, D-03, D-10, D-20, D-21, D-22, D-26, D-31, D-36, D-43 closed |
| Discovery | Search index and pipeline, Arabic analysis, filters, sort, autocomplete; Buy Box; product, category and store pages; home page from CMS |
| Buying | Cart, quote engine, checkout session, five-step checkout, guest checkout, place-order saga, order and sub-order state machine, SLA timers, cancellation |
| Inventory | Reservation, allocation, movements, expiry sweep |
| Payments | PSP adapter framework, launch wallets (or aggregator), COD collections, webhooks, polling, refunds with manual queue |
| Risk | COD risk engine, COD confirmation, basic rule set, review queue |
| Logistics | Serviceability, shipping fees, courier adapters (Tier C first, then available APIs), labels, pickup, tracking, proof of delivery, RTO |
| Finance | Commission, escrow hold and release, wallet views, holds, payout runs with file fallback, statements, receipts, credit notes, commission invoices, reconciliation jobs and exception queues |
| Seller Dashboard | Home, orders, catalog with bulk import, wallet, notification centre, account security |
| Customer account | Orders, tracking, addresses, profile, security, favourites |
| Notifications | Inbox, email and SMS providers, transactional templates |
| Admin | Order and logistics queues, finance screens, COD remittance, platform settings |

**Exit criteria:** an end-to-end COD order and an end-to-end prepaid order complete on staging against provider sandboxes or mocks, with correct ledger entries, payout statement and reconciliation.

### Phase 3: Trust and growth (months 4–5)

| Stream | Deliverables |
|---|---|
| Decisions | D-05, D-13, D-25, D-30, D-38, D-45 closed |
| After-sales | Returns, reverse logistics, refunds, disputes, customer-abuse controls |
| Trust | Seller performance score, levels and consequences; reviews and ratings with pre-screen; risk signals across accounts; self-dealing detection |
| Seller Dashboard | Returns and disputes, performance, reviews, sales analytics, settings |
| Admin | Dispute, moderation, risk, privacy-request and 1P merchandising screens; analytics dashboards |
| Privacy and compliance | Consent records, cookie banner and consent-gated tags, data-subject requests, legal pages in CMS, disclosures |
| Support and content | Ticketing, static pages, templates |
| Analytics | Event consumers, read models, metric checks, finance reports |
| P1 work begins | Cards, loyalty, promotions, ads, messaging, Q&A, staff roles (in priority order agreed by the owner) |

**Exit criteria:** all P0 features complete on staging; critical scenario catalogue automated; closed-beta sellers onboarded.

### Phase 4: Launch preparation (months 5–6)

Performance tuning against SLOs · full bilingual and RTL visual pass · accessibility checks · penetration test and remediation · load test · restore test and staged failover · reconciliation validation with the synthetic month · runbooks and on-call set-up · operations training for every admin role · closed beta with real sellers, customers, couriers and payments · defect fixing · launch-gate review · public launch.

## 3. Scope warning (D-15)

The P0 scope is large: about 220 P0 pages and components in the [sitemap](../09-information-architecture/sitemap.md) §12, a double-entry ledger, three payment integrations plus COD, courier integrations, a full Seller Dashboard and an Admin Panel with 11 roles. Six months is achievable only if:

1. the Phase 1 decisions are closed in the first weeks;
2. external contracts (PSP, couriers, SMS, licence) do not slip;
3. P1 work is not allowed to displace P0 work;
4. human review capacity keeps pace with the agent's output, especially on protected paths.

If any of these fails, the owner chooses between extending the timeline and reducing P0. Candidates for reduction, in recommended order: launch with COD plus one wallet (or the aggregator) and add the others as fast-follows; launch couriers on Tier C only; launch with a reduced set of categories (deferring regulated categories with licence handling); defer 1P to a fast-follow. These are options for the owner, not decisions.

## 4. Launch gates (cannot be waived)

1. Ledger and reconciliation validation; accountant sign-off (D-37).
2. Penetration-test critical and high findings closed.
3. Load test at the defined profile with invariants intact.
4. Restore test and staged regional failover within recovery objectives.
5. Legal entity, commercial registration and e-commerce licence in place; counsel sign-off of legal documents, custody model and invoice form (D-09, D-14, D-26, D-38); disclosures live.
6. Mobile-readiness checklist signed off.
7. Contracts live with at least one PSP or aggregator, two couriers and two SMS routes.
8. Every admin role has a named, trained person; on-call arrangement decided (D-27).
9. Closed beta exit criteria met.
10. Full RTL, bilingual and accessibility checks passed for all P0 pages.
11. Market readiness verified: the second-market test passes and no market literal exists in business logic ([market-expansion](../01-product/market-expansion.md) §8).

## 5. Long-lead external dependencies

| Dependency | Why it is long-lead | Start |
|---|---|---|
| Legal entity, registration, licences | Government processes | Kickoff |
| PSP or aggregator onboarding and sandbox access | Commercial and compliance onboarding per provider | Kickoff |
| Courier contracts, zone lists, API or file specifications | Negotiation of SLA, COD remittance and liability | Kickoff |
| SMS sender ID and template registration | Carrier approval | Phase 1 |
| Accountant and counsel engagement | Needed for Phase 1 and 2 decisions | Kickoff |
| Domain, DNS, email authentication, edge account | Reputation warm-up for sending domains | Phase 1 |
| Apple and Google developer organisation accounts | Verification of the legal entity | After D-14 |
| Seller acquisition and catalogue seeding | 200 sellers and 50,000 offers do not appear at launch by themselves | Phase 2 |
| Penetration-test booking | Vendor lead time | Phase 3 |

## 6. Operating readiness

The platform assumes people perform these functions from the closed beta onward: KYC review (24-hour target), catalogue review (24-hour target), support (24- and 12-hour first response), review moderation (48-hour), dispute decisions (72-hour), finance operations (refund queue, payout runs, reconciliation exceptions, funding position), logistics operations (exceptions, COD remittance, courier files), risk review (12-hour), content management, 1P merchandising, and on-call engineering. Staffing levels are part of D-27.

## 7. Post-launch roadmap

| Order | Item |
|---|---|
| 1 | Fast-follow of remaining P1 features (within 30 days) |
| 2 | Flutter customer app (M1), then seller companion app (M2) |
| 3 | Weekly payouts for all eligible sellers, if not already live |
| 4 | Kurdish interface and Kurdistan Region operations (after D-13) |
| 5 | 1P purchase orders and warehouse management |
| 6 | Recommendations; semantic search; machine-learned risk models |
| 7 | Same-day delivery in Baghdad; subscriptions |
| 8 | Expansion to Syria and the Gulf, one market at a time, each through the entry gates in [market-expansion](../01-product/market-expansion.md) §6 (D-40) |
| 9 | Service extraction where load or organisation requires it |
