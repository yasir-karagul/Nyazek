# Search, Discovery & Buy Box

**Authoritative for:** search behaviour, Arabic handling, ranking, filters, autocomplete, search integrity, Buy Box eligibility, scoring and stability.
**Related:** [catalog-listings](catalog-listings.md) · [advertising](advertising.md) · [seller-performance](../03-sellers/seller-performance.md) · [inventory](inventory.md)

---

## 1. Search

### 1.1 Scope and unit

- SRC-1 The search result unit is the **product** (canonical or seller-owned), not the offer. Each result shows the Buy Box offer's price, seller and delivery estimate (for seller-owned listings, the single offer).
- SRC-2 The index is a derived read model built from events (`product.*`, `offer.*`, `stock.changed`, `buybox.winner_changed`, `review.published`). It can be rebuilt from PostgreSQL at any time.
- SRC-3 Freshness: price, stock and availability changes reach the index within 60 seconds. Cart and checkout never trust the index for price or stock.

### 1.2 Arabic and English handling (P0)

- Arabic-primary analysis with English fallback; both fields are searched for every query.
- Normalisation at index and query time: unify alef forms; ya / alef-maqsura; ta-marbuta / ha; remove diacritics and tatweel; treat Arabic-Indic and Western digits as equal.
- Admin-managed synonyms and transliterations (for example آيفون ↔ iPhone; common Iraqi dialect terms), held per market and applied at query time so changes take effect without reindexing.
- Light Arabic stemming; brand names and model numbers are matched exactly as a boosted field.

### 1.3 Features

| Feature | Priority |
|---|---|
| Full-text search across title, brand, category, key attributes, GTIN and model number | P0 |
| Autocomplete: product titles, categories, brands, ranked by popularity | P0 |
| Filters: category, price range, brand, seller type (1P / 3P), rating, in stock, condition, deliverable to governorate, category attributes | P0 |
| Sort: relevance, price ascending, price descending, newest, best selling, rating | P0 |
| Typo tolerance, "did you mean", zero-result suggestions | P1 |
| Delivery-speed filter (next day / standard) based on the customer's selected governorate | P1 |
| Personalised ordering and personalised autocomplete from the customer's history | P1 |
| Query analytics: top queries, zero-result rate, click-through by position | P1 |
| Semantic (vector) retrieval | P2 |

v6 placed personalised autocomplete at P0. It needs behavioural history that does not exist at launch and consent handling; the non-personalised version is P0 and personalisation moves to P1 (listed for ratification under D-33).

### 1.4 Ranking

Relevance sort uses text relevance (BM25 over weighted fields) multiplied by a quality boost:

`score = textRelevance × (1 + Σ wᵢ × signalᵢ)` with each signal normalised to 0–1.

| Signal | Definition | Initial weight |
|---|---|---|
| Seller performance | Performance score of the Buy Box seller ÷ 100 | `cfg:search.w_performance` (default 0.30) |
| Sales popularity | Units sold in the last 30 days with exponential decay, log-scaled within category | `cfg:search.w_popularity` (default 0.30) |
| Price competitiveness | Buy Box price relative to the median price of the same product type | `cfg:search.w_price` (default 0.20) |
| Rating | Bayesian average of verified product ratings | `cfg:search.w_rating` (default 0.20) |
| Recency | 1 at publication, decaying linearly to 0 over 30 days | `cfg:search.w_recency` (default 0.10) |

Weights are starting values to be tuned in the closed beta. v6 gave qualitative weights ("High", "Medium") that cannot be implemented or tested.

- SRC-4 Out-of-stock products rank after all in-stock results.
- SRC-5 Personalisation (P1) may reorder results only within a band of similar relevance; it can never lift an irrelevant product to the top.
- SRC-6 Sponsored results are inserted in labelled slots ([advertising](advertising.md) §4). Ad spend never affects organic score.

### 1.5 Integrity

- Relisting a product does not reset the recency boost (boost is tied to the canonical product and to the seller's first offer on it).
- Orders flagged as suspicious, cancelled or refunded are excluded from the popularity signal.
- Abnormal sales velocity, click patterns or review bursts are reported to Risk and excluded from signals while under review.
- Search endpoints are rate-limited and protected against scraping ([security](../05-trust/security.md) §6).

### 1.6 Listings and SEO

- Search and category pages have canonical, paginated URLs; deep pagination is capped at `cfg:search.max_page_depth` (default 50 pages).
- Category pages use the same engine with the category as a filter plus that category's attribute filters.

## 2. Buy Box

### 2.1 Scope

- BBX-1 The Buy Box selects the default offer for each **variant of a canonical product**. It does not apply to seller-owned (Type C) listings.
- BBX-2 Only offers in condition `NEW` compete. Offers in other conditions appear under "Other sellers", grouped by condition.

### 2.2 Eligibility

An offer is eligible when all are true:

- `available > 0`;
- offer `ACTIVE` and compliant with price rules;
- seller state `ACTIVE`, or `RESTRICTED` at performance Level 2 only (a seller at Level 3 or 4, with a lapsed document, suspended, or on vacation is not eligible);
- seller performance score ≥ `cfg:buybox.min_performance` (default 40), where sellers without enough history use the neutral score 50 ([seller-performance](../03-sellers/seller-performance.md) §2).

### 2.3 Score

`score = 0.40 × price + 0.35 × performance + 0.20 × delivery + 0.05 × firstParty`, each component 0–100. Weights: `cfg:buybox.w_price` (default 40), `cfg:buybox.w_performance` (default 35), `cfg:buybox.w_delivery` (default 20), `cfg:buybox.w_1p` (default 5).

| Component | Definition |
|---|---|
| Price | `100 × lowestEligiblePrice ÷ offerPrice`, using the price after seller-funded deals. Shipping is standardised and excluded |
| Performance | Seller performance score (for 1P, its computed score, PRF-7); multiplied by `cfg:buybox.level2_factor` (default 0.85) for sellers at Level 2 |
| Delivery | From the offer's handling time (1 to `cfg:orders.max_handling_days`, SLA-6) and the seller's on-time shipment rate: `100 − 20 × (handlingDays − 1)`, floored at 0, then multiplied by the on-time rate over 30 days (neutral 0.9 when no history) |
| First party | 100 for the 1P store, 0 otherwise |

The 1P boost is capped by construction at 5 points: 1P cannot win on the boost alone against a clearly better price and performance. Delivery is destination-independent at launch; destination-aware scoring is P2.

v6 gave the formula without defining scales, so it could not be implemented or tested.

### 2.4 Stability and recalculation

- BBX-3 The current winner keeps the Buy Box unless a challenger's score exceeds it by more than `cfg:buybox.hysteresis_points` (default 3), or the winner becomes ineligible.
- BBX-4 Ties are broken by lower price, then by higher performance score, then by earlier offer creation.
- BBX-5 Recalculation is triggered by price, stock, eligibility or performance-level changes for any offer on the variant, and at least every `cfg:buybox.max_interval_minutes` (default 15). A stock-out or seller restriction triggers immediate recalculation.
- BBX-6 The winner is persisted per variant (not only cached) and published as `buybox.winner_changed`.
- BBX-7 If no offer is eligible, the page shows "Currently unavailable" and still lists other offers that can be bought (for example non-new conditions). In search results such a product shows the lowest-priced buyable offer with its condition label, or "Currently unavailable" when there is none (SRC-1).

### 2.5 Transparency

- Sellers see their Buy Box win rate per product and the main reason for losing (price gap, performance, delivery); weights and competitors' scores are not disclosed (P1 analytics page).
- The product page discloses that the default seller is selected automatically and shows the 1P badge where applicable.

## 3. Acceptance criteria

- Queries written with any alef, ya or ta-marbuta variant, with or without diacritics, and with Arabic-Indic or Western digits return the same results.
- A price or stock change is reflected in search within 60 seconds (measured in staging under load).
- Given fixed inputs, the Buy Box calculation is deterministic and matches a table of worked examples kept in the test suite.
- Two sellers alternately undercutting by one price step do not flip the Buy Box unless the score gap exceeds the hysteresis margin.
- Ad spend has no effect on organic ranking (test with identical products, one advertised).
