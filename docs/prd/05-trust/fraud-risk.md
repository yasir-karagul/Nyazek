# Fraud & Risk

**Authoritative for:** risk scoring, risk tiers and their effects, the COD risk engine, COD confirmation, seller-side risk, self-dealing detection, case handling.
**Related:** [checkout-orders](../02-commerce/checkout-orders.md) · [payments](../04-finance/payments.md) · [returns-disputes](../02-commerce/returns-disputes.md) §7 · [identity-access](identity-access.md) · [privacy-audit](privacy-audit.md)

---

## 1. Approach

- RSK-1 The launch engine is **rule-based and explainable**: weighted rules produce a score and a list of the signals that fired. Machine-learned models are P2, once labelled outcome data exists.
- RSK-2 Rules, weights and thresholds are configuration owned by the Fraud/Risk Manager, versioned and audited.
- RSK-3 Risk assessment runs synchronously in the place-order flow with a 300 ms budget. If the Risk module is unavailable: COD orders are treated as Medium (confirmation required) and prepaid orders proceed; the fallback is logged.

## 2. Signals

| Dimension | Signals |
|---|---|
| Account | Age, verified identifiers, completed orders, refused or failed deliveries, return and dispute history, claimed or guest-created |
| Device | First-party device ID, device seen on other accounts, previously flagged device |
| Order | Value against the customer's history and category norms, velocity, first order on COD, high-resale items, many units of one item |
| Network | IP reputation, proxy or VPN indication, many accounts from one IP. IP location is a weak signal on Iraqi mobile networks and carries low weight |
| Address and phone | Address or phone linked to refused deliveries, to blocked accounts, or to many accounts |
| Relationships | Links between customer and seller accounts (§5) |

Device identification uses a first-party identifier and basic signals at launch; its use is disclosed in the privacy policy and it is not used for advertising. Commercial fingerprinting is a P2 option.

## 3. Risk tiers

| Tier | Effect |
|---|---|
| Low | No restriction |
| Medium | COD allowed with reduced limits and mandatory COD confirmation; order monitored |
| High | COD not offered (prepaid only); order may be held `ON_HOLD` for manual review |
| Blocked | Account suspended pending investigation; open sub-orders not yet released to the seller stay `ON_HOLD`, later ones are reviewed for cancellation (`RISK_REJECTED` before shipping) |

- RSK-4 Tier boundaries are score thresholds set in configuration and tuned in the closed beta.
- RSK-5 Crossing a threshold opens a review item without automatically blocking, except for the Blocked tier, which requires a rule marked as blocking or a manual decision.
- RSK-6 Manual review SLA: `cfg:risk.review_sla_hours` (default 12); the sub-order stays `ON_HOLD` meanwhile and the seller's SLA clock does not run.
- RSK-7 A customer can contest a restriction through Support; the Fraud/Risk Manager decides and may override.
- RSK-8 Every override records admin, reason and time in the audit trail; overriding a Blocked account requires dual control.

## 4. COD risk engine

COD eligibility and limits are decided at quote time, so an ineligible customer never sees COD offered.

| Control | Default |
|---|---|
| COD orders per day for new accounts | `cfg:cod.new_account_daily_orders` (default 2) |
| COD order value cap for new accounts | `cfg:cod.new_account_max_value` (default 250,000) |
| Maximum open (undelivered) COD value per customer | `cfg:cod.max_open_value` (default 500,000) |
| Limits rise with delivered-order history | Tiers in configuration |
| COD suspended after refused or failed deliveries | `cfg:cod.suspend_after_failed` (default 2 in the last 5 COD orders) |
| COD availability per governorate, district, category and seller | Serviceability and admin settings |

"New account" means fewer than `cfg:cod.new_account_delivered_orders` (default 2) delivered orders.

### 4.1 COD confirmation (P0)

The most effective single control against failed COD deliveries.

- CODC-1 Confirmation is required for COD orders at Medium tier and, by default, for every customer's first COD order (`cfg:cod.confirm_first_order` (default true)).
- CODC-2 The customer confirms through an SMS link (one tap) or by replying; an automated voice call is the P1 fallback. Support can confirm manually after a phone call.
- CODC-3 The sub-orders stay `ON_HOLD` and invisible to sellers until confirmed. Unconfirmed orders are cancelled with reason `COD_UNCONFIRMED` after `cfg:cod.confirmation_window_hours` (default 24); a reminder is sent halfway.
- CODC-4 Confirmation rate is a tracked KPI.

## 5. Seller-side and relationship risk

- Self-dealing: a seller buying their own products, or reviewing them, through a customer account. Detected by shared device, phone, address, payout or refund account, or identity-document signals between customer and seller accounts. Effects: reviews blocked, orders excluded from ranking and performance signals, case opened.
- Fake-order patterns: abnormal sales velocity, repeated customer–seller pairs, orders cancelled after ranking benefit.
- Listing manipulation, counterfeit reports, off-platform dealing attempts in messages.
- Collusive refunds and courier–seller collusion on COD.
- Payout risk: payout-destination change followed by an unusual payout; many sellers sharing one destination.

A seller risk case can place a wallet hold and, with dual control, suspend the seller ([commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §4).

## 6. Cases and lists

- A case groups related flags on a subject (customer, seller, device, address) with timeline, evidence, decision and outcome label. Outcome labels are kept to train future models.
- Blocklists for devices, phones, addresses and refund accounts are maintained by the Fraud/Risk Manager; entries have a reason and an expiry or review date.
- Chargebacks, confirmed fraud and confirmed abuse feed back into scores.

## 7. Metrics

COD confirmation rate, RTO rate by tier, governorate, category and seller, fraud-flag rate, false-positive rate (overridden flags), chargeback rate, value held and released, review SLA compliance.

## 8. Acceptance criteria

- A customer over the COD limits is not offered COD at checkout and cannot place a COD order through the API.
- An unconfirmed COD order is cancelled automatically and its stock released.
- With the Risk module stopped, checkout still works under the fallback rule.
- A review from an account linked to the seller is blocked.
