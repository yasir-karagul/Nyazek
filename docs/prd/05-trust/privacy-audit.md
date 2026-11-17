# Privacy, Data Governance & Audit Trail

**Authoritative for:** personal-data principles, consent, data-subject requests, retention, the immutable audit trail, log classes and access.
**Related:** [compliance-legal](compliance-legal.md) · [security](security.md) · [identity-access](identity-access.md) · [data-analytics](../06-platform/data-analytics.md)

---

## 1. Principles

- PRV-1 Collect only what a feature needs; every personal-data field has a documented purpose and retention period.
- PRV-2 Explicit consent before using personal data for purposes beyond fulfilling orders (marketing, analytics cookies, personalisation).
- PRV-3 Personal data is shared with sellers and couriers only as needed to fulfil the order; sellers may not use customer data for marketing outside the platform (Seller Agreement).
- PRV-4 Iraq has no comprehensive data-protection statute in force; the platform follows the duties in E-Commerce Regulation No. 4 of 2025 (security, minimal collection, explicit consent, breach notification) and applies GDPR-style rights as its own standard ([compliance-legal](compliance-legal.md) §2). Markets with a data-protection law in force (several Gulf states) add their own duties at market entry ([market-expansion](../01-product/market-expansion.md) §5).
- PRV-5 A data inventory (data map) is maintained in the repository: field, module, classification, purpose, retention, who can access.

### 1.1 Classification

| Class | Examples | Handling |
|---|---|---|
| Restricted | Identity documents, bank and wallet numbers, passwords, 2FA secrets, OTPs | Field-level encryption or hashing; access logged; never in logs, events or analytics |
| Personal | Name, phone, email, addresses, order history, device identifiers | Encrypted at rest; masked in admin by default; pseudonymous IDs in events and analytics |
| Business confidential | Seller sales, wallet, cost prices, commission terms | Visible to the seller and permitted admin roles only |
| Public | Catalogue content, published reviews, store pages | – |

## 2. Consent

- Consent records store: account or anonymous ID, purpose, channel, decision, timestamp, policy version, source (banner, checkout, preferences).
- Purposes: marketing email, marketing SMS, marketing push, analytics cookies, advertising cookies, personalisation.
- Withdrawal is as easy as granting and takes effect immediately for new sends.
- The cookie banner offers accept, reject and choose, with no pre-ticked boxes; rejecting does not degrade the shopping flow.
- Terms and privacy-policy acceptance is recorded with document version ([support-cms](../02-commerce/support-cms.md) CMS-2).

## 3. Data-subject requests

| Request | Behaviour |
|---|---|
| Access / export | Machine-readable export of profile, addresses, orders, reviews, consents; delivered to the verified account |
| Rectification | Self-service for profile and addresses; identity-verified request for other data |
| Erasure / account deletion | Blocked while orders, returns, disputes or balances are open. Then the profile is anonymised; records under legal retention are kept in pseudonymous form; identifier claims are released after the cool-down |
| Objection to marketing | Immediate opt-out |

- DSR-1 Requests are tracked with an SLA of `cfg:privacy.dsr_sla_days` (default 30) and handled by the Compliance role.
- DSR-2 The requester's identity is verified by signed-in session plus step-up authentication.
- DSR-3 Sellers' KYC and financial records follow legal retention and are not erasable on request during that period.
- DSR-4 Requests for user data from courts, regulators or law-enforcement bodies are handled only by the Compliance role with counsel: each request is logged with its legal basis, scope and response, the minimum data that satisfies it is disclosed, and no other role may answer one. The procedure is part of the legal pack for each market.

## 4. Retention

| Data | Retention | Then |
|---|---|---|
| Ledger, invoices, credit notes, payout records | 7 years | Archive or delete per counsel |
| Orders and order lines | 7 years (financial evidence) | Customer-identifying fields anonymised on erasure, record kept |
| Audit trail | 7 years | Delete |
| KYC documents | Life of the seller relationship + period set by counsel (default 5 years) | Delete |
| Closed-account profile data | Anonymised at closure | – |
| Unverified registrations | 72 hours | Delete |
| Carts and abandoned checkout sessions | 90 days | Delete |
| Messages and dispute evidence | 2 years after closure of the order | Delete |
| Support tickets | 2 years after closure | Delete or anonymise |
| Notification delivery log | 12 months | Delete |
| Operational logs and traces | 30 days hot, up to 90 days archived | Delete |
| Clickstream analytics (identified) | 14 months | Aggregate and anonymise |
| Domain event log | 25 months (EVT-7); payloads carry no personal data | Delete |
| Backups | 35 days rolling, plus monthly copies for 12 months | Expire |

Retention periods are defaults pending counsel's confirmation. Erasure from backups happens by expiry; restored backups re-apply pending erasures before use.

## 5. Audit trail

v6 required all logs to be append-only and immutable for 7 years and also required erasure rights, and it placed the audit store on a log-search cluster. Two corrections: the **audit trail** (business accountability) is separated from **operational logs** (debugging); and the audit trail never contains raw personal data, so immutability and erasure do not conflict.

### 5.1 What is recorded

| Stream | Events | Read access |
|---|---|---|
| Financial | Every journal entry, payment, refund, payout, hold, adjustment, reconciliation decision | Finance Manager, Compliance |
| Admin actions | Every admin write and every reveal of masked data: user, role, time, IP, device, action, target, before/after (non-personal fields) or changed-field names (personal fields) | Super Admin, Compliance |
| Seller actions | Price, stock, offer, settings, payout-destination and staff changes | Seller Manager, Compliance; the seller sees their own |
| Security | Logins, failures by pattern, 2FA changes, session revocations, permission changes, break-glass | Super Admin, Compliance |
| Risk | Score changes, flags, overrides with justification | Fraud/Risk Manager, Compliance |
| Disputes and returns | State changes, evidence references, decisions, accounting links | Support, Finance, Compliance |
| Orders | Every state transition with actor and reason | Support, Logistics, Compliance |
| Configuration | Every `cfg:` change and feature-flag change | Super Admin, Compliance |

### 5.2 Integrity

- AUD-1 Audit records are written to an append-only schema; the application role can insert only. No role, including Super Admin, can update or delete through the application.
- AUD-2 Records are hash-chained per stream (each record stores the hash of the previous one).
- AUD-3 Every hour new records are exported to object storage with Object Lock in compliance mode (write once, read many) in a separate cloud account; a copy goes to the backup location.
- AUD-4 A daily checkpoint (latest hash per stream) is signed with a managed asymmetric key and stored with the export. A verification job recomputes the chain weekly and alerts on mismatch.
- AUD-5 Audit writes for financial and admin actions happen in the same transaction as the action; an action that cannot be audited does not commit.

### 5.3 Personal data in audit records

- AUD-6 Audit records reference people by account ID, order ID and similar pseudonymous identifiers. They never contain names, phone numbers, emails, addresses, document numbers or document images.
- AUD-7 Where a personal value must be evidenced (for example which payout account was changed), the record stores a keyed hash or an encrypted value under a per-subject key; erasure is performed by destroying that key (crypto-shredding).

## 6. Operational logs

- Structured JSON with trace ID, module, severity and pseudonymous user context; no personal data or secrets (SEC-21).
- Shipped through OpenTelemetry to the observability platform; retention per §4.
- Access limited to engineering roles; not a source of business truth.

## 7. Acceptance criteria

- A deletion request for an account with completed orders results in an anonymised profile, intact financial records, and no personal data in any audit record.
- Tampering with an exported audit file or a database audit row is detected by the verification job.
- An attempt to update or delete an audit row with the application's database role fails.
- No marketing message is sent without a matching consent record.
