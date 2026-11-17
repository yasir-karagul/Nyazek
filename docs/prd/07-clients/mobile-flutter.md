# Mobile Applications (Flutter)

**Authoritative for:** mobile technology, what is shared with the web, mobile-readiness requirements for the backend, app architecture, the readiness checklist and the app roadmap.
**Owner mandates:** the platform must be ready for Android and iOS apps; the mobile technology is Flutter; React Native is not used.
**Related:** [api-standards](../06-platform/api-standards.md) · [identity-access](../05-trust/identity-access.md) §5 · [design-system-ui-workflow](design-system-ui-workflow.md) · [notifications-messaging](../02-commerce/notifications-messaging.md)

---

## 1. Scope and timing

- The native apps are **not** part of v1.0. They are built after launch (P2): the customer app first, then the seller companion app.
- **Readiness is P0:** everything in §5 is verified before launch so the apps can be added without changing the backend.

## 2. Technology

| Concern | Choice |
|---|---|
| Framework and language | Flutter (stable channel), Dart 3 |
| Minimum operating systems | Proposed: Android 8.0 (API 26) and iOS 15; confirmed from real device data when mobile work starts |
| Apps | `apps/mobile_customer`, `apps/mobile_seller`; shared Dart packages under `packages/dart/` |
| State management | Riverpod |
| Navigation and deep links | go_router with typed routes that mirror Storefront URLs |
| Networking | dio with the generated API client (`packages/dart/nyazek_api`), interceptors for auth, idempotency keys, client headers, retries |
| Secure storage | flutter_secure_storage (Keychain / Keystore) |
| Push | Firebase Cloud Messaging (APNs for iOS through FCM) |
| Localisation | `flutter_localizations` with ARB files generated from the shared catalogues |
| Crash and error reporting | Sentry SDK for Flutter |
| Builds and release | GitHub Actions with macOS runners for iOS; Fastlane for signing and store upload; staged rollouts |
| Tests | Unit and widget tests, golden tests in Arabic and English, integration tests on emulators |

Flutter Web is not used: the web apps remain React-based for SEO and bundle size.

## 3. What is shared with the web

TypeScript code cannot be imported by Dart. Sharing happens through language-neutral sources of truth, each with a generator and a CI check that generated output is current.

| Source of truth | Web output | Flutter output |
|---|---|---|
| OpenAPI 3.1 contract (`packages/contracts/openapi.json`) | TypeScript client | Dart client |
| Design tokens (`packages/design-tokens/tokens.json`) | CSS variables and Tailwind theme | Dart `ThemeData`, colour, spacing and typography constants |
| Message catalogues (`packages/i18n`, ICU format) | JSON for `next-intl` / `use-intl` | ARB files |
| Analytics event taxonomy (`packages/contracts/analytics`) | Typed helpers | Dart constants and helpers |
| Error codes | Typed map of code → message key | Same, generated |
| Formatting test vectors (money, dates, phone display) | Run by web tests | Run by Dart tests |

Because the API returns computed amounts, eligibility and state, the apps need no business logic and no money arithmetic; the Dart side formats values only ([architecture](../06-platform/architecture.md) ARC-6).

## 4. App architecture rules

- MOB-1 Feature-first folders; each feature has presentation, application (state) and data (API) layers. No feature calls another feature's data layer directly.
- MOB-2 Authentication uses short-lived access tokens and rotating refresh tokens stored only in secure storage ([identity-access](../05-trust/identity-access.md) §5). Social login uses the system browser with PKCE. Sign in with Apple is offered on iOS alongside Google and Facebook.
- MOB-3 At start and on resume the app calls `GET /v1/app-config`: below the minimum version it shows a blocking update screen; in maintenance it shows the maintenance screen.
- MOB-4 Language and direction follow the user's setting and switch at runtime without restarting the app. Arabic is the default.
- MOB-5 Fonts for Arabic and Latin are bundled; the theme is generated from tokens; light theme only (the app declares a light interface style).
- MOB-6 Payments by wallet or card open the provider's page in the system browser or hand off to the provider's app, and return through a deep link; the app then polls payment status. The redirect is never proof of payment.
- MOB-7 Network behaviour: timeouts, retry with idempotency keys, cached last-known data for lists, clear offline states; no optimistic updates for money or order state.
- MOB-8 Push: device token registered per account and device, removed at sign-out; payloads carry a deep-link route and no personal data; notification permission is requested in context, not at first launch.
- MOB-9 Store compliance: in-app account deletion, privacy-policy link, accurate data-safety declarations; physical goods are paid outside the stores' in-app purchase systems.
- MOB-10 Security (with the apps): certificate pinning for the API host, root and jailbreak signals reported to Risk, screenshots disabled on sensitive seller screens, biometric re-authentication for payout actions in the seller app.
- MOB-11 Accessibility: semantics labels, scalable text, minimum touch targets 48 × 48 dp.

## 5. Mobile-readiness checklist (P0, verified before launch)

1. The OpenAPI contract is published and all three web apps use generated clients only.
2. The API authenticates with bearer tokens and refresh rotation on `api.<domain>`; no capability depends on cookies.
3. `GET /v1/app-config`, feature flags and the forced-update policy exist.
4. The device-token registry and the push port exist in Notifications (provider calls may be stubbed).
5. Storefront routes are stable and human-readable; the app-link verification files are served.
6. Message catalogues, design tokens and error codes are generated for Dart in CI.
7. The analytics taxonomy is defined in the contracts package.
8. The account-deletion API exists.
9. A minimal Flutter app in `apps/mobile_customer` builds for Android and iOS in CI, signs in against staging with the generated client, renders a screen in Arabic RTL using generated tokens and catalogues, and receives a test push.
10. No web app contains a server action or direct data access that bypasses the API.
11. Every list endpoint has cursor pagination and image variants; every creating `POST` accepts an idempotency key.

Item 9 replaces v6's "empty Expo app" spike and is a Phase 1 deliverable.

## 6. Roadmap after launch

| Phase | Scope | Prerequisites |
|---|---|---|
| M1 Customer app | Home, search, category, product, store, favourites, cart, checkout with payment hand-off, orders and tracking, returns, disputes, reviews, addresses, notifications, profile and security | Checklist complete; design tokens and Arabic typography final (D-19); Apple and Google developer accounts |
| M2 Seller companion app | Order alerts and SLA countdown, accept and mark ready, stock and price updates, barcode scan to create offers, notifications | Seller API coverage; biometric re-authentication |
| M3 Enhancements | Biometrics for customers, campaign deep links, in-app support, offline improvements | Production data from M1 and M2 |

Web-only by design: Admin Panel, bulk import, financial statements, KYC document upload (KYC upload from the seller app is a later option).

## 7. Toolchain notes

- The Dev Container includes the Flutter SDK and Android toolchain. iOS builds require macOS and Xcode, provided by CI macOS runners; local iOS development needs a Mac.
- Flutter version is pinned (for example with FVM) and upgraded on an N-1 cadence after each stable release.
- Developer accounts (Apple organisation enrolment, Google Play) are long-lead items tracked in the release plan.

## 8. Acceptance criteria

- The checklist in §5 is signed off as a launch gate.
- Generated Dart artefacts are reproducible: CI fails if regenerating changes any file.
- The spike app switches between Arabic and English at runtime with correct direction and fonts.
