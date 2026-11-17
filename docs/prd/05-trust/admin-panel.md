# Admin Panel

**Authoritative for:** the Admin Panel as an application: its modules and priorities, the catalogue of operational queues with their owners and service levels, and the behaviour rules common to all admin screens.
**Related:** [admin-governance](admin-governance.md) (roles, permissions, dual control) · [web-apps](../07-clients/web-apps.md) §5 · [sitemap](../09-information-architecture/sitemap.md) §8 (page IDs `AD-*`) · page specifications: the `pages-admin-*` documents in [09-information-architecture](../09-information-architecture/README.md) · [navigation](../09-information-architecture/navigation.md) §3 · [release-plan](../00-governance/release-plan.md) §6

The rules each queue applies live in the domain documents. This document says which queues exist, who owns them and how every admin screen behaves, so that the panel is built consistently.

---

## 1. Modules

| Module | Sitemap | Main roles | Priority | Domain rules |
|---|---|---|---|---|
| Sign-in, dashboard, approvals inbox | §8.1 | All | P0 | [admin-governance](admin-governance.md) §3–4 |
| Users and roles (customers, sellers, admins) | §8.2 | Support, Seller Manager, Super Admin | P0 | [identity-access](identity-access.md), [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) |
| Catalogue | §8.3 | Catalog Manager | P0 | [catalog-listings](../02-commerce/catalog-listings.md), [pricing-promotions](../02-commerce/pricing-promotions.md) |
| 1P merchandising | §8.4 | 1P Merchandiser | P0 | [first-party-operations](../03-sellers/first-party-operations.md) |
| Orders and logistics | §8.5 | Support, Logistics | P0 | [checkout-orders](../02-commerce/checkout-orders.md), [logistics](../02-commerce/logistics.md) |
| Returns and disputes | §8.6 | Support, Finance | P0 | [returns-disputes](../02-commerce/returns-disputes.md) |
| Finance | §8.7 | Finance | P0 | [04-finance](../04-finance/ledger-reconciliation.md) |
| Fraud and risk | §8.8 | Fraud/Risk | P0 | [fraud-risk](fraud-risk.md) |
| Promotions, loyalty, ads | §8.9 | Marketing | P1 (1P pricing rules, `AD-PRO-PRICING`, P0) | [pricing-promotions](../02-commerce/pricing-promotions.md), [loyalty](../02-commerce/loyalty.md), [advertising](../02-commerce/advertising.md) |
| Reviews, support, CMS | §8.10 | Support, Content | P0 | [reviews-qa](../02-commerce/reviews-qa.md), [support-cms](../02-commerce/support-cms.md) |
| Notifications, analytics, privacy | §8.11 | Marketing, Compliance, all | P0 | [notifications-messaging](../02-commerce/notifications-messaging.md), [data-analytics](../06-platform/data-analytics.md), [privacy-audit](privacy-audit.md) |
| Platform settings, audit viewer | §8.12 | Super Admin (Finance for the commission schedule); owning roles review ([admin-governance](admin-governance.md) §5) | P0 | [admin-governance](admin-governance.md) §5, [configuration-register](../00-governance/configuration-register.md) |

## 2. Queue catalogue

Every queue is a P0 work surface unless marked. "Target" is the configured service level whose breach alerts the owner.

| Queue | Owner role | Target | Rules |
|---|---|---|---|
| Seller applications (KYC) | Seller Manager | `kyc.review_sla_hours` | KYC-1 to KYC-8 |
| New-product requests | Catalog Manager | `catalog.review_sla_hours` | CAT-5 |
| Price-rule violations (anti-dumping holds) | Catalog Manager | Same day | PRC-3, PRC-4 |
| Listing reports and IP notices | Catalog Manager | 24 hours; immediate for safety | PRH-1, PRH-2 |
| Unconfirmed COD orders | Support | Within the confirmation window | CODC-2, CODC-3 |
| Risk review | Fraud/Risk Manager | `risk.review_sla_hours` | RSK-5, RSK-6 |
| Order and shipment exceptions | Logistics Manager | `orders.stuck_alert_hours` | ORD-10, ORD-11, SHP-1, SHP-4 |
| COD remittance exceptions | Logistics Manager with Finance | Per remittance | COD-3 to COD-5 |
| Returns oversight | Support | Timers of the return machine | RET-3 |
| Disputes | Support; Finance above the limit | `disputes.decision_hours` | DSP-1 to DSP-4 |
| Refunds (manual disbursement) | Finance Manager | `refunds.execution_sla_days` | PAY-14, PAY-15 |
| Reconciliation exceptions | Finance Manager | Same day | REC-1 to REC-3 |
| Failed payouts | Finance Manager | Next payout run | PO-6 |
| Review moderation | Support | `reviews.moderation_sla_hours` | Moderation table |
| Support tickets | Support | `support.customer_first_response_hours`, `support.seller_first_response_hours` | SUP-4, SUP-5 |
| Data-subject requests | Compliance | `privacy.dsr_sla_days` | DSR-1 |
| Dual-control approvals | Approving roles | `backoffice.approval_ttl_hours` | DC-1 |
| 1P restock and receiving tasks | 1P Merchandiser | Same day | FP-5, FP-11 |
| Seller appeals (P1) | Seller Manager | `performance.appeal_sla_hours` | Appeals |
| Seller coupon approvals, ad moderation, Q&A moderation (P1) | Marketing, Support | 24 hours | PRM-2, ad policy, Q&A |

## 3. Behaviour common to all admin screens

- ADM-1 **Queues** show age and time to target for every item, sort oldest-at-risk first by default, and support claim and release so two people never work the same item. An item claimed and untouched for 30 minutes returns to the queue.
- ADM-2 **Decisions** that reject, restrict, refund or override require a reason code from a managed list, plus a free-text note where the code is "other". The reason shown to the customer or seller is a translated, externally safe text mapped to the code, never the internal note.
- ADM-3 **Bulk actions** show the count and a summary before confirmation, run as background jobs, and report per-item results. Bulk actions never bypass dual control: each item that needs approval creates its own request.
- ADM-4 **Search**: a global search finds orders, sub-orders, shipments, customers, sellers, tickets, returns and disputes by their identifiers. Searching by phone number or email is restricted to roles with the permission and is logged.
- ADM-5 **Personal data** is masked by default and revealed per record with a reason (RBAC-4). Exports are background jobs scoped by role, logged, and subject to the bulk-export approval ([admin-governance](admin-governance.md) §3).
- ADM-6 **Acting for a customer**: Support may create a ticket, a return request or a cancellation on behalf of a customer who phones, after verifying the caller with an OTP sent to the account's phone. The record shows it was created by staff. Support never places orders, changes refund destinations or changes login identifiers on a caller's behalf.
- ADM-7 **View as seller** (P1): Seller Manager and Support may open a read-only view of a seller's dashboard to help with a ticket. Nothing can be changed in this mode; each use is audited and visible to the seller in the activity log.
- ADM-8 **History**: every entity page (order, seller, product, return, dispute, payout) shows its full timeline from the audit trail, including automated actions.
- ADM-9 **Internal notes** can be attached to orders, sellers, customers and cases. They are never shown outside the Admin Panel and are subject to data-subject access rules as decided by counsel.
- ADM-10 **Dashboards** are built per role from the Analytics read models; a role sees only the widgets its permissions allow.
- ADM-11 **Platform calendar**: Super Admin maintains platform holidays and force-majeure declarations that pause seller SLA clocks (SLA-1), by governorate where needed.
- ADM-12 The panel works in Arabic and English, is desktop-first (minimum width 1280 px) and remains usable at tablet width for queue work.

## 4. Acceptance criteria

- Two admins cannot decide the same queue item; the second sees it as claimed.
- No decision that needs a reason code can be saved without one, through the panel or the API.
- Revealing a masked value, searching by phone, exporting data and using view-as-seller each leave an audit record.
- Every queue in §2 shows its target and raises its breach alert in staging tests.
