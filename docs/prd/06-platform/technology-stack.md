# Technology Stack

**Authoritative for:** the reasons behind Nyazek's technology choices (selection criteria, justification of significant changes, retained choices, cost profile). The decision itself is [ADR-0004](../../adr/0004-technology-stack.md); the living list of components and versions is `docs/architecture/foundation.md` once it exists.
**Related:** [architecture](architecture.md) · [infrastructure-devops](infrastructure-devops.md) · [mobile-flutter](../07-clients/mobile-flutter.md) · [claude-workflow](../08-engineering/claude-workflow.md)
**Status:** the stack was decided on 17 November 2026 by [ADR-0004](../../adr/0004-technology-stack.md) (D-35 closed). Where this document and ADR-0004 differ, ADR-0004 wins. The prohibition of PHP and the choice of Flutter are owner mandates and are final.

---

## 1. Selection criteria

1. Fits Nyazek's real scale: tens of orders per minute at peak, hundreds of thousands of offers, a small human team and one AI engineering agent.
2. Fewest moving parts that still meet the requirements. Every additional datastore or service must pay for its operating cost.
3. Mature, actively maintained, with a managed offering available.
4. Works for Arabic/RTL, for Iraqi networks and for an API shared by web and Flutter clients.
5. **PHP is prohibited** anywhere in the project: no PHP code, frameworks, libraries, or self-hosted PHP products (for example WordPress, Magento, Matomo, phpMyAdmin). Any future tool proposal is checked against this rule.

Rules elsewhere in the PRD that name a technology (for example a database feature behind a ledger invariant) bind their **intent**; the means is the stack confirmed by ADR-0004, and an equivalent mechanism in that stack satisfies the rule.

Version policy: exact versions are pinned by lockfiles and container digests, updated by an automated dependency bot, and never hand-pinned in this document. Use the current LTS or stable release at kickoff unless a listed constraint says otherwise.

## 2. Stack

The confirmed stack, layer by layer, is in [ADR-0004](../../adr/0004-technology-stack.md) §Decision; exact versions are recorded in `docs/architecture/foundation.md` (T-0022). This section previously held the proposal that ADR-0004 confirmed.

## 3. Justification of significant changes

Each entry answers: problem solved, why better than v6, advantages and disadvantages, compatibility, operating complexity and cost.

### 3.1 MongoDB → PostgreSQL JSONB

- **Problem.** v6 kept canonical product content in MongoDB and offers, prices and stock in PostgreSQL. Publishing a product together with its first offer, merging duplicates, or deleting a product could not be atomic, and every listing page needed two stores.
- **Why better.** `JSONB` with GIN indexes stores per-category attributes with the same flexibility; attribute documents are validated against the category schema in the application. One store, one transaction, one backup, one access model.
- **Advantages.** Removes a datastore, a driver, a backup regime and a class of consistency bugs. **Disadvantages.** Very large or deeply nested documents are less ergonomic than in a document database; not relevant for product attributes.
- **Compatibility.** Search and filters are served by OpenSearch, not by the catalogue store, so attribute query flexibility in the primary store is not a constraint.
- **Operations and cost.** Lower: one fewer managed cluster.

### 3.2 Kafka → transactional outbox + pg-boss (D-17, decided by ADR-0004)

- **Problem.** Modules need reliable asynchronous events and background jobs. v6 specified Kafka and a Kafka-compatible broker in development.
- **Why better.** Realistic event volume is far below what PostgreSQL handles comfortably ([reliability-sre](reliability-sre.md) §5). pg-boss stores jobs in PostgreSQL, so enqueueing a job or event is part of the business transaction, which is exactly the outbox guarantee. Retries, backoff, scheduling, dead-lettering and singleton jobs are built in.
- **Advantages.** No broker to run, identical semantics in local, CI and production, transactional enqueue. **Disadvantages.** Not suitable for very high throughput or for many independent consuming services; queue tables need routine maintenance (partitioning, archiving).
- **Compatibility.** Modules depend on the `EventBus` and `JobQueue` ports. A Kafka or managed-queue adapter can be added when a module is extracted or when sustained volume exceeds roughly 500 events per second.
- **Operations and cost.** Lower. Monitor queue depth, oldest-job age and table bloat.

### 3.3 Redis as a system of record → Valkey as a cache only

- **Problem.** v6 placed inventory reservations, carts, sessions and KPI read models in Redis. A cache failover can lose recent writes, which for reservations means overselling or orphaned holds.
- **Why better.** Reservations, carts and sessions are PostgreSQL rows (correct by construction). Valkey holds only rate-limit counters, short-lived caches (catalogue fragments, Buy Box lookups, configuration) and pub/sub fan-out for server-sent events.
- **Rule.** Nothing in the cache is a system of record. A cold or missing cache affects latency only.
- **Why Valkey.** Open-source (BSD), protocol-compatible with Redis clients, offered as a managed service, and avoids Redis licensing changes. **Cost.** A small managed instance; can be omitted in local development.

### 3.4 Elasticsearch / OpenSearch → OpenSearch (managed)

- **Problem.** v6 left the engine ambiguous. Search needs an Arabic analyser with custom normalisation, synonyms, facets, autocomplete, multi-signal ranking and sponsored blending.
- **Why OpenSearch.** Apache-2.0 licence, managed offerings, full control of analysis chains and function scoring, and vector search available later for semantic ranking. Lighter engines (Typesense, Meilisearch) were considered: simpler to run but with less control over Arabic analysis and custom scoring, which are core to Section [search-buy-box](../02-commerce/search-buy-box.md).
- **Disadvantages.** The heaviest component in the stack: a multi-node JVM cluster with its own cost. Mitigation: managed service, small data volume, and the `SearchPort` adapter keeps the engine replaceable.
- **Version note.** OpenSearch 3.x requires JDK 21 and Lucene 10; start on 3.x to avoid an early major upgrade.

### 3.5 Data access: Kysely with SQL migrations

- **Problem.** v6 did not choose an ORM, yet required one schema per module, separate database roles, partial unique indexes (identity claims), check constraints (non-negative stock, balanced journals) and append-only tables.
- **Why Kysely.** A typed SQL query builder: queries are explicit SQL with compile-time types generated from the database, and migrations are plain SQL, so every PostgreSQL feature is available without workarounds. This suits a ledger-centric system where the database enforces invariants.
- **Alternatives considered.** Drizzle ORM matches the requirements but its 1.0 line was still at release-candidate stage at review time. Prisma is mature but its schema language does not natively express several constraints used here, which would force hand-edited migrations. Either may be reconsidered by ADR.
- **Disadvantages.** No automatic relation loading or change tracking; repositories are written by hand. Acceptable: explicit queries are easier to review in financial code.
- **Rule.** One migration folder and one connection pool (with its own role) per module.

### 3.6 Seller Dashboard and Admin Panel as static single-page apps

- **Problem.** v6 built all three web apps on Next.js with a server-side proxy in each for cookies. The two dashboards need no SEO or server rendering, and a server runtime in each invites business logic to leak into server code.
- **Why better.** Vite-built React SPAs are static files on the CDN: no server to run, scale or patch, a much smaller attack surface for the Admin origin, and it is structurally impossible to bypass the API. Session cookies are set by the API through the same-origin `/api` path ([architecture](architecture.md) §2).
- **Advantages.** Two fewer server deployments; simpler CSP. **Disadvantages.** Two build systems in the monorepo (Next.js and Vite); mitigated by the shared `ui-web`, `contracts`, `api-client` and `i18n` packages and by identical lint and test tooling.
- **Storefront stays on Next.js** because public pages need server rendering, caching and structured data for SEO and fast first paint on slow networks.

### 3.7 React Native + Expo → Flutter

- **Reason.** Owner mandate. Flutter also gives consistent Arabic text shaping and RTL layout across Android versions, a single rendering engine, and runtime direction switching without an app restart.
- **Consequence.** TypeScript packages cannot be shared with the apps. Sharing moves to language-neutral artefacts: the OpenAPI contract (generated Dart client), design tokens (generated Dart theme), i18n catalogues (generated ARB files) and shared test vectors. Details: [mobile-flutter](../07-clients/mobile-flutter.md).
- **Cost.** A second language (Dart) in the repository and macOS runners for iOS builds.

### 3.8 CloudFront + AWS WAF → Cloudflare at the edge

- **Problem.** First-paint time for Iraqi users depends mostly on edge proximity. v6 planned CloudFront.
- **Why better.** Cloudflare operates points of presence inside Iraq (public listings show Baghdad, Basra, Erbil, Najaf, Nasiriyah and Sulaymaniyah), which shortens TLS and cache-hit latency for in-country users. The same platform provides WAF, bot management, rate limiting, Turnstile and zero-trust access for the Admin origin.
- **Disadvantages.** A second infrastructure vendor and an extra hop to the origin for uncached requests. The edge must be validated by latency measurement from Iraqi networks in delivery Phase 1, Foundation; the `CdnPort`, DNS in Route 53 and the standby CloudFront path of ADR-0004 keep a fallback to another CDN possible.

### 3.9 Kubernetes → ECS on Fargate

- **Problem.** D-18 left the container platform open; ADR-0004 closed it with this choice. The system has three container deployables (`api`, `worker`, `storefront`) and two static apps (ADR-0004).
- **Decision.** A managed container service without cluster management. **Disadvantages.** Less portable than Kubernetes and fewer ecosystem tools; acceptable at this size. Revisit if the team gains Kubernetes skills and a need for it.

### 3.10 Region

- **Fact check.** Public reporting in 2026 confirms that AWS facilities in the UAE and Bahrain were physically damaged in March 2026 and that, as of mid-September 2026, AWS stated it could not restore resources held only in Bahrain or in one UAE availability zone.
- **Decision.** No Middle East cloud region may be the sole location of any production data or backup. Recommended: primary in a European region, DR in a second European region, immutable backups copied to a third location with a different provider. The legal meaning of "Iraqi data residency" is defined with counsel (INF-8, tracked in T-0015).

### 3.11 Analytics store deferred

- **Problem.** v6 required ClickHouse or BigQuery from Phase 3.
- **Decision.** Launch with a separate PostgreSQL analytics database (partitioned event and clickstream tables, rollups). Move clickstream and heavy aggregates to ClickHouse Cloud when either trigger is met: more than 50 million analytics events per month, or seller-analytics p95 query time above 2 seconds after tuning. The Analytics module API does not change.

### 3.12 Audit and observability

- v6 mixed the immutable business audit trail with operational logging on ELK. They are now separate: the audit trail is an append-only PostgreSQL schema exported to object-locked storage ([privacy-audit](../05-trust/privacy-audit.md) §5); operational telemetry goes through OpenTelemetry to a managed backend ([reliability-sre](reliability-sre.md) §3). This removes a self-run ELK cluster and a self-run Prometheus stack.

### 3.13 In-house identity retained

- Off-the-shelf identity servers were considered. The owner rule "one email, one account across customer, seller, staff and admin realms", phone-OTP login, guest checkout binding and realm-scoped sessions are easier and safer to implement in one module than to bend a multi-realm identity server to. No cryptography is hand-written: password hashing, token signing, TOTP and WebAuthn use maintained libraries.

### 3.14 Arabic PDF documents

- Invoices, statements, packing slips and labels contain Arabic. PDF libraries that draw text directly often break Arabic shaping and bidirectional text. Rendering HTML templates with headless Chromium uses the same text engine as the browser and the same fonts as the design system. Cost: a Chromium binary in the worker image.

### 3.15 Local object storage emulator

- v6 used MinIO in the local stack. Its community edition entered maintenance mode in December 2025 and the repository was later archived. The Dev Container uses a maintained S3-compatible emulator (SeaweedFS or Garage) instead.

## 4. Retained choices and why

| Choice | Reason to keep |
|---|---|
| TypeScript + NestJS | Module system maps one-to-one to domain modules; shared types with web clients; first-class schema validation with Zod in NestJS 12; strong fit for AI-assisted development with strict typing |
| PostgreSQL | Transactions, constraints and row-level locking are exactly what orders, inventory and the ledger need |
| REST + OpenAPI | One contract for web and Flutter with generated clients; simpler caching and tooling than GraphQL for this product |
| pnpm + Turborepo | Fast, cache-aware builds for the TypeScript workspace |
| GitHub Actions | Sufficient; macOS runners available for iOS |
| VS Code Dev Containers | Owner mandate; the same image is used by humans, Claude and CI |

## 5. Version and compatibility notes

Versions and compatibility were re-verified in [ADR-0004](../../adr/0004-technology-stack.md) §Verification; exact versions in force are recorded in `docs/architecture/foundation.md` (T-0022).

## 6. Operating cost profile (qualitative)

| Component | Relative cost | Scales with |
|---|---|---|
| PostgreSQL primary + replica + analytics instance | High | Storage, connections |
| OpenSearch cluster | High | Index size, query rate |
| Containers (`api`, `worker`, `storefront`) | Medium | Traffic |
| Cloudflare plan with WAF and bot management | Medium | Plan tier |
| SMS | Medium to high, variable | OTPs and transactional messages; the largest variable cost |
| Observability and error tracking | Medium | Telemetry volume; sample traces |
| Valkey, S3, SES, static hosting | Low | Usage |

A costed estimate is a deliverable of delivery Phase 1, Foundation, once the region (D-06) and vendors (D-11, D-28, D-29) are chosen.

## 7. Sources

The sources for the version and fact checks are listed in [ADR-0004](../../adr/0004-technology-stack.md) §Sources. The fact check on Middle East cloud regions (§3.10) used: [Khaleej Times](https://www.khaleejtimes.com/tech/amazon-aws-unable-restore-access-bahrain-one-uae-cloud-data-zone), [TeleGeography](https://resources.telegeography.com/war-middle-east-damaged-data-centers-cloud-disruptions).
