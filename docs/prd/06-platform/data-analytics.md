# Data Architecture, Analytics & Reporting

**Authoritative for:** data ownership, metric definitions and owners, the analytics pipeline, clickstream, reporting access, the event taxonomy for product analytics.
**Related:** [architecture](architecture.md) · [overview-vision-kpis](../01-product/overview-vision-kpis.md) · [privacy-audit](../05-trust/privacy-audit.md) · [technology-stack](technology-stack.md) §3.11

---

## 1. Data ownership

- DAT-1 PostgreSQL is the system of record; each table is owned by exactly one module ([architecture](architecture.md) §3).
- DAT-2 Derived stores: search index (OpenSearch), cache (Valkey), analytics database, CDN. Each can be rebuilt from the system of record and the event log.
- DAT-3 Reporting never queries operational schemas directly. All analytical access goes through the Analytics module's read models and API.
- DAT-4 Finance reports are produced from the ledger ([ledger-reconciliation](../04-finance/ledger-reconciliation.md)), not from analytics read models. Where a finance figure and an analytics figure differ, the ledger is correct.

## 2. Pipeline

```
operational modules ──outbox──► event_log ──► analytics consumers ──► analytics database (read models, rollups)
clients ──/v1/track──► clickstream intake ──► analytics database (partitioned raw + rollups)
ledger ──nightly extract──► finance summaries
```

- The analytics database is a separate PostgreSQL instance at launch, so reporting load never touches the transactional primary. Migration triggers to a columnar store are in [technology-stack](technology-stack.md) §3.11.
- Analytics consumers are idempotent and ordered per aggregate. Late or out-of-order events are handled by sequence number and a reprocessing queue.
- Read models can be rebuilt by replaying the event log for the period it covers (25 months, EVT-7); aggregates older than that are kept as stored snapshots and are not rebuilt. Operational modules are state-based, not event-sourced.
- Freshness targets: admin operational dashboard within 60 seconds; seller sales analytics within 5 minutes; trend reports hourly; finance summaries daily.

v6 kept real-time KPIs in an in-memory cache "updated on every event"; they are now rollup tables with a short cache in front, which survive restarts and can be audited.

## 3. Clickstream

- Product-analytics events (page and screen views, impressions, clicks, add-to-cart, checkout steps, search queries and result clicks, ad impressions and clicks) are sent by clients to a batching endpoint, never published on the domain event bus.
- One event taxonomy, defined in `packages/contracts/analytics`, is used by the three web apps and the Flutter apps: event name, required properties, platform, app version, pseudonymous user or anonymous ID, session ID, consent state.
- Events are recorded only with analytics consent, except strictly necessary operational measurements (for example ad click validation and fraud signals), which are disclosed in the privacy policy.
- No personal data in event properties. Search queries are stored as typed; queries that look like phone numbers or emails are discarded.
- Bot traffic is filtered at the edge and again by heuristics before rollups.
- Clickstream is P1 except for the pieces P0 features rely on: search query logging (zero-result rate) and order funnel counts derived from server events. Ad impression and click tracking ships with Ads (P1).

## 4. Metric definitions and owners

Every metric is computed per market and carries the market as a dimension. Monetary metrics are in the market's currency; figures in different currencies are never added without an explicit, dated conversion performed for group reporting ([market-expansion](../01-product/market-expansion.md) §3).

| Metric | Definition | Owner | Source |
|---|---|---|---|
| GMV (delivered) | Sum of item value (after seller-funded discounts, before platform-funded discounts) of sub-orders that reached `DELIVERED` in the period | orders | `suborder.delivered` |
| Net GMV | Delivered GMV minus item value refunded in the period | orders + returns | `refund.succeeded` |
| Orders | Count of orders placed that had at least one sub-order delivered | orders | events |
| AOV | Delivered GMV ÷ delivered orders | analytics | derived |
| Monthly active customers (MAC) | Distinct customers with at least one delivered sub-order in the calendar month | orders | events |
| Purchase frequency | Delivered orders ÷ MAC in the month | analytics | derived |
| Active sellers | Approved sellers with at least one live offer and one order in the last 30 days | sellers + orders | events |
| Active listings | Live, approved offers with `available > 0` | catalog + inventory | snapshot |
| Take rate | Commission revenue ÷ 3P delivered GMV | ledger | journal |
| Payment success rate | Succeeded intents ÷ intents that reached `PENDING`, per method | payments | events |
| COD confirmation rate | Confirmed ÷ confirmation requests | risk | events |
| COD RTO rate | COD sub-orders ending `DELIVERY_FAILED` ÷ COD sub-orders shipped | orders + logistics | events |
| On-time delivery | Delivered within the promised estimate ÷ delivered | logistics | events |
| Return rate; dispute rate | Sub-orders with a return (or dispute) ÷ delivered sub-orders | returns | events |
| Seller SLA compliance | Sub-orders meeting both SLAs ÷ sub-orders released to sellers | orders | events |
| Search zero-result rate | Queries with no results ÷ queries | search | query log |
| Loyalty liability | Balance of account 2140 | ledger | journal |
| Fraud-flag and false-positive rates | Flags ÷ orders; overridden flags ÷ flags | risk | events |
| Contribution margin per order | Revenue per order minus variable costs (PSP fees, logistics net of fees, promotions, loyalty, losses) | ledger + analytics | journal |

v6 defined GMV as "completed orders excluding cancelled/returned" without a time basis, so a later return would silently change past months. Delivered GMV is fixed at delivery; refunds are reported in the period they occur.

## 5. Reporting surfaces

| Surface | Audience | Content |
|---|---|---|
| Admin dashboard | Admin roles (widgets by role) | Orders, GMV, payment success, queue sizes, SLA breaches, COD exposure |
| Admin analytics | Per role | Sales, users, sellers, categories, search, payments, logistics; export |
| Seller analytics | Sellers | Own sales, units, orders, conversion, returns, ratings; Buy Box and traffic at P1 |
| Finance reports | Finance, Compliance | Trial balance, reconciliation summaries, payables ageing, funding position, loyalty liability, commission by category |
| Engineering dashboards | Engineering | SLOs, queues, errors ([reliability-sre](reliability-sre.md)) |

- Exports are background jobs, scoped by role and tenant, logged in the audit trail, and neutralise spreadsheet formulas.
- Seller analytics never expose other sellers' figures or customer identities.

## 6. Data quality

- Each read model has a reconciliation check against its source (for example daily delivered GMV in analytics versus the orders module) with an alert on drift.
- Metric definitions live in one place (this section and `packages/contracts/analytics/metrics`); dashboards reference them by key.

## 7. Acceptance criteria

- Rebuilding analytics read models from the event log reproduces the same totals.
- Replaying or reordering events does not change any metric.
- A seller cannot obtain another seller's data through any analytics endpoint.
- With analytics consent declined, no clickstream event is stored for that visitor.
