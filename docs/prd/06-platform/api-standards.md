# API Standards

**Authoritative for:** API style, versioning, authentication schemes at the transport level, errors, idempotency, pagination, localisation, webhooks and contract tooling.
**Related:** [architecture](architecture.md) · [identity-access](../05-trust/identity-access.md) · [mobile-flutter](../07-clients/mobile-flutter.md) · [testing-quality](../08-engineering/testing-quality.md)

---

## 1. Surfaces

| Surface | Path prefix | Audience | Reachable from |
|---|---|---|---|
| Customer and public | `/v1/*` | `storefront` | `www.<domain>/api`, `api.<domain>` |
| Seller | `/v1/seller/*` | `seller` | `seller.<domain>/api`, `api.<domain>` |
| Admin | `/v1/admin/*` | `admin` | `admin.<domain>/api` only (zero-trust protected) |
| Provider webhooks | `/webhooks/<provider>` | signed provider calls | `api.<domain>` |
| Operations | `/health/live`, `/health/ready` | load balancer | internal |
| App configuration | `GET /v1/app-config` | all clients, unauthenticated | all |

- API-1 Every endpoint declares exactly one audience. The API rejects a session or token whose audience differs, with `403` ([identity-access](../05-trust/identity-access.md) §5).
- API-2 Admin endpoints are not routed on the public API host.

## 2. Versioning and compatibility

- API-3 Major version in the path (`/v1`). Within a major version only additive changes are allowed: new endpoints, new optional request fields, new response fields, new enum values **only where the field is documented as open**.
- API-4 Clients must ignore unknown response fields and treat unknown enum values as a documented fallback. Generated clients are configured accordingly.
- API-5 A breaking change requires `/v2`. The previous major version stays supported for at least 6 months after the next is released, and at most two major versions are live.
- API-6 `GET /v1/app-config` returns, per platform, `minSupportedVersion`, `recommendedVersion`, `maintenance` (boolean, message) and public feature flags. Mobile apps call it at start and on resume; an app below `minSupportedVersion` shows a forced-update screen.
- API-7 Every request carries `X-Client-Platform` (`web-storefront`, `web-seller`, `web-admin`, `android-customer`, `ios-customer`, `android-seller`, `ios-seller`) and `X-Client-Version`. Missing headers are accepted on `/v1` but logged.

## 3. Contract tooling

- Request and response schemas are Zod schemas in `packages/contracts`. NestJS validates with the same schemas.
- OpenAPI 3.1 is generated from the schemas on every build and committed (`packages/contracts/openapi.json`).
- Generated clients: TypeScript (`openapi-typescript` types with a thin fetch client) in `packages/api-client`; Dart (`dio`-based) in `packages/dart/nyazek_api`.
- CI gates: the committed OpenAPI file matches the generated one; `oasdiff` blocks breaking changes on `/v1`; contract tests run the API against the schema.

## 4. Requests and responses

- JSON only (`application/json; charset=utf-8`); file uploads use pre-signed URLs, never multipart through the API.
- Field names are `camelCase`. Timestamps are RFC 3339 UTC strings. IDs are opaque strings.
- Money is an object: `{ "amount": 125000, "currency": "IQD" }` with an integer amount in the currency's platform minor unit (MON-8). `GET /v1/app-config` publishes the currency table (exponent, price step, display format) so clients format without assumptions.
- Enumerations are upper snake case strings.
- Responses never include fields the caller is not authorised to see; there is no client-side filtering of sensitive data.

### 4.1 Errors

Errors follow RFC 9457 problem details with stable machine codes:

```json
{
  "type": "https://docs.nyazek.example/errors/stock-unavailable",
  "title": "Stock unavailable",
  "status": 409,
  "code": "STOCK_UNAVAILABLE",
  "detail": "الكمية المطلوبة غير متوفرة",
  "correlationId": "…",
  "errors": [{ "field": "lines[0].quantity", "code": "MAX_AVAILABLE", "params": { "available": 2 } }]
}
```

- `code` is the contract; `detail` is localised by `Accept-Language` for display.
- Status usage: `400` malformed, `401` unauthenticated, `403` unauthorised or audience mismatch, `404` not found **or not visible to the caller**, `409` state conflict, `422` validation, `429` rate limited (with `Retry-After`), `5xx` server.
- Object-level authorisation failures on another party's resource return `404`, not `403`, to avoid confirming existence.
- Authentication endpoints return uniform responses that do not reveal whether an identifier exists ([identity-access](../05-trust/identity-access.md) §4).

### 4.2 Idempotency

- API-8 Every `POST` that creates an order, payment, refund, payout, return, dispute, wallet adjustment, coupon redemption or shipment requires an `Idempotency-Key` header (client-generated UUID).
- API-9 The server stores `(principal, endpoint, key) → request hash, response` for 24 hours. A repeat with the same hash returns the stored response; a repeat with a different body returns `409 IDEMPOTENCY_KEY_REUSED`.
- API-10 A request in progress with the same key returns `409 REQUEST_IN_PROGRESS`; clients retry with backoff.

### 4.3 Lists

- Cursor pagination: `?limit=` (default 20, max 100) and `?cursor=`; response `{ "items": [], "nextCursor": "…" | null }`.
- Storefront search and category listings also support page numbers for SEO-friendly URLs, capped at a maximum depth ([search-buy-box](../02-commerce/search-buy-box.md)).
- Filtering uses documented query parameters; sorting uses `?sort=field` or `?sort=-field`.
- Payload budgets: list responses default to compact item shapes (no nested collections); detail endpoints carry the full object. Target compressed size for a 20-item list is under 50 kB.
- Cacheable reads return `ETag`; clients may send `If-None-Match`. Updates to editable resources (offers, addresses, settings) require `If-Match` or a `version` field for optimistic concurrency and return `409 VERSION_CONFLICT` on mismatch.

### 4.4 Localisation

- `Accept-Language: ar` or `en`; default `ar`. Signed-in users' stored preference wins when the header is absent.
- Localised catalogue fields are returned for the requested language with fallback to Arabic; admin and seller editing endpoints return all languages.
- Numbers are returned as numbers; clients format them (Western digits by default). The server accepts Arabic-Indic digits in text inputs and normalises them.
- API-15 Market is separate from language. The market of a request is resolved by the API from the account or, for guests, from the host; clients never choose prices, currency or tax by sending a locale. Market-scoped resources include their market code. Only `IQ` exists at launch.

### 4.5 Images

- Media fields return an object with named variants (`thumb`, `card`, `detail`, `zoom`) and intrinsic sizes, not a single URL, so clients choose by layout and network.

## 5. Rate limiting and abuse

- Limits apply per IP, per account and per endpoint class. Classes and default budgets are configuration ([security](../05-trust/security.md) §6).
- `429` responses include `Retry-After`. Authentication, OTP, checkout initiation, coupon validation, search and review posting have dedicated budgets.

## 6. Real-time updates

- Server-sent events on `/v1/seller/stream` and `/v1/admin/stream` deliver "something changed" signals (new order, SLA tick, queue change); clients refetch through normal endpoints. Polling every 30 seconds is the fallback and the only mechanism required of mobile apps at first release.

## 7. Webhooks (inbound)

- API-11 Each provider adapter verifies the signature, checks a timestamp tolerance of 5 minutes, rejects replays by provider event ID, and applies an IP allow-list where the provider publishes one. For a webhook buffered at the edge during an origin outage, the tolerance and the allow-list apply to the edge receipt time and source address signed by the edge ([ADR-0004](../../adr/0004-technology-stack.md) "Edge buffering of webhooks").
- API-12 The handler stores the raw event and returns `2xx` immediately; processing is asynchronous and idempotent.
- API-13 A browser redirect from a PSP is never proof of payment. Only a verified webhook or a server-to-server status query changes payment state ([payments](../04-finance/payments.md)).
- API-14 Every webhook-driven integration also has a polling or file-based reconciliation fallback.

## 8. Health and configuration

- `/health/live` reports process liveness; `/health/ready` reports database connectivity and migration state. Cache and search outages do not fail readiness.
- All configuration comes from validated environment variables and the `backoffice` configuration store. There are no environment-specific code paths.

## 9. Acceptance criteria

- The three web apps and the Flutter spike use only generated clients.
- Replaying any idempotent `POST` returns the original result and creates no duplicate (automated test per endpoint).
- A customer session calling any `/v1/seller/*` or `/v1/admin/*` endpoint receives `403`; a seller requesting another seller's resource receives `404`.
- `oasdiff` fails a pull request that removes or renames a field on `/v1`.
