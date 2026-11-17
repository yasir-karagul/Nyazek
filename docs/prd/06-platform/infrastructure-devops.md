# Infrastructure, Deployment & DevOps

**Authoritative for:** hosting topology, regions, environments, networking, CI/CD, migrations, release and rollback, backups.
**Related:** [technology-stack](technology-stack.md) · [reliability-sre](reliability-sre.md) · [security](../05-trust/security.md) · [claude-workflow](../08-engineering/claude-workflow.md)

---

## 1. Topology

```
Users (Iraq) ─► Cloudflare edge (DNS, CDN, WAF, bot defence, Turnstile, zero-trust for admin)
                  ├─ static: seller SPA, admin SPA, media (origin: object storage)
                  ├─ www.<domain>      ─► storefront containers (Next.js)
                  ├─ <origin>/api/*    ─► api containers (NestJS)
                  └─ api.<domain>      ─► api containers (mobile, webhooks)
Primary region (private network):
   api, worker, storefront containers  ─► PostgreSQL (primary + standby, read replica)
                                       ─► analytics PostgreSQL
                                       ─► OpenSearch · Valkey · object storage · secrets and keys
DR region: database replica, replicated object storage, container definitions, infrastructure code
Third location (different provider): immutable backup copies, audit exports
```

- INF-1 All stateful components are managed services. Nothing stateful runs in containers.
- INF-2 Containers run on a managed container platform in at least two availability zones behind a load balancer; no public IPs on workloads.
- INF-3 Only the edge can reach the load balancer (origin access restricted to the edge provider and authenticated origin pulls).
- INF-4 Outbound traffic from workloads goes through controlled egress with an allow-list for PSP, courier, SMS, email and push endpoints, and the SSRF-safe proxy for user-supplied URLs.

## 2. Regions and residency

- INF-5 No Middle East cloud region may be the sole location of production data or backups ([technology-stack](technology-stack.md) §3.10).
- INF-6 Placement (D-06, decided): primary in a European region with good connectivity to Iraq, DR in a second European region, backup copies with a different provider. Network latency from Iraqi fixed and mobile networks to candidate regions and through the edge is measured in delivery Phase 1, Foundation ([release-plan](../00-governance/release-plan.md) §2), to choose the specific regions.
- INF-7 Storage and databases are region-pinned and defined in code so that data can be relocated if D-06 or a future law requires it.
- INF-8 The legal meaning of "Iraqi data residency" (data physically in Iraq, an Iraqi controller under Iraqi law, or contractual protections) is defined by the owner with counsel (follow-up of D-06, tracked in T-0015); the placement in INF-6 applies until then.

## 3. Environments

| Environment | Purpose | Data | Integrations |
|---|---|---|---|
| Local (Dev Container) | Development by humans and Claude | Seed fixtures | Mock PSP, courier, SMS; local emulators |
| CI | Automated checks | Ephemeral | Mocks; Testcontainers |
| Preview (per pull request) | Review of UI and API changes | Seed fixtures | Mocks |
| Staging | Release candidates, end-to-end, load and security tests | Synthetic | Provider sandboxes |
| Production | Live | Real | Live providers |

- ENV-1 Environments differ only in configuration and scale. No environment-specific code paths.
- ENV-2 Production and staging are separate cloud accounts with separate credentials and keys. The audit export bucket is in its own account.
- ENV-3 Staging mirrors production topology at reduced size, including the edge configuration.

## 4. Infrastructure as code

- All cloud and edge resources are defined in OpenTofu under `infra/`, reviewed by pull request, planned in CI and applied through the pipeline with human approval for production.
- State is stored remotely with locking and encryption. Manual console changes in production are prohibited outside break-glass, which must be followed by a code change.
- Drift detection runs daily.

## 5. CI/CD

### 5.1 Pull-request pipeline (all must pass)

Format and lint · type-check · unit tests · module-boundary check · contract generation check and breaking-change check · integration tests with real PostgreSQL · security scans (SEC-25) · build of affected apps · Storybook and visual tests for UI changes · Flutter analyze, test and build when Dart code changes · preview deployment.

### 5.2 Release pipeline

1. Merge to `main` builds signed images tagged by commit and deploys to staging automatically.
2. Staging runs migrations, smoke tests, end-to-end tests and the DAST baseline.
3. Production deployment is started by the owner (or a designated human), never by the AI agent alone.
4. Production rollout is rolling with health checks; a canary step (10% of traffic for 15 minutes with automatic rollback on error-rate or latency regression) is added before public launch.
5. Unfinished features are merged behind feature flags (trunk-based development).

- REL-1 Every release is identified by commit; the running version is visible on `/health/ready` and in telemetry.
- REL-2 Rollback is redeploying the previous image, possible at any time because of REL-3.
- REL-3 Database migrations are backward compatible with the previous application version (expand, migrate, contract): add before use, remove only in a later release. Destructive migrations require explicit owner approval and a verified backup.
- REL-4 Migrations run as a separate pipeline step before the new version starts, with a lock, a timeout and a dry run on a staging copy. Long data backfills run as background jobs, not inside migrations.
- REL-5 Deployments are avoided during peak events (Ramadan evenings, Eid, flash sales) except for fixes; a change freeze calendar is maintained.
- REL-6 Static apps are deployed atomically with immutable asset names; the previous version stays available for clients mid-session.

## 6. Database operations

- Managed PostgreSQL with a synchronous standby in another availability zone, automated failover, and point-in-time recovery.
- Connection pooling in transaction mode in front of the database; one pool per module role; statement and lock timeouts set per pool.
- A read replica serves the search indexer's bulk reads and operational reports that tolerate lag; nothing that affects money or stock reads from a replica.
- Partitioning by month for `event_log`, audit, journal lines, tracking events, notification log and clickstream; old partitions are archived per retention.
- Routine maintenance (vacuum, index health, bloat, slow-query review) is monitored.

## 7. Backups

| Asset | Method | Retention | Location |
|---|---|---|---|
| PostgreSQL (transactional and analytics) | Continuous backup + daily snapshots (mechanisms below) | 35 days point-in-time; monthly snapshot for 12 months | Primary region, copied to DR region and to the third location |
| Object storage (media, documents, KYC) | Versioning + cross-region replication | Per data class | DR region; KYC and documents also to the third location |
| Audit exports | Object Lock, compliance mode | 7 years | Separate account + third location |
| Search index | Not backed up (rebuildable); snapshots optional for faster recovery | – | – |
| Infrastructure code, configuration store | Git; configuration exported daily | – | – |
| Secrets | Managed service with replication | – | DR region |

The mechanism for each copy (AWS Backup with Vault Lock, cross-account copies under a separate key, a daily encrypted logical dump to the third location) is defined in [ADR-0004](../../adr/0004-technology-stack.md) "Backups".

- BKP-1 Backups are encrypted with keys separate from the production data keys and are immutable for their retention period.
- BKP-2 Restore is tested automatically every month into an isolated environment with integrity checks (row counts, ledger trial balance, audit chain verification).

## 8. Cost and capacity controls

- Budgets and alerts per account; autoscaling limits; scheduled pre-scaling for known peaks ([reliability-sre](reliability-sre.md) §5).
- Telemetry sampling and log levels are tuned to control observability cost.

## 9. Acceptance criteria

- A new environment can be created from code alone.
- A production deployment can be rolled back within 10 minutes without data loss.
- A monthly restore test passes its integrity checks and records the measured restore time.
- The load balancer rejects requests that do not come through the edge.
