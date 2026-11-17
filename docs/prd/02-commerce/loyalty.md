# Loyalty & Referrals

**Priority:** P1 (launch target; may ship within 30 days after launch). The quote engine, order lines and ledger carry the loyalty fields from P0 so the programme can be switched on without schema changes.
**Authoritative for:** points earning, redemption, tiers, expiry, refund effects, customer referrals, birthday reward, seller referral programme.
**Related:** [checkout-orders](checkout-orders.md) §4 · [pricing-promotions](pricing-promotions.md) · [ledger-reconciliation](../04-finance/ledger-reconciliation.md) · [fraud-risk](../05-trust/fraud-risk.md)

---

## 1. Points ledger

- LOY-1 Points are recorded in an append-only points ledger per customer account; the balance is derived. Entries: `EARN_PENDING`, `EARN_CONFIRMED`, `REDEEM`, `RESTORE`, `REVERSE`, `EXPIRE`, `ADJUST`.
- LOY-2 Admin adjustments require a reason and are audited; adjustments above `cfg:loyalty.adjust_dual_control_points` (default 50,000) need dual control.
- LOY-3 Only claimed accounts ([customer-account](customer-account.md) CUS-1) can redeem. Guest-created accounts accrue points that become usable once claimed.

## 2. Earning

- LOY-4 Points are earned on the cash actually paid for items: line value after seller coupons, platform coupons and loyalty redemption. No points on shipping fees, COD fees or tax.
- LOY-5 Earn rate = `cfg:loyalty.base_points_per_1000_units` (default 10, points per 1,000 units of the market currency) × category multiplier × tier multiplier. Category multipliers are set by the Marketing Manager.
- LOY-6 Points are recorded as pending at delivery and become usable only when the sub-order is `COMPLETED` and its return window has closed.
- LOY-7 The cost of points is recognised when they are confirmed (posting JE-27).

## 3. Redemption

- LOY-8 Redemption rate: `cfg:loyalty.value_per_point` (default 1, in the market currency's minor unit), meaning 1,000 points = 1,000 IQD in Iraq.
- LOY-9 Maximum redemption per order: `cfg:loyalty.max_redeem_percent` (default 20%) of the eligible product value.
- LOY-10 Points cannot be redeemed on a sub-order that carries a seller coupon; they can be combined with a platform coupon ([pricing-promotions](pricing-promotions.md) §2.2).
- LOY-11 Redemption is validated and committed server-side inside the place-order flow; the redeemed amount is rounded per MON-5.
- LOY-12 Redemption is platform-funded (posting JE-4). Sellers receive full proceeds.

## 4. Tiers

v6 defined tiers by "points range" without saying whether that meant the spendable balance (which would demote a customer for redeeming) or something else. Tiers are based on **qualifying points**: points confirmed in the previous 12 months, regardless of redemption.

| Tier | Qualifying points (12 months) | Perks |
|---|---|---|
| Bronze | 0 – 999 | Base earn rate |
| Silver | 1,000 – 4,999 | Higher earn multiplier; lower free-delivery threshold |
| Gold | 5,000 and above | Highest earn multiplier; priority support; exclusive deals; birthday reward |

- LOY-13 Tiers are evaluated daily. An upgrade is immediate; a downgrade takes effect at the next monthly evaluation.
- LOY-14 Thresholds, multipliers and the tier free-delivery thresholds are configuration; values are ratified under D-34.

## 5. Expiry, cancellation and refund effects

- LOY-15 Points expire after 12 months without any earn or redeem activity on the account. A reminder is sent 30 days before expiry.
- LOY-16 On cancellation or refund: points earned on the affected value are reversed (a balance may become negative and is settled against future earnings); points redeemed on the affected value are restored unless they would already have expired.
- LOY-17 Expired and reversed points reduce the liability (posting JE-28).

## 6. Customer referrals

- Each claimed customer account has a referral code and link.
- The referrer and the new customer each receive `cfg:loyalty.referral_points` (default 0, set under D-34) when the new customer's first order is `COMPLETED` and its return window has closed.
- Controls: one reward per new customer; self-referral blocked by phone, device, address and payment-instrument signals; a cap of `cfg:loyalty.referral_monthly_cap` (default 20) rewarded referrals per referrer per month; suspicious clusters go to Risk.

## 7. Birthday reward

- Date of birth is optional profile data, used only for this reward and for confirming the customer is an adult; it can be changed at most once.
- Gold members receive a coupon or bonus points in their birthday month (value under D-34).

## 8. Seller referral programme (P1)

- Each approved seller has a referral link.
- The referring seller receives a wallet bonus of `cfg:sellers.referral_bonus` (default 0, set by the owner) when the referred seller is approved and their first sale has cleared its return window (posting JE-29).
- Self-referral is blocked using identity-document, payout-account, phone, device and IP signals.

## 9. Abuse and governance

- Order cycling (buy, earn, return), referral rings and points farming through linked accounts are flagged to Risk.
- The points liability is reported to Finance daily ([data-analytics](../06-platform/data-analytics.md)).
- Programme terms are published and versioned; changes that reduce the value of earned points require notice per counsel's advice.

## 10. Acceptance criteria

- Points never become spendable before the return window closes.
- Redeeming points never demotes a tier.
- For any sequence of earn, redeem, partial refund and expiry, the points ledger and the Loyalty Points Liability account agree.
