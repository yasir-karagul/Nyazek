# Architecture review — T-0061: Decisions raised by T-0060 (ADR-0007), re-review
Date: 2026-11-18 · Reviewer agent: `architecture-reviewer` (skill `nyazek-architecture-review`) · Scope: uncommitted changes on branch `task/T-0061-t0060-decisions` against `yasir` (`git diff yasir`). Focus on the revised texts: ledger-reconciliation MON-4 and MON-8, seller-accounts-kyc SEL-6 and SEL-9, payments §7 (COD fee), architecture.md event catalogue (product events), web-apps §4.3, inventory STK-6, support-cms CMS-7, admin-governance §3 and §5, checkout-orders GST-3a, and `docs/adr/0007-decisions-from-the-ia-consistency-pass.md`. Cross-checked against checkout-orders §5 and §6, seller-performance PRF-4 and the metric table, catalog-listings CAT-10 and CAT-12, and pages-storefront-discovery `SF-PDP`. · Follows up: `docs/reviews/architecture/2026-11-18-T-0061-decisions.md`

## Verdict
approve with findings

The major finding F-ARCH-037 is resolved. All the minor findings and notes from the first report are resolved. Two new minor findings remain. Both are rule contradictions between documents, introduced by the fixes. Neither is critical or major.

## Status of previous findings
| ID | Status | Evidence |
|---|---|---|
| F-ARCH-037 (major) | Resolved | MON-8 now locks the exponent and price step once a market is enabled. That covers prices, coupons, `cfg:` values and ledger entries created before the first order. It also names `backoffice` as owner of both the market's enabled state and the currency table, so the lock is enforced inside one foundation module with no upward dependency. ADR-0007 Q7 matches. |
| F-ARCH-038 | Resolved | MON-4 now takes the price step from the currency table (MON-8). It says the step is held as `cfg:money.price_step` and locked with the table, so no unlocked path remains. |
| F-ARCH-039 | Resolved | SEL-9 names `sellers` as the enforcer, calling the `orders` exported query (ARC-3). That is a same-layer read through a public interface, and `orders` gains no dependency on `sellers`. |
| F-ARCH-040 | Resolved in substance | SEL-9 defines what happens to later arrivals: normal SLA, the seller is notified, and an SLA cancellation is excluded from performance. See F-ARCH-049 for the documents that were not aligned. |
| F-ARCH-041 | Resolved | payments §7 makes the mechanism P0. Quotes and orders always carry the field, and a zero fee posts no ledger line. |
| F-ARCH-042 | Resolved | web-apps §4.3 defines the product resource states (`unpublished`, `archived`, `merged` + survivor ID) and the HTTP answer for each. The event catalogue adds `product.archived` and `product.merged` (with `survivorProductId`), and these events purge the edge cache and the search index. `SF-PDP` matches. |
| F-ARCH-043 | Resolved | STK-6 has the API apply the threshold and compute the count at response time, and it states the cache lag. |
| F-ARCH-044 | Resolved, with a residual inconsistency | admin-governance §5 names who edits each group of settings and that owner roles are notified. The dual-control table now has a Finance approval row for financially sensitive settings. See F-ARCH-050. |
| F-ARCH-045 | Resolved | ADR-0007 Q3 now states that metrics and alerts reach engineers and that retrying or discarding a dead letter stays a Super Admin action. It no longer claims that engineers already operate the queues. |
| F-ARCH-046 | Resolved | SEL-6 defines the slug: transliterated from the store name, a numeric suffix on collision, read-only for the seller, former slugs reserved and redirected, a reserved-word list, and a correction that holds until the next rename. The schema needs are now determinable. |
| F-ARCH-047 (note) | Resolved | ADR-0007 Q13 says the API refuses onboarding until the phone is verified. |
| F-ARCH-048 (note) | Resolved | CMS-7 says the content API applies both limits. |

## Findings
| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| F-ARCH-049 | minor | seller-accounts-kyc SEL-9; checkout-orders §5 SLA table (row 1: "Auto-cancel `SLA_CONFIRM_TIMEOUT`; counts against seller") and §6 cancellation table ("Timeouts count against seller"); seller-performance metric table (Cancellation rate includes `SLA_CONFIRM_TIMEOUT`) and PRF-4 (exclusions) | **The vacation exclusion in SEL-9 is not reflected in the documents that compute seller metrics.** SEL-9 says an SLA cancellation of a sub-order that reached the seller during vacation is excluded from performance metrics. The two checkout-orders tables still say timeouts always count against the seller. PRF-4, the authoritative exclusion list that the metric calculation in `sellers` follows, does not list this case. Whoever implements the score from seller-performance would count these cancellations, which contradicts ADR-0007 Q1. The cancellation reason code is the same (`SLA_CONFIRM_TIMEOUT`), so the exclusion also depends on the vacation interval recorded in `sellers` at the cancellation time. No document says this. | Add the case to PRF-4, for example "confirmation timeouts of sub-orders released to the seller during vacation mode (SEL-9)". Qualify the checkout-orders §5 row and §6 row with a reference to it. State that `sellers` decides the exclusion from its own vacation history, so `orders` needs no new reason code and no dependency on `sellers`. |
| F-ARCH-050 | minor | admin-governance §2.1 matrix row "Platform settings" (Finance "R, A (tax)"); §3 row "Financially sensitive setting change (payout cycle, escrow hold, COD limits and fee, shipping rates, loyalty rates)"; §5 second bullet "Financially sensitive settings (thresholds, commission, payout cycle, escrow hold, COD limits) change under dual control" | **The list of financially sensitive settings and Finance's approval right are stated three ways.** The §3 row adds COD fee, shipping rates and loyalty rates. The §5 bullet does not have them, and it adds thresholds and commission, which are covered by other §3 rows. The matrix gives Finance approval only for tax, although §3 now makes Finance the approver of every financially sensitive setting. `backoffice` has to store which keys need dual control and who approves them (F-ARCH-044), so it has no single list to implement from. This also breaks the "No duplication" rule. | Keep the list in one place: the §3 row, or a dual-control column in the generated configuration register. Have §5 point to it instead of restating it. Change the matrix cell to "R, A (tax, financially sensitive settings)" or an equivalent reference. |

## Checked without findings
- MON-8 lock: the "market enabled" fact and the currency table are both in `backoffice`, so no layering violation remains. The lock leaves the display format editable, and nothing else in the PRD depends on that being mutable or immutable.
- Event catalogue: adding `product.archived` and `product.merged` before launch needs no EVT-3 version bump. `survivorProductId` appears only on `product.merged`. Consumers (search index, edge revalidation) follow from web-apps §4.2 and §4.3.
- web-apps §4.3 and CAT-12: archived keeps resolving (410 page with content replaced by "No longer available"), so CAT-12 holds. Unpublished returns 404 and `SYS-404` already returns 404. Policy takedowns expose no content.
- COD fee: always present in the contract and 0 by default. D-21 stays with the owner. No new posting path (JE-8 or account 4130 unchanged, zero posts nothing).
- GST-3a: stays inside `orders` and `identity`, with no new dependency.
- Market readiness: none of the revised texts adds a country, currency, time-zone or phone literal to business logic. IQD values appear only as register defaults.
- Standing decisions: no new module, datastore, service or dependency. No ADR is needed beyond ADR-0007.

## Not reviewed
- Security aspects of the admin-reset row, Q14 and Q15 step-up, and the Finance approval rows. These belong to the security re-review.
- Wording consistency between the PRD and the IA pages beyond what the checks above needed. This belongs to the documentation re-review.
- Q9 and the wider access in Q16 (T-0064) are reserved to the owner and were not decided.

## Disposition (added by the author, 2026-11-18)

| Finding | Disposition |
|---|---|
| F-ARCH-049 | Fixed: PRF-4 excludes confirmation timeouts of sub-orders that reached the seller during vacation (identified by `sellers` from its own vacation history); checkout-orders §5 and §6 point to PRF-4 |
| F-ARCH-050 | Fixed: admin-governance §3 holds the single list; §5 links to it; matrix cell names it; `AD-SET-SLA` and `AD-RISK-COD` cite it |
