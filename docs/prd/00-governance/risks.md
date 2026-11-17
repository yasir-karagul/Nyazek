# Risks & Mitigations

**Authoritative for:** the product, delivery, financial, operational, technical and regulatory risk register.
**Related:** [open-decisions](open-decisions.md) · [release-plan](release-plan.md)

Likelihood and impact: H high · M medium · L low. The register is reviewed at every phase exit.

---

## 1. Delivery and team

| # | Risk | L | I | Mitigation | Residual |
|---|---|---|---|---|---|
| R-01 | P0 scope does not fit six months | H | H | Strict P0/P1/P2; phase exit reviews; reduction options listed in the release plan; D-15 | Owner may need to cut scope or extend |
| R-02 | Single AI agent writes code and tests: correlated mistakes go unnoticed | M | H | Acceptance criteria defined in the PRD first; property- and model-based tests; fresh-context review sessions; human review of every pull request; accountant validation; penetration test | Depends on human review capacity |
| R-03 | Human review becomes the bottleneck, or reviews become superficial | H | H | Small pull requests; protected-path rules; second human reviewer (D-27); checklists | Open until D-27 |
| R-04 | No 24/7 on-call capacity | H | H | D-27; managed services; alerting and runbooks; honest status communication | Out-of-hours response best-effort until staffed |
| R-05 | Owner decisions arrive late and block work | M | H | Decision register with "needed by"; defaults implemented behind configuration | – |
| R-06 | AI agent violates module boundaries or introduces unreviewed dependencies | M | M | CI boundary checks, database roles, dependency justification rule, ADRs | – |
| R-07 | Operations staff not hired or trained by the beta | M | H | Operating-readiness list; named owner per admin role as a launch gate | – |

## 2. Financial

| # | Risk | L | I | Mitigation | Residual |
|---|---|---|---|---|---|
| R-08 | Unit economics negative: logistics subsidy and COD failures exceed commission | H | H | Contribution-margin model before D-20 and D-21; COD confirmation; cost attribution; levers in the business model | Until the model is complete |
| R-09 | Funds-custody model unavailable or requires a licence | M | H | D-09 with counsel and PSP at kickoff; ledger independent of custody | Launch-blocking if unresolved |
| R-10 | Ledger or reconciliation errors | M | H | Double entry with database invariants; idempotent postings; daily reconciliation; accountant sign-off; synthetic-month validation gate | – |
| R-11 | COD cash leakage or late courier remittance | H | H | Per-waybill reconciliation; exposure caps; remittance SLAs; contract liability; no seller payout before reconciliation | Courier credit risk remains |
| R-12 | Payouts exceed cash available (platform-funded discounts, COD timing) | M | H | Funding position report; payout run blocked without funds | – |
| R-13 | Refund or payout fraud (destination change, refund to third-party account) | M | H | Destination verification and holds; dual control; risk signals on refund accounts | – |
| R-14 | Seller wallet deficits that cannot be recovered | M | M | Hold follows return window; deficit rules; Seller Agreement recovery terms | Bad-debt exposure |
| R-15 | Seller churn from slow payouts | M | M | Weekly cycle for good-standing sellers (D-03); clear statements | – |
| R-16 | KPI targets inconsistent, leading to wrong sizing or expectations | H | M | D-01 | – |

## 3. Operational and marketplace

| # | Risk | L | I | Mitigation | Residual |
|---|---|---|---|---|---|
| R-17 | High COD refusal and RTO rates | H | H | COD risk engine and confirmation; limits; incentives for prepaid | Market behaviour |
| R-18 | Couriers lack APIs, proof of delivery or reliable status | H | H | Tier C integration as P0; proof hierarchy; fallback couriers; performance tracking | Manual effort for Logistics |
| R-19 | Payment providers unstable or without refund and payout APIs | H | M | Adapter capability matrix; circuit breaker; manual queues; COD as fallback; aggregator option | – |
| R-20 | Too few sellers and listings at launch | M | H | Pre-launch seller acquisition; bulk import with barcode matching; 1P fills gaps | – |
| R-21 | Catalogue review bottleneck | M | H | Listing types; automated pre-checks; auto-approval for trusted brands; SLA alerts | Staffing |
| R-22 | Counterfeit and prohibited goods | M | H | KYC, brand gating, screening, reports, authenticity override | – |
| R-23 | Fraud: fake orders, self-dealing, review manipulation, coupon and referral abuse | M | M | Risk engine; cross-account signals; verified-purchase reviews; redemption limits | – |
| R-24 | Return abuse | M | M | Reason-based cost rules; proof requirements; abuse score | – |
| R-25 | SMS delivery failures or cost overrun (OTP, confirmations) | M | H | Two aggregators; delivery monitoring; rate limits and anti-pumping controls; SMS reserved for critical messages | – |
| R-26 | Address ambiguity causes failed deliveries | H | M | Structured address with mandatory landmark; courier call before delivery; map pin (P1); geo dataset (D-32) | – |
| R-27 | Shared-catalogue disputes between sellers | M | M | Catalog Manager owns canonical content; suggested edits; seller-owned listing type | – |

## 4. Technical

| # | Risk | L | I | Mitigation | Residual |
|---|---|---|---|---|---|
| R-28 | Overselling or stuck reservations | L | H | Atomic conditional updates in PostgreSQL; constraints; lazy expiry; concurrency tests | – |
| R-29 | Event loss or duplicate processing | L | H | Transactional outbox; idempotent consumers; dead-letter alerts | – |
| R-30 | Business logic leaks into web apps, blocking Flutter reuse | M | H | Static dashboards; lint ban on server actions; generated clients; readiness checklist | – |
| R-31 | Identity-separation bypass (aliases, races, disposable mail) | M | H | Canonicalisation; verified-only claims with unique index; KYC duplicate signals; cross-account risk signals | Custom-domain aliases undetectable |
| R-32 | Cloud region outage or regional conflict damage | M | H | No sole Middle East region; cross-region replication; third-location backups; drills; D-06 | – |
| R-33 | Edge provider outage or poor routing from Iraqi networks | M | H | Phase 1 latency measurements; documented DNS fallback; real-user monitoring | – |
| R-34 | Slow experience on Iraqi mobile networks | H | M | Edge presence in Iraq; image variants; performance budgets; real-user monitoring | – |
| R-35 | Search quality in Arabic and dialect is poor at launch | M | M | Normalisation; synonym management; query analytics; tuning in the beta | – |
| R-36 | Security breach or data leak (KYC documents, personal data) | M | H | Security baseline; field-level encryption; masking and access logging; penetration test | – |
| R-37 | Prompt injection or misuse of the AI agent's tools | M | M | Agent guardrails: no production access, untrusted-content rule, scoped credentials, sandboxed execution | – |
| R-38 | Dependency churn (framework major versions, tool licence changes) | M | L | Lockfiles; automated updates; ports and adapters around infrastructure components | – |
| R-39 | Operating load of the stack exceeds the team | M | M | Reduced, fully managed stack; ADR required for any new stateful component | – |
| R-40 | Design-system defects (no Arabic glyphs, failing contrast) reach production | H | M | D-19 before screens; accessibility checks in CI | – |
| R-41 | Design reference and implementation drift without an automated Figma link | M | M | Versioned reference folders; visual tests; human approval on previews; tokens in the repository as the single source | – |

## 5. Legal and regulatory

| # | Risk | L | I | Mitigation | Residual |
|---|---|---|---|---|---|
| R-42 | Licence or registration not obtained by launch | M | H | Workstream from kickoff; launch gate (D-14) | Launch date depends on it |
| R-43 | Regulatory change (tax on e-commerce, data-protection law, platform rules) | M | M | Tax abstraction; region-pinned, relocatable data; counsel monitoring | – |
| R-44 | Liability and policy terms unenforceable under consumer law | M | M | Counsel review (D-38) before publication | – |
| R-45 | Regional competitor entry | M | M | Speed to launch; local payments, logistics and language fit; seller tools | – |

## 6. Expansion (Syria and the Gulf)

| # | Risk | L | I | Mitigation | Residual |
|---|---|---|---|---|---|
| R-46 | Iraq-specific assumptions hard-coded now make a second market a rewrite | M | H | Market readiness as P0 (MKT-8, MKT-9); second-market test as a launch gate | – |
| R-47 | Building for future markets displaces Iraq launch work | M | H | Readiness is limited to the data model, contracts and configuration; nothing market-specific is built before D-40 | – |
| R-48 | Sanctions, banking and currency instability in Syria | M | H | Market-entry assessment with counsel; party and bank screening; price-step and currency rules per market; no entry without the gates in MKT-12 | Political and monetary risk remains |
| R-49 | Gulf markets are mature and contested by established regional and global marketplaces | H | M | Entry only with a differentiated proposition in the assessment; one market at a time | Market risk |
| R-50 | Tax, e-invoicing and data-protection duties in Gulf states are heavier than Iraq's and change often | H | M | Tax and e-invoicing ports; per-market legal pack; local advisers; deployment model left open (D-39) | – |
| R-51 | A data-localisation rule forces a separate deployment for a market | M | M | One codebase, deployment decided per market; region-pinned, relocatable data | Higher operating cost |
