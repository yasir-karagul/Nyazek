# Security review — T-0061: Decisions raised by T-0060 (ADR-0007), second re-review
Date: 2026-11-18 · Reviewer agent: security-reviewer · Scope: `git diff yasir` on branch `task/T-0061-t0060-decisions` (uncommitted), limited to the fixes listed in the Disposition tables of the three re-review reports: `pages-admin-growth-settings.md` `AD-SET-LOYALTY`, `AD-SET-SLA`, `AD-SET-SHIP`, `AD-LOY-CONFIG`; `pages-admin-finance-risk.md` `AD-RISK-COD`; `admin-governance.md` §3 and §5; `pages-seller-operations.md` `SL-AUTH-VERIFY`; ADR-0007 question 13; `seller-performance.md` PRF-4; `seller-accounts-kyc.md` SEL-6 and SEL-9; `checkout-orders.md` §5 and §6 rows; `pages-admin-operations.md` `AD-USR-SELLER`; read against `identity-access.md` AUTH-5, AUTH-7, §4.1 and SES-5 · Follows up: [2026-11-18-T-0061-decisions-rereview.md](2026-11-18-T-0061-decisions-rereview.md)

## Verdict
approve with findings

F-SEC-026 and F-SEC-027 are resolved. None of the other dispositions introduces a critical or major security problem. The new phone-change path leaves one minor gap (F-SEC-028), and there is one note (F-SEC-029). Neither blocks `done`.

### Status of earlier findings
| Finding | Status | Evidence |
|---|---|---|
| F-SEC-026 | resolved | `AD-SET-LOYALTY` shows the `AD-LOY-CONFIG` values read-only, with a link to edit them there under dual control. Its only action is turning the programme on or off. Admin-governance §5 says loyalty rates are edited by Marketing, only on `AD-LOY-CONFIG`. The §3 single list names loyalty rates, with Finance as approver. A single Super Admin can no longer change rates through Settings. |
| F-SEC-027 | resolved, with residual F-SEC-028 | `SL-AUTH-VERIFY` and ADR-0007 question 13: the registration phone can be changed only after a fresh confirmation link to the verified email, and the change is audited. The API refuses onboarding until the phone is verified. Support is no longer named. An attacker who has only the password cannot complete the change without the email. OTP sends to the new number fall under §4.1 (daily cap per phone, purpose and session binding, Turnstile before the first send) and AUTH-7. |

### Other dispositions checked
| Item | Result |
|---|---|
| PRF-4 vacation exclusion (F-ARCH-049) | No new exposure. While a seller is on vacation, offers are not purchasable, so only sub-orders already in flight can reach the seller (a released COD hold or a late prepaid payment). SEL-9 stops vacation from starting while any sub-order awaits confirmation. The customer is refunded through the normal timeout path. The exclusion is narrow and recorded with a reason; see note F-SEC-029. |
| Single dual-control list, admin-governance §3 (F-ARCH-050, F-DOC-197) | Sound. One row covers payout cycle, escrow hold, order and payment timers, COD limits and fee, shipping rates and loyalty rates. The requester is the editing role, and the approver is Finance, or the Super Admin when Finance edits. Because the general §3 rule applies, no one can approve their own request. §5 links to the list, and the commission schedule and thresholds keep their own rows (DC-2). |
| `AD-SET-SLA` | Consistent with §3: dual control covers escrow hold and the order and payment timers. Seller confirmation and hand-over times stay single-edit by the Super Admin. They affect timing, not money movement, and are audited (§4). |
| `AD-RISK-COD` | Consistent with §3: dual control covers COD limits, and the editor is Fraud/Risk (§5). The other COD rules stay with the Risk owner role, as accepted earlier. The COD fee is on `AD-SET-SHIP` under dual control and is in the §3 list. |
| `AD-USR-SELLER` slug correction (F-DOC-198) | No new exposure. The action is limited to the Seller Manager. The SEL-6 constraints apply to every slug: uniqueness, former slugs reserved to their store, and the reserved-word list. Admin actions are audited with before and after values (admin-governance §4). |

## Findings
| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| F-SEC-028 | minor | `pages-seller-operations.md` `SL-AUTH-VERIFY`; ADR-0007 question 13 | The texts do not say how the email confirmation is bound to the new phone number. They do not say where the new number is entered (before the link is sent, in the requesting session, or after the link is opened), or whether the email names the change. **Failure scenario:** an attacker holding a new seller's phished password signs in, sees `SL-AUTH-VERIFY`, asks to change the phone and enters their own number. The real seller is in the middle of registration and expects verification emails, so they click the "confirm" link. If the confirmation is bound only to the request, the attacker's number is accepted. The attacker verifies it by OTP, enrols 2FA and takes over the account before KYC, which is the F-SEC-021 scenario again through link confirmation. | State that the email names the action and shows the new number masked, with an "I did not request this" option that cancels the change and prompts a password reset. Alternatively, have the new number entered only in the session opened from the link. Either way, the link is single-use, short-lived and bound to the account. |
| F-SEC-029 | note | `seller-performance.md` PRF-4; `seller-accounts-kyc.md` SEL-9 | A seller who wants to drop an in-flight COD-held or late-paid sub-order without a penalty can turn vacation on before it reaches confirmation. SEL-9 only blocks vacation while a sub-order is already in `PENDING_SELLER_CONFIRMATION`. The effect is bounded by the maximum vacation duration, offers are not purchasable during vacation, and the customer is refunded. No action is required now. Consider having seller-performance monitoring flag frequent vacations that coincide with excluded timeouts. | — |

## Not reviewed
- There is no code, configuration or dependency in scope, so the checklist items for secrets, supply chain, CI and enforcing code are not applicable.
- Only the dispositions named in the scope were reviewed. The other parts of the diff were covered by the two earlier security reports.

## Disposition (added by the author, 2026-11-18)

| Finding | Disposition |
|---|---|
| F-SEC-028 | Fixed: `SL-AUTH-VERIFY` phone change uses a single-use, short-lived, account-bound email link; the new number is entered only in the session the link opens; the email names the action and offers "I did not request this"; audited |
| F-SEC-029 | No action now (note accepted); candidate signal for seller-performance monitoring |
