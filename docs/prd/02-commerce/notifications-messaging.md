# Notifications & Messaging

**Authoritative for:** notification channels, event catalogue, consent and quiet hours, templates, delivery tracking, customer–seller messaging.
**Related:** [architecture](../06-platform/architecture.md) §4 · [privacy-audit](../05-trust/privacy-audit.md) · [mobile-flutter](../07-clients/mobile-flutter.md)

---

## 1. Channels

| Channel | Availability | Used for |
|---|---|---|
| In-app inbox (Storefront account, Seller Dashboard, Admin Panel) | P0 | Every notification |
| Email | P0 | Transactional, security, documents; promotional with opt-in |
| SMS | P0 | OTP and security, COD confirmation, delivery-critical messages; promotional only with opt-in |
| Automated voice call | P1 | COD confirmation fallback |
| Web push | P1 | Customers and sellers who grant permission |
| Mobile push (FCM, APNs through FCM) | With the Flutter apps (P2); device-token registry and push abstraction are P0 readiness items | All classes |

v6 said all events go out by "push, email and Arabic SMS". There is no native app at launch, so push at launch means the in-app inbox (and web push at P1). SMS is the most expensive channel and is reserved for messages that must reach a phone.

## 2. Classes and rules

| Class | Can the user disable it? | Quiet hours |
|---|---|---|
| Security (OTP, password/email/phone change, new device) | No | None |
| Transactional (orders, payments, delivery, returns, refunds, payouts, KYC) | No (channel fallbacks apply) | None, except non-urgent seller reminders |
| Informational (review reminder, points earned, new Q&A) | Yes | Yes |
| Promotional (flash deals, price drops, campaigns) | Opt-in required | Yes |
| Operational (admin alerts) | By role | None |

- NTF-1 Promotional messages require explicit opt-in consent per channel, recorded with timestamp and policy version ([privacy-audit](../05-trust/privacy-audit.md) §2). Every promotional email has an unsubscribe link; promotional SMS carries opt-out instructions.
- NTF-2 Quiet hours: no informational or promotional SMS or push between `cfg:notifications.quiet_start` (default 22:00) and `cfg:notifications.quiet_end` (default 08:00) in the market's time zone (Asia/Baghdad for Iraq); messages are queued. Quiet hours, sender IDs and templates are held per market.
- NTF-3 Messages are sent in the user's language preference; Arabic is the default.
- NTF-4 Frequency caps: at most `cfg:notifications.promo_max_per_day` (default 2) promotional messages per user per channel per day.
- NTF-5 Each message is recorded with status per channel (`QUEUED`, `SENT`, `DELIVERED`, `FAILED`) and is visible to Support in the delivery log.
- NTF-6 A notification is requested by publishing `notification.requested` with a template key and data; the Notifications module resolves recipients' contact details itself, so other modules and the event log never carry personal data.
- NTF-7 Deduplication: the same template for the same reference is not sent twice within its dedupe window.

## 3. Catalogue

P0 unless marked. "Inbox" is always included.

### 3.1 Customer

| Event | Channels | Class |
|---|---|---|
| OTP, verification, password/email/phone change, new device | SMS, email | Security |
| Order placed; payment pending, failed or expired | Email, SMS | Transactional |
| COD confirmation request | SMS (voice call P1) | Transactional |
| Order cancelled (any reason) | Email, SMS | Transactional |
| Shipped; out for delivery; delivery attempt failed | SMS, email | Transactional |
| Delivered (with receipt link) | Email | Transactional |
| Return status changes; refund processed | Email, SMS for refund | Transactional |
| Refund account needed (COD refund with no verified account); refund destination rejected; refund failed and under review (PAY-21) | SMS, email | Transactional |
| Order expired, with "restore to cart" (ORD-16, PAY-9) | Email, SMS | Transactional |
| Safety recall of a product received (PRH-5) | SMS, email | Transactional |
| Dispute opened, updated, resolved | Email | Transactional |
| Review reminder | Email | Informational |
| Loyalty points earned or expiring (P1) | Email | Informational |
| Price drop on a favourite; favourite back in stock (P1) | Email, web push | Promotional |
| Flash deal and campaign alerts (P1) | Email, web push; SMS only with SMS opt-in | Promotional |

### 3.2 Seller

| Event | Channels | Class |
|---|---|---|
| OTP, security events | SMS, email | Security |
| New order (SLA started); SLA reminders at 50% and 90%; SLA breach | Dashboard live update, email, SMS for the 90% reminder | Transactional |
| Customer cancelled before shipping | Dashboard, email | Transactional |
| RTO parcel delivered back: confirm receipt within the window (logistics §9) | Dashboard, email | Transactional |
| Seller-fault charge or courier compensation posted to the wallet | Dashboard, email | Transactional |
| Offer suspended (recall, violation, licence lapse); seller state changed (SEL-4) | Dashboard, email, SMS for suspension | Transactional |
| Payout returned after execution | Dashboard, email | Transactional |
| Return requested; return received; inspection due; dispute response due | Dashboard, email | Transactional |
| Payout executed or failed; commission invoice issued | Dashboard, email | Transactional |
| KYC decision; document expiring; listing approved or rejected | Dashboard, email | Transactional |
| Performance warning or level change; price-rule violation | Dashboard, email | Transactional |
| Low stock; new Q&A (P1); new message (P1); staff invitation (P1) | Dashboard, email | Informational |

### 3.3 Admin

| Event | Channels |
|---|---|
| Queue backlog or SLA breach (KYC, catalogue, moderation, disputes, refunds) | Admin inbox, email |
| Reconciliation mismatch, ledger invariant failure, payout failure | Admin inbox, email, pager |
| Daily reconciliation awaiting sign-off (REC-6); chargeback received (P1) | Admin inbox, email |
| Unallocated receipt refunded automatically (PAY-20) | Admin inbox |
| Fraud flag, risk case | Admin inbox |
| Dual-control approval requested | Admin inbox, email |

Pager alerts for engineering are defined in [reliability-sre](../06-platform/reliability-sre.md) §3.

## 4. Templates

- Templates are managed in the CMS by the Content Manager, per channel and language, with versioning and preview. Transactional templates expose only whitelisted variables.
- SMS templates fit within two segments (Arabic uses 70 characters per segment); sender ID and template registration with carriers are handled through the aggregator (D-29).
- Email is sent from an authenticated domain (SPF, DKIM, DMARC enforced) with separate sub-domains for transactional and promotional mail.
- All templates are RTL-correct in Arabic and tested with long names and mixed-direction content.

## 5. Provider resilience

- SMS: primary and fallback aggregator behind `SmsPort`; automatic failover on error rate; OTP delivery success rate is a paged metric.
- Email: bounce and complaint handling; suppressed addresses are not retried.
- Critical transactional messages fall back from push to SMS when push is not delivered within 60 seconds (once push exists).

## 6. Customer–seller messaging (P1)

- One thread per sub-order, opened by the customer from the order page or by the seller from the order detail. No pre-purchase messaging at launch (use product Q&A).
- Text and images only; contact details, links and payment requests are blocked by the same pre-screen used for reviews, and attempts are flagged to Risk (off-platform dealing).
- Threads close 30 days after the sub-order reaches a terminal state.
- Support and dispute handlers can read a thread when a ticket or dispute references the sub-order; this is stated in the privacy policy.
- Seller response time (first response within the thread) feeds the performance score once messaging is live ([seller-performance](../03-sellers/seller-performance.md) §1).

## 7. Acceptance criteria

- No promotional message is sent to a user without a recorded opt-in for that channel, or during quiet hours.
- Disabling all optional preferences still delivers OTP and order messages.
- A failing primary SMS provider triggers failover without lost OTPs (chaos test in staging).
