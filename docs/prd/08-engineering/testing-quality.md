# Testing & Quality

**Authoritative for:** test strategy, required test types per area, coverage rules, test data, quality gates and launch test gates.
**Related:** [claude-workflow](claude-workflow.md) · [infrastructure-devops](../06-platform/infrastructure-devops.md) §5 · [reliability-sre](../06-platform/reliability-sre.md) · [security](../05-trust/security.md) §11

---

## 1. Principles

- TST-1 Tests are written with the code in the same pull request.
- TST-2 Because one AI agent writes both code and tests, tests alone are not independent evidence. Independence comes from: acceptance criteria written in this PRD before implementation, property-based and model-based tests that explore cases the author did not enumerate, human review, external validation (accountant, penetration test) and end-to-end tests derived from user stories.
- TST-3 Integration tests use real PostgreSQL (and OpenSearch where relevant) in containers, not mocks of the database.
- TST-4 External providers are replaced by contract-faithful mock servers in CI and by provider sandboxes in staging.
- TST-5 A flaky test is fixed or quarantined with a task in `tasks/MASTER_TASKS.md` within one working day; it is never left to be retried indefinitely.

## 2. Test types

| Type | Tooling | Scope |
|---|---|---|
| Unit | Vitest | Domain rules, calculators, mappers, validators |
| Property-based | fast-check | Money rounding and allocation, quote calculation, ledger postings and invariants, stock counters, points ledger, commission and refund proportionality |
| Model-based (state machines) | fast-check model runs or equivalent | Sub-order, payment intent, COD collection, return, dispute, seller state, checkout session |
| Integration | Vitest + Testcontainers | Repositories, migrations, module public interfaces, outbox and consumers, database constraints and role privileges |
| Contract | Generated from OpenAPI; `oasdiff` | Responses match schemas; no breaking changes on a live major version |
| Provider adapters | Mock servers + recorded fixtures; sandbox runs nightly | PSP, courier, SMS, email, push adapters, including forged, replayed and out-of-order webhooks |
| Authorisation | Generated suite | Every route: authentication, audience, permission, cross-tenant access |
| Component and visual | Storybook, Playwright | Components and pages in Arabic and English, RTL and LTR, three breakpoints |
| Accessibility | axe checks in component and end-to-end tests | WCAG 2.2 AA rules that can be automated |
| End-to-end | Playwright against preview and staging | The journeys and edge cases in [user-journeys](../01-product/user-journeys.md), which include: customer journey (search → product → cart → checkout COD and prepaid → tracking → return → refund), seller journey (onboarding → listing → order → ship → wallet), admin journeys (KYC, catalogue review, dispute, payout run) |
| Flutter | flutter_test, golden tests, integration_test | Widgets, golden screens in both languages, sign-in and deep-link flows |
| Load | k6 | Profiles in [reliability-sre](../06-platform/reliability-sre.md) CAP-4 |
| Resilience | Fault injection in staging | Database failover, cache loss, search loss, worker kill mid-saga, provider outage, webhook loss |
| Security | Static and dependency scans, DAST baseline, penetration test | [security](../05-trust/security.md) |
| Data integrity | Scheduled checks in staging and production | Ledger invariants, stock reconciliation, read-model drift |

## 3. Coverage rules

- Line and branch coverage of at least 80% per backend module, enforced in CI; 90% for `ledger`, `wallet`, `payments`, `commission`, `inventory`, `identity` and the Money library.
- Coverage is a floor, not the goal: every state transition and every posting rule has at least one explicit test, every `cfg:` value that changes behaviour has tests at its boundaries, and every acceptance criterion in this PRD maps to at least one automated test (traceable by rule ID in the test name or annotation).
- UI components: every component has stories for all states in both languages and is covered by visual tests.

## 4. Critical scenario catalogue (must be automated)

1. Last-unit race: concurrent checkouts and place-order calls.
2. Duplicate place-order, payment webhook, refund request and payout instruction.
3. Payment success after expiry, with and without stock.
4. Multi-seller order with one seller rejecting, one SLA timeout, one delivered.
5. COD order: unconfirmed and cancelled; delivered, remitted short; refused at door.
6. Partial return of a discounted order with platform coupon and loyalty redemption, before and after escrow release.
7. Chargeback after payout leading to a wallet deficit and recovery.
8. Email claim race between a customer and a seller registration; all canonicalisation variants.
9. Cross-realm and cross-tenant access attempts on every resource.
10. Out-of-order and replayed courier events.
11. Regional restore followed by reconciliation.
12. Arabic search normalisation set (alef, ya, ta-marbuta, diacritics, digits, transliteration).
13. Buy Box worked examples including hysteresis.
14. Invoice numbering under concurrency.
15. Erasure request with retained financial records.
16. A second test market with a two-decimal and a three-decimal currency, another time zone and a non-zero tax rate: quote, order, ledger and document suites pass unchanged (MKT-8).
17. Every entry of the edge-case register ([user-journeys](../01-product/user-journeys.md) §4).

## 5. Test data

- Deterministic seed fixtures cover both languages, all seller types, all categories and their mandatory attributes, the 19 governorates, and orders in every state.
- Factories generate valid domain objects; tests never depend on shared mutable data.
- No production data in any test environment ([security](../05-trust/security.md) SEC-22).
- A synthetic month of PSP settlement files, courier manifests and remittance statements, including deliberate mismatches, is maintained for reconciliation tests.

## 6. Quality gates

| Gate | When | Blocks |
|---|---|---|
| Pull-request pipeline ([infrastructure-devops](../06-platform/infrastructure-devops.md) §5.1) | Every pull request | Merge |
| Staging end-to-end and DAST baseline | Every release candidate | Production deploy |
| Phase exit review | End of each phase | Next phase scope ([release-plan](../00-governance/release-plan.md)) |

### 6.1 Launch test gates (cannot be waived)

- Ledger and reconciliation validation with the synthetic month: zero unexplained differences; accountant sign-off.
- Penetration test: critical and high findings closed and retested.
- Load test at the CAP-4 profile with SLOs met and invariants intact.
- Restore test and staged regional failover within recovery objectives.
- Full RTL and bilingual visual pass of all P0 pages; accessibility checks passed.
- Mobile-readiness checklist ([mobile-flutter](../07-clients/mobile-flutter.md) §5).
- End-to-end journeys green against provider sandboxes for every launch payment method and courier tier.
- Closed beta completed with defined exit criteria (order success, payment success, delivery success, defect counts).

## 7. Acceptance criteria

- CI fails when coverage drops below thresholds, when an acceptance-criterion test is missing for a changed rule, or when a route lacks an authorisation test.
- The critical scenario catalogue is fully automated before the closed beta.
