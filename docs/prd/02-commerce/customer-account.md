# Customer Account, Favourites & Alerts

**Authoritative for:** the customer profile, the account home, favourites, stock and price alerts, recently viewed, reorder, sharing, and what happens to customer data at account deletion.
**Related:** [identity-access](../05-trust/identity-access.md) · [checkout-orders](checkout-orders.md) §1–2 · [notifications-messaging](notifications-messaging.md) · [privacy-audit](../05-trust/privacy-audit.md) §3 · [loyalty](loyalty.md) · [web-apps](../07-clients/web-apps.md) §4.1 · [sitemap](../09-information-architecture/sitemap.md) §5 · [pages-storefront-account](../09-information-architecture/pages-storefront-account.md)

Login, sessions, addresses, orders, returns, reviews and consent are specified in their own documents; this document covers what had no owner.

---

## 1. Profile

| Field | Rule |
|---|---|
| Name | Required at first order; used on the address snapshot and documents |
| Phone | Verified login identifier ([identity-access](../05-trust/identity-access.md) §2) |
| Email | Optional; must be verified before use |
| Language | Arabic or English; drives notifications and documents |
| Date of birth | Optional; used only for the adult check and the birthday reward ([loyalty](loyalty.md) §7) |
| Gender | Not collected |
| Default address, default governorate for delivery estimates | Optional |

- CUS-1 A guest-created account (GST-3) becomes a **claimed** account when the customer sets a password or verifies an email. Unclaimed accounts can order, track, return and dispute by phone OTP; they cannot redeem loyalty points (LOY-3) or save payment tokens.
- CUS-2 The account home shows recent orders with their next action, open returns and disputes, favourites, and (P1) loyalty balance and active coupons. It contains no information that is not available on the dedicated pages.

## 2. Favourites (P0)

- CUS-3 A favourite references a **product variant**, not an offer, so it survives a change of Buy Box winner and seller.
- CUS-4 Guests keep favourites on the device; at sign-in they are merged into the account (union, newest first). Signed-in favourites are stored server-side and follow the customer across devices and the future apps.
- CUS-5 Limit: `cfg:customers.max_favourites` (default 500) per account; the oldest is not removed automatically, the customer is told the list is full.
- CUS-6 The list shows the current Buy Box price and availability, with filters All, In stock and Price dropped (lower than when the item was added). Prices come from the API on every read; nothing is cached on the client.
- CUS-7 A favourite whose product was unpublished or merged is kept and shown as unavailable, or follows the redirect to the surviving product (CAT-10).
- CUS-8 "Move to cart" adds the current Buy Box offer for the variant; unavailable items are skipped and reported.
- CUS-9 Favourites are private. Public or shared lists are out of scope.

## 3. Alerts (P1)

| Alert | Trigger | Class and consent |
|---|---|---|
| Back in stock | The customer taps "Notify me" on an unavailable variant; one message when `available > 0` again | Informational; explicit per-item request, so no marketing opt-in is needed |
| Price drop on a favourite | Buy Box price falls below the price when the item was favourited, by at least one price step | Promotional; requires marketing opt-in for the channel |
| Abandoned cart reminder | A signed-in customer's cart has items and no order for 24 hours; at most one reminder per cart | Promotional; requires marketing opt-in |

- CUS-10 Back-in-stock subscriptions are limited to `cfg:customers.back_in_stock_alerts_max` (default 50) per customer, expire after 90 days and are removed when the alert is sent.
- CUS-11 All alerts respect quiet hours and frequency caps (NTF-2, NTF-4) and never state a price in the message that may be stale: the message links to the product.

## 4. Convenience features

| Feature | Rule | Priority |
|---|---|---|
| Reorder | "Buy again" on a past order adds the same variants at the **current** Buy Box offers and prices; unavailable lines are reported | P1 |
| Share a product | Native share sheet or copy link; the link is the canonical product URL without personal or tracking parameters; Open Graph tags give a correct preview | P1 |
| Recently viewed | Stored on the device for guests; server-side with personalisation consent for signed-in customers | P2 |
| Gift options (wrapping, message, hidden prices) | Not supported | Out of scope |

## 5. Deletion and closure effects

When a customer account is closed or erased ([privacy-audit](../05-trust/privacy-audit.md) §3):

- CUS-12 Favourites, alerts, the cart, saved addresses, refund accounts, payment tokens and device tokens are deleted.
- CUS-13 Unredeemed loyalty points and unused coupons are forfeited; the customer is told the amount before confirming. A negative points balance is written off.
- CUS-14 Published reviews and questions stay, shown as "Verified customer" with no name.
- CUS-15 Orders, documents and ledger records are retained in pseudonymous form for the retention period.

## 6. Acceptance criteria

- A favourite added as a guest appears in the account after sign-in on another device.
- A back-in-stock alert is sent once, only to customers who asked for that variant, and never during quiet hours.
- After account deletion no favourite, alert, address or token remains, and the customer's reviews show no name.
