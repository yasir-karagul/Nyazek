# Flows

**Authoritative for:** the order of screens in multi-page flows, what each step requires before the next, what "back" does, and where each flow can exit.
**Not here:** the business rules applied at each step (linked) and the journeys with their edge cases ([user-journeys](../01-product/user-journeys.md), which says *what* must be possible; this document says *through which screens*).

| ID | Flow | Application |
|---|---|---|
| FL-1 | Checkout | Storefront |
| FL-2 | Prepaid payment and return | Storefront |
| FL-3 | COD confirmation | Storefront |
| FL-4 | Customer sign-in, registration and recovery | Storefront |
| FL-5 | Return request | Storefront |
| FL-6 | Dispute | Storefront |
| FL-7 | Account deletion | Storefront |
| FL-8 | Seller registration and onboarding | Seller Dashboard |
| FL-9 | Creating an offer on an existing product | Seller Dashboard |
| FL-10 | New-product request | Seller Dashboard |
| FL-11 | Bulk import | Seller Dashboard |
| FL-12 | Fulfilling an order | Seller Dashboard |
| FL-13 | Queue decision | Admin Panel |
| FL-14 | Dual-control approval | Admin Panel |
| FL-15 | Payout run | Admin Panel |

---

## FL-1 Checkout

| Step | Page | To continue | Back | Notes |
|---|---|---|---|---|
| 1 | `SF-CART` | No blocking flag on any line; at least one line | – | "Checkout" is disabled with the reason while a line is unavailable |
| 2 | `SF-CHK-ADDR` | A serviceable address; for a guest, a phone verified by OTP and the 18+ confirmation | Cart (session abandoned, reservation released) | The checkout session is created here (CHK-1). A signed-out customer may sign in or continue as a guest; choosing sign-in returns here |
| 3 | `SF-CHK-SHIP` | Nothing to choose; "Continue" | Address (session kept) | Shows shipments, estimates and fees |
| 4 | `SF-CHK-PAY` | A payment method; "Place order" | Shipping | Final quote. If the quote changed, a dialog shows old and new totals and asks to confirm (QTE-2) |
| 5a | `SF-CHK-DONE` | – | Browser back leads to the order, not to payment | COD orders arrive here directly |
| 5b | FL-2 | – | – | Prepaid orders |

- Opening a later step without the earlier ones redirects to the first incomplete step. Opening any step with an empty cart redirects to the cart.
- If the reservation lapses and cannot be renewed, the customer is returned to the cart with the affected lines flagged (CHK-4).
- Refreshing or resubmitting "Place order" never creates a second order (ORD-8).
- A guest whose phone already belongs to an account is signed in by the OTP and continues with that account's saved addresses, subject to the recycled-number and 2FA checks; if the recycled-number check fails, checkout continues with a new account for the number (GST-2, ID-REC-1).

## FL-2 Prepaid payment and return

1. "Place order" with a prepaid method creates the order (`AWAITING_PAYMENT`) and sends the customer to the provider's page or app.
2. The provider returns the customer to `SF-CHK-RETURN`, which shows "Confirming your payment" and polls.
3. Outcomes: **paid** → `SF-CHK-DONE`; **failed** → the same page offers "Try again" (same or another prepaid method, until the payment deadline, shown as a countdown; ORD-16) and "Cancel order"; **still pending after the polling period** → "We will notify you" with a link to the order; **expired** (deadline passed) → explanation and "Restore to cart" (CRT-7); a payment that still arrives is refunded automatically (PAY-9).
4. Closing the browser at the provider changes nothing: the order page shows the same state and actions when the customer comes back (PAY-6, PAY-9). Switching to cash on delivery means placing a new order (PAY-18).

## FL-3 COD confirmation

1. After a COD order that needs confirmation, `SF-CHK-DONE` and the order page show "Confirm your order" with the deadline.
2. The SMS link opens `SF-CHK-CODCONF` without sign-in: order summary (items, total to pay in cash, address area) and two actions, "Confirm order" and "Cancel order".
3. Either action shows its result on the same page and makes the link single-use. An expired or used link explains the current state of the order and links to tracking.

## FL-4 Customer sign-in, registration and recovery

| Path | Screens |
|---|---|
| Phone sign-in or registration | `SF-AUTH-LOGIN` (phone) → `SF-AUTH-OTP` → destination. A new phone creates the account after the 18+ confirmation; an existing one signs in. The screens do not reveal which happened until the OTP is verified |
| Password sign-in | `SF-AUTH-LOGIN` (email or phone, password) → destination; after repeated failures a challenge, then a temporary lock message |
| Registration with email | `SF-AUTH-REGISTER` → `SF-AUTH-OTP` (phone) → destination; a verification email is sent and `SF-AUTH-EMAIL` completes it when the link is opened |
| Social | Provider → `SF-AUTH-SOCIAL` → phone verification if the account has no verified phone → destination. A claim conflict shows the generic message (AUTH-2, AUTH-4) |
| Recovery | `SF-AUTH-FORGOT` → uniform confirmation → OTP or emailed link → `SF-AUTH-RESET` → signed in, other sessions revoked |
| Returning after long absence | OTP → second-factor question (recycled-number rule) → destination, or a new account |

Destination is `returnTo` if present, otherwise the page the customer came from, otherwise home. The guest cart and favourites are merged at sign-in.

## FL-5 Return request

1. Entry: "Return items" on a delivered shipment in `SF-ORD-DETAIL`, shown only while at least one line is returnable.
2. `SF-RET-NEW`, one screen in four parts: choose lines and quantities (non-returnable lines listed with the reason) → reason per line → evidence (required or optional per the reason and value) → refund destination (original method, or a refund account for COD; adding one happens in a dialog without leaving) and the refund summary (REF-6).
3. Submit → `SF-RET-DETAIL` with the timeline and next step. The customer may withdraw while `REQUESTED` or `APPROVED`, before hand-over.
4. Later steps happen on `SF-RET-DETAIL`: hand-over instructions, tracking of the return shipment, answering a seller's contest (accept the proposal or dispute), refund status.

## FL-6 Dispute

1. Entry points appear only when a dispute type is open to the customer: on a delivered shipment ("I did not receive this"), on a shipment past its promised date plus the grace period ("My order has not arrived"), on a rejected or contested return, on an overdue refund.
2. `SF-DISP-NEW`: type (pre-selected by the entry point), description, evidence → submit → `SF-DISP-DETAIL`.
3. `SF-DISP-DETAIL` shows the timeline, the seller's response, deadlines, the decision with its reasons, and, within the review window after a decision, "Request a review" with new evidence (DSP-4). Withdraw is available while `OPENED` or `SELLER_RESPONSE`.

## FL-7 Account deletion

`SF-PRIV` → "Delete my account" → a dialog listing what blocks deletion (open orders, returns, disputes, refunds) or, if nothing blocks it, what will be deleted and forfeited (CUS-12 to CUS-15) → step-up authentication → confirmation → signed out to a confirmation page.

## FL-8 Seller registration and onboarding

`SF-SELL-LANDING` → `SL-AUTH-REGISTER` → `SL-AUTH-VERIFY` (email link) and phone OTP → `SL-AUTH-2FASETUP` (recovery codes shown once, confirmation required) → `SL-ONB-BIZ` → `SL-ONB-DOCS` → `SL-ONB-PAYOUT` → `SL-ONB-REVIEW` (accept the Seller Agreement, submit) → `SL-ONB-STATUS`.

- Each step saves; signing in again resumes at the first incomplete step.
- After submission the steps are read-only. `NEEDS_INFO` reopens only the items the reviewer listed. `REJECTED` shows reasons and "Reapply" while attempts remain (KYC-4).
- On approval, the next sign-in lands on `SL-HOME` with its setup checklist.

## FL-9 Creating an offer on an existing product

`SL-CAT-OFFER-NEW`: search by barcode, brand and model, or title → pick the product → pick the variant(s) → for each: condition, price, stock, handling time, origin address, seller SKU, warranty where required → save as draft or publish. Price-rule failures are shown per field before saving (PRC-1, PRC-6); an anti-dumping hold is explained on the saved offer. "I can't find my product" leads to FL-10 with the search text carried over.

## FL-10 New-product request

`SL-CAT-REQ-NEW` wizard: Information (listing type, category, brand, titles in Arabic and English, description) → Media → Attributes (the category's schema, mandatory ones marked) → Variants (identifiers, package weight and dimensions per variant) → Offer (as FL-9) → Review and submit. A likely duplicate found at any step is shown with "Sell this product instead" (to FL-9). After submission: `SL-CAT-REQ-DETAIL` shows automated-check results and the review outcome; `NEEDS_CHANGES` reopens the wizard with the reviewer's notes.

## FL-11 Bulk import

`SL-CAT-IMPORT`: choose the category template → download → upload the file → map columns (remembered per seller) → dry run → summary (to create, to update, matched to existing products, to review, errors) → confirm → `SL-CAT-IMPORT-JOB` with progress, then the row-level report to download. Nothing changes before "confirm". Leaving the page does not stop the job.

## FL-12 Fulfilling an order

Notification or `SL-HOME` action queue → `SL-ORD-DETAIL` → **Confirm** (or **Reject** with a reason) → pack → **Mark ready to ship** (captures serial numbers where required; creates the waybill; label, packing slip and receipt become printable) → request a pickup or declare drop-off (`SL-SHIP-PICKUP`, or inline) → the courier's scan moves it to Shipped. From `SL-ORD-LIST` the same actions run in bulk for selected orders in the same state.

## FL-13 Queue decision (Admin)

Queue page (`TPL-QUEUE`) → claim an item → decision view: the object's detail, the evidence, the history, and a decision panel with the allowed outcomes → choose an outcome with a reason code → confirm → next item in the queue. Releasing the claim or timing out returns the item. Outcomes under dual control go to FL-14 instead of taking effect.

## FL-14 Dual-control approval (Admin)

Requester completes the action form → sees "Sent for approval" with a link to the request → approver opens `AD-APPROVALS` → request detail (what, who, why, before and after, the object's page) → step-up authentication → approve or reject with a reason → requester is notified; the action takes effect on approval. The urgent account freeze is the one exception: it takes effect at once and lapses after 24 hours unless a second approver confirms it here (SEL-3). The requester cannot open their own request for decision; expired requests are closed and can be resubmitted (DC-1).

## FL-15 Payout run (Admin)

`AD-FIN-RECON` (previous business day signed off, REC-6) and `AD-FIN-FUNDING` (funding sufficient?) → `AD-FIN-PAYOUTS` → "New run" (run states PO-11): cut-off, eligible sellers and amounts, exclusions with reasons (holds, below minimum, unverified destination) → submit for approval (FL-14) → after approval: execute by API or download the bank file → record confirmations (automatic or by upload) → run summary; failures appear in `AD-FIN-FAILED`.
