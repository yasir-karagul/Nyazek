# Sponsored Advertising

**Priority:** P1.
**Authoritative for:** ad products, auction and pricing, budgets and billing, click validity, placements, policy.
**Related:** [search-buy-box](search-buy-box.md) · [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) · [data-analytics](../06-platform/data-analytics.md)

---

## 1. Ad products

| Product | Description | Pricing |
|---|---|---|
| Sponsored products | A seller promotes its own active offers; ads appear in labelled slots | Cost per click, auction |
| Home-page banners | Managed by the Content and Marketing teams as CMS placements | Fixed price by booking; not auctioned at launch |

## 2. Campaign model

- A campaign belongs to one seller and contains: products (offers), targeting (keywords and/or categories), maximum CPC bid, daily budget, optional total budget, start and end dates, status.
- States: `DRAFT → ACTIVE ⇄ PAUSED`, `→ ENDED`. System pauses: daily budget exhausted, insufficient Available balance, offer out of stock or ineligible, seller restricted.
- Minimum bid `cfg:ads.min_cpc` (default 250) and minimum daily budget `cfg:ads.min_daily_budget` (default 5,000), configurable per placement.

## 3. Auction

- AD-1 For each slot, eligible ads are ranked by `adRank = maxCpc × qualityScore`.
- AD-2 Quality score (1–10) combines predicted click-through rate for the query or category and the relevance of the product to it. New ads start at a neutral 5.
- AD-3 An ad below a minimum relevance threshold is not eligible, whatever its bid: sponsored slots never show irrelevant products.
- AD-4 Price per click (generalised second price): `price = ceil(nextAdRank ÷ ownQualityScore) + 1` (one minor unit of the market currency; 1 IQD in Iraq), never more than the advertiser's maximum CPC and never less than the minimum bid. When there is no competitor, the price is the minimum bid.
- AD-5 Ads are not served for offers that are out of stock, ineligible, or from sellers who are restricted or in wallet deficit.

## 4. Placements

| Placement | Rule |
|---|---|
| Search results | Up to `cfg:ads.search_slots` (default 2) sponsored products at the top and one every 10 organic results |
| Category pages | Same slot pattern as search |
| Home page | One "Sponsored" product row |
| Product page | "Sponsored alternatives" carousel below the fold; never inside the "Other sellers" list |

- AD-6 Every sponsored item carries a visible "Sponsored" label (Arabic: "إعلان مموّل").
- AD-7 Organic ranking and the Buy Box are never influenced by ad spend.

## 5. Click validity and billing

- AD-8 A click is billable only after validation. Signals: duplicate clicks from the same device or IP within a window, bot signatures, the seller's own accounts and devices, abnormal click-through without engagement.
- AD-9 Clicks are validated in a batch that closes each day; validated clicks are billed daily to the seller's Available balance (posting JE-25) and reported as `ad.spend_billed`.
- AD-10 Ad spend is debited only from Available, never from Pending. If Available cannot cover the day's spend the campaign pauses and the shortfall is collected from the next release.
- AD-11 Clicks later found invalid are credited back (JE-26).
- AD-12 A daily budget may be exceeded by at most one click's price because of concurrency; any excess beyond that is not billed.
- AD-13 Advertising is available only to sellers with a positive Available balance. Prepaid ad credit top-ups are P2.

## 6. Reporting

Per campaign and product: impressions, clicks, click-through rate, average CPC, spend, attributed orders and sales (an order is attributed to the last ad click by the same customer on the same product within 7 days). Impression and click events use the clickstream path, not the domain event bus ([data-analytics](../06-platform/data-analytics.md) §3).

## 7. Policy

- Sellers may bid on competitor brand keywords.
- Sellers may not use brand names or trademarks they are not authorised for in ad text or banner creative.
- Banner creative is moderated by the Marketing Manager before going live.
- No ads for regulated categories without the corresponding licence.
- Counsel confirms advertising-disclosure requirements ([compliance-legal](../05-trust/compliance-legal.md)).

## 8. Acceptance criteria

- With two advertisers of different quality scores, the price charged matches AD-4 worked examples in the test suite.
- A seller clicking their own ads from a linked device is not billed.
- A campaign stops serving within one minute of its daily budget being exhausted.
