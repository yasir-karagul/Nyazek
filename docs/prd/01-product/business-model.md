# Business Model & Unit Economics

**Authoritative for:** revenue streams, planning assumptions, 1P/3P revenue recognition, per-order economics and who bears which cost.
**Related:** [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) · [ledger-reconciliation](../04-finance/ledger-reconciliation.md) · [logistics](../02-commerce/logistics.md) · [open-decisions](../00-governance/open-decisions.md)

---

## 1. Planning assumptions

These are planning figures, to be replaced by measured data after the closed beta.

| Assumption | Value | Status |
|---|---|---|
| Blended take rate (commission ÷ 3P GMV) | 12%–18% | Not yet supported by a rate schedule (D-20) |
| Average order value | 50,000–100,000 IQD | Planning range |
| COD share of orders | Majority | To be measured |
| COD RTO rate | 25% (conservative) | Reduction target through COD confirmation and risk controls |
| Free-delivery threshold, shipping rate card, COD fee | Not set | D-21 |

USD equivalents are not used anywhere in the product; in Iraq Nyazek prices and settles in IQD only. The model in this document is the Iraq model; each later market has its own (one currency per market, MKT-3).

## 2. Revenue streams

| Stream | Recognition | Priority |
|---|---|---|
| 3P commission | At escrow release | P0 |
| 1P product sales | At escrow release; cost of goods recognised with the sale | P0 |
| Shipping fees charged to customers | At delivery | P0 |
| Sponsored ads (CPC) | When a click is validated and billed | P1 |
| COD handling fee (optional) | At delivery | P1 |
| Seller subscriptions (advanced analytics, priority support) | – | P2 |

v6 listed "escrow float" as a revenue stream. It depends on a custody arrangement that is not confirmed (D-09) and is excluded from all plans.

## 3. Revenue recognition (IFRS 15)

| | 3P order (Nyazek as agent) | 1P order (Nyazek as principal) |
|---|---|---|
| Revenue | Commission only | Full item value |
| Cost of goods | None | Purchase cost |
| Inventory risk | Seller | Nyazek |
| Shipping | Nyazek contracts couriers and sets fees (treated as Nyazek's service; presentation confirmed by the accountant) | Same |

The accountant validates the treatment and timing before the ledger is frozen ([ledger-reconciliation](../04-finance/ledger-reconciliation.md)).

## 4. Per-order economics

| Line | 3P | 1P | Borne by |
|---|---|---|---|
| Item value | Passes to seller | Revenue | – |
| Commission | Revenue | – | Seller |
| Shipping fee from customer | Revenue | Revenue | Customer |
| Courier cost (outbound) | Cost | Cost | Nyazek |
| Free-delivery subsidy | Cost | Cost | Nyazek (D-21) |
| Payment processing fee | Cost | Cost | Nyazek |
| COD handling and remittance cost | Cost | Cost | Nyazek |
| Platform coupons, loyalty points | Cost | Cost | Nyazek |
| Seller coupons and deals | – | – | Seller (reduces proceeds and commission base) |
| Failed delivery (RTO) | Per cause ([logistics](../02-commerce/logistics.md) §7) | Nyazek or courier | Seller / Nyazek / courier |
| Return shipping | Per reason ([returns-disputes](../02-commerce/returns-disputes.md) §3) | Nyazek or customer | Seller / customer / Nyazek / courier |
| SMS and notifications | Cost | Cost | Nyazek |

### 4.1 Launch-gating analysis: contribution margin

Nyazek pays the courier for every 3P shipment, funds free delivery, and absorbs outbound and return cost on customer-refused COD parcels. At a 25% COD RTO rate, the logistics cost of failed orders can consume most of the commission earned on successful ones.

Worked illustration (placeholder numbers, not decisions): order value 60,000 IQD at 12% commission earns 7,200 IQD. If courier cost is 5,000 IQD outbound and the customer paid a 4,000 IQD shipping fee, the delivered order contributes about 6,200 IQD before payment and other costs. Each refused COD parcel costs roughly 5,000 IQD outbound plus a return charge with no revenue. With one failure for every three successes, a large part of the margin on the three successes is consumed.

Therefore, before commission rates (D-20) and shipping terms (D-21) are approved, Finance completes a contribution-margin model per category and governorate using real courier and PSP quotes. This model is a Phase 1 deliverable and a condition for launch pricing.

## 5. Levers designed into the product

| Lever | Where |
|---|---|
| COD confirmation, COD limits, risk tiers | [fraud-risk](../05-trust/fraud-risk.md) §4 |
| Optional COD fee; incentives for prepaid | [payments](../04-finance/payments.md) §7 |
| Free-delivery threshold and tier thresholds | [checkout-orders](../02-commerce/checkout-orders.md) §4 |
| Heavy-item surcharges; weight-based rate card | [logistics](../02-commerce/logistics.md) §4 |
| Commission by category, sub-category and product type | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §1 |
| Cost attribution for seller-fault failures and returns | [logistics](../02-commerce/logistics.md) §7 |
| Ads revenue | [advertising](../02-commerce/advertising.md) |

## 6. Financial reporting

Contribution margin per order, take rate, promotion and loyalty cost, logistics cost per order and per failure, payables ageing and funding position are standard Finance reports ([data-analytics](../06-platform/data-analytics.md) §5).
