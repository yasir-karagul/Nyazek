# Inventory

**Authoritative for:** stock model, reservation rules, stock movements, concurrency and abuse controls.
**Related:** [checkout-orders](checkout-orders.md) · [catalog-listings](catalog-listings.md) · [returns-disputes](returns-disputes.md)

---

## 1. Model

Stock is tracked per **offer** (seller × product variant × condition). Each offer has three counters:

| Counter | Meaning |
|---|---|
| `on_hand` | Units the seller physically has |
| `reserved` | Units held by open checkout sessions and unpaid prepaid orders |
| `allocated` | Units belonging to placed orders not yet handed to the courier |

`available = on_hand − reserved − allocated`. Only `available` is shown to customers and used by search and the Buy Box.

Database constraints: all counters `>= 0` and `on_hand >= reserved + allocated`. Every change writes a `stock_movement` row (offer, delta per counter, reason, reference, actor).

v6 described five "states" including Released and Returned, which are transitions, not states, and stored reservations as Redis TTL locks. Reservations are now rows in PostgreSQL and the only source of truth ([technology-stack](../06-platform/technology-stack.md) §3.3).

## 2. Movements

| Trigger | on_hand | reserved | allocated |
|---|---|---|---|
| Checkout session created | | +q | |
| Session abandoned or expired | | −q | |
| COD order placed | | −q | +q |
| Prepaid order placed | (stays reserved) | | |
| Prepaid payment succeeded | | −q | +q |
| Prepaid payment attempt failed | (no change; the reservation holds until the payment deadline) | | |
| Sub-order cancelled while `AWAITING_PAYMENT` (customer, or payment window lapsed) | | −q | |
| Sub-order cancelled after allocation and before `SHIPPED` | | | −q |
| Sub-order `SHIPPED` | −q | | −q |
| `RTO_RECEIVED` and inspected resellable | +q (seller confirms restock) | | |
| Return received and inspected resellable | +q (seller confirms restock) | | |
| `DELIVERY_FAILED`, `RTO_IN_TRANSIT` | – (already deducted at `SHIPPED`) | | |
| `LOST` after shipping | – (already deducted) | | |
| Seller edit, bulk import, 1P stock receipt or adjustment | set or ±q | | |

## 3. Reservation rules

- RSV-1 Stock is reserved when the checkout session is created, not at add-to-cart ([checkout-orders](checkout-orders.md) CHK-1).
- RSV-2 A reservation lasts `cfg:inventory.reservation_ttl_minutes` (default 15).
- RSV-3 When a prepaid order is placed, its reservation is held until the order's payment deadline ([checkout-orders](checkout-orders.md) ORD-16), whatever the reservation TTL, and is released at the deadline if no payment succeeded. It is never extended beyond the deadline.
- RSV-4 Reserving is one atomic conditional update: it succeeds only if `available >= q`. Two customers can never both reserve the last unit.
- RSV-5 An expiry sweep runs every 30 seconds and releases lapsed reservations. Expiry is also checked lazily whenever a reservation is read, so a delayed sweep cannot cause overselling or a stuck hold.
- RSV-6 Reserved stock is not available to other customers during the hold.
- RSV-7 If stock runs out between add-to-cart and checkout, the customer sees a clear message for the affected line and cannot proceed with it.
- RSV-8 A payment confirmed after the deadline never re-reserves stock; it is refunded automatically (PAY-9, [payments](../04-finance/payments.md)).

## 4. Seller stock changes

- STK-1 Manual edits, the quick-edit grid, bulk import and any future API use optimistic concurrency (version check).
- STK-2 A seller cannot set `on_hand` below `reserved + allocated`; the request is rejected with the minimum allowed value.
- STK-3 Low-stock alerts fire when `available` falls to the seller's threshold per offer (default `cfg:inventory.low_stock_default` (default 3)).
- STK-4 An offer with `available = 0` is shown as out of stock, loses Buy Box eligibility immediately and pauses its ads.
- STK-5 Restocking after RTO or a return is a seller action (the goods are in the seller's hands) prompted by a task in the Seller Dashboard. For 1P it is a stock adjustment by the 1P Merchandiser.

## 5. Freshness

- Stock and availability changes are published as `stock.changed` and reach the search index within 60 seconds.
- Cart, quote and place-order always read stock from the Inventory module, never from the search index or a cache.

## 6. Abuse controls

- Checkout-session caps per account and device (CHK-5), quantity limits per line, and optional per-customer purchase limits per SKU for promotional items.
- Guests must verify a phone number before a session can reserve stock.
- Repeated reserve-and-abandon behaviour is a risk signal ([fraud-risk](../05-trust/fraud-risk.md)).

## 7. Acceptance criteria

- A concurrency test with many customers competing for limited stock never produces `available < 0` or more allocations than `on_hand`.
- With the expiry sweep stopped, expired reservations are still not honoured.
- With the cache unavailable, reservation and allocation behave identically.
- For every order outcome in [checkout-orders](checkout-orders.md) §6, counters return to consistent values (property-based test).
