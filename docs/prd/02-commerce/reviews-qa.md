# Reviews, Ratings & Q&A

**Authoritative for:** product reviews, seller ratings, customer ratings by sellers, moderation, product Q&A.
**Related:** [seller-performance](../03-sellers/seller-performance.md) · [search-buy-box](search-buy-box.md) · [fraud-risk](../05-trust/fraud-risk.md)

---

## 1. Rating objects

| Object | Attached to | Shown on | Feeds |
|---|---|---|---|
| Product review (1–5 stars, optional text and photos) | The product, shared by all sellers of a canonical product | Product page | Search rating signal |
| Seller rating (1–5 stars, optional text) | A delivered sub-order | Seller storefront | Seller performance score (25%) |
| Customer rating by seller (1–5 stars, reason code), P1 | A completed or returned sub-order | Nyazek admins only | Weak signal for Risk |

v6 described a "two-way rating" at launch. Sellers never meet customers (couriers do), so a seller's rating of a customer is a weak, retaliation-prone signal; it is kept as P1 and may only inform manual risk review, never automatic restrictions (ratification under D-33).

## 2. Rules

- REV-1 Only customers with a delivered sub-order containing the product may review it, once per product per order, within `cfg:reviews.window_days` (default 30) of delivery.
- REV-2 A customer may edit a review once within 7 days; edits are re-screened.
- REV-3 Reviewer identity is partially anonymised (first name and initial, or "Verified customer").
- REV-4 A seller's aggregate rating is displayed publicly only after `cfg:reviews.min_ratings_for_display` (default 5) ratings.
- REV-5 Sellers cannot reply publicly at launch; they can flag a review for moderation with a reason.
- REV-6 Reviews and Q&A from accounts linked to the seller (shared device, phone, payout account, address or identity-document signals) are blocked ([fraud-risk](../05-trust/fraud-risk.md) §5).
- REV-7 A review reminder is sent once, a few days after delivery, subject to notification preferences.
- REV-8 If the order is later fully refunded for non-delivery, the product review is removed; reviews on returned items remain (they are legitimate experience) but are marked.

## 3. Moderation

v6 said in one place that every review needs admin approval and in another that an automated pre-screen approves low-risk reviews. The pre-screen is the rule; manual approval of every review does not scale.

| Step | Behaviour |
|---|---|
| Automated pre-screen | Profanity and abuse lists (Arabic and English), links, phone numbers and contact details, duplicate or templated text, rating-manipulation patterns, linked-account detection, image checks |
| Low risk | Published immediately |
| Flagged | Queue for a Support Agent; decision within `cfg:reviews.moderation_sla_hours` (default 48) |
| Reported by seller or user | Re-queued with the report reason |

- Moderators may approve or remove; they do not edit review text.
- Removed ratings are excluded from the seller performance score and from product aggregates.
- Removal reasons are recorded and shown to the author.

## 4. Product Q&A (P1)

- Any signed-in customer may ask a question on a product page; the same pre-screen applies.
- Sellers with an active offer on the product, and the Catalog team, may answer; answers show the answering seller's name.
- Questions and answers are shared across all sellers of a canonical product.
- Sellers are notified of new questions; response time on Q&A is not part of the performance score.

## 5. Acceptance criteria

- A customer without a delivered order for the product cannot submit a review through any client.
- A review containing a phone number or link is never published without moderation.
- Removing a rating updates the seller's displayed aggregate and performance input within one recompute cycle.
