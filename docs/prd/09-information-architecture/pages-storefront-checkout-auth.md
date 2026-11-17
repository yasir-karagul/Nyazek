# Storefront Pages: Sign-in and Checkout

**Authoritative for:** the content and actions of customer authentication pages, the checkout steps, the payment return page, COD confirmation and guest order lookup.
**Read with:** [README](README.md) §2 · [flows](flows.md) FL-1 to FL-4 · [shared-components](shared-components.md) · [sitemap](sitemap.md) §4 and §6
**Rules live in:** [identity-access](../05-trust/identity-access.md) · [checkout-orders](../02-commerce/checkout-orders.md) · [payments](../04-finance/payments.md) · [fraud-risk](../05-trust/fraud-risk.md) §4 · [logistics](../02-commerce/logistics.md) §3–4

---

## 1. Authentication

All use `TPL-AUTH`. Messages never reveal whether an identifier is registered (AUTH-1).

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-AUTH-LOGIN | `TPL-AUTH` | Two ways on one page: **phone** (default) with "Send code", and **email or phone with password**. Social buttons (Google, Facebook; Apple on iOS) beneath. Links: create account, forgot password, track an order without an account | Send code → `SF-AUTH-OTP`; sign in with password; start social sign-in | Signed-in customers are redirected to `returnTo` or the account home; challenge after repeated failures; temporary-lock message; a seller or staff identifier gets the same generic failure | [identity-access](../05-trust/identity-access.md) §4, AUTH-3, AUTH-7 |
| SF-AUTH-REGISTER | `TPL-AUTH` | Name, phone (required); email and password (optional, with the password policy shown); 18+ confirmation; acceptance line linking Terms and Privacy; marketing opt-in checkboxes, unticked | Create account → `SF-AUTH-OTP` | Same uniform response if the phone is already registered (the OTP then signs in) | [identity-access](../05-trust/identity-access.md) §4, ID-11, PRV-2 |
| SF-AUTH-OTP | `TPL-AUTH` | The masked phone; phone and OTP input; resend countdown; "Change number" | Verify; resend; change number | Attempts and resend limits with clear messages; code expiry; opening this page without a pending verification redirects to login. When the recycled-number rule applies (ID-REC-1), a second step asks for the verified email link, the password or details of a past order; failing that, the page explains that a new account will be created for the number | OTP table in [identity-access](../05-trust/identity-access.md) §4.1, §4.2 |
| SF-AUTH-EMAIL | `TPL-AUTH` | Result of opening an email verification link: verified, expired (with "Send a new link" when signed in) or already used | Continue to the account or `returnTo` | The generic claim-conflict message when the email belongs to another account type, shown only here, after control is proven | AUTH-2, ID-5 |
| SF-AUTH-FORGOT | `TPL-AUTH` | One field: phone or email | Submit → uniform confirmation ("If an account exists, we sent instructions") | Rate limits | AUTH-1 |
| SF-AUTH-RESET | `TPL-AUTH` | New password and confirmation with the policy and breached-password check result | Save → signed in, other sessions revoked, notice sent | Invalid or expired token: explanation and a link to request a new one | Recovery rules |
| SF-AUTH-SOCIAL | `TPL-AUTH` | Progress while the provider's response is processed; then, if needed, the phone verification step | Verify phone; cancel | Provider error or cancel returns to login with a neutral message; an unverified provider email is not linked; conflicts show the generic message | AUTH-2, AUTH-4 |
| SF-AUTH-GUESTTRACK | `TPL-AUTH` | Order number and phone | Send code → OTP → the order's tracking view | Wrong combinations get a uniform "we could not find that order"; rate-limited; a successful lookup opens an order-lookup session limited to that one order (GST-4) | GST-4 |

## 2. Checkout

Checkout pages use the reduced header ([navigation](navigation.md) §1.1) and show the **quote summary** in a side panel (collapsible bar on mobile) at every step. Flow rules: FL-1.

### SF-CHK-ADDR — Step 2: Address

- **Content:**
  - Signed-in customer: saved addresses as selectable address blocks (default pre-selected), each with edit; "Add a new address" opens the address form in a dialog.
  - Guest: "Have an account? Sign in" link; then name, phone with OTP verification in a dialog, the address form, and the 18+ confirmation.
  - Delivery notes (optional).
- **Actions:** select, add or edit an address; verify phone; **Continue**.
- **States and guards:** an address outside every courier's service area is refused with a clear message and a way to pick or enter another (ADR-3); lines that cannot be delivered to the chosen address (hazardous, perishable, per-seller coverage) are listed with "Remove these items and continue" or "Change address"; the address limit message when adding beyond it.
- **Rules:** [checkout-orders](../02-commerce/checkout-orders.md) §1, §3 · GST-1 to GST-3 · SVC-1 to SVC-5

### SF-CHK-SHIP — Step 3: Shipping

- **Content:** one card per shipment (seller): seller block, items, delivery estimate (date range), shipping fee or "Free"; remote-area or bulky surcharges named; a note that shipments arrive separately; the selected address with "Change".
- **Actions:** **Continue**; change address (back to step 2).
- **States and guards:** there is nothing to choose: couriers are assigned by Nyazek and fees are standard (LOG-1, FEE-1). If free delivery applies, each fee shows as waived.
- **Rules:** [logistics](../02-commerce/logistics.md) §4 · FEE-1 to FEE-5

### SF-CHK-PAY — Step 4: Payment and review

- **Content:**
  1. Payment method list (only methods this customer may use for this order).
  2. For cash on delivery: the COD fee if any, "Pay <total> in cash when your order arrives", and, when confirmation will be required, "We will send you an SMS to confirm this order".
  3. Review: address summary, shipments with items, coupon and loyalty fields (P1) if not applied earlier.
  4. Final quote summary.
  5. Legal line: placing the order accepts the Terms and the return policy (links); who the seller of each shipment is.
  6. **Place order** button showing the total.
- **Actions:** choose a method; apply or remove a coupon (P1); place the order.
- **States and guards:** the button is disabled until a method is chosen and while the request is in flight; `QUOTE_CHANGED` opens the confirm-new-total dialog; a payment method that became unavailable is removed with a notice; when no prepaid method is available and COD is not offered, the page says the order cannot be completed now and keeps the cart.
- **Rules:** [checkout-orders](../02-commerce/checkout-orders.md) §4–5 · QTE-1, QTE-2 · [payments](../04-finance/payments.md) §1 · CODC-1 · PRM-1 to PRM-5

**Place-order outcomes**

| Outcome | Where the customer goes | What they see |
|---|---|---|
| COD, no confirmation needed | `SF-CHK-DONE` (COD variant) | "The seller is preparing your order" |
| COD, confirmation needed | `SF-CHK-DONE` (confirm variant) | "Confirm your order by SMS" with the deadline (FL-3) |
| COD, held for review (`ON_HOLD`) | `SF-CHK-DONE` (COD variant) | Neutral "We are checking your order and will update you"; risk is never mentioned |
| Prepaid | Provider page or app, then `SF-CHK-RETURN` (FL-2) | Payment deadline countdown; cart lines removed (CRT-7) |
| Quote changed | Stays on `SF-CHK-PAY` | Confirm-new-total dialog (QTE-2) |
| Stock no longer available | `SF-CART` | Affected lines flagged (CHK-4) |
| Payment method no longer available | Stays on `SF-CHK-PAY` | Method removed with a notice |
| Order refused by risk rules | Stays on `SF-CHK-PAY` | Generic "We cannot complete this order. Try another payment method or contact support" |
| Duplicate submission | `SF-CHK-DONE` of the original order (ORD-8) | The original order |

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-CHK-RETURN | `TPL-SYSTEM`, with live content as described | Order number; live payment status with a progress indicator; the amount | Paid: continue to confirmation (automatic). Failed: try again (method list) or cancel the order. Pending too long: go to the order | Per FL-2; the page reads the status from the API and ignores anything in the redirect; reachable again from the order page while the order awaits payment | PAY-6 to PAY-10, PAY-18 |
| SF-CHK-DONE | Dedicated layout | "Thank you" with the order number; what happens next (COD: confirm by SMS if required, then the seller prepares; prepaid: the seller prepares); shipments with estimates; total and payment method; for unclaimed accounts, "Set a password to manage your orders" | Track the order; continue shopping; set a password | Only the order's owner can open it; a guest is signed in to the unclaimed account created at checkout (GST-2, GST-3), so this is the same check; revisiting later redirects to the order page | GST-3, CODC-1 |
| SF-CHK-CODCONF | `TPL-AUTH`, with the order summary as described | Per FL-3: order number, items count, total to pay in cash, delivery area, deadline | Confirm order; cancel order | Token valid once; expired or used token shows the order's current state; no sign-in; no personal data beyond what is listed | CODC-1 to CODC-3 |
