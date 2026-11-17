# ADR-0004: Technology stack

- **Status:** Accepted (owner, 2026-11-17)
- **Date:** 2026-11-17
- **Decided by:** Owner
- **Task:** T-0020
- **Closed on acceptance:** D-35 (stack as a whole), D-16 (separate origins), D-17 (event broker and timing), D-18 (container platform) in [open-decisions](../prd/00-governance/open-decisions.md) §4

## Context

The PRD proposes a stack in [technology-stack](../prd/06-platform/technology-stack.md) and states that no named technology binds until the owner closes D-35 in the architecture phase. ADR-0002 §4 makes this decision a condition for opening the architecture phase: `foundation.md` and the module specifications are written against the stack chosen here. T-0020 is therefore the phase's entry step; it prepares D-35, and the rest of Phase 2 starts only after the owner closes it. T-0020 asks for three things. First, re-verify the proposed stack against current versions and support. Second, check it against the AI-agent workflow, Flutter and the ban on PHP. Third, give options and a recommendation per layer, so that every PRD platform requirement maps to a component.

This ADR does not restate why each PRD choice was made; [technology-stack](../prd/06-platform/technology-stack.md) §3 holds the reasoning and stays the authority for it. This ADR records what was verified, what changes, what was missing, and the mapping.

## Decision drivers

Sources: the selection criteria in [technology-stack](../prd/06-platform/technology-stack.md) §1, the PRD rules cited in each item, and the standing owner decisions in `CLAUDE.md`.

1. Real scale ([technology-stack](../prd/06-platform/technology-stack.md) §1, [reliability-sre](../prd/06-platform/reliability-sre.md) §5): tens of orders per minute at peak, with a pre-launch load test at 40 orders per minute sustained and 100 search queries per second (CAP-4); a small human team and one AI engineering agent.
2. Fewest moving parts that meet the requirements (§1 criterion 2). Every stateful component is a managed service ([infrastructure-devops](../prd/06-platform/infrastructure-devops.md) INF-1).
3. Mature, maintained, with a managed offering.
4. Arabic and RTL, Iraqi networks, one API shared by web and Flutter.
5. Owner mandates: no PHP anywhere; Flutter for mobile; modular monolith, API-first and client-agnostic; market-ready for Syria and the Gulf (`CLAUDE.md`); Claude as the only AI agent and VS Code Dev Containers (technology-stack §2 and §4).
6. Strict typing and explicit SQL, so that an AI agent's changes are reviewable and financial invariants are enforced by the database (technology-stack §3.5 and §4; a driver of this ADR, not a PRD rule).

## Verification (17 November 2026)

Each proposed version was checked against current public sources. Results:

| Component | PRD proposal | Status found | Consequence |
|---|---|---|---|
| Node.js | 26 LTS | 26.x promoted to LTS on 28 October 2026 ("Lithium"), end of life April 2029. Node.js 26 is the last release under the even-numbers-only LTS model | Confirmed. Node.js 24 LTS stays the fallback if a dependency lags |
| NestJS | 12 (ESM) | 12.0.0 released August 2026; 12.x patch releases through October 2026; Standard Schema validation on route decorators; no end-of-life date announced | Confirmed |
| PostgreSQL | 18 | Amazon RDS for PostgreSQL has supported 18 since November 2025 (18.4 in May 2026). PostgreSQL 19 general availability is planned for 19 November 2026 | Confirmed: start on 18. Adopt 19 only under the PRD rule (managed service offers it and one minor release has shipped) |
| Kysely | query builder | 0.29.x current (October 2026), ESM-only, Node.js 22+; maintenance line 0.28.x. Several 2026 CVEs, in MySQL and SQLite JSON-path compilation and fixed in 0.28.12 and 0.28.17 | Confirmed. Use the latest 0.29.x patch; never a version below 0.28.17. Still pre-1.0 (see risks) |
| Drizzle ORM (alternative) | not chosen | 1.0 still at release-candidate stage (rc.4 to rc.5, with breaking changes between candidates); stable line 0.45 | Reason for not choosing it still holds |
| pg-boss | job queue | 12.26.x (July 2026), Node.js 22.12+, schema migrates automatically on start | Confirmed |
| OpenSearch | 3.x managed | Amazon OpenSearch Service supports up to 3.7 (July 2026) | Confirmed: start on the newest 3.x the managed service offers |
| Next.js | 16 | 16.x current (16.0 October 2025, 16.2 March 2026, security batch fixed in 16.2.6, May 2026; the newest evidence found is from mid-2026) | Confirmed. Use the latest 16.x patch at kickoff; never a version below 16.2.6. T-0022 re-checks for a newer major |
| Flutter | latest stable | 3.50 with Dart 3.14 stable; the official 3.50.0 release-notes page exists, and the date (11 November 2026) comes from a secondary source | Confirmed; N-1 upgrade cadence as in the PRD |
| MinIO (local) | replaced | Community edition archived (PRD §3.15) | PRD position holds |

Not re-checked here, because no evidence suggests a change and their versions are fixed by lockfiles at kickoff: React 19, Vite, TanStack, Tailwind CSS 4, Radix UI, Zod 4, Valkey, Turborepo, pnpm, OpenTofu, Playwright, Vitest. T-0022 records the exact versions in force when the repository skeleton is created.

**Compatibility check.** Node.js 26 meets the floors of NestJS 12, Kysely 0.29 (Node.js 22+) and pg-boss 12 (Node.js 22.12+). The whole backend is ESM, which NestJS 12 and Kysely 0.29 require. PostgreSQL 18 provides native `uuidv7()` for keys.

**Mandate check.** No component is written in PHP or is a PHP product. Mobile is Flutter. The backend is one NestJS application with two roles (ARC-1), so the modular-monolith mandate holds. Claude Code runs in the Dev Container and CI, which use the same image.

## Decision

Adopt the stack in [technology-stack](../prd/06-platform/technology-stack.md) §2 as proposed, with the version floors from the verification above, and add the components in "Gaps filled" below, which the PRD requires but does not name. Per layer:

| Layer | Recommendation | Options considered | Why the recommendation |
|---|---|---|---|
| Backend language and runtime | TypeScript (strict), Node.js 26 LTS | Kotlin/JVM, Go, C#/.NET | One language with the web clients and `packages/contracts`; strict types suit AI-written code; the PRD reasoning (§4) holds |
| Backend framework | NestJS 12, ESM | Fastify with hand-built modules; Hono | NestJS modules map one-to-one to domain modules (ARC-2, ARC-3); Zod validation through Standard Schema |
| Contracts | Zod 4 in `packages/contracts`, OpenAPI 3.1 generated, `oasdiff` in CI | Hand-written OpenAPI; TypeSpec | One source for validation, types and the contract (API-3 to API-5) |
| System of record | PostgreSQL 18, Amazon RDS, Multi-AZ with synchronous standby, cross-region read replica in the DR region | Aurora PostgreSQL; self-run on containers (excluded by INF-1) | RDS Multi-AZ meets the zero-loss AZ objective and supports PostgreSQL 18; Aurora is a valid later option if read scaling or failover time demands it, with no application change. T-0022 chooses between the Multi-AZ instance and Multi-AZ cluster shapes by failover time and PostgreSQL 18 availability |
| Catalogue content | PostgreSQL `JSONB` validated against the category schema | MongoDB (v6) | One store and one transaction (technology-stack §3.1) |
| Data access | Kysely, plain SQL migrations per module | Drizzle (1.0 not stable), Prisma (constraints need hand-edited migrations), raw `pg` | Explicit SQL with generated types; every PostgreSQL constraint available (§3.5) |
| Jobs and events | Transactional outbox per module + pg-boss on PostgreSQL, wired as in "Events and jobs across role boundaries" below | Kafka, SQS/SNS, RabbitMQ | The event or job request commits with the state change (ARC-5); volume far below PostgreSQL limits; `EventBus` port keeps a broker adapter possible. Closes D-17 |
| Cache | Valkey, Amazon ElastiCache, cache only | Redis (licence), none | Rate limits, short caches, server-sent-event fan-out; nothing stored there is a system of record (§3.3) |
| Search | OpenSearch 3.x, Amazon OpenSearch Service | Typesense, Meilisearch, PostgreSQL full-text | Arabic analysis chains and function scoring (§3.4); `SearchPort` keeps it replaceable |
| Object storage | Amazon S3, versioning, cross-region replication, Object Lock for audit | – | Required by BKP and AUD-3 |
| Edge | Cloudflare (CDN, WAF, bot management, rate limiting, Turnstile, zero-trust for Admin); authoritative DNS in Route 53 and a CloudFront standby path ("Edge provider outage"), a change from PRD §2, which puts DNS on Cloudflare | CloudFront + AWS WAF as the only edge | Points of presence inside Iraq (§3.8); latency is measured in delivery Phase 1 before go-live (INF-6) |
| Compute | Amazon ECS on Fargate, two availability zones, behind an Application Load Balancer | EKS (Kubernetes), App Runner | No cluster to operate for three container deployables (`api`, `worker`, `storefront`). Closes D-18 |
| Cloud and region | AWS; primary and DR in two European regions per D-06 (closed) | Other clouds | Matches INF-5 and INF-6; the specific regions are chosen from the latency measurement in delivery Phase 1, Foundation, of the [release-plan](../prd/00-governance/release-plan.md) (`eu-central-1` stays the working assumption) |
| Storefront | Next.js 16 App Router, React 19 | Remix / React Router 7, Astro | Server rendering and caching for SEO and first paint on slow networks (§3.6) |
| Seller Dashboard, Admin Panel | React 19 SPAs, Vite, TanStack Router, hosted as Cloudflare static assets (Workers static assets) | Next.js; S3 bucket as origin behind Cloudflare | No server runtime; the API cannot be bypassed (§3.6). Cloudflare hosting gives atomic deploys with the previous version kept (REL-6) and per-branch previews, without an origin bucket to protect |
| Mobile API certificate | `api.<domain>` served at the edge with a custom certificate whose keys Nyazek holds; the app pins the public keys of the current and a backup key (MOB-10) | Pinning to edge-managed certificates | Edge-managed certificates rotate without notice and would break pinned apps |
| Origins | Separate sub-domains for Storefront, Seller and Admin, each with a same-origin `/api` path | One origin with paths | Host-only session cookies per realm ([architecture](../prd/06-platform/architecture.md) §2). Closes D-16 |
| Web UI and i18n | Tailwind CSS 4, Radix UI primitives, shared `ui-web`, TanStack Query and Table, React Hook Form; ICU catalogues with `next-intl` and `use-intl` | – | As PRD §2 |
| Mobile | Flutter stable (3.50 / Dart 3.14 now), N-1 cadence | – | Owner mandate |
| Identity | In-house Identity module on maintained libraries (Argon2id, `jose`, `otplib`, SimpleWebAuthn) | Keycloak, Ory, Cognito | One account across four realms and phone OTP fit poorly in a multi-realm identity server (§3.13) |
| Analytics | Separate PostgreSQL analytics database; ClickHouse Cloud only when the §3.11 triggers are met | ClickHouse from day one | Fewer components at launch |
| Audit trail | Append-only PostgreSQL schema, hourly export to S3 Object Lock in a separate account, signed daily checkpoint | ELK | As PRD §3.12 and AUD-3 |
| Observability | OpenTelemetry to managed Grafana Cloud; Sentry for errors and crashes | Self-run Prometheus and ELK; Datadog | Managed, vendor-neutral instrumentation |
| Messaging providers | Amazon SES (`EmailPort`); Iraqi SMS aggregator, primary and fallback (`SmsPort`, D-29); FCM and APNs; Web Push P1 | – | As PRD §2 |
| Media and documents | `sharp` and ClamAV in the worker; HTML to PDF with headless Chromium (Playwright) | PDF libraries | Correct Arabic shaping (§3.14) |
| Bot challenge, maps, tags | Cloudflare Turnstile; Google Maps Platform behind `MapsPort` (P1); Google Tag Manager, GA4 and Meta Pixel, consent-gated, Storefront only | – | As PRD §2 |
| Developer environment | VS Code + Dev Containers, one image for humans, Claude and CI | – | Owner mandate |
| Feature flags | In-house `backoffice` configuration behind the OpenFeature API | Hosted flag services | No new vendor; configuration register already owned by `backoffice` |
| Local stack | Dev Container with PostgreSQL, OpenSearch, Valkey, mail catcher, provider mocks and a maintained S3-compatible emulator (SeaweedFS or Garage, chosen in T-0022) | MinIO (archived) | technology-stack §3.15 |
| Repository and delivery | pnpm workspaces + Turborepo; OpenTofu; GitHub Actions; VS Code Dev Containers | – | As PRD §2 and §4 |
| Testing and security tooling | As PRD §2 (Vitest, Testcontainers, fast-check, Playwright, Storybook, k6, `oasdiff`, Flutter tests; CodeQL or Semgrep, gitleaks, Trivy, dependency bot, OWASP ZAP baseline, SBOM) | – | The choice between CodeQL and Semgrep is left to the security guide (T-0044) |
| AI engineering agent | Claude only (Claude Code in the Dev Container and CI) | – | Owner mandate |

### Events and jobs across role boundaries

ARC-4 gives each module role privileges only on its own schema, and [architecture](../prd/06-platform/architecture.md) §3.2 allows only two cross-schema exceptions inside a business transaction. pg-boss keeps its jobs in one shared schema, so a module cannot enqueue there directly. The wiring is:

1. A module's business transaction writes events **and job requests** only to the outbox table in its own schema, under its own role.
2. Each module schema exposes two `SECURITY DEFINER` functions owned by the module role, each with a fixed `search_path`: one claims a batch of undispatched outbox rows (`FOR UPDATE SKIP LOCKED`), one marks rows dispatched. Execute on them, and nothing else, is granted to a platform role, `dispatcher`.
3. The outbox dispatcher in the `worker` role connects as `dispatcher`. In **one transaction** it claims a batch, appends each event to `event_log` (EVT-7), enqueues the jobs into pg-boss with the event ID as the deduplication key, and marks the rows dispatched. Because pg-boss lives in the same database, the claim, the enqueue and the mark commit or fail together.
4. `event_log` and the pg-boss schema are owned by a `queue_owner` role. `queue_owner` also creates queues and `event_log` partitions (at deploy, in the migration step) and runs pg-boss maintenance (archiving and purging) and monthly partition management. That recurring work runs as a separate scheduled maintenance task, not in the `worker`; only that task and the migration step hold `queue_owner` credentials, so no long-running process can change or delete `event_log` rows (EVT-7). `dispatcher` holds only insert on `event_log` and the runtime privileges pg-boss needs to enqueue; the job runner holds only the runtime privileges to fetch and complete jobs.
5. A job or event handler runs the consuming module's code under **that module's** role and records `(consumer, eventId)` in the consumer's own inbox table in the same transaction (EVT-5).
6. pg-boss does not migrate its schema at start (automatic migration off). Its schema changes run in the migration pipeline step under `queue_owner`, like any other migration (REL-3, REL-4).
7. The dispatcher uses one small pool and polls the module outboxes in turn. That pool is counted in the connection budget of [reliability-sre](../prd/06-platform/reliability-sre.md) §5.2.

This is the same execute-only pattern as the two §3.2 exceptions, but it runs outside any business transaction and by platform roles, not modules. On acceptance, ARC-4 and architecture §3.2 gain one sentence naming the platform roles `dispatcher`, `queue_owner` and `backup_reader` ("Backups"), so that the PRD and this ADR agree. The security architecture (T-0028) reviews the `SECURITY DEFINER` functions.

### Edge buffering of webhooks

[reliability-sre](../prd/06-platform/reliability-sre.md) §4.3 requires payment webhooks that reach the edge during an origin outage to be queued and replayed. Recommendation:

1. A Cloudflare Worker on the webhook routes records the edge receipt time, passes the request to the origin, and returns the origin's response when the origin answers.
2. Only when the origin is unreachable, times out, or answers `502`, `503`, `504` or an edge origin error, the Worker stores the raw request in Cloudflare Queues, encrypted with a public key whose private key only the `api` holds, together with the edge receipt time and the provider's source IP address, both signed with a key shared by the Worker and the `api`. It then answers `2xx` to the provider. A `4xx` from the origin is passed back unchanged and never buffered.
3. A consumer replays queued requests only while the origin's readiness check passes; while it fails, the consumer pauses and retries are not consumed. Queue retention is set to cover the regional recovery time of [reliability-sre](../prd/06-platform/reliability-sre.md) §4.2 (4 hours) with margin. A request goes to a dead-letter queue, which alerts on-call, only after the retry limit is reached while the origin is healthy; the reconciliation of API-14 covers anything lost.
4. On replay the `api` verifies the provider signature, applies the timestamp tolerance of API-11 to the **signed edge receipt time**, not to the replay time, and applies the IP allow-list of API-11 to the signed source address. The provider event ID makes the replay idempotent.

Point 4 needs a one-sentence clarification of API-11 (and PAY-6, which cites it), recorded in Consequences and made on acceptance. Whether Worker requests to the origin pass the ALB mutual-TLS check is confirmed in T-0032. Cost: usage-based and small at webhook volumes, within the Cloudflare plan in [technology-stack](../prd/06-platform/technology-stack.md) §6. The alternative is to rely only on the providers' own retries plus the reconciliation of API-14; it is weaker, because retry windows differ by provider. The detailed design belongs to the integration architecture (T-0029, F-DOC-056).

### Edge provider outage

[reliability-sre](../prd/06-platform/reliability-sre.md) §4.5 requires a documented DNS switch to an alternative path when the edge provider is down. A switch needs DNS that does not depend on that provider and a path that already exists:

1. **Authoritative DNS in Amazon Route 53**, not Cloudflare. Each public host is a record pointing to Cloudflare (Cloudflare's partial or CNAME setup, which needs a plan that supports it; confirmed in T-0032).
2. **A pre-provisioned standby path:** a CloudFront distribution with AWS WAF managed rules in front of the same ALB, plus an S3 bucket to which every release of the two static apps is also deployed. The ALB has a **second listener without mutual TLS** (mutual TLS applies to a whole listener, so the Cloudflare listener cannot serve it). That listener forwards only requests carrying a secret origin header and rejects all others; a security-group rule admits the CloudFront origin prefix list to it. Both stay disabled until the switch. The root domain uses a Route 53 alias record, since a root record cannot be a CNAME. The standby distribution for `api.<domain>` presents a certificate built on the key pair the mobile apps pin, imported into ACM (MOB-10), so pinned apps keep working after the switch.
3. **The switch** (runbook, incident commander's decision): enable the standby listener and its security-group rule and change the Route 53 records to CloudFront. Expected effect: DNS time-to-live plus minutes.
4. **Degraded while switched:** no bot management or Turnstile challenge (place-order rate limits stay in the `api`); no webhook buffering (provider retries and API-14 reconciliation cover it); Admin access falls back to the AWS-side zero-trust path defined in the security architecture (T-0028).

The standby path costs little while idle and is exercised in the drills of [reliability-sre](../prd/06-platform/reliability-sre.md) §4.4. The alternative, a Cloudflare-only setup with a planned migration, does not meet §4.5 and would need the owner to amend it.

### Backups

| Copy | Mechanism | Recovery point and retention | Immutability and key |
|---|---|---|---|
| Point-in-time recovery, 35 days (transactional and analytics databases) | AWS Backup continuous backup for RDS, in a vault with Vault Lock in compliance mode | Minutes; 35 days | Locked vault; the RDS key in the primary account (see the copy below for key separation) |
| Daily and monthly snapshots, primary and DR region, separate backup account | AWS Backup plans with cross-region and cross-account copy, into vaults with Vault Lock in compliance mode | Daily for 35 days; monthly for 12 months ([infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §7) | Locked vaults; the cross-account copy is encrypted with the backup account's KMS key, separate from the production data keys (BKP-1). That AWS Backup re-encrypts RDS copies this way is confirmed in T-0032 |
| Third location, different provider | Daily, a scheduled stateless task restores the latest snapshot to a temporary instance, takes a logical dump (`pg_dump`) of each database as the `backup_reader` role (read-only on every schema, used by nothing else), deletes the instance, encrypts the dump client-side to two recipients, and uploads it to R2 (or B2) under a retention lock | Daily; retention as the monthly snapshots | Bucket lock. Recipients: a key held offline by named owners, for the loss of the AWS accounts, and a KMS key in an isolated restore-test account, for the automated monthly test |
| Object storage (media, documents, KYC) | S3 versioning and cross-region replication; KYC and documents also copied to the third location by the same task, encrypted client-side as above | Per data class | Bucket lock at the third location |
| Audit exports | S3 Object Lock in the audit account (AUD-3); copied to the third location by the same task | 7 years | Exports are already signed; copies encrypted client-side as above and locked |
| Configuration store | Daily export of the `backoffice` configuration to the backup account and the third location by the same task; infrastructure code in Git | Daily | As above |

RDS gives no access to its transaction-log files and its snapshots cannot leave AWS, which is why the third-location copy is a logical dump, taken from a restored snapshot so that it never loads the production database or its replica. The monthly restore test (BKP-2) restores the latest third-location dump through the restore-test key into an isolated environment; its restore time is measured there and reported against the recovery objectives. On acceptance, [infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §7 is updated to name these mechanisms.

**Reading of BKP-1 for the owner to accept.** The 35-day point-in-time copy can only be encrypted with the production database key, because RDS restores in place from it. This ADR meets BKP-1's key separation through the snapshot copies in the backup account and the third-location dumps, which use separate keys, not through the point-in-time copy. Accepting this ADR accepts that reading.

### Gaps filled

The PRD requires these capabilities but does not name a component. Each recommendation is a managed service of the chosen cloud, or a small stateless container, so INF-1 holds.

| Requirement | Recommendation | Alternative | Note |
|---|---|---|---|
| Secrets manager (SEC-20) and separate backup keys (BKP-1) | AWS Secrets Manager; AWS KMS customer-managed keys, with a distinct key for backups | HashiCorp Vault (self-run) | Secrets replicated to the DR region, as [infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §7 requires |
| Connection pooling in transaction mode, one pool per module role ([infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §6) | Amazon RDS Proxy | PgBouncer as a stateless sidecar container | RDS Proxy limits connections per proxy, not per user, so each module's connection budget ([reliability-sre](../prd/06-platform/reliability-sre.md) §5.2) is enforced by the client pool size in each task, with either pooler. Each module role has its own credential (one secret per role, or IAM authentication). Statement and lock timeouts are set for each pool; with one pool per role they are set on the role (`ALTER ROLE … SET`). Replica reads use a separate connection to the replica endpoint. A Phase 2 spike answers: pinning under Kysely, pg-boss and the §3.2 shared-transaction calls; the other pinning triggers (session `SET`, named prepared statements, session advisory locks, `LISTEN`, temporary tables); whether the proxy can front the RDS read replica. If pinning defeats pooling, use PgBouncer |
| Load balancer reachable only from the edge (INF-2, INF-3) | Application Load Balancer restricted to Cloudflare address ranges, with per-hostname authenticated origin pulls verified by ALB mutual TLS | Cloudflare Tunnel (outbound connector containers, no public load balancer) | The ALB keeps the origin independent of one edge vendor (CDN fallback in Consequences); Tunnel is the alternative if the owner prefers no public ingress at all |
| Controlled egress allow-list (INF-4) and SSRF-safe proxy for user-supplied URLs (SEC-12) | Smokescreen (open-source egress proxy, Go) as a stateless container running in both availability zones, with two profiles: a provider allow-list for all workload egress, and an open-internet profile that blocks private, loopback and metadata addresses for user-supplied URLs. Workloads have no other route to the internet; AWS services are reached through VPC endpoints (S3, Secrets Manager, KMS, ECR, SES and logging where used) | AWS Network Firewall with domain rules (managed, but a fixed hourly cost per availability zone for the same control) | The allow-list names every external destination of this stack: PSPs, couriers, SMS aggregators, FCM and APNs, Grafana Cloud, Sentry, R2 or B2, the ClamAV signature mirror, Google Maps (server-side calls), the Cloudflare API, the status-page API if workloads post to it |
| Container registry | Amazon ECR in a shared tooling account, replicated to the DR region, pulled by staging and production through cross-account policies (ENV-2); images signed with Sigstore cosign and scanned | GitHub Container Registry | One image promoted unchanged from staging to production |
| Backup copy with a different provider (INF-6, BKP-1, AUD-3 third location) | Cloudflare R2 with bucket lock rules | Backblaze B2 with Object Lock | R2 reuses an existing vendor. Before T-0022 is approved, confirm that R2's lock gives compliance-mode immutability for the 7-year audit retention; if not, use B2 |
| Public status page (INC-2) | Hosted status-page service, outside the AWS and Cloudflare accounts | Self-hosted | Vendor is open item OI-1 below |
| Edge buffering of payment webhooks ([reliability-sre](../prd/06-platform/reliability-sre.md) §4.3) | Cloudflare Workers and Queues | Provider retries plus API-14 reconciliation only | See "Edge buffering of webhooks" |

## Requirement mapping

Scope: every numbered rule in `docs/prd/06-platform/` (ARC, EVT, API, DAT, INF, ENV, REL, BKP, CAP, INC), every row of the non-functional table in [reliability-sre](../prd/06-platform/reliability-sre.md) §1, and the client rules WEB, MOB and UI in `docs/prd/07-clients/`, followed by the platform requirements that carry no rule ID. A rule that is a policy (for example REL-5, the change freeze) maps to the component that enforces or records it.

| Rules | Component(s) |
|---|---|
| ARC-1 | NestJS 12 application, one image in two roles on ECS Fargate |
| ARC-2, ARC-4, DAT-1 | PostgreSQL 18: one schema and one database role per module; Kysely migrations per module; RDS Proxy pool per role |
| ARC-3 | NestJS module exports; boundary lint in CI (tool chosen in the backend guide, T-0041) |
| ARC-5, EVT-5 to EVT-8 | Module outbox and inbox tables, the `dispatcher` role and pg-boss as in "Events and jobs across role boundaries" (retries, backoff, dead-letter); Grafana alerts on outbox age |
| ARC-6, ARC-7, WEB-1 to WEB-6 | Generated API client; Next.js lint rule blocking server actions; SPAs with no server runtime |
| ARC-8, API-11 to API-14 | Ports and adapters in NestJS; raw webhook store in PostgreSQL; pg-boss for async processing and reconciliation polling; Cloudflare Workers and Queues buffer webhooks during an origin outage |
| ARC-9, DAT-2 | PostgreSQL as system of record; OpenSearch, Valkey, analytics database and Cloudflare cache rebuildable from it and the event log |
| ARC-10 | Narrow module interfaces; `EventBus` port with an optional broker adapter later |
| EVT-1 to EVT-4, EVT-9 | Zod event schemas in `packages/contracts`, versioned; per-aggregate `sequence` column |
| API-1, API-2 | NestJS guards per audience; Cloudflare and ALB routing (no admin routes on the public host) |
| API-3 to API-5 | Zod → OpenAPI 3.1; `oasdiff` breaking-change check in GitHub Actions |
| API-6, API-7, MOB-3 | `GET /v1/app-config` from `backoffice` configuration (OpenFeature) |
| API-8 to API-10 | Idempotency table in PostgreSQL with unique `(principal, endpoint, key)` |
| API-15 | Market resolution in the API from account or host; market configuration in `backoffice` |
| DAT-3, DAT-4 | Analytics PostgreSQL database fed from events; finance reports from the ledger schema |
| INF-1 | RDS, ElastiCache, OpenSearch Service, S3, Secrets Manager (all managed) |
| INF-2, INF-3 | ECS Fargate in two availability zones; ALB restricted to Cloudflare; no public IPs |
| INF-4 | Smokescreen allow-list and SSRF profiles; VPC endpoints |
| INF-5 to INF-8 | Two European AWS regions; OpenTofu with region as a variable; R2 (or B2) third location ("Backups") |
| ENV-1 to ENV-3 | OpenTofu modules shared by staging and production; separate AWS accounts; Cloudflare configuration in code |
| REL-1 to REL-6 | GitHub Actions release pipeline; ECS rolling and canary deploys; migration step with lock and timeout; immutable static assets on Cloudflare |
| BKP-1, BKP-2 | As in "Backups": RDS point-in-time recovery; AWS Backup with Vault Lock and the backup KMS key; daily encrypted logical dump to the third location; monthly restore test that includes the third-location copy |
| CAP-1 to CAP-4 | ECS scheduled and target-tracking scaling; Cloudflare rate limiting and waiting room on place-order; circuit breakers and bounded queues in adapters and pg-boss; k6 load test |
| INC-1 to INC-3 | Grafana alerting and on-call routing; hosted status page; staffing per D-27 |
| NFR: web performance, low bandwidth | Next.js server rendering; Cloudflare edge in Iraq; `sharp` image variants; real-user monitoring through Grafana Faro or Sentry |
| NFR: API and search latency | PostgreSQL with read replica for tolerant reads; Valkey caches; OpenSearch |
| NFR: availability and continuity | Multi-AZ RDS and ECS; cross-region replica and runbook promotion ([reliability-sre](../prd/06-platform/reliability-sre.md) §4); edge-down switch to the CloudFront standby path (§4.5, "Edge provider outage") |
| NFR: RTL and localisation | ICU catalogues; Tailwind logical properties; Chromium PDF rendering; Flutter runtime direction |
| NFR: accessibility | Radix UI primitives; Storybook accessibility checks; Flutter semantics |
| NFR: card data (SAQ A) | PSP-hosted entry only; no card fields in any client |
| NFR: audit integrity | Append-only audit schema; S3 Object Lock export; signed checkpoint job |
| NFR: observability | OpenTelemetry SDKs; Grafana Cloud; Sentry |
| NFR: maintainability | Turborepo pipeline with boundary lint, contract tests, coverage thresholds |
| NFR: scalability | Stateless `api` and `worker` on ECS autoscaling; PostgreSQL sized per [reliability-sre](../prd/06-platform/reliability-sre.md) §5.2; OpenSearch Service scaling; Cloudflare caching |
| NFR: SEO | Next.js server rendering, metadata and structured data; sitemap and robots route handlers (WEB-3 technical exception) |
| NFR: security | Cloudflare WAF and bot management; ALB mutual TLS; Secrets Manager and KMS; Smokescreen; CI security tooling (SEC-25); penetration test before launch |
| NFR: privacy | Per-module ownership of personal data in PostgreSQL; EVT-2 payload rule enforced by event schemas; consent-gated tags; KMS encryption at rest |
| NFR: data integrity | PostgreSQL constraints and transactions; idempotency table (API-8 to API-10); outbox and inbox; ledger invariants as constraints and jobs |
| NFR: API compatibility | Zod → OpenAPI, `oasdiff`, `/v1/app-config` forced update (API-3 to API-6) |
| UI-1 to UI-4 | Design tokens generated into the Tailwind theme and the Dart theme; Storybook as the component reference; ICU message catalogues with a missing-key check in CI |
| MOB-1 to MOB-11 | Flutter with Riverpod, go_router, dio, flutter_secure_storage, firebase_messaging and sentry_flutter (decided here); generated Dart API client; generated theme and ARB files |
| WEB-7 | Browserslist targets in the shared build configuration; Playwright projects for the listed browsers |

Platform requirements without a rule ID:

| Requirement | Component(s) |
|---|---|
| Synthetic probes, including from Iraq ([reliability-sre](../prd/06-platform/reliability-sre.md) §3) | Grafana Cloud synthetic monitoring, with a private probe hosted in Iraq |
| Preview deployments per pull request ([release-plan](../prd/00-governance/release-plan.md) §2, delivery Phase 1) | Cloudflare previews for the two static apps; an ephemeral Storefront and `api` on ECS against a seeded database, on the same runtime as production (ENV-1); Lighthouse CI runs against that preview |
| Infrastructure state and drift detection ([infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §4) | OpenTofu state in S3 with locking, in the tooling account; scheduled `plan` in GitHub Actions that alerts on drift |
| Cost budgets ([infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §8) | AWS Budgets and Cost Anomaly Detection; Cloudflare and Grafana usage alerts |
| Performance budgets in CI ([web-apps](../prd/07-clients/web-apps.md)) | Lighthouse CI and a bundle-size check in GitHub Actions |
| Design-token generation ([design-system-ui-workflow](../prd/07-clients/design-system-ui-workflow.md)) | One token generator producing CSS variables, the Tailwind theme and the Dart theme (tool is open item OI-4) |
| Mobile build and release ([mobile-flutter](../prd/07-clients/mobile-flutter.md)) | Fastlane on GitHub Actions macOS runners; Flutter version pinned with FVM |
| Licence and infrastructure-as-code scans (SEC-25) | A licence checker over pnpm and pub dependencies; Trivy configuration scanning of the OpenTofu code |

## Open items

Choices this ADR leaves to a later task. Each is recorded here and linked from the task that closes it; none blocks `foundation.md`. A vendor chosen under an open item needs the owner's approval before use.

| ID | Item | Decided in |
|---|---|---|
| OI-1 | Status-page vendor | Deployment guide (T-0045) |
| OI-2 | CodeQL or Semgrep for static analysis | Security guide (T-0044) |
| OI-3 | Module-boundary lint tool | Backend guide (T-0041) |
| OI-4 | Design-token generator | Frontend guide (T-0042) |
| OI-5 | Real-user monitoring through Grafana Faro or Sentry | Foundation (T-0022) |
| OI-6 | RDS Multi-AZ instance or cluster shape; RDS Proxy or PgBouncer after the spike | Foundation (T-0022) |
| OI-7 | Cloudflare R2 or Backblaze B2 for the third location, after the lock check | Foundation (T-0022) |

## Consequences

- **Where the stack lives after acceptance.** This ADR is the decision record and is not edited afterwards except for its status. `foundation.md` (T-0022) is the one living list of the confirmed stack and its versions, as ADR-0002 §1 requires, and links here for the reasons. [technology-stack](../prd/06-platform/technology-stack.md) keeps the reasoning (§1, §3, §4, §6); its status line, §2, §5 and §7 are replaced by a pointer to this ADR and `foundation.md`, so that the list is not kept in three places.
- **Decisions closed on acceptance:** D-35, D-16, D-17 and D-18, recorded in [open-decisions](../prd/00-governance/open-decisions.md) §5. Closing them updates, in the same change, the documents in their Spec column: [technology-stack](../prd/06-platform/technology-stack.md) (D-35; §3.2 for D-17; §3.9 for D-18) and [identity-access](../prd/05-trust/identity-access.md) §6 (D-16). [architecture](../prd/06-platform/architecture.md) replaces its "proposed" status wording with a pointer to this ADR, and ARC-4 and §3.2 gain the platform-role sentence from "Events and jobs across role boundaries". [api-standards](../prd/06-platform/api-standards.md) API-11 and [payments](../prd/04-finance/payments.md) PAY-6 gain the clarification on signed edge receipt time and source address from "Edge buffering of webhooks". [infrastructure-devops](../prd/06-platform/infrastructure-devops.md) §7 names the backup mechanisms. The other "proposed stack" wording is replaced too: the technology-stack "Authoritative for" line, [PRD README](../prd/README.md) §1 (06-platform intro and table row) and §4, the [open-decisions](../prd/00-governance/open-decisions.md) §4 intro, and the status lines in `CLAUDE.md` and `IMPLEMENTATION_STATUS.md`.
- T-0022 (`foundation.md`) starts from this stack, records the exact versions in force at that time, re-checks the components not verified here, and closes OI-5 to OI-7.
- Two spikes run in Phase 2 before `foundation.md` is approved: the RDS Proxy questions in "Gaps filled", and the R2 lock check. Each answers its questions and is archived afterwards (Phase 2 rules).
- The latency measurement from Iraqi networks in delivery Phase 1 (INF-6) picks the two European regions and validates Cloudflare. If Cloudflare fails it, the CloudFront standby path from "Edge provider outage" becomes the primary edge: a planned change, made small because that path, Route 53 and the static-app bucket already exist.
- **New services and tools relative to PRD v7.3**, listed for the owner's decision with this ADR: a hosted status page; Cloudflare Workers, Queues, Waiting Room and static-asset hosting; Smokescreen; Sigstore cosign; AWS Backup, Secrets Manager, KMS, RDS Proxy (or PgBouncer), ECR, Budgets and Cost Anomaly Detection; Route 53, and CloudFront with AWS WAF as the standby edge; Grafana Cloud synthetic monitoring with a probe hosted in Iraq (hosting provider chosen in T-0022); Fastlane and FVM; Lighthouse CI; a licence checker; Cloudflare R2 or Backblaze B2. Every vendor chosen later under an open item comes back to the owner for approval before use.
- T-0032 runs the spikes and needs AWS and Cloudflare accounts with paid resources; it starts only after the owner approves those accounts.

## Risks

| Risk | Mitigation |
|---|---|
| Kysely is pre-1.0 and had security fixes in 2026 | Version floor at the latest fix; dependency bot; queries isolated in repositories so a move to another query builder is mechanical |
| PostgreSQL 19 releases two days after this ADR | Stay on 18 until the managed service offers 19 and one minor release has shipped (PRD §5) |
| Flutter 3.50 release date from a secondary source | Mobile work starts post-launch; the version is fixed then |
| Cloudflare as a second infrastructure vendor | Measured in delivery Phase 1; DNS in Route 53; pre-provisioned CloudFront standby path and runbook switch |
| RDS Proxy pinning | Spike; PgBouncer fallback |

## Sources (checked 17 November 2026)

- Node.js 26 LTS: [linuxcompatible.org](https://www.linuxcompatible.org/story/nodejs-26130-lithium-reaches-lts-support-through-april-2029/), [nodejs.org release schedule](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule)
- NestJS 12: [InfoQ](https://infoq.com/news/2026/10/nestjs-12-observability), [endoflife.date](https://endoflife.date/nestjs), [release PR](https://github.com/nestjs/nest/pull/16391)
- PostgreSQL on RDS: [AWS announcement, major version 18](https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-rds-postgresql-major-version-18), [RDS PostgreSQL versions](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-versions.html); PostgreSQL 19 schedule: [devx.com](https://www.devx.com/cybersecurity/postgresql-19-new-features-release-date/)
- Kysely: [issoh.co.jp](https://www.issoh.co.jp/tech/details/19069/), [Snyk advisory](https://security.snyk.io/vuln/SNYK-JS-KYSELY-16642092), [NVD CVE-2026-32763](https://nvd.nist.gov/vuln/detail/CVE-2026-32763)
- Drizzle ORM 1.0 status: [release notes](https://newreleases.io/project/npm/drizzle-orm/release/1.0.0-rc.4)
- pg-boss: [SourceForge mirror of releases](https://sourceforge.net/projects/pg-boss.mirror/files/12.26.0/)
- OpenSearch on AWS: [OpenSearch 3.7 support](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-opensearch-service/)
- Next.js 16: [nextjs.org](https://nextjs.org/blog/next-16), [versionlog](https://versionlog.com/nextjs/16/)
- Flutter 3.50: [release notes](https://docs.flutter.dev/release/release-notes/release-notes-3.50.0), [Very Good Ventures](https://verygood.ventures/blog/flutter-3-50-dart-3-14/) (date)

Where a fact rests on a secondary or mirror source (Node.js LTS date, NestJS patch level, PostgreSQL 19 date, Kysely, Drizzle status, pg-boss, Next.js patch level, the Flutter date), T-0022 confirms it against the npm registry or the project's own release page when it fixes the exact version.
