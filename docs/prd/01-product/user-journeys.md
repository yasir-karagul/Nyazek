# User Journeys & Edge Cases

**Authoritative for:** the end-to-end journeys the product must support, the pages and rules each journey passes through, and the register of cross-cutting edge cases.
**How to use it:** every journey is an end-to-end test ([testing-quality](../08-engineering/testing-quality.md) §2) and a design walkthrough. A journey never defines a rule; it links to the document that does. Page IDs refer to the [sitemap](../09-information-architecture/sitemap.md); the screen-by-screen order of multi-page flows is in [flows](../09-information-architecture/flows.md).
**Related:** [users-personas](users-personas.md) · [scope-priorities](scope-priorities.md) · [checkout-orders](../02-commerce/checkout-orders.md) · [returns-disputes](../02-commerce/returns-disputes.md)

---

## 1. Customer journeys

| ID | Journey | Path (pages) | Governing rules | Must also handle |
|---|---|---|---|---|
| JC-1 | First purchase as a guest, cash on delivery | `SF-HOME` → `SF-SEARCH` → `SF-PDP` → `SF-CART` → `SF-CHK-ADDR` (phone OTP) → `SF-CHK-SHIP` → `SF-CHK-PAY` → `SF-CHK-DONE` → SMS → `SF-CHK-CODCONF` | CHK-1, GST-1 to GST-4, QTE-1, CODC-1 to CODC-3, ID-11 | Phone already has a customer account (GST-2); phone belongs to a seller (refused); address not serviceable (ADR-3); COD not offered to this customer (§4 of fraud-risk); confirmation never given (auto-cancel) |
| JC-2 | Signed-in customer, prepaid, items from several sellers | `SF-AUTH-LOGIN` → `SF-CART` → checkout → wallet redirect → `SF-CHK-RETURN` → `SF-CHK-DONE` | §5.1 place-order flow, PAY-5 to PAY-10, ORD-5, RSV-3 | Payment fails or expires; payment succeeds late (PAY-9); paid twice (PAY-10); price or stock changed (QTE-2); one seller rejects (only that sub-order refunded) |
| JC-3 | Track and receive | `SF-ORD-LIST` → `SF-ORD-DETAIL` → `SF-ORD-TRACK`; notifications | Sub-order state machine, DLV-1 to DLV-4 | Reschedule once; courier without "out for delivery" status; parcels from different sellers arriving on different days |
| JC-4 | Cancel before shipping | `SF-ORD-DETAIL` → cancel | Cancellation table, ORD-5 to ORD-7 | Waybill already printed (voided); coupon and points reversal; COD versus prepaid refund |
| JC-5 | Refuse the parcel or miss every attempt | Courier attempt(s) → `DELIVERY_FAILED` | DLV-5, failed-delivery attribution, ORD-9, COD suspension rule | Prepaid refund less the outbound fee (D-31); effect on COD eligibility; customer disputes the "refused" reason |
| JC-6 | Return an item and get a refund | `SF-ORD-DETAIL` → `SF-RET-NEW` → `SF-RET-DETAIL`; `SF-REFACC` for COD orders | RET-1 to RET-8, refund table, REF-1 to REF-6, PAY-14 to PAY-17 | Seller silent (auto-approve); partial return of a discounted order; seller contests; return after escrow release; change-of-mind fee; return parcel lost |
| JC-7 | Dispute: "delivered" but not received | `SF-DISP-NEW` → `SF-DISP-DETAIL` | Dispute windows and machine, DSP-1 to DSP-5, DLV-3 | Weak proof of delivery; decision above the agent limit; review request with new evidence |
| JC-8 | Review a purchase | Reminder → `SF-REV-PENDING` → review | REV-1 to REV-8 | Text with a phone number (moderation); linked-account block; order later refunded |
| JC-9 | Come back after a long absence or with a recycled number | `SF-AUTH-LOGIN` → OTP → second factor | Recycled phone rule, AUTH-5 | No second factor available (old account closed, new one created) |
| JC-10 | Export or delete personal data | `SF-PRIV` | DSR-1 to DSR-3, CUS-12 to CUS-15 | Open order, return, dispute or refund blocks deletion; points forfeited |
| JC-11 | Save and come back | `SF-FAV`, alerts (P1), cart on another device | CUS-3 to CUS-11, CRT-1, CRT-2 | Product merged or unpublished; offer no longer valid |

## 2. Seller journeys

| ID | Journey | Path (pages) | Governing rules | Must also handle |
|---|---|---|---|---|
| JS-1 | Register, pass KYC, go live | `SF-SELL-LANDING` → `SL-AUTH-REGISTER` → `SL-AUTH-VERIFY` → `SL-AUTH-2FASETUP` → `SL-ONB-*` → `SL-ONB-STATUS` → `SL-HOME` | ID-1 to ID-7, KYC-1 to KYC-9, seller states | Email already used by a customer account (AUTH-2); documents rejected and resubmitted; duplicate identity document; regulated-category licence |
| JS-2 | List products | `SL-CAT-OFFER-NEW` (existing product) · `SL-CAT-REQ-NEW` (new product) · `SL-CAT-IMPORT` | CAT-1 to CAT-13, PRC-1 to PRC-10, listing caps | Duplicate detected; price below floor or MAP; anti-dumping hold; missing mandatory attribute; cap reached; gated brand |
| JS-3 | Fulfil an order | Notification → `SL-ORD-LIST` → `SL-ORD-DETAIL` → confirm → label → `SL-SHIP-PICKUP` → shipped | Seller SLAs, SLA-1 to SLA-5, LOG-1, SHP-1 to SHP-6 | Order on hold for COD confirmation; out of stock (reject); SLA about to breach; pickup fails; customer cancels after confirmation |
| JS-4 | Handle a return | `SL-RET-LIST` → `SL-RET-DETAIL` → inspect → restock | Return machine, RET-3, RET-4, STK-5 | Item not as sent (contest with evidence, partial refund proposal); no response in time; return shipping charged to the seller |
| JS-5 | Get paid | `SL-WAL-HOME` → `SL-WAL-TX` → `SL-WAL-PAYOUT` → `SL-WAL-INV` | WAL-1 to WAL-11, PO-1 to PO-10, COM-1 to COM-5 | COD not yet remitted; hold after a late return; deficit; payout fails; destination change with 72-hour hold |
| JS-6 | Performance drops and recovers | `SL-PERF` → appeal | PRF-1 to PRF-11 | Not enough data; customer-caused cancellations excluded; repeat offence; authenticity override |
| JS-7 | Keep the account valid | `SL-ACC-KYC` → renewal | KYC-7, KYC-8 | Identity document lapses (restricted); licence lapses (only affected offers suspended) |
| JS-8 | Take a break or leave | `SL-SET-VACATION` · `SL-ACC-CLOSE` | Vacation mode, closure rules | Open orders during vacation; final settlement after the last return window |

## 3. Staff journeys

| ID | Journey | Role | Path (pages) | Governing rules |
|---|---|---|---|---|
| JA-1 | Review a seller application | Seller Manager | `AD-SEL-KYC` → `AD-SEL-KYC-CASE` | KYC-1 to KYC-6, RBAC-4 |
| JA-2 | Review a new-product request | Catalog Manager | `AD-CAT-REQUESTS` → `AD-CAT-REQUEST` | CAT-5, CAT-6, automated checks |
| JA-3 | Clear held orders | Support, Fraud/Risk | `AD-ORD-COD` · `AD-RISK-QUEUE` → `AD-RISK-CASE` | CODC-2, RSK-5 to RSK-8 |
| JA-4 | Run a file-based courier | Logistics | `AD-LOG-COURIERS` → status upload → `AD-ORD-EXC` | Courier tiers, SHP-1 to SHP-4, ORD-10, ORD-11 |
| JA-5 | Reconcile COD cash | Logistics, Finance | `AD-LOG-COD` → `AD-FIN-RECON` | COD-1 to COD-5, REC-1 to REC-4 |
| JA-6 | Pay a refund by hand | Finance | `AD-FIN-REFUNDS` | PAY-14, PAY-15, dual control |
| JA-7 | Run payouts | Finance (two people) | `AD-FIN-FUNDING` → `AD-FIN-PAYOUTS` → `AD-APPROVALS` → `AD-FIN-FAILED` | PO-1 to PO-6, treasury requirement |
| JA-8 | Decide a dispute | Support, Finance | `AD-DISP-LIST` → `AD-DISP-DETAIL` | DSP-1 to DSP-5 |
| JA-9 | Act on a listing report or IP notice | Catalog Manager | `AD-CAT-REPORTS` | PRH-1 to PRH-5 |
| JA-10 | Receive 1P stock and sell it | 1P Merchandiser | `AD-1P-STOCK` → `AD-1P-OFFERS` → `AD-1P-ORDERS` | FP-1 to FP-11 |
| JA-11 | Answer a data-subject request | Compliance | `AD-PRIV-REQ` | DSR-1 to DSR-3 |
| JA-12 | Change a sensitive setting | Any owner role + approver | `AD-SET-*` → `AD-APPROVALS` | DC-1 to DC-3, configuration rules |
| JA-13 | Suspend a seller for fraud | Fraud/Risk, Seller Manager | `AD-USR-SELLER` → freeze → `AD-APPROVALS` | SEL-3, SEL-4, wallet holds |
| JA-14 | Help a customer who phones or writes | Support | `AD-SUP-LIST` → `AD-SUP-DETAIL` | SUP-1 to SUP-11, ADM-6 |

## 4. Edge-case register

Situations that cross documents. "Rule" names where the behaviour is defined; entries marked *new in v7.1* were unspecified before this review.

| ID | Situation | Required behaviour | Rule |
|---|---|---|---|
| EC-1 | Category return window or policy changes after an order was placed | The order line keeps the window and policy snapshotted at placement | RET-6 *(new in v7.1)* |
| EC-2 | Customer asks to return more units than were delivered, or the same unit twice | Rejected: returnable quantity = delivered − already in a return | RET-7 *(new)* |
| EC-3 | Partial return brings the order below the free-delivery threshold | No retroactive shipping charge | REF-4 *(new)* |
| EC-4 | Return or refund is due but the seller is suspended, closing or closed | Nyazek handles the return; refund is paid on schedule and recorded against the seller | REF-5 *(new)* |
| EC-5 | Customer changes phone number while a COD order is open | The order keeps its phone snapshot for delivery, OTP and confirmation | ADR-4, ORD-13 *(new)* |
| EC-6 | Prepaid payment failed; customer wants to pay cash instead | Not a retry: the customer places a new order, which passes COD eligibility | PAY-18 *(new)* |
| EC-7 | Seller deletes a pickup address used by live offers or open orders | Blocked until offers are moved and orders are terminal | SEL-5 *(new)* |
| EC-8 | Seller renames the store | Slug redirects; rate-limited; name pre-screened | SEL-6 *(new)* |
| EC-9 | Same GTIN submitted for two different products | Held for the Catalog queue; never auto-merged | CAT-11 *(new)* |
| EC-10 | Variant or product removed while offers, carts or favourites reference it | Archived, not deleted; offers end; carts and favourites show it as unavailable | CAT-12 *(new)*, CRT-2, CUS-7 |
| EC-11 | Product moved to another category | Attributes revalidated; existing orders keep their frozen commission and return terms | CAT-13 *(new)*, COM-5, RET-6 |
| EC-12 | Product recalled or found unsafe after sale | Offers suspended; customers of the affected batch notified | PRH-5 *(new)* |
| EC-13 | Lost parcel on a 3P order | Customer refunded at once; seller compensated per courier contract; claim tracked | JE-38, JE-39 *(new)* |
| EC-14 | Two devices edit one cart | Last write wins per line with a version check; the other device refreshes | CRT-6 *(new)* |
| EC-15 | Price, stock or coupon changes between cart and placement | Customer must confirm the new quote | QTE-2 |
| EC-16 | Payment confirmed after the order expired | The order stays expired; the amount is refunded automatically and the customer can restore the cart | PAY-9, ORD-16 |
| EC-17 | Courier events arrive late, duplicated or out of order | Never regress a status | SHP-2 |
| EC-18 | Seller silent on a return at every step | Auto-advance in the customer's favour | RET-3 |
| EC-19 | Refund destination rejects the transfer | Manual review, new destination requested from the customer | Refund machine, PAY-14 |
| EC-20 | Holiday or force majeure during a seller SLA | Clock paused by admin declaration | SLA-1 |
| EC-21 | Account deletion with points, coupons or a negative points balance | Forfeited or written off after warning | CUS-13 |
| EC-22 | Region failover in the middle of payments and payouts | Payouts and automatic refunds paused until reconciliation passes | REC-5 |

## 5. Acceptance criteria

- Every journey in §1–§3 marked P0 by its pages has an automated end-to-end test in Arabic, and the customer journeys also in English.
- Every edge case in §4 has at least one automated test named with its ID.
