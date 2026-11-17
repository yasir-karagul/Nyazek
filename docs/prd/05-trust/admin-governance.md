# Admin Governance & RBAC

**Authoritative for:** admin roles, permission matrix, dual control, admin security rules, platform configuration governance.
**Related:** [admin-panel](admin-panel.md) (modules, queues, screen behaviour) · [identity-access](identity-access.md) · [privacy-audit](privacy-audit.md) §5 · [security](security.md) · [sitemap](../09-information-architecture/sitemap.md) §8 (page IDs `AD-*`)

---

## 1. Roles (11)

| Role | Purpose |
|---|---|
| Super Admin | Platform administration: admin users, roles, thresholds, platform settings |
| Catalog Manager | Catalogue requests, canonical content, categories, attribute schemas, brands, price-rule queues, listing reports |
| Seller Manager | KYC review, seller lifecycle, performance levels and appeals |
| Finance Manager | Ledger, reconciliation, refunds queue, payout runs, commission schedule, wallet adjustments |
| Support Agent | Tickets, returns oversight, dispute handling, review and Q&A moderation |
| Content Manager | CMS: home page, banners, static pages, templates, help articles |
| Fraud / Risk Manager | Risk queue and cases, overrides, COD risk configuration, blocklists, account freezes |
| Compliance / Audit Viewer | Read-only access to audit trail, ledger, KYC records and reports. Its only write actions are handling data-subject requests and approving, as second person, bulk personal-data exports and legal-page publication |
| 1P Merchandiser | Operates the Nyazek Official Store: offers, cost, stock, pricing, 1P orders |
| Logistics Manager | Couriers, serviceability, shipments and exceptions, COD remittance |
| Marketing Manager | Coupons, deals, campaigns, loyalty configuration, ad moderation, notification campaigns |

An admin may hold more than one role, except that Compliance / Audit Viewer cannot be combined with any other role. Custom roles are not supported at launch: the eleven roles are fixed, and only their permission lists change (RBAC-3).

## 2. Permission model

- RBAC-1 Deny by default. Each role has an explicit list of permissions; a permission is `resource:action` (for example `kyc:decide`, `payout:approve`).
- RBAC-2 Permissions are enforced by the API on every `/v1/admin/*` endpoint. The Admin Panel hides what the API would refuse; it is never the control.
- RBAC-3 The role-to-permission mapping is data, changed only by a Super Admin under dual control, and every change is audited.
- RBAC-4 Sensitive personal data (full phone, address, identity documents, bank details) is masked by default and revealed per record with a logged reason.

### 2.1 Baseline matrix

M = manage (create, edit, decide) · R = read · A = approve as second person · – = none.

| Domain | Super | Catalog | Seller Mgr | Finance | Support | Content | Risk | Compliance | 1P | Logistics | Marketing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Admin users, roles, thresholds | M, A | – | – | – | – | – | – | R | – | – | – |
| Platform settings | M | R | R | R, A (tax and the financially sensitive settings in §3) | R | R | R | R | – | R | R |
| Catalogue, categories, brands | R | M | R | – | R | – | R | R | R | – | R |
| Price-rule and listing-report queues | R | M | R | – | R | – | R | R | – | – | – |
| Sellers and KYC | R | – | M, A | R | R | – | R | R | – | – | – |
| Seller suspension | A | – | M, A | – | – | – | M | R | – | – | – |
| Customers (accounts) | R, A | – | – | – | M | – | M | R | – | – | – |
| Orders | R, A | – | R | R, A | M | – | R | R | M (1P only) | M | – |
| Shipments, couriers, serviceability | R | – | – | R | R | – | – | R | – | M | – |
| COD remittance | R | – | – | A | – | – | – | R | – | M | – |
| Returns and disputes | R | – | R | A | M | – | R | R | – | R | – |
| Refund queue, payouts, adjustments | A | – | – | M, A | – | – | – | R | – | – | – |
| Ledger and reconciliation | R, A | – | – | M | – | – | – | R | – | – | – |
| Commission schedule | A | – | – | M | – | – | – | R | – | – | – |
| Risk queue, overrides, blocklists | R, A | – | R | A | R | – | M | R | – | – | – |
| Reviews and Q&A moderation | R | – | – | – | M | – | R | R | – | – | – |
| Support tickets | R | – | R | R | M | – | R | R | – | R | – |
| CMS and templates | R | – | – | – | – | M | – | R | – | – | R |
| Promotions, loyalty, ads | R | – | – | R | – | – | R | R | – | – | M |
| 1P offers, cost, stock, margin | R | – | – | R | – | – | – | R | M | – | – |
| Audit trail | R | – | – | – | – | – | – | R | – | – | – |
| Analytics | R | R (own domain) | R | R | R | R | R | R | R | R | R |
| Legal-page publication | R | – | – | – | – | M | – | A | – | – | – |
| Data-subject requests (including approval of bulk personal-data exports) | R | – | – | – | R | – | – | M, A | – | – | – |

This matrix is the starting configuration; the detailed permission list per endpoint is generated from the API contract. Cost and margin figures, in any domain including Analytics, are visible only to the roles in FP-2. Approvals marked A are the dual-control approvals in §3; "M, A" means the role may also approve another person's request in that row; nobody approves their own request.

## 3. Dual control

A dual-control action is requested by one admin and approved by a different admin holding an approving permission. The requester can never approve their own request.

| Action | Requester | Approver |
|---|---|---|
| Manual refund or goodwill credit above `cfg:refunds.dual_control_threshold` | Support, Finance | Finance, Super Admin |
| Wallet adjustment (any amount) | Finance | Finance (different person), Super Admin |
| Payout run approval | Finance | Finance (different person), Super Admin |
| Seller suspension or reinstatement | Seller Manager, Risk | Super Admin, Seller Manager (different person) |
| Urgent account freeze | Risk (immediate, temporary 24 h) | Super Admin or Seller Manager (for sellers), Super Admin (for customers) |
| Dispute decision above `cfg:disputes.agent_limit` | Support | Finance |
| Commission schedule change | Finance | Super Admin |
| COD write-off | Logistics | Finance |
| Seller receivable write-off (JE-49) | Finance | Super Admin |
| Refund cancellation (refund `CANCELLED`) | Finance | Finance (different person) |
| Risk hold on a seller above `cfg:risk.hold_dual_control_threshold` (default 1,000,000 IQD) | Risk | Super Admin, Finance |
| Legal-page publication | Content Manager | Compliance |
| Role, permission or threshold change | Super Admin | Super Admin (different person) |
| Password or 2FA reset of an admin ([identity-access](identity-access.md) §4) | Super Admin (not the target) | Super Admin (different person, not the target); where fewer than two other Super Admins exist, the owner performs the reset |
| Tax configuration change | Super Admin | Finance |
| Financially sensitive setting change (the single list: payout cycle, escrow hold, order and payment timers, COD limits and fee, shipping rates, loyalty rates; the commission schedule and the thresholds of this table have their own rows) | The editing role | Finance; Super Admin when Finance edits |
| Manual order state override after `SHIPPED` | Support, Logistics | Super Admin, Finance |
| Bulk personal-data export | Any | Compliance |
| Manual journal entry | Finance | Super Admin |

- DC-1 Requests appear in the approvals inbox with full context; they expire after `cfg:backoffice.approval_ttl_hours` (default 72).
- DC-2 Thresholds are configured by a Super Admin under dual control and cannot be changed by a person they constrain.
- DC-3 A minimum of two Super Admins must exist. The platform refuses to disable the second-to-last one.

## 4. Admin security

- Invitation-only accounts; unique email across the platform; mandatory 2FA (TOTP or passkey); no shared accounts.
- The Admin origin is reachable only through zero-trust access ([identity-access](identity-access.md) §6).
- Session limits per SES-2; step-up before approvals.
- Every admin action is audited with user, role, time, IP, device, action and before/after values ([privacy-audit](privacy-audit.md) §5).
- No role, including Super Admin, can edit or delete audit records, journal entries or issued documents.
- Break-glass access is a documented, logged procedure with a separate, normally disabled account and automatic notification to all Super Admins.
- Admin offboarding: accounts are disabled the same day; a quarterly access review is performed by the Super Admin and Compliance.
- The Admin Panel is available in Arabic and English.

## 5. Platform configuration

- Every value marked `cfg:` in this documentation is stored in the `backoffice` configuration store, typed and validated, with an owner role, audit history and effective-from time. Values on the platform settings pages (`AD-SET-*`) are edited by the Super Admin (matrix row "Platform settings"), except the commission schedule, which Finance edits. Values with their own pages are edited by the role that page names: COD limits by Fraud/Risk (`AD-RISK-COD`), loyalty rates by Marketing, only on `AD-LOY-CONFIG`, 1P pricing rules by the 1P Merchandiser (`AD-PRO-PRICING`). The owner role named in the configuration register is notified of every change to its values ([ADR-0007](../../adr/0007-decisions-from-the-ia-consistency-pass.md)). The full list is in [configuration-register](../00-governance/configuration-register.md).
- Financially sensitive settings change under dual control as listed in §3.
- Feature flags and the app-configuration values (minimum app versions, maintenance mode) are managed in the same store ([api-standards](../06-platform/api-standards.md) API-6).
- A configuration value resolves in this order: market override, then platform default. Market configuration (currency table, time zone, phone ranges, address labels, working week, tax region) is held in the same store. Admin roles are granted per market; at launch every role is scoped to Iraq.

## 6. Acceptance criteria

- Each role can perform only the actions in its permission list (automated test generated from the matrix).
- No dual-control action completes with a single person, including when that person holds both roles.
- An admin viewing a masked field leaves an audit record with the stated reason.
