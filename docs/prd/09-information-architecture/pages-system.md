# System Pages, Technical Routes and Redirects

**Authoritative for:** error and state pages, technical routes, and the redirect table.
**Read with:** [ia-model](ia-model.md) §6 · [sitemap](sitemap.md) §10 · [web-apps](../07-clients/web-apps.md) §4.3, §8 · [api-standards](../06-platform/api-standards.md)

---

## 1. Error and state pages

Each application has its own versions in its own shell, in both languages. All use `TPL-SYSTEM`.

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SYS-404 | `TPL-SYSTEM` | "We can't find that page" | Storefront: search field, home, popular categories. Seller and admin: back to the dashboard | Also shown for objects the user may not see (IA model §6); returns a 404 status | SEC-2 |
| SYS-403 | `TPL-SYSTEM` | "You don't have access to this page"; for staff, the permission needed and who can grant it | Back; sign in with another account | Returned when a signed-in user's realm or role does not allow the page | RBAC-2 |
| SYS-401 | `TPL-SYSTEM` | "Your session has ended" | Sign in (keeps `returnTo`) | Form data is preserved where possible | SES rules |
| SYS-500 | `TPL-SYSTEM` | "Something went wrong on our side" with the correlation ID | Try again; home; contact support | No technical detail is shown | API error rules |
| SYS-MAINT | `TPL-SYSTEM` | Maintenance message and expected end from app configuration | Refresh | Storefront and Seller Dashboard only; the Admin Panel stays reachable | API-6 |
| SYS-OFFLINE | `TPL-SYSTEM` | "You're offline"; the last-viewed order list where cached | Retry | P1 | – |
| SYS-APP | `TPL-CONTENT` | App download page with store badges | Open the store | P2, with the apps | – |

## 2. Technical routes

| ID | Template | Content | Actions | States and guards | Rules |
|---|---|---|---|---|---|
| SYS-ROBOTS | – | Storefront: allow public pages; disallow account, checkout, cart, search results and API paths; link to the sitemap index. Seller and admin hosts: disallow everything | – | – | [web-apps](../07-clients/web-apps.md) §4.3 |
| SYS-SITEMAPXML | – | Sitemap index with files per type (products, categories, brands, stores, static pages) and language, with alternate-language links; only indexable, live URLs | – | Regenerated on change events; no out-of-scope or suspended items | [web-apps](../07-clients/web-apps.md) §4.3 |
| SYS-MANIFEST | – | Name, icons, colours, start URL, display mode | – | P1 | – |
| SYS-AASA | – | iOS universal-link file listing the Storefront paths the app handles | – | P1 | [web-apps](../07-clients/web-apps.md) §4.4 |
| SYS-ASSETLINKS | – | Android app-link file | – | P1 | [web-apps](../07-clients/web-apps.md) §4.4 |
| SYS-SECURITYTXT | – | Security contact and policy link | – | P1 | [security](../05-trust/security.md) |
| SYS-APPCONFIG | – | Minimum and recommended client versions, maintenance state, feature flags, currency table | – | Public, cacheable for a short time | API-6, MON-8 |
| SYS-HEALTH | – | Liveness and readiness | – | Not public beyond the load balancer | [reliability-sre](../06-platform/reliability-sre.md) |

## 3. Redirects

| From | To | Type |
|---|---|---|
| `/wishlist`, `/account/favorites` | `/favorites` | Permanent |
| Product URL with an outdated title part | Canonical product URL (IA-10) | Permanent |
| Merged product | Surviving product | Permanent |
| Renamed category, brand or store slug | New slug | Permanent |
| `/seller/*`, `/admin/*` on the Storefront host | The seller or admin host's login | Temporary |
| A checkout step opened out of order | The first incomplete step (FL-1) | Temporary |
| A page needing sign-in | Login with `returnTo` (IA-13) | Temporary |
| Seller routes before onboarding or 2FA is complete | The pending onboarding or 2FA page ([navigation](navigation.md) §2.4) | Temporary |
| `/en` paths when the page has no English content yet | The Arabic page with a notice | Temporary |
