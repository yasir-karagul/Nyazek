# Documentation review — T-0060: IA consistency detail (second re-review)
Date: 2026-11-17 · Reviewer agent: `documentation-reviewer` (fresh context) · Scope: narrow. The items in the author's Disposition of the previous report, checked against the uncommitted working-tree text of `docs/prd/09-information-architecture/` (`sitemap`, `ia-model`, `shared-components`, `navigation`, `pages-admin-operations`, `pages-admin-growth-settings` (`AD-SET-TAX` only), `pages-seller-business`, `pages-storefront-account`, `pages-storefront-discovery` and `pages-storefront-checkout-auth` (the dedicated-layout pages only)), the T-0060 and T-0061 rows of `tasks/MASTER_TASKS.md`, and the owner-question list in [2026-11-17-T-0060-ia-detail.md](2026-11-17-T-0060-ia-detail.md) (Disposition section) · Follows up: [2026-11-17-T-0060-ia-detail-rereview.md](2026-11-17-T-0060-ia-detail-rereview.md)

## Verdict
approve

Every item in the previous report's Disposition is resolved in the files. This pass found no new critical, major or clear-defect minor problems.

**Tool results (run 2026-11-17 on the working tree):**
- `python -I docs/prd/_tools/check_docs.py docs/prd`: 69 files, 0 broken links, 137 `cfg:` keys, 47 decisions with none undefined, no duplicate rule IDs, no rule IDs referenced but undefined. The same four `cfg:` keys have no default as before (`identity.session_*`, `returns.abuse_proof_threshold`, `returns.abuse_restrict_threshold`, `shipping.free_threshold`). They are out of scope.
- `python -I docs/prd/_tools/check_ia.py docs/prd`: 293 sitemap pages, 293 specified, none missing, none extra, none duplicated.
- No Page IDs or `cfg:` keys changed in this round, so `count_pages.py` and `gen_config_register.py` were not re-run.

## Resolution of the previous findings

| Finding | Disposition claim | Result | Evidence |
|---|---|---|---|
| F-DOC-088.9 / F-DOC-144 | Fixed | Resolved | `pages-admin-operations.md:75` (`AD-LOG-COD`) now says "confirm a remittance (Logistics)" and asserts no approval step. |
| F-DOC-089.1 / F-DOC-142 | Fixed (column redefined) | Resolved | `sitemap.md:43` defines the Role column as "the main users of the page, for orientation only". The admin-governance §2.1 matrix decides access and wins. Under that definition, read-only users such as `AD-AUDIT` "Compliance (read only)" and `AD-FIN-LEDGER` Compliance no longer contradict the column. |
| F-DOC-089.2 / F-DOC-143 | Rows changed; owner question 18 | Resolved (IA part), rest deferred | `sitemap.md:546–563`: every settings row except `AD-SET-COMM` reads "Super Admin, owning role (admin-panel §1)". That row links to the configuration register. Q18 states the edit-rights conflict fairly and names `AD-SET-TAX`. The T-0061 Source column lists F-DOC-143. |
| F-DOC-092.1, .10 / F-DOC-145 | Fixed | Resolved | `AD-CAT-PRODUCT` names one template, "`TPL-DETAIL`, with each tab editable in place". This is a stated deviation, which ia-model §5 allows ("unless the specification says otherwise"). `SF-MSG` and `SL-MSG` name `TPL-LIST` plus the Message thread component on a sub-route, which fits the two-template sentence and IA-14. |
| F-DOC-146 | Fixed | Resolved | `ia-model.md:101` now says the specification states its empty states and guards, and that loading and request errors follow §6 per section. All four pages do this. `SF-HOME` omits empty sections. `SF-PDP` has "States and guards". `SF-CART` has its empty state. `SF-CHK-DONE` has its owner-only guard and redirect. |
| F-DOC-147 | Fixed | Resolved | `shared-components.md:46` no longer claims cropping for store and banner images. Line 48, `SF-MSG` and `SL-MSG` say contact details are "blocked", citing notifications-messaging §6. |
| F-DOC-148 | Fixed | Resolved | Q11 now asks the owner to decide all three cases and lists the follow-up edits (web-apps §4.3 citing CAT-12, the `410` row moving to `SF-PDP` states). `SF-PDP` still says the page "stays", which is acceptable while T-0061 is pending. |
| F-DOC-149 | Fixed | Resolved | Q2 names the sitemap and `SL-PERF` "override" wording. Q3 covers the configuration-register `events` group. The T-0061 Source column lists F-DOC-095.7. The wording at `sitemap.md:409` and the `SL-PERF` spec stays until Q2 is answered, as Q2 says. |
| F-DOC-150 | Fixed | Resolved | `navigation.md:164` reads "`AD-CMS-PUSH` (P1)", so only the push templates are P1. |
| F-DOC-151 | Fixed | Resolved | T-0060 is `in-review` (`MASTER_TASKS.md:64`). |

T-0061 (`MASTER_TASKS.md:65`) is `blocked`, depends on T-0060, says "18 questions" and matches the 18 numbered questions in the first report's Disposition.

## Findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| — | — | — | No new findings. | — |

## Not reviewed

- The text is uncommitted, so there is no diff. Only the locations named in the Disposition and their immediate context were read. Edits made elsewhere in this round were not looked for.
- Wording differences that are not defects were not raised. For example, `SF-MSG` says "contact details and links are blocked" while `SL-MSG` says "contact details blocked". Both defer to the Message thread component and notifications-messaging §6.
- The scope of the earlier reports was not re-sampled: domain citations in the other specifications, Arabic labels and design references.
