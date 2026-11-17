# Open Decisions Register

**Authoritative for:** every decision that needs the owner (or counsel, or the accountant), its recommended default, and when it starts to block work.
**How engineering treats an open decision:** the recommended default is implemented behind configuration and the decision stays open until the owner closes it here ([claude-workflow](../08-engineering/claude-workflow.md) GRD-9).

IDs D-01 to D-19 are unchanged from PRD v6 so existing references remain valid. D-39 to D-45 were added by the v7.1 completeness review, D-46 by v7.2 and D-47 by v7.3. Status values: **Open** · **Proposed** (a review changed a rule or proposes a default and asks for ratification) · **Closed** (recorded in §5).

---

## 1. Business and product decisions

| ID | Decision | Recommended default | Owner | Needed by | Status | Spec |
|---|---|---|---|---|---|---|
| D-01 | Re-baseline GMV, MAC, frequency and AOV targets so they agree | Derive GMV from MAC × frequency × AOV | Owner | Phase 1 | Open | [overview-vision-kpis](../01-product/overview-vision-kpis.md) §4.1 |
| D-02 | Refund destination for COD orders | Customer's verified mobile-wallet or bank account; no store credit | Owner | Phase 2 | Open | [payments](../04-finance/payments.md) §6 |
| D-03 | Seller payout cadence; escrow hold versus return window | Monthly default, weekly for sellers in good standing (P1); hold = longer of 7 days and the category return window | Owner | Phase 2 | Open | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §3, §6 |
| D-04 | Listing cap by seller type | 50 for Individual Entrepreneurs in the first 3 months; 5,000 for businesses | Owner | Phase 1 | Open | [catalog-listings](../02-commerce/catalog-listings.md) §5 |
| D-05 | Who pays return shipping, by reason | Seller for seller-fault reasons; customer for change of mind | Owner | Phase 3 | Open | [returns-disputes](../02-commerce/returns-disputes.md) §3 |
| D-07 | Phone-number exclusivity across account types | Exclusive | Owner | Phase 1 | Open | [identity-access](../05-trust/identity-access.md) ID-10 |
| D-08 | Social login for sellers | Customers only | Owner | Phase 1 | Open | [identity-access](../05-trust/identity-access.md) §4 |
| D-10 | Commission base when Nyazek funds the discount | Pre-discount value | Owner | Phase 2 | Open | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §1.2 |
| D-11 | Payment channels and whether to use an aggregator | Evaluate an aggregator for launch; Qi Card, FIB, Nass as P1 | Owner | Phase 1 | Open | [payments](../04-finance/payments.md) §1 |
| D-12 | Cash rounding | Price step of 250 IQD for prices and fees; payable totals always multiples of 250, rounding in the customer's favour | Owner + accountant | Phase 1 | Open | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §2 |
| D-13 | Kurdistan Region coverage, Kurdish language, legal and customs rules | Validate before announcing coverage; Kurdish interface after launch | Owner + counsel | Phase 3 | Open | [logistics](../02-commerce/logistics.md) SVC-4 |
| D-15 | Kickoff date and scope versus the six-month window | Confirm the date; keep P0 as launch gates and move P1 to the 30-day fast-follow; see the scope warning in the release plan | Owner | Phase 1 | Open | [release-plan](release-plan.md) §3 |
| D-19 | Design-system corrections (Arabic typeface, accessible orange, missing tokens, numerals) | Adopt the recommended resolutions before any screen is produced | Owner + designer | Phase 1 | Open | [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §3 |
| D-20 | Commission schedule by category, sub-category and product type, reconciled with the target take rate | Finance proposes after the contribution-margin model | Owner + Finance | Phase 2 | Open | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §1.1 |
| D-21 | Shipping rate card, free-delivery threshold, COD fee, and who funds free delivery | Finance proposes after courier quotes; Nyazek funds free delivery | Owner + Finance | Phase 2 | Open | [logistics](../02-commerce/logistics.md) §4, [business-model](../01-product/business-model.md) §4.1 |
| D-22 | Early escrow release when the customer confirms receipt | Not enabled at launch | Owner | Phase 2 | Proposed | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) WAL-6 |
| D-23 | Customer email optional; the order gate is a verified phone | Adopt | Owner | Phase 1 | Proposed | [identity-access](../05-trust/identity-access.md) §2 |
| D-24 | Remove automatic KYC approval; every seller reviewed by a person | Adopt; priority queue for businesses | Owner | Phase 1 | Proposed | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) KYC-1 |
| D-25 | Refund as the default outcome of a return; replacement optional (P1) | Adopt | Owner | Phase 3 | Proposed | [returns-disputes](../02-commerce/returns-disputes.md) §4.1 |
| D-28 | Launch couriers and their integration tiers | At least two couriers covering all launch-serviceable governorates; assume Tier C until proven otherwise | Owner + Logistics | Phase 1 | Open | [logistics](../02-commerce/logistics.md) §1.1 |
| D-29 | SMS aggregators (primary and fallback), sender ID, email sending domain | Two Iraqi-routed aggregators | Owner | Phase 1 | Open | [notifications-messaging](../02-commerce/notifications-messaging.md) §4–5 |
| D-30 | Cash-pickup payouts | Defer to P1 until a partner network and controls exist | Owner | Phase 3 | Proposed | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §6.2 |
| D-31 | Prepaid order refused at delivery: what is deducted from the refund | Outbound shipping fee retained; no other deduction | Owner | Phase 2 | Open | [checkout-orders](../02-commerce/checkout-orders.md) ORD-9 |
| D-32 | Source and ownership of the Iraq geo reference dataset (districts, neighbourhoods) | Compile with the launch couriers' zone lists; Logistics owns it | Owner + Logistics | Phase 1 | Open | [checkout-orders](../02-commerce/checkout-orders.md) ADR-1 |
| D-33 | Priority changes proposed by this review | Adopt the table | Owner | Phase 1 | Proposed | [scope-priorities](../01-product/scope-priorities.md) §3 |
| D-34 | Loyalty parameters: tier basis (12-month qualifying points), earn and redeem rates, tier perks, referral and birthday rewards | Adopt the tier basis; Marketing proposes values | Owner + Marketing | Before loyalty ships | Open | [loyalty](../02-commerce/loyalty.md) |
| D-36 | Ratify proposed configuration defaults (SLAs, windows, limits, thresholds) | Review the register once; tune in the closed beta | Owner | Phase 2 | Open | [configuration-register](configuration-register.md) |
| D-39 | Multi-market operating model | One codebase with market as a first-class dimension; shared or separate deployment decided per market at entry | Owner | Before architecture sign-off | Closed | [market-expansion](../01-product/market-expansion.md) §2–3 |
| D-40 | Order and timing of expansion (Syria, Gulf states) | No expansion work before Iraq meets MKT-11; first market chosen from a written market-entry assessment | Owner | After launch | Open | [market-expansion](../01-product/market-expansion.md) §6 |
| D-41 | Cross-border selling, and whether one seller login can manage entities in several markets | Not supported: each market is domestic; revisit at the second market | Owner | With D-40 | Closed | [market-expansion](../01-product/market-expansion.md) MKT-3, MKT-5 |
| D-43 | Who bears payout transfer fees | Nyazek for the standard cycle | Owner + Finance | Phase 2 | Open | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) PO-9 |
| D-44 | Item conditions allowed at launch | New, open box, refurbished; used goods not enabled | Owner | Phase 1 | Closed | [catalog-listings](../02-commerce/catalog-listings.md) §4.2 |
| D-45 | Inbound phone support line at launch, and its hours | Publish a line staffed in business hours; all calls logged as tickets | Owner | Phase 3 (with D-27) | Open | [support-cms](../02-commerce/support-cms.md) SUP-11 |
| D-46 | Information-architecture proposals: level-2 category tree, Arabic wording of navigation and status labels (including العميل for Customer), slug format, "buy now" behaviour, mobile bottom bar | Ratify as proposed; wording finalised in copy review | Owner | With the review of `09-information-architecture` | Closed | [information architecture](../09-information-architecture/README.md) §4 |
| D-47 | Defaults chosen while fixing the v7.2 review: payment window, change-of-mind return fee, seller store return policy, dispute review without clawback, suspended-seller orders, 1P performance score in the Buy Box, Kurdistan Region not serviceable at launch, daily reconciliation sign-off before payouts, commission notice period | Ratify as written | Owner | With T-0013 | Closed | [review-findings](review-findings.md) §14.1 |

## 2. Legal, regulatory and financial-control decisions

| ID | Decision | Recommended default | Owner | Needed by | Status | Spec |
|---|---|---|---|---|---|---|
| D-06 | Hosting regions and the meaning of "Iraqi data residency" | European primary and DR regions, backups with a second provider; residency defined with counsel | Owner + counsel | Phase 1 | Closed | [infrastructure-devops](../06-platform/infrastructure-devops.md) §2 |
| D-09 | Funds custody for **prepaid and COD** money before it is paid to sellers | Confirm with counsel and the PSP: PSP-held escrow if offered, otherwise a segregated client account; never a commingled account | Owner + counsel + PSP | Phase 1 | Closed | [payments](../04-finance/payments.md) §2 |
| D-14 | Legal entity, commercial registration, e-commerce licence, digital-platform registration tier | Start immediately; launch gate | Owner + counsel | Phase 1 | Open | [compliance-legal](../05-trust/compliance-legal.md) §3 |
| D-26 | Legal form and issuer of customer documents for 3P sales; per-period commission invoices | Receipt naming the seller, issued by Nyazek on the seller's behalf; one commission invoice per settlement period | Counsel + accountant | Phase 2 | Open | [tax-invoicing](../04-finance/tax-invoicing.md) §3 |
| D-37 | Accountant sign-off of chart of accounts, posting rules and recognition timing | Sign off before the ledger schema is frozen | Accountant | Phase 1 | Open | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) |
| D-38 | Counsel positions: liability cap, arbitration threshold, MAP enforcement, seller licensing, retention periods, breach-notification timelines | Counsel's wording governs | Counsel | Phase 3 | Open | [compliance-legal](../05-trust/compliance-legal.md) |
| D-42 | 1P inventory costing method | Weighted average cost | Accountant | Phase 1 (with D-37) | Open | [first-party-operations](../03-sellers/first-party-operations.md) FP-6 |

## 3. Team and operating decisions

| ID | Decision | Recommended default | Owner | Needed by | Status | Spec |
|---|---|---|---|---|---|---|
| D-27 | Human team: reviewers for protected code, on-call rota, and operations staff (KYC, catalogue, support, finance, logistics, risk) | At least one additional qualified human reviewer; three people for a 24/7 on-call rota or reduced out-of-hours commitment stated publicly; named owner for each admin role before the beta | Owner | Phase 1 | Open | [claude-workflow](../08-engineering/claude-workflow.md) §4, [reliability-sre](../06-platform/reliability-sre.md) INC-3 |

## 4. Technical proposals from the v7 review

These were closed by [ADR-0004](../../adr/0004-technology-stack.md) on 17 November 2026.

| ID | Decision | Proposed outcome | Status | Spec |
|---|---|---|---|---|
| D-16 | Separate origins for Storefront, Seller Dashboard and Admin Panel | Separate sub-domains, with a same-origin `/api` path on each | Closed | [identity-access](../05-trust/identity-access.md) §6 |
| D-17 | Event broker and timing | Transactional outbox + PostgreSQL job queue; no broker at launch | Closed | [technology-stack](../06-platform/technology-stack.md) §3.2 |
| D-18 | Container platform | Managed containers (no Kubernetes) | Closed | [technology-stack](../06-platform/technology-stack.md) §3.9 |
| D-35 | Ratify the revised technology stack as a whole (PostgreSQL-only data layer, OpenSearch, Valkey as cache only, Cloudflare edge, static dashboards, Flutter, managed observability, Claude as sole agent) | As specified | Closed | [technology-stack](../06-platform/technology-stack.md) |

## 5. Decision log

When a decision is closed, record here: ID, date, decision, decided by, and the change that updated the affected documents (the task ID while work stays local; the pull request once GitHub is used). Closing a decision always updates the documents listed in its "Spec" column in the same change.

| ID | Date | Decision | Decided by | Change |
|---|---|---|---|---|
| D-39 | 2026-11-17 | Default ratified: one codebase with market as a first-class dimension; shared or separate deployment decided per market at entry (MKT-7) | Owner | T-0014 |
| D-06 | 2026-11-17 | Default ratified: primary and DR in two European regions, backups with a second provider (INF-6). The legal meaning of "Iraqi data residency" is defined with counsel (INF-8, T-0015); the placement applies until then | Owner | T-0014 |
| D-09 | 2026-11-17 | Default ratified: PSP-held escrow (model A) where the contracted PSP offers it, otherwise a segregated client account (model B); never a commingled account. Counsel and the PSP confirm the model in use and any authorisation it needs before launch (T-0015; release-plan §4, gate 5) | Owner | T-0014 |
| D-44 | 2026-11-17 | Default ratified: New, Open box and Refurbished at launch; Used not enabled | Owner | T-0014 |
| D-41 | 2026-11-17 | Default ratified: no cross-border selling; each market is domestic; one seller entity per market; revisited at the second market | Owner | T-0014 |
| D-46 | 2026-11-17 | Ratified as proposed ([review-findings](review-findings.md) §13.1); Arabic wording finalised in copy review (UI-4) | Owner | T-0013 |
| D-47 | 2026-11-17 | Ratified as written ([review-findings](review-findings.md) §14.1) | Owner | T-0013 |
| D-35 | 2026-11-17 | Stack decided as in [ADR-0004](../../adr/0004-technology-stack.md) | Owner | T-0020 |
| D-16 | 2026-11-17 | Separate sub-domains with a same-origin `/api` path (ADR-0004) | Owner | T-0020 |
| D-17 | 2026-11-17 | Transactional outbox + pg-boss on PostgreSQL; no broker at launch (ADR-0004) | Owner | T-0020 |
| D-18 | 2026-11-17 | Amazon ECS on Fargate (ADR-0004) | Owner | T-0020 |
