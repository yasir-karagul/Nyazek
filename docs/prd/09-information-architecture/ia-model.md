# IA Model: Principles, Objects, URLs, Templates

**Authoritative for:** IA principles, the navigable objects, URL and state rules, page templates, global page states, responsive behaviour by template.
**Related:** [README](README.md) · [sitemap](sitemap.md) · [navigation](navigation.md) · [web-apps](../07-clients/web-apps.md) · [design-system-ui-workflow](../07-clients/design-system-ui-workflow.md)

---

## 1. Principles

| ID | Principle |
|---|---|
| IA-1 | **Three applications, three mental models.** The Storefront is organised around products and the customer's own orders; the Seller Dashboard around the seller's daily work queue; the Admin Panel around roles and queues. They never share navigation, sessions or shells. |
| IA-2 | **One object, one home.** Every object (§2) has one canonical page per application. Other pages link to it; they do not re-present it in full. |
| IA-3 | **The next action is on the page.** A page that shows something waiting on the user (an order to confirm, a return to hand over, a queue item) shows the action and its deadline, without sending the user elsewhere to find it. |
| IA-4 | **Arabic first.** Structures are designed right-to-left and for Arabic text length, then verified in English. Nothing is positioned by left or right. |
| IA-5 | **Phone first for customers and sellers.** Storefront and Seller Dashboard pages are designed at 360 px first. The Admin Panel is desktop-first (ADM-12). |
| IA-6 | **Clients display; the API decides.** No page computes a price, a total, an eligibility or an allowed action. Pages show what the API returns and offer the actions it says are available (ARC-6). |
| IA-7 | **Same names everywhere.** A thing has one name in every application, document, message and notification ([taxonomy-and-labels](taxonomy-and-labels.md)). |

## 2. Objects people navigate

| Object | Customer sees it at | Seller sees it at | Staff see it at | Identifier in URLs |
|---|---|---|---|---|
| Category | `SF-CATEGORY` | Picker in catalog forms | `AD-CAT-CATS` | Slug path |
| Brand | `SF-BRAND` (P1), filter | Picker | `AD-CAT-BRANDS` | Slug |
| Product and its variants | `SF-PDP` | Search result in `SL-CAT-OFFER-NEW` | `AD-CAT-PRODUCT` | Slug with short ID |
| Offer | Buy Box and "Other sellers" on `SF-PDP` | `SL-CAT-OFFERS` | Inside product and seller pages | Opaque ID |
| Store (seller) | `SF-STORE` | `SL-SET-STORE` | `AD-USR-SELLER` | Seller slug |
| Cart, checkout session | `SF-CART`, `SF-CHK-*` | – | – | None (one per customer) |
| Order | `SF-ORD-DETAIL` | – (sellers see sub-orders) | `AD-ORD-DETAIL` | Order number |
| Sub-order and its shipment | Block inside the order; `SF-ORD-TRACK` | `SL-ORD-DETAIL` | Block inside `AD-ORD-DETAIL` | Sub-order number |
| Return | `SF-RET-DETAIL` | `SL-RET-DETAIL` | `AD-RET-DETAIL` | Opaque ID |
| Dispute | `SF-DISP-DETAIL` | `SL-DISP-DETAIL` | `AD-DISP-DETAIL` | Opaque ID |
| Refund | Inside order, return and dispute pages | Wallet movement | `AD-FIN-REFUNDS` | – |
| Review, seller rating | Product and store pages; `SF-REV-*` | `SL-REV` | `AD-REV-QUEUE` | – |
| Address, refund account | `SF-ADDR`, `SF-REFACC` | Pickup addresses in `SL-SET-PICKUP` | Masked inside detail pages | – |
| Notification | `SF-NOTIF` | `SL-NOTIF` | Admin inbox in the top bar | – |
| Wallet movement, payout, commission invoice | – | `SL-WAL-*` | `AD-FIN-*` | Opaque ID |
| Receipt, credit note | Download on the order | Download on the sub-order | `AD-FIN-DOCS` | Document number |
| KYC application | – | `SL-ONB-*`, `SL-ACC-KYC` | `AD-SEL-KYC-CASE` | Opaque ID |
| New-product request | – | `SL-CAT-REQ-*` | `AD-CAT-REQUEST` | Opaque ID |
| Support ticket | Contact form; email thread | `SL-TICKET` (P1) | `AD-SUP-DETAIL` | Ticket number |
| Risk case, reconciliation exception, approval request | – | – | `AD-RISK-CASE`, `AD-FIN-RECON`, `AD-APPROVALS` | Opaque ID |

## 3. URL and state rules

- IA-8 Routes are those in the [sitemap](sitemap.md). A route never changes without a permanent redirect from the old one.
- IA-9 Storefront: Arabic at the root and English under `/en`, same paths. Seller Dashboard and Admin Panel have no language prefix; language is an account setting.
- IA-10 Slugs: Latin characters, lower case, hyphens. Product: `/product/<title-slug>-<shortId>`, where the short ID is what identifies the product and the title part is cosmetic; a request with a wrong or outdated title part is redirected permanently to the canonical URL. Category and brand slugs are unique names set by the Catalog Manager; store slugs are unique and derived from the store name (SEL-6). Changing a slug leaves a redirect, and former slugs are never reassigned.
- IA-11 Orders and sub-orders appear in URLs by their public numbers (ORD-1). Every other object uses an opaque ID. No URL contains a phone number, an email or a name.
- IA-12 **List state lives in the query string**: active tab (`tab`), search text (`q`), filters, sort (`sort`) and page or cursor. Reloading, sharing or going back restores the same view. Default values are omitted from the URL.
- IA-13 A page that needs sign-in redirects to the application's login with `returnTo` set to the requested path; after sign-in the user lands there. `returnTo` accepts only same-origin relative paths.
- IA-14 Modals, drawers and in-page actions have no route. Closing one returns to the page beneath with its state intact. A destructive or money-moving action always asks for confirmation in a dialog that restates the object and the consequence.
- IA-15 Each page has one level-one heading equal to its name, and a document title of the form `<page or object name> | Nyazek`. Index and canonical rules are in [web-apps](../07-clients/web-apps.md) §4.3.
- IA-16 The same route always shows the same kind of content. What differs by state (for example a restricted seller) is shown inside the page or by redirecting to a state page, never by silently swapping in another page.

## 4. Storefront search and listing parameters

Used by `SF-SEARCH`, `SF-CATEGORY`, `SF-BRAND`, `SF-STORE` and deal pages.

| Parameter | Values | Notes |
|---|---|---|
| `q` | Text | Search page only; trimmed; empty redirects to home |
| `brand` | One or more brand slugs | Repeated parameter |
| `price_min`, `price_max` | Integers in the market currency | |
| `seller_type` | `1p`, `3p` | |
| `rating` | `4`, `3`, `2` | Minimum average rating |
| `in_stock` | `1` | Default off: out-of-stock results are shown last (SRC-4) |
| `condition` | `new`, `open_box`, `refurbished` | Used not enabled at launch (D-44) |
| `gov` | Governorate code | Defaults to the "Deliver to" selection ([navigation](navigation.md) §1.1) |
| `speed` | `next_day`, `standard` | P1 |
| `attr.<code>` | Attribute value codes | Only attributes flagged filterable for the category |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, `newest`, `best_selling`, `rating` | |
| `page` | 1 to the depth cap | Numbered for canonical URLs |
| `view` | `grid` (default), `list` | Remembered on the device |

Changing a filter resets `page`. Filter counts (facets) come from the API with each response. Unknown parameters are ignored; invalid values are dropped, not errors.

## 5. Page templates

A page specification names one template, or a template variant below. It names two when a list page also hosts the create and edit form, or the detail, of its own records in a drawer or on a sub-route without a Page ID of its own (IA-14); the first template governs the page and the second the drawer or sub-route. The template's regions and behaviour apply unless the specification says otherwise.

| Template | Used for | Regions, in order | Behaviour |
|---|---|---|---|
| `TPL-LISTING` | Storefront product listings | Breadcrumb · title and result count · filter panel (side on desktop, drawer on mobile) with applied-filter chips · sort and view controls · product grid · pagination | Parameters per §4; skeleton cards while loading; no-results state with suggestions; filters stay visible when there are no results |
| `TPL-LIST` | Lists of records in account, seller and admin pages | Title and primary action · tabs · search and filters · table (cards on mobile) · bulk-action bar when rows are selected · pagination | State in the query string (IA-12); row opens the detail page; empty state per tab with a reason and, where it helps, an action; default sort newest first unless stated |
| `TPL-QUEUE` | Admin work queues | As `TPL-LIST`, plus age and time-to-target on every row and a claim control | Sorted oldest-at-risk first; claim and release; item opens a decision view (ADM-1, ADM-2) |
| `TPL-DETAIL` | One object | Header (identifier, status chip, primary actions) · summary · sections or tabs · timeline or history · related objects | Actions shown are those the API reports as allowed; a stale page that attempts a disallowed action shows the API's message and refreshes |
| `TPL-FORM` | Create or edit on one screen | Title · grouped fields with labels and help · submit and cancel | Inline validation on blur and on submit; API field errors mapped to fields; unsaved-changes warning on leaving; submit disabled while in flight; success returns to the origin page with a toast |
| `TPL-WIZARD` | Multi-step creation | Step indicator · one step's fields · back and next · final review step | Each step saves a draft; the user can leave and resume; steps can be revisited before submission; the review step shows everything entered |
| `TPL-DASH` | Home and overview pages | Greeting or context line · key figure cards · action list · secondary widgets | Every figure links to the list it summarises, pre-filtered; figures show their period |
| `TPL-SETTINGS` | Platform and store settings | Title · explanation · grouped settings · save · change history (admin) | Admin settings show the current value, the value pending approval if any, and effective-from; settings under dual control create an approval request instead of saving (DC-1) |
| `TPL-AUTH` | Sign-in, registration, verification, recovery | Logo · title · one short form · secondary links | No header navigation or footer menus; uniform responses (AUTH-1); rate-limit and lock messages |
| `TPL-CONTENT` | Static, legal and help pages | Breadcrumb · title · last-updated date and version (legal pages) · content blocks · related links | Content from the CMS; printable |
| `TPL-LIST` (cards) | Lists of a few records best read as cards (addresses, payment destinations, coupons, favourites) | As `TPL-LIST`, with cards at every width instead of a table | As `TPL-LIST` |
| `TPL-LIST` (editable grid) | Bulk editing of many rows | As `TPL-LIST`, with the Data table in its editable-grid variant | Each cell validates on change; "save all" sends the changes in one request; rows that fail keep the old value and show why |
| `TPL-LIST` (matrix) | Two-dimensional settings (for example areas by courier) | Row and column headers, one editable cell per pair | As the editable grid |
| `TPL-LIST` (tree) | Hierarchies (category tree) | Expandable tree with search; node selection opens its form | Reordering and moving are actions on the node |
| `TPL-DETAIL` (decision view) | Admin decisions on one case (KYC, product request, dispute, risk case) | As `TPL-DETAIL`, with the evidence beside the object and a decision panel: outcomes, reason codes (ADM-2), note, and the second-person step where dual control applies | Claim state from the queue is shown; the decision panel lists only the outcomes the API allows |
| `TPL-LISTING` (store header) | A seller's store page | Store header (name, logo, rating, policies link) above the `TPL-LISTING` regions | As `TPL-LISTING`, scoped to the store |
| Dedicated layout | Pages whose layout is specified in full in their specification (home, product detail, cart, order confirmation) | As specified | The specification states its empty states and guards; loading and request errors follow §6 for each section or region |
| `TPL-SYSTEM` | Error and state pages | Illustration or icon · one-line explanation · one or two actions | See [pages-system](pages-system.md) |

## 6. States every page handles

| State | Behaviour |
|---|---|
| Loading | Skeleton of the template's regions; no spinner-only pages; no layout shift when content arrives |
| Empty | A sentence saying why it is empty and, where there is one, the action that would fill it |
| Error (request failed) | Inline error with a retry action and the correlation ID; the rest of the page stays usable |
| Not found or not yours | The application's not-found page (the API does not reveal that a resource exists: SEC-2) |
| Permission denied | For staff roles: a page saying which permission is needed; the navigation never offered the link |
| Session expired | The session-expired page with `returnTo`; entered form data is kept where the browser allows |
| Offline or timeout | A banner; actions that change data are disabled until the connection returns; no optimistic changes for money or order state |
| Maintenance | The maintenance page from app configuration |
| Language and direction | Every page in Arabic (right-to-left) and English (left-to-right) at worst-case text length |

## 7. Responsive behaviour

Breakpoints are the design system's (360, 768, 1280 px).

| Element | 360–767 | 768–1279 | 1280 and above |
|---|---|---|---|
| Storefront navigation | Compact header, bottom bar, drawers | Full header, no bottom bar | Full header with mega menu |
| Listing filters | Drawer opened from a "Filter" button with a result count on its apply button | Collapsible side panel | Side panel |
| Product grid | 2 columns | 3 columns | 4 to 5 columns |
| Tables in `TPL-LIST` | Cards, one record each, key fields only, actions in a menu | Table with fewer columns | Full table |
| Detail pages | Single column; actions in a sticky bottom bar | Two columns | Two columns with a side panel |
| Seller navigation | Bottom bar and "More" drawer | Collapsed sidebar (icons) | Full sidebar |
| Admin navigation | Not targeted | Collapsible sidebar | Full sidebar |
