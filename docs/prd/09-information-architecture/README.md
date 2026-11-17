# Information Architecture

How Nyazek's three web applications are organised: what pages exist, how people move between them, what every page contains and does, and what things are called. Together with the domain documents (which hold the rules), this section is what a page is built from.

**Authoritative for:** navigation structures, page templates, shared components, the content and actions of every page, screen-to-screen flows, category taxonomy, status and navigation labels, URL rules, and the page inventory.
**Not authoritative for:** business rules, calculations, state machines, permissions and priorities of features. Page specifications name the rule IDs that govern them; where a page specification and a domain document differ, the domain document wins and the page specification is corrected ([document-control](../00-governance/document-control.md) §3.1).

---

## 1. Documents

| Document | Authoritative for | Read it when |
|---|---|---|
| [ia-model](ia-model.md) | Principles, the objects people navigate, URL rules, page templates, global states, how to read a page specification | First |
| [sitemap](sitemap.md) | Page inventory: Page IDs, routes, access, priorities, counts | To find a page or its priority |
| [navigation](navigation.md) | Header, menus, footer, sidebars, role-based visibility, breadcrumbs, mobile navigation | Building a shell or any link between pages |
| [taxonomy-and-labels](taxonomy-and-labels.md) | Category tree, order and return status labels, tab-to-state mappings, navigation labels in Arabic and English | Showing a status, a tab or a menu label |
| [shared-components](shared-components.md) | The catalogue of components reused across pages and what each must show | Before building any page |
| [flows](flows.md) | Multi-page flows step by step: guards, back behaviour, exits | Building checkout, sign-in, onboarding, returns, imports, approvals |
| [pages-storefront-discovery](pages-storefront-discovery.md) | Shell, home, search, category, product, brand, store, deals, favourites, cart | |
| [pages-storefront-checkout-auth](pages-storefront-checkout-auth.md) | Sign-in and registration pages, checkout, payment return, COD confirmation, guest tracking | |
| [pages-storefront-account](pages-storefront-account.md) | Customer account pages, public seller pages, static and legal pages | |
| [pages-seller-operations](pages-seller-operations.md) | Seller sign-in, onboarding, home, orders, catalog, returns and disputes | |
| [pages-seller-business](pages-seller-business.md) | Seller wallet, promotions, ads, messages, reviews, performance, analytics, settings, team, account, help | |
| [pages-admin-operations](pages-admin-operations.md) | Admin sign-in, dashboard, approvals, users, catalogue, 1P, orders, logistics, returns and disputes | |
| [pages-admin-finance-risk](pages-admin-finance-risk.md) | Admin finance and risk pages | |
| [pages-admin-growth-settings](pages-admin-growth-settings.md) | Admin promotions, ads, reviews, support, CMS, notifications, analytics, privacy, settings | |
| [pages-system](pages-system.md) | Error and system pages, technical routes, redirects | |

## 2. How a page is specified

Every Page ID in the [sitemap](sitemap.md) has exactly one specification row or block in a `pages-*` document, checked by `_tools/check_ia.py`. A specification gives:

| Field | Meaning |
|---|---|
| Template | The page template from [ia-model](ia-model.md) §5. Everything the template defines (regions, loading, empty and error states, pagination, responsive behaviour) applies without being repeated |
| Content | What the page shows beyond the template: regions in order, and the data in each |
| Actions | What the user can do, and where each action leads |
| States and guards | Who may open the page, conditions that change it, redirects, page-specific empty or blocked states |
| Rules | The rule IDs and document sections that govern the page's behaviour |

Priority and route are in the sitemap and are not repeated. A page's priority is the minimum; an element marked P1 or P2 inside a page ships later than the page.

## 3. Building a page: reading order

1. The page's row in the [sitemap](sitemap.md) (route, access, priority).
2. Its specification in the `pages-*` document, and the template it names.
3. The [shared-components](shared-components.md) it uses and the [navigation](navigation.md) it sits in.
4. The rules it cites, in the domain documents.
5. Labels and statuses from [taxonomy-and-labels](taxonomy-and-labels.md); strings go to the message catalogues.
6. The design reference for the Page ID ([design-system-ui-workflow](../07-clients/design-system-ui-workflow.md) §6). If the design and this section disagree on structure or content, raise it; the PRD wins (UI-3).

If something needed to build a page is in none of these, it is a gap: stop and ask rather than invent ([claude-workflow](../08-engineering/claude-workflow.md) GRD-8).

## 4. Ratified proposals

The owner ratified the proposals made in this section on 2026-11-17 ([open-decisions](../00-governance/open-decisions.md) §5, D-46; the full list is in [review-findings](../00-governance/review-findings.md) §13.1). Arabic wording, still marked *proposed*, is finalised in copy review (UI-4).
