# Seller Performance

**Authoritative for:** performance metrics and score, consequence levels, fairness rules, appeals.
**Related:** [checkout-orders](../02-commerce/checkout-orders.md) §7 · [search-buy-box](../02-commerce/search-buy-box.md) · [seller-accounts-kyc](seller-accounts-kyc.md) §5 · [seller-dashboard](seller-dashboard.md)

---

## 1. Metrics and weights

| Metric | Definition (rolling 30 days) | Weight |
|---|---|---|
| Cancellation rate | Sub-orders cancelled with a seller-attributed reason (`SELLER_REJECTED`, `SELLER_CANCELLED`, `SLA_CONFIRM_TIMEOUT`, `SLA_SHIP_TIMEOUT`) ÷ sub-orders released to the seller | 30% |
| Seller rating | Average of published seller ratings | 25% |
| Late shipment rate | Sub-orders reaching `READY_TO_SHIP` after the shipment SLA, or with a seller-caused pickup failure ÷ sub-orders shipped | 20% |
| Return / refund rate | Sub-orders with a return or refund attributed to the seller (defective, wrong item, not as described) ÷ delivered sub-orders | 15% |
| Response time | Median first-response time to customer messages (active once messaging is live; neutral until then) | 5% |
| Authenticity | Verified counterfeit or fraud complaints | 5% + override |

Each metric is normalised to 0–100 by the mapping below, linear between the two points. The table is configuration (`cfg:performance.mapping` (default as in the table below)), reviewed during the closed beta.

| Metric | 100 points at | 0 points at | When there is no data |
|---|---|---|---|
| Cancellation rate | 0% | ≥ 10% | Excluded |
| Seller rating | 5.0 | ≤ 3.0 | Excluded (no published ratings) |
| Late shipment rate | 0% | ≥ 10% | Excluded |
| Return / refund rate | 0% | ≥ 8% | Excluded |
| Response time | ≤ 2 hours | ≥ 24 hours | Excluded (always, until messaging is live) |
| Authenticity | No verified complaint | One or more verified complaints | – (always computed) |

The score is the weighted sum of the computed metrics; when a metric is excluded, the remaining weights are scaled up proportionally so they sum to 100%. The minimum-sample rule PRF-2 applies before this.

## 2. Calculation rules

- PRF-1 Window: the most recent 30 days. Recomputed hourly and on relevant events.
- PRF-2 **Minimum sample:** a score is computed only if the seller had at least `cfg:performance.min_orders` (default 10) sub-orders in the window. Otherwise the score is the neutral value 50 and the dashboard shows "not enough data". This single rule replaces v6's separate "inactivity decay" rule.
- PRF-3 **Grace period:** during the first 30 days after approval a seller receives no automatic consequence levels; metrics are shown for information.
- PRF-4 **Exclusions** (recorded with a reason): cancellations and returns caused by the customer (customer cancelled, unreachable, refused, change of mind), by proven courier failure, by Nyazek (risk rejection, unconfirmed COD, admin action), or during an admin-declared force majeure.
- PRF-5 The seller's SLA clocks do not run during `ON_HOLD` or `AWAITING_PAYMENT` ([checkout-orders](../02-commerce/checkout-orders.md) SLA-2).
- PRF-6 Ratings removed by moderation are excluded.
- PRF-7 The 1P store's score is computed with the same metrics and rules and is used as its Buy Box and search input, so 1P gains no advantage beyond the capped 1P component ([search-buy-box](../02-commerce/search-buy-box.md) §2.3). Consequence levels, appeals and seller states do not apply to it; a 1P score below the Level 1 band alerts the 1P Operations Manager.

## 3. Consequence levels

| Level | Trigger (score below) | Effect |
|---|---|---|
| 1 Warning | `cfg:performance.level1_below` (default 70) | Notification with metric breakdown |
| 2 Reduced visibility | `cfg:performance.level2_below` (default 60) | Search performance signal set to 0; Buy Box performance component × `cfg:buybox.level2_factor` (default 0.85); payouts revert to monthly |
| 3 Listing restriction | `cfg:performance.level3_below` (default 50) | No new offers; not eligible for the Buy Box; seller state `RESTRICTED` |
| 4 Suspension review | `cfg:performance.level4_below` (default 40) | Case opened for the Seller Manager; suspension requires dual control |

Band values are proposals to be set during the closed beta and written into the Seller Agreement.

- PRF-8 **Authenticity override:** one verified counterfeit complaint moves the seller straight to a Level 4 review regardless of score.
- PRF-9 **Recovery:** Levels 1–3 lift automatically when the score has stayed above the band for `cfg:performance.recovery_days` (default 14) consecutive days. Level 4 lifts only by admin decision.
- PRF-10 **Repeat offences:** a seller who re-enters the same level within 60 days is escalated one level.
- PRF-11 Levels 1–3 are applied automatically; every automatic consequence is explainable: the seller sees the metrics and the specific orders behind it.

v6 combined a 30-day window with "recovery over 60 days", which cannot both hold: old data leaves a 30-day window after 30 days. PRF-9 and PRF-10 give the two figures distinct, compatible meanings.

## 4. Appeals

- A seller can appeal a level, a metric attribution (for example a failed pickup blamed on them) or a specific order's inclusion.
- The Seller Manager decides within `cfg:performance.appeal_sla_hours` (default 48) and records the reason. A successful appeal removes the affected orders from the metric and recomputes the score.
- Appeals are P1 as a dashboard feature; at launch they are submitted through Support with the same SLA.

## 5. Visibility

- The seller's dashboard shows the live score, each metric with its value and normalised points, SLA history, current level, time to recovery, and the list of orders counted against them.
- Admins see scores, levels, overrides and trends for all sellers.
- Customers see the seller's rating, not the performance score.

## 6. Acceptance criteria

- A seller with one cancelled order out of two shows "not enough data", not a 50% cancellation rate.
- A customer-refused delivery does not change any seller metric.
- Level changes always carry a list of contributing orders.
- A granted appeal changes the score at the next recompute.
