# Nyazek (نيازك) Marketplace · Product Requirements v7.3

Multi-vendor marketplace (1P + 3P) · launching in **Iraq** (IQD, Arabic by default with RTL, and English) · planned expansion to **Syria and the Gulf** · API-first modular monolith · web at launch, Flutter apps after · Claude as the sole AI engineering agent under human supervision.

This folder is the source of truth for product requirements. It supersedes the PRD v6 DOCX and Sitemap v2. Start with [document-control](00-governance/document-control.md) for conventions.

---

## 1. Document map

### 00 Governance

| Document | Authoritative for |
|---|---|
| [document-control](00-governance/document-control.md) | Version, conventions, authority rules, v6 traceability |
| [review-findings](00-governance/review-findings.md) | Every issue found in v6 and in the v7.1 completeness review, with its resolution and the assumptions made |
| [open-decisions](00-governance/open-decisions.md) | Decisions awaiting the owner, counsel or the accountant |
| [configuration-register](00-governance/configuration-register.md) | Every configurable value with its proposed default (generated) |
| [release-plan](00-governance/release-plan.md) | Delivery phases, exit criteria, launch gates, external dependencies, roadmap |
| [risks](00-governance/risks.md) | Risk register |
| [glossary](00-governance/glossary.md) | Terms |

### 01 Product

| Document | Authoritative for |
|---|---|
| [overview-vision-kpis](01-product/overview-vision-kpis.md) | Summary, problem, vision, goals, KPIs, positioning |
| [users-personas](01-product/users-personas.md) | Customer, seller and internal personas |
| [user-journeys](01-product/user-journeys.md) | End-to-end journeys for customers, sellers and staff; edge-case register |
| [business-model](01-product/business-model.md) | Revenue streams, recognition, unit economics |
| [scope-priorities](01-product/scope-priorities.md) | Priority definitions, feature map, out of scope |
| [market-expansion](01-product/market-expansion.md) | Expansion to Syria and the Gulf: market concept, readiness requirements, market profiles, entry gates |

### 02 Commerce

| Document | Authoritative for |
|---|---|
| [catalog-listings](02-commerce/catalog-listings.md) | Categories, shared catalogue, listing types, offers, media, prohibited items |
| [pricing-promotions](02-commerce/pricing-promotions.md) | Price rules, coupons, deals, campaigns, stacking |
| [search-buy-box](02-commerce/search-buy-box.md) | Search, ranking, Buy Box |
| [customer-account](02-commerce/customer-account.md) | Customer profile, favourites, alerts, reorder, deletion effects |
| [checkout-orders](02-commerce/checkout-orders.md) | Addresses, cart, checkout, quote, order model and state machine, SLAs, cancellation |
| [inventory](02-commerce/inventory.md) | Stock model and reservations |
| [logistics](02-commerce/logistics.md) | Couriers, serviceability, shipping fees, delivery, RTO, COD remittance |
| [returns-disputes](02-commerce/returns-disputes.md) | Returns, refunds, warranty, disputes |
| [reviews-qa](02-commerce/reviews-qa.md) | Reviews, ratings, moderation, Q&A |
| [loyalty](02-commerce/loyalty.md) | Points, tiers, referrals |
| [advertising](02-commerce/advertising.md) | Sponsored ads |
| [notifications-messaging](02-commerce/notifications-messaging.md) | Channels, notification catalogue, consent, customer–seller messaging |
| [support-cms](02-commerce/support-cms.md) | Support tickets, static pages, CMS, marketing tags |

### 03 Sellers

| Document | Authoritative for |
|---|---|
| [seller-accounts-kyc](03-sellers/seller-accounts-kyc.md) | Seller types, onboarding, KYC, seller states, store rules |
| [seller-performance](03-sellers/seller-performance.md) | Score, levels, fairness, appeals |
| [seller-dashboard](03-sellers/seller-dashboard.md) | Seller Dashboard modules and staff roles |
| [first-party-operations](03-sellers/first-party-operations.md) | The Nyazek Official Store: receiving, cost, adjustments, fulfilment, returns |

### 04 Finance

| Document | Authoritative for |
|---|---|
| [payments](04-finance/payments.md) | Methods, custody, payment and COD state machines, refund execution |
| [ledger-reconciliation](04-finance/ledger-reconciliation.md) | Money rules, chart of accounts, posting rules, invariants, reconciliation |
| [commission-wallet-payouts](04-finance/commission-wallet-payouts.md) | Commission, escrow release, wallet, holds, payouts |
| [tax-invoicing](04-finance/tax-invoicing.md) | Tax engine, receipts, credit notes, commission invoices |

### 05 Trust

| Document | Authoritative for |
|---|---|
| [identity-access](05-trust/identity-access.md) | Realms, one-email-one-account, login, OTP, sessions, 2FA, origins |
| [admin-governance](05-trust/admin-governance.md) | Admin roles, permission matrix, dual control, configuration governance |
| [admin-panel](05-trust/admin-panel.md) | Admin Panel modules, queue catalogue, behaviour of admin screens |
| [fraud-risk](05-trust/fraud-risk.md) | Risk scoring, COD risk engine, self-dealing |
| [security](05-trust/security.md) | Security baseline, AI-agent guardrails |
| [privacy-audit](05-trust/privacy-audit.md) | Consent, data-subject and authority requests, retention, audit trail |
| [compliance-legal](05-trust/compliance-legal.md) | Regulation in Iraq, obligations, governing law, contracts |

### 06 Platform

Requirements in this folder are binding; the stack is decided by [ADR-0004](../adr/0004-technology-stack.md) (D-35 closed).

| Document | Authoritative for |
|---|---|
| [architecture](06-platform/architecture.md) | Pattern, modules, events, jobs, market as a dimension |
| [technology-stack](06-platform/technology-stack.md) | The reasons behind the technology choices (the decision is ADR-0004) |
| [api-standards](06-platform/api-standards.md) | API surfaces, versioning, errors, idempotency, webhooks |
| [data-analytics](06-platform/data-analytics.md) | Data ownership, metrics, analytics pipeline |
| [infrastructure-devops](06-platform/infrastructure-devops.md) | Hosting, environments, CI/CD, backups |
| [reliability-sre](06-platform/reliability-sre.md) | NFRs, SLOs, observability, incidents, DR, capacity |

### 07 Clients

| Document | Authoritative for |
|---|---|
| [web-apps](07-clients/web-apps.md) | Storefront, Seller Dashboard and Admin Panel as clients; RTL, SEO, accessibility |
| [mobile-flutter](07-clients/mobile-flutter.md) | Flutter apps, sharing strategy, readiness checklist |
| [design-system-ui-workflow](07-clients/design-system-ui-workflow.md) | Tokens, corrections, design-to-code workflow, computer use |

### 08 Engineering

| Document | Authoritative for |
|---|---|
| [claude-workflow](08-engineering/claude-workflow.md) | Owner and Claude roles, delivery rules, guardrails (day-to-day workflow: `docs/adr/0001-development-workflow.md`) |
| [testing-quality](08-engineering/testing-quality.md) | Test strategy, coverage, launch test gates |

### 09 Information Architecture

How the three web applications are organised and what every page contains. Index and reading order: [09-information-architecture/README](09-information-architecture/README.md).

| Document | Authoritative for |
|---|---|
| [ia-model](09-information-architecture/ia-model.md) | Principles, navigable objects, URL rules, page templates, global states |
| [sitemap](09-information-architecture/sitemap.md) | Page inventory, Page IDs, routes and page priorities |
| [navigation](09-information-architecture/navigation.md) | Headers, menus, footer, sidebars, visibility by role and state |
| [taxonomy-and-labels](09-information-architecture/taxonomy-and-labels.md) | Category tree, status labels, tab mappings, navigation labels |
| [shared-components](09-information-architecture/shared-components.md) | Components reused across pages and what each shows |
| [flows](09-information-architecture/flows.md) | Multi-page flows step by step |
| `pages-storefront-*`, `pages-seller-*`, `pages-admin-*`, [pages-system](09-information-architecture/pages-system.md) | The content, actions, states and governing rules of every page |

### Tools

`_tools/check_docs.py` (consistency checks) · `_tools/gen_config_register.py` (rebuilds the configuration register) · `_tools/count_pages.py` (sitemap counts) · `_tools/check_ia.py` (every page has one specification). Run all four after any change: `python3 _tools/<script> .` from this folder.

## 2. How the documents relate

```
Product (why, who, journeys, priorities, markets)
   └─► Commerce · Sellers · Finance · Trust        (domain rules: what the system must do)
          └─► Platform                             (qualities and constraints of how it is built and run)
                 └─► Information architecture      (pages, navigation, labels: what each screen contains)
                        └─► Clients                (how the web apps and Flutter apps are built on the one API)
                               └─► Engineering     (how Claude and the owner deliver it)
Governance cuts across all: decisions, configuration, risks, release plan, glossary.
```

### 2.1 Where cross-cutting topics live

| Topic | Authoritative document | Referenced by |
|---|---|---|
| Markets, currencies per market, expansion | market-expansion | architecture, ledger, tax, identity, logistics, compliance |
| Money, rounding, price step, currency table | ledger-reconciliation §2 | checkout-orders, pricing-promotions, loyalty, commission, tax, api-standards |
| Sub-order states and cancel reasons | checkout-orders §6 | seller-performance, logistics, returns-disputes, inventory, ledger |
| Who pays for failed delivery | logistics §7 | business-model, checkout-orders, seller-performance |
| Who pays return shipping | returns-disputes §3 | business-model, ledger |
| Discount stacking and funding | pricing-promotions §2 | checkout-orders, loyalty, commission |
| Escrow hold and release | commission-wallet-payouts §3 | returns-disputes, ledger, payments |
| COD eligibility and confirmation | fraud-risk §4 | checkout-orders, payments, logistics |
| COD cash controls | logistics §8, payments §7 | ledger |
| Realm, audience, sessions | identity-access | api-standards, security, web-apps, mobile-flutter |
| Events and module boundaries | architecture | data-analytics, every domain document |
| Personal data, retention, audit | privacy-audit | security, notifications, data-analytics |
| Priorities | scope-priorities (features), sitemap (pages) | every document |
| Journeys and edge cases | user-journeys | testing-quality, design workflow |
| Page IDs | sitemap | user-journeys, seller-dashboard, admin-panel, design workflow |
| Page content, navigation, status labels | 09-information-architecture | web-apps, seller-dashboard, admin-panel, design workflow |
| Terminology (Customer, not buyer) | glossary | every document |
| Admin queues and screen behaviour | admin-panel | every domain document with a queue |
| Metric definitions | data-analytics §4 | overview-vision-kpis, seller-performance |
| Configuration values | configuration-register | every document |

## 3. Fixed project constraints

- Launch market is **Iraq**; **Syria and the Gulf** follow as separate markets. The platform is market-ready from day one; nothing for another market is built in v1.0.
- Mobile apps use **Flutter**. React Native is not used.
- **Claude** is the only AI engineering agent. The human owner supervises, decides, approves and validates.
- Design flow: **Stitch → Figma → manual refinement → Claude**. No Figma MCP integration exists. Claude may use computer use to inspect designs and verify results.
- The architecture is a **modular monolith**, **API-first and client-agnostic**; clients hold no business rules.
- **PHP is prohibited.**
- One email address belongs to exactly one account across customer, seller, staff and admin.
- Sellers have a dedicated Seller Dashboard.
- The person who shops is called the **Customer** everywhere: documents, interfaces, APIs and code. "Buyer" is not used.

## 4. Status

Version 7.3 is approved; its approval and change control are recorded in [document-control](00-governance/document-control.md) §1. The technology stack is decided by `docs/adr/0004-technology-stack.md` (D-35 closed). Legal, tax and accounting statements are assumptions until confirmed by counsel and the accountant.
