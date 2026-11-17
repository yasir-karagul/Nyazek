# Document Control

**Authoritative for:** version, status, documentation conventions, authority rules between documents, the v6-to-v7 traceability map, and required sitemap alignment.

---

## 1. Version

| | |
|---|---|
| Product | Nyazek (نيازك) Marketplace |
| Document set | Product Requirements Document v7.3 (Markdown), in the repository under `docs/prd/` |
| Supersedes | Nyazek PRD v6.0 (DOCX, October 2026) |
| Date | November 2026 |
| Status | Approved by the owner, section by section, on 17 November 2026 (T-0002 to T-0010, T-0017 in `tasks/MASTER_TASKS.md`). Changes after approval follow the change control in ADR-0002 §7 |
| Market | Iraq at launch (IQD, Arabic and English); planned expansion to Syria and the Gulf ([market-expansion](../01-product/market-expansion.md)) |
| Information architecture | [09-information-architecture](../09-information-architecture/README.md): sitemap v3 and the specification of every page |
| Classification | Confidential |

## 2. What v7 is

v7 is the result of an independent, end-to-end review of v6 from first principles ([review-findings](review-findings.md)), restructured into maintainable Markdown documents. It:

- applies the owner mandates: Flutter for mobile, Claude as the sole AI engineering agent, the Stitch → Figma → manual refinement → Claude design workflow without any Figma MCP integration, explicit authorisation of computer use, prohibition of PHP;
- resolves contradictions and corrects unsafe or infeasible requirements, giving the reason each time;
- makes ambiguous behaviour precise through rules, state machines, posting tables and acceptance criteria;
- re-evaluates the technology stack ([technology-stack](../06-platform/technology-stack.md));
- preserves every valid v6 requirement (traceability in §5);
- registers every point that needs the owner, counsel or the accountant ([open-decisions](open-decisions.md)).

## 3. Conventions

| Convention | Meaning |
|---|---|
| **Authoritative for** (top of each document) | The topics for which that document is the single source. Other documents link to it and do not restate the rule |
| Rule IDs (for example `ORD-5`, `PAY-9`, `ID-1`) | Stable identifiers for rules; used in tasks, tests and reviews. IDs are never reused |
| `JC-n`, `JS-n`, `JA-n`, `EC-n` | Customer, seller and staff journeys and edge cases in [user-journeys](../01-product/user-journeys.md) |
| Page IDs (for example `SF-PDP`) | Stable page identifiers in the [sitemap](../09-information-architecture/sitemap.md) |
| `IA-n`, `NAV-n`, `FL-n`, `TPL-…` | Information-architecture rules, navigation rules, flows and page templates in [09-information-architecture](../09-information-architecture/README.md) |
| Customer | The official term for the person who shops; "buyer" is retired. Identifiers follow it: realm `CUSTOMER`, module `customers`, rule prefix `CUS-`, journeys `JC-n` |
| `cfg:<key>` (default …) | A platform configuration value. The first, authoritative mention gives the proposed default; all keys are listed in the [configuration-register](configuration-register.md) |
| D-nn | An entry in the [open-decisions](open-decisions.md) register |
| F-nn | A finding in [review-findings](review-findings.md) |
| R-nn | A risk in [risks](risks.md) |
| P0 / P1 / P2 / Future | Priorities as defined in [scope-priorities](../01-product/scope-priorities.md) §1 |
| "v6 said …" notes | Short explanations kept where a v6 rule was changed, so the reason is not lost |
| State names | Upper snake case in code font; defined once in the owning document's state machine |

### 3.1 Authority and conflict rules

1. If two documents disagree, the one that lists the topic under **Authoritative for** wins, and the other is corrected in the same change.
2. The PRD wins over the sitemap, designs and code. A design or implementation that differs from the PRD is either corrected or the PRD is changed first by a reviewed pull request.
3. Proposed defaults for open decisions are implemented as configuration and remain "proposed" until the decision is closed.
4. Statements about law, tax and accounting are assumptions until confirmed by counsel or the accountant.

### 3.2 Change process

- The documents live in the repository under `docs/prd/` and change only with the owner's approval. The development workflow (`docs/adr/0001-development-workflow.md`) governs how: changes are tasks in `tasks/MASTER_TASKS.md`, are checked by the documentation review, and stay local until the owner approves a push.
- A PRD section is binding for implementation once its review task is `done`. Until then it is a complete draft.
- Every change that alters behaviour updates: the authoritative document, any cross-references, the configuration register if a `cfg:` value changed, the decision log if a decision closed, and the version table below.
- `_tools/check_docs.py` (links, configuration keys, decisions, rule IDs, retired terms), `_tools/gen_config_register.py` (rebuilds the configuration register) and `_tools/count_pages.py` (sitemap counts) are run on every documentation change, and in CI once it exists.

| Version | Date | Summary |
|---|---|---|
| 7.0 | November 2026 | Independent review of v6; restructure into Markdown; mandates applied; stack revised |
| 7.1 | 15 November 2026 | Completeness review: expansion scope (Syria and the Gulf) and market readiness; six new documents (market-expansion, user-journeys, customer-account, first-party-operations, admin-panel, sitemap v3); gaps, contradictions and broken references fixed ([review-findings](review-findings.md) §12); stack marked as proposed; workflow aligned with ADR-0001 |
| 7.2 | 15 November 2026 | "Customer" adopted as the official term in place of "buyer" in every document, identifier, tag, route and rule prefix; new section `09-information-architecture` (IA model, navigation, taxonomy and labels, shared components, flows, a specification for each of the 293 pages); sitemap moved into it ([review-findings](review-findings.md) §13) |
| 7.3 | 17 November 2026 | Independent review of v7.2 (T-0012, report in `docs/reviews/documentation/`): order payment window, stock and money effects per state, partial releases and line quantities, return–dispute linkage, seller return policy, suspended-seller orders, seller state transitions, performance mapping, chargeback, payout, refund and COD-collection machines, new ledger accounts and postings, shared-transaction mechanism, RBAC and dual-control alignment, workflow alignment with ADR-0001 and ADR-0002, IA pages and labels updated; defaults collected under D-47 ([review-findings](review-findings.md) §14) |

## 4. Reading order

1. [README](../README.md) for the map.
2. [overview-vision-kpis](../01-product/overview-vision-kpis.md), [scope-priorities](../01-product/scope-priorities.md), [market-expansion](../01-product/market-expansion.md), [user-journeys](../01-product/user-journeys.md).
3. [open-decisions](open-decisions.md), because several affect everything else.
4. [architecture](../06-platform/architecture.md) and [technology-stack](../06-platform/technology-stack.md).
5. Domain documents as needed.

## 5. Traceability: v6 section → v7 document

| v6 section | v7 location |
|---|---|
| Document control and revision summary | This document; [review-findings](review-findings.md) |
| 1 Executive Summary; 2 Problem Statement; 3 Vision & Goals; 7 Competitive Differentiation | [overview-vision-kpis](../01-product/overview-vision-kpis.md) |
| 4 Target Users & Personas | [users-personas](../01-product/users-personas.md) |
| 5 Unit Economics & Financial Model | [business-model](../01-product/business-model.md) |
| 6 Financial Reconciliation & Ledger (6.1 escrow, 6.4 COD) | [ledger-reconciliation](../04-finance/ledger-reconciliation.md); custody and COD in [payments](../04-finance/payments.md) §2, §7 |
| 8.1 Platform & Language | [web-apps](../07-clients/web-apps.md) §3; [architecture](../06-platform/architecture.md) |
| 8.2 Categories; 8.3 Shared Catalog; 8.5 Image Standards; 8.6 Prohibited Products | [catalog-listings](../02-commerce/catalog-listings.md) |
| 8.4 Search & Discovery | [search-buy-box](../02-commerce/search-buy-box.md) §1 |
| 8.7 Customer-Facing Features | [web-apps](../07-clients/web-apps.md) §4.1; addresses in [checkout-orders](../02-commerce/checkout-orders.md) §1; reviews in [reviews-qa](../02-commerce/reviews-qa.md) |
| 8.8 Authentication & Accounts | [identity-access](../05-trust/identity-access.md) |
| 8.9 Payment Methods | [payments](../04-finance/payments.md) |
| 8.10 COD Risk Engine | [fraud-risk](../05-trust/fraud-risk.md) §4 |
| 8.11 Free Delivery & Shipping | [logistics](../02-commerce/logistics.md) §3–4; [checkout-orders](../02-commerce/checkout-orders.md) §4 |
| 8.12 Notification Events | [notifications-messaging](../02-commerce/notifications-messaging.md) |
| 8.13 Seasonal Campaigns | [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| 8.14 Seller Portal Features | [seller-dashboard](../03-sellers/seller-dashboard.md) |
| 8.15 Seller Payout Methods | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §6 |
| 8.16 Seller Referral Program | [loyalty](../02-commerce/loyalty.md) §8 |
| 8.17 Customer Support; 8.18 Static & Legal Pages; 8.19 Third-Party Integrations | [support-cms](../02-commerce/support-cms.md); adapters in [technology-stack](../06-platform/technology-stack.md) |
| 9 Seller KYC & Onboarding | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) |
| 10 Pricing Strategy Governance | [pricing-promotions](../02-commerce/pricing-promotions.md) §1 |
| 11 Buy Box & Search Ranking | [search-buy-box](../02-commerce/search-buy-box.md) |
| 12 Seller Performance System (12.4 order SLA) | [seller-performance](../03-sellers/seller-performance.md); SLA in [checkout-orders](../02-commerce/checkout-orders.md) §7 |
| 13 Multi-Seller Order Architecture | [checkout-orders](../02-commerce/checkout-orders.md) |
| 14 Inventory Reservation Logic | [inventory](../02-commerce/inventory.md) |
| 15 Courier Integration & Logistics | [logistics](../02-commerce/logistics.md) |
| 16 Commission Model | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §1 |
| 17 Tax Model | [tax-invoicing](../04-finance/tax-invoicing.md) |
| 18.1 Fraud scoring | [fraud-risk](../05-trust/fraud-risk.md) |
| 18.2 Dispute Resolution | [returns-disputes](../02-commerce/returns-disputes.md) §6 |
| 18.3 Trust Mechanisms; 18.4 Two-Way Rating | [returns-disputes](../02-commerce/returns-disputes.md) §1; [reviews-qa](../02-commerce/reviews-qa.md) |
| 18.5 Platform Security Baseline | [security](../05-trust/security.md) |
| 19 Seller Wallet | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §2–5 |
| 20 Returns & Refunds | [returns-disputes](../02-commerce/returns-disputes.md) |
| 21 Loyalty Program | [loyalty](../02-commerce/loyalty.md) |
| 22 Sponsored Ads | [advertising](../02-commerce/advertising.md) |
| 23 Data Governance & Audit Logs | [privacy-audit](../05-trust/privacy-audit.md) |
| 24 Data Architecture & Reporting | [data-analytics](../06-platform/data-analytics.md) |
| 25 Legal Jurisdiction; 36 Compliance | [compliance-legal](../05-trust/compliance-legal.md) |
| 26 Admin Governance | [admin-governance](../05-trust/admin-governance.md) |
| 27 Business Continuity & DR; 28 Observability & SRE; 29 Capacity; 30 NFRs | [reliability-sre](../06-platform/reliability-sre.md); hosting in [infrastructure-devops](../06-platform/infrastructure-devops.md) |
| 31.1–31.3 Architecture, modules, events | [architecture](../06-platform/architecture.md) |
| 31.4 Tech Stack | [technology-stack](../06-platform/technology-stack.md) |
| 31.5 AI-Agent Engineering Workflow | [claude-workflow](../08-engineering/claude-workflow.md) |
| 32 Identity, Accounts & Access Separation | [identity-access](../05-trust/identity-access.md) |
| 33 Seller Dashboard (33.5 1P store) | [seller-dashboard](../03-sellers/seller-dashboard.md); 1P in [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) §8 |
| 34 Cross-Platform Architecture & Developer Environment | [mobile-flutter](../07-clients/mobile-flutter.md); [api-standards](../06-platform/api-standards.md); [claude-workflow](../08-engineering/claude-workflow.md) §5–6 |
| 35 Design System & UI Delivery Workflow | [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) |
| 37 Release Plan | [release-plan](release-plan.md) |
| 38 Risks | [risks](risks.md) |
| 39 Out of Scope | [scope-priorities](../01-product/scope-priorities.md) §4 |
| 40 Glossary | [glossary](glossary.md) |
| Appendix A Open Decisions | [open-decisions](open-decisions.md) |

New documents with no v6 counterpart: [api-standards](../06-platform/api-standards.md), [testing-quality](../08-engineering/testing-quality.md), [configuration-register](configuration-register.md), [review-findings](review-findings.md); and, from v7.1, [market-expansion](../01-product/market-expansion.md), [user-journeys](../01-product/user-journeys.md), [customer-account](../02-commerce/customer-account.md), [first-party-operations](../03-sellers/first-party-operations.md), [admin-panel](../05-trust/admin-panel.md) and [sitemap](../09-information-architecture/sitemap.md).

## 6. Sitemap

The page inventory is [sitemap](../09-information-architecture/sitemap.md) v3, inside the information-architecture section, where every Page ID also has a page specification. It applies every alignment change that v7.0 listed here against Sitemap v2 (its §0 records them) and the additions of the v7.1 review. Sitemap v2 and the PRD v6 DOCX are superseded and are not sources for implementation.
