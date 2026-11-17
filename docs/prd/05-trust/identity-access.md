# Identity, Accounts & Access Separation

**Authoritative for:** account types and realms, the one-email-one-account rule, identifiers and canonicalisation, registration and login, OTP, sessions and tokens, 2FA, origin isolation, account lifecycle.
**Owner mandate:** a customer cannot open a seller account with the email used for a customer account, and vice versa.
**Related:** [security](security.md) · [admin-governance](admin-governance.md) · [api-standards](../06-platform/api-standards.md) · [mobile-flutter](../07-clients/mobile-flutter.md) · [privacy-audit](privacy-audit.md)

---

## 1. Account types

| Realm | Who | Created by | Login surface | Audience |
|---|---|---|---|---|
| `CUSTOMER` | Shoppers | Self-registration or guest checkout | Storefront | `storefront` |
| `SELLER` (owner or staff) | Store owners and their staff | Self-registration (owner); invitation (staff, P1) | Seller Dashboard | `seller` |
| `ADMIN` | Nyazek staff | Super Admin invitation only | Admin Panel | `admin` |

Each account has its own record, credentials, sessions and permissions. Accounts in different realms can never be linked or merged and share no session, profile, order history, wallet or loyalty points.

## 2. Identifiers

| Realm | Email | Phone |
|---|---|---|
| Customer | Optional. If provided it must be verified before it can be used for login, receipts or recovery | Required and OTP-verified before any order |
| Seller owner and staff | Required and verified | Required and verified |
| Admin | Required and verified | Optional (used for security alerts) |

**Change from v6 (ratification: D-23).** v6 required email verification before a registered customer could order but exempted guests, who need only a phone. The exemption made the rule pointless (anyone could check out as a guest) and blocked phone-first customers. The order gate is now a verified phone for everyone; email is optional for customers.

## 3. Business rules

| ID | Rule |
|---|---|
| ID-1 | One email address can be bound to exactly one account across all realms. A customer account cannot use an email held by a seller, staff or admin account, and the reverse. |
| ID-2 | The rule applies at registration, email addition or change, social login (the email returned by the provider), invitation acceptance and any admin-assisted correction. |
| ID-3 | A seller account is never an upgrade of a customer account. A person who buys and sells uses two emails and two accounts. Support cannot merge or link accounts. |
| ID-4 | Emails are compared in canonical form (§3.1). |
| ID-5 | Only a **verified** email holds a claim. Unverified registrations do not block anyone. When two registrations race for one email, the first to verify wins and the other is invalidated. |
| ID-6 | Seller staff follow the same rule; a staff member who shops on Nyazek uses a different email for the customer account. |
| ID-7 | Admin accounts exist by invitation only; the invited email must be unclaimed at invitation and at acceptance. |
| ID-8 | When an account is closed, its email and phone claims are released after `cfg:identity.claim_cooldown_days` (default 90). For sellers the cool-down starts when final settlement completes. Re-registration creates a new account with no data carried over. |
| ID-9 | Device, IP, phone, payment-instrument, refund-account and address signals are compared between customer and seller accounts to detect self-dealing ([fraud-risk](fraud-risk.md) §5). |
| ID-10 | Phone numbers used for login or verification are exclusive across realms (recommended default, D-07). A seller's public store contact number is a display field, not an identifier. Consequence: a seller cannot shop as a guest with the seller login phone. |
| ID-11 | Customers must confirm they are at least 18 years old at registration and guest checkout. |

v6 kept seller emails blocked "until financial retention duties are complete", which could mean seven years. Retaining financial records does not require holding the identifier claim; ID-8 uses one cool-down for all realms.

### 3.1 Canonicalisation

- Email: trim; Unicode NFKC; lower-case local part and domain; internationalised domains to punycode; remove any `+tag` for every domain; remove dots in the local part for `gmail.com` and `googlemail.com` only. Both `email_original` (display, sending) and `email_canonical` (uniqueness) are stored.
- Phone: parse to E.164; accept Arabic-Indic digits and local formats (`07…`, `+9647…`, `009647…`); valid mobile ranges are defined per market, and only Iraqi mobile ranges are accepted for login identifiers at launch.
- Known limits: custom-domain aliases, catch-all domains and disposable mailboxes cannot be detected by string rules. Mitigations: mandatory verification, a disposable-domain blocklist for seller registration, KYC duplicate signals.

### 3.2 Enforcement

- The Identity module owns an `identity_claim` table: `claimId, accountId, realm, kind (EMAIL|PHONE), value_canonical, value_original, verified_at, released_at`.
- A partial unique index on `(kind, value_canonical)` where `verified_at IS NOT NULL AND released_at IS NULL` enforces the rule in the database.
- An account is created with unverified claims. Verification sets `verified_at` in one transaction; the unique index makes a concurrent second verification fail, and that account's pending claim is invalidated.
- Unverified accounts and claims are purged after `cfg:identity.unverified_ttl_hours` (default 72).

v6 said both that only verified emails hold claims and that the claim is inserted with the account so that simultaneous registrations cannot both succeed. Those statements conflict; the sequence above is the precise behaviour.

## 4. Registration, login and recovery

| Flow | Customer | Seller | Admin |
|---|---|---|---|
| Register | Phone + OTP (password optional), or email + password + phone OTP | Email + password + phone, both verified | Invitation link → set password → enrol 2FA |
| Login | Phone + OTP, or email/phone + password | Email + password, then 2FA | Email + password, then 2FA (or SSO if enabled) |
| Social login | Google and Facebook (P0). Sign in with Apple is added with the iOS app (required by App Store rules when other social logins are offered) | Not available (D-08) | Not available |
| Recovery | OTP to verified phone, or link to verified email | Link to verified email plus 2FA or a recovery code | Password and 2FA reset initiated by a Super Admin and approved by a second Super Admin; the account, its roles and its audit history are kept |

- AUTH-1 Responses to registration, login, email check and password reset are identical in content and timing whether or not the identifier exists. There is no live "already registered" check while typing.
- AUTH-2 Conflict message for any claim conflict, in every flow. English: "This email address can't be used to create this type of account. Please use a different email address." Arabic: "لا يمكن استخدام هذا البريد الإلكتروني لإنشاء هذا النوع من الحسابات. يرجى استخدام بريد إلكتروني آخر." An equivalent message exists for phone numbers. The message never says which realm holds the identifier. To avoid enumeration it is shown only after the applicant has proved control of the identifier (clicked the verification link or entered the OTP).
- AUTH-3 Realm-scoped login: customer credentials submitted to the seller login fail exactly like a wrong password.
- AUTH-4 Social login: if the provider's email is claimed by another realm, the conflict message is shown and nothing is created or linked. A provider that returns no email leads to phone verification instead.
- AUTH-5 Email change: re-authentication, verification link to the new address, uniqueness re-checked at confirmation, the old address notified and able to revert for 7 days. Phone change: OTP to the new number plus re-authentication; the old number is notified.
- AUTH-6 Passwords: minimum 8 characters for customers and 12 for sellers and admins; no composition rules; checked against breached-password lists; hashed with Argon2id; never logged.
- AUTH-7 Abuse controls: per-identifier and per-IP rate limits, progressive delays, Turnstile challenge after repeated failures, temporary lock with notification.

### 4.1 OTP

- 6 digits, valid 5 minutes, single use, maximum 5 attempts per code, resend cool-down 60 seconds, daily cap per phone `cfg:identity.otp_daily_cap` (default 10), stored hashed, bound to the purpose and the session that requested it.
- SMS through the primary aggregator with automatic fallback; delivery success is a monitored, paged metric.
- OTP SMS cost and SMS-pumping fraud are controlled by per-IP and per-prefix limits and by requiring a Turnstile pass before the first send from a new device.

### 4.2 Recycled phone numbers

Carriers reassign numbers. For a customer account that has had no sign-in for `cfg:identity.phone_stale_months` (default 12), an OTP alone does not restore access to saved addresses, refund accounts, order history or points: the person must also confirm a second factor (verified email, password, or details of a past order). Failing that, the old account is closed and a new one is created for the number. This rule is referred to as **ID-REC-1** and applies to every OTP sign-in path, including guest checkout (GST-2) and order lookup.

## 5. Sessions and tokens

| Client | Mechanism |
|---|---|
| Web apps | Opaque session ID in a host-only cookie: `__Host-` prefix, `Secure`, `HttpOnly`, no `Domain`, separate name per origin; `SameSite=Lax` on the Storefront, `Strict` on Seller and Admin. Sessions are rows in PostgreSQL (cached), revocable immediately |
| Flutter apps | Access token (signed JWT, lifetime 15 minutes) and rotating refresh token (opaque, stored in Keychain / Keystore). Refresh-token reuse revokes the whole device session and alerts the user |

- SES-1 Every session and token is bound to one realm and one audience. Each endpoint accepts exactly one audience ([api-standards](../06-platform/api-standards.md) API-1).
- SES-2 Lifetimes: customer web sessions 30 days sliding; seller 12 hours idle and 7 days absolute; admin 30 minutes idle and 12 hours absolute (`cfg:identity.session_*`). Mobile refresh tokens: customer 60 days sliding; seller bound to the seller limits above (7 days absolute); admins have no mobile sessions.
- SES-3 Cookie-authenticated state-changing requests require a CSRF token (double-submit) and pass an `Origin` check.
- SES-4 Users see their devices and sessions and can sign out one or all. Password change, 2FA reset and suspected compromise revoke all sessions.
- SES-5 Step-up authentication (password or 2FA again) is required for: payout destination changes, email or phone change, viewing recovery codes, staff role changes, and for admins before dual-control approvals.
- SES-6 New-device sign-in sends a security notification.

## 6. Origin isolation

- Three web origins: `www` (Storefront), `seller`, `admin` (decision D-16, decided by ADR-0004). Seller-authored content is rendered on the Storefront; separate origins ensure a script-injection flaw there cannot reach seller or admin sessions.
- Each origin reaches the API on its own `/api` path, so cookies are first-party and host-only ([architecture](../06-platform/architecture.md) §2).
- CORS on `api.<domain>` allows no browser origins with credentials; it serves bearer-token clients and webhooks.
- Each origin has its own content-security policy. The Admin origin is reachable only through zero-trust access (identity-aware proxy with device and location policy), which replaces v6's "IP allow-list or VPN".

## 7. Two-factor authentication

| Realm | Requirement | Methods |
|---|---|---|
| Admin | Mandatory | TOTP or passkey (WebAuthn); SMS not permitted |
| Seller owner and staff | Mandatory | TOTP (preferred) or SMS OTP; recovery codes issued at enrolment |
| Customer | Optional (P1) | TOTP or SMS OTP |

Seller 2FA reset without recovery codes requires identity re-verification by the Seller Manager.

## 8. Account lifecycle

- States: `PENDING_VERIFICATION → ACTIVE ⇄ LOCKED` (security), `→ SUSPENDED` (risk or admin, customer realm; seller states are in [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) §5), `→ CLOSED`.
- Deletion requested by the user is blocked while orders, returns, disputes or balances are open; afterwards the profile is anonymised and records under legal retention are kept in pseudonymous form ([privacy-audit](privacy-audit.md) §3).
- An in-app account-deletion flow exists in the API and web from launch (required by both app stores for the later apps).

## 9. Edge cases

- A customer who later wants to sell creates a new seller account with a different email; a help article explains why accounts cannot be merged.
- Family members or business partners cannot share one email; each person needs their own.
- A mistyped email is corrected before verification; after verification the email-change flow applies.
- A seller's staff member who leaves keeps no access: the owner removes the staff account, which is closed and its claims released after the cool-down.
- Break-glass admin access uses a separate, logged account with its own unique email.

## 10. Acceptance criteria

- Given a verified customer email A, a seller registration with A or any case, dot (Gmail) or `+tag` variant fails with the generic message after verification is attempted, and no seller account becomes active.
- The same holds in reverse, for staff and admin invitations, for social login and for email change.
- Two concurrent verifications of one canonical email result in exactly one verified claim (database-level test).
- A customer session or token on any seller or admin endpoint returns `403`.
- A closed account's email cannot be registered again during the cool-down.
- Registration and password-reset responses are indistinguishable for existing and non-existing identifiers (content and timing test).
- Reusing a rotated refresh token revokes the session family.
