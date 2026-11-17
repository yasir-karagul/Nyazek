# Shared Components

**Authoritative for:** the catalogue of content components reused across pages: what each shows, its variants and the rules behind it.
**Not here:** visual design, tokens and interaction states (default, hover, focus, disabled, loading, error), which are in [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §4.
**Related:** [ia-model](ia-model.md) §5 · the `pages-*` documents, which refer to these components by name

A page specification that names a component gets everything in its row. Components are built once in the shared library and are not re-implemented per page.

---

## 1. Commerce components (Storefront)

| Component | Shows | Variants and behaviour | Rules |
|---|---|---|---|
| Product card | Main image · title (two lines) · price block · rating stars with count · seller name or 1P badge · delivery estimate for the "Deliver to" governorate · discount badge when a reference price qualifies · favourite toggle | Grid, list and compact (carousel); deal variant (deal price, remaining-stock bar, sold-out marker); "Sponsored" label variant (P1); out-of-stock variant (dimmed, "Out of stock", no add-to-cart). The whole card links to the product page | SRC-1, PRC-9, AD-6 |
| Price block | Current price with currency · crossed-out reference price and percentage only when the API marks it eligible | Large (product page), medium (card), small (line items). Never shows a price computed on the client | PRC-9, MON-7, IA-6 |
| Rating summary | Average, count, distribution bars by star | Compact (stars and count). Hidden for sellers below the minimum rating count ("New seller") | REV-4 |
| Seller block | Seller name linking to the store · seller rating · verified badge · 1P badge · "The seller shown is selected automatically" disclosure | Product page (Buy Box), offers list row, order shipment header | [search-buy-box](../02-commerce/search-buy-box.md) §2.5 |
| Offers list ("Other sellers") | One row per offer: seller block, condition, price, delivery estimate, add-to-cart | Grouped by condition; sorted by price then seller rating; the Buy Box offer is marked | BBX-2, BBX-7 |
| Variant selector | One control per variant attribute (swatches for colour, buttons for size, dropdown beyond 8 values) | Unavailable combinations are shown disabled, not hidden; selecting a variant updates price, stock, images and URL | – |
| Media gallery | Images with thumbnails, zoom, swipe; video where present | Uses named image variants (`thumb`, `card`, `detail`, `zoom`); first image is the main image | [catalog-listings](../02-commerce/catalog-listings.md) §8 |
| Delivery estimate | "Delivery to <governorate> by <date range>" or "Not deliverable to <governorate>" with a change link | Inline (card), block (product page), per shipment (checkout) | SVC-3 |
| Stock badge | In stock · "Only N left" when the API marks the stock as low · Out of stock | – | Availability from the API only |
| Quantity stepper | Minus, value, plus | Limits from the API (stock, per-line and per-item caps) with the reason shown at the limit | CRT-4 |
| Cart line | Image, title, variant, seller, unit price, quantity stepper, line total, remove, move to favourites | Flags: price changed (old and new), low stock, unavailable, offer replaced (accept or remove) | CRT-2, CRT-3 |
| Quote summary | Items subtotal · seller discounts · platform discount · loyalty redemption (P1) · shipping per shipment · surcharges · COD fee · tax line when non-zero · total payable | Cart (estimate, shipping shown after a governorate is known), checkout (final), order (as charged) | [checkout-orders](../02-commerce/checkout-orders.md) §4 |
| Free-delivery progress | "Add <amount> more for free delivery" or "You have free delivery" | Hidden when no threshold is configured | FEE-2 |
| Coupon field (P1) | Code input, apply, applied coupon with remove, error reason | One seller coupon per shipment, one platform coupon per order | PRM-1 to PRM-5 |
| Payment method list | One option per method the customer is eligible for: name, logo, one-line note | Methods not offered are absent, not disabled; unavailable (circuit open) methods are absent | PAY-12, COD eligibility |
| Report listing dialog | Reason (counterfeit, prohibited, wrong information, intellectual property, other), details, optional contact | Available to guests; rate-limited | PRH-1, PRH-2 |
| Review card | Stars, title or first line, text, photos, reviewer display name, date, "returned item" marker | Product and store variants | REV-3, REV-8 |
| Review form | Product stars (required), text and photos (optional), seller stars (required), seller comment (optional) | One per product per order within the window; one edit | REV-1, REV-2 |

## 2. Order and after-sales components (all applications)

| Component | Shows | Variants and behaviour | Rules |
|---|---|---|---|
| Order card | Order number, date, derived status, total, payment method, thumbnails of items, shipment count | Customer list; admin list (adds customer reference, masked) | §3.2 of taxonomy-and-labels |
| Shipment block | "Shipment N of M", seller block, status chip, next step and date, items with quantities and line status, tracking link, allowed actions | Customer, seller and admin variants differ in data and actions, not in structure | Sub-order machine |
| Status chip | Label from [taxonomy-and-labels](taxonomy-and-labels.md); staff variant adds the exact state | Fixed colour role per meaning plus text or icon | – |
| Timeline | Dated entries, newest first or milestone order; actor shown to staff | Tracking (milestones), history (audit view for staff), case (returns, disputes, tickets) | ADM-8 |
| Countdown | Time remaining to a deadline, turning to warning at 50% and urgent at 90% of the window | Seller SLA, seller return response, return auto-advance, dispute response, dispute review window, admin queue target, COD confirmation, payment deadline, flash-deal end, review window ("days left"), pickup hand-over deadline | SLA-3, SLA-6, ORD-16, RET-3, DSP-4, REV-1 |
| Address block | Recipient, phones, governorate › district › neighbourhood, landmark, details, notes | Customer: full. Seller: full on the order detail while fulfilling, phone masked in lists. Admin: masked with reveal | SHP-6, SDB-7, RBAC-4 |
| Address form | Fields per the market's address model with dependent pickers; landmark required in Iraq; optional map pin (P1) | Checks serviceability on save and shows the result | ADR-1 to ADR-5 |
| Phone and OTP input | Phone field with country code fixed to the market, Arabic-Indic digits accepted; six-box OTP with resend countdown, attempts left, paste and SMS autofill | Purposes: sign-in, registration, guest checkout, refund account, sensitive change, guest order lookup (GST-4), staff caller verification (ADM-6), two-factor fallback by SMS, seller registration | [identity-access](../05-trust/identity-access.md) §4.1 |
| Evidence uploader | Photos and short video with previews, per-file progress, type and size limits, remove | Returns, disputes, tickets, KYC (documents variant accepts PDF); product media (order, main image) and store or banner images | Media pipeline, [catalog-listings](../02-commerce/catalog-listings.md) §8 |
| File import | Template download, file picker, upload progress, validation report per row, confirm | Catalogue import, courier statements, reconciliation files, geo data, serviceability | Rows that fail are reported and not applied |
| Message thread | Messages with sender and time, attachments, compose box | Customer–seller (contact details blocked, notifications-messaging §6); ticket; staff variant adds internal notes | [notifications-messaging](../02-commerce/notifications-messaging.md) §6, [support-cms](../02-commerce/support-cms.md) |
| Attention list | Items that need the user's action, each with a reason and a link | Account home, seller home, order detail banner; seller state banner; setup checklist (`SL-HOME`) | – |
| Document viewer | A document or image beside its data, with zoom and page navigation | KYC case and dispute evidence | – |
| Refund summary | Amount, components (items, shipping, deductions), destination, status and expected date | Return, dispute and order pages | REF-3, REF-6 |
| Document download | Receipt, credit note, statement, invoice as PDF (and CSV where stated) | Shows document number and date | [tax-invoicing](../04-finance/tax-invoicing.md) §5 |

## 3. General components (all applications)

| Component | Shows | Behaviour |
|---|---|---|
| Data table | Sortable columns, row selection, column set per breakpoint | Cards on mobile (IA model §7); sticky header; keyboard navigable. Editable-grid variant: inline cell editing with per-cell validation and "save all" |
| Filter bar | Tabs, search field, filter controls, applied-filter chips, clear all | Writes to the query string (IA-12) |
| Bulk-action bar | Count selected, available bulk actions | Summary and confirmation before running; results per item (ADM-3, SDB-5) |
| Pagination | Numbered pages on Storefront listings; "load more" or next and previous with cursor elsewhere | Keeps scroll position on back navigation |
| Key figure card | Label, value, period, change against the previous period, link | Value and change come from the API |
| Period selector | Preset periods and a custom range | Writes to the query string (IA-12) |
| Chart | Line or bar chart for a period with a legend | Always paired with an accessible table of the same data |
| Sticky action bar | The page's primary action and its key figure, fixed to the bottom on small screens | Product page (price, add to cart) and cart (total, checkout) |
| Two-factor enrolment | QR code, setup key, code confirmation, recovery codes shown once | All realms; 2FA rules in [identity-access](../05-trust/identity-access.md) |
| New-password field | Password with the policy shown and the breached-password check result | Registration, reset, change, invitation; password rules in [identity-access](../05-trust/identity-access.md) |
| Empty state | Icon, one sentence, optional action | Text is specific to the page and tab |
| Inline error | Message, retry, correlation ID | Never replaces the whole page unless the page's main object failed to load |
| Confirm dialog | Restates object and consequence; primary action named after the action ("Cancel shipment"), not "OK" | Required for destructive and money-moving actions (IA-14) |
| Reason select | Reason codes from the managed list for the action, with a note field when "other" | ADM-2; also used for customer cancellation and return reasons |
| Masked value | Masked text with a reveal control that asks for a reason (staff) | Reveal is logged (RBAC-4) |
| Money | Formatted amount with currency per the currency table and language | MON-7, MON-8 |
| Date and time | Absolute date in the market's time zone; relative ("2 hours ago") for recent events with the absolute value on focus | – |
| Step indicator | Steps with current, done and upcoming | Checkout, wizards |
| Toast | Short confirmation or error | Never the only place an error is shown for a form |
| Step-up prompt | Password or 2FA again before a sensitive action | SES-5, SDB-3 |
| Consent banner | Accept, reject, choose; link to the cookie policy | [privacy-audit](../05-trust/privacy-audit.md) §2 |
| Language switch | Arabic and English | Storefront: changes the URL prefix and keeps the page; dashboards: changes the account setting |
| Notification item | Icon by class, title, one line, time, unread marker, link to the object | Opening marks it read |
| Rich text view | Sanitised seller or CMS content | Restricted rendering (SEC-6) |
