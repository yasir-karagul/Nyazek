# Pricing Governance & Promotions

**Authoritative for:** price rules (floor, anti-dumping, MAP, 1P margin, reference price), coupons, deals, campaigns, discount stacking and funding.
**Related:** [catalog-listings](catalog-listings.md) · [checkout-orders](checkout-orders.md) §4 · [loyalty](loyalty.md) · [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md)

---

## 1. Price rules

Price rules are evaluated by the Catalog module on the offer's item price (shipping excluded) at offer creation, price update, bulk import and when a coupon or deal is created. All thresholds are configurable per category.

### 1.1 Price floor

- PRC-1 An offer below the category minimum price is rejected with an error; the seller must correct it.
- PRC-2 A seller coupon or deal cannot bring the effective price below the floor.

### 1.2 Anti-dumping

- PRC-3 An offer priced below `cfg:pricing.dumping_percent` (default 50%) of the reference for its product is held before going live and enters an admin queue. The reference is the median active offer price for the same variant; when fewer than 3 offers exist, the category median for the product type.
- PRC-4 The Catalog Manager approves, rejects or requests justification. Repeated violations are reported to seller performance as an authenticity concern.

v6 compared against the "category average", which is meaningless across products of very different prices (a cable and a phone are both Electronics).

### 1.3 MAP (minimum advertised price)

- PRC-5 MAP is set per product by an admin at the brand's request and applies to authorised distributors of that brand.
- PRC-6 An offer below MAP is rejected at submission and price update. Repeat attempts trigger a review of the brand authorisation.
- PRC-7 Counsel must confirm that MAP enforcement by the platform is permitted under Iraqi competition rules before it is enabled ([compliance-legal](../05-trust/compliance-legal.md)).

### 1.4 1P margin floor

- PRC-8 For 1P offers the Finance Manager and Super Admin are alerted when margin (price − cost) falls below `cfg:pricing.1p_margin_floor_percent` (default 10%). The alert is visible to the 1P Merchandiser, Finance Manager and Super Admin only.

### 1.5 Reference (strike-through) price

- PRC-9 A crossed-out original price may be shown only if the same offer was actually priced at or above it for at least `cfg:pricing.reference_min_days` (default 7) of the previous `cfg:pricing.reference_lookback_days` (default 30) days. The system computes eligibility from price history; sellers cannot type an arbitrary reference price.
- PRC-10 Violations are impossible by construction; attempts to manipulate history (brief price spikes) are a monitored pattern.

## 2. Promotion types

| Type | Created by | Funded by | Priority |
|---|---|---|---|
| Seller coupon | Seller; approved by Marketing Manager | Seller | P1 |
| Seller deal (time-limited price) | Seller | Seller | P1 |
| Platform coupon | Marketing Manager | Nyazek | P1 |
| Flash deal | Marketing Manager invites or sellers apply; countdown and quantity cap | Seller, unless Nyazek agrees a subsidy in writing | P1 |
| Seasonal campaign | Marketing Manager; CMS landing page (Ramadan, Eid Al-Fitr, Eid Al-Adha, Back to School, New Year, custom) | Per participating promotion | P1 |
| Free delivery above threshold | Platform setting | Nyazek (D-21) | P0 |

The quote engine and order model support discounts with a funder from P0 so that promotions can ship as a fast-follow without schema changes.

### 2.1 Coupon rules

- PRM-1 Fields: code, funder, type (percent or fixed amount), value, minimum spend, maximum discount, eligible scope (seller, category, brand, products), start and mandatory end date, total and per-customer usage limits.
- PRM-2 Seller coupons: percentage between `cfg:promo.seller_coupon_min_percent` (default 5) and `cfg:promo.seller_coupon_max_percent` (default 70); expiry required; must pass price-floor and MAP checks for every eligible offer.
- PRM-3 Redemption is atomic and counted inside the place-order flow; usage limits cannot be exceeded under concurrency.
- PRM-4 Coupon validation endpoints are rate-limited; codes are case-insensitive and at least 6 characters.
- PRM-5 Cancellation and refund effects follow ORD-7 ([checkout-orders](checkout-orders.md)).

### 2.2 Stacking

| Combination | Allowed |
|---|---|
| One seller coupon per sub-order | Yes |
| One platform coupon per order | Yes |
| Seller coupon + platform coupon | Yes, applied in that order |
| Loyalty redemption + platform coupon | Yes |
| Loyalty redemption on a sub-order with a seller coupon | No |
| Two coupons of the same kind | No |
| Coupon on top of a deal price | Yes, unless the deal is marked exclusive |

Order of application: item (deal) price → seller coupon → platform coupon → loyalty redemption.

### 2.3 Funding and commission

- Seller-funded discounts reduce the seller's proceeds and the commission base.
- Platform-funded discounts do not reduce the seller's proceeds; Nyazek covers them (posting JE-3) and commission is calculated on the pre-discount value ([commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §1.2).
- Loyalty redemption is platform-funded unless a seller has agreed in writing to fund a specific promotion.

## 3. Abuse controls

- Per-customer limits are enforced by account, phone and device signals.
- Multiple new accounts redeeming the same new-customer coupon from one device or address are flagged ([fraud-risk](../05-trust/fraud-risk.md)).
- Sellers buying their own products with platform coupons is a self-dealing signal.

## 4. Acceptance criteria

- No path (form, bulk import, coupon, deal) can produce an effective price below the floor or MAP.
- A strike-through price never appears for an offer that does not meet PRC-9.
- With 100 concurrent redemptions of a coupon limited to 10 uses, exactly 10 succeed.
- The seller's proceeds for a line are identical with and without a platform-funded coupon.
