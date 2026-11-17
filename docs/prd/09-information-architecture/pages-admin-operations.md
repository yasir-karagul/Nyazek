# Admin Panel Pages: Sign-in, Users, Catalogue, 1P, Orders, Logistics, Returns

**Authoritative for:** the content and actions of these Admin Panel pages.
**Read with:** [README](README.md) §2 · [navigation](navigation.md) §3 · [admin-panel](../05-trust/admin-panel.md) (queues and the behaviour common to all admin screens: claim, reason codes, masking, bulk actions, history) · [flows](flows.md) FL-13, FL-14 · [sitemap](sitemap.md) §8.1–8.6
**Rules live in:** [admin-governance](../05-trust/admin-governance.md) · [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) · [catalog-listings](../02-commerce/catalog-listings.md) · [first-party-operations](../03-sellers/first-party-operations.md) · [checkout-orders](../02-commerce/checkout-orders.md) · [logistics](../02-commerce/logistics.md) · [returns-disputes](../02-commerce/returns-disputes.md)

Every page is limited to the roles in the sitemap. Every detail page ends with the object's history (ADM-8) and internal notes (ADM-9); these are not repeated below. Personal data is masked with a logged reveal (ADM-5).

---

## 1. Sign-in, dashboard, approvals

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-AUTH-LOGIN | `TPL-AUTH` | Email and password, after the zero-trust access layer | Sign in → 2FA | No self-registration, no social sign-in, no "forgot password" self-service: a reset is initiated by a Super Admin and approved by a second Super Admin ([identity-access](../05-trust/identity-access.md) §4) | [admin-governance](../05-trust/admin-governance.md) §1, [security](../05-trust/security.md) |
| AD-AUTH-2FA | `TPL-AUTH` | Authenticator code or hardware key; first sign-in runs setup with recovery codes | Verify | No SMS fallback for admins | 2FA rules |
| AD-AUTH-INVITE | `TPL-AUTH` | Name, roles granted, set password, then 2FA setup | Accept | Expired or used invitation; email belonging to another account is refused | ID-1 |
| AD-HOME | `TPL-DASH` | Widgets by role: each main queue with count, oldest age and breaches; key figures for the role's domain; system notices (provider outage, payouts paused, reconciliation unsigned) | Open a queue | A role with no widgets sees a neutral welcome | ADM-10 |
| AD-APPROVALS | `TPL-QUEUE` | Tabs: Awaiting my decision · My requests · Decided. Columns: action type, object, requester, requested at, expires in. Detail per FL-14 | Approve or reject with a reason (step-up) | An admin never sees their own request under "Awaiting my decision" | DC-1 to DC-3 |

## 2. Users and sellers

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-USR-CUSTOMERS | `TPL-LIST` | Tabs: Active · Suspended · Blocked. Columns: customer reference, name, phone (masked), registered, orders, risk tier, account state. Search by reference or order number; by phone or email only with the permission (ADM-4) | Open | – | [identity-access](../05-trust/identity-access.md) §8 |
| AD-USR-CUSTOMER | `TPL-DETAIL` | Profile (masked), account state and whether claimed; orders; returns and disputes; tickets; risk tier with its factors, return-abuse score, COD eligibility and overrides; consents; sessions | Suspend or reinstate (reason); set a risk override with expiry (Fraud/Risk); revoke sessions; open a ticket on the customer's behalf (ADM-6) | Staff cannot change login identifiers or view passwords or OTPs | RSK-7, RSK-8, [identity-access](../05-trust/identity-access.md) §8 |
| AD-USR-SELLERS | `TPL-LIST` | Tabs by seller state: Active · In onboarding · Restricted · Suspended · Closing · Closed · Rejected. Columns: store name, type, state, performance level, live offers, 30-day orders, wallet available, joined | Open | – | Seller states |
| AD-USR-SELLER | `TPL-DETAIL` | Tabs: Overview (identity, state, level, key figures) · KYC (documents, expiry, verification history) · Offers · Orders · Performance · Wallet (balances, holds, payouts; Finance roles) · Staff · Violations and appeals | Correct the store slug (Seller Manager, SEL-6); restrict, suspend, reinstate (reason; suspension for fraud freezes the wallet under dual control); set listing-cap override; set the payout cycle (Finance, PO-1); view as seller (P1) | Actions shown by role | SEL-3, SEL-4, listing caps, [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §5 |
| AD-SEL-KYC | `TPL-QUEUE` | Applications: store name, seller type, submitted at, attempt number, time to target, flags (duplicate document, mismatch) | Claim and open | – | KYC-2 |
| AD-SEL-KYC-CASE | `TPL-DETAIL` (decision view) | Business details; each document with a viewer beside the entered data (number, expiry, name); payout destination and holder-name match; duplicate-document and linked-account flags; previous attempts | Approve; request information (choose the items and write the request); reject with reason codes | Document viewing is logged; approval is blocked while a mandatory document is unverified | KYC-1 to KYC-6 |
| AD-SEL-PERF | `TPL-LIST` | Sellers with score, level, each metric, trend, time at level, active consequences. Filters by level and category | Open a seller; lift a Level 4 restriction with a reason (PRF-9) | – | PRF-8 to PRF-11 |
| AD-SEL-APPEALS | `TPL-QUEUE` | Appeals: seller, subject, submitted at, time to target | Uphold, partly uphold or reject with reasons | P1 | Appeals |
| AD-USR-ADMINS | `TPL-LIST` | Admin users: name, email, roles, 2FA state, last sign-in, state | Invite (email and roles); change roles; deactivate; reset password or 2FA (dual control, [identity-access](../05-trust/identity-access.md) §4) | Super Admin only; role changes under dual control; an admin cannot change their own roles | RBAC-1, DC-1 |
| AD-USR-ROLES | `TPL-SETTINGS` | The eleven roles; the permission matrix (role × domain: none, read, manage, approve); dual-control thresholds | Edit a role's permission list; edit thresholds | The eleven roles are fixed; no role can be added or removed; every change under dual control (RBAC-3) | [admin-governance](../05-trust/admin-governance.md) §2–3 |

## 3. Catalogue

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-CAT-PRODUCTS | `TPL-LIST` | Columns: image, title, brand, category, listing type, variants, live offers, state. Search by title, barcode or product code; filters by category, brand, state, type | Create a product; open | – | [catalog-listings](../02-commerce/catalog-listings.md) §3 |
| AD-CAT-PRODUCT | `TPL-DETAIL`, with each tab editable in place | Tabs: Content (titles and descriptions in both languages, attributes per schema, media) · Variants (identifiers, package data) · Offers (all sellers' offers with price, stock, state, Buy Box) · Reviews · History | Edit content; add or archive a variant; move category; unpublish; suspend an offer with a reason | Category move revalidates attributes (CAT-13); archive instead of delete (CAT-12) | CAT-1 to CAT-13 |
| AD-CAT-REQUESTS | `TPL-QUEUE` | Requests: title, seller, category, type, automated-check summary, time to target | Claim and open | – | CAT-5 |
| AD-CAT-REQUEST | `TPL-DETAIL` (decision view) | The submission as the customer would see it (preview) beside the data; automated-check results; likely duplicates with comparison; seller's standing | Approve (as a shared product or as the seller's own listing); request changes with notes per field; reject with reason codes; merge into an existing product | – | CAT-5 to CAT-9, CAT-11 |
| AD-CAT-EDITS | `TPL-QUEUE` | Suggested edits to shared products: field, current and proposed value, proposer | Accept, edit and accept, reject | P1 | CAT-1 |
| AD-CAT-VIOL | `TPL-QUEUE` | Offers held or flagged: rule, detected value against the limit, seller's justification | Release; uphold (keep suspended); record a MAP notice | – | PRC-3 to PRC-5 |
| AD-CAT-REPORTS | `TPL-QUEUE` | Listing reports and intellectual-property notices: listing, reason, reporter type, count of reports, time to target | Dismiss; suspend the offer or product; escalate to Compliance; reply to the notifier | Safety and IP notices are prioritised | PRH-1 to PRH-5 |
| AD-CAT-DUP | `TPL-LIST` | Candidate duplicate pairs with similarity signals | Merge (choose the survivor; preview what moves); mark not duplicates | P1 | CAT-10 |
| AD-CAT-CATS | `TPL-LIST` (tree) and `TPL-FORM` | Category tree. Node form: names and slug in both languages, parent, order, image, attribute schema (attributes, mandatory, filterable, variant-defining), compliance flags, return policy, commission link, weight defaults | Add, edit, reorder, hide | A node with products cannot be deleted; slug changes create redirects | [catalog-listings](../02-commerce/catalog-listings.md) §2 |
| AD-CAT-BRANDS | `TPL-LIST` and `TPL-FORM` | Brands: names, logo, gated or open, authorised sellers with documents and expiry, MAP values where the brand provides them | Add, edit, gate, authorise a seller | – | Brand gating, PRC-5 |
| AD-CAT-ATTR | `TPL-LIST` and `TPL-FORM` | Attribute definitions: code, names, type (text, number with unit, single or multiple choice), allowed values with translations, where used | Add, edit, retire | An attribute in use cannot be deleted; value codes are stable | [catalog-listings](../02-commerce/catalog-listings.md) §2 |
| AD-CAT-COMPL | `TPL-SETTINGS` | Prohibited keywords and patterns (both languages); restricted categories and the licence each requires; regulated-category rules | Edit (Catalog Manager; Compliance reads, admin-governance §2.1) | Changes are audited and take effect for new submissions; a rescan of live listings can be started | PRH-1, PRH-4 |

## 4. 1P store

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-1P-OFFERS | `TPL-LIST` | 1P offers: product, variant, price, cost, margin, available stock, Buy Box state | Create or edit an offer; inline price edit | Cost and margin columns only for permitted roles; a price below the margin floor raises the PRC-8 alert | FP-2, FP-3, PRC-8 |
| AD-1P-STOCK | `TPL-LIST` and `TPL-FORM` | Tabs: On hand (by variant: quantity, value, batches with expiry) · Receipts · Adjustments. Receipt form: supplier, reference, date, lines (variant, quantity, unit cost, batch, expiry, serials). Adjustment form: variant, quantity, reason code, evidence | Record a receipt; record an adjustment; record a stock count | Adjustments above the threshold go to approval | FP-5 to FP-10 |
| AD-1P-ORDERS | `TPL-LIST` and `TPL-DETAIL` | The seller order list and detail for the 1P store (same tabs and fields as `SL-ORD-LIST` and `SL-ORD-DETAIL`), plus pick list | Confirm, mark ready, print, arrange pickup | Stock is allocated first-expiring-first | FP-7, [first-party-operations](../03-sellers/first-party-operations.md) §6 |
| AD-1P-RETURNS | `TPL-QUEUE` | Returned and RTO parcels to inspect and restock: source (return or failed delivery), items, received at | Record inspection and disposition (restock, write off, return to supplier) | – | FP-11 |
| AD-1P-MARGIN | `TPL-LIST` | Alerts: offers below the margin threshold or below cost, ageing and expiring stock | Open the offer; acknowledge | – | PRC-8 |
| AD-1P-SUPPLIERS | `TPL-LIST` and `TPL-FORM` | Supplier records per [first-party-operations](../03-sellers/first-party-operations.md) §2; receipts and payable balance per supplier | Add, edit | – | – |
| AD-1P-PO | `TPL-LIST` | Purchase orders | – | P2 | – |

## 5. Orders and logistics

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-ORD-LIST | `TPL-LIST` | Tabs per [taxonomy-and-labels](taxonomy-and-labels.md) §3.1. Columns: order number, placed at, customer reference, shipments with exact states, total, payment method and status, governorate, flags (held, exception, dispute). Search by order, sub-order, waybill; filters by exact state, seller, courier, payment method, date | Open | – | – |
| AD-ORD-COD | `TPL-QUEUE` | COD orders awaiting confirmation: time left, customer risk tier, attempts made (SMS, call) | Record a call outcome; confirm or cancel on the customer's instruction; resend the SMS | – | CODC-2, CODC-3 |
| AD-ORD-EXC | `TPL-QUEUE` | Tabs: SLA breaches · Stuck states · Failed deliveries to attribute · Unknown courier statuses · Pickup failures. Each row: what is wrong, since when, the object | Apply the allowed remedy for the exception (remind or cancel for the seller; set the failed-delivery reason; map a status; reassign courier) | – | ORD-10, ORD-11, SHP-1, SHP-4, failed-delivery table |
| AD-LOG-COURIERS | `TPL-LIST` and `TPL-FORM` | Couriers: tier, status, service areas, performance summary. Form: integration type, status mapping table, COD terms and remittance cycle, exposure cap, fallback order. Upload area for status files and COD statements (file-based couriers) with import results | Add, edit, pause; upload a file | Unmapped statuses in a file are listed and go to the exceptions queue | Courier tiers, SHP-1, COD-1 |
| AD-LOG-SERVICE | `TPL-LIST` (matrix) | Governorate › district rows by courier columns: served, COD available, COD limit, hazardous accepted, estimate days. Bulk edit and import | Edit cells; import | A change that leaves an area with no courier warns before saving | SVC-1 to SVC-6 |
| AD-LOG-PERF | `TPL-DASH` | Per courier and governorate: delivery success, on-time rate, average days, RTO rate, lost and damaged, remittance timeliness | Change period; export | – | – |
| AD-LOG-COD | `TPL-LIST` and `TPL-DETAIL` | Tabs: Expected · Statements · Exceptions. Expected: delivered COD shipments not yet remitted, by courier with ageing and exposure against the cap. Statement detail: lines matched, short, over, unknown | Import or open a statement; match manually; record a resolution for an exception; confirm a remittance (Logistics) | Exposure over the cap is highlighted and can pause COD assignment to that courier | COD-1 to COD-5 |
| AD-LOG-PICKUPS | `TPL-LIST` | Pickups by day, courier and seller: scheduled, completed, failed with reason | Reschedule; attribute a failure | – | Pickup rules |

### AD-ORD-DETAIL — Order detail

- **Template:** `TPL-DETAIL`.
- **Content:** header (order number, derived status, placed at, channel); customer summary (reference, masked contact, risk tier, link); payment (method, intent status, provider reference, amounts captured and refunded; COD collection state); one shipment block per sub-order in the admin variant (seller, exact state and reason codes, items, courier and waybill, raw courier events, SLA timers, proof of delivery, linked return and dispute); address (masked); quote as charged with the funding of each discount; ledger entries for the order (Finance roles); documents; history.
- **Actions (by role and state):** cancel a sub-order with a reason; move a sub-order along a transition the machine allows (reason, audited; after `SHIPPED` dual control); release an `ON_HOLD` sub-order after risk review or COD confirmation by phone; reassign the courier; trigger a refund (creates a refund request; above the threshold, approval); record goodwill compensation (approval); open a ticket; resend a notification.
- **States and guards:** no action can produce a state the machine forbids (ORD-12); money actions never edit amounts directly, they create refund or adjustment requests.
- **Rules:** [checkout-orders](../02-commerce/checkout-orders.md) §6–8 · ORD-10 to ORD-12, ORD-16 · [payments](../04-finance/payments.md) §6 · DC-1

## 6. Returns and disputes

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-RET-LIST | `TPL-LIST` | Tabs: Open (`REQUESTED` to `RECEIVED`, `ACCEPTED`) · Contested or in dispute (`CONTESTED`, `IN_DISPUTE`) · Overdue (seller or courier) · Closed (`REFUNDED`, `CLOSED`, `EXPIRED`, `CANCELLED`). Columns: return number, order, seller, reason, state, age | Open | – | Return machine |
| AD-RET-DETAIL | `TPL-DETAIL` | Customer reason and evidence; seller response and inspection; return shipment; refund request and status; who bears return shipping; timers | Act in the seller's place when the seller is suspended or closed (REF-5); override an outcome with a reason; mark a return parcel lost | – | RET-3, RET-4, REF-5 |
| AD-DISP-LIST | `TPL-QUEUE` | Tabs: Awaiting seller (`OPENED`, `SELLER_RESPONSE`) · Awaiting decision (`UNDER_REVIEW`) · Review requested (`REVIEW_REQUESTED`) · Closed (`RESOLVED_*`, `WITHDRAWN`, `CLOSED`; a resolved dispute shows its review-window countdown until it closes). Columns: dispute number, type, amount, order, seller, time to target | Claim and open | – | DSP-1 |
| AD-DISP-DETAIL | `TPL-DETAIL` (decision view) | Both parties' statements and evidence side by side; proof of delivery; order and shipment facts; each party's history (customer return and dispute record, seller performance); decision panel with outcome, amount for a split, reason codes and the text each party will see | Decide; ask a party for more evidence; escalate to Finance above the limit | Decisions above the agent limit go to approval; a review is decided by a different person | DSP-2 to DSP-5 |
