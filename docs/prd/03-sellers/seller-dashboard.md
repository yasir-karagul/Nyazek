# Seller Dashboard

**Authoritative for:** the Seller Dashboard application: purpose, modules, priorities, store staff roles, behaviour rules.
**Owner mandate:** sellers have a dedicated dashboard through which they fully manage their stores.
**Related:** [seller-accounts-kyc](seller-accounts-kyc.md) · [seller-performance](seller-performance.md) · [web-apps](../07-clients/web-apps.md) · [sitemap](../09-information-architecture/sitemap.md) §7 (page IDs `SL-*`) · page specifications: [pages-seller-operations](../09-information-architecture/pages-seller-operations.md), [pages-seller-business](../09-information-architecture/pages-seller-business.md) · [navigation](../09-information-architecture/navigation.md) §2

---

## 1. Purpose and principles

The Seller Dashboard is a separately deployed web application on its own origin (`seller.<domain>`) with its own session, mandatory 2FA and its own design shell. A seller can run the whole store without contacting Nyazek.

- Arabic-first RTL, English available; language is an account setting.
- Usable on a phone browser: many sellers manage orders from phones. A Flutter seller companion app follows after launch ([mobile-flutter](../07-clients/mobile-flutter.md)).
- Every dashboard capability is an API capability (`/v1/seller/*`); the dashboard contains no business rules.
- Data-isolated: every query is scoped to the seller in the data-access layer; cross-seller access tests run in CI.
- Performance target: interactive within 2.5 seconds on a mid-range phone over 4G ([reliability-sre](../06-platform/reliability-sre.md) §2).

## 2. Modules

| Module | Capabilities | Priority |
|---|---|---|
| Home (command centre) | KPI cards (sales, orders, pending actions, wallet, rating, performance score); action queue (orders awaiting confirmation with SLA countdown, return requests, disputes due, restock tasks, low stock, expiring documents, policy warnings); setup checklist; platform announcements | P0 |
| Orders | Tabs by state; order detail; accept or reject with reason; mark ready to ship; print label, packing slip and receipt; request pickup or declare drop-off; bulk accept, label and ready; SLA timers; customer phone in full only while fulfilling (SDB-7) | P0 |
| Catalog | Offers on canonical products; new-product requests with status and reasons; seller-owned listings; drafts; bulk import and export; quick-edit grid for price and stock; variants; violations centre (price floor, MAP, anti-dumping); low-stock alerts | P0 |
| Returns & Disputes | Return requests (approve, reject with reason and evidence, inspection result, partial-refund proposal); dispute centre (respond, upload evidence, decision history) | P0 |
| Wallet & Payouts | Pending, Awaiting courier remittance, Available and On hold; transaction history with filters; payout schedule, history, statements; commission invoices; payout destinations with re-verification | P0 |
| Reviews | Read product reviews and seller ratings; flag for moderation | P0 |
| Performance | Live score, metric breakdown, contributing orders, level, recovery tracker | P0 |
| Analytics | Sales, units, orders and conversion by product, category and governorate; ranges 7 days, 30 days, custom; export | P0 (traffic and funnel views P1) |
| Store Settings | Profile, logo and banner, pickup and return addresses, handling time, return policy, notification preferences | P0 |
| Account & Security | Profile, password, 2FA, devices and sessions, login history, KYC documents and renewals | P0 |
| Notification Centre | Inbox for all seller events ([notifications-messaging](../02-commerce/notifications-messaging.md) §3.2) | P0 |
| Promotions | Coupons (admin-approved), deals, join campaigns | P1 |
| Advertising | Campaigns, budgets, reports, billing | P1 |
| Messages & Q&A | Per-order customer threads; answers to product questions | P1 |
| Activity log | Owner sees every action by the owner and staff (SDB-2) | P0 |
| Team & Roles | Invite staff, assign preset roles | P1 |
| Help & Appeals | Help articles, tickets, performance appeals | P1 |
| Buy Box insights | Win rate and reasons for loss | P1 |
| Vacation mode, referral link, account closure request | | P1 |

Scope note: analytics "traffic and conversion funnel" was P0 in v6. It depends on the clickstream pipeline, which is not otherwise needed for launch; sales analytics from order data stay P0 and traffic views move to P1 (ratification: D-33).

## 3. Store staff roles (P1)

Legend: F full · R read · – none. Roles are preset; a per-permission editor is out of scope.

| Area | Owner | Manager | Catalog | Fulfilment | Finance | Support |
|---|---|---|---|---|---|---|
| Orders | F | F | R | F | R | R |
| Catalog | F | F | F | R | – | R |
| Returns & Disputes | F | F | – | F | R | F |
| Wallet & Payouts (view) | F | R | – | – | F | – |
| Payout destinations, payout settings | F | – | – | – | – | – |
| Promotions & Ads | F | F | R | – | R | – |
| Customers (reviews, messages, Q&A) | F | F | R | R | – | F |
| Performance & Analytics | F | F | R | R | R | – |
| Store Settings | F | R | – | – | – | – |
| Team & Roles (including the activity log and account closure) | F | – | – | – | – | – |

- Home is open to every role; its figures and lists show only the areas the role can read.
- Every staff member manages their own account (profile, security) and sees their own notifications, filtered to the areas they can read.
- Vacation mode is part of Store Settings; pickups are part of Orders.
- KYC documents, appeals, the referral programme and help and support tickets are Owner only until the owner decides wider access (T-0064) ([ADR-0007](../../adr/0007-decisions-from-the-ia-consistency-pass.md)).

- Staff are separate accounts in the seller realm with their own email, password and mandatory 2FA.
- Permissions are enforced by the API per endpoint; the dashboard only hides what the API would refuse.
- The owner role cannot be removed; ownership transfer is a Support-assisted, KYC-verified process.

## 4. Behaviour rules

- SDB-1 What the dashboard allows in each seller state is defined in [seller-accounts-kyc](seller-accounts-kyc.md) §5.
- SDB-2 Activity log: every change to price, stock, offers, settings, payout destinations and staff permissions records who, what, when and from which device; the owner can view it.
- SDB-3 Sensitive actions (payout destination change, staff role change, bulk price change above `cfg:sellers.bulk_price_change_confirm_percent` (default 30%)) require re-authentication with 2FA.
- SDB-4 New orders and SLA countdowns update live (server-sent events with polling fallback) and also raise notifications.
- SDB-5 Orders, offers and transactions can be exported to CSV or Excel; exports are generated as background jobs and are scoped to the seller.
- SDB-6 Every list has search, filters, empty, loading and error states, and works in Arabic and English.
- SDB-7 The dashboard never displays a customer's full phone number in list views; the order detail shows it only while the order is being fulfilled.

## 5. Acceptance criteria

- A new seller can complete onboarding, list a product, fulfil an order, handle a return and see the resulting wallet movement without contacting support.
- With a second seller's identifiers substituted into any request, the API returns `404`.
- Every P0 module is usable at a 360-pixel viewport width in Arabic.
