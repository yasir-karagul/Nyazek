# Seller Dashboard Pages: Sign-in, Onboarding, Home, Orders, Catalog, Returns

**Authoritative for:** the content and actions of these Seller Dashboard pages.
**Read with:** [README](README.md) §2 · [navigation](navigation.md) §2 · [flows](flows.md) FL-8 to FL-12 · [taxonomy-and-labels](taxonomy-and-labels.md) · [sitemap](sitemap.md) §7.2–7.6
**Rules live in:** [seller-dashboard](../03-sellers/seller-dashboard.md) · [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) · [checkout-orders](../02-commerce/checkout-orders.md) §6–7 · [catalog-listings](../02-commerce/catalog-listings.md) · [pricing-promotions](../02-commerce/pricing-promotions.md) §1 · [inventory](../02-commerce/inventory.md) · [logistics](../02-commerce/logistics.md) · [returns-disputes](../02-commerce/returns-disputes.md)

Every page shows only the signed-in seller's data (SEC-2). Actions that change data are disabled in read-only states ([navigation](navigation.md) §2.4). Pages marked with an area follow the staff-role matrix once staff roles ship.

---

## 1. Sign-in

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-AUTH-LOGIN | `TPL-AUTH` | Email, password; links: forgot password, create a seller account | Sign in → `SL-AUTH-2FA` | No social sign-in; generic failure for wrong credentials and for customer or staff identifiers; lock message | [identity-access](../05-trust/identity-access.md) §4, AUTH-3 |
| SL-AUTH-2FA | `TPL-AUTH` | Code from the authenticator app; "Use SMS instead" (Phone and OTP input, two-factor purpose); "Use a recovery code" | Verify | Limited attempts; SMS fallback only to the verified phone | 2FA rules |
| SL-AUTH-2FASETUP | `TPL-WIZARD` | QR code and key; confirm with a code; recovery codes shown once with download and a confirmation checkbox | Finish | Mandatory before any other page | 2FA rules |
| SL-AUTH-REGISTER | `TPL-AUTH` | Email, password with policy, phone; the notice that the email must not be one used for shopping on Nyazek; acceptance of terms | Create account → email and phone verification | Uniform "check your email" response; nothing reveals an existing account | ID-1 to ID-7, AUTH-2 |
| SL-AUTH-VERIFY | `TPL-AUTH` | Result of the email link; then phone OTP if not yet verified | Continue to 2FA setup | Claim conflict: the generic message, shown only after control of the email is proven | AUTH-2 |
| SL-AUTH-FORGOT | `TPL-AUTH` | Email | Submit → uniform confirmation | – | AUTH-1 |
| SL-AUTH-RESET | `TPL-AUTH` | New password; 2FA code or a recovery code ([identity-access](../05-trust/identity-access.md) §4) | Save → all sessions revoked | – | Recovery rules |
| SL-AUTH-INVITE | `TPL-AUTH` | Store name and role the person is invited to; set password; then 2FA setup | Accept | Expired or used invitation; email belongs to another account → generic message; P1 | [seller-dashboard](../03-sellers/seller-dashboard.md) §3 |

## 2. Onboarding (FL-8)

All use `TPL-WIZARD` with the steps Business · Documents · Payout · Review.

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-ONB-BIZ | `TPL-WIZARD` | Seller type (individual, registered business, brand distributor); legal name; store name (with availability check); categories intended; contact person; business address; for regulated categories, a notice of the licence needed | Save and continue | Changing seller type resets the document step | Seller types, SEL-6 |
| SL-ONB-DOCS | `TPL-WIZARD` | The document list for the chosen type, each with what is accepted, an uploader (PDF or image), document number and expiry date where applicable | Upload, replace, continue | Type, size and legibility checks at upload; every mandatory document required to continue | KYC documents table, KYC-9 |
| SL-ONB-PAYOUT | `TPL-WIZARD` | Destination type (bank account or mobile wallet), provider, account number, account-holder name; the rule that the holder must match the verified identity | Save and continue | Format validation per type | PO-4 |
| SL-ONB-REVIEW | `TPL-WIZARD` | Everything entered, by step, with edit links; Seller Agreement with acceptance; declaration that the information is true | Submit application | Submission disabled until the agreement is accepted | CMS-2 |
| SL-ONB-STATUS | `TPL-DETAIL` | Application status with expected time; for `NEEDS_INFO` the exact items requested, each with its uploader or field; for `REJECTED` the reasons and remaining attempts | Provide requested items; reapply | Approved → link to the dashboard | KYC-2 to KYC-4 |

## 3. Home (all roles; content by area)

### SL-HOME — Seller home

- **Template:** `TPL-DASH`.
- **Content:**
  1. State banners ([navigation](navigation.md) §2.1).
  2. Key figures (today and last 7 days): orders, sales value, available balance with next payout date, seller rating, performance score and level.
  3. **Action queue**, most urgent first, each with a countdown and a link: orders awaiting confirmation; orders to hand over today; return requests awaiting a response; returns to inspect; disputes awaiting a response; restock tasks; low-stock offers; documents expiring; policy warnings and violations.
  4. Setup checklist until complete: store profile, pickup address, first offer, payout destination verified.
  5. Announcements from Nyazek.
- **Actions:** open any item; dismiss an announcement.
- **States and guards:** a new seller with no orders sees the checklist first; staff roles see only what their role allows ([navigation](navigation.md) §2.3).
- **Rules:** [seller-dashboard](../03-sellers/seller-dashboard.md) §2 · SLA-3 · figures from Analytics read models (DAT-4 for money)

## 4. Orders (area: Orders)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-ORD-LIST | `TPL-LIST` | Tabs per [taxonomy-and-labels](taxonomy-and-labels.md) §3.1 with counts: Awaiting confirmation · Processing · Ready to ship · Shipped · Delivered · Cancelled · Returned. Columns: sub-order number, placed at, items (count and first title), total, payment type (prepaid or COD), destination governorate, status chip, countdown to the SLA deadline. Search by number or product; filters by date, governorate, payment type | Open; bulk confirm, bulk mark ready, bulk print labels for selected rows in the same state | Held sub-orders are not listed; default tab is Awaiting confirmation when it is not empty | Seller SLAs, SLA-1 to SLA-5 |
| SL-SHIP-PICKUP | `TPL-LIST` | Tabs: To arrange · Scheduled · Completed · Failed. Shipments ready to ship with courier, pickup address, slot and the handover deadline | Request a pickup slot for selected shipments; declare drop-off; reschedule a failed pickup | A failed pickup shows the recorded reason and whether it counts against the seller | Pickup rules, SHP-4 |

### SL-ORD-DETAIL — Order detail (one sub-order)

- **Template:** `TPL-DETAIL`.
- **Content:**
  1. Header: sub-order number, status chip, countdown to the current deadline, payment type; COD amount to be collected by the courier where relevant.
  2. Items: image, title, variant, seller SKU, quantity, unit price, line total, serial numbers once captured.
  3. Delivery: recipient name, governorate, district, neighbourhood, landmark and notes; the customer's phone in full while the sub-order is being fulfilled (`CONFIRMED`, `READY_TO_SHIP`), masked in every other state and in lists (SDB-7). The label carries it for the courier (SHP-6).
  4. Shipment: courier, waybill, pickup or drop-off arrangement, tracking timeline.
  5. Money: items total, seller-funded discounts, expected commission and net proceeds, and when they become available (escrow and remittance states in seller words).
  6. Documents: label, packing slip, receipt.
  7. History timeline; linked return or dispute.
- **Actions (as allowed by state):** confirm; reject (reason select; out-of-stock offers a stock correction); mark ready to ship (asks for serial numbers where the category requires them; one parcel per sub-order, ORD-4); print label, packing slip and receipt; arrange pickup or drop-off; confirm receipt of a returned parcel (`RTO_IN_TRANSIT` delivered back, with the condition of each unit; logistics §9); report a problem to support (`SF-ST-CONTACT`, seller topic, until seller tickets ship, SUP-10).
- **States and guards:** cancelled sub-orders show who cancelled, the reason and whether it counts toward performance; after `SHIPPED` no fulfilment action is offered except confirming an RTO receipt; a seller in `SUSPENDED` or `CLOSING` keeps these actions for open sub-orders (SLA-7); a customer cancellation arriving after confirmation shows a prominent "Do not ship" notice.
- **Rules:** sub-order machine · SLA-2 to SLA-7 · SHP-5, SHP-6 · SDB-7 · COM-5 · WAL-1 to WAL-5 · PRF-4

## 5. Catalog (area: Catalog)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-CAT-OFFERS | `TPL-LIST` | Tabs: Active · Out of stock · Draft · Paused · Suspended. Columns: image, product title and variant, seller SKU, condition, price, available stock, Buy Box state (winning, not winning, not eligible with the reason), offer status. Search by title, SKU or barcode; filters by category and brand | Create offer; edit; inline price and stock edit; bulk pause, resume, price change by amount or percentage (step-up above `cfg:sellers.bulk_price_change_confirm_percent`, SDB-3), stock update; export | Listing-cap usage shown ("42 of 100 offers"); creating is disabled at the cap or when the seller state blocks it, with the reason | Offer states, listing caps, BBX-1 |
| SL-CAT-OFFER-NEW | `TPL-WIZARD` | Per FL-9: product search, variant pick, offer fields | Save draft; publish | Gated brand without authorisation: explanation and how to apply; category needing a licence the seller lacks: blocked with the reason | [catalog-listings](../02-commerce/catalog-listings.md) §4.2, PRC-1 to PRC-7 |
| SL-CAT-OFFER-EDIT | `TPL-FORM` | The offer fields; read-only product summary; current Buy Box state and reason; price-rule notices; change history | Save; pause or resume; archive | Suspended offers show the reason and what resolves it | PRC-1 to PRC-6 |
| SL-CAT-REQ | `TPL-LIST` | Tabs: In review · Changes needed · Approved · Rejected. Columns: title, category, submitted at, status, time in review | Submit a new product; open | – | CAT-5 |
| SL-CAT-REQ-NEW | `TPL-WIZARD` | Per FL-10 | Save draft; submit | Duplicate warning with "Sell this product instead"; mandatory attributes per category; media checks at upload | [catalog-listings](../02-commerce/catalog-listings.md) §5, §8 |
| SL-CAT-REQ-DETAIL | `TPL-DETAIL` | The submission; results of automated checks, each passed or failed with the reason; reviewer decision and notes; resulting product and offer links when approved | Edit and resubmit when changes are needed; withdraw; "Suggest an edit" on an approved shared product (P1) | – | CAT-5 to CAT-9 |
| SL-CAT-IMPORT | `TPL-WIZARD` | Per FL-11; plus the list of past imports with status | Download template; upload; map; dry run; confirm | File type, size and row limits stated before upload | [catalog-listings](../02-commerce/catalog-listings.md) §9, CAT-7 |
| SL-CAT-IMPORT-JOB | `TPL-DETAIL` | Progress; counts created, updated, matched, sent for review, failed; row-level error report | Download the report; download failed rows as a file to fix and re-upload | Job continues if the page is closed | [catalog-listings](../02-commerce/catalog-listings.md) §9 |
| SL-CAT-STOCK | `TPL-LIST` (editable grid) | One row per offer: product, variant, SKU, price, available, reserved (read-only), low-stock threshold | Edit price, stock and threshold inline; save all changes at once (step-up for price changes above `cfg:sellers.bulk_price_change_confirm_percent`, SDB-3); import and export the grid | Each cell validates against price rules; a row that fails keeps its old value and shows why | STK-2, PRC-1 |
| SL-CAT-ALERTS | `TPL-LIST` | Offers at or below their threshold, and those out of stock, with recent sales rate | Update stock; change threshold | – | STK-3 |
| SL-CAT-VIOL | `TPL-LIST` | Tabs: Open · Resolved. Violations: offer, rule (price floor, anti-dumping hold, MAP, content), what was detected, what to do, state of any review | Fix the offer; submit a justification (text and evidence) for an anti-dumping hold | – | PRC-3 to PRC-5, PRH-3 |

## 6. Returns and disputes (area: Returns and disputes)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-RET-LIST | `TPL-LIST` | Tabs: Needs response (`REQUESTED`) · Coming back (`APPROVED`, `IN_TRANSIT`) · To inspect (`RECEIVED`) · Awaiting customer or dispute (`CONTESTED`, `IN_DISPUTE`, `REJECTED` within the dispute window) · Closed (`ACCEPTED` onward, `CLOSED`). Columns: return number, sub-order, items, reason, status chip, countdown | Open | Default tab is the first non-empty one | RET-3 |
| SL-RET-DETAIL | `TPL-DETAIL` | Customer's reason and evidence; items and quantities; who pays return shipping for this reason; return shipment tracking; inspection form when received: per unit the condition `RESELLABLE`, `DAMAGED` or `NOT_AS_SENT` and the outcome accept or contest; contesting requires photos and a note and allows an optional partial-refund proposal (RET-4, RET-12); refund amount and its effect on the wallet; restock task; timeline | Approve; reject with a policy reason; record the inspection; propose a partial refund; confirm restock with quantity | Doing nothing by a deadline advances the return automatically, and the page says so with the countdown | Return machine, RET-3, RET-4, STK-5 |
| SL-DISP-LIST | `TPL-LIST` | Tabs: Needs response (`SELLER_RESPONSE`) · Under review (`UNDER_REVIEW`, `REVIEW_REQUESTED`) · Closed (resolved or withdrawn). Columns: dispute number, type, sub-order, amount at stake, status, countdown | Open | – | DSP-1 |
| SL-DISP-DETAIL | `TPL-DETAIL` | The customer's claim and evidence; proof of delivery where relevant; response form with evidence uploader; decision with reasons; money effect on the wallet; timeline | Respond with evidence; accept the customer's claim (resolves for the customer); add evidence; request a review within the review window after a decision | Funds on hold for the dispute are shown | DSP-2 to DSP-6, WAL-4 |
