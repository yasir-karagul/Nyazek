# Navigation

**Authoritative for:** the navigation structure of each application: headers, menus, footer, sidebars, visibility by role and state, breadcrumbs, mobile navigation, links between applications.
**Related:** [sitemap](sitemap.md) · [ia-model](ia-model.md) · [taxonomy-and-labels](taxonomy-and-labels.md) §4 (labels) · [seller-dashboard](../03-sellers/seller-dashboard.md) §3 · [admin-governance](../05-trust/admin-governance.md) §2

- NAV-1 A navigation item is shown only if the user can open its page. Hiding is a convenience; the API is the control (RBAC-2).
- NAV-2 An item whose page is P1 or P2 does not appear until the page ships. No "coming soon" entries.
- NAV-3 The current section is marked in the navigation, and the marker is conveyed by more than colour.

---

## 1. Storefront

### 1.1 Header (`SF-SH-HEADER`)

Order of elements from the start side (right in Arabic):

| Element | Behaviour |
|---|---|
| Logo | Links to home |
| Categories button | Opens the mega menu (`SF-SH-MEGAMENU`) |
| Search field | Opens the search overlay (`SF-SH-SEARCH`) on focus; submitting goes to `SF-SEARCH` |
| Deliver to | Shows the selected governorate. Opens a picker of the 19 governorates. The choice is kept on the device for guests and defaults to the default address for signed-in customers. It drives delivery estimates, the `gov` filter default and "not deliverable" notices. It is not a serviceability guarantee: the address step is (ADR-3) |
| Language | Switches between Arabic and English on the same page |
| Favourites | Links to `SF-FAV`, with a count |
| Cart | Opens the cart drawer (`SF-SH-CART`); count of lines |
| Account | Guest: Sign in · Create account · Track an order. Signed in: first name, then the account menu (§1.4) and Sign out |

Above the header: the announcement bar (`SF-SH-ANNOUNCE`, P1), dismissible per visit. A secondary row on desktop: top-level categories as links, "Deals" (P1) and "Sell on Nyazek" (to `SF-SELL-LANDING`).

**Checkout header.** On `SF-CHK-*` pages the header is reduced to the logo, the step indicator with the checkout steps ([taxonomy-and-labels](taxonomy-and-labels.md) §5), and a help link; no search, menus or footer menus, so nothing pulls the customer out of checkout.

### 1.2 Mega menu (`SF-SH-MEGAMENU`)

- Desktop: a panel listing top-level categories; pointing at or focusing one shows its level-2 categories as column headings with their level-3 categories beneath, and a "View all in <category>" link. Opens on click or keyboard, not on hover alone.
- Mobile: a full-height drawer with drill-down (category → sub-categories → "View all"), a back control and the category name as title.
- Content comes from the category tree; only categories with at least one live product are shown. Order is set by the Catalog Manager.

### 1.3 Mobile bottom bar (below 768 px)

Home · Categories (opens the drawer) · Favourites · Cart (count) · Account (or Sign in). Hidden in checkout, on `TPL-AUTH` pages and when the on-screen keyboard is open. On `SF-PDP` it is replaced by the sticky purchase bar.

### 1.4 Account navigation (`/account/*`)

A side menu on desktop and a menu page (the account home) on mobile.

| Group | Items (page) |
|---|---|
| Overview | Account home (`SF-ACC-HOME`) |
| Orders | My orders (`SF-ORD-LIST`) · Returns (`SF-RET-LIST`) · Disputes (`SF-DISP-LIST`) · Reviews (`SF-REV-PENDING`, `SF-REV-DONE`) |
| Saved | Favourites (`SF-FAV`) · Addresses (`SF-ADDR`) · Refund accounts (`SF-REFACC`) · Saved cards (`SF-PAYM`, P1) |
| Rewards (P1) | Loyalty (`SF-LOY`) · Coupons (`SF-COUP`) |
| Inbox | Notifications (`SF-NOTIF`) · Messages (`SF-MSG`, P1) · My questions (`SF-QA-MY`, P1) |
| Settings | Personal information (`SF-PROF`) · Password (`SF-SEC-PW`) · Email and phone (`SF-SEC-EMAIL`) · Devices (`SF-SEC-DEV`) · Two-factor (`SF-SEC-2FA`, P1) · Linked accounts (`SF-SEC-LINK`) · Privacy (`SF-PRIV`) |
| – | Sign out |

An unclaimed (guest-created) account sees the same menu plus a "Set a password" prompt on the account home (CUS-1).

### 1.5 Footer (`SF-SH-FOOTER`)

| Column | Links |
|---|---|
| Nyazek | About (`SF-ST-ABOUT`) · Contact us (`SF-ST-CONTACT`) · How it works, Careers, Blog, Press (P2) |
| Help | FAQ (`SF-ST-FAQ`) · Track an order (`SF-AUTH-GUESTTRACK`) · Shipping (`SF-ST-SHIPPING`) · Returns and refunds (`SF-ST-RETURNS`) · Customer protection (`SF-ST-PROTECT`) · Dispute resolution (`SF-ST-DISPUTE`) · Payment methods (`SF-ST-PAYGUIDE`, P1) · Report a listing (`SF-ST-REPORT`) |
| Sell | Become a seller (`SF-SELL-LANDING`) · Fees (`SF-SELL-FEES`) · Seller FAQ (`SF-ST-FAQ-SELLER`) · Seller Agreement (`SF-ST-SELLERAGR`) · Seller sign-in (to the seller host) |
| Legal | Terms (`SF-ST-TERMS`) · Privacy (`SF-ST-PRIVACY`) · Cookies (`SF-ST-COOKIES`) · Prohibited items (`SF-ST-PROHIBITED`) · Cookie settings (reopens `SF-SH-CONSENT`) |

Bottom strip: legal entity name, commercial registration and e-commerce licence numbers (CMS-1) · accepted payment methods · social links · language switch · copyright. On mobile the columns collapse into accordions; the bottom strip is always visible.

### 1.6 Breadcrumbs

| Page | Trail |
|---|---|
| Category | Home › level 1 › … › current category |
| Product | Home › the product's category path › product title (not a link) |
| Search | Home › "Results for <query>" |
| Brand, store, campaign | Home › Brands or Stores or Deals › name |
| Account pages | Account › section › object (for example Account › Orders › order number) |
| Static pages | Home › page title |

Breadcrumbs follow reading direction and are emitted as structured data on public pages.

### 1.7 Search overlay (`SF-SH-SEARCH`)

Opens under the search field (full screen on mobile). Before typing: recent searches on this device (clearable) and popular searches. While typing (from 2 characters, debounced): up to 5 product suggestions with thumbnail and price, up to 3 categories and up to 3 brands; Enter or "See all results" goes to `SF-SEARCH`. Escape or the close control dismisses it and returns focus.

## 2. Seller Dashboard

### 2.1 Shell

- **Top bar:** store name with the seller-state chip (shown when not `ACTIVE`) · "View my store" (opens `SF-STORE` in a new tab) · notifications bell with unread count (to `SL-NOTIF`) · language · account menu: Account profile, Security, KYC documents, Referral (P1), Close account (P1), Sign out.
- **Sidebar** (bottom bar and "More" drawer on mobile; the bottom bar holds Home, Orders, Catalog, Wallet, More).
- **State banners** under the top bar: restricted (reason, link to `SL-PERF` or `SL-ACC-KYC`), document expiring, wallet deficit, vacation mode on.

### 2.2 Sidebar

| Group | Items (page) | Badge |
|---|---|---|
| Home | `SL-HOME` | – |
| Orders | Orders (`SL-ORD-LIST`) · Pickups (`SL-SHIP-PICKUP`) | Orders awaiting confirmation |
| Catalog | Offers (`SL-CAT-OFFERS`) · New-product requests (`SL-CAT-REQ`) · Bulk import (`SL-CAT-IMPORT`) · Price and stock (`SL-CAT-STOCK`) · Low stock (`SL-CAT-ALERTS`) · Violations (`SL-CAT-VIOL`) | Open violations |
| Returns and disputes | Returns (`SL-RET-LIST`) · Disputes (`SL-DISP-LIST`) | Items awaiting the seller's response |
| Wallet | Overview (`SL-WAL-HOME`) · Transactions (`SL-WAL-TX`) · Payouts (`SL-WAL-PAYOUTS`) · Commission invoices (`SL-WAL-INV`) · Payout destinations (`SL-WAL-METHODS`) | – |
| Marketing (P1) | Promotions (`SL-PRO-LIST`) · Advertising (`SL-ADS-LIST`) | – |
| Customers | Reviews (`SL-REV`) · Messages (`SL-MSG`, P1) · Questions (`SL-QA`, P1) | Unanswered messages |
| Performance | Performance (`SL-PERF`) · Appeals (`SL-APPEAL`, P1) | Level, when 1 or higher |
| Analytics | Overview (`SL-AN-HOME`) · Sales (`SL-AN-SALES`) · Reviews (`SL-AN-REV`) · Traffic (`SL-AN-TRAFFIC`, P1) · Buy Box (`SL-AN-BUYBOX`, P1) | – |
| Settings | Store profile (`SL-SET-STORE`) · Pickup addresses (`SL-SET-PICKUP`) · Policies (`SL-SET-POLICY`) · Notifications (`SL-SET-NOTIF`) · Vacation (`SL-SET-VACATION`, P1) · Team (`SL-TEAM`, P1) · Activity log (`SL-TEAM-LOG`) | – |
| Help (P1) | Help centre (`SL-HELP`) · Tickets (`SL-TICKET-LIST`) | – |

### 2.3 Visibility by staff role (P1; the owner sees everything)

From the role matrix in [seller-dashboard](../03-sellers/seller-dashboard.md) §3: a group is visible when the role has read or full access to its area.

| Group | Owner | Manager | Catalog | Fulfilment | Finance | Support |
|---|---|---|---|---|---|---|
| Home, Orders | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Catalog | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| Returns and disputes | ✓ | ✓ | – | ✓ | ✓ | ✓ |
| Wallet (except payout destinations) | ✓ | ✓ | – | – | ✓ | – |
| Payout destinations | ✓ | – | – | – | – | – |
| Marketing | ✓ | ✓ | ✓ | – | ✓ | – |
| Customers (reviews, messages, questions) | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| Performance, Analytics | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| Settings (store, pickup, policies) | ✓ | ✓ (read) | – | – | – | – |
| Team, Activity log, Close account | ✓ | – | – | – | – | – |
| KYC documents, Appeals, Referral, Help and tickets | ✓ | – | – | – | – | – |

The home page shows each role only the cards and action-queue items of the groups it can see.

### 2.4 Navigation by seller state

| Seller state | What is reachable |
|---|---|
| `REGISTERED`, `KYC_SUBMITTED`, `KYC_IN_REVIEW`, `NEEDS_INFO`, `REJECTED` | Only onboarding pages (`SL-ONB-*`), security and sign-out; no sidebar. Any other route redirects to `SL-ONB-STATUS` (or the next incomplete onboarding step) |
| `ACTIVE` | Everything |
| `RESTRICTED` | Everything, with the restricted banner; create-offer entry points are disabled with the reason when new offers are blocked |
| `SUSPENDED`, `CLOSING` | Read-only: every page opens and every action that changes data is disabled, except the fulfilment actions on open sub-orders (including RTO receipt), responses to returns and disputes, security settings and payout-destination verification (SLA-7). Landing page is `SL-SUSPENDED`; support (`SF-ST-CONTACT` until seller tickets ship, SUP-10; appeals P1) stays available |
| `CLOSED` | Sign-in leads to `SL-SUSPENDED` in its closed variant, which offers the history export only |

While the phone is unverified, every route redirects to `SL-AUTH-VERIFY`; then, before 2FA is enrolled, every route redirects to `SL-AUTH-2FASETUP`.

## 3. Admin Panel

### 3.1 Shell

- **Top bar:** global search (ADM-4) · approvals inbox with a count (to `AD-APPROVALS`) · notifications (admin inbox) · language · account menu (profile, security, sign out). The environment name is shown when it is not production.
- **Sidebar:** the groups below. A group or item appears only when the admin's roles hold a permission on its domain ([admin-governance](../05-trust/admin-governance.md) §2.1). Groups with a single visible item collapse into that item.

### 3.2 Sidebar

| Group | Items (page) | Badge |
|---|---|---|
| Dashboard | `AD-HOME` | – |
| Users | Customers (`AD-USR-CUSTOMERS`) · Sellers (`AD-USR-SELLERS`) · KYC queue (`AD-SEL-KYC`) · Seller performance (`AD-SEL-PERF`) · Appeals (`AD-SEL-APPEALS`, P1) · Admin users (`AD-USR-ADMINS`) · Roles (`AD-USR-ROLES`) | KYC items waiting |
| Catalogue | Products (`AD-CAT-PRODUCTS`) · Requests (`AD-CAT-REQUESTS`) · Suggested edits (`AD-CAT-EDITS`, P1) · Offer violations (`AD-CAT-VIOL`) · Reports (`AD-CAT-REPORTS`) · Duplicates (`AD-CAT-DUP`, P1) · Categories (`AD-CAT-CATS`) · Brands (`AD-CAT-BRANDS`) · Attributes (`AD-CAT-ATTR`) · Compliance (`AD-CAT-COMPL`) | Requests and reports waiting |
| 1P store | Offers (`AD-1P-OFFERS`) · Stock (`AD-1P-STOCK`) · Orders (`AD-1P-ORDERS`) · Returns (`AD-1P-RETURNS`) · Margin (`AD-1P-MARGIN`) · Suppliers (`AD-1P-SUPPLIERS`) · Pricing rules (`AD-PRO-PRICING`) | 1P orders awaiting confirmation |
| Orders | All orders (`AD-ORD-LIST`) · COD confirmations (`AD-ORD-COD`) · Exceptions (`AD-ORD-EXC`) | Exceptions |
| Logistics | Couriers (`AD-LOG-COURIERS`) · Serviceability (`AD-LOG-SERVICE`) · Pickups (`AD-LOG-PICKUPS`) · COD remittance (`AD-LOG-COD`) · Courier performance (`AD-LOG-PERF`) | Remittance exceptions |
| Returns and disputes | Returns (`AD-RET-LIST`) · Disputes (`AD-DISP-LIST`) | Disputes awaiting a decision |
| Finance | Transactions (`AD-FIN-TX`) · Ledger (`AD-FIN-LEDGER`) · Reconciliation (`AD-FIN-RECON`) · Funding position (`AD-FIN-FUNDING`) · Refunds (`AD-FIN-REFUNDS`) · Payouts (`AD-FIN-PAYOUTS`) · Failed payouts (`AD-FIN-FAILED`) · Adjustments (`AD-FIN-ADJ`) · Commission invoices (`AD-FIN-INV`) · Documents (`AD-FIN-DOCS`) · Loyalty liability (`AD-FIN-LOY`, P1) | Refunds and exceptions waiting |
| Risk | Queue (`AD-RISK-QUEUE`) · COD rules (`AD-RISK-COD`) · Blocklists (`AD-RISK-BLOCK`) · Return abuse (`AD-RISK-ABUSE`, P1) · Overrides (`AD-RISK-OVR`) | Cases waiting |
| Marketing (P1) | Coupons (`AD-PRO-COUPONS`) · Seller coupon approvals (`AD-PRO-APPROVALS`) · Flash deals (`AD-PRO-FLASH`) · Campaigns (`AD-PRO-CAMP`) · Loyalty (`AD-LOY-CONFIG`) · Ads (`AD-ADS-HOME`, `AD-ADS-SPONSORED`, `AD-ADS-MOD`) · Notification campaigns (`AD-NOT-CAMP`) | Approvals waiting |
| Moderation and support | Reviews (`AD-REV-QUEUE`) · Review rules (`AD-REV-RULES`, P1) · Q&A (`AD-QA-QUEUE`, P1) · Tickets (`AD-SUP-LIST`) · Delivery log (`AD-NOT-LOG`) | Flagged reviews, open tickets |
| Content | Home page (`AD-CMS-HOME`) · Banners (`AD-CMS-BANNERS`) · Pages (`AD-CMS-PAGES`) · Announcements (`AD-CMS-ANNOUNCE`, P1) · Help articles (`AD-CMS-HELP`, P1) · Email, SMS and push templates (`AD-CMS-EMAIL`, `AD-CMS-SMS`, `AD-CMS-PUSH` (P1)) | – |
| Analytics | `AD-AN-HOME` and its sub-pages | – |
| Compliance | Data requests (`AD-PRIV-REQ`) · Audit trail (`AD-AUDIT`) | Requests near their deadline |
| Settings | The `AD-SET-*` pages · System health (`AD-SYS-HEALTH`, P1) | – |

### 3.3 Landing page by role

After sign-in an admin lands on `AD-HOME`, whose widgets are chosen by role (ADM-10). Each widget's primary link is that role's main queue: Seller Manager → KYC queue; Catalog Manager → requests; Support → tickets; Finance → reconciliation; Fraud/Risk → risk queue; Logistics → exceptions; 1P Merchandiser → 1P orders; Marketing → approvals (P1); Content → home page editor; Compliance → data requests; Super Admin → approvals inbox.

## 4. Links between applications

| From | To | How |
|---|---|---|
| Storefront footer and `SF-SELL-LANDING` | Seller login or registration | Plain link to the seller host; no session is carried |
| Seller Dashboard "View my store" and product links | Storefront | New tab; the seller is a guest there |
| Admin detail pages | Storefront product or store page | New tab, public view |
| Admin | Seller Dashboard | Only through read-only "view as seller" (ADM-7, P1); never a shared session |
| Emails and SMS | The page for the object, on the right host | Deep link; sign-in with `returnTo` if needed; `SF-CHK-CODCONF` and guest tracking work without sign-in |

No application embeds another in a frame.

## 5. Acceptance criteria

- Every route in the sitemap is reachable from the navigation or from a page that the specifications name as its entry point; none is reachable only by typing its address.
- A staff member with a single role sees only that role's groups, in both languages.
- A seller in each state can reach exactly the pages in §2.4.
- The storefront header, mega menu, bottom bar and footer are fully operable by keyboard and screen reader in Arabic and English.
