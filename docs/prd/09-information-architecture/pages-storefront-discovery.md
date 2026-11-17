# Storefront Pages: Shell, Discovery, Favourites, Cart

**Authoritative for:** the content and actions of the Storefront shell components and the public browse pages.
**Read with:** [README](README.md) §2 (how to read a specification) · [ia-model](ia-model.md) (templates, parameters) · [navigation](navigation.md) §1 · [shared-components](shared-components.md) · [sitemap](sitemap.md) §2–3
**Rules live in:** [search-buy-box](../02-commerce/search-buy-box.md) · [catalog-listings](../02-commerce/catalog-listings.md) · [pricing-promotions](../02-commerce/pricing-promotions.md) · [checkout-orders](../02-commerce/checkout-orders.md) §2 · [customer-account](../02-commerce/customer-account.md) · [web-apps](../07-clients/web-apps.md) §4

---

## 1. Shell components

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-SH-HEADER | – | As [navigation](navigation.md) §1.1 | As listed there | Reduced variant in checkout; sign-in state, cart count and favourites count load on the client so cached pages stay anonymous | [web-apps](../07-clients/web-apps.md) §4.2 |
| SF-SH-MEGAMENU | – | As [navigation](navigation.md) §1.2 | Open a category | Categories without live products are hidden | [catalog-listings](../02-commerce/catalog-listings.md) §2 |
| SF-SH-FOOTER | – | As [navigation](navigation.md) §1.5 | Links; reopen cookie settings | Legal identity lines are mandatory and come from general settings | CMS-1 |
| SF-SH-CONSENT | – | Short explanation, link to the cookie policy; choices: accept all, reject non-essential, choose by purpose (analytics, marketing) | Save choice | Shown until a choice is made and again when the policy version changes; marketing tags load only after consent; does not block reading the page | [privacy-audit](../05-trust/privacy-audit.md) §2 |
| SF-SH-CART | – | Drawer: cart lines (compact), items subtotal, free-delivery progress, "View cart" and "Checkout" | Change quantity, remove, go to cart, go to checkout | Empty state with a link to home; flags on lines as in the cart page | CRT-2 |
| SF-SH-SEARCH | – | As [navigation](navigation.md) §1.7 | Pick a suggestion, submit a search, clear recent searches | Suggestion failure degrades to plain submit | [search-buy-box](../02-commerce/search-buy-box.md) §1 |
| SF-SH-TOAST | – | One message at a time, queueing; announced to screen readers | Dismiss; optional single action ("View cart", "Undo" for remove-from-favourites) | Errors that need a decision are never toasts | – |
| SF-SH-ANNOUNCE | – | One line of CMS text with an optional link; scheduled | Dismiss for the visit | Hidden in checkout | CMS-4 |
| SF-SH-PWA | – | Prompt to install the web app | Install, not now | Never during checkout; P2 | – |

## 2. Home

### SF-HOME — Home

- **Template:** dedicated layout (CMS-composed). Sections render in the order set in the CMS; the default order is below.
- **Content:**
  1. Hero banner carousel: the scheduled banners (CMS-4, at most `cfg:content.home_banners_max`, CMS-7), each an image per language and breakpoint with a link (category, campaign, product, store or search). Auto-advance pauses on focus or touch; reduced-motion shows the first banner only.
  2. Category grid: the ten top-level categories with icon or image and name.
  3. Flash deals strip (P1): countdown and a carousel of deal products; link to `SF-DEAL-FLASH`.
  4. Product rows with tabs: New Arrivals · Best Sellers · Top Rated · Deals & Offers. One tab is shown at a time; each shows up to `cfg:content.home_row_cards` product cards (CMS-7) and "See all". The rows are computed per CMS-7; "See all" opens `SF-SEARCH` sorted by newest, best selling or rating, or filtered to deals.
  5. Sponsored row (P1), labelled.
  6. Featured brands (P1).
  7. Trust strip (CMS): cash on delivery, returns, verified sellers; each links to its policy page.
  8. Recently viewed (P2).
- **Actions:** open any linked destination; add to favourites from a card.
- **States and guards:** a section with no content is omitted, not shown empty. The page is cached and anonymous; personal elements load on the client.
- **Rules:** CMS-4 · "best sellers", "top rated" and "new arrivals" are computed from the search read model (SRC-2), not curated · AD-6.

## 3. Listings

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-SEARCH | `TPL-LISTING` | Title "Results for <query>" with count; corrected-query notice (P1); filters: category (tree with counts), price range, brand, seller type, rating, in stock, condition, deliver-to governorate, attributes common to the result set; product cards | Filter, sort, change view, paginate, open product, favourite | No results: the query, spelling tips, popular categories, and "did you mean" (P1); `noindex`; over-long or empty query redirects home | [search-buy-box](../02-commerce/search-buy-box.md) §1, [ia-model](ia-model.md) §4 |
| SF-CATEGORY | `TPL-LISTING` | Category banner (CMS, optional); sub-category pills (children of the current node); filters as search plus the category's filterable attributes; brand showcase (P1) | As search; open a sub-category | A category with children and no direct products still lists its descendants' products; unknown path → not found; a renamed slug redirects | [catalog-listings](../02-commerce/catalog-listings.md) §2 |
| SF-BRAND | `TPL-LISTING` | Brand logo, banner and description; authorised-distributor note where relevant; products of the brand | As search | Brand filter hidden; P1 | – |
| SF-DEAL-FLASH | `TPL-LISTING` | Countdown to the end of the current deal window; product cards with deal price, reference price, remaining-stock bar | Filter by category and discount; sort by time left or discount | Between windows: next start time; a sold-out deal card stays, marked sold out; P1 | [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| SF-CAMPAIGN | `TPL-LISTING` | Campaign banner and text (CMS); participating products | As search | Before start or after end: campaign unavailable page with a link home; P1 | [pricing-promotions](../02-commerce/pricing-promotions.md) §2 |
| SF-DEAL-DAILY | `TPL-LISTING` | Today's deals | As flash deals | P2 | – |
| SF-DEAL-CLEAR | `TPL-LISTING` | Clearance products | As search | P2 | – |

## 4. Product page

### SF-PDP — Product detail

- **Template:** dedicated layout.
- **Layout:** two columns from 768 px: media at the start side; purchase column beside it; full-width sections beneath. Below 768 px: single column with a sticky purchase bar (price, "Add to cart") once the main button scrolls out of view.
- **Content, purchase column, in order:**
  1. Breadcrumb; brand name (link to brand page when it exists); title; rating summary (compact, jumps to reviews); product code.
  2. Price block for the selected variant's Buy Box offer.
  3. Variant selector.
  4. Stock badge.
  5. Delivery estimate for the "Deliver to" governorate, with change.
  6. Quantity stepper; **Add to cart**; **Buy now**; favourite toggle; share (P1); "Notify me when back in stock" in place of the buttons when no offer is available (P1).
  7. Seller block (Buy Box winner) with the automatic-selection disclosure and a one-line return summary ("Returns within N days", or "Not returnable" with the reason category).
  8. Payment note: "Cash on delivery available" only when the API reports it for this customer and destination; otherwise the note is absent.
  9. "Other sellers (N) from <lowest price>", jumping to the offers list. Absent when there is one offer.
- **Content, sections beneath:**
  1. Offers list ("Other sellers").
  2. Tabs: Description (rich text view) · Specifications (attribute table in the category's schema order; warranty, origin, expiry or serial requirements where they apply) · Reviews (rating summary, sort by newest or most helpful, review cards with pagination) · Shipping & Returns (delivery estimate, fees summary, the return window and conditions for this product, link to the policies) · Q&A (P1).
  3. Similar products and sponsored alternatives (P1); frequently bought together and recently viewed (P2).
  4. "Report this listing".
- **Actions:**
  - *Add to cart* adds the selected offer and opens the cart drawer; at a limit, the reason is shown.
  - *Buy now* adds the selected offer if it is not already in the cart and goes to checkout with the whole cart.
  - Choosing an offer in the offers list adds that offer; `?offer=` pre-selects one and marks it "Selected seller".
  - Selecting a variant updates price, stock, media, delivery estimate, seller block and the URL (`?variant=`), without a full reload.
- **States and guards:**
  - No offer for the selected variant (BBX-7): "Currently unavailable", no price, alert sign-up (P1), other variants still selectable.
  - Unpublished product: "Not available", HTTP `404`, `noindex`. Archived product: "No longer available" and similar products, HTTP `410`, `noindex`. Taken down for a policy or legal reason: the generic notice only. Merged product: redirect to the survivor (CAT-10, CAT-12, [web-apps](../07-clients/web-apps.md) §4.3).
  - Seller-owned (Type C) listing: one seller, no offers list.
  - Hazardous or not deliverable to the selected governorate: delivery block says so; adding to cart is still allowed, and the address step decides (ADR-3).
  - Price, stock and Buy Box are fetched fresh or revalidated on change; the rest of the page is cached.
- **Rules:** [catalog-listings](../02-commerce/catalog-listings.md) §3–4, 8 · [search-buy-box](../02-commerce/search-buy-box.md) §2 · PRC-9 · [reviews-qa](../02-commerce/reviews-qa.md) · RET-6 · structured data per [web-apps](../07-clients/web-apps.md) §4.3

## 5. Store

### SF-STORE — Seller store page

- **Template:** `TPL-LISTING` (store header).
- **Content:** header with logo, banner, store name, verified and 1P badges, seller rating (or "New seller"), "Selling on Nyazek since <month year>"; tabs: **All products** (listing with filters; search within store at P1) · **Reviews** (seller ratings: summary and comments) · **About** (store description, return policy within platform rules, the seller's legal identity as required by regulation, CMS-1) · Featured, New arrivals, On sale (P1).
- **Actions:** browse, filter, open product, report store (P1).
- **States and guards:** a seller on vacation shows a notice and no purchasable offers; a suspended or closed seller's store returns the not-found page; an old store slug redirects (SEL-6).
- **Rules:** [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) §6 · REV-4 · [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) §6.1 (vacation)

## 6. Favourites and cart

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SF-FAV | `TPL-LIST` (cards) | Tabs: All · In stock · Price dropped. Product cards with current Buy Box price, availability, and for price drops the previous and current price | Remove (with undo), move to cart (single and bulk), open product | Guests see device favourites and a prompt to sign in to keep them; unavailable items stay, marked; list-full notice at the limit; `/wishlist` and `/account/favorites` redirect here | CUS-3 to CUS-9 |

### SF-CART — Cart

- **Template:** dedicated layout: lines on the start side, summary beside them (beneath on mobile, with a sticky checkout bar).
- **Content:**
  1. Lines grouped by seller, each group headed "Shipment from <seller>" so the customer sees that sellers ship separately. Each line is a cart line component.
  2. Notices at the top when anything changed since the last visit (price changes, items no longer available, replaced offers).
  3. Coupon field and loyalty redemption (P1).
  4. Quote summary (estimate) with the free-delivery progress; shipping shows "Calculated at checkout" until a governorate is known, then the estimate for the "Deliver to" governorate.
  5. **Checkout** button.
- **Actions:** change quantity, remove, move to favourites, accept or remove a replaced offer, apply or remove a coupon (P1), proceed to checkout, continue shopping.
- **States and guards:** empty cart shows a message and links to home and favourites; "Checkout" is disabled with the reason while any line is unavailable or over a limit; guests proceed without signing in (FL-1); every amount comes from the quote (CRT-5); two-device conflicts refresh the cart (CRT-6).
- **Rules:** [checkout-orders](../02-commerce/checkout-orders.md) §2 and §4 · [pricing-promotions](../02-commerce/pricing-promotions.md) §2 · FEE-2
