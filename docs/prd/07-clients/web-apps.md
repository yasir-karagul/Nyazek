# Web Applications

**Authoritative for:** the three web apps (Storefront, Seller Dashboard, Admin Panel): rendering model, boundaries with the API, language and RTL, SEO, accessibility, performance budgets, customer-facing feature list.
**Related:** [architecture](../06-platform/architecture.md) · [design-system-ui-workflow](design-system-ui-workflow.md) · [seller-dashboard](../03-sellers/seller-dashboard.md) · [admin-governance](../05-trust/admin-governance.md) · [admin-panel](../05-trust/admin-panel.md) · [information architecture](../09-information-architecture/README.md) (sitemap, navigation, and the specification of every page)

---

## 1. The three apps

| App | Origin | Technology | Rendering |
|---|---|---|---|
| Storefront | `www.<domain>` | Next.js (App Router) | Server-rendered and cached public pages; client-rendered account and checkout |
| Seller Dashboard | `seller.<domain>` | React single-page app (Vite) | Client-rendered; static hosting |
| Admin Panel | `admin.<domain>` | React single-page app (Vite) | Client-rendered; static hosting behind zero-trust access |

Shared packages: `ui-web` (components), `design-tokens`, `i18n`, `contracts`, `api-client`, `config` (lint, TypeScript, Tailwind presets).

## 2. Boundary rules

- WEB-1 Web apps are API clients only. They contain no business rules, no database access and no secrets other than public configuration.
- WEB-2 All data access uses the generated API client. In the Storefront, server components call the API with the visitor's cookie forwarded; nothing else.
- WEB-3 Next.js server actions and route handlers that perform business operations are prohibited and blocked by a lint rule. The only permitted route handlers are technical (health, sitemap, robots, well-known files).
- WEB-4 Session cookies are set by the API on the app's own origin through the `/api` path ([identity-access](../05-trust/identity-access.md) §5–6). No token is readable by browser JavaScript.
- WEB-5 Client-side validation exists for usability only; the API is authoritative and its error codes drive messages.
- WEB-6 Amounts, totals, eligibility and availability shown in the UI always come from API responses.
- WEB-7 Supported browsers: the current and previous major versions of Chrome, Safari, Firefox, Edge and Samsung Internet, and the in-app browsers of Facebook, Instagram and TikTok on Android and iOS (a large share of traffic arrives from social links). Minimum viewport width 360 px for the Storefront and Seller Dashboard; the Admin Panel is desktop-first (ADM-12). Unsupported browsers get a functional page, not a block.

## 3. Language, direction and formatting

- Arabic (RTL) is the default; English (LTR) is optional.
- Storefront URLs: Arabic at the root, English under `/en`, with `hreflang` and canonical tags; the choice is remembered in a cookie and, when signed in, in the account. The dashboards use the account's language setting.
- All user-facing strings come from the shared ICU message catalogues; no hard-coded text in components.
- Layout uses CSS logical properties; directional icons mirror; mixed-direction text (English brand names, numbers, order numbers inside Arabic) uses bidi isolation.
- Western digits are displayed in both languages unless D-19 decides otherwise; inputs accept Arabic-Indic digits.
- Dates and times display in the market's time zone (Asia/Baghdad for Iraq); Gregorian calendar.
- Every component and page is reviewed in both languages at worst-case text length.
- Kurdish (Sorani) is out of scope until D-13.

## 4. Storefront

### 4.1 Feature set

| Feature | Description | Priority |
|---|---|---|
| Home | Hero banners, category grid, product rows (New Arrivals, Best Sellers, Top Rated, Deals) from the CMS | P0 |
| Category pages | Hierarchical browse with attribute filters | P0 |
| Search | [search-buy-box](../02-commerce/search-buy-box.md) | P0 |
| Product page | Gallery and video, variants, price, Buy Box seller, other sellers, delivery estimate by governorate, tabs (Description, Specifications, Reviews, Shipping & Returns; Q&A at P1), report listing | P0 |
| Product card | Name, price, seller name and rating, delivery estimate, discount badge | P0 |
| Seller store page | Product grid, ratings, about, policies, legal identity | P0 |
| Favourites | Save products; tabs All / In Stock / Price Dropped; guest favourites merge at sign-in ([customer-account](../02-commerce/customer-account.md) §2) | P0 (price-drop notification P1) |
| Cart and five-step checkout, guest checkout | [checkout-orders](../02-commerce/checkout-orders.md) | P0 |
| Payment return page and COD confirmation landing page | [payments](../04-finance/payments.md), [fraud-risk](../05-trust/fraud-risk.md) §4.1 | P0 |
| Account: orders, tracking, cancellation, receipts | Internal timeline plus courier tracking link | P0 |
| Returns, refunds, disputes, refund accounts | [returns-disputes](../02-commerce/returns-disputes.md) | P0 |
| Reviews | Write and manage reviews | P0 |
| Addresses, profile, security (password, devices), privacy and consent, account deletion | | P0 |
| Notifications inbox and preferences | | P0 |
| Static and legal pages, contact form, cookie banner | [support-cms](../02-commerce/support-cms.md) | P0 |
| Brand pages | | P1 |
| Flash deals and campaign pages | | P1 |
| Loyalty, coupons, referral | [loyalty](../02-commerce/loyalty.md) | P1 |
| Customer–seller messaging, product Q&A | | P1 |
| Optional 2FA; saved card tokens | | P1 |
| Back-in-stock alerts, buy again, share a product | [customer-account](../02-commerce/customer-account.md) §3–4 | P1 |
| Offline shell and installable web app | | P1 |
| Recently viewed, frequently bought together | | P2 |

Out of scope: product comparison, public wishlist sharing, store "follow".

The structure, content and actions of each page are specified in [09-information-architecture](../09-information-architecture/README.md); the table above is the feature list and its priorities.

### 4.2 Rendering and caching

- Public pages (home, category, search, product, store, static) are server-rendered and cached at the edge with short lifetimes and background revalidation; price, stock and Buy Box fragments are fetched fresh or revalidated on change events.
- Personalised and account pages are never cached at the edge.
- The cart badge, sign-in state and favourites hydrate on the client so cached HTML stays anonymous.

### 4.3 SEO (structure P0)

- Clean, stable, human-readable URLs (the same routes later serve as deep links for the apps).
- Canonical URLs, `hreflang` pairs, paginated listing URLs, XML sitemaps per type and language, `robots.txt` (Seller and Admin origins disallow everything).
- Structured data (JSON-LD): Product with offers and aggregate rating, Breadcrumb, Organization. Open Graph and equivalent tags on product, store and campaign pages so shared links preview correctly.
- Out-of-stock products keep their URL; removed products return `410` or redirect to the merged product.
- Search-result pages are `noindex`; category pages are indexable.

### 4.4 Deep-link readiness

`/.well-known/apple-app-site-association` and `/.well-known/assetlinks.json` are served from launch (P0) so app links work as soon as the Flutter apps ship.

## 5. Seller Dashboard and Admin Panel

- Functional scope: [seller-dashboard](../03-sellers/seller-dashboard.md), [admin-panel](../05-trust/admin-panel.md) and [admin-governance](../05-trust/admin-governance.md), with the page inventory in the [sitemap](../09-information-architecture/sitemap.md).
- Dense, table-oriented variant of the design system; keyboard-friendly; saved filters; bulk actions with confirmation.
- Role-aware navigation built from the permissions the API returns; the API remains the control.
- Long operations (imports, exports, payout runs) are background jobs with progress and result pages.
- Admin screens mask personal data by default with an explicit, logged reveal.
- Neither app loads third-party marketing or analytics tags.

## 6. Accessibility

- The component library meets WCAG 2.2 AA: contrast, visible focus, keyboard operation, labels and names, error identification, target size (minimum 24 × 24 CSS pixels, 44 × 44 for primary touch targets), reduced-motion support.
- Colour is never the only carrier of meaning (status chips, price changes, validation).
- Screen-reader checks in Arabic and English for the core customer flow (search → product → cart → checkout → order tracking).
- Automated accessibility checks run in component tests and end-to-end tests; a manual audit of core flows is P1.

## 7. Performance budgets (Storefront, mobile)

| Budget | Limit |
|---|---|
| JavaScript for first load of Home and PDP | ≤ 170 kB compressed |
| Largest image above the fold | Responsive variant, AVIF or WebP, ≤ 100 kB typical |
| Fonts | Two families, subset, `font-display: swap`, preloaded Arabic text face |
| Third-party tags | Loaded after consent and after interaction readiness |
| API calls for first render of PDP | Server-side, in parallel, total server time ≤ 300 ms p95 |

Budgets are enforced in CI (bundle-size check, Lighthouse CI against the preview deployment).

## 8. Error, empty and loading states

Every page defines loading, empty, error and permission-denied states in both languages. System pages: not found, forbidden, session expired, server error (with correlation ID), maintenance (driven by app configuration), offline (P1).

## 9. Acceptance criteria

- A static check finds no server action or direct data access in any web app.
- Every Storefront public page renders correctly with JavaScript disabled for its primary content.
- All P0 pages pass automated accessibility checks and RTL visual tests in both languages.
- Bundle and Lighthouse budgets pass in CI.
