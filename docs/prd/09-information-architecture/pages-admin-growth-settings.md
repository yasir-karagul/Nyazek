# Admin Panel Pages: Marketing, Moderation, Support, Content, Analytics, Compliance, Settings

**Authoritative for:** the content and actions of these Admin Panel pages.
**Read with:** [README](README.md) §2 · [navigation](navigation.md) §3 · [admin-panel](../05-trust/admin-panel.md) · [sitemap](sitemap.md) §8.9–8.12
**Rules live in:** [pricing-promotions](../02-commerce/pricing-promotions.md) · [loyalty](../02-commerce/loyalty.md) · [advertising](../02-commerce/advertising.md) · [reviews-qa](../02-commerce/reviews-qa.md) · [support-cms](../02-commerce/support-cms.md) · [notifications-messaging](../02-commerce/notifications-messaging.md) · [data-analytics](../06-platform/data-analytics.md) · [privacy-audit](../05-trust/privacy-audit.md) · [admin-governance](../05-trust/admin-governance.md) §5 · [configuration-register](../00-governance/configuration-register.md)

---

## 1. Promotions, loyalty and ads

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-PRO-COUPONS | `TPL-LIST` and `TPL-FORM` | Platform coupons: code, discount, conditions, budget and spend, redemptions, dates, state. Form: code, type, value, cap, minimum spend, eligible categories or sellers, audience (all, new customers, segment), limits, budget, dates | Create; pause; end | P1; budget and funding shown; high-value coupons under dual control | PRM-1 to PRM-5 |
| AD-PRO-APPROVALS | `TPL-QUEUE` | Seller coupons awaiting approval: seller, terms, estimated cost to the seller | Approve; reject with a reason | P1 | PRM-2 |
| AD-PRO-FLASH | `TPL-LIST` and `TPL-FORM` | Deal windows with their products, deal prices, stock limits, results | Create a window; add or remove products; reorder | P1; deal prices validated against the reference-price rule | [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| AD-PRO-CAMP | `TPL-LIST` and `TPL-FORM` | Campaigns: name, dates, landing content, participation rules, funding split, participating sellers and offers | Create; open to sellers; lock; publish | P1 | [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| AD-PRO-PRICING | `TPL-SETTINGS` | 1P pricing rules: margin floor alert threshold by category (PRC-8) | Edit | 1P Merchandiser | PRC-8 |
| AD-LOY-CONFIG | `TPL-SETTINGS` | Earn and redeem rates, tier thresholds and benefits, expiry, referral rewards and limits | Edit (dual control for rates) | P1 | LOY-1 to LOY-14 |
| AD-ADS-HOME | `TPL-DASH` | Ad revenue, active campaigns and sellers, fill rate, click-through, invalid-click rate | Change period | P1 | [advertising](../02-commerce/advertising.md) |
| AD-ADS-SPONSORED | `TPL-SETTINGS` | Placements (search, category, product page, home row): slots, minimum bid, relevance threshold, labelling | Edit | P1 | AD-1 to AD-6 |
| AD-ADS-MOD | `TPL-QUEUE` | Campaigns and products flagged by policy checks; invalid-click clusters with the credit to issue | Approve, pause, reject; issue an invalid-click credit | P1 | Ad policy |

## 2. Reviews, Q&A and support

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-REV-QUEUE | `TPL-QUEUE` | Tabs: Flagged by pre-screen · Reported · Published · Removed. Review text and photos, product, order facts (verified purchase, returned), pre-screen reasons, reporter and reason | Publish; remove with a reason code; remove a photo only | Reviews are never edited by staff; the customer is told when one is removed and why | Moderation table, REV-5 to REV-7 |
| AD-REV-RULES | `TPL-SETTINGS` | Pre-screen rules: blocked words and patterns in both languages, contact-detail detection, thresholds | Edit; test against sample text | P1 | [reviews-qa](../02-commerce/reviews-qa.md) §3 |
| AD-QA-QUEUE | `TPL-QUEUE` | Questions and answers flagged or reported | Publish; remove with a reason | P1 | Q&A rules |
| AD-SUP-LIST | `TPL-QUEUE` | Tabs: Open · In progress · Waiting for requester · Resolved · Closed. Columns: ticket number, requester type (customer, seller, guest), topic, subject, linked object, assignee, time to first-response and resolution targets | Claim; create a ticket on a caller's behalf (ADM-6) | – | SUP-1 to SUP-11 |
| AD-SUP-DETAIL | `TPL-DETAIL` | Conversation (public replies and internal notes distinguished); requester summary and recent orders; linked order, return or dispute with shortcuts; canned replies in both languages | Reply; add an internal note; change topic, priority or assignee; link an object; escalate to another role's queue; resolve | Agents see only what their role permits; reveals are logged | SUP-4 to SUP-9 |
| AD-NOT-LOG | `TPL-LIST` | Messages sent: time, recipient (masked), channel, template, related object, provider status (queued, sent, delivered, failed with reason) | Resend a transactional message; open the related object | Message bodies containing codes or links are never shown | NTF-5, NTF-6 |

## 3. Content

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-CMS-HOME | `TPL-FORM` | The home page sections in order, each with its settings (banners in a carousel, category grid selection, product-row definitions, trust strip text); preview in both languages and at mobile and desktop widths | Add, remove, reorder, schedule, publish | Publishing is versioned and can be rolled back | CMS-4 |
| AD-CMS-BANNERS | `TPL-LIST` and `TPL-FORM` | Banners: placement, images per language and breakpoint, alternative text, link, schedule, state | Create, schedule, end | Images pass the media checks; a banner without an image for a language is not shown in that language | CMS-4 |
| AD-CMS-PAGES | `TPL-LIST` and `TPL-FORM` | Static and legal pages: title, slug (fixed for the launch set), state, version, effective date. Editor with content blocks in both languages | Edit; preview; publish a new version; for legal pages, mark whether re-acceptance is required | Legal pages need the Compliance role to publish; old versions are kept | CMS-1 to CMS-5 |
| AD-CMS-ANNOUNCE | `TPL-LIST` and `TPL-FORM` | Announcement-bar messages with link and schedule | Create, schedule, end | P1 | – |
| AD-CMS-HELP | `TPL-LIST` and `TPL-FORM` | Help articles for customers and for sellers: topic, title, body in both languages, state | Create, edit, publish | P1 | SUP-10 |
| AD-CMS-EMAIL | `TPL-LIST` and `TPL-FORM` | Email templates per event: subject and body in both languages with the event's variables listed; preview with sample data | Edit; send a test to oneself | Variables are fixed by the event; unknown variables are rejected; transactional templates cannot contain promotion | Notification catalogue |
| AD-CMS-SMS | `TPL-LIST` and `TPL-FORM` | SMS templates per event with character and segment count per language; sender ID; registration status with carriers | Edit | A template change that needs carrier re-registration is flagged and not sent until approved | [notifications-messaging](../02-commerce/notifications-messaging.md) §2 |
| AD-CMS-PUSH | `TPL-LIST` and `TPL-FORM` | Push templates per event: title, body, deep link | Edit | P1; no personal data in payloads | MOB-8 |
| AD-NOT-CAMP | `TPL-LIST` and `TPL-WIZARD` | Promotional campaigns: audience (segment, with the count after consent and frequency-cap filtering), channel, content, schedule, results | Create; schedule; cancel | P1; only opted-in recipients; quiet hours enforced | NTF-1, NTF-2, NTF-4 |

## 4. Analytics and compliance

Analytics pages use `TPL-DASH` with a period selector, comparison to the previous period, filters (category, governorate, seller type) and export under the export rules (ADM-5). Definitions are in [data-analytics](../06-platform/data-analytics.md) §4.

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-AN-HOME | `TPL-DASH` | The platform KPIs of [overview-vision-kpis](../01-product/overview-vision-kpis.md) §5: GMV, orders, monthly active customers, active sellers, conversion, AOV, cancellation, delivery success, return rate | Open a detail page | Widgets by role | DAT-4 |
| AD-AN-SALES | `TPL-DASH` | Sales over time; by category, governorate, seller type, payment method | Export | – | – |
| AD-AN-USERS | `TPL-DASH` | New and returning customers, registration to first order, repeat rate, by governorate and channel | Export | Aggregates only; no personal data | – |
| AD-AN-SELLERS | `TPL-DASH` | Active sellers, onboarding funnel, level distribution, top and at-risk sellers | Open a seller | – | – |
| AD-AN-CATS | `TPL-DASH` | Category sales, share, growth, return rate, stock coverage | Export | – | – |
| AD-AN-SEARCH | `TPL-LIST` | Top queries, queries with no results, low click-through queries; synonym suggestions | Add a synonym (to `AD-SET-RANK`) | – | [search-buy-box](../02-commerce/search-buy-box.md) §1.2 |
| AD-AN-PAY | `TPL-DASH` | Success rate, time to confirm, failures by reason, per method and provider | – | P1 | – |
| AD-AN-LOG | `TPL-DASH` | Delivery times, on-time rate, failed-delivery and RTO rates by courier and governorate | – | P1 | – |
| AD-PRIV-REQ | `TPL-QUEUE` | Data-subject requests: type (access, export, correction, erasure), requester, received, deadline, state; blockers for erasure | Verify identity; fulfil (export file generated; erasure executed after checks); reject with a reason; log an authority request (DSR-4) | Compliance manages; Support and Super Admin read ([admin-governance](../05-trust/admin-governance.md) §2.1) | DSR-1 to DSR-4 |
| AD-AUDIT | `TPL-LIST` | Audit records: time, actor (person, system, agent), action, object, before and after (sensitive values masked), reason, correlation ID. Filters by actor, action, object, date | Open the object; export under approval | Read-only for everyone; viewing is itself logged | AUD-1 to AUD-6 |

## 5. Settings

All use `TPL-SETTINGS`: each value shows its current setting, default, owner role, effective-from date, pending change if any, and its change history. The values, defaults and owners are in the [configuration-register](../00-governance/configuration-register.md); the page for a value is the page whose group matches its key. Values flagged for dual control create an approval request (FL-14).

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| AD-SET-GENERAL | `TPL-SETTINGS` | Platform name, legal entity details shown in the footer and on documents, support contacts, social links | Edit | – | CMS-1 |
| AD-SET-LOCAL | `TPL-SETTINGS` | The market's settings: languages, currency table entry (exponent, price step, display format), time zone, digits, phone ranges | Edit | – | MON-7, MON-8, MKT-8 |
| AD-SET-GEO | `TPL-LIST` and `TPL-FORM` | The address reference data: level names, governorates, districts, neighbourhoods with names in both languages and codes; import | Add, rename, deactivate, import | Codes are stable; a deactivated area stays on past orders | ADR-5, D-32 |
| AD-SET-CALENDAR | `TPL-LIST` and `TPL-FORM` | Platform holidays and force-majeure declarations: dates, governorates affected, which clocks pause | Add, end | Super Admin; audited; sellers and customers are informed where it affects estimates | SLA-1, ADM-11 |
| AD-SET-SHIP | `TPL-SETTINGS` | Zones, rate card by weight band, bulky and remote surcharges, free-delivery threshold, COD fee | Edit (dual control) | A simulator shows the fee for a sample parcel and route | FEE-1 to FEE-5, D-21 |
| AD-SET-TAX | `TPL-SETTINGS` | Tax regions, categories and rates; inclusive or exclusive display; document texts | Edit (dual control, Finance) | Zero in Iraq at launch | TAX-1 to TAX-6 |
| AD-SET-PAY | `TPL-SETTINGS` | Payment methods: enabled, order, limits, customer-facing note; provider status and health; circuit-breaker state | Enable, disable, reorder | Credentials are never shown or entered here: they live in the secret store | PAY-12 |
| AD-SET-COMM | `TPL-SETTINGS` | Commission schedule by product type, sub-category and top-level category (COM-2) with effective dates; no seller-specific rates at launch | Schedule a change (dual control; effective no earlier than the notice period, COM-3) | The public fees page reflects the schedule in force | COM-1 to COM-5 |
| AD-SET-PRICE | `TPL-SETTINGS` | Price floor, anti-dumping percentage, MAP enforcement mode, reference-price period | Edit | – | PRC-1 to PRC-10 |
| AD-SET-LIMITS | `TPL-SETTINGS` | Listing caps by seller age and level; media limits | Edit | – | Listing caps |
| AD-SET-SLA | `TPL-SETTINGS` | Seller confirmation and hand-over times, escrow hold, order and payment timers, stuck-state alert times | Edit (dual control for escrow and order timers) | – | SLA-1 to SLA-6, ORD-16, escrow rules |
| AD-SET-RETURNS | `TPL-SETTINGS` | Return window, change-of-mind allowed, non-returnable flag and evidence requirement by category; return-shipping rules; response and inspection times | Edit | Changes apply to new orders only (RET-6), stated on the page | RET-1 to RET-6 |
| AD-SET-RANK | `TPL-SETTINGS` | Buy Box weights and hysteresis; search ranking weights; synonyms and dialect terms; pinned results | Edit (weights under dual control); preview the effect on sample queries and products | – | [search-buy-box](../02-commerce/search-buy-box.md) §1.2, §2.3, BBX-3 |
| AD-SET-LOYALTY | `TPL-SETTINGS` | Programme on or off; the values of `AD-LOY-CONFIG` grouped for Super Admin | Edit | P1 | LOY-14 |
| AD-SET-NOTIF | `TPL-SETTINGS` | Quiet hours, frequency caps, channel fallback order, sender IDs | Edit | – | NTF-2, NTF-4 |
| AD-SET-INTEG | `TPL-LIST` | Integrations (PSPs, couriers, SMS, email, push, storage, monitoring): environment, status, last successful call, credential age and rotation due date | Test a connection; start a credential rotation (which is completed in the secret store) | No secret is ever displayed | SEC secrets rules |
| AD-SET-APP | `TPL-SETTINGS` | Minimum and recommended app versions per platform, maintenance mode with message and schedule, feature flags with their audience | Edit; turn maintenance on (confirmation) | Maintenance mode leaves the Admin Panel reachable | API-6 |
| AD-SET-SEC | `TPL-SETTINGS` | Admin session lengths, password policy, 2FA requirements, access-layer status | Edit (Super Admin, dual control) | – | SES-2, AUTH-6, [security](../05-trust/security.md) |
| AD-SYS-HEALTH | `TPL-DASH` | Job queues (depth, oldest job), outbox age, dead-lettered jobs with reason, provider circuit states, scheduled-job results | Retry or discard a dead-lettered job with a reason | P1; Super Admin | EVT-8, job rules |
