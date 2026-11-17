# Reliability, Observability, DR, Capacity & Non-Functional Requirements

**Authoritative for:** non-functional requirements, SLOs and error budgets, observability and alerting, incident response, business continuity and disaster recovery, capacity planning.
**Related:** [infrastructure-devops](infrastructure-devops.md) · [technology-stack](technology-stack.md) · [security](../05-trust/security.md) · [testing-quality](../08-engineering/testing-quality.md)

---

## 1. Non-functional requirements

| Area | Requirement | Target | Priority |
|---|---|---|---|
| Web performance | Largest Contentful Paint for Home, Search, Category and PDP, measured from real users in Iraq on mobile | p75 ≤ 2.5 s on 4G | P0 |
| | Interaction to Next Paint; Cumulative Layout Shift | p75 ≤ 200 ms; ≤ 0.1 | P0 |
| API performance | Read endpoints / write endpoints, server time | p95 ≤ 300 ms / ≤ 800 ms | P0 |
| Search | Query latency, server time | p95 ≤ 500 ms | P0 |
| Availability | Storefront and API, monthly, excluding announced maintenance | 99.9% | P0 |
| Scalability | Sustain 10× baseline load for peak events | See §5 | P0 |
| RTL and localisation | Arabic RTL on every page, component, email, SMS and document | 100% | P0 |
| Accessibility | Design-system components meet WCAG 2.2 AA (contrast, focus, keyboard, labels) | Built in | P0 |
| | Full audit of core customer flows against WCAG 2.2 AA | Audit passed | P1 |
| SEO | Server-rendered public pages, structured data, sitemaps, hreflang, canonical URLs | Pass | P1 (structure P0) |
| Security | [security](../05-trust/security.md) baseline; penetration test | Pre-launch | P0 |
| Card data | No card data in Nyazek systems; PSP-hosted entry | SAQ A scope | P0 with cards |
| Privacy | [privacy-audit](../05-trust/privacy-audit.md) | Full | P0 |
| Data integrity | Idempotent financial and order operations; outbox; ledger invariants; stock constraints | Zero silent loss | P0 |
| Audit integrity | Append-only, hash-chained, exported to write-once storage, signed checkpoints | 100% of audited actions | P0 |
| Continuity | Recovery objectives in §4 | Met in drills | P0 |
| Observability | Tracing, metrics, logs, SLO dashboards, alerts | All modules | P0 |
| API compatibility | Versioned, additive within a version, two majors supported, forced-update support | [api-standards](api-standards.md) §2 | P0 |
| Maintainability | Boundary checks, contract tests, coverage thresholds, ADRs | Enforced in CI | P0 |
| Low-bandwidth behaviour | Image variants, compressed payloads, timeouts and safe retries; offline shell for the Storefront | P0; offline shell P1 | – |

Corrections to v6: "page load under 2 seconds on 3G/4G" was not measurable as written and is replaced by Core Web Vitals from real-user monitoring on 4G; 3G is best-effort. WCAG 2.1 is updated to 2.2, and component-level accessibility is P0 because retrofitting it is far more expensive than building it in.

## 2. Service-level objectives

| SLO | Definition | Target (monthly) |
|---|---|---|
| Storefront availability | Successful responses ÷ all requests at the edge for Storefront pages (5xx and timeouts are failures) | 99.9% |
| API availability | Non-5xx responses ÷ all API requests | 99.9% |
| Checkout availability | Non-5xx responses for quote, session, place-order and payment-status endpoints | 99.95% |
| Order integrity | Verified PSP confirmations reflected in order state within 60 s | 99.9% |
| Search latency | Queries answered within 500 ms server time | 95% |
| Web vitals | Page views with LCP ≤ 2.5 s (Iraq, mobile) | 75% |
| Notification hand-off | Transactional messages handed to the provider within 60 s of the triggering event | 99.5% |
| Event delivery | Outbox events dispatched within 10 s | 99.9% |

v6 set "99.9% checkout success" and "99.95% payment success" as SLOs. Customers abandoning checkout and PSPs or banks declining payments are outside Nyazek's control, so those are **monitored business metrics with alerts**, not SLOs. Likewise SMS delivery depends on carriers; the SLO covers hand-off, and delivery rate is monitored.

### 2.1 Error budgets

- Each SLO has a monthly error budget (99.9% ≈ 43 minutes of full unavailability per month).
- Burn-rate alerts: page when the budget is burning at 14.4× over 1 hour or 6× over 6 hours; ticket at 1× over 3 days.
- When a budget is exhausted, feature releases affecting that service pause until reliability work restores it; fixes continue.

## 3. Observability

- **Tracing:** OpenTelemetry in the API, worker, Storefront server and clients (trace context propagated from browser and app). Every log line and event carries the trace or correlation ID.
- **Metrics:** request rate, errors and duration per route and module; queue depth and age; database, cache and search health; business metrics below.
- **Logs:** structured, sampled where high-volume, free of personal data.
- **Errors and crashes:** error tracking for API, web apps and (later) Flutter apps with release tagging and source maps.
- **Real-user monitoring:** web vitals by country, network type and page; this is the source for the web-performance SLO.
- **Synthetic checks:** scripted journeys (home, search, product, add to cart, checkout to payment step, login) every few minutes from outside the cloud. Probes inside Iraq (Baghdad, Erbil, Basra) run from small hosted machines or a monitoring provider that offers Iraqi locations; where none exists, real-user monitoring is the reference.
- Telemetry goes to a managed backend ([technology-stack](technology-stack.md)); dashboards and alert rules are defined in code.

### 3.1 Alerts

| Pages on-call (Sev1–2) | Ticket or business-hours alert |
|---|---|
| SLO burn-rate alerts | Queue backlog (KYC, catalogue, moderation) |
| Ledger invariant failure; reconciliation mismatch of any amount | Search zero-result rate spike |
| Payment success rate for a method drops below its threshold; checkout error spike | Notification delivery rate degradation |
| OTP delivery failure rate above threshold | Slow queries, index bloat |
| Outbox oldest-event age > 60 s; dead-letter growth | Cost budget alerts |
| Courier webhook silence; COD exposure cap exceeded | Certificate or domain expiry (30 days) |
| Sub-orders stuck beyond timers (volume threshold) | Dependency vulnerabilities |
| Database failover, replication lag, storage or connection exhaustion | |
| Audit chain verification failure; backup or restore-test failure | |
| Security patterns (credential stuffing, mass data access) | |

### 3.2 Runbooks

Every paging alert links to a runbook in `docs/runbooks/` with diagnosis steps, safe actions and escalation. Runbooks are reviewed after each incident and each drill.

## 4. Incidents, continuity and disaster recovery

### 4.1 Severity

| Severity | Definition | Response | Communication |
|---|---|---|---|
| Sev1 | Platform down, checkout or payments unavailable, data integrity risk, security breach | Acknowledge within 5 minutes, all hands | Updates every 15 minutes; status page |
| Sev2 | Critical feature degraded (search, login, one payment method, seller order handling) | Acknowledge within 30 minutes | Hourly updates |
| Sev3 | Non-critical degradation (analytics, non-urgent notifications) | Next business day | Ticket |

v6 gave two different Sev2 and Sev3 definitions (one by response time, one by resolution time). This table is the single definition; resolution targets are not promised, recovery objectives are.

- INC-1 Every Sev1 and Sev2 has an incident commander, a timeline and a blameless post-incident review within 5 business days, with tracked actions.
- INC-2 A public status page reports availability and incidents.
- INC-3 On-call requires humans. A 24/7 rota with a 5-minute response needs at least three trained people; the staffing model is decision D-27. Until it is decided, Sev1 response outside staffed hours is best-effort and this is stated in the risk register. The AI agent assists with diagnosis during incidents but is not an on-call responder and does not act on production alone.

### 4.2 Recovery objectives

| Scenario | Recovery point (max data loss) | Recovery time |
|---|---|---|
| Container or node failure | 0 | Automatic, seconds |
| Availability-zone failure | 0 (synchronous standby) | ≤ 15 minutes, automatic |
| Region failure | ≤ 15 minutes target; ≤ 1 hour committed | ≤ 4 hours |
| Accidental data corruption or deletion | To any point within 35 days | ≤ 4 hours for the affected data |
| Loss of cache or search index | None (derived data) | Cache immediate; search rebuild ≤ 2 hours with degraded search meanwhile |

v6 listed a 1-hour recovery point next to "daily backups", which cannot meet it; continuous log archiving and replication are required and specified in [infrastructure-devops](infrastructure-devops.md) §7.

### 4.3 Regional failover

- Stateless services and traffic routing fail over automatically or by a single switch.
- Promoting the database in the DR region is a deliberate, runbook-driven decision by the incident commander, because automatic cross-region promotion risks split-brain and data loss.
- After any failover or point-in-time restore: payouts and automatic refunds stay paused until a full reconciliation against every PSP and courier has run and the ledger invariants pass (REC-5). Payment webhooks received by the edge during the outage are queued and replayed.
- The search index and cache are rebuilt in the DR region; search runs degraded until complete.

### 4.4 Drills

| Drill | Frequency |
|---|---|
| Automated restore test with integrity checks | Monthly |
| Regional failover game-day in staging | Quarterly |
| Production failover rehearsal (controlled) | Before launch, then yearly |
| Incident response tabletop including breach notification | Twice a year |

v6 required both a monthly DR drill and a quarterly restore test; the table above assigns each cadence to a specific exercise.

### 4.5 Business continuity beyond technology

- Provider outage playbooks: PSP down (method hidden, COD continues), SMS primary down (fallback), courier down (fallback courier), edge provider down (documented DNS switch to the alternative path).
- Manual operating procedures for Finance (payout files, refund queue) and Logistics (CSV status and remittance uploads) are part of the P0 scope ([payments](../04-finance/payments.md) §10).

## 5. Capacity planning

### 5.1 Demand model

Load is derived from the KPI targets ([overview-vision-kpis](../01-product/overview-vision-kpis.md)); until D-01 is closed the higher scenario is used for sizing.

| Input | 6-month | 12-month |
|---|---|---|
| Orders per month (MAC × frequency) | 30,000 | 250,000 |
| Average orders per minute | 0.7 | 5.8 |
| Peak-hour factor (evening, ×6) → orders per minute | 4 | 35 |
| Event peak (×10 of peak hour, flash sale) → orders per minute | 40 | 350 |
| Concurrent sessions at peak hour (conversion 1.5%, 6-minute sessions) | ~1,700 | ~14,000 |
| Concurrent sessions at event peak (conversion 3%, 6-minute sessions) | ~8,000 | ~70,000 |
| Search queries per second at event peak (3 searches per session) | ~70 | ~600 |
| Domain events per order (≈ 40 including tracking, stock, notifications) → events per second at event peak | ~30 | ~250 |

v6's sizing table (500 concurrent users, 5 payments per second, but 1,000 events per second at baseline) was not derived from its own targets and overstated event volume by two orders of magnitude, which was the main justification for Kafka. The assumptions above (peak factors, conversion) are placeholders to be replaced by measured data after the beta.

### 5.2 Launch sizing targets

| Component | Launch target | Scaling approach |
|---|---|---|
| API and worker | Handle 100 place-order requests per minute and 100 search queries per second with p95 targets met | Horizontal autoscaling on CPU and request latency; worker scaling on queue age |
| PostgreSQL | Headroom for 10× launch write load; connection budget defined per module pool | Vertical scaling first; read replica for lagging reads; partitioning |
| OpenSearch | 500,000 products, 100 queries per second | Add data nodes; replicas for read scaling |
| Edge cache | ≥ 90% cache-hit ratio for static assets and media; cacheable public HTML with short lifetimes | Cache rules; stale-while-revalidate |
| Queue | 500 jobs per second sustained | Worker concurrency; partitioned job tables |

- CAP-1 Known peaks (Ramadan, Eid, flash sales, campaigns) are pre-scaled at least 60 minutes before start; autoscaling handles the rest.
- CAP-2 Flash-sale protection: queueing or rate shaping on place-order for limited-stock deals; stock contention is safe by construction ([inventory](../02-commerce/inventory.md) RSV-4).
- CAP-3 Back-pressure: every external call has a timeout, bounded retries and a circuit breaker; queues have maximum sizes and shed non-critical work first (analytics, promotional notifications).
- CAP-4 Load test before launch at 10× the 6-month peak hour (launch gate): 40 orders per minute sustained with a 2× burst, 100 search queries per second, with SLOs met and no ledger or stock inconsistency.

### 5.3 Operating complexity

The stack was reduced to what a small team can run: one database engine, one search engine, one cache, managed everywhere, no broker, no self-run observability or log cluster ([technology-stack](technology-stack.md)). Any proposal to add a stateful component needs an ADR with its operating cost.

## 6. Acceptance criteria

- SLO dashboards and burn-rate alerts exist for every SLO before the beta.
- A load test at the CAP-4 profile passes with invariants intact.
- A staged regional failover meets the recovery objectives and the post-failover reconciliation completes cleanly.
- Every paging alert has a runbook.
