# Documentation review — T-0060: IA consistency detail (re-review of the fixes)
Date: 2026-11-17 · Reviewer agent: `documentation-reviewer` (fresh context) · Scope: the uncommitted working-tree text of `docs/prd/09-information-architecture/` (`ia-model` §5, `shared-components`, `sitemap`, `navigation`, `flows`, `pages-admin-operations`, `pages-admin-growth-settings`, `pages-storefront-account`, `pages-storefront-discovery`, `pages-storefront-checkout-auth`, `pages-seller-operations`, `pages-seller-business`), `03-sellers/seller-dashboard.md` §2–3, `05-trust/admin-panel.md` §1, and the T-0060 and T-0061 rows of `tasks/MASTER_TASKS.md`. Checked against `05-trust/admin-governance.md` §1–5, `00-governance/configuration-register.md`, `05-trust/identity-access.md` (§4, AUTH-5, SES-5), `02-commerce/support-cms.md` (SUP-3, SUP-10, CMS-4, CMS-7), `02-commerce/notifications-messaging.md` §6, `02-commerce/catalog-listings.md` §8, `02-commerce/checkout-orders.md` (ORD-16, SLA-3, SLA-6, GST-4), `03-sellers/seller-performance.md` (PRF-9), `04-finance/payments.md` (PAY-17), `07-clients/web-apps.md` §4.3 · Follows up: [2026-11-17-T-0060-ia-detail.md](2026-11-17-T-0060-ia-detail.md) (findings and author's Disposition)

## Verdict
approve with findings

No finding is critical or major. Most claimed fixes are correct. Five claimed fixes are wrong or only partly done: F-DOC-088.9, F-DOC-089.1, F-DOC-089.2, F-DOC-092.1 and F-DOC-092.10. Their residues are raised below as F-DOC-142 to F-DOC-145, together with three new minor findings and three notes. Narrowing or removing the unsupported assertions did not create new rules, with one exception: `AD-LOG-COD` now states a dual-control approval that admin-governance §3 does not contain (F-DOC-144). Fifteen of the 17 owner questions are stated fairly. Question 11 assumes part of its answer, and question 2 leaves related "override" wording in place (F-DOC-148, F-DOC-149).

**Changed documents and what they are authoritative for:** `ia-model` §5 covers templates. `shared-components` covers reusable components. `sitemap` covers Page IDs, priorities and the admin Role column. `navigation` covers menus and visibility. `flows` covers multi-page flows, and the `pages-*` files cover page content. `seller-dashboard` §2–3 covers seller modules, priorities and staff areas. `admin-panel` §1 covers admin modules. Domain documents win on rules (IA README).

**Tool results (run 2026-11-17 on the working tree):**
- `python -I docs/prd/_tools/check_docs.py docs/prd`: 69 files, 0 broken links, 137 `cfg:` keys, 47 decisions with none undefined, no duplicate rule IDs, no rule IDs referenced but undefined. The same four `cfg:` keys have no default as at the first review (`identity.session_*`, `returns.abuse_proof_threshold`, `returns.abuse_restrict_threshold`, `shipping.free_threshold`). They are out of scope.
- `python -I docs/prd/_tools/check_ia.py docs/prd`: 293 sitemap pages, 293 specified, none missing, none extra, none duplicated.
- `count_pages.py` and `gen_config_register.py` were run on a copy of `docs/prd` in the session scratchpad, not on the repository. Their output equals the committed `sitemap.md` and `configuration-register.md` except for Windows path separators (`..\`) and line endings, which are artefacts of running them on Windows. Page counts are unchanged (220/62/11 = 293). Every `cfg:` key used in the IA files is defined in a domain document.
- A tally of the Template column across the 13 `pages-*` files gives the values checked under F-DOC-145.

## Resolution of the T-0060 findings

| Finding | Disposition claim | Result | Evidence |
|---|---|---|---|
| F-DOC-088.1 | Fixed | Resolved | `SF-MSG` now says "threads close per notifications-messaging §6". |
| F-DOC-088.2 | Narrowed; T-0061 Q1 | Resolved | `SL-SET-VACATION` keeps only `cfg:sellers.vacation_max_days`. |
| F-DOC-088.3 | Narrowed; Q2 | Resolved in the spec | `AD-SEL-PERF` now offers only the Level 4 lift (PRF-9). Leftover "overrides" wording elsewhere: F-DOC-149. |
| F-DOC-088.4 | Fixed | Resolved | `AD-CAT-COMPL`: Catalog Manager edits and Compliance reads. Sitemap role is Catalog Manager. |
| F-DOC-088.5 | Narrowed; Q3 | Resolved | `AD-SYS-HEALTH` is Super Admin in both the spec and the sitemap. |
| F-DOC-088.6 | Fixed | Resolved | `AD-PRIV-REQ` "Compliance manages; Support and Super Admin read". |
| F-DOC-088.7 | Specs fixed; §3 row to Q4 | Resolved (IA part) | `AD-AUTH-LOGIN` and `AD-USR-ADMINS` cite identity-access §4 and dual control. That matches identity-access line 69. |
| F-DOC-088.8 | Fixed | Resolved | `AD-PRO-PRICING`: 1P Merchandiser only. |
| F-DOC-088.9 | Fixed | **Not resolved** | The fix adds a dual-control approval that admin-governance §3 does not contain: F-DOC-144. |
| F-DOC-088.10 | Narrowed; Q5 | Resolved | Stock badge: "when the API marks the stock as low"; the literal 5 is gone. |
| F-DOC-088.11 | Fixed | Resolved | `SF-SH-PWA` trigger removed. |
| F-DOC-088.12 | Narrowed; Q6 | Resolved | `SF-HOME` limits removed. Rows are computed per CMS-7, and CMS-7 says that. |
| F-DOC-088.13 | Narrowed; Q7 | Resolved | `AD-SET-LOCAL` lock removed. |
| F-DOC-088.14 | Fixed | Resolved | `SF-REFACC` keeps only the PAY-17 maximum. |
| F-DOC-089.1 | Fixed | **Partly resolved** | The column is now defined (sitemap §1), but at least 10 rows contradict the definition: F-DOC-142. |
| F-DOC-089.2 | Fixed | **Partly resolved** | §8.12 has a Role column, but it contradicts the configuration-register owners, admin-panel §1 and `AD-SET-TAX`: F-DOC-143. |
| F-DOC-089.3 | Fixed | Resolved | `AD-USR-SELLER` adds Fraud/Risk (suspension) and Finance (payout cycle). |
| F-DOC-089.4 | Fraud/Risk dropped; Q8 | Resolved | `AD-ORD-COD`: Support. |
| F-DOC-089.5 | Fixed | Resolved | `AD-ORD-DETAIL` adds 1P Merchandiser (1P orders) and Finance (A). |
| F-DOC-089.6 | Fixed | Resolved | `AD-AN-SEARCH`, `-PAY` and `-LOG` are "Per role". |
| F-DOC-089.7 | Q9 | Deferred to owner | Fairly stated. |
| F-DOC-089.8 | Fixed | Resolved | `AD-USR-ROLES` shows none, read, manage and approve. |
| F-DOC-089.9 | Fixed | Resolved | Follows 088.4–.6. |
| F-DOC-090.1 | Fixed | Resolved | seller-dashboard §2 adds an "Activity log" P0 module (SDB-2). |
| F-DOC-090.2 | Fixed | Resolved | The admin-panel row reads "P1 (1P pricing rules, `AD-PRO-PRICING`, P0)". |
| F-DOC-090.3 | Q10 | Deferred to owner | Fairly stated. |
| F-DOC-090.4 | Fixed | Resolved | Product card "Sponsored" variant is marked "(P1)". |
| F-DOC-090.5 | Fixed | Resolved, with a wording note | See F-DOC-150. |
| F-DOC-090.6 | Fixed | Resolved | `SF-RET-NEW` has "replace instead" (P1, D-25). `SL-WAL-TX` marks the P1 movement types. |
| F-DOC-092.1 | Fixed | **Partly resolved** | The two-template rule is now in ia-model §5, but three specs break it: F-DOC-145. |
| F-DOC-092.2 – .9 | Fixed | Resolved | `TPL-LIST` (cards, editable grid, matrix, tree), `TPL-DETAIL` (decision view), `TPL-LISTING` (store header), the dedicated layout and the Countdown variants are catalogued. The Countdown variants cite SLA-3, SLA-6, ORD-16, RET-3, DSP-4 and REV-1, which all exist. The Phone and OTP purposes are complete. `SF-CHK-RETURN` and `SF-CHK-CODCONF` state how they differ from their template. `SL-SUSPENDED` uses `TPL-DETAIL`. The dedicated layout raises a new gap: F-DOC-146. |
| F-DOC-092.10 | Fixed | **Partly resolved** | The Message thread component exists. `SF-MSG` and `SL-MSG` still name "thread view" (F-DOC-145), and the component says "masked" where the rule says "blocked" (F-DOC-147). |
| F-DOC-092.11 – .16 | Fixed | Resolved | The components exist. The Evidence uploader image variant is covered by F-DOC-147. |
| F-DOC-092.17, F-DOC-096.2 | Notes | No action | Accepted. |
| F-DOC-093.1 | Fixed | Resolved | FL-8 refers to the `SL-HOME` checklist. |
| F-DOC-093.2 | Fixed | Resolved | The sitemap `SL-CAT-REQ-NEW` note says "Steps per FL-10". |
| F-DOC-093.3 | Q11 | Deferred, but question not fairly stated | F-DOC-148. |
| F-DOC-093.4 | Line removed; Q12 | Resolved (IA part) | `SF-CHK-ADDR` has no separate contact-phone line. |
| F-DOC-094.1, .5, .6 | Q13–Q15 | Deferred to owner | Fairly stated. The specs still carry the step-ups that Q14 asks about, which is acceptable while it is pending. |
| F-DOC-094.2 – .4 | Fixed | Resolved | `SL-AUTH-2FA`, `SL-ACC-PROFILE` (AUTH-5), `SL-ACC-SEC` (SES-5), and `SL-CAT-OFFERS`/`SL-CAT-STOCK` (SDB-3). |
| F-DOC-095.1 – .4, .7 | Fixed | Resolved | seller-dashboard §3 now covers Home, the Customers area, own account and notifications, Team & Roles (activity log, closure), vacation and pickups. navigation §2.3 matches the matrix cell by cell. |
| F-DOC-095.5, .6 | Q16 | Deferred to owner | Fairly stated. The Referral part of F-DOC-095.7 is included in Q16 but missing from T-0061's Source column (F-DOC-149). |
| F-DOC-095.8 | Fixed | Resolved for the areas that exist | Home and Customers are marked. pages-seller-business §6 stays unmarked until Q16 is answered. |
| F-DOC-096.1 | Fixed | Resolved | navigation §1.1 links to taxonomy-and-labels §5. |
| F-DOC-138, F-DOC-139 | Fixed | Resolved | The sitemap and seller-dashboard say "customer phone in full only while fulfilling (SDB-7)". The hold badge is removed, and the sitemap §0 entry is marked withdrawn. |
| F-DOC-140 | Fixed | Resolved | `SL-SUSPENDED`, `SL-ORD-DETAIL` and navigation §2.4 point to `SF-ST-CONTACT` (seller topic, SUP-3) until seller tickets ship (SUP-10). |
| F-DOC-141 | Q17 | Deferred to owner | Fairly stated. The contradiction stays until it is answered. |
| Sitemap note (Contact seller route) | Fixed | Resolved | The route is now a sub-route of `SF-MSG`. |

Totals: of the 60 items the Disposition reports as fixed or narrowed, 55 are resolved, 4 are partly resolved (F-DOC-089.1, 089.2, 092.1, 092.10) and 1 is not resolved (F-DOC-088.9). Of the 17 owner questions, 16 are fairly stated and 1 is not (Q11). The 2 notes are accepted.

## Findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| F-DOC-142 | minor | 09/sitemap.md:43 (definition) vs :439, :454, :463–464, :471, :480, :492, :519, :564, and §8 rows generally | Residue of F-DOC-089.1. The new definition says the Role column lists the roles holding **M** on the page's domain, plus approving roles marked "(A)". Many rows contradict it. **Read-only roles listed as if they manage:** `AD-1P-MARGIN` lists Finance and Super Admin (both R on "1P offers, cost, stock, margin"). `AD-FIN-LEDGER` and `AD-FIN-DOCS` list Compliance (R). `AD-RISK-OVR` lists Compliance (R). `AD-AUDIT` lists "Super Admin, Compliance (read only)", but nobody holds M on "Audit trail". **Approvers listed without "(A)":** `AD-LOG-COD` (Finance holds A on COD remittance) and `AD-DISP-LIST`/`AD-DISP-DETAIL` (Finance holds A on returns and disputes). **"(A)" applied in only two rows** (`AD-ORD-DETAIL`, `AD-SET-COMM`). Other approvers are missing, such as Compliance (A) on `AD-CMS-PAGES` (legal-page publication, which the page spec requires), Super Admin (A) on customers, refunds, ledger and risk, and Finance (A) on `AD-RET-*` and risk. | Apply the definition row by row from admin-governance §2.1. Or redefine the column, for example "roles that work on the page; approvers marked (A)" and say how read-only roles such as Compliance appear. Then make the rows follow that definition. |
| F-DOC-143 | minor | 09/sitemap.md:546–565 (§8.12); 05-trust/admin-panel.md:25; 09/pages-admin-growth-settings.md:67, :76; 00-governance/configuration-register.md group owners | Residue of F-DOC-089.2. Every §8.12 settings page except `AD-SET-COMM` is now "Super Admin" only. Three sources disagree. (1) admin-panel §1 gives this module to "Super Admin and owning roles". (2) The settings pages show each value's owner role from the configuration-register, whose owners include Finance (`shipping`, `payments`, `escrow` → `AD-SET-SHIP`, `AD-SET-PAY`, `AD-SET-SLA`), Marketing (`loyalty`, `notifications` → `AD-SET-LOYALTY`, `AD-SET-NOTIF`) and Catalog Manager (`search`, `buybox`, `pricing` → `AD-SET-RANK`, `AD-SET-PRICE`). (3) `AD-SET-TAX` says "Edit (dual control, Finance)". The matrix gives "Platform settings" M to Super Admin alone, so the conflict is between domain documents (admin-governance §2.1 against the configuration-register owners), not only in the IA. | Owner decides whether a register "owner" edits the value or only answers for it. Record the answer in admin-governance §2.1 or §5, then fill §8.12 from it. Until then, do not present "Super Admin" as settled for the pages listed. |
| F-DOC-144 | minor | 09/pages-admin-operations.md:75 (`AD-LOG-COD`) | Residue of F-DOC-088.9. The new text makes confirming a remittance a Logistics action that "Finance approves as second person, admin-governance §2.1". admin-governance §2.1 says the A cells are "the dual-control approvals in §3". §3's only COD-remittance row is "COD write-off: Logistics → Finance". So the page now states a dual-control rule that the domain document does not contain, which the "no invented rules" rule forbids. | Do what F-DOC-088.9 recommended: "confirm a remittance (Logistics); write-offs need Finance approval (admin-governance §3)". If remittance confirmation should need approval, add it to T-0061 as a §3 row. |
| F-DOC-145 | minor | 09/ia-model.md:81; pages-admin-operations.md:41 (`AD-CAT-PRODUCT`); pages-storefront-account.md:68 (`SF-MSG`); pages-seller-business.md:38 (`SL-MSG`) | Residue of F-DOC-092.1 and .10. ia-model §5 now allows two templates only when "a list page also hosts the create and edit form, or the detail, of its own records". `AD-CAT-PRODUCT` (`TPL-DETAIL` and `TPL-FORM`) is not a list page. `SF-MSG` and `SL-MSG` name "`TPL-LIST` and thread view", but "thread view" is not a template. The Message thread component added for F-DOC-092.10 is not named by either page. | `AD-CAT-PRODUCT`: use `TPL-DETAIL` with "edit in place per `TPL-FORM` behaviour", or widen the ia-model sentence to cover detail pages with an edit mode. `SF-MSG`/`SL-MSG`: "`TPL-LIST`; the thread sub-route uses the Message thread component". |
| F-DOC-146 | minor | 09/ia-model.md:101 vs pages-storefront-discovery.md:25–39 (`SF-HOME`), :55–85 (`SF-PDP`), :103–114 (`SF-CART`); pages-storefront-checkout-auth.md:75 (`SF-CHK-DONE`) | The new "Dedicated layout" row says the specification "states its loading, empty and error states, since no template supplies them". None of the four pages that use it does this in full. `SF-HOME` gives only "a section with no content is omitted". `SF-CART` gives only its empty state. `SF-PDP` and `SF-CHK-DONE` give neither loading nor error states. The fix therefore leaves four P0 pages that do not meet the rule it introduced. ia-model §6 already defines loading and error behaviour for every page, so the new requirement may be stricter than needed. | Either add the missing states to the four specs, or reword the row: "ia-model §6 states apply; the specification gives its skeleton layout and any page-specific empty state". |
| F-DOC-147 | minor | 09/shared-components.md:46 (Evidence uploader), :48 (Message thread); pages-storefront-account.md:68; pages-seller-business.md:38 | Two new component rows say something the cited rules do not. (1) The Evidence uploader's "store or banner images (crop to the named variants)" applies the product-media variants (`thumb`, `card`, `detail`, `zoom`, catalog-listings §8.2) to store and banner images. No rule defines variants or cropping for those images, and banners use "images per language and breakpoint" (`AD-CMS-BANNERS`). (2) The Message thread says "contact details masked", as do `SF-MSG` and `SL-MSG`. notifications-messaging §6 says contact details, links and payment requests are **blocked** by the pre-screen and attempts are flagged to Risk. Masking and blocking behave differently for users. | (1) Say "store and banner images (media pipeline, catalog-listings §8.2)" without "crop to the named variants", or have the owner define image variants for stores and banners. (2) Say "contact details, links and payment requests blocked by the pre-screen (notifications-messaging §6)" in the component and in both pages. |
| F-DOC-148 | minor | Disposition Q11 (2026-11-17-T-0060-ia-detail.md:199); 07-clients/web-apps.md:84; 09/pages-system.md:48; pages-storefront-discovery.md:81 | Q11 is not stated fairly. "Archived or removed products return `410` with the 'No longer available' page" is presented as settled, but no document says it: web-apps still says only "removed products return `410`", and `SF-PDP` still says the page "stays", which reads as a normal 200. F-DOC-093.3 also had parts that need no owner decision: map archived to removed (CAT-12) in web-apps §4.3, and move the `410` row out of the redirects table into the `SF-PDP` states. Those parts were neither done nor listed. If the owner answers only the question asked, the original inconsistency stays. | Reword Q11 so the owner confirms both halves: (a) archived or removed → `410` with the "No longer available" body and similar products, `noindex`; (b) what a temporarily unpublished product returns. Then fix the non-owner parts of F-DOC-093.3 in T-0060, or list them explicitly in T-0061. |
| F-DOC-149 | note | 09/sitemap.md:409 ("Scores, levels, overrides"); pages-seller-business.md:45 (`SL-PERF` "overrides shown with their reason"); 03-sellers/seller-performance.md:69; tasks/MASTER_TASKS.md:65; 00-governance/configuration-register.md:20 | Gaps in what the owner questions name. (1) Q2 narrows `AD-SEL-PERF`, but the sitemap note and `SL-PERF` still mention performance "overrides". seller-performance also says admins see "overrides" without defining them. Q2 should name these places so that they are corrected whichever way the owner answers. (2) The T-0061 Source column omits F-DOC-095.7, although Q16 covers Referral. (3) Q3 (engineer access) should also cover the configuration-register `events` group, whose owner is "Engineering", the same role that does not exist. | Add these references to Q2, Q3 and the T-0061 Source column. |
| F-DOC-150 | note | 09/navigation.md:164 | "Email, SMS and push templates (`AD-CMS-EMAIL`, `AD-CMS-SMS`, `AD-CMS-PUSH`, P1)" can be read as making all three P1. Under NAV-2 that would hide two P0 pages. | "Email and SMS templates (`AD-CMS-EMAIL`, `AD-CMS-SMS`) · Push templates (`AD-CMS-PUSH`, P1)". |
| F-DOC-151 | note | tasks/MASTER_TASKS.md:64 | T-0060 is `in-progress` while its reviews run. CLAUDE.md step 5 sets `in-review` before the reviews. | Set the status the session protocol expects when the task goes back to the owner. |

## Owner questions (T-0061): fairness check

Questions 1–10 and 12–17 restate the original findings accurately. Each says what was removed or narrowed meanwhile, and none presents an answer as decided. Question 11 does (F-DOC-148). Questions 2 and 3 should also name the places listed in F-DOC-149. The T-0061 row is `blocked`, depends on T-0060 and cites the report and the finding IDs, apart from the F-DOC-095.7 omission.

## Not reviewed

- The text in scope is uncommitted, so there is no diff. "What changed" was inferred from the Disposition and the current text, and edits made outside the listed locations may not have been seen. The listed files were read in full except `flows.md` (FL-6 to FL-15 only) and `sitemap.md` (§0–2, §5, §7 and §8–14).
- The other domain citations in the 293 specifications were not re-sampled. Arabic labels and design references were not reviewed (as in the first report).
- `gen_config_register.py` and `count_pages.py` were run only on a scratchpad copy. Their Windows path-separator output is a platform artefact and is not raised as a finding.

## Disposition (added by the author, 2026-11-17)

| Finding | Disposition |
|---|---|
| F-DOC-088.9 / F-DOC-144 | Fixed: `AD-LOG-COD` says "confirm a remittance (Logistics)"; no approval step asserted |
| F-DOC-089.1 / F-DOC-142 | Fixed: the Role column is redefined as the page's main users, for orientation; the matrix decides access and wins |
| F-DOC-089.2 / F-DOC-143 | Settings rows now read "Super Admin, owning role (admin-panel §1)"; whether the owning role edits values is owner question 18 in T-0061 |
| F-DOC-092.1, .10 / F-DOC-145 | Fixed: `AD-CAT-PRODUCT` is `TPL-DETAIL` with in-place editing; `SF-MSG` and `SL-MSG` use `TPL-LIST` with the Message thread component on a sub-route |
| F-DOC-146 | Fixed: the dedicated-layout row says loading and request errors follow ia-model §6 per section; the specs already state empty states and guards |
| F-DOC-147 | Fixed: no cropping claim; contact details "blocked" per notifications-messaging §6 in the component and both message pages |
| F-DOC-148 | Fixed: owner question 11 reworded and lists the follow-up edits |
| F-DOC-149 | Fixed: questions 2 and 3 extended; T-0061 Source lists F-DOC-095.7 and F-DOC-143 |
| F-DOC-150 | Fixed: "`AD-CMS-PUSH` (P1)" |
| F-DOC-151 | Fixed: T-0060 is `in-review` |
