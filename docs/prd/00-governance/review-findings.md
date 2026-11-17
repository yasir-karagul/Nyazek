# Review Findings (v6 → v7, v7.1 and v7.2)

**Purpose:** the record of the independent, first-principles review of Nyazek PRD v6: what was found, how it was resolved, and where the resolution lives. No earlier gap list was used as a source.
**Classes:** C contradiction · I incomplete or ambiguous · U unsafe or infeasible as written · E factual or logical error · S simplification · M owner mandate.

---

## 1. Owner-mandated changes

| # | Class | Change | Where |
|---|---|---|---|
| F-01 | M | Mobile technology changed from React Native + Expo to **Flutter**. Sharing moved from TypeScript packages to language-neutral sources (OpenAPI, tokens, catalogues) with generators; the Phase 1 spike is a Flutter app | [mobile-flutter](../07-clients/mobile-flutter.md), [technology-stack](../06-platform/technology-stack.md) §3.7 |
| F-02 | M | **Claude is the sole AI engineering agent.** The backend/frontend split between two agents, separate branch prefixes and separate instruction files were removed; review independence was strengthened to compensate | [claude-workflow](../08-engineering/claude-workflow.md) |
| F-03 | M | Design workflow is **Stitch → Figma → manual refinement → Claude**; no Figma MCP or automated Figma export is assumed; the token file in the repository is the source of truth; designs reach Claude as provided references or through computer use | [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §6 |
| F-04 | M | **Computer use** is explicitly authorised for design inspection, visual verification, tool navigation and UI testing, with security boundaries | [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §6.3, [security](../05-trust/security.md) §9 |
| F-05 | M | **PHP prohibited**, including self-hosted PHP products | [technology-stack](../06-platform/technology-stack.md) §1 |
| F-06 | M | Technology stack re-evaluated end to end with justification per change | [technology-stack](../06-platform/technology-stack.md) |
| F-07 | M | References to the companion "Review and Gap List" were removed; items v6 deferred to it are now specified here or registered as decisions | whole set |

## 2. Product, scope and KPIs

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-08 | C | "All P0 and P1 must be complete before launch" versus "P1 may ship within 30 days" | One definition of priorities | [scope-priorities](../01-product/scope-priorities.md) §1 |
| F-09 | E | KPI targets mutually inconsistent by 3×–12× | Kept as D-01; capacity planning uses the higher scenario | [overview-vision-kpis](../01-product/overview-vision-kpis.md) §4.1 |
| F-10 | I | GMV had no time basis; a later return would change past months | Delivered GMV and Net GMV defined | [data-analytics](../06-platform/data-analytics.md) §4 |
| F-11 | I | "SKU", "listing" and "offer" used interchangeably | Offer defined as the unit; KPI counts active offers | [catalog-listings](../02-commerce/catalog-listings.md) §1 |
| F-12 | E | Example commission rates (4%–12%) cannot produce a 12%–18% blended take rate | D-20; contribution-margin model as a pricing precondition | [business-model](../01-product/business-model.md) |
| F-13 | U | "Escrow float" presented as a revenue stream without a confirmed custody model | Removed from plans | [business-model](../01-product/business-model.md) §2 |
| F-14 | I | Unit economics incomplete: Nyazek pays couriers for all shipments and absorbs refused COD parcels | Explicit cost table; worked illustration; launch-gating model | [business-model](../01-product/business-model.md) §4 |
| F-15 | U | Competitive "moats" stated as facts | Reframed as goals with dependencies | [overview-vision-kpis](../01-product/overview-vision-kpis.md) §5 |
| F-16 | U | Six-month timeline with about 197 P0 pages | Scope warning with reduction options; launch gates | [release-plan](release-plan.md) §3 |

## 3. Identity and accounts

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-17 | C | Email verification required before ordering, but guests exempt (trivially bypassed); phone-OTP customers may have no email | Order gate is a verified phone; customer email optional (D-23) | [identity-access](../05-trust/identity-access.md) §2 |
| F-18 | C | "Only verified emails hold a claim" versus "claim inserted with the account so races cannot both succeed" | Unverified claim at creation; uniqueness enforced at verification | [identity-access](../05-trust/identity-access.md) §3.2 |
| F-19 | U | Conflict message at form submission enables account enumeration | Message shown only after control of the identifier is proven | AUTH-2 |
| F-20 | I | Seller email blocked "until financial retention is complete" (possibly 7 years) | One 90-day cool-down for all realms | ID-8 |
| F-21 | I | Recycled phone numbers could take over phone-only accounts | Stale-number rule | [identity-access](../05-trust/identity-access.md) §4.2 |
| F-22 | I | Guest checkout with a phone already registered was undefined | OTP signs in to the existing customer account; other realms refused | GST-2 |
| F-23 | I | Session model mixed JWT and cookies without stating which is authoritative | Opaque server sessions for web; JWT + rotating refresh for mobile | [identity-access](../05-trust/identity-access.md) §5 |
| F-24 | S | Per-app Next.js proxy for cookies | Same-origin `/api` path at the edge | [architecture](../06-platform/architecture.md) §2 |
| F-25 | I | Admin "IP allow-list or VPN" | Zero-trust access in front of the Admin origin | [identity-access](../05-trust/identity-access.md) §6 |
| F-26 | I | App Store rule: Sign in with Apple required when other social logins are offered | Added for the iOS app | AUTH table |
| F-27 | I | No minimum age | Customers confirm 18+ | ID-11 |

## 4. Catalogue, search and Buy Box

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-28 | C | 50-listing cap stated for all sellers in the seller feature table but only for individuals elsewhere | One rule (D-04) | [catalog-listings](../02-commerce/catalog-listings.md) §5 |
| F-29 | I | Buy Box formula had no scales or component definitions | Components normalised 0–100 with formulas | [search-buy-box](../02-commerce/search-buy-box.md) §2.3 |
| F-30 | I | Buy Box ignored item condition and variants | Per variant; only `NEW` competes | BBX-1, BBX-2 |
| F-31 | I | Search weights were qualitative; "TF-IDF + semantic" | Numeric starting weights; BM25; semantic search P2 | [search-buy-box](../02-commerce/search-buy-box.md) §1.4 |
| F-32 | I | Search result unit undefined | Product is the unit, showing the Buy Box offer | SRC-1 |
| F-33 | E | Anti-dumping measured against "category average" | Median of the same variant or product type | PRC-3 |
| F-34 | I | Reference-price rule could be gamed and relied on seller input | Computed from price history | PRC-9 |
| F-35 | I | Package weight and dimensions were not mandatory though fees and courier limits need them | Mandatory per variant | [catalog-listings](../02-commerce/catalog-listings.md) §6 |
| F-36 | U | Bulk import by image URL is a server-side request forgery vector | Egress proxy rule | SEC-12 |
| F-37 | U | MAP enforcement may conflict with competition rules | Counsel check before enabling | PRC-7 |

## 5. Checkout, orders and inventory

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-38 | I | No state for COD confirmation or risk review although the seller's clock "pauses" | `ON_HOLD` state | [checkout-orders](../02-commerce/checkout-orders.md) §6 |
| F-39 | E | Return and dispute modelled as sub-order states; cannot represent partial returns | Separate records linked to the sub-order | same |
| F-40 | I | Customer could not cancel after label creation though the rule says "before shipping" | Customer cancellation allowed until `SHIPPED`; waybill voided | §8 |
| F-41 | I | No retry path between delivery attempts; no direct `SHIPPED → DELIVERED` | Added | §6 |
| F-42 | E | COD modelled as one order-level payment | COD collection per shipment | [payments](../04-finance/payments.md) §3 |
| F-43 | C | Free-delivery threshold basis: "full cart total" versus "subtotal after coupons before loyalty" | One rule | [checkout-orders](../02-commerce/checkout-orders.md) §4.1 |
| F-44 | C | Loyalty "cannot be combined with seller coupons" versus a discount order that chains them | Stacking table | [pricing-promotions](../02-commerce/pricing-promotions.md) §2.2 |
| F-45 | I | No single price-calculation definition | Quote engine with stored per-line allocations | [checkout-orders](../02-commerce/checkout-orders.md) §4 |
| F-46 | U | Reservations in Redis TTL locks; durability risk and drift | PostgreSQL rows with atomic conditional updates | [inventory](../02-commerce/inventory.md) |
| F-47 | E | Inventory "state machine" listed transitions as states | Three counters and a movement table | [inventory](../02-commerce/inventory.md) §1–2 |
| F-48 | U | Reservation at checkout start by unauthenticated visitors enables stock denial | Session requires a signed-in customer or OTP-verified guest; caps | CHK-1, CHK-5 |
| F-49 | I | Seller shipment SLA could be breached by courier delay | SLA ends at `READY_TO_SHIP`; handover grace handled by Logistics | [checkout-orders](../02-commerce/checkout-orders.md) §7 |
| F-50 | I | Prepaid refund on failed delivery undefined | Rule plus D-31 | ORD-9 |
| F-51 | S | Carts and sessions in the cache | PostgreSQL; server-side carts for signed-in customers | CRT-1 |

## 6. Payments, ledger, commission and wallet

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-52 | U | PSP-held escrow stated as fact; many PSPs only settle to the merchant | Custody models and widened D-09; neutral wording until decided | [payments](../04-finance/payments.md) §2 |
| F-53 | I | No fallback when a PSP has no refund or payout API | Manual queues as P0 | [payments](../04-finance/payments.md) §10 |
| F-54 | E | Loyalty redemption posted as promotion expense although the liability already exists (double expense) | Redemption debits the liability | JE-4 |
| F-55 | I | 1P sale, cost of goods, PSP settlement, payout-in-transit, chargeback and seller-deficit postings missing | Added | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §4 |
| F-56 | C | Commission "accrued at confirmation" versus "charged at release" | Recognised once, at release | JE-9 |
| F-57 | I | Seller "Pending balance" had no ledger definition | Wallet balances defined as views | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §2 |
| F-58 | I | Payouts can exceed cash on hand (platform-funded discounts, COD timing) | Funding position report; payout precondition | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §4.6 |
| F-59 | I | Cash rounding left as a line item idea | Price step and payable-total rule (D-12) | MON-4, MON-5 |
| F-60 | I | Late, duplicate, under- and over-payment handling | Rules PAY-8 to PAY-10 | [payments](../04-finance/payments.md) §5 |
| F-61 | U | Early escrow release on customer confirmation adds recovery risk | Disabled by default (D-22) | WAL-6 |
| F-62 | E | Customer invoice issued by Nyazek for 3P sales; one commission invoice per order | Seller named as seller of record; per-period commission invoice (D-26) | [tax-invoicing](../04-finance/tax-invoicing.md) §3 |
| F-63 | U | "Tax can be activated without code changes" | Reworded as an expectation with review | TAX-3 |
| F-64 | I | Cash-pickup payouts without a partner network or controls | P1 subject to D-30 | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §6.2 |

## 7. Logistics, returns and disputes

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-65 | C | Sellers "do not choose" and "select" couriers in the same rule | Automatic assignment | LOG-1 |
| F-66 | U | Design assumed courier APIs and delivery OTP | Courier tiers with a file-based tier as P0; proof hierarchy | [logistics](../02-commerce/logistics.md) §1.1, §6 |
| F-67 | C | Three different statements of who pays for failed delivery; "customer bears it through risk scoring" is not a cost rule | One attribution table | [logistics](../02-commerce/logistics.md) §7 |
| F-68 | C | Seller feature table says the seller always pays return shipping | Reason-based matrix (D-05) | [returns-disputes](../02-commerce/returns-disputes.md) §3 |
| F-69 | U | Replacement required before refund contradicts the money-back guarantee | Refund default (D-25) | §4.1 |
| F-70 | C | Dispute only "before 7-day auto-release" although returns continue after it | Dispute windows tied to their triggering events | [returns-disputes](../02-commerce/returns-disputes.md) §6.1 |
| F-71 | I | Return and dispute machines lacked withdrawal, expiry, partial outcome, hand-over timeout | Completed | §4, §6.2 |
| F-72 | I | Address reference data source undefined | D-32 | ADR-1 |

## 8. Sellers, reviews, loyalty, ads, notifications

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-73 | U | Automatic KYC approval for "verified" retailers with no verification source | Human review for all (D-24) | KYC-1 |
| F-74 | C | 30-day rolling window versus "recovery over 60 days"; separate inactivity-decay rule | Recovery and repeat-offence rules; one minimum-sample rule | [seller-performance](../03-sellers/seller-performance.md) §2–3 |
| F-75 | I | Performance metrics lacked denominators and attribution | Defined with cancel reasons | [seller-performance](../03-sellers/seller-performance.md) §1 |
| F-76 | C | Reviews "all held for admin approval" versus automated pre-screen | Pre-screen is the rule | [reviews-qa](../02-commerce/reviews-qa.md) §3 |
| F-77 | I | Loyalty tiers "by points" would demote customers who redeem | Qualifying points over 12 months (D-34) | [loyalty](../02-commerce/loyalty.md) §4 |
| F-78 | I | Customer referral and birthday rewards named but unspecified | Specified with controls | [loyalty](../02-commerce/loyalty.md) §6–7 |
| F-79 | I | Ad auction lacked reserve price, relevance floor, no-competitor price, budget overrun rule, attribution | Added | [advertising](../02-commerce/advertising.md) |
| F-80 | C | "Push" at launch with no app; SMS for every event | Channel plan; SMS reserved for critical messages | [notifications-messaging](../02-commerce/notifications-messaging.md) §1 |
| F-81 | I | Customer–seller messaging had no owning module or abuse rules | Messaging module; pre-screen | §6 |
| F-82 | I | Invoices and labels in Arabic need a rendering approach | HTML-to-PDF | [technology-stack](../06-platform/technology-stack.md) §3.14 |

## 9. Governance, security, privacy, compliance

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-83 | I | 11 roles without a permission matrix or dual-control list | Baseline matrix and action list | [admin-governance](../05-trust/admin-governance.md) |
| F-84 | U | Dual control on suspension blocks urgent fraud response | 24-hour temporary freeze | SEL-3 |
| F-85 | C | Immutable 7-year logs versus erasure; audit trail conflated with operational logs | Separate streams; no personal data in audit records; crypto-shredding | [privacy-audit](../05-trust/privacy-audit.md) §5 |
| F-86 | I | No retention schedule per data class | Added | [privacy-audit](../05-trust/privacy-audit.md) §4 |
| F-87 | I | AI-agent security risks (prompt injection, tool misuse) absent | Agent guardrails | [security](../05-trust/security.md) §9 |
| F-88 | I | Fraud engine unspecified as rules or model; no failure mode | Rule-based, explainable, with fallback | [fraud-risk](../05-trust/fraud-risk.md) §1 |
| F-89 | U | Liability limited to commission value | Flagged for counsel | [compliance-legal](../05-trust/compliance-legal.md) §1.1 |
| F-90 | I | Terms acceptance not versioned | Acceptance records | CMS-2 |

## 10. Architecture, infrastructure and operations

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-91 | S | Two primary datastores (PostgreSQL + MongoDB) with no cross-store consistency | PostgreSQL only | [technology-stack](../06-platform/technology-stack.md) §3.1 |
| F-92 | S | Kafka for tens of events per second | Outbox + PostgreSQL queue | §3.2 |
| F-93 | I | Search engine, ORM, feature-flag provider, container platform left open | Decided | [technology-stack](../06-platform/technology-stack.md) |
| F-94 | S | Three Next.js servers | Storefront on Next.js; dashboards as static apps | §3.6 |
| F-95 | S | Self-run ELK, Prometheus and Grafana | Managed observability; audit trail in PostgreSQL with locked exports | §3.12 |
| F-96 | S | Analytics warehouse from Phase 3 | Deferred with triggers | §3.11 |
| F-97 | E | Capacity table not derived from KPIs; event volume overstated about 100× | Derived demand model | [reliability-sre](../06-platform/reliability-sre.md) §5 |
| F-98 | E | SLOs on outcomes Nyazek does not control (checkout completion, PSP approval, SMS delivery) | SLOs on availability and correctness; outcomes monitored | [reliability-sre](../06-platform/reliability-sre.md) §2 |
| F-99 | C | Two severity tables; monthly drill versus quarterly restore; 1-hour recovery point with daily backups | Single definitions | [reliability-sre](../06-platform/reliability-sre.md) §4 |
| F-100 | I | "Page load under 2 s on 3G/4G" not measurable | Core Web Vitals from real users | [reliability-sre](../06-platform/reliability-sre.md) §1 |
| F-101 | I | Synthetic probes "from Iraqi vantage points" may not be purchasable | Self-hosted probes or real-user data | §3 |
| F-102 | I | Module list lacked owners for cart and checkout, ledger, invoicing, messaging, configuration | 28 modules with owners | [architecture](../06-platform/architecture.md) §3 |
| F-103 | I | Event catalogue inconsistent (dispute publisher, delivery mixed with release) | Naming rules and catalogue | [architecture](../06-platform/architecture.md) §4 |
| F-104 | I | No rule for post-failover financial reconciliation | REC-5 | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §6 |
| F-105 | E | Local stack relied on MinIO community edition, now unmaintained | Replaced | [technology-stack](../06-platform/technology-stack.md) §3.15 |
| F-106 | I | On-call assumed without people | D-27; stated limitation | INC-3 |
| F-107 | I | "Two human reviewers" on protected paths without confirming two exist | GRD-2 | [claude-workflow](../08-engineering/claude-workflow.md) §4 |
| F-108 | I | Dozens of "admin-configurable" values without names or defaults | Configuration register | [configuration-register](configuration-register.md) |

## 11. Facts re-verified

| Fact | Result |
|---|---|
| Iraq has 19 governorates (Halabja the 19th) | Retained |
| AWS UAE and Bahrain facilities damaged in March 2026; unrecoverable resources reported in September 2026 | Confirmed in public reporting; region rule retained |
| E-Commerce Regulation No. 4 of 2025; CMC framework of February 2025; no data-protection law in force | Consistent with public law-firm summaries; counsel to validate |
| Contrast figures for the orange palette | Recomputed; retained |

## 12. v7.1 completeness review (November 2026)

A second pass over the v7 set, requested by the owner before the architecture phase: find missing topics, rules, journeys and edge cases; add the expansion scope (Iraq first, then Syria and the Gulf); remove contradictions and duplication. Classes as above, plus **G** gap (topic absent) and **X** expansion scope.

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-109 | X | The set was written as Iraq-only: "IQD only", Iraqi phone ranges, Baghdad time and the 19 governorates appear as fixed facts, with "international expansion" as one word under Future | Market defined as a first-class dimension; readiness requirements made P0; Syria and Gulf profiles and entry gates documented; decisions D-39 to D-41 | [market-expansion](../01-product/market-expansion.md) |
| F-110 | E | "Amounts are integers in IQD" cannot represent a two- or three-decimal currency, and ISO 4217 itself gives IQD three decimals, which formatting libraries and some providers assume | Platform minor unit with a per-currency exponent and price step; adapter conversion rule | MON-1, MON-8, PAY-19 |
| F-111 | G | One ledger with no notion of legal entity, book or period close | One book per market and entity; monthly close | LED-6, LED-7 |
| F-112 | G | Tax engine had regions but no place for invoices that must be reported to a tax authority | E-invoicing port; per-market document rules | TAX-5, TAX-6 |
| F-113 | G | No user journeys: the set specified rules by domain but never the end-to-end paths that tests and designs follow | Journey catalogue for customers, sellers and staff, with an edge-case register | [user-journeys](../01-product/user-journeys.md) |
| F-114 | G | The sitemap lived outside the repository, still aligned to v6, with its corrections listed but not applied | Sitemap v3 added to the PRD with all corrections applied and counts generated by a script | [sitemap](../09-information-architecture/sitemap.md) |
| F-115 | G | The Admin Panel had roles and pages but no description of its queues or of how admin screens behave | Admin Panel document: modules, queue catalogue, common rules | [admin-panel](../05-trust/admin-panel.md) |
| F-116 | G | Favourites, alerts, reorder and the effects of account deletion on customer data had no owner | Customer account document | [customer-account](../02-commerce/customer-account.md) |
| F-117 | G | 1P had four lines of operations; no goods receipt, cost method, adjustments or return handling, and the ledger credited 1P inventory without ever debiting it | 1P operations document; postings JE-34 to JE-37; decision D-42 | [first-party-operations](../03-sellers/first-party-operations.md), [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §4.5 |
| F-118 | G | "Seller compensated per courier contract" for lost parcels had no posting or receivable | JE-38, JE-39; account 1150 | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §4.5 |
| F-119 | I | Return terms could change under an existing order when a category policy or a product's category changed | Terms snapshotted on the order line | RET-6, CAT-13 |
| F-120 | I | No upper bound on returned quantity; no rule for a refund falling due on a suspended or closed seller; no rule against retroactive shipping after a partial return | Added | RET-7, REF-4, REF-5 |
| F-121 | G | Warranty after the return window was collected as listing data but had no process | Warranty rule; structured claims P2 | RET-8 |
| F-122 | C | "Digital items" listed as non-returnable although nothing digital can be listed or delivered | Removed; digital goods and services explicitly out of scope | PRH-6, [scope-priorities](../01-product/scope-priorities.md) §4 |
| F-123 | C | Offer condition `USED` in the catalogue but absent from the customer filter | Allowed conditions made configuration; `USED` off at launch pending D-44 | [catalog-listings](../02-commerce/catalog-listings.md) §4.2 |
| F-124 | G | Hazardous goods (batteries, aerosols, perfumes) had no listing flag or courier rule | `hazardous` flag and serviceability rule | SVC-5 |
| F-125 | G | Product recall, GTIN conflicts, archiving of referenced products, category moves | Added | PRH-5, CAT-11 to CAT-13 |
| F-126 | G | Cart conflicts between devices; phone snapshot on orders; switching a failed prepaid order to cash | Added | CRT-6, ORD-13, PAY-18 |
| F-127 | G | Seller rules missing: one store per account, seller must be established in the market, pickup-address removal, store-name changes | Added | SEL-5 to SEL-8 |
| F-128 | G | Payout transfer fees and the final payout of a closing account were unspecified | Added; decision D-43 | PO-9, PO-10 |
| F-129 | G | Customers who phone had no path; staff acting for a customer and read-only view of a seller's dashboard were undefined | Added; inbound phone line is D-45 | SUP-11, ADM-6, ADM-7 |
| F-130 | G | Requests for user data from authorities had no owner or procedure | Added | DSR-4 |
| F-131 | G | No supported-browser statement, although much traffic arrives through in-app browsers | Added | WEB-7 |
| F-132 | E | Quiet hours hard-coded to Baghdad time | Configuration per market | NTF-2 |
| F-133 | E | Broken cross-references (order-number rule, unit-economics section, treasury section, a mislabelled link) | Corrected | [architecture](../06-platform/architecture.md) §6, [logistics](../02-commerce/logistics.md) FEE-4 |
| F-134 | C | The stack was recorded as "decided" and implementation as able to start, while the owner has not finalised the stack and the workflow puts PRD approval and architecture first | Stack marked proposed; technical decisions returned to "Proposed"; README and workflow document aligned with ADR-0001 | [technology-stack](../06-platform/technology-stack.md), [claude-workflow](../08-engineering/claude-workflow.md) |
| F-135 | C | Engineering workflow tracked tasks as GitHub issues under `docs/tasks/`; the approved workflow uses `tasks/MASTER_TASKS.md` and four review disciplines | Aligned | [claude-workflow](../08-engineering/claude-workflow.md) |
| F-136 | S | Sitemap listed the seller FAQ twice under two IDs and banners under both CMS and Ads | One ID each | [sitemap](../09-information-architecture/sitemap.md) |

### 12.1 Assumptions made in this review

These were decided as routine professional judgement so the set is complete. The owner ratified them with T-0013 and the section approvals on 2026-11-17.

| Assumption | Where |
|---|---|
| Markets are domestic marketplaces; no cross-border selling (D-41 records the question) | MKT-3 |
| One seller account runs one store; sellers must be established in the market | SEL-7, SEL-8 |
| `USED` condition disabled at launch | D-44 |
| No minimum order value, gift options, delivery slots, pickup points or substitutions in v1.0 | ORD-14 |
| Favourites reference variants; limit of 500 | CUS-3, CUS-5 |
| Loyalty points are forfeited at account deletion after a warning | CUS-13 |
| Store name changeable once every 30 days | SEL-6 |
| Nyazek bears payout transfer fees by default | PO-9, D-43 |
| Weighted-average cost for 1P stock | FP-6, D-42 |
| Supplier record (basic) and the seller activity log are P0; purchase orders stay P2 | [sitemap](../09-information-architecture/sitemap.md) §8.4, §7.12 |
| Supported browsers and minimum mobile operating systems | WEB-7, [mobile-flutter](../07-clients/mobile-flutter.md) §2 |
| Expansion work starts only after Iraq meets the precondition in MKT-11 | [market-expansion](../01-product/market-expansion.md) §6 |

## 13. v7.2: terminology and information architecture (November 2026)

| # | Class | Finding | Resolution | Where |
|---|---|---|---|---|
| F-137 | S | The owner adopted **Customer** as the official term; "buyer" was used in every document, in identifiers (realm, module, configuration group, rule prefix, journey IDs, page tags and IDs, routes, app names) and in user-facing names ("Buyer Protection Policy", "Verified buyer", "Buyer Funds Held", "monthly active buyers") | Replaced everywhere, including identifiers, so documents, interfaces and code use one word: realm `CUSTOMER`, module and configuration group `customers`, `CUS-n`, `JC-n`, `[CUSTOMER]`, `AD-USR-CUSTOMERS`, `/legal/customer-protection`, `mobile_customer`, MAC | All documents; [glossary](glossary.md) |
| F-138 | S | "Customer" was also used loosely for anyone contacting support, including sellers | Ticket state renamed `WAITING_ON_REQUESTER`; support wording uses "requester" or "caller" where a seller may be meant | SUP-4, SUP-7, SUP-11 |
| F-139 | G | Pages had an inventory line each but no specification: structure, content, actions and states were left to the designer or the implementer | A specification for every Page ID, built on eleven page templates and a shared-component catalogue; checked by `_tools/check_ia.py` | [09-information-architecture](../09-information-architecture/README.md) |
| F-140 | G | Navigation was undefined: header, mega menu, footer, account menu, seller and admin sidebars, visibility by staff role and seller state, landing pages | Defined | [navigation](../09-information-architecture/navigation.md) |
| F-141 | G | List tabs ("Pending", "Processing", "Returned") had no mapping to the sub-order states, and no state had a customer-facing label | Mapping and labels for orders, returns, disputes, refunds, payments, offers, requests, payouts, tickets | [taxonomy-and-labels](../09-information-architecture/taxonomy-and-labels.md) §3–4 |
| F-142 | G | Delivery estimates depend on a "selected governorate" that no page let the customer select | "Deliver to" selector in the header | [navigation](../09-information-architecture/navigation.md) §1.1 |
| F-143 | G | URL rules were missing: slug format, identifiers in URLs, list state, sign-in return, listing parameters | Defined | [ia-model](../09-information-architecture/ia-model.md) §3–4 |
| F-144 | G | Multi-page flows (checkout, payment return, sign-in, returns, onboarding, import, approvals, payout run) had rules but no step order, back behaviour or exits | Defined | [flows](../09-information-architecture/flows.md) |
| F-145 | G | Only the ten top-level categories existed | Proposed second level so navigation and seed data can be built | [taxonomy-and-labels](../09-information-architecture/taxonomy-and-labels.md) §2 |

### 13.1 Assumptions made in v7.2

Ratified by the owner on 2026-11-17 (D-46). Arabic wording is still finalised in copy review (UI-4).

| Assumption | Where |
|---|---|
| Arabic interface term for Customer is العميل; all Arabic labels listed are proposals for copy review | [taxonomy-and-labels](../09-information-architecture/taxonomy-and-labels.md) |
| The folder is `09-information-architecture`, lower case and numbered, following the convention decided for `docs/` | [document-control](document-control.md) |
| Slugs are Latin; product URLs carry a short ID that identifies the product | IA-10 |
| "Buy now" adds the item and opens checkout for the whole cart | `SF-PDP` |
| A mobile bottom bar on the Storefront and Seller Dashboard | NAV rules, [navigation](../09-information-architecture/navigation.md) §1.3, §2.1 |
| Customers see "Shipment" for a sub-order; failed deliveries appear under the customer's "Cancelled" tab and the seller's "Returned" tab | [taxonomy-and-labels](../09-information-architecture/taxonomy-and-labels.md) §3.1 |
| Admin password resets go through a Super Admin (no self-service) | `AD-AUTH-LOGIN` |
| Level-2 category tree | [taxonomy-and-labels](../09-information-architecture/taxonomy-and-labels.md) §2 |

## 14. v7.3: independent review of v7.2 (November 2026)

Task T-0012. Three fresh-context reviewers covered product and commerce, finance to engineering, and the information architecture (with a sample check of about 250 page citations). The full list of 96 findings, each with its disposition, is in `docs/reviews/documentation/2026-11-17-T-0012-prd-v7-2.md` (finding IDs with the prefix `F-DOC`); it is not repeated here. Summary: 4 critical and 47 major findings fixed (one part of a major finding rejected with reason: CodCollection creation at shipment); 45 minor findings, of which 34 fixed, 2 deferred to Phase 2 (T-0022, T-0029) and 9 deferred to T-0060. A re-review of the fixes raised 22 further points (6 major), all fixed, and corrected 28 page citations.

Main changes:

| Area | Change | Where |
|---|---|---|
| Orders | Payment window and expiry without revival; parent status table; derived line status from quantity counters; handling-time bound; admin cancel only before shipping; suspended and closing sellers | ORD-15, ORD-16, §6, §6.1, SLA-6, SLA-7, §8 |
| Payments | Refund, CodCollection and chargeback machines; refunds without order lines | payments §4, §8, PAY-9, PAY-20, PAY-21, CBK-1, CBK-2 |
| Ledger | Accounts 1160, 2180, 2190; JE-14 balanced; JE-40 to JE-49; LED-8; REC-6 | ledger-reconciliation §3–6 |
| Wallet and payouts | Partial releases, completion rule, payout and run states, movement types, commission notice | WAL-2 to WAL-5, WAL-10, PO-6, PO-7, PO-11, COM-3 |
| Returns and disputes | `IN_DISPUTE`, `CLOSED`, `REVIEW_REQUESTED`; seller store policy; change-of-mind fee; goods outcome; inspection | RET-9 to RET-12, DSP-4, DSP-6 |
| Sellers | State transition table; performance mapping; 1P scored for the Buy Box; offer state table | seller-accounts-kyc §5, seller-performance §1, PRF-7, catalog §4.1 |
| Platform and workflow | Shared-transaction mechanism; proposed-stack wording; one protected-path list; claude-workflow aligned with ADR-0001 and ADR-0002 | architecture §3.2, technology-stack §1–2, claude-workflow |
| Information architecture | Pages, flows, tabs and labels updated to the rules above | `09-information-architecture` |

### 14.1 Defaults chosen in v7.3

Ratified by the owner on 2026-11-17 (D-47).

| Default | Where |
|---|---|
| A prepaid order must be paid within 30 minutes of placement; stock stays reserved until then; a payment after the deadline is refunded automatically | ORD-16, PAY-9 |
| Cart lines are removed at placement, with "restore to cart" after expiry | CRT-7 |
| Customer-fault failed delivery: outbound shipping retained, no other deduction (the D-31 recommendation, now implemented) | ORD-9 |
| Change-of-mind return fee equals the rate-card return-shipping price | RET-10 |
| Sellers may offer a longer return window (up to 30 days) and free change-of-mind returns, never less than the category policy | RET-9 |
| When a received return ends in the seller's favour, the item goes back to the customer (customer pays for change of mind) unless the customer leaves it | RET-11 |
| A dispute review never claws back a refund from the customer; Nyazek compensates the seller | DSP-4 |
| On suspension, unconfirmed sub-orders are cancelled and confirmed ones stay with the seller | SLA-7 |
| The 1P store's score is computed like any seller's and feeds the Buy Box and search | PRF-7 |
| Kurdistan Region governorates are not serviceable at launch until D-13 closes | SVC-1 |
| A payout run needs the previous business day's reconciliation signed off | REC-6 |
| Commission increases take effect at least 30 days after publication; no seller-specific rates | COM-3 |
| `READY_TO_SHIP` means packed with a waybill; the pickup request follows within the handover grace | checkout-orders §6, logistics §5 |

