# Customer Support & Content Management

**Authoritative for:** support tickets and SLAs, static and legal pages, CMS-managed content, third-party marketing tags.
**Related:** [admin-governance](../05-trust/admin-governance.md) · [compliance-legal](../05-trust/compliance-legal.md) · [web-apps](../07-clients/web-apps.md)

---

## 1. Support

- SUP-1 Support at launch is ticket-based (no live chat). Arabic and English.
- SUP-2 Tickets are created from the Contact page (guests and customers), from an order, return or dispute page (pre-linked), and from the Seller Dashboard help area.
- SUP-3 Categories: order, payment, delivery, return or refund, account, seller, report, other. The category routes the ticket to a queue.
- SUP-4 States: `OPEN → IN_PROGRESS ⇄ WAITING_ON_REQUESTER → RESOLVED → CLOSED` (auto-close `cfg:support.auto_close_days` (default 7) after `RESOLVED`; the requester can reopen before then).
- SUP-5 Targets: first response within `cfg:support.customer_first_response_hours` (default 24) for customers and `cfg:support.seller_first_response_hours` (default 12) for sellers; breach alerts the queue owner.
- SUP-6 Agents can assign, respond, add internal notes, attach files, escalate to another role and link to orders, returns, disputes and risk cases.
- SUP-7 Agents see only the data their role permits; viewing a requester's full phone number or address is logged.
- SUP-8 Attachments go through the media pipeline (scanning included).
- SUP-9 A satisfaction survey after resolution is P1. Live chat and WhatsApp support are out of scope for v1.0.
- SUP-10 The seller help centre (articles), seller tickets and performance appeals are P1 in the Seller Dashboard; until then sellers use the Contact form and email.
- SUP-11 Customers and sellers who contact Nyazek by phone or by reply to an email are served through the same ticket system: the agent creates the ticket on the caller's behalf after verifying them ([admin-panel](../05-trust/admin-panel.md) ADM-6). Whether Nyazek publishes an inbound phone line at launch, and its hours, is decision D-45.

## 2. Static and legal pages

Fourteen pages are live at launch in Arabic and English, managed in the CMS with version history:

About Us · Contact Us · FAQ (Customers) · FAQ (Sellers) · Terms & Conditions · Privacy Policy · Cookie Policy · Return & Refund Policy · Shipping Policy · Customer Protection Policy · Dispute Resolution Policy · Seller Agreement · Prohibited & Restricted Items Policy · Report a Listing / Intellectual Property Notice.

- CMS-1 Every page footer shows the legal entity name, commercial registration and e-commerce licence number ([compliance-legal](../05-trust/compliance-legal.md) §3).
- CMS-2 Legal documents are versioned and held per market. Acceptance of the Terms (customers) and the Seller Agreement (sellers) is recorded with document version and timestamp; a material change requires re-acceptance at next sign-in.
- CMS-3 Legal text is drafted by counsel; engineering supplies the publishing mechanism only.

## 3. CMS-managed content

| Content | Editor | Priority |
|---|---|---|
| Home page sections: hero banners, category grid, product rows (New Arrivals, Best Sellers, Top Rated, Deals) | Content Manager | P0 |
| Banners and announcement bar | Content Manager | P0 / P1 |
| Campaign landing pages | Marketing and Content | P1 |
| Email, SMS and push templates | Content Manager | P0 |
| Help-centre articles (customer and seller) | Content Manager | P1 |
| Static and legal pages | Content Manager (legal text from counsel) | P0 |

- CMS-4 Content is built from structured blocks with Arabic and English fields, scheduling (start and end), preview and publish, and rollback to a previous version.
- CMS-5 Rich text passes the same server-side sanitiser as seller content.
- CMS-6 The CMS is a module of the platform (no separate CMS product), edited in the Admin Panel.
- CMS-7 Home product rows are computed, not hand-picked; the Content Manager places, orders or hides them. New Arrivals: products first published within `cfg:content.new_arrivals_days` (default 30), newest first. Best Sellers: the sales-popularity signal ([search-buy-box](search-buy-box.md) §1.4). Top Rated: Bayesian rating, products with at least `cfg:content.top_rated_min_ratings` (default 5) ratings. Deals: products whose Buy Box offer has an active deal. Each row's "See all" opens the search listing with the matching sort or filter.

## 4. Third-party tags

- Google Tag Manager with GA4 and Meta Pixel (P0); TikTok Pixel (P1). Snapchat Pixel is out of scope.
- Tags load only on the Storefront and only after consent through the cookie banner (consent mode). No marketing tags run on the Seller Dashboard or Admin Panel.
- No personal data (email, phone, name, address) is placed in the data layer; purchase events carry order value and item IDs only.
- The Storefront's content-security policy lists the permitted tag domains explicitly.

## 5. Acceptance criteria

- A ticket created from an order page is linked to that order and visible to the right queue.
- Publishing a new version of the Terms forces re-acceptance and records it.
- With consent declined, no request is made to any marketing-tag domain.
