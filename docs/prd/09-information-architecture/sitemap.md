# Sitemap (Page Inventory) v3.0

**Authoritative for:** the inventory of pages, shell components and technical routes of the three web apps, their stable **Page IDs**, routes, access and priorities.
**Not authoritative for behaviour:** rules live in the domain documents; where this file and a domain document differ, the domain document wins and this file is corrected ([document-control](../00-governance/document-control.md) §3.1).
**Supersedes:** Nyazek Sitemap v2.0 (October 2026), which was aligned to PRD v6. Version 3.0 applies the alignment changes listed in document-control and the v7.1 review.
**Page content:** what each page contains and does is specified in the `pages-*` documents of this section ([README](README.md)); navigation is in [navigation](navigation.md).
**Related:** [web-apps](../07-clients/web-apps.md) · [seller-dashboard](../03-sellers/seller-dashboard.md) · [admin-panel](../05-trust/admin-panel.md) · [user-journeys](../01-product/user-journeys.md) · [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §7

Market: Iraq (launch market) · IQD · Arabic (default, RTL) and English.

---

## 0. Changes from v2.0

| Area | Change |
|---|---|
| Location | Part of the PRD's information-architecture section; versioned with it |
| Terminology | "Customer" replaces "buyer" in tags, IDs and routes (`[CUSTOMER]`, `AD-USR-CUSTOMERS`, `/legal/customer-protection`) |
| Topology | Same-origin `/api` path on each web host; admin API not on the public API host; Admin Panel behind zero-trust access |
| Identity | Email verification is required to use an email, not to order; Sign in with Apple added with the iOS app |
| Orders | "Confirm delivery" is evidence only unless D-22 enables early release; held sub-orders are not shown to sellers (the v3.0 "On hold" badge was withdrawn in v7.3) |
| Returns | Refund is the default outcome; "replace instead" is P1 (D-25) |
| Seller wallet | "On hold" balance added |
| Priorities | `SL-AN-TRAFFIC` to P1; `AD-SET-APP` to P0; price-drop notification P1; delivery-speed filter P1 |
| Added pages | `AD-1P-ORDERS`, `AD-1P-RETURNS`, `AD-FIN-FUNDING`, `AD-FIN-DOCS`, `AD-SET-GEO`, `AD-SET-CALENDAR`, `SF-ST-LOYALTY` |
| Removed duplicate | `SF-SELL-FAQ` (same route as `SF-ST-FAQ-SELLER`) |
| Mobile | Native apps are Flutter: `mobile_customer` and `mobile_seller` |

## 1. Topology and conventions

| App | Host | Audience | Authentication | Specified in |
|---|---|---|---|---|
| Storefront | `www.<domain>` | Guests and customers | Optional (guest checkout) | [web-apps](../07-clients/web-apps.md) §4 |
| Seller Dashboard | `seller.<domain>` | Sellers and store staff | Required; 2FA mandatory | [seller-dashboard](../03-sellers/seller-dashboard.md) |
| Admin Panel | `admin.<domain>` | Nyazek staff (11 roles) | Required; 2FA mandatory; zero-trust access | [admin-panel](../05-trust/admin-panel.md) |
| API | `<app-host>/api/v1` for each web app; `api.<domain>/v1` for mobile apps and webhooks (no admin endpoints) | All clients | Session cookie (web) or bearer token (mobile) | [api-standards](../06-platform/api-standards.md) §1 |

**Conventions**

- Routes are relative to the host of their section. Storefront: Arabic at the root, English under `/en`. The dashboards store the language as an account setting.
- **Page ID** = `<APP>-<AREA>-<NAME>` (`SF` Storefront, `SL` Seller, `AD` Admin, `SYS` system). Priority: **P0** launch gate · **P1** launch target (30-day fast-follow allowed) · **P2** post-launch ([scope-priorities](../01-product/scope-priorities.md) §1).
- Tags: `[PUB]` guest · `[CUSTOMER]` signed-in customer · `[SELLER]` seller owner or staff · `[ADMIN]` staff with the stated role · `[FILTER]` tab or filter inside a page, not a route · `[MODAL]` modal or drawer · `[ACTION]` action on a page.
- The Role column of the Admin Panel tables names the main users of the page, for orientation only. Access is decided by the matrix in [admin-governance](../05-trust/admin-governance.md) §2.1 (manage, read, approve), which wins wherever the column differs.
- Rows whose ID is "—" are modals, filters or actions of the page above them; they have no ID and are not counted.
- Every page defines loading, empty, error and permission-denied states in both languages and directions ([web-apps](../07-clients/web-apps.md) §8).

---

## 2. Storefront: shell and global components

| ID | Component | Notes | Pri |
|---|---|---|---|
| SF-SH-HEADER | Header | Logo, search, language toggle, cart, favourites, account menu | P0 |
| SF-SH-MEGAMENU | Mega menu | Category tree dropdown or drawer | P0 |
| SF-SH-FOOTER | Footer | Information links, social, payment logos, legal entity name, commercial registration and e-commerce licence number (CMS-1) | P0 |
| SF-SH-CONSENT | Cookie and consent banner | Gates marketing tags; records consent version | P0 |
| SF-SH-CART | Cart drawer `[MODAL]` | Quick view; stock and price change notices | P0 |
| SF-SH-SEARCH | Search overlay `[MODAL]` | Suggestions: products, categories, brands | P0 |
| SF-SH-TOAST | Toast stack | Global feedback | P0 |
| SF-SH-ANNOUNCE | Announcement bar | CMS-driven | P1 |
| SF-SH-PWA | Install prompt | Mobile browsers | P2 |

## 3. Storefront: discovery and browse `[PUB]`

### 3.1 Home `/` — SF-HOME (P0)

| Section | Description | Pri |
|---|---|---|
| Hero banner carousel | CMS-driven | P0 |
| Category grid | Top-level categories | P0 |
| Product rows `[FILTER]` | New Arrivals · Best Sellers · Top Rated · Deals & Offers | P0 |
| Flash deals strip; featured brands; sponsored row (labelled) | | P1 |
| Recently viewed | | P2 |

### 3.2 Search results `/search?q=` — SF-SEARCH (P0)

| Element | Values and behaviour | Pri |
|---|---|---|
| Query | Editable; Arabic normalisation and synonyms applied | P0 |
| Filters | Category · price range (IQD) · brand · seller type (1P / 3P) · rating · in stock · condition (New, Open box, Refurbished; Used is not enabled at launch, D-44) · deliverable to governorate (19) · category attributes | P0 |
| Filter: delivery speed | Next day / standard, by selected governorate | P1 |
| Sort | Relevance (default) · price low to high · price high to low · newest · best selling · rating | P0 |
| View toggle; numbered pagination with canonical URLs | | P0 |
| No-results state | Suggestions; "did you mean" at P1 | P0 |

### 3.3 Category `/category/*path` — SF-CATEGORY (P0)

Same filter bar as search, plus category banner (CMS), sub-category pills, dynamic attribute filters, brand showcase (P1). Unlimited depth.

### 3.4 Product detail `/product/:slug` — SF-PDP (P0)

Serves canonical and seller-owned listings. `?offer=:offerId` pre-selects an offer.

| Section | Description | Pri |
|---|---|---|
| Breadcrumb, gallery (images, video, zoom), title, rating | | P0 |
| Price block | Strike-through only when the reference-price rule is met (PRC-9) | P0 |
| Variant selector | Swatches or dropdowns | P0 |
| Buy Box seller block | 1P badge or seller name and rating; disclosure that the default seller is selected automatically | P0 |
| Delivery estimate | By selected governorate | P0 |
| Stock badge, add to cart, buy now, add to favourites | | P0 |
| Tabs | Description · Specifications · Reviews · Shipping & Returns | P0 |
| Tab: Q&A | | P1 |
| Other sellers | All competing offers, grouped by condition | P0 |
| Report listing `[MODAL]` | Counterfeit, prohibited, wrong information, intellectual property | P0 |
| Notify me when back in stock `[ACTION]`; share `[ACTION]` | CUS-10; canonical link | P1 |
| Similar products; sponsored alternatives | | P1 |
| Frequently bought together; recently viewed | | P2 |

### 3.5 Brand `/brand/:slug` — SF-BRAND (P1)

Logo and banner, description, product grid with search filters, authorised-distributor badge.

### 3.6 Store `/store/:seller-slug` — SF-STORE (P0)

| Section | Pri |
|---|---|
| Header: logo, banner, name, rating (after the minimum count), since date, verified badge, legal identity | P0 |
| Tabs: All products · Reviews · About (bio, policies) | P0 |
| Tabs: Featured · New arrivals · On sale; search within store; report store `[MODAL]` | P1 |

### 3.7 Deals and campaigns

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-DEAL-FLASH | Flash deals | `/deals/flash` | P1 | Countdown per product |
| SF-CAMPAIGN | Campaign landing | `/campaign/:slug` | P1 | CMS: Ramadan, Eid Al-Fitr, Eid Al-Adha, Back to School, New Year, custom |
| SF-DEAL-DAILY | Daily deals | `/deals/daily` | P2 | |
| SF-DEAL-CLEAR | Clearance | `/deals/clearance` | P2 | |

### 3.8 Favourites `/favorites` — SF-FAV (P0)

Guest favourites on the device, merged at sign-in ([customer-account](../02-commerce/customer-account.md) §2). `/wishlist` and `/account/favorites` redirect here. Tabs `[FILTER]`: All · In stock · Price dropped. Move to cart (bulk). Price-drop notification is P1.

### 3.9 Cart `/cart` — SF-CART (P0)

Lines, quantity limits, remove, coupon and loyalty-points fields (P1), price and stock revalidation notices, shipping estimate and free-delivery progress.

## 4. Storefront: customer authentication `[PUB]`

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-AUTH-LOGIN | Login | `/login` | P0 | Phone OTP, or email or phone with password; customer realm only |
| SF-AUTH-REGISTER | Register | `/register` | P0 | Phone OTP (email and password optional); 18+ confirmation |
| SF-AUTH-OTP | Phone OTP verification | `/verify-otp` | P0 | 6 digits, 5 minutes, cool-down, attempt limits |
| SF-AUTH-EMAIL | Email verification | `/verify-email` | P0 | Required before an email is used for login, receipts or recovery; not required to order (D-23) |
| SF-AUTH-FORGOT | Forgot password | `/forgot-password` | P0 | Uniform response whether or not the account exists |
| SF-AUTH-RESET | Reset password | `/reset-password?token=` | P0 | |
| SF-AUTH-SOCIAL | Social login callback | `/auth/callback/:provider` | P0 | Google, Facebook; Apple with the iOS app; customers only |
| SF-AUTH-GUESTTRACK | Guest order lookup | `/track-order` | P0 | Order number + phone OTP |

State, not a route: the generic "this email can't be used to create this type of account" message, shown only after control of the identifier is proven (AUTH-2).

## 5. Storefront: customer account `[CUSTOMER]`

All under `/account/*`.

### 5.1 Account home `/account` — SF-ACC-HOME (P0)

Recent orders with next action, open returns and disputes, favourites; loyalty balance and coupons at P1.

### 5.2 Orders

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-ORD-LIST | My orders | `/account/orders` | P0 | Orders grouped with sub-orders; filters `[FILTER]`: All · Pending · Processing · Shipped · Delivered · Cancelled · Returned |
| SF-ORD-DETAIL | Order detail | `/account/orders/:orderId` | P0 | Sub-orders per seller, totals, payment, address snapshot |
| SF-ORD-TRACK | Tracking | `/account/orders/:orderId/tracking/:subOrderId` | P0 | Internal timeline plus courier number and link |
| — | Cancel sub-order `[MODAL]` | | P0 | Before `SHIPPED`; reason required |
| — | Receipt and credit-note download `[ACTION]` | | P0 | PDF |
| — | Confirm receipt `[ACTION]` | | P0 | Recorded as evidence; no early release unless D-22 enables it |
| — | Buy again `[ACTION]` | | P1 | |

### 5.3 Returns, refunds and disputes

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-RET-LIST | Returns | `/account/returns` | P0 | |
| SF-RET-NEW | Request a return | `/account/returns/new?subOrder=` | P0 | Lines and quantities, reason, evidence, refund destination for COD; "replace instead" at P1 |
| SF-RET-DETAIL | Return detail | `/account/returns/:returnId` | P0 | Pickup, inspection, refund status and expected timing |
| SF-DISP-LIST | Disputes | `/account/disputes` | P0 | |
| SF-DISP-NEW | Open a dispute | `/account/orders/:orderId/dispute/new` | P0 | Within the window for its type; evidence upload |
| SF-DISP-DETAIL | Dispute detail | `/account/disputes/:disputeId` | P0 | Timeline, decision, review request |

### 5.4 Reviews and Q&A

| ID | Page | Route | Pri |
|---|---|---|---|
| SF-REV-PENDING | Pending reviews | `/account/reviews/pending` | P0 |
| SF-REV-DONE | My reviews | `/account/reviews/submitted` | P0 |
| — | Write review `[MODAL]` (product review and seller rating) | | P0 |
| SF-QA-MY | My questions | `/account/qa` | P1 |

### 5.5 Addresses `/account/addresses` — SF-ADDR (P0)

Add or edit `[MODAL]`: governorate → district → neighbourhood → nearest landmark (required) → street and house details → recipient name → phone(s) → delivery notes; map pin at P1. Default address. Limit per ADR-2.

### 5.6 Refund accounts and payment methods

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-REFACC | Refund accounts | `/account/refund-accounts` | P0 | Mobile-wallet or bank account for COD refunds; OTP-verified (D-02) |
| SF-PAYM | Saved cards | `/account/payment-methods` | P1 | PSP tokens only |

### 5.7 Loyalty, coupons, notifications, messages

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-LOY | Loyalty and rewards | `/account/loyalty` | P1 | Tier, points, history, referral |
| SF-COUP | Coupons | `/account/coupons` | P1 | |
| SF-NOTIF | Notifications | `/account/notifications` | P0 | Tabs `[FILTER]`: All · Orders · Promotions · System; preferences `[MODAL]` |
| SF-MSG | Messages | `/account/messages` | P1 | Per-order seller threads; a thread opens on the sub-route `/account/messages/:threadId` ("Contact seller" from an order) |

### 5.8 Profile, security and privacy

| ID | Page | Route | Pri |
|---|---|---|---|
| SF-PROF | Personal information | `/account/profile` | P0 |
| SF-SEC-PW | Password | `/account/security/password` | P0 |
| SF-SEC-EMAIL | Email and phone | `/account/security/email` | P0 |
| SF-SEC-DEV | Devices and sessions | `/account/security/devices` | P0 |
| SF-SEC-2FA | Two-factor authentication (optional) | `/account/security/2fa` | P1 |
| SF-SEC-LINK | Linked social accounts | `/account/security/linked` | P0 |
| SF-PRIV | Privacy, consent, data export, delete account `[MODAL]` | `/account/privacy` | P0 |

## 6. Storefront: checkout

| Step | ID | Route | Pri | Notes |
|---|---|---|---|---|
| 2 Address | SF-CHK-ADDR | `/checkout/address` | P0 | Select or add; guests verify a phone by OTP `[MODAL]`; checkout session created |
| 3 Shipping | SF-CHK-SHIP | `/checkout/shipping` | P0 | Per-seller parcels, estimates, standard fees; no option to choose |
| 4 Payment and review | SF-CHK-PAY | `/checkout/payment` | P0 | Methods the customer is eligible for (COD, launch wallets; cards P1; others per D-11); final quote; place order |
| Payment return | SF-CHK-RETURN | `/checkout/payment/return/:paymentId` | P0 | Shows live status and polls; never trusts the redirect |
| 5 Confirmation | SF-CHK-DONE | `/checkout/confirmation/:orderId` | P0 | Order number, sub-orders, next steps |
| COD confirmation | SF-CHK-CODCONF | `/confirm-order/:token` | P0 | SMS-link landing to confirm or cancel a COD order |

Step 1 is the cart (`SF-CART`, §3.9).

---

## 7. Seller Dashboard — `seller.<domain>`

Routes relative to the seller host. Staff roles are P1; at launch only the owner signs in.

### 7.1 Public seller pages (on the Storefront host)

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SF-SELL-LANDING | Become a seller | `/sell` | P0 | States the separate-email rule |
| SF-SELL-FEES | Fees and commission schedule | `/sell/fees` | P0 | Published schedule (COM-3) |

Seller FAQ is `SF-ST-FAQ-SELLER` (§9).

### 7.2 Authentication and onboarding

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-AUTH-LOGIN | Login | `/login` | P0 | Email + password, then 2FA; no social login |
| SL-AUTH-2FA | 2FA challenge | `/login/2fa` | P0 | TOTP; SMS fallback; recovery codes |
| SL-AUTH-2FASETUP | 2FA setup | `/security/2fa/setup` | P0 | Mandatory at first login |
| SL-AUTH-REGISTER | Create seller account | `/register` | P0 | Email, password, phone; both verified |
| SL-AUTH-VERIFY | Email verification | `/verify-email` | P0 | |
| SL-AUTH-FORGOT | Forgot password | `/forgot-password` | P0 | |
| SL-AUTH-RESET | Reset password | `/reset-password?token=` | P0 | |
| SL-AUTH-INVITE | Accept staff invitation | `/accept-invite/:token` | P1 | |
| SL-ONB-BIZ | Step 1: Business information | `/onboarding/business` | P0 | Seller type |
| SL-ONB-DOCS | Step 2: Documents | `/onboarding/documents` | P0 | Per KYC table; regulated-category licences |
| SL-ONB-PAYOUT | Step 3: Payout destination | `/onboarding/payout` | P0 | Must match the KYC identity |
| SL-ONB-REVIEW | Step 4: Review and submit | `/onboarding/review` | P0 | Seller Agreement acceptance |
| SL-ONB-STATUS | Application status | `/onboarding/status` | P0 | Progress, information requests, decision, reapply |

### 7.3 Home `/` — SL-HOME (P0)

KPI cards, action queue (orders awaiting confirmation with countdown, returns, disputes due, restock tasks, low stock, expiring documents, warnings), setup checklist, announcements.

### 7.4 Orders

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-ORD-LIST | Orders | `/orders` | P0 | Tabs `[FILTER]`: Awaiting confirmation · Processing · Ready to ship · Shipped · Delivered · Cancelled · Returned; SLA timers; bulk confirm, label and ready `[ACTION]` |
| SL-ORD-DETAIL | Order detail | `/orders/:subOrderId` | P0 | Items, customer phone in full only while fulfilling (SDB-7), timeline; confirm or reject `[MODAL]`; mark ready; print label, packing slip and receipt. Courier is assigned automatically (LOG-1) |
| SL-SHIP-PICKUP | Pickups | `/shipping/pickups` | P0 | Request a pickup slot or declare drop-off |

Sub-orders that are `ON_HOLD` (COD confirmation, risk review) are not visible to the seller until released.

### 7.5 Catalog

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-CAT-OFFERS | Offers | `/catalog/offers` | P0 | Filters `[FILTER]`: Active · Draft · Paused · Suspended · Out of stock; search; bulk actions; export `[ACTION]` |
| SL-CAT-OFFER-NEW | Create offer on an existing product | `/catalog/offers/new` | P0 | Find by barcode, brand and model, or title |
| SL-CAT-OFFER-EDIT | Edit offer | `/catalog/offers/:offerId/edit` | P0 | |
| SL-CAT-REQ | New-product requests | `/catalog/requests` | P0 | Status and reasons |
| SL-CAT-REQ-NEW | Submit a new product or seller-owned listing | `/catalog/requests/new` | P0 | Steps per FL-10; duplicate warning |
| SL-CAT-REQ-DETAIL | Request detail | `/catalog/requests/:requestId` | P0 | Suggest an edit `[MODAL]` is P1 |
| SL-CAT-IMPORT | Bulk import | `/catalog/import` | P0 | Template, mapping, dry run |
| SL-CAT-IMPORT-JOB | Import result | `/catalog/import/:jobId` | P0 | Row-level report |
| SL-CAT-STOCK | Price and stock quick-edit | `/catalog/inventory` | P0 | |
| SL-CAT-ALERTS | Low-stock alerts | `/catalog/inventory/alerts` | P0 | |
| SL-CAT-VIOL | Violations centre | `/catalog/violations` | P0 | Price floor, MAP, anti-dumping |

### 7.6 Returns and disputes

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-RET-LIST | Return requests | `/returns` | P0 | Response countdown |
| SL-RET-DETAIL | Return detail | `/returns/:returnId` | P0 | Approve or reject `[MODAL]`; inspection result; partial-refund proposal; restock task |
| SL-DISP-LIST | Disputes | `/disputes` | P0 | |
| SL-DISP-DETAIL | Dispute detail | `/disputes/:disputeId` | P0 | Evidence, response, decision history |

### 7.7 Wallet and payouts

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-WAL-HOME | Wallet | `/wallet` | P0 | Pending · Awaiting courier remittance · Available · On hold; next payout date |
| SL-WAL-TX | Transactions | `/wallet/transactions` | P0 | Filters by movement type |
| SL-WAL-PAYOUTS | Payouts | `/wallet/payouts` | P0 | History |
| SL-WAL-PAYOUT | Payout statement | `/wallet/payouts/:payoutId` | P0 | PDF and CSV |
| SL-WAL-INV | Commission invoices | `/wallet/invoices` | P0 | Per settlement period |
| SL-WAL-METHODS | Payout destinations | `/wallet/payout-methods` | P0 | Re-verification; 72-hour hold on the first payout |

### 7.8 Promotions and advertising

| ID | Page | Route | Pri |
|---|---|---|---|
| SL-PRO-LIST | My promotions | `/promotions` | P1 |
| SL-PRO-COUPON | Create coupon | `/promotions/coupons/new` | P1 |
| SL-PRO-DEAL | Create deal | `/promotions/deals/new` | P1 |
| SL-PRO-CAMP | Join a campaign | `/promotions/campaigns` | P1 |
| SL-ADS-LIST | Ad campaigns | `/ads` | P1 |
| SL-ADS-NEW | Create campaign | `/ads/new` | P1 |
| SL-ADS-DETAIL | Campaign detail | `/ads/:campaignId` | P1 |
| SL-ADS-BILL | Budget and billing | `/ads/billing` | P1 |

### 7.9 Messages, Q&A, reviews

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-MSG | Messages | `/messages` | P1 | Per-order customer threads |
| SL-QA | Product Q&A | `/qa` | P1 | |
| SL-REV | Reviews | `/reviews` | P0 | Read; flag for moderation `[MODAL]` |

### 7.10 Performance and analytics

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-PERF | Performance | `/performance` | P0 | Score, metrics, contributing orders, level, recovery |
| SL-APPEAL | Appeals | `/performance/appeals` | P1 | Through Support until then |
| SL-AN-HOME | Analytics overview | `/analytics` | P0 | Ranges `[FILTER]`: 7 days · 30 days · custom |
| SL-AN-SALES | Sales | `/analytics/sales` | P0 | By product, category, governorate; export |
| SL-AN-REV | Reviews | `/analytics/reviews` | P0 | |
| SL-AN-TRAFFIC | Traffic and funnel | `/analytics/traffic` | P1 | Needs clickstream |
| SL-AN-BUYBOX | Buy Box insights | `/analytics/buy-box` | P1 | |

### 7.11 Store settings

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-SET-STORE | Store profile | `/settings/store` | P0 | Logo, banner, name, about |
| SL-SET-PICKUP | Pickup and return addresses | `/settings/pickup-addresses` | P0 | |
| SL-SET-POLICY | Handling time and return policy | `/settings/policies` | P0 | Within platform rules |
| SL-SET-NOTIF | Notification preferences | `/settings/notifications` | P0 | |
| SL-SET-VACATION | Vacation mode | `/settings/vacation` | P1 | |

### 7.12 Team, account and help

| ID | Page | Route | Pri | Notes |
|---|---|---|---|---|
| SL-TEAM | Team | `/team` | P1 | Invite `[MODAL]`, preset roles |
| SL-TEAM-LOG | Activity log | `/team/activity` | P0 | Owner sees all changes (SDB-2) |
| SL-ACC-PROFILE | Account profile | `/account` | P0 | |
| SL-ACC-SEC | Security | `/account/security` | P0 | Password, 2FA, devices, login history |
| SL-ACC-KYC | KYC documents and renewals | `/account/kyc` | P0 | Expiry warnings |
| SL-ACC-REF | Referral link | `/account/referral` | P1 | |
| SL-ACC-CLOSE | Close account | `/account/close` | P1 | |
| SL-NOTIF | Notification centre | `/notifications` | P0 | |
| SL-HELP | Help centre | `/help` | P1 | |
| SL-TICKET-LIST | Support tickets | `/help/tickets` | P1 | |
| SL-TICKET-NEW | New ticket | `/help/tickets/new` | P1 | |
| SL-TICKET | Ticket detail | `/help/tickets/:ticketId` | P1 | |
| SL-SUSPENDED | Restricted or suspended state | `/restricted` | P0 | Read-only, reason, appeal route |

---

## 8. Admin Panel — `admin.<domain>`

Routes relative to the admin host. Access by role ([admin-governance](../05-trust/admin-governance.md) §2).

### 8.1 Sign-in, dashboard, approvals

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-AUTH-LOGIN | Login | `/login` | P0 | All |
| AD-AUTH-2FA | 2FA challenge and setup | `/login/2fa` | P0 | All |
| AD-AUTH-INVITE | Accept invitation | `/accept-invite/:token` | P0 | Invited staff |
| AD-HOME | Dashboard | `/` | P0 | All (widgets by role) |
| AD-APPROVALS | Dual-control approvals inbox | `/approvals` | P0 | Approving roles |

### 8.2 Users and roles

| ID | Page | Route | Pri | Role | Notes |
|---|---|---|---|---|---|
| AD-USR-CUSTOMERS | Customers | `/users/customers` | P0 | Support, Fraud/Risk | Tabs: Active · Suspended · Blocked |
| AD-USR-CUSTOMER | Customer detail | `/users/customers/:userId` | P0 | Support, Fraud/Risk | Orders, risk tier, return-abuse score, overrides |
| AD-USR-SELLERS | Sellers | `/users/sellers` | P0 | Seller Manager | Tabs by seller state |
| AD-USR-SELLER | Seller detail | `/users/sellers/:sellerId` | P0 | Seller Manager, Fraud/Risk (suspension), Finance (payout cycle) | KYC, performance, wallet, listings, staff, history; view as seller `[ACTION]` P1 |
| AD-SEL-KYC | KYC queue | `/sellers/kyc` | P0 | Seller Manager | |
| AD-SEL-KYC-CASE | KYC application | `/sellers/kyc/:applicationId` | P0 | Seller Manager | Approve, reject, request information; duplicate flags |
| AD-SEL-PERF | Seller performance | `/sellers/performance` | P0 | Seller Manager | Scores, levels, overrides |
| AD-SEL-APPEALS | Appeals | `/sellers/appeals` | P1 | Seller Manager | |
| AD-USR-ADMINS | Admin users | `/users/admins` | P0 | Super Admin | Invite `[MODAL]` |
| AD-USR-ROLES | Roles and permissions | `/users/roles` | P0 | Super Admin | 11 roles, matrix, thresholds |

### 8.3 Catalogue

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-CAT-PRODUCTS | Canonical products | `/catalog/products` | P0 | Catalog Manager |
| AD-CAT-PRODUCT | Product detail and edit | `/catalog/products/:productId` | P0 | Catalog Manager |
| AD-CAT-REQUESTS | New-product request queue | `/catalog/requests` | P0 | Catalog Manager |
| AD-CAT-REQUEST | Request review | `/catalog/requests/:requestId` | P0 | Catalog Manager |
| AD-CAT-EDITS | Suggested edits | `/catalog/suggested-edits` | P1 | Catalog Manager |
| AD-CAT-VIOL | Price, MAP and anti-dumping queue | `/catalog/offer-violations` | P0 | Catalog Manager |
| AD-CAT-REPORTS | Listing reports and IP notices | `/catalog/reports` | P0 | Catalog Manager |
| AD-CAT-DUP | Duplicates and merge | `/catalog/duplicates` | P1 | Catalog Manager |
| AD-CAT-CATS | Categories (attribute schema, compliance flags, return policy, commission link) | `/catalog/categories` | P0 | Catalog Manager |
| AD-CAT-BRANDS | Brands (gating, authorised sellers) | `/catalog/brands` | P0 | Catalog Manager |
| AD-CAT-ATTR | Attributes | `/catalog/attributes` | P0 | Catalog Manager |
| AD-CAT-COMPL | Prohibited keywords and restricted categories | `/catalog/compliance` | P0 | Catalog Manager |

### 8.4 1P merchandising

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-1P-OFFERS | 1P offers and pricing | `/1p/offers` | P0 | 1P Merchandiser |
| AD-1P-STOCK | Goods receipts and adjustments | `/1p/stock` | P0 | 1P Merchandiser |
| AD-1P-ORDERS | 1P order fulfilment | `/1p/orders` | P0 | 1P Merchandiser |
| AD-1P-RETURNS | 1P returns and restock tasks | `/1p/returns` | P0 | 1P Merchandiser |
| AD-1P-MARGIN | Cost and margin alerts | `/1p/margin` | P0 | 1P Merchandiser, Finance, Super Admin |
| AD-1P-SUPPLIERS | Suppliers | `/1p/suppliers` | P0 | 1P Merchandiser |
| AD-1P-PO | Purchase orders | `/1p/purchase-orders` | P2 | 1P Merchandiser |

### 8.5 Orders and logistics

| ID | Page | Route | Pri | Role | Notes |
|---|---|---|---|---|---|
| AD-ORD-LIST | All orders | `/orders` | P0 | Support, Logistics | Tabs by state |
| AD-ORD-DETAIL | Order detail | `/orders/:orderId` | P0 | Support, Logistics, 1P Merchandiser (1P orders), Finance (A) | Sub-orders, history; overrides and refund trigger under dual control |
| AD-ORD-COD | COD confirmations | `/orders/cod-confirmations` | P0 | Support | |
| AD-ORD-EXC | Order and shipment exceptions | `/orders/exceptions` | P0 | Logistics | SLA breaches, stuck states, failed deliveries, unknown courier statuses |
| AD-LOG-COURIERS | Couriers | `/logistics/couriers` | P0 | Logistics | Tier, mapping, fallback rules; status and COD file upload |
| AD-LOG-SERVICE | Serviceability matrix | `/logistics/serviceability` | P0 | Logistics | Governorates, districts, COD availability, limits |
| AD-LOG-PERF | Courier performance | `/logistics/performance` | P0 | Logistics | |
| AD-LOG-COD | COD remittance and reconciliation | `/logistics/cod-remittance` | P0 | Logistics, Finance | Per-waybill matching, ageing, exposure caps |
| AD-LOG-PICKUPS | Pickups | `/logistics/pickups` | P0 | Logistics | |

### 8.6 Returns and disputes

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-RET-LIST | Returns | `/returns` | P0 | Support |
| AD-RET-DETAIL | Return detail | `/returns/:returnId` | P0 | Support |
| AD-DISP-LIST | Disputes | `/disputes` | P0 | Support, Finance |
| AD-DISP-DETAIL | Dispute detail | `/disputes/:disputeId` | P0 | Support, Finance |

### 8.7 Finance

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-FIN-TX | Transactions | `/finance/transactions` | P0 | Finance |
| AD-FIN-LEDGER | Ledger and trial balance | `/finance/ledger` | P0 | Finance, Compliance |
| AD-FIN-RECON | Reconciliation and exceptions | `/finance/reconciliation` | P0 | Finance |
| AD-FIN-FUNDING | Funding position | `/finance/funding-position` | P0 | Finance |
| AD-FIN-REFUNDS | Refund queue | `/finance/refunds` | P0 | Finance |
| AD-FIN-PAYOUTS | Payout runs | `/finance/payouts` | P0 | Finance |
| AD-FIN-PAYOUT | Payout detail | `/finance/payouts/:payoutId` | P0 | Finance |
| AD-FIN-FAILED | Failed payouts | `/finance/failed-payouts` | P0 | Finance |
| AD-FIN-ADJ | Wallet adjustments | `/finance/adjustments` | P0 | Finance |
| AD-FIN-INV | Commission invoices | `/finance/commission-invoices` | P0 | Finance |
| AD-FIN-DOCS | Document search (receipts, credit notes) | `/finance/documents` | P0 | Finance, Compliance |
| AD-FIN-LOY | Loyalty liability | `/finance/loyalty-liability` | P1 | Finance |

### 8.8 Fraud and risk

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-RISK-QUEUE | Risk queue | `/risk/queue` | P0 | Fraud/Risk |
| AD-RISK-CASE | Case detail | `/risk/cases/:caseId` | P0 | Fraud/Risk |
| AD-RISK-COD | COD risk configuration | `/risk/cod-config` | P0 | Fraud/Risk |
| AD-RISK-BLOCK | Blocklists | `/risk/blocklist` | P0 | Fraud/Risk |
| AD-RISK-ABUSE | Return-abuse monitor | `/risk/return-abuse` | P1 | Fraud/Risk |
| AD-RISK-OVR | Override log | `/risk/overrides` | P0 | Fraud/Risk, Compliance |

### 8.9 Promotions, loyalty and ads

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-PRO-COUPONS | Platform coupons | `/promotions/coupons` | P1 | Marketing |
| AD-PRO-APPROVALS | Seller coupon approvals | `/promotions/approvals` | P1 | Marketing |
| AD-PRO-FLASH | Flash deals | `/promotions/flash-deals` | P1 | Marketing |
| AD-PRO-CAMP | Campaigns | `/promotions/campaigns` | P1 | Marketing |
| AD-PRO-PRICING | 1P pricing rules | `/promotions/pricing-rules` | P0 | 1P Merchandiser |
| AD-LOY-CONFIG | Loyalty and referral configuration | `/loyalty/config` | P1 | Marketing |
| AD-ADS-HOME | Ads overview | `/ads` | P1 | Marketing |
| AD-ADS-SPONSORED | Sponsored placements | `/ads/sponsored` | P1 | Marketing |
| AD-ADS-MOD | Ad moderation and invalid clicks | `/ads/moderation` | P1 | Marketing |

### 8.10 Reviews, support and CMS

| ID | Page | Route | Pri | Role | Notes |
|---|---|---|---|---|---|
| AD-REV-QUEUE | Review moderation | `/reviews` | P0 | Support | Tabs: Flagged · Reported · Published · Removed |
| AD-REV-RULES | Pre-screen rules | `/reviews/rules` | P1 | Support | |
| AD-QA-QUEUE | Q&A moderation | `/qa` | P1 | Support | |
| AD-SUP-LIST | Tickets | `/support` | P0 | Support | Tabs by state; create on behalf `[ACTION]` (ADM-6) |
| AD-SUP-DETAIL | Ticket detail | `/support/:ticketId` | P0 | Support | |
| AD-CMS-HOME | Home page sections | `/cms/homepage` | P0 | Content | |
| AD-CMS-BANNERS | Banners | `/cms/banners` | P0 | Content | |
| AD-CMS-PAGES | Static and legal pages | `/cms/pages` | P0 | Content | Versions; re-acceptance trigger |
| AD-CMS-ANNOUNCE | Announcement bar | `/cms/announcements` | P1 | Content | |
| AD-CMS-HELP | Help-centre articles | `/cms/help` | P1 | Content | |
| AD-CMS-EMAIL | Email templates | `/cms/email-templates` | P0 | Content | |
| AD-CMS-SMS | SMS templates | `/cms/sms-templates` | P0 | Content | |
| AD-CMS-PUSH | Push templates | `/cms/push-templates` | P1 | Content | |

### 8.11 Notifications, analytics and privacy

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-NOT-CAMP | Targeted campaigns | `/notifications/campaigns` | P1 | Marketing |
| AD-NOT-LOG | Delivery log | `/notifications/delivery-log` | P0 | Support |
| AD-AN-HOME | Platform overview | `/analytics` | P0 | Per role |
| AD-AN-SALES | Sales | `/analytics/sales` | P0 | Per role |
| AD-AN-USERS | Customers | `/analytics/users` | P0 | Per role |
| AD-AN-SELLERS | Sellers | `/analytics/sellers` | P0 | Per role |
| AD-AN-CATS | Categories | `/analytics/categories` | P0 | Per role |
| AD-AN-SEARCH | Search (zero results, synonyms) | `/analytics/search` | P0 | Per role |
| AD-AN-PAY | Payments by method | `/analytics/payments` | P1 | Per role |
| AD-AN-LOG | Logistics | `/analytics/logistics` | P1 | Per role |
| AD-PRIV-REQ | Data-subject requests | `/privacy/requests` | P0 | Compliance |

### 8.12 Platform settings

| ID | Page | Route | Pri | Role |
|---|---|---|---|---|
| AD-SET-GENERAL | General | `/settings/general` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-LOCAL | Market, languages and formats | `/settings/localization` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-GEO | Geo reference data | `/settings/geo` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-CALENDAR | Platform holidays and force majeure | `/settings/calendar` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-SHIP | Shipping zones, rates, free threshold, surcharges | `/settings/shipping` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-TAX | Tax configuration | `/settings/tax` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-PAY | Payment methods and gateways | `/settings/payments` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-COMM | Commission schedule | `/settings/commissions` | P0 | Finance, Super Admin (A) |
| AD-SET-PRICE | Price floors, anti-dumping, MAP | `/settings/price-rules` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-LIMITS | Seller listing caps | `/settings/seller-limits` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-SLA | Seller SLAs, escrow hold, order timers | `/settings/sla` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-RETURNS | Return windows and eligibility by category | `/settings/return-policies` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-RANK | Buy Box and search weights, synonyms | `/settings/ranking` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-LOYALTY | Loyalty programme | `/settings/loyalty` | P1 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-NOTIF | Notification settings | `/settings/notifications` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-INTEG | Integrations and credentials status | `/settings/integrations` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-APP | App configuration and feature flags | `/settings/app-config` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-SET-SEC | Admin security | `/settings/security` | P0 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |
| AD-AUDIT | Audit trail viewer | `/audit-log` | P0 | Super Admin, Compliance (read only) |
| AD-SYS-HEALTH | System health (queues, outbox, dead letters) | `/system/health` | P1 | Super Admin, owning role ([admin-panel](../05-trust/admin-panel.md) §1) |

---

## 9. Static and information pages (Storefront) `[PUB]`

Managed in the CMS, Arabic and English. The first fourteen are the launch set ([support-cms](../02-commerce/support-cms.md) §2).

| ID | Page | Route | Pri |
|---|---|---|---|
| SF-ST-ABOUT | About Nyazek | `/about` | P0 |
| SF-ST-CONTACT | Contact us (ticket form) | `/contact` | P0 |
| SF-ST-FAQ | FAQ (customers) | `/faq` | P0 |
| SF-ST-FAQ-SELLER | FAQ (sellers) | `/faq/seller` | P0 |
| SF-ST-TERMS | Terms & Conditions | `/legal/terms` | P0 |
| SF-ST-PRIVACY | Privacy Policy | `/legal/privacy` | P0 |
| SF-ST-COOKIES | Cookie Policy | `/legal/cookies` | P0 |
| SF-ST-RETURNS | Return & Refund Policy | `/legal/returns` | P0 |
| SF-ST-SHIPPING | Shipping Policy | `/legal/shipping` | P0 |
| SF-ST-PROTECT | Customer Protection Policy | `/legal/customer-protection` | P0 |
| SF-ST-DISPUTE | Dispute Resolution Policy | `/legal/dispute-resolution` | P0 |
| SF-ST-SELLERAGR | Seller Agreement | `/legal/seller-agreement` | P0 |
| SF-ST-PROHIBITED | Prohibited & Restricted Items Policy | `/legal/prohibited-items` | P0 |
| SF-ST-REPORT | Report a listing / intellectual-property notice | `/report` | P0 |
| SF-ST-PAYGUIDE | Payment methods guide | `/payments` | P1 |
| SF-ST-LOYALTY | Loyalty programme terms | `/legal/loyalty` | P1 |
| SF-ST-HOW | How it works | `/how-it-works` | P2 |
| SF-ST-TRUST | Safety and trust centre | `/trust` | P2 |
| SF-ST-CAREERS | Careers | `/careers` | P2 |
| SF-ST-BLOG | Blog | `/blog` | P2 |
| SF-ST-PRESS | Press | `/press` | P2 |
| SF-ST-SITEMAP | HTML sitemap | `/sitemap` | P2 |

## 10. System and technical routes

| ID | Page or resource | Route | Pri | Notes |
|---|---|---|---|---|
| SYS-404 | Not found | `*` | P0 | Every app |
| SYS-403 | Forbidden | — | P0 | Realm or role denied |
| SYS-401 | Session expired | — | P0 | |
| SYS-500 | Server error | — | P0 | Correlation ID shown |
| SYS-MAINT | Maintenance | — | P0 | Driven by app configuration |
| SYS-OFFLINE | Offline shell | — | P1 | |
| SYS-APP | App download interstitial | `/app` | P2 | With the apps |
| SYS-ROBOTS | `robots.txt` | `/robots.txt` | P0 | Seller and admin hosts disallow all |
| SYS-SITEMAPXML | XML sitemaps | `/sitemap.xml` | P0 | Per type and language, with hreflang |
| SYS-MANIFEST | Web app manifest | `/manifest.webmanifest` | P1 | |
| SYS-AASA | iOS universal-link file | `/.well-known/apple-app-site-association` | P1 | |
| SYS-ASSETLINKS | Android app-link file | `/.well-known/assetlinks.json` | P1 | |
| SYS-SECURITYTXT | Security contact | `/.well-known/security.txt` | P1 | |
| SYS-APPCONFIG | App configuration endpoint | `GET /v1/app-config` | P0 | [api-standards](../06-platform/api-standards.md) API-6 |
| SYS-HEALTH | Health endpoints | `/health/live`, `/health/ready` | P0 | |

## 11. Mobile mapping (after launch)

Storefront routes are stable so each can become a deep link. The native apps are Flutter ([mobile-flutter](../07-clients/mobile-flutter.md) §6).

| Phase | App | Storefront and seller Page IDs reused as screen specifications |
|---|---|---|
| M1 | `mobile_customer` | `SF-HOME`, `SF-SEARCH`, `SF-CATEGORY`, `SF-PDP`, `SF-STORE`, `SF-FAV`, `SF-CART`, `SF-CHK-*`, `SF-ORD-*`, `SF-RET-*`, `SF-DISP-*`, `SF-REV-*`, `SF-ADDR`, `SF-NOTIF`, `SF-PROF`, `SF-SEC-*`, `SF-PRIV` |
| M2 | `mobile_seller` | `SL-HOME`, `SL-ORD-*`, `SL-CAT-STOCK`, `SL-CAT-OFFER-NEW`, `SL-NOTIF` |

Web-only by design: Admin Panel, bulk import, financial statements, KYC document upload.

## 12. Page count

<!--COUNTS-->
| Zone | P0 | P1 | P2 | Total |
|---|---|---|---|---|
| Storefront (incl. public seller and static pages) | 65 | 12 | 9 | 86 |
| Seller Dashboard | 52 | 22 | 0 | 74 |
| Admin Panel | 94 | 23 | 1 | 118 |
| System and technical routes | 9 | 5 | 1 | 15 |
| **Total** | **220** | **62** | **11** | **293** |
<!--/COUNTS-->

Counts are produced by `_tools/count_pages.py` from the Page IDs in this file. Modals, filters and actions are specified inside their page and are not counted.

## 13. Traceability rules

- Every epic, story, task, design reference folder, Storybook story and end-to-end test references Page IDs.
- A page without an ID, a priority and a signed-off design is not ready for implementation ([design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §7).
- The sitemap never introduces a feature the domain documents do not contain. A new page is added here in the same change as its requirement.

## 14. Open decisions that change pages

| Decision | Effect |
|---|---|
| D-02 COD refund destination | `SF-REFACC` stays for customer-supplied accounts; replaced by a refund-credit page if store credit were chosen |
| D-03 payout cadence | `SL-WAL-PAYOUTS` shows the seller's cycle |
| D-11 payment channels | `SF-CHK-PAY` and `AD-SET-PAY` gain the chosen methods |
| D-13 Kurdistan Region and Kurdish | Adds a language (`/ku`), templates and serviceability |
| D-40 new markets | Market selection and market-specific pages; none in v1.0 |
