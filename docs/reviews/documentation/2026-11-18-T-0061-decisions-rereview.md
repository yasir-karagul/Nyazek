# Documentation review — T-0061: Decisions raised by T-0060 (ADR-0007), re-review
Date: 2026-11-18 · Reviewer agent: `documentation-reviewer` (fresh context) · Scope: uncommitted changes on branch `task/T-0061-t0060-decisions` (`git diff yasir`): `docs/adr/0007-decisions-from-the-ia-consistency-pass.md` and the 27 changed files under `docs/prd/` and `tasks/MASTER_TASKS.md`. Each disposition of F-DOC-184 to F-DOC-196 was checked, ADR-0007 was compared with the PRD rules it names, and cross-document effects were checked in admin-governance §2.1, §3 and §5, `pages-admin-operations.md` (`AD-USR-SELLER`), `pages-admin-finance-risk.md` (`AD-RISK-COD`), `pages-admin-growth-settings.md`, notifications-messaging NTF-5, checkout-orders ORD-13, catalog-listings CAT-10 and CAT-12, and identity-access §4 · Follows up: [2026-11-18-T-0061-decisions.md](2026-11-18-T-0061-decisions.md)

## Tool results

- `python -I docs/prd/_tools/check_docs.py docs/prd`: broken links 0, cfg keys 141, decisions used but undefined [], defined only in register [], duplicate rule IDs {}, referenced but not defined []. The four "no default" keys are the same as before.
- `python -I docs/prd/_tools/check_ia.py docs/prd`: 293 sitemap pages, 293 specified; no page missing, extra or specified twice.
- `gen_config_register.py` and `count_pages.py` were re-run on a copy of `docs/prd` in the scratchpad. `diff -r` against the working tree shows no difference. The register (141 keys, including the new `identity.phone_change_cooldown_hours`) and the page counts are current.

## Previous findings

| Finding | Status | Evidence |
|---|---|---|
| F-DOC-184 | Resolved | admin-governance §5 now limits Super Admin editing to the `AD-SET-*` pages and names the editing roles for `AD-RISK-COD`, `AD-LOY-CONFIG` and `AD-PRO-PRICING`. admin-panel §1 agrees. |
| F-DOC-185 | Resolved | The ADR-0007 Consequences no longer claims an interim Super Admin restriction. It records that NTF-5 and the sitemap give Support access today, and states that the ADR changes none of it. T-0064 (`blocked`) now covers `AD-NOT-LOG`, `AD-SET-NOTIF` and `AD-NOT-CAMP`. See F-DOC-199 for one inaccuracy that remains in that description. |
| F-DOC-186 | Resolved | web-apps §4.3 and `SF-PDP` name every state: no live offer (normal page), unpublished or taken down (`404`, `noindex`), policy takedown (generic notice only), archived (`410`, `noindex`) and merged (`301`). architecture §4.2 adds `product.archived` and `product.merged`. ADR Q11 uses the same terms. No other document still says `410` or "No longer available". |
| F-DOC-187 | Resolved | Q16 is now Owner only for all four areas, and wider access moved to T-0064. The ADR header no longer claims a loosening and names Q16 explicitly. |
| F-DOC-188 | Resolved | payments §7 marks the mechanism P0 with the value at 0 until D-21. This matches scope-priorities §2.2. |
| F-DOC-189 | Resolved for tax | The matrix has "R, A (tax)" for Finance, and the sitemap has `AD-SET-TAX` "Super Admin, Finance (A)" with a matching page spec. The new "financially sensitive setting" row added since then reopens the same gap for other settings (F-DOC-197). |
| F-DOC-190 | Resolved | navigation §2.3 has a row "KYC documents, Appeals, Referral, Help and tickets", Owner only. seller-dashboard §3 states the rule as a bullet beside the matrix. That is clear enough, though it is not the matrix row first suggested. |
| F-DOC-191 | Resolved | navigation §2.4 sends unverified phones to `SL-AUTH-VERIFY` first and to 2FA setup after that. The pages-system redirect row defers to §2.4. |
| F-DOC-192 | Resolved | GST-3a in checkout-orders is the domain rule. `SF-CHK-ADDR` agrees. |
| F-DOC-193 | Partly resolved | SEL-6 now defines uniqueness, transliteration, collisions, reserved words and the Seller Manager's correction on `AD-USR-SELLER`. IA-10 agrees. The `AD-USR-SELLER` page spec does not list the action (F-DOC-198). |
| F-DOC-194 | Resolved | document-control §3.2 has a 7.3.2 row. |
| F-DOC-195 | Resolved | SEL-9 names `PENDING_SELLER_CONFIRMATION`, says the check runs when vacation is turned on and again at a scheduled start, and covers sub-orders that arrive later. |
| F-DOC-196 | Resolved | The T-0061 Source text says the questions were decided in ADR-0007 and that question 9 and wider staff access are held in T-0064. |

ADR-0007 and the PRD agree on all 18 questions. Every "Where" entry was checked against the changed rule, and the ADR wording matches the rule text, including Q7 (lock when the market is enabled, enforced by `backoffice`), Q11, Q14 and Q15 (SES-5), and Q18.

## Verdict
approve with findings

## Findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| F-DOC-197 | minor | 05-trust/admin-governance.md §3, new row "Financially sensitive setting change"; §2.1 matrix rows "Platform settings" (Finance "R, A (tax)") and "Promotions, loyalty, ads" (Finance R); §5 bullet 2; 09/pages-admin-growth-settings.md `AD-SET-SLA` ("dual control for escrow and order timers"); 09/pages-admin-finance-risk.md `AD-RISK-COD` ("dual control where configured") | (1) The new §3 row makes Finance the approver for escrow hold, COD fee, shipping rates and loyalty rates. In the matrix, Finance has A on Platform settings for tax only and no A on "Promotions, loyalty, ads". Yet the matrix note says the A marks are the §3 approvals. This is the same gap as F-DOC-189, now for these settings. (2) There are now three lists of dual-controlled settings, and they differ. §3: payout cycle, escrow hold, COD limits and fee, shipping rates, loyalty rates. §5 bullet 2: thresholds, commission, payout cycle, escrow hold, COD limits (no fee, shipping or loyalty). Page specs: `AD-SET-SLA` also puts order timers under dual control, and no §3 row names an approver for them. `AD-RISK-COD` says "where configured", while §3 makes it unconditional. An implementer of the approvals inbox cannot tell which list is authoritative. | Make §3 the single list. Have §5 bullet 2 refer to it instead of listing settings. Either add order timers to the row or drop them from `AD-SET-SLA`, and remove "where configured" from `AD-RISK-COD`. Widen Finance's A in the matrix to match the row, for example "R, A (tax, financially sensitive settings)" on Platform settings and A on "Promotions, loyalty, ads". |
| F-DOC-198 | minor | 09/pages-admin-operations.md:28 (`AD-USR-SELLER`); 03-sellers/seller-accounts-kyc.md SEL-6 | SEL-6 says "The Seller Manager may correct a slug on `AD-USR-SELLER`". That page spec does not list a "Correct slug" action and does not cite SEL-6. Since its actions are "shown by role", a design brief (T-0019) written from the page spec would leave the action out. | Add "correct store slug (Seller Manager; holds until the next name change)" to the Actions of `AD-USR-SELLER`, and add SEL-6 to its Rules. |
| F-DOC-199 | minor | ADR-0007 Consequences ("the current documents already give Support read access to the delivery log"); 09/pages-admin-growth-settings.md:32 (`AD-NOT-LOG` Actions: "Resend a transactional message") | The ADR describes Support's current access as "read access" and recommends confirming it. The `AD-NOT-LOG` spec also gives Support a write action, resending transactional messages, which F-SEC-016 also named. T-0064 sends the owner to this paragraph for the recommendation, so the owner would rule on an incomplete account of the access in place. ADR-0007 is append-only, so a follow-up note is needed. | In T-0064's row, or in a dated note appended to ADR-0007, state that Support currently has read access plus "Resend a transactional message", and make the recommendation cover both. |

## Not reviewed

- Whether the decisions are right on security or architecture grounds, and whether F-SEC-016/017 and F-ARCH-037 to F-ARCH-048 are resolved. Those belong to the `security-reviewer` and `architecture-reviewer` re-reviews.
- `AD-SET-LOYALTY` shows "the values of `AD-LOY-CONFIG` grouped for Super Admin", so both Super Admin and Marketing can edit loyalty rates. §5 and the §3 row ("the editing role") tolerate this, so it is not raised as a finding. A design brief should make sure both pages use the same dual-control path.
- Whether the valid findings of the three T-0061 reports have their own rows in `MASTER_TASKS.md`. They were fixed within T-0061, as in earlier tasks (for example T-0018), so this was not treated as a finding.
- The Graphify graph was not used. Cross-document effects were traced with plain search for the rule IDs, Page IDs and terms in the diff.

## Disposition (added by the author, 2026-11-18)

| Finding | Disposition |
|---|---|
| F-DOC-197 | Fixed: one list in admin-governance §3, linked from §5, the matrix and the page specs |
| F-DOC-198 | Fixed: `AD-USR-SELLER` lists the slug correction (SEL-6) |
| F-DOC-199 | Fixed: the T-0064 row states that the `AD-NOT-LOG` spec already lets Support read and resend |
