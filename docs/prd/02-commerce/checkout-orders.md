# Cart, Checkout & Orders

**Authoritative for:** customer addresses, cart, checkout session, price calculation (quote), order data model, place-order flow, sub-order state machine, seller order SLAs, cancellation, order edge cases.
**Related:** [inventory](inventory.md) · [payments](../04-finance/payments.md) · [logistics](logistics.md) · [returns-disputes](returns-disputes.md) · [pricing-promotions](pricing-promotions.md) · [fraud-risk](../05-trust/fraud-risk.md) · [seller-performance](../03-sellers/seller-performance.md)

---

## 1. Customer addresses

Iraq has no reliable postal-code or street-naming system; addresses are structured for couriers.

| Field | Rule |
|---|---|
| Governorate | Required; one of the 19 governorates (including Halabja) |
| District | Required; from reference data for the governorate |
| Neighbourhood | Required; from reference data, or free text when not listed |
| Nearest landmark | Required free text |
| Street / house details | Optional free text |
| Map pin | Optional (P1) |
| Recipient name | Required |
| Primary phone | Required; a mobile number valid for the market (Iraqi ranges at launch) in E.164; defaults to the account's verified phone |
| Secondary phone | Optional |
| Delivery notes | Optional |

- ADR-1 The geo reference dataset (governorates, districts, neighbourhoods, Arabic and English names) is owned by Logistics. Its source is decision D-32.
- ADR-2 Saved addresses per customer are limited to `cfg:customers.max_saved_addresses` (default 3).
- ADR-3 Each address is checked against the serviceability matrix ([logistics](logistics.md) §3). A non-serviceable address is rejected at the address step with a clear message.
- ADR-4 The order stores an immutable snapshot of the address. Later edits to saved addresses never change past orders.
- ADR-5 The address model is stored as a generic hierarchy (country → level 1 → level 2 → level 3 → free-text details) with labels, required fields and reference data defined per market. In Iraq the levels are governorate, district and neighbourhood, and the landmark is required. No code path assumes Iraq's structure ([market-expansion](../01-product/market-expansion.md) §3).

## 2. Cart

- CRT-1 Signed-in customers have a server-side cart (one active cart per account) so it follows them across devices and the future apps. Guests keep the cart on the device; at sign-in the **guest device cart** is merged once into the account cart (quantities added, capped by limits) and then cleared from the device. This one-time merge is the only merge; CRT-6 governs concurrent edits of the account cart afterwards.
- CRT-7 Lines are removed from the cart when an order containing them is placed (prepaid included, at placement rather than at payment). If the order is later cancelled for `PAYMENT_EXPIRED`, the customer is offered a one-tap "restore to cart".
- CRT-2 A cart line references an **offer** (seller, variant, condition) and a quantity. If the offer becomes invalid, the customer is shown, as a replacement they must accept, the current Buy Box offer for the same variant when the invalid offer was `NEW`, otherwise the lowest-priced eligible offer in the same condition; if none exists the line is flagged unavailable.
- CRT-3 Carts never reserve stock. Unavailable or changed lines are flagged whenever the cart is read.
- CRT-4 Limits: `cfg:cart.max_qty_per_line` (default 10), `cfg:cart.max_lines` (default 50), optional per-SKU purchase limits set by admin.
- CRT-5 The cart page and every later step display amounts from the **quote** endpoint (§4); clients never compute totals.
- CRT-6 Cart writes carry a version. When two devices change the same account cart, the later write to a line wins and the other device receives `409 VERSION_CONFLICT` with the current cart, which it displays. Apart from the one-time guest merge in CRT-1, carts are never silently merged.

## 3. Checkout

### 3.1 Steps

`Cart → Address → Shipping → Payment → Confirmation` (five steps, as in v6 and the sitemap).

| Step | What happens |
|---|---|
| Cart | Review lines, apply coupons and loyalty redemption, see quote |
| Address | Signed-in customer selects or adds an address. A guest enters a phone number and verifies it by OTP, then enters the address. The **checkout session** is created here |
| Shipping | Shows the per-seller parcels, delivery estimates and shipping fees. There is no option to choose at launch: rates are standardised by Nyazek |
| Payment | Shows the payment methods the customer is eligible for, the final quote and the place-order action |
| Confirmation | Order number, sub-orders, next steps; for prepaid redirects the return page shows the live payment status |

### 3.2 Checkout session

- CHK-1 A checkout session is created when an authenticated customer, or a guest with an OTP-verified phone, proceeds from Cart to Address. It snapshots the cart lines and reserves stock ([inventory](inventory.md) §3).
- CHK-2 States: `OPEN → PLACED`, or `OPEN → EXPIRED` (reservation lapsed and could not be renewed), or `OPEN → ABANDONED` (customer returned to cart or a new session replaced it).
- CHK-3 One open session per customer. Starting a new one abandons the previous and releases its reservation.
- CHK-4 If the reservation expires while the customer is still in checkout, the next action transparently re-reserves; if stock is no longer available the customer returns to the cart with the affected lines flagged.
- CHK-5 Abuse limits: `cfg:checkout.max_sessions_per_hour` (default 10) per account and per device.

### 3.3 Guest checkout

- GST-1 The phone number is verified by OTP before the session exists.
- GST-2 If the phone already belongs to a customer account, the OTP signs the customer in to that account and checkout continues as that customer, subject to the same checks as a normal sign-in. If the recycled-number check (ID-REC-1) fails, ID-REC-1 applies: the old account is closed and checkout continues with the new account created for the number. If the account has 2FA enabled and the second factor is not given, checkout cannot continue as that account and the customer is offered normal sign-in or recovery. If the phone belongs to another account type, checkout is refused with the generic identity message ([identity-access](../05-trust/identity-access.md) §4).
- GST-3 Otherwise a customer account is created with the verified phone and no password. The customer can set a password and add an email later.
- GST-3a A guest's verified phone is always the first contact phone of the delivery address; a second phone is optional ([ADR-0007](../../adr/0007-decisions-from-the-ia-consistency-pass.md)).
- GST-4 Guests look up orders with order number + OTP to the order's phone. A successful lookup opens an **order-lookup session** scoped to that one order (view, track, cancel, return, dispute, download documents), lasting `cfg:identity.order_lookup_session_minutes` (default 30); it gives no access to the account's other orders, addresses or refund accounts.

## 4. Quote (price calculation)

One backend function produces the quote for the cart, every checkout step and order placement. Its output is stored on the order.

### 4.1 Calculation order

1. **Line price** = current offer price (which already reflects any active deal price) × quantity. Revalidated against the Catalog and price rules.
2. **Seller coupon**: at most one per sub-order, applied to eligible lines of that seller.
3. **Platform coupon**: at most one per order, allocated across eligible lines in proportion to their value after step 2.
4. **Free-delivery test**: the order's product subtotal across all sellers after steps 2 and 3 is compared with `cfg:shipping.free_threshold` (value set under D-21; Silver and Gold loyalty tiers may have a lower threshold).
5. **Shipping fee** per sub-order from the rate card (destination zone, parcel weight tier); zero for every sub-order when the test in step 4 passes. Heavy or oversized surcharges always apply.
6. **Loyalty redemption**: applied to eligible lines, capped per [loyalty](loyalty.md) LOY-9, computed on their value after steps 2 and 3. Not available on a sub-order that carries a seller coupon ([loyalty](loyalty.md) §3).
7. **COD fee** if the method is COD and a fee is configured.
8. **Tax** lines (0% at launch).
9. **Rounding** to the price step per MON-4 and MON-5 ([ledger-reconciliation](../04-finance/ledger-reconciliation.md) §2).

### 4.2 Quote output (stored per order line and sub-order)

Per line: unit price, quantity, seller discount, platform discount, loyalty discount, tax, payable, commission rate and expected commission, funder of each discount. Per sub-order: items payable, shipping fee, surcharge, COD fee, total payable. Per order: totals and the payment method. These stored allocations are the basis for partial cancellations and refunds; nothing is recomputed from current prices later.

### 4.3 Revalidation

- QTE-1 Price, offer validity, stock, coupon validity, COD eligibility and serviceability are revalidated at session creation and again at place-order.
- QTE-2 If a total changed since the customer last saw it, place-order returns `409 QUOTE_CHANGED` with the new quote and the customer must confirm.

## 5. Order model

| Entity | Key fields |
|---|---|
| `Order` (parent) | orderNumber, customerId, address snapshot, payment method, quote totals, derived status, placedAt |
| `SubOrder` (one per seller) | orderId, sellerId, status, cancelReason, SLA deadlines, shipmentId, totals, escrow hold end |
| `OrderLine` | subOrderId, offerId, variantId, product snapshot (title, image, attributes), the quote fields in §4.2, return-policy snapshot (RET-6), quantity counters `qtyOrdered`, `qtyCancelled`, `qtyReturned` (accepted returns), `qtyRefunded`, and the per-line settlement amounts `releasedAmount`, `refundedAmount` |

- ORD-1 Order numbers are human-readable and non-guessable: `NZ-XXXX-XXXX` using an unambiguous alphabet with a check character. Sub-orders append `-1`, `-2`, …. Both are shown to customers and sellers.
- ORD-2 Items cannot be edited after placement; the customer cancels and reorders.
- ORD-3 The delivery address can be changed by the customer until `READY_TO_SHIP` if the new address has the same shipping fee and is serviceable; otherwise through Support.
- ORD-4 One sub-order ships as one parcel with one waybill at launch. Multi-parcel sub-orders are P2.
- ORD-15 Line status is **derived** from the quantity counters and is never stored on its own: `CANCELLED` when `qtyCancelled = qtyOrdered`; `REFUNDED` when every non-cancelled unit is refunded; `PARTIALLY_REFUNDED` when some units are refunded; otherwise `ACTIVE`. Counters satisfy `qtyCancelled + qtyRefunded ≤ qtyOrdered` and `qtyReturned ≤ qtyOrdered − qtyCancelled`; `qtyCancelled` changes only on cancellation (whole sub-order at launch, SLA-5), `qtyReturned` on return `ACCEPTED`, `qtyRefunded` on refund events; enforced in the database.
- ORD-16 **Payment window.** A prepaid order must be paid within `cfg:orders.payment_window_minutes` (default 30) of placement. The deadline is stored on the order; every payment intent for the order expires no later than it, and the order's stock stays reserved until it ([inventory](inventory.md) RSV-3). When the window lapses without a successful payment, every sub-order moves to `CANCELLED` with `PAYMENT_EXPIRED` and the parent becomes `EXPIRED`. A failed payment attempt does not cancel anything; the customer may retry until the deadline (PAY-18).

### 5.1 Place-order flow (saga)

| # | Step | Module | Compensation on failure |
|---|---|---|---|
| 1 | Validate idempotency key, session, quote (QTE-1) | checkout | – |
| 2 | Assess risk; decide COD confirmation or review | risk | – |
| 3 | Create order, sub-orders, lines with quote snapshot | orders | – |
| 4 | Redeem coupons and loyalty points | promotions, loyalty | Reverse redemption |
| 5a | COD: allocate stock; create COD collections; sub-orders go to `ON_HOLD` or `PENDING_SELLER_CONFIRMATION` | inventory, payments | Release stock |
| 5b | Prepaid: set the payment deadline (ORD-16); create payment intent; order and sub-orders `AWAITING_PAYMENT`; reservation held until the deadline | payments, inventory | Expire order at the deadline |
| 6 | Prepaid, on `payment.succeeded` before the deadline: allocate stock; sub-orders move forward as in 5a | inventory, orders | Success after the deadline: PAY-9 (automatic refund, never revival) |
| 7 | Emit `order.placed`; notify customer; start timers | orders | – |

A second submit with the same idempotency key returns the first order.

## 6. Sub-order state machine

One definition, validated server-side. Illegal transitions are rejected; every transition is idempotent, emits an event and writes an audit entry.

| State | Entered when | Allowed next | Timer |
|---|---|---|---|
| `AWAITING_PAYMENT` | Prepaid order placed | `ON_HOLD`, `PENDING_SELLER_CONFIRMATION`, `CANCELLED` (customer cancels the whole order, payment window lapsed, or seller suspended) | Payment window (ORD-16) |
| `ON_HOLD` | COD confirmation required, or risk review | `PENDING_SELLER_CONFIRMATION`, `CANCELLED` | `cfg:cod.confirmation_window_hours` (default 24) or risk review SLA |
| `PENDING_SELLER_CONFIRMATION` | Paid or COD-cleared; visible to seller | `CONFIRMED`, `CANCELLED` | Confirmation SLA |
| `CONFIRMED` | Seller accepts | `READY_TO_SHIP`, `CANCELLED` | Shipment SLA |
| `READY_TO_SHIP` | Seller marks the parcel packed and ready; the courier is assigned and the waybill and label are created ([logistics](logistics.md) §5). The pickup request or drop-off declaration is made in this state | `SHIPPED`, `CANCELLED` | Handover grace |
| `SHIPPED` | Courier scans the parcel at handover | `OUT_FOR_DELIVERY`, `DELIVERED`, `DELIVERY_FAILED`, `LOST` | Courier SLA |
| `OUT_FOR_DELIVERY` | Courier dispatches for delivery | `DELIVERED`, `SHIPPED` (attempt failed, will retry), `DELIVERY_FAILED`, `LOST` | `cfg:logistics.max_attempts` (DLV-1) |
| `DELIVERED` | Proof of delivery captured | `COMPLETED` | Escrow hold; return window |
| `COMPLETED` | Every line is settled: its escrow released or its value refunded ([commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) WAL-5) | terminal (returns and disputes still possible within their windows) | – |
| `DELIVERY_FAILED` | Attempts exhausted or customer refused | `RTO_IN_TRANSIT`, `LOST` | – |
| `RTO_IN_TRANSIT` | Courier returning the parcel | `RTO_RECEIVED`, `LOST` | Courier SLA |
| `RTO_RECEIVED` | Seller (or Nyazek for 1P) confirms receipt | terminal | – |
| `LOST` | Courier declares loss or the loss timer elapses | terminal | – |
| `CANCELLED` | See §8 | terminal | – |

Notes on changes from v6:

- Returns and disputes are separate records linked to the sub-order ([returns-disputes](returns-disputes.md)); they are no longer sub-order states, because a customer may return one item of several and a dispute may run alongside.
- All cancellations share one terminal state with a mandatory `cancelReason`: `CUSTOMER`, `SELLER_REJECTED`, `SELLER_CANCELLED`, `SLA_CONFIRM_TIMEOUT`, `SLA_SHIP_TIMEOUT`, `COD_UNCONFIRMED`, `RISK_REJECTED`, `PAYMENT_EXPIRED`, `SELLER_SUSPENDED`, `ADMIN`. The reason decides seller-performance attribution ([seller-performance](../03-sellers/seller-performance.md) §1). A failed payment attempt is not a cancellation reason (ORD-16).
- `ON_HOLD` was missing: v6 paused the seller's SLA during COD confirmation but had no state for it.
- `SHIPPED → DELIVERED` is allowed because some couriers do not report "out for delivery".

Effects of terminal and key states:

Stock movements are defined only in [inventory](inventory.md) §2; the column below summarises them.

| State | Stock | Money | Other |
|---|---|---|---|
| `CANCELLED` | From `AWAITING_PAYMENT`: release reservation. Later: release allocation | Prepaid and paid: refund the sub-order total (JE-14). Unpaid: nothing. COD: void collection | Reverse coupons and points for the sub-order's lines |
| `SHIPPED` | Deducted from on-hand and allocated | – | Sales receipt issued |
| `DELIVERED` | – | COD: collection `COLLECTED`. Shipping and COD fees earned (JE-7, JE-8) | Hold and return window start |
| `DELIVERY_FAILED` | No movement (already deducted at `SHIPPED`) | Prepaid: item value refunded and shipping retained or refunded per ORD-9 (JE-14, JE-40), so the sub-order's escrow is zero. COD: collection `NOT_COLLECTED` | Cost attribution per [logistics](logistics.md) §7; credit note issued |
| `RTO_RECEIVED` | Seller (Nyazek for 1P) restocks resellable units after inspection | – | – |
| `LOST` | No movement (already deducted at `SHIPPED`) | Prepaid: full refund (JE-14). COD: collection `NOT_COLLECTED`. 3P: seller compensated (JE-38). 1P: goods written off (JE-43) and claim recognised (JE-44) | Courier claim opened |

### 6.1 Parent order status (derived)

The parent status is computed from the sub-orders, never set directly. Rules are evaluated top to bottom; the first match wins.

| # | Condition | Parent status |
|---|---|---|
| 1 | Every sub-order is `CANCELLED` with `PAYMENT_EXPIRED` | `EXPIRED` |
| 2 | Every sub-order is `AWAITING_PAYMENT` (no sub-order can be cancelled alone in this state, §8) | `AWAITING_PAYMENT` |
| 3 | Every sub-order is `CANCELLED` | `CANCELLED` |
| 4 | At least one sub-order is not terminal | `IN_PROGRESS` |
| 5 | Every sub-order is terminal and at least one is `COMPLETED` | `COMPLETED` |
| 6 | Every sub-order is terminal and none is `COMPLETED` (mix of `CANCELLED`, `RTO_RECEIVED`, `LOST`) | `CLOSED` |

Terminal sub-order states: `COMPLETED`, `CANCELLED`, `RTO_RECEIVED`, `LOST`. Customer-facing labels and list tabs map these values in [taxonomy-and-labels](../09-information-architecture/taxonomy-and-labels.md).

## 7. Seller order SLAs

| Stage | Obligation | Default | On breach |
|---|---|---|---|
| 1 Confirmation | Accept or reject from `PENDING_SELLER_CONFIRMATION` | `cfg:orders.confirm_sla_hours` (default 24) | Auto-cancel `SLA_CONFIRM_TIMEOUT`; counts against seller except as PRF-4 excludes |
| 2 Shipment | Reach `READY_TO_SHIP` (packed, waybill and label created) after confirmation | 24 hours × the largest handling time among the sub-order's offers (SLA-6) | Auto-cancel `SLA_SHIP_TIMEOUT`; counts against seller |
| Handover | Pickup requested or drop-off declared, and parcel scanned by the courier, after `READY_TO_SHIP` | `cfg:orders.handover_grace_hours` (default 48) | No auto-cancel; goes to the Logistics exception queue. A pickup that failed because of the seller counts as a late shipment |

- SLA-1 Clocks run in calendar hours and pause on days declared as platform holidays or force majeure by an admin.
- SLA-2 The seller's clock does not run while the sub-order is `ON_HOLD` or `AWAITING_PAYMENT`.
- SLA-3 Reminders are sent at 50% and 90% of each window.
- SLA-4 A seller may reject at stage 1 with a reason. Rejections count toward the cancellation rate; repeated rejections trigger review ([seller-performance](../03-sellers/seller-performance.md)).
- SLA-5 At launch a seller accepts or rejects the whole sub-order. Rejecting individual lines is P1.
- SLA-6 An offer's handling time is a whole number of days from 1 to `cfg:orders.max_handling_days` (default 3); new offers default to `cfg:orders.default_handling_days` (default 2), which gives the 48-hour shipment SLA. Handling time is part of the delivery estimate (SVC-3) and the Buy Box delivery component.
- SLA-7 Suspension and closure: when a seller becomes `SUSPENDED`, its sub-orders in `AWAITING_PAYMENT`, `ON_HOLD` or `PENDING_SELLER_CONFIRMATION` are cancelled with `SELLER_SUSPENDED` (paid ones refunded per §6; for an unpaid order the customer pays only for the remaining sub-orders, the payment intent being re-issued for the new total); sub-orders already `CONFIRMED` or `READY_TO_SHIP` stay with the seller, who keeps the fulfilment actions for them until they ship or time out. A seller in `CLOSING` keeps fulfilment actions for all open sub-orders and receives no new orders ([seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) §5). `SELLER_SUSPENDED` does not count in seller metrics; the suspension is the consequence.

## 8. Cancellation

| Actor | Allowed while | Effect on seller metrics |
|---|---|---|
| Customer | `ON_HOLD`, `PENDING_SELLER_CONFIRMATION`, `CONFIRMED`, `READY_TO_SHIP`, per sub-order (the waybill is voided if it exists). While the order is `AWAITING_PAYMENT`, only the whole order can be cancelled, because one payment covers every sub-order | None |
| Seller | `PENDING_SELLER_CONFIRMATION` (reject), `CONFIRMED`, `READY_TO_SHIP` | Counts as seller cancellation |
| System | SLA timeouts, payment window lapse, unconfirmed COD, risk rejection, seller suspension (SLA-7) | Timeouts count against seller except as PRF-4 excludes; others do not |
| Admin | Any state before `SHIPPED`, with reason | Per reason recorded |

After `SHIPPED` nobody can cancel. The customer refuses delivery (`DELIVERY_FAILED`) or uses the returns process. An admin who must stop a shipped parcel asks the courier to return it and records the outcome through a manual state override (ORD-12: `DELIVERY_FAILED` or `LOST`, dual control per [admin-governance](../05-trust/admin-governance.md) §3); money then follows the effects table above.

## 9. Edge cases

- ORD-5 One payment covers a multi-seller order. When one sub-order is cancelled, only its stored total is refunded; other sub-orders continue.
- ORD-6 Shipping already charged is not recomputed after partial cancellation. If a seller-side cancellation drops the order below the free-delivery threshold, the customer is not charged retroactively.
- ORD-7 Coupons and loyalty points redeemed on cancelled lines are reversed using the stored per-line allocation. A single-use platform coupon becomes usable again only if the whole order is cancelled.
- ORD-8 Duplicate submissions (double click, back button, retry after timeout) return the original order.
- ORD-9 Prepaid order with failed delivery: item value is refunded when the sub-order enters `DELIVERY_FAILED`. The outbound shipping fee is refunded when the cause is the seller, the courier or undetermined ([logistics](logistics.md) §7), and retained (JE-40) when the customer refused or was unreachable; no further deduction is made. The customer-fault part is decision D-31, implemented with this recommended default. Either way the sub-order's escrow reaches zero at `DELIVERY_FAILED`.
- ORD-10 A sub-order stuck in any non-terminal state beyond its timer plus `cfg:orders.stuck_alert_hours` (default 12) appears in the admin exception queue and raises an alert.
- ORD-11 Lost-parcel timer: a `SHIPPED` or `RTO_IN_TRANSIT` sub-order with no tracking event for `cfg:logistics.lost_after_days` (default 14) is escalated to Logistics, who declare it `LOST` or correct the status.
- ORD-12 Admin manual state overrides are limited to transitions the machine allows, require a reason, and are audited.
- ORD-13 The order snapshots the contact phone numbers together with the address (ADR-4). Delivery calls, the delivery OTP, COD confirmation and guest order lookup use the order's phone, even if the customer later changes the account's phone number.
- ORD-14 There is no minimum order value at launch and no gift option (wrapping, message, hidden prices). Scheduled delivery slots, pickup points and item substitution by the seller are not supported; a seller who cannot supply a line rejects the sub-order (SLA-4).

## 10. Acceptance criteria

- Model-based tests cover every transition in §6 and prove that every illegal transition is rejected.
- Concurrent place-order calls for the last unit result in exactly one order.
- For every terminal state, stock counters and ledger account 2100 for the sub-order end at their expected values.
- A multi-seller order with one seller cancelling refunds exactly that sub-order's stored total and leaves the others unaffected.
- Quote totals are always multiples of the price step and equal the sum of their parts.
