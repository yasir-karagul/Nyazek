# Scope & Priorities

**Authoritative for:** the meaning of priorities, the feature map by priority with links to the specifying document, proposed priority changes, and what is out of scope.
**Related:** [release-plan](../00-governance/release-plan.md) · [open-decisions](../00-governance/open-decisions.md) · [sitemap](../09-information-architecture/sitemap.md) (page-level priorities) · [user-journeys](user-journeys.md) · [market-expansion](market-expansion.md)

---

## 1. Priority definitions

| Priority | Meaning |
|---|---|
| **P0** | Launch gate. v1.0 does not go live without it |
| **P1** | Launch target. Planned for v1.0 but may ship in a fast-follow release within 30 days after launch |
| **P2** | Post-launch roadmap; not built for v1.0 |
| **Future** | Direction only; no commitment |

v6 said in one place that all P0 and P1 features must be complete before launch and in another that P1 may ship up to 30 days later. The table above is the single definition. Readiness work for a later feature (for example mobile readiness, loyalty fields in the order model) carries its own priority.

## 2. Feature map

### 2.1 P0

| Area | Features | Specified in |
|---|---|---|
| Platform | API-first backend; three web apps on separate origins; Arabic and English; Iraq market in IQD; mobile readiness; market readiness for later expansion | [architecture](../06-platform/architecture.md), [web-apps](../07-clients/web-apps.md), [mobile-flutter](../07-clients/mobile-flutter.md), [market-expansion](market-expansion.md) §3 |
| Customer account | Profile, favourites, account home, deletion effects | [customer-account](../02-commerce/customer-account.md) |
| Identity | Customer registration and login (phone OTP, email + password, Google, Facebook); guest checkout; seller and admin authentication with mandatory 2FA; one-email-one-account | [identity-access](../05-trust/identity-access.md) |
| Catalogue | Categories and attribute schemas; shared catalogue; listing types A, B, C; offers; bulk import and export; media pipeline; prohibited-item enforcement | [catalog-listings](../02-commerce/catalog-listings.md) |
| Pricing | Price floor, anti-dumping, MAP, 1P margin alerts, reference-price rule; free delivery threshold | [pricing-promotions](../02-commerce/pricing-promotions.md) |
| Discovery | Search with Arabic handling, filters, sort, autocomplete; Buy Box | [search-buy-box](../02-commerce/search-buy-box.md) |
| Buying | Cart, five-step checkout, quote engine, multi-seller orders, order tracking, cancellation | [checkout-orders](../02-commerce/checkout-orders.md) |
| Inventory | Reservation, allocation, stock movements | [inventory](../02-commerce/inventory.md) |
| Payments | COD with risk engine and confirmation; Zain Cash, Asia Hawala, FastPay (directly or through an aggregator, D-11); refunds including manual queue | [payments](../04-finance/payments.md), [fraud-risk](../05-trust/fraud-risk.md) |
| Finance | Double-entry ledger, reconciliation, commission, wallet, escrow release, payouts, statements, receipts and commission invoices, tax abstraction | [04-finance](../04-finance/ledger-reconciliation.md) |
| Logistics | Courier abstraction with tiers A–C, serviceability, labels, pickup, tracking, proof of delivery, RTO, reverse logistics, COD remittance | [logistics](../02-commerce/logistics.md) |
| After-sales | Returns, refunds, disputes | [returns-disputes](../02-commerce/returns-disputes.md) |
| Trust | Seller KYC; seller performance score and levels; reviews and ratings with pre-screen moderation; risk scoring | [03-sellers](../03-sellers/seller-accounts-kyc.md), [reviews-qa](../02-commerce/reviews-qa.md), [fraud-risk](../05-trust/fraud-risk.md) |
| Seller Dashboard | Home, orders, catalog, returns and disputes, wallet, reviews, performance, sales analytics, settings, security, notification centre | [seller-dashboard](../03-sellers/seller-dashboard.md) |
| Admin Panel | 11 roles, permission matrix, dual control, all operational queues, platform settings, audit viewer | [admin-panel](../05-trust/admin-panel.md), [admin-governance](../05-trust/admin-governance.md) |
| 1P store | Goods receipts with cost, adjustments, pricing and margin alerts, fulfilment, returns to the warehouse, basic supplier record | [first-party-operations](../03-sellers/first-party-operations.md) |
| Communication | In-app inbox, email, SMS; transactional catalogue; templates | [notifications-messaging](../02-commerce/notifications-messaging.md) |
| Support and content | Ticketing; 14 static and legal pages; CMS for home page and banners; consent-gated tags | [support-cms](../02-commerce/support-cms.md) |
| Cross-cutting | Security baseline, privacy and consent, audit trail, observability, DR, compliance disclosures | [05-trust](../05-trust/security.md), [reliability-sre](../06-platform/reliability-sre.md) |

### 2.2 P1

Card payments through a PSP-hosted page · additional channels (Qi Card, FIB, Nass) per D-11 · weekly payouts · charging a COD fee (the fee mechanism is P0 with `cfg:cod.fee` at 0 until D-21, [ADR-0007](../../adr/0007-decisions-from-the-ia-consistency-pass.md)) · loyalty programme, customer referrals, birthday reward · seller referral programme · seller coupons, deals, flash deals, campaign pages · sponsored ads · customer–seller messaging · product Q&A · brand pages · typo tolerance and "did you mean" · personalised ordering and autocomplete · delivery-speed filter · web push · voice-call COD confirmation · price-drop and back-in-stock alerts · optional customer 2FA · saved card tokens · store staff and roles · seller help centre, tickets and appeals in the dashboard · Buy Box insights and traffic analytics for sellers · vacation mode · seller rates customer · suggested edits and duplicate merge tooling · map pin on addresses · line-level order rejection · replacement as an option on returns · optional shipment insurance · offline shell · WCAG audit of core flows · satisfaction survey · clickstream analytics · back-in-stock alerts, buy again, share a product, abandoned-cart reminder · read-only "view as seller" for Support.

### 2.3 P2

Flutter customer app (M1), seller companion app (M2), enhancements (M3) · cash-top-up ad credit · semantic search · destination-aware Buy Box · multi-parcel sub-orders · returnless refunds · inspection hub for 3P returns · machine-learned risk models · commercial device fingerprinting · automated KYC document verification · bug-bounty programme · seller subscriptions · 1P purchase orders and warehouse management · Kurdish (Sorani) interface and Kurdistan Region operations (after D-13) · recommendations (recently viewed, frequently bought together) · structured warranty claims · used-goods listings (if D-44 allows).

### 2.4 Future

Expansion to Syria and the Gulf as additional markets ([market-expansion](market-expansion.md); D-40) · AI-powered recommendations · same-day delivery in Baghdad · subscription and recurring orders · fulfilment of sellers' goods by Nyazek · a public API for sellers · extraction of Payments, Ledger, Wallet and Risk into services.

## 3. Priority changes proposed by this review (ratification: D-33)

| Item | v6 | v7 | Reason |
|---|---|---|---|
| Personalised autocomplete | P0 | P1 | Needs behavioural history and consent that do not exist at launch; popularity-based autocomplete stays P0 |
| Seller traffic and funnel analytics | P0 | P1 | Depends on the clickstream pipeline; sales analytics stay P0 |
| Seller rates customer ("two-way rating") | Unprioritised, implied launch | P1 | Weak, retaliation-prone signal; never drives automatic restrictions |
| Replacement before refund | Mandatory | Optional, P1 | Conflicts with the money-back guarantee; unspecified fulfilment flow (D-25) |
| Cash-pickup payouts | Launch method | P1, subject to D-30 | Needs a partner network and cash controls |
| "Push" notifications at launch | P0 | In-app inbox P0; web push P1; mobile push with the apps | No native app exists at launch |
| Component-level accessibility | P1 | P0 | Cheap to build in, expensive to retrofit; full audit stays P1 |
| Courier Tier C (file-based) integration | Not specified | P0 | Launch must not depend on courier APIs |
| Manual refund and payout fallbacks | Not specified | P0 | Launch must not depend on PSP refund and payout APIs |
| Price-drop notification on favourites | P0 | P1 | Promotional class requiring opt-in and price-history jobs; favourites themselves stay P0 |

## 4. Out of scope for v1.0

- Native mobile applications (readiness is in scope).
- Product comparison; public wishlist sharing; store follow.
- Customer wallet, stored balance or store credit (unless D-02 chooses it).
- eDinar; instalments; buy-now-pay-later.
- B2B / wholesale portal; live shopping.
- WhatsApp notifications and support; live chat; Snapchat Pixel.
- Any customer-to-seller account conversion, linking or merging (prohibited by ID-3).
- Custom per-permission role editor for seller staff.
- Partial acceptance of a COD parcel at the door.
- Seller-chosen couriers or seller-set shipping fees.
- Public seller replies to reviews.
- Pre-purchase customer–seller chat.
- Digital goods, services, vouchers and gift cards; gift options.
- Scheduled delivery slots, pickup points and lockers; substitution of items by the seller.
- Cross-border selling or shipping; sellers located outside the market; any market other than Iraq.
- Multi-currency display or currency conversion.
- Dark theme.
- PHP in any part of the system.
- Any AI coding agent other than Claude; any Figma MCP integration.
