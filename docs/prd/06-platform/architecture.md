# Architecture

**Authoritative for:** architecture pattern, module boundaries and ownership, cross-module communication, event catalogue, deployable units.
**Related:** [technology-stack](technology-stack.md) · [api-standards](api-standards.md) · [data-analytics](data-analytics.md) · [infrastructure-devops](infrastructure-devops.md) · [identity-access](../05-trust/identity-access.md)
**Status of technology names:** the pattern, module boundaries, events and rules in this document are requirements. The named technologies are those confirmed by [ADR-0004](../../adr/0004-technology-stack.md) (D-35 closed); the requirements here do not depend on them.

---

## 1. Pattern

Nyazek is a **modular monolith**: one backend codebase, one database server, strict domain boundaries enforced in code and in the database. It is **API-first and client-agnostic**: every capability is exposed through one versioned HTTP API consumed by all clients.

| Principle | Rule |
|---|---|
| ARC-1 One backend | A single NestJS application in `apps/api`. The same container image runs in two roles: `api` (HTTP) and `worker` (outbox dispatcher, jobs, schedulers). No other backend service exists at launch. |
| ARC-2 Domain isolation | Each module owns its tables in its own PostgreSQL schema, its business rules and its public contract. No module reads or writes another module's tables. |
| ARC-3 Contract-only access | Cross-module calls go through the owning module's exported service interface (synchronous, in-process) or through domain events (asynchronous). Importing another module's internals is a build failure. |
| ARC-4 Database-enforced boundaries | Each module connects with its own database role that has privileges only on its own schema. A cross-schema query fails in the database, not only in lint. Cross-module foreign keys are not used; modules reference each other by ID. Platform roles that are not modules (`dispatcher`, `queue_owner`, `backup_reader`) reach module schemas only through execute-only functions or read-only grants, as defined in [ADR-0004](../../adr/0004-technology-stack.md) "Events and jobs across role boundaries" and "Backups". |
| ARC-5 Reliable events | Every domain event is written to the module's outbox table in the same transaction as the state change. Publishing after commit without an outbox is prohibited. Delivery is at-least-once; every consumer is idempotent. |
| ARC-6 Clients hold no business rules | Web and mobile clients render, validate input for usability and call the API. Prices, totals, eligibility, state transitions and permissions are decided only by the API. No client computes money. |
| ARC-7 No client-only capability | A feature ships as API plus client. Nothing depends on Next.js server actions, server-rendered state or browser-only cookies. |
| ARC-8 Anti-corruption layers | Every external provider (PSP, courier, SMS, email, push, maps, storage, search engine) sits behind a port/adapter. Provider identifiers and status codes never appear in domain models. |
| ARC-9 Single source of truth per fact | PostgreSQL is the only system of record. The search index, caches, analytics store and CDN are derived and rebuildable. Loss of the cache or search index must never lose or corrupt business data. |
| ARC-10 Extraction-ready, not extracted | Payments, Ledger, Wallet and Risk keep narrow interfaces so they can be extracted later. Extraction is out of scope for v1.0. |

### Why these corrections were made to v6

- v6 split data across PostgreSQL (commerce) and MongoDB (catalogue content). A product page and its offers could not be changed in one transaction and the two stores could drift. All data now lives in PostgreSQL; flexible attributes use `JSONB` validated against the category attribute schema ([catalog-listings](../02-commerce/catalog-listings.md)).
- v6 used Redis TTL locks for inventory reservations and for carts, sessions and KPI read models. Redis-compatible caches are not durable. Reservations, carts and sessions are now PostgreSQL rows; the cache holds only data that can be lost ([inventory](../02-commerce/inventory.md)).
- v6 named Kafka as the event bus. The planned load (tens of events per second at peak, see [reliability-sre](reliability-sre.md) §5) does not justify operating a broker. The outbox plus a PostgreSQL-backed job queue gives the same guarantees with one fewer system. The `EventBus` port keeps a broker adapter possible.

## 2. Deployable units

| Unit | Technology | Hosts | Notes |
|---|---|---|---|
| `api` | NestJS (role `api`) | `api.<domain>`, and path `/api/*` on each web origin | Stateless; horizontal scaling |
| `worker` | Same image (role `worker`) | none (no inbound traffic) | Outbox dispatch, jobs, schedules, indexers |
| `storefront` | Next.js (SSR/ISR) | `www.<domain>` | Customers and guests; SEO |
| `seller` | Static single-page app | `seller.<domain>` | Seller Dashboard |
| `admin` | Static single-page app | `admin.<domain>` | Admin Panel, behind zero-trust access |
| `mobile-customer`, `mobile-seller` | Flutter | App stores | Post-launch (P2); readiness is P0 ([mobile-flutter](../07-clients/mobile-flutter.md)) |

Platform tasks without inbound traffic (scheduled queue maintenance, the backup and third-location copy task) and edge components (the webhook buffer, the standby edge path) are defined in [ADR-0004](../../adr/0004-technology-stack.md); they hold no business logic.

**Same-origin API path.** The edge routes `https://<app-origin>/api/*` to the `api` unit. Each web app therefore calls the API on its own origin, which lets the API set host-only `__Host-` session cookies per origin without any app-side proxy code and without exposing tokens to browser JavaScript. Mobile apps call `api.<domain>` with bearer tokens. Details: [identity-access](../05-trust/identity-access.md) §6.

## 3. Modules

One NestJS module per row. "Schema" is the PostgreSQL schema name and the module folder name.

| Schema | Module | Owns | Spec |
|---|---|---|---|
| `identity` | Identity | Accounts, identity claims (email/phone), credentials, sessions, tokens, OTP, 2FA, devices | [identity-access](../05-trust/identity-access.md) |
| `customers` | Customers | Customer profile, addresses, favourites, consents, refund accounts | [checkout-orders](../02-commerce/checkout-orders.md), [privacy-audit](../05-trust/privacy-audit.md) |
| `sellers` | Sellers | Seller entity, KYC, store profile, staff and roles, payout destinations, performance score | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md), [seller-performance](../03-sellers/seller-performance.md) |
| `catalog` | Catalog | Categories, attribute schemas, brands, products, variants, offers, price rules, Buy Box | [catalog-listings](../02-commerce/catalog-listings.md), [search-buy-box](../02-commerce/search-buy-box.md) |
| `inventory` | Inventory | Stock counters, reservations, stock movements | [inventory](../02-commerce/inventory.md) |
| `search` | Search | Index documents, ranking configuration, synonyms, query log | [search-buy-box](../02-commerce/search-buy-box.md) |
| `checkout` | Cart & Checkout | Carts, checkout sessions, quotes (price calculation) | [checkout-orders](../02-commerce/checkout-orders.md) |
| `orders` | Orders | Orders, sub-orders, lines, state machine, SLA timers, cancellations | [checkout-orders](../02-commerce/checkout-orders.md) |
| `payments` | Payments | Payment intents, PSP adapters, COD collections, refunds, chargebacks | [payments](../04-finance/payments.md) |
| `ledger` | Ledger | Chart of accounts, journal, balances, invariants, reconciliation | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) |
| `wallet` | Wallet & Payouts | Seller balance views, escrow release, holds, payout runs, statements | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |
| `commission` | Commission | Commission schedule, calculation, reversal | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |
| `invoicing` | Tax & Invoicing | Tax rates, invoices, credit notes, numbering | [tax-invoicing](../04-finance/tax-invoicing.md) |
| `logistics` | Logistics | Couriers, serviceability, shipments, tracking, pickups, COD remittance, geo reference data | [logistics](../02-commerce/logistics.md) |
| `returns` | Returns & Disputes | Returns, inspections, disputes, evidence | [returns-disputes](../02-commerce/returns-disputes.md) |
| `risk` | Risk | Risk scores, rules, cases, blocklists, COD eligibility | [fraud-risk](../05-trust/fraud-risk.md) |
| `reviews` | Reviews & Q&A | Product reviews, seller ratings, Q&A, moderation | [reviews-qa](../02-commerce/reviews-qa.md) |
| `promotions` | Promotions | Coupons, deals, campaigns | [pricing-promotions](../02-commerce/pricing-promotions.md) |
| `loyalty` | Loyalty | Points ledger, tiers, referrals | [loyalty](../02-commerce/loyalty.md) |
| `ads` | Ads | Campaigns, auctions, clicks, billing | [advertising](../02-commerce/advertising.md) |
| `notifications` | Notifications | Templates, preferences, delivery log, device tokens | [notifications-messaging](../02-commerce/notifications-messaging.md) |
| `messaging` | Messaging (P1) | Customer–seller threads per sub-order | [notifications-messaging](../02-commerce/notifications-messaging.md) |
| `media` | Media | Upload pipeline, scanning, variants | [catalog-listings](../02-commerce/catalog-listings.md) §8 |
| `content` | Content (CMS) | Static pages, banners, home sections, help articles | [support-cms](../02-commerce/support-cms.md) |
| `support` | Support | Tickets | [support-cms](../02-commerce/support-cms.md) |
| `analytics` | Analytics | Read models, reporting API, clickstream intake | [data-analytics](data-analytics.md) |
| `backoffice` | Backoffice | Admin users, roles, permissions, dual-control approvals, platform and market configuration, feature flags | [admin-governance](../05-trust/admin-governance.md) |
| `audit` | Audit | Append-only audit trail, hash chain, exports | [privacy-audit](../05-trust/privacy-audit.md) |

Shared kernel (no schema, no business state): `packages/contracts` types, the Money value object, IDs, clock, error model, the outbox/inbox library and the port interfaces.

### 3.1 Dependency rules

- Synchronous calls are allowed only "downward" in this order, never in a cycle: *experience* modules (checkout, search, content, support, notifications) → *commerce* modules (orders, catalog, inventory, promotions, loyalty, returns, reviews, ads, logistics, sellers, customers) → *finance and trust* modules (payments, wallet, commission, invoicing, ledger, risk) → *foundation* (identity, backoffice, audit, media).
- A lower layer never calls a higher layer; it publishes an event instead.
- A synchronous call may be used only when the caller needs the answer to complete its own transaction (for example checkout asking Inventory to reserve stock). Everything else is event-driven.
- Analytics and Search consume events only; no module calls them for writes.

### 3.2 Cross-module transactions

Each module commits its own transaction. Flows that span modules (place order, cancel, refund, release escrow) are **sagas**: an ordered set of local transactions connected by events, each step idempotent, each with a defined compensation. The saga for each flow is specified in the owning document (place order: [checkout-orders](../02-commerce/checkout-orders.md) §5; refund: [returns-disputes](../02-commerce/returns-disputes.md) §5; release: [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §3).

Exceptions (the only two):

1. **Ledger posting.** The Ledger exposes `post(journalEntry)` that the finance modules `payments`, `wallet`, `commission`, `loyalty` and `ads` call inside their own transaction through a shared transaction handle, so that a state change and its journal entry commit atomically. Inside the database this is a posting function owned by the ledger role and granted (execute only) to those modules' roles; their roles still have no table privileges on the ledger schema, so ARC-4 holds. Modules outside that list that originate financial events (`orders`, `returns`, `logistics`, `inventory` for 1P stock) never post: they emit an event, and the finance module that owns the money movement posts the entry idempotently from it (refunds by `payments`, seller charges and courier compensation by `wallet`, 1P goods receipts and stock adjustments by the `ledger` consumer itself).
2. **Audit append.** Every module writes its audit records in its own transaction (AUD-5) through an append function owned by the audit role and granted (execute only) to every module role.

Outside business transactions, the outbox dispatcher reads each module's outbox only through execute-only functions granted to the platform role `dispatcher` ([ADR-0004](../../adr/0004-technology-stack.md) "Events and jobs across role boundaries"). This is not a third exception: it never joins a module's business transaction.

## 4. Events

### 4.1 Envelope

```json
{
  "eventId": "uuidv7",
  "type": "suborder.delivered",
  "version": 1,
  "occurredAt": "2027-01-15T09:30:00Z",
  "producer": "orders",
  "aggregateType": "suborder",
  "aggregateId": "uuid",
  "sequence": 12,
  "correlationId": "uuid",
  "causationId": "uuid",
  "actor": { "type": "system|customer|seller|admin|courier|psp", "id": "uuid|null" },
  "payload": {}
}
```

Rules:

- EVT-1 Names are `<aggregate>.<past_tense_verb>`, lower snake case.
- EVT-2 Payloads carry IDs and facts, never raw personal data (no names, phones, emails, addresses, document numbers).
- EVT-3 Changes within a version are additive; consumers ignore unknown fields; a breaking change creates `version + 1` and both versions are published during migration.
- EVT-4 Ordering is guaranteed per aggregate (`sequence`), not globally. Consumers that need order process one aggregate at a time and park out-of-order events.
- EVT-5 Consumers record `(consumer, eventId)` in an inbox table in the same transaction as their side effect.
- EVT-6 Failed handling retries with exponential backoff (max `cfg:events.max_attempts` (default 10)), then moves to a dead-letter table that raises an alert.
- EVT-7 All events are retained in an append-only `event_log` (partitioned by month) for `cfg:events.retention_months` (default 25) to allow read-model rebuilds.
- EVT-8 Outbox dispatch latency target: p95 under 2 seconds; outbox age over 60 seconds pages on-call.
- EVT-9 Every event about a market-scoped aggregate (order, offer, shipment, payment, journal entry, seller) carries the market code in its payload, and every amount carries its currency (MKT-4).

### 4.2 Catalogue (launch set)

| Event | Producer | Key payload fields |
|---|---|---|
| `account.registered`, `account.verified`, `account.closed` | identity | accountId, realm |
| `seller.kyc_submitted`, `seller.kyc_decided`, `seller.status_changed` | sellers | sellerId, from, to, reasonCode |
| `seller.performance_level_changed` | sellers | sellerId, fromLevel, toLevel, score |
| `product.published`, `product.updated`, `product.unpublished` | catalog | productId, variantIds |
| `offer.created`, `offer.price_changed`, `offer.status_changed` | catalog | offerId, sellerId, variantId, price |
| `buybox.winner_changed` | catalog | variantId, fromOfferId, toOfferId |
| `stock.changed` | inventory | offerId, available, reason |
| `stock.reserved`, `stock.released`, `stock.allocated` | inventory | offerId, qty, checkoutSessionId or subOrderId |
| `order.placed` | orders | orderId, customerId, subOrderIds, paymentMethod, totals |
| `order.expired`, `order.completed`, `order.cancelled`, `order.closed` | orders | orderId |
| `suborder.released_to_seller`, `suborder.confirmed`, `suborder.ready_to_ship`, `suborder.shipped`, `suborder.out_for_delivery`, `suborder.delivered`, `suborder.completed`, `suborder.delivery_failed`, `suborder.rto_in_transit`, `suborder.rto_received`, `suborder.lost`, `suborder.cancelled` | orders | subOrderId, sellerId, at, reasonCode where relevant |
| `suborder.sla_breached` | orders | subOrderId, sellerId, stage (confirm or ship) |
| `payment.succeeded`, `payment.failed`, `payment.expired`, `payment.unallocated_received` | payments | paymentId, orderId, amount, method |
| `cod.collected`, `cod.not_collected`, `cod.exception_opened`, `cod.written_off` | payments | subOrderId, shipmentId, amount |
| `cod.remitted` | logistics | remittanceId, courierId, shipmentIds, amount |
| `refund.requested`, `refund.awaiting_destination`, `refund.succeeded`, `refund.failed`, `refund.manual_review`, `refund.returned`, `refund.cancelled` | payments | refundId, subOrderId (none for PAY-20 refunds), amount, destinationType |
| `chargeback.opened`, `chargeback.evidence_submitted`, `chargeback.resolved` | payments | chargebackId, paymentId, amount, outcome (won, lost, accepted) |
| `escrow.released` | wallet | subOrderId, releaseSeq, sellerId, lines, gross, commission, net |
| `wallet.hold_placed`, `wallet.hold_released` | wallet | sellerId, amount, reference |
| `payout.created`, `payout.rejected`, `payout.executed`, `payout.failed`, `payout.returned`, `payout_run.status_changed` | wallet | payoutId or runId, sellerId, amount |
| `shipment.created`, `shipment.tracking_updated`, `pickup.scheduled`, `pickup.failed` | logistics | shipmentId, subOrderId, courierId, status |
| `return.requested`, `return.approved`, `return.rejected`, `return.received`, `return.inspected`, `return.contested`, `return.in_dispute`, `return.accepted`, `return.closed` | returns | returnId, subOrderId, lineIds, outcome |
| `dispute.opened`, `dispute.resolved`, `dispute.review_requested`, `dispute.closed`, `dispute.withdrawn` | returns | disputeId, subOrderId, returnId where linked, outcome, amount |
| `risk.assessed`, `risk.flag_raised`, `risk.override_applied` | risk | subjectType, subjectId, tier |
| `review.published`, `review.removed` | reviews | reviewId, productId or sellerId, rating |
| `coupon.redeemed`, `coupon.reversed` | promotions | couponId, orderId, amount, funder |
| `loyalty.points_earned`, `loyalty.points_redeemed`, `loyalty.points_reversed`, `loyalty.points_expired` | loyalty | accountId, points, reference |
| `ad.click_validated`, `ad.spend_billed` | ads | campaignId, sellerId, amount |
| `invoice.issued`, `credit_note.issued` | invoicing | documentId, number, subOrderId |
| `notification.requested` | any module | templateKey, recipientAccountId, data |

The schema for each payload lives in `packages/contracts/events` and is the source for generated types and consumer tests.

## 5. Scheduled and background work

All jobs run in the `worker` role through the PostgreSQL-backed queue. Each job is idempotent, has a timeout and an owner module.

| Job | Owner | Schedule |
|---|---|---|
| Outbox dispatch | shared | Continuous |
| Reservation expiry sweep | inventory | Every 30 s |
| SLA timers (confirm, ship, handover, COD confirmation, payment deadline) and return, dispute and RTO timers | orders, returns, logistics | Timer per sub-order, plus sweep every minute |
| Escrow release | wallet | Every 15 min |
| Payment status polling (pending intents) | payments | Every minute while pending |
| PSP settlement and COD remittance reconciliation; COD remittance overdue check | ledger, payments | Daily, plus on file arrival |
| Ledger invariant check | ledger | Every 5 min (lightweight), full trial balance daily |
| Performance score recompute | sellers | Hourly |
| Buy Box recompute | catalog | On events, plus max interval `cfg:buybox.max_interval_minutes` (default 15) |
| Search index sync | search | On events; full reindex on demand |
| Payout run | wallet | Per payout schedule |
| Points expiry, tier evaluation | loyalty | Daily |
| Audit export and checkpoint signing | audit | Hourly export, daily signature |
| Analytics rollups | analytics | Every 5 min and nightly |
| Document expiry reminders (KYC, licences) | sellers | Daily |

## 6. Time, identifiers and money

- All timestamps are stored in UTC (`timestamptz`) and displayed in the market's time zone (`Asia/Baghdad`, UTC+3, no daylight saving, for Iraq).
- Internal IDs are UUIDv7. Public order numbers are short, non-guessable and human-readable ([checkout-orders](../02-commerce/checkout-orders.md) ORD-1).
- Money is an integer amount in the platform minor unit of its currency with an explicit currency code (IQD at launch) ([ledger-reconciliation](../04-finance/ledger-reconciliation.md) §2).
- **Market** is a first-class dimension ([market-expansion](../01-product/market-expansion.md) §2–3). Currency, locale, country, time zone and tax region are explicit fields resolved from market configuration (`IQD`, `ar-IQ`, `IQ`, `Asia/Baghdad`, `IQ-0` for Iraq), never literals in business logic (MKT-9). Only the Iraq market is enabled at launch; whether a later market shares this deployment or runs separately is decided per market at entry (D-39, decided), and module boundaries must allow both.

## 7. Acceptance criteria

- A CI check fails the build when a module imports another module's internals.
- An integration test proves a module's database role cannot select from another module's schema.
- Killing the `worker` between a state change and event dispatch loses no event (outbox test).
- Delivering any event twice causes no duplicate side effect (consumer idempotency test per consumer).
- Stopping the cache and the search engine leaves checkout, order management and ledger operations correct (degraded performance and search unavailability are acceptable).
