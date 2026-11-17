# Seller Dashboard Pages: Wallet, Marketing, Customers, Performance, Analytics, Settings, Account

**Authoritative for:** the content and actions of these Seller Dashboard pages.
**Read with:** [README](README.md) §2 · [navigation](navigation.md) §2 · [taxonomy-and-labels](taxonomy-and-labels.md) §4 · [sitemap](sitemap.md) §7.7–7.12
**Rules live in:** [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) · [pricing-promotions](../02-commerce/pricing-promotions.md) §2–3 · [advertising](../02-commerce/advertising.md) · [reviews-qa](../02-commerce/reviews-qa.md) · [notifications-messaging](../02-commerce/notifications-messaging.md) §6 · [seller-performance](../03-sellers/seller-performance.md) · [seller-dashboard](../03-sellers/seller-dashboard.md)

---

## 1. Wallet (area: Wallet)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-WAL-HOME | `TPL-DASH` | Four balances, each with a one-line explanation and a link to its movements: Pending · Awaiting courier remittance · Available · On hold (with the reason of each hold). Next payout date, estimated amount and destination (masked). Deficit notice when the balance is negative. Recent movements | Open movements, payouts, destinations | First-payout hold and suspension-hold notices where they apply | WAL-1 to WAL-11, PO-1 |
| SL-WAL-TX | `TPL-LIST` | Movements: date, type (the movement types in commission-wallet-payouts §2: sale release, commission, refund, shipping charge, payout, payout returned, transfer fee, adjustment, chargeback, ad spend (P1), ad credit (P1), referral bonus (P1), courier compensation; holds are listed separately on `SL-WAL-HOME`), reference (sub-order, return, payout), amount, balance affected. Filters by type, date, reference; totals for the filtered period | Open the referenced object; export CSV | – | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) §2, SDB-5 |
| SL-WAL-PAYOUTS | `TPL-LIST` | Payouts: period, amount, destination (masked), status, paid date, reference | Open a statement | The seller's payout cycle and minimum are shown above the list; failed, rejected and returned payouts show the reason and the action needed | PO-1 to PO-7 |
| SL-WAL-PAYOUT | `TPL-DETAIL` | Statement: period, opening balance, every movement grouped by sub-order (gross, commission, fees, refunds, adjustments), transfer fee line if the seller bears it, net paid, destination, bank reference | Download PDF and CSV | A failed payout shows the reason and what the seller should do | PO-7, PO-9 |
| SL-WAL-INV | `TPL-LIST` | Commission invoices per settlement period: number, period, amount, tax line when non-zero | Download PDF | – | PO-8, [tax-invoicing](../04-finance/tax-invoicing.md) §3 |
| SL-WAL-METHODS | `TPL-LIST` (cards) | Payout destinations: type, provider, masked number, holder name, verification state, date added, hold notice for a new destination | Add or change (step-up, then form; the holder must match the verified identity) | Owner only; a change is announced to the owner's email and phone and starts the hold | PO-4, PO-5, SDB-3 |

## 2. Marketing (P1; area: Promotions and ads)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-PRO-LIST | `TPL-LIST` | Tabs: Active · Scheduled · Awaiting approval · Ended. Promotions: type (coupon, deal, campaign participation), products, discount, dates, usage, cost to the seller so far | Create coupon; create deal; join a campaign; end early | – | PRM-1 to PRM-5, [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| SL-PRO-COUPON | `TPL-FORM` | Code or auto-generated, discount (percentage or amount), products or whole store, minimum spend, per-customer limit, total budget, dates | Submit for approval | Discount floor and stacking limits validated; preview of the customer-facing terms | PRM-2 |
| SL-PRO-DEAL | `TPL-FORM` | Products, deal price, quantity limit, dates | Publish | Deal price must satisfy the reference-price and floor rules | [pricing-promotions](../02-commerce/pricing-promotions.md) §2, PRC-2, PRC-9 |
| SL-PRO-CAMP | `TPL-LIST` | Platform campaigns open for participation: name, dates, conditions, who funds what | Opt in with selected offers and prices; withdraw before the lock date | – | [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| SL-ADS-LIST | `TPL-LIST` | Campaigns: name, status, budget, spend, impressions, clicks, orders, sales, return on spend | Create; pause; resume | Requires good standing; blocked with the reason otherwise | [advertising](../02-commerce/advertising.md) §2, AD-13 |
| SL-ADS-NEW | `TPL-WIZARD` | Products → keywords or automatic targeting → bid and daily and total budget → dates → review | Launch | Minimum bid; eligibility of each product (active, in stock) | [advertising](../02-commerce/advertising.md) §2–3 |
| SL-ADS-DETAIL | `TPL-DETAIL` | Settings; performance by day, product and keyword; invalid clicks removed | Edit bids and budgets; pause; end | – | [advertising](../02-commerce/advertising.md) §5, §6, AD-11 |
| SL-ADS-BILL | `TPL-LIST` | Ad charges by period, how they were settled (deducted from wallet), invoices | Download | – | [advertising](../02-commerce/advertising.md) §5 |

## 3. Customers (area: Customers)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-REV | `TPL-LIST` | Tabs: Product reviews · Seller ratings. Review cards with product, stars, text, photos, date, order reference; average and distribution above; filters by stars and product | Flag for moderation (reason select) | Sellers cannot reply to or remove reviews; the customer's name is the display name only | REV-3, REV-5 |
| SL-MSG | `TPL-LIST`; a thread opens on a sub-route with the Message thread component | Threads per order: customer display name, sub-order number, last message, unread marker, time waiting. Thread view with the order summary pinned | Reply (text, images); report | P1; contact details blocked; response time is tracked and shown | Messaging rules |
| SL-QA | `TPL-LIST` | Tabs: Unanswered · Answered. Product questions on the seller's offers | Answer; report a question | P1; answers pass the content pre-screen | Q&A rules |

## 4. Performance and analytics (area: Performance and analytics)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-PERF | `TPL-DASH` | Score and level with what the level means; each metric with its value, target, weight and trend; the orders behind each metric (list, with exclusions marked); active consequences and what ends them; recovery tracker; violation history | Open a contributing order; start an appeal (P1) | "Not enough data yet" until the minimum order count; overrides shown with their reason | PRF-1 to PRF-11 |
| SL-APPEAL | `TPL-LIST` and `TPL-FORM` | Appeals with subject (metric event, level, violation), status, decision. Form: what is appealed, explanation, evidence | Submit | P1; one appeal per event; deadline to appeal shown | Appeals |
| SL-AN-HOME | `TPL-DASH` | Period selector (7 days, 30 days, custom). Sales value, orders, units, average order value, cancellation rate, return rate, rating; chart of sales over time; top products | Change period; open a detail page | Figures show their period and when they were last updated | DAT-4 |
| SL-AN-SALES | `TPL-LIST` | Sales by product, by category or by governorate (switch): units, orders, sales value, returns | Export CSV | – | – |
| SL-AN-REV | `TPL-DASH` | Rating over time; distribution; products with the lowest ratings; common reasons in returns | Open the product's reviews | – | – |
| SL-AN-TRAFFIC | `TPL-DASH` | Product views, add-to-cart rate, conversion, by product and day | Export | P1 (needs clickstream) | [data-analytics](../06-platform/data-analytics.md) §5 |
| SL-AN-BUYBOX | `TPL-LIST` | Per offer: share of time winning the Buy Box, current state, main reason when not winning, price gap to the winner | Open the offer | P1 | [search-buy-box](../02-commerce/search-buy-box.md) §2 |

## 5. Settings (area: Store settings)

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-SET-STORE | `TPL-FORM` | Store name, slug (read-only, derived from the name, SEL-6), logo, banner, about text in Arabic and English; preview of the store page | Save | Name change limit and pre-screen; images through the media checks | SEL-6 |
| SL-SET-PICKUP | `TPL-LIST` (cards) | Pickup and return addresses with contact name and phone, working hours, which is default for new offers | Add, edit, set default, remove | Removal blocked while in use, with the list of offers and orders using it | SEL-5 |
| SL-SET-POLICY | `TPL-FORM` | Default handling time (1 to the platform maximum, SLA-6); store return policy: a longer return window up to the platform maximum, and free change-of-mind return shipping in categories that allow change of mind; the category rules shown read-only beside each field | Save (applies to orders placed afterwards, RET-6) | Sellers cannot set shipping fees or shorten a window; values outside limits are refused | RET-9, RET-6, SLA-6 |
| SL-SET-NOTIF | `TPL-FORM` | Per event group (orders, returns and disputes, wallet, catalog, account) and channel (in-app always on; email; SMS for urgent events) | Save | Critical notices cannot be turned off | [notifications-messaging](../02-commerce/notifications-messaging.md) §3 |
| SL-SET-VACATION | `TPL-FORM` | Start and end dates; what happens (offers hidden from sale, open orders must still be fulfilled) | Turn on (disabled, with the reason, while sub-orders await confirmation, SEL-9); end early | P1; maximum duration per `cfg:sellers.vacation_max_days` | Vacation mode |

## 6. Team, account, help

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SL-TEAM | `TPL-LIST` | Staff: name, email, role, 2FA state, last sign-in, invitation state | Invite (email and role); change role; remove; resend invitation | P1; owner only; step-up for changes | [seller-dashboard](../03-sellers/seller-dashboard.md) §3 |
| SL-TEAM-LOG | `TPL-LIST` | Changes to prices, stock, offers, settings, payout destinations and permissions: when, who, what, old and new value; uses of "view as seller" by Nyazek staff (P1). Filters by person, type, date | Export | Owner only | SDB-2, ADM-7 |
| SL-ACC-PROFILE | `TPL-FORM` | Owner name, sign-in email and phone with verified states, language | Change email or phone (Step-up prompt; for a phone, Phone and OTP input to the new number, AUTH-5; notice to the old one) | Claim-conflict message per AUTH-2 | ID-5 |
| SL-ACC-SEC | `TPL-FORM` | Password; 2FA method and recovery codes; active sessions; sign-in history | Change password; regenerate codes (step-up, SES-5); sign out a session | 2FA cannot be disabled | SES-4, 2FA rules |
| SL-ACC-KYC | `TPL-LIST` | Verified identity and business details (read-only); documents with expiry dates and state (valid, expiring, expired, in review) | Upload a renewal; request a change of business details (re-verification) | Expiry warnings at 30 and 7 days; consequences of lapse stated | KYC-7, KYC-8 |
| SL-ACC-REF | `TPL-DASH` | Referral link, referred sellers and their status, rewards | Copy the link | P1 | Referral rules |
| SL-ACC-CLOSE | `TPL-FORM` | What closing means: offers end, open orders must complete, final settlement after the last return window; current blockers | Request closure (step-up) | P1; owner only; not available while suspended for an investigation. Open orders, returns, disputes and a deficit do not block the request; they are listed because they delay final settlement in `CLOSING` | Seller states (seller-accounts-kyc §5), PO-10 |
| SL-NOTIF | `TPL-LIST` | Tabs: All · Orders · Returns and disputes · Wallet · Catalog · Account. Notification items | Open the linked object; mark all read | – | Seller events in the notification catalogue |
| SL-HELP | `TPL-CONTENT` | Help articles by topic with search; link to tickets | Open an article; contact support | P1 | SUP-10 |
| SL-TICKET-LIST | `TPL-LIST` | Tickets: number, subject, status, last update | New ticket; open | P1 | SUP-4 |
| SL-TICKET-NEW | `TPL-FORM` | Topic, related order or offer (picker), description, attachments | Submit | P1 | SUP-1 |
| SL-TICKET | `TPL-DETAIL` | Conversation, status, related object | Reply; attach; mark resolved | P1 | SUP-4 |
| SL-SUSPENDED | `TPL-DETAIL` | The state (restricted, suspended, closing, closed), the reason category and what it affects; what remains available; how to appeal or contact support; wallet status (frozen or not) | Contact support through `SF-ST-CONTACT` (seller topic) or the support email until seller tickets ship (SUP-10; appeals go through Support at launch; the appeal page is P1); continue to the dashboard (read-only except SLA-7 actions); for `CLOSED`, only the history export | Landing page for suspended and closing sellers | Seller states, SEL-3, SEL-4 |
