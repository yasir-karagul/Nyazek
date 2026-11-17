# Storefront Pages: Customer Account, Seller Landing, Static Pages

**Authoritative for:** the content and actions of the signed-in customer pages, the public seller pages on the Storefront host, and static and legal pages.
**Read with:** [README](README.md) §2 · [navigation](navigation.md) §1.4 · [taxonomy-and-labels](taxonomy-and-labels.md) §3–4 · [flows](flows.md) FL-5 to FL-7 · [sitemap](sitemap.md) §5, §7.1, §9
**Rules live in:** [checkout-orders](../02-commerce/checkout-orders.md) §6–8 · [returns-disputes](../02-commerce/returns-disputes.md) · [reviews-qa](../02-commerce/reviews-qa.md) · [customer-account](../02-commerce/customer-account.md) · [identity-access](../05-trust/identity-access.md) · [privacy-audit](../05-trust/privacy-audit.md) · [support-cms](../02-commerce/support-cms.md)

All account pages require a signed-in customer (IA-13) and show only that customer's data.

---

## 1. Account home and orders

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-ACC-HOME | `TPL-DASH` | Greeting; "Needs your attention" list (confirm a COD order, complete a payment, hand over a return, answer a seller, review a purchase); the three most recent orders as order cards; favourites preview; loyalty balance and coupons (P1); on mobile, the account menu | Open any item; set a password (unclaimed accounts) | New customer with no orders: a welcome message and a link to home | CUS-1, CUS-2 |
| SF-ORD-LIST | `TPL-LIST` | Tabs per [taxonomy-and-labels](taxonomy-and-labels.md) §3.1: All · Pending · Processing · Shipped · Delivered · Cancelled · Returned. Order cards, newest first; search by order number or product name | Open an order; "Buy again" (P1) | Empty state per tab | Order model |
| SF-ORD-TRACK | `TPL-DETAIL` | For one shipment: seller block, status chip, estimated delivery, milestone timeline ([taxonomy-and-labels](taxonomy-and-labels.md) §3.3), courier name, tracking number and link, "Courier details" (raw events), delivery address area | Reschedule a failed attempt once (where the courier supports it); contact support | Before a waybill exists: milestones only; guest sessions reach this page through `SF-AUTH-GUESTTRACK` | SHP-1, DLV-1 |

### SF-ORD-DETAIL — Order detail

- **Template:** `TPL-DETAIL`.
- **Content:**
  1. Header: order number, date, derived status ([taxonomy-and-labels](taxonomy-and-labels.md) §3.2), payment method and payment status.
  2. Attention banner when something is waiting on the customer (complete payment before the deadline, with a countdown → `SF-CHK-RETURN`; confirm COD order; add a refund account for a refund `AWAITING_DESTINATION`). An expired order offers "Restore to cart" (CRT-7).
  3. One shipment block per sub-order: seller block, status chip, next step with its date, items (image, title, variant, quantity with cancelled, returned and refunded quantities where any, unit price, line total, derived line status, ORD-15), "Track", and the shipment's allowed actions.
  4. Delivery address block and contact phone (as snapshotted, ORD-13).
  5. Quote summary as charged: items, discounts, shipping per shipment, COD fee, tax when non-zero, total; refunds issued so far as separate lines.
  6. Documents: receipt per shipment, credit notes.
  7. Related: returns and disputes for this order, each linking to its page.
- **Actions (each shown only when the API allows it):** cancel a shipment (dialog with reason select; states what will be refunded and how); change the delivery address of a shipment until `READY_TO_SHIP` when the new address has the same fee and is serviceable, otherwise "Contact support" (ORD-3); return items (FL-5); "I did not receive this" on a delivered shipment and "My order has not arrived" after the promised date plus the grace period (FL-6); confirm receipt; write a review; contact the seller (P1); download documents; buy again (P1).
- **States and guards:** cancelled or failed shipments keep their block with the reason in customer words and the refund status; a shipment with no action available shows why nothing can be done now (for example "Can be returned until <date>" or "Return window closed on <date>").
- **Rules:** cancellation table and ORD-3, ORD-5 to ORD-9, ORD-15, ORD-16 · RET-1, RET-6 · dispute windows ([returns-disputes](../02-commerce/returns-disputes.md) §6.1) · REV-1 · [tax-invoicing](../04-finance/tax-invoicing.md) §3

## 2. Returns and disputes

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-RET-LIST | `TPL-LIST` | Returns with product thumbnails, return status, refund amount and status; tabs: Open (every state before `CLOSED`) · Closed | Open a return | Empty state links to orders | – |
| SF-RET-NEW | `TPL-FORM` | Per FL-5: returnable lines with quantity steppers; reason select per line; evidence uploader; refund destination; refund summary; "replace instead" (P1, D-25) | Submit; add a refund account (dialog) | Lines not returnable are listed with the reason; change-of-mind reasons show the return-shipping deduction before submission; opened without a returnable line → redirect to the order | RET-1 to RET-7, REF-1 to REF-6 |
| SF-RET-DETAIL | `TPL-DETAIL` | Status chip and next step with its deadline; items; hand-over instructions (pickup slot or drop-off) with the return waybill; return tracking; seller's contest and proposed partial refund when there is one; refund summary; timeline | Withdraw (before hand-over); accept or decline a proposal; open a dispute when the return was rejected or contested; contact support | – | Return machine, RET-3, RET-4 |
| SF-DISP-LIST | `TPL-LIST` | Disputes with type, order, status, last update; tabs: Open (`OPENED` to `REVIEW_REQUESTED`) · Closed (`CLOSED`, with the outcome) | Open a dispute | – | – |
| SF-DISP-NEW | `TPL-FORM` | Per FL-6: type (fixed by entry point), what happened, evidence uploader, what the customer asks for (refund, partial refund) | Submit | Opened outside the window for the type → explanation and a link to support; one open dispute per shipment and type | Dispute windows, DSP-1 |
| SF-DISP-DETAIL | `TPL-DETAIL` | Status chip; both parties' statements and evidence (the seller's as provided to the customer); deadlines; decision with reasons and the refund summary; timeline | Add evidence or a reply while open; withdraw while `OPENED` or `SELLER_RESPONSE`; request a review within the review window after a decision | – | DSP-2 to DSP-6 |

## 3. Reviews and questions

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-REV-PENDING | `TPL-LIST` | Delivered items not yet reviewed and still inside the review window, with the days left | Write a review (dialog with the review form) | Items outside the window are not listed | REV-1 |
| SF-REV-DONE | `TPL-LIST` | The customer's reviews with status (published, under review, removed with the reason category) | Edit once within 7 days of posting (REV-2); delete | – | REV-2, moderation table |
| SF-QA-MY | `TPL-LIST` | The customer's product questions with answers | Open the product; delete a question | P1 | Q&A rules |

## 4. Saved details

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-ADDR | `TPL-LIST` (cards) | Address blocks with the default marked | Add or edit (address form in a dialog); set default; delete | Limit message; deleting an address never affects past orders | ADR-1 to ADR-5 |
| SF-REFACC | `TPL-LIST` (cards) | Refund accounts: type (mobile wallet or bank), provider, masked number, holder name, verified state | Add (form, then OTP to the customer's verified phone, payments §6); delete | A destination used by a refund in progress cannot be deleted; maximum per customer (`cfg:refunds.max_refund_accounts`) | PAY-17 |
| SF-PAYM | `TPL-LIST` (cards) | Saved card tokens: brand, last four digits, expiry | Delete | P1; adding happens only during payment at the provider | [payments](../04-finance/payments.md) §1 |
| SF-LOY | `TPL-DASH` | Tier and progress to the next tier; points available and pending; value in currency; history of earned, redeemed, expired and reversed points; how to earn; referral link and its results | Copy the referral link | P1; unclaimed accounts are asked to set a password before redeeming | [loyalty](../02-commerce/loyalty.md) |
| SF-COUP | `TPL-LIST` (cards) | Available coupons with conditions and expiry; used and expired in a second tab | Copy a code; shop eligible products | P1 | PRM-1 to PRM-5 |

## 5. Inbox

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-NOTIF | `TPL-LIST` | Tabs: All · Orders · Promotions · System. Notification items, newest first | Open the linked object; mark all read; open preferences (dialog) | Preferences dialog: per-category and per-channel opt-ins for promotional messages; language; transactional messages shown as always on | NTF-1 to NTF-4, PRV-2 |
| SF-MSG | `TPL-LIST`; a thread opens on a sub-route with the Message thread component | Threads, one per order and seller: seller name, order number, last message, unread marker. Thread: messages with times, the order summary pinned on top | Send a message (text, images); report a message | P1; contact details and links are blocked; threads close per [notifications-messaging](../02-commerce/notifications-messaging.md) §6 | Messaging rules |

## 6. Profile, security, privacy

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-PROF | `TPL-FORM` | Name, language, date of birth (optional), default governorate | Save | – | CUS profile table |
| SF-SEC-PW | `TPL-FORM` | Current password (if one exists), new password with the policy | Save; "Set a password" variant for accounts without one | Other sessions are signed out after a change | Password rules |
| SF-SEC-EMAIL | `TPL-FORM` | Current phone (masked) and email with verified states | Change phone (OTP to the new number, step-up first); add or change email (verification link) | Old identifier is notified; claim-conflict message per AUTH-2; cool-down before a new identifier can be used for recovery | ID-5, AUTH-5 |
| SF-SEC-DEV | `TPL-LIST` | Active sessions: device and browser, approximate location, last active, "This device" | Sign out one; sign out all others | A sign-in from a new device sends a security notice (SES-6) | SES-4 |
| SF-SEC-2FA | `TPL-FORM` | State of two-factor authentication; setup (authenticator app, recovery codes) | Enable, disable (step-up), regenerate codes | P1 | 2FA rules |
| SF-SEC-LINK | `TPL-LIST` | Linked providers with linked date | Link another; unlink | Unlinking the only sign-in method is blocked until a phone or password exists | Social rules |
| SF-PRIV | `TPL-FORM` | Consent switches (marketing per channel, personalisation); "Download my data"; "Delete my account" (FL-7); links to the privacy and cookie policies | Save consents; request an export (delivered by notification when ready); start deletion | Export limited to one request in progress | DSR-1 to DSR-3, CUS-12 to CUS-15 |

## 7. Public seller pages

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-SELL-LANDING | `TPL-CONTENT` | Why sell on Nyazek; how it works in steps (register, verify, list, ship, get paid); what is needed to apply (documents by seller type); the separate-email notice; fees summary with a link | "Start selling" → seller registration on the seller host; seller sign-in | – | SEL-1, SEL-2, ID-1 |
| SF-SELL-FEES | `TPL-CONTENT` | Commission schedule by category (table from the live schedule); what commission is charged on; who pays shipping, return shipping and failed delivery; payout schedule and minimum; date the schedule took effect | – | The table is generated from configuration, not typed into the CMS | COM-1 to COM-4, failed-delivery and return-shipping tables |

## 8. Static, legal and help pages

All use `TPL-CONTENT`, are managed in the CMS in both languages (CMS-1 to CMS-5) and need no sign-in. Legal pages show their version and effective date; counsel-drafted text is a launch gate.

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-ST-ABOUT | `TPL-CONTENT` | Who Nyazek is, legal identity, contact | – | – | CMS-1 |
| SF-ST-CONTACT | `TPL-FORM` | Topic, order number (optional, validated when signed in), message, attachments, name and reply contact for guests | Submit → ticket number and expected reply time | Rate-limited; signed-in customers have contact fields pre-filled | SUP-1 to SUP-4 |
| SF-ST-FAQ | `TPL-CONTENT` | Questions grouped by topic (orders, delivery, payment, returns, account) with search within the page | Expand; contact support | – | – |
| SF-ST-FAQ-SELLER | `TPL-CONTENT` | Seller questions (registration, documents, fees, shipping, payouts) | Start selling | – | – |
| SF-ST-TERMS | `TPL-CONTENT` | Terms & Conditions | – | A new version triggers re-acceptance at next sign-in | CMS-2 |
| SF-ST-PRIVACY | `TPL-CONTENT` | Privacy Policy | – | As above | CMS-2 |
| SF-ST-COOKIES | `TPL-CONTENT` | Cookie Policy with the list of purposes | Open cookie settings | – | [privacy-audit](../05-trust/privacy-audit.md) §2 |
| SF-ST-RETURNS | `TPL-CONTENT` | Return & Refund Policy, including windows by category generated from configuration | – | – | RET-1 |
| SF-ST-SHIPPING | `TPL-CONTENT` | Shipping Policy: coverage, estimates, fees and free-delivery threshold generated from configuration | – | – | FEE-1 to FEE-5 |
| SF-ST-PROTECT | `TPL-CONTENT` | Customer Protection Policy | – | – | – |
| SF-ST-DISPUTE | `TPL-CONTENT` | Dispute Resolution Policy | – | – | – |
| SF-ST-SELLERAGR | `TPL-CONTENT` | Seller Agreement | – | – | CMS-2 |
| SF-ST-PROHIBITED | `TPL-CONTENT` | Prohibited & Restricted Items Policy | – | – | PRH-4 |
| SF-ST-REPORT | `TPL-FORM` | Report a listing or file an intellectual-property notice: listing link, reason, details, the reporter's identity and authority for IP notices | Submit → reference number | Rate-limited | PRH-2 |
| SF-ST-PAYGUIDE | `TPL-CONTENT` | How each payment method works, step by step | – | P1 | – |
| SF-ST-LOYALTY | `TPL-CONTENT` | Loyalty programme terms | – | P1 | [loyalty](../02-commerce/loyalty.md) |
| SF-ST-HOW | `TPL-CONTENT` | How Nyazek works | – | P2 | – |
| SF-ST-TRUST | `TPL-CONTENT` | Safety and trust centre | – | P2 | – |
| SF-ST-CAREERS | `TPL-CONTENT` | Careers | – | P2 | – |
| SF-ST-BLOG | `TPL-LIST` and `TPL-CONTENT` | Blog index and posts | – | P2 | – |
| SF-ST-PRESS | `TPL-CONTENT` | Press | – | P2 | – |
| SF-ST-SITEMAP | `TPL-CONTENT` | Links to categories and main pages | – | P2 | – |
