# Security review — T-0061: Decisions raised by T-0060 (ADR-0007), re-review
Date: 2026-11-18 · Reviewer agent: security-reviewer · Scope: `git diff yasir` on branch `task/T-0061-t0060-decisions` (uncommitted), focused on the revised texts: `identity-access.md` SES-5 (with AUTH-5 and §4), `admin-governance.md` §2.1 matrix, §3 dual-control table and §5, `seller-accounts-kyc.md` SEL-6 and SEL-9, `pages-seller-operations.md` `SL-AUTH-VERIFY`, `navigation.md` §2.4, `web-apps.md` §4.3, `ia-model.md` IA-10, `pages-storefront-discovery.md` `SF-PDP`, `pages-admin-growth-settings.md`, `shared-components.md` Step-up prompt, sitemap admin settings rows, `configuration-register.md`, ADR-0007 and the T-0064 row in `tasks/MASTER_TASKS.md` · Follows up: [2026-11-18-T-0061-decisions.md](2026-11-18-T-0061-decisions.md)

## Verdict
approve with findings

Both major findings are resolved. F-SEC-016: the documents now agree that Support already has read access to the delivery log (NTF-5, sitemap `AD-NOT-LOG`). ADR-0007 Consequences says so, and T-0064 asks the owner to confirm, with `AD-NOT-CAMP` in its scope. F-SEC-017: SES-5 now requires step-up before a password, 2FA or email is added or changed, and a factor added in the session cannot satisfy a step-up in that session. A stolen Customer session can no longer create its own step-up factor.

The minor and note findings are resolved, with the residuals listed below. The fixes leave two minor defects (F-SEC-026, F-SEC-027). Neither blocks `done`.

### Status of earlier findings
| Finding | Status | Evidence |
|---|---|---|
| F-SEC-016 | resolved | ADR-0007 Consequences; T-0064 row names the delivery log, `AD-SET-NOTIF` and `AD-NOT-CAMP`. Residual wording only: the ADR header and question 9 row still say question 9 "grants access", although Consequences correctly says the access already exists. This is a documentation point with no security effect. |
| F-SEC-017 | resolved | SES-5: "adding or changing a password, 2FA or email"; "A factor added in the current session cannot satisfy a step-up in that session." |
| F-SEC-018 | resolved | SES-5: 2FA for sellers and admins ("password alone is not enough"); refund accounts (PAY-17) and data-subject requests (DSR-2) are listed. |
| F-SEC-019 | resolved | SES-5: the step-up OTP names the action and is valid only for it; the email is notified with a revert link; refund-account changes are held for `cfg:identity.phone_change_cooldown_hours` (72, in the register). Not taken: a lost-number recovery path and a hold on points or balances. Both were suggestions, and the scenario's main harm (redirecting refunds) is now contained. |
| F-SEC-020 | resolved, with residual F-SEC-026 | §5 names the editing role for each page with its own values; the owner role is notified of every change; the new §3 row names Finance as approver of financially sensitive settings (Super Admin when Finance edits); tax has a Finance approval in §2.1, §3, `AD-SET-TAX` and the sitemap. The `AD-SET-LOYALTY` page spec was not aligned (F-SEC-026). |
| F-SEC-021 | resolved, with residual F-SEC-027 | `SL-AUTH-VERIFY`: the registration phone cannot be changed at this step and the API refuses onboarding until it is verified; navigation §2.4 routes there before 2FA setup. A password-only attacker cannot substitute their own phone in the app. The replacement path "through Support" is undefined (F-SEC-027). |
| F-SEC-022 | resolved | SEL-6 and IA-10: former slugs stay reserved to the store and are never reassigned; managed reserved-word list. |
| F-SEC-023 | resolved | §3 row: the target can be neither requester nor approver; the owner performs the reset when fewer than two other Super Admins exist. The mechanism the owner uses is not stated; it should be the break-glass procedure (§4) when the runbook is written. This is not a finding. |
| F-SEC-024 | resolved | web-apps §4.3 and `SF-PDP`: a policy or legal takedown shows only the generic notice; unpublished `404`/`noindex`, archived `410`/`noindex`; events purge cache and index. |
| F-SEC-025 | resolved | ADR-0007 question 3 and `AD-SYS-HEALTH`: job payloads stay out of telemetry (SEC-21); engineers use the observability backend. |

## Findings
| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| F-SEC-026 | minor | `pages-admin-growth-settings.md` `AD-SET-LOYALTY` ("Edit"); `admin-governance.md` §5 first bullet and §3 new row | `AD-SET-LOYALTY` still offers a plain "Edit" of "the values of `AD-LOY-CONFIG`". `AD-LOY-CONFIG` edits the loyalty rates under dual control, and §3 now requires a Finance approval for loyalty rates. §5 says `AD-SET-*` values are edited by the Super Admin, while loyalty rates are edited by Marketing on `AD-LOY-CONFIG`. So two pages edit the same money-relevant values, and only one of them states dual control. The §3 row is binding per setting, but implementers build page actions from the page spec. **Failure scenario:** the Settings page is built as specified and a single Super Admin raises the earn rate or the referral reward through `AD-SET-LOYALTY`. The change is not approved by Finance and Marketing never sees it beforehand, so points liability grows unchecked. This is the bypass F-SEC-020(c) named. | Make `AD-SET-LOYALTY` either read-only for the rates (programme on or off only, with a link to `AD-LOY-CONFIG`) or "Edit (dual control for rates, admin-governance §3)". In §5, state which of the two pages is the editor of loyalty rates. Optionally align the second §5 bullet with the full list in the §3 row. |
| F-SEC-027 | minor | `pages-seller-operations.md` `SL-AUTH-VERIFY` ("a change goes through Support"); `admin-governance.md` §2.1 (Support has R on "Sellers and KYC"); `admin-panel.md` ADM-6 | The fix for F-SEC-021 routes a change of the unverified registration phone to Support. No document defines that path. Support has read-only access to sellers in the RBAC matrix, ADM-6 forbids Support to change login identifiers (for Customers), and nothing says how the caller is verified. **Failure scenario:** someone holding a new seller's phished password contacts Support during onboarding, says the phone was mistyped and gives their own number. With no defined verification, an agent changes it (or escalates to whoever can). The attacker verifies the phone, enrols 2FA and owns the account before KYC, which is the F-SEC-021 scenario again through a human channel. If instead nobody may make the change, a seller who mistyped the phone has no way forward. | Define the path in identity-access or seller-accounts-kyc. One option is that the seller restarts registration (the unverified account expires and its claims are released). Another is a self-service change confirmed by a fresh link to the verified email, which notifies the email and is held to the AUTH-7 and §4.1 limits. If staff are involved, name the role that has `M` on sellers (Seller Manager), require proof of control of the verified email, and audit the change. Remove the reference to Support. |

## Not reviewed
- There is no code, configuration or dependency in scope, so the checklist items for secrets, supply chain, CI and enforcing code are not applicable.
- Changes outside the listed texts (the configuration-register additions other than the cool-down key, CMS limits, low-stock threshold, COD fee mechanism, SEL-9 vacation guard) were read for security impact only. SEL-9 and the COD-fee change open no new exposure. The `events` owner change and the generator's path-separator change were already found sound.

## Disposition (added by the author, 2026-11-18)

| Finding | Disposition |
|---|---|
| F-SEC-026 | Fixed: `AD-SET-LOYALTY` shows the values read-only and links to `AD-LOY-CONFIG`; admin-governance §5 says loyalty rates are edited only there |
| F-SEC-027 | Fixed: the registration phone can be changed at `SL-AUTH-VERIFY` only after a fresh link to the verified email, audited; Support is no longer named |
