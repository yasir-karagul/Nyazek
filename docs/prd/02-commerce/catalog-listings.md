# Catalog & Listings

**Authoritative for:** categories and attributes, the shared catalogue model, listing types, offers, listing caps, content rules, prohibited and regulated products, media standards and pipeline.
**Related:** [search-buy-box](search-buy-box.md) · [pricing-promotions](pricing-promotions.md) · [inventory](inventory.md) · [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) · [seller-dashboard](../03-sellers/seller-dashboard.md)

---

## 1. Entities

| Entity | Description | Owner of content |
|---|---|---|
| Category | Tree of unlimited depth under 10 top-level categories | Catalog Manager |
| Attribute schema | Per category: attribute definitions, types, allowed values, mandatory flags, filterable flags | Catalog Manager |
| Brand | Name (Arabic, English), logo, gating flag, authorised sellers | Catalog Manager |
| Product | Canonical page: title, description, brand, category, attributes, images, video | Nyazek (canonical) or the seller (seller-owned) |
| Variant | A purchasable variation of a product (size, colour, storage), with its own identifiers (GTIN where it exists), images, package weight and dimensions | Same as product |
| Offer | One seller's price, stock, condition, handling time and shipping origin for one variant | Seller |

Localised fields (title, description, attribute labels and values) are stored in Arabic (required) and English (optional, falls back to Arabic). Flexible attributes are stored as `JSONB` validated against the category attribute schema.

**SKU** in this documentation means an active offer. The KPI "active listings" counts live, approved, in-stock offers ([overview-vision-kpis](../01-product/overview-vision-kpis.md)).

## 2. Categories

Launch top-level categories: Electronics & Mobile Phones · Fashion & Clothing · Home & Kitchen · Beauty & Personal Care · Groceries & Food · Baby & Kids · Sports & Outdoors · Books & Stationery · Automotive & Tools · Health & Pharmacy.

Each category node carries: attribute schema, commission rule link, return policy (window, change-of-mind flag, non-returnable flag), tax category, price-rule settings, compliance flags (`regulated`, `requires_expiry`, `requires_serial`, `hazardous`), and weight defaults. Category rules, compliance flags and the prohibited and restricted lists are held per market (MKT-6).

### 2.1 Category compliance rules

| Category | Mandatory listing data | Other rules |
|---|---|---|
| Health & Pharmacy | – | Non-prescription and wellness items only; seller licence required at KYC; opened or hygiene items non-returnable |
| Groceries & Food | Expiry date, storage condition | Minimum remaining shelf life at dispatch `cfg:catalog.min_shelf_life_days` (default 30, per category); perishables only in zones that support them; non-returnable except damaged, wrong or expired |
| Beauty & Personal Care; Baby & Kids | Ingredients or safety information; age grading | Hygiene items non-returnable once opened |
| Electronics & Mobile Phones | Warranty type and duration, condition | IMEI or serial captured at shipment for phones |
| Automotive & Tools | Vehicle compatibility fields | – |
| Fashion | Size chart, variant images | – |
| Any category, items flagged `hazardous` (lithium batteries shipped loose, aerosols, perfumes, flammable liquids) | Hazard type | Shipped only by couriers and to areas that accept them (SVC-5); never by air where the courier forbids it |

A listing cannot be published without its category's mandatory attributes. Categories flagged `regulated` require the matching licence on the seller account; lapse of the licence suspends the affected offers.

## 3. Shared catalogue model

- CAT-1 There is one canonical page per product. Canonical content is edited only by the Catalog Manager role. Sellers propose corrections through "Suggest an edit" (P1), which enters a review queue.
- CAT-2 Each seller attaches offers to the canonical variant with their own price, stock, condition, handling time and origin.
- CAT-3 The default offer on the page is chosen by the Buy Box ([search-buy-box](search-buy-box.md) §2). All other offers are listed under "Other sellers".
- CAT-4 Sellers cannot set shipping fees; Nyazek standardises them ([logistics](logistics.md) §4).

## 4. Listing types

| Type | When | Flow | Review |
|---|---|---|---|
| A. Offer on an existing canonical product | Product already exists | Seller finds it by barcode, brand + model or title and creates an offer | None; price rules still apply |
| B. New canonical product request | No match exists and the product is a standard, branded or barcoded item | Seller submits full content (title, brand, category, mandatory attributes, at least 3 images, package weight and dimensions) | Automated checks, then Catalog queue |
| C. Seller-owned listing | Item cannot be shared: handmade, private label, bundles, many fashion items, fresh groceries | Same submission as B; content stays owned by the seller | Automated checks, then Catalog queue; excluded from Buy Box competition |

Automated checks before the queue: duplicate detection (exact GTIN, then fuzzy brand/model/title), image standards, prohibited-keyword screening, mandatory-attribute completeness, category plausibility. Failures are returned to the seller with reasons and do not consume reviewer time.

- CAT-5 Catalog review SLA: `cfg:catalog.review_sla_hours` (default 24). Breach alerts the Catalog Manager.
- CAT-6 On approval of a Type B request the page becomes canonical and the submitting seller's offer goes live.
- CAT-7 Bulk import matches rows to canonical variants by GTIN so most rows become Type A offers; only unmatched rows become requests.
- CAT-8 Brand distributors with a verified badge can be placed on auto-approval for their own brand.
- CAT-9 Brand gating: a gated brand accepts offers only from sellers authorised for it.
- CAT-10 Duplicate canonical pages found later are merged by the Catalog Manager (P1 tooling); offers, reviews and URLs redirect to the surviving page.
- CAT-11 A GTIN identifies one variant. A request or import row whose GTIN is already attached to a different product is never merged automatically: it is held for the Catalog queue, which decides whether the barcode, the existing page or the request is wrong.
- CAT-12 Products and variants are archived, never deleted, once any offer, order, review or favourite references them. Archiving a variant ends its offers (`ARCHIVED`), removes it from search and shows it as unavailable in carts and favourites; its URL keeps resolving.
- CAT-13 Moving a product to another category revalidates it against the new attribute schema and compliance flags (missing mandatory attributes return the offers to `PAUSED` until completed). Orders already placed keep their frozen commission rate (COM-5) and return terms (RET-6).

### 4.1 Offer and request states

Offer:

| State | Entered when | Next |
|---|---|---|
| `DRAFT` | Seller saves an incomplete offer | `PENDING_REVIEW`, `ACTIVE`, `ARCHIVED` |
| `PENDING_REVIEW` | Submitted in a restricted category, or flagged by the content pre-screen (PRH-1) | `ACTIVE` (approved), `DRAFT` (changes needed, with reason) |
| `ACTIVE` | Published | `PAUSED`, `SUSPENDED`, `ARCHIVED` |
| `PAUSED` | Seller pauses, or vacation mode | `ACTIVE`, `ARCHIVED` |
| `SUSPENDED` | Admin action, violation, recall, licence lapse, or seller `SUSPENDED` (a `RESTRICTED` seller's existing offers stay `ACTIVE`) | `ACTIVE` (cause cleared; automatic for seller-state causes, by admin otherwise), `ARCHIVED` |
| `ARCHIVED` | Seller or admin archives | terminal (a new offer may be created) |

Out of stock never changes the state.

Product request: `DRAFT → SUBMITTED → AUTO_REJECTED | IN_REVIEW → APPROVED | REJECTED | NEEDS_CHANGES → SUBMITTED`; the seller may move `DRAFT`, `SUBMITTED` or `NEEDS_CHANGES` to `WITHDRAWN` (terminal).

### 4.2 Offer fields

Price (multiple of the price step), optional reference price (rules in [pricing-promotions](pricing-promotions.md) §1.5), condition (`NEW`, `OPEN_BOX`, `REFURBISHED`, `USED`; the conditions sellers may use are `cfg:catalog.allowed_conditions` (default NEW, OPEN_BOX, REFURBISHED), per category, and `USED` is not enabled at launch: D-44, decided), handling time in days, shipping origin (one of the seller's pickup addresses), seller SKU code, stock (owned by Inventory), warranty details where the category requires them.

## 5. Listing caps (D-04)

| Seller type | Cap |
|---|---|
| Individual Entrepreneur | `cfg:catalog.cap_individual` (default 50) active offers during the first 3 months after approval, then unlimited |
| Business, Brand Distributor | `cfg:catalog.cap_business` (default 5,000) at approval, raised by the Seller Manager on request |

v5 and parts of v6 applied the 50-listing cap to every new seller, which contradicted bulk import and the active-listings KPI.

## 6. Product content rules

- Titles follow a per-category template (brand + model + key attributes); promotional words, contact details and links are rejected.
- Seller-authored rich text (descriptions, store "About") is sanitised server-side with an allow-list and rendered in a restricted component ([security](../05-trust/security.md) §4).
- Package weight and dimensions are mandatory for every variant because shipping fees, surcharges and courier limits depend on them.

## 7. Prohibited and restricted products

Strictly prohibited: weapons and ammunition · alcohol and tobacco · counterfeit or replica goods · adult content and products · prescription medicines · political or religious material · live animals.

- PRH-1 Enforcement: keyword and image screening at submission; "Report listing" on every product page; takedown within `cfg:catalog.takedown_hours` (default 24), immediately for safety-critical reports.
- PRH-2 Intellectual-property notice-and-takedown: a public form, a review queue, counter-notice handling.
- PRH-3 Repeat offenders escalate through performance Levels 3–4; counterfeit findings trigger the authenticity override ([seller-performance](../03-sellers/seller-performance.md) §3).
- PRH-4 The restricted list (items allowed only for licensed sellers) is maintained by Compliance and published on the Prohibited & Restricted Items Policy page.
- PRH-5 Safety recall: when a product or batch is recalled or found unsafe, the Catalog Manager suspends the affected offers at once, and customers who received the affected product or batch are notified with instructions (a transactional message). Returns for a recall are fault-based and never count against the customer or, unless the seller caused the defect, the seller.
- PRH-6 Digital goods, services, vouchers and gift cards cannot be listed in v1.0: every listing is a physical item with package weight and dimensions.

## 8. Media

### 8.1 Standards

- At least 3 images per listing; main image on a white or neutral background; minimum 800 × 800 pixels.
- No seller logos, watermarks or promotional text on images.
- Video is allowed alongside images: maximum `cfg:media.max_video_seconds` (default 60) and `cfg:media.max_video_mb` (default 50).
- Limits: `cfg:media.max_images_per_listing` (default 10), `cfg:media.max_image_mb` (default 8).

### 8.2 Pipeline

1. Client requests a pre-signed upload URL and uploads directly to a private quarantine bucket.
2. Worker validates MIME type and file signature, scans for malware, strips EXIF metadata, re-encodes, and generates named variants (`thumb`, `card`, `detail`, `zoom`) in WebP and AVIF.
3. Processed files move to the public media bucket under random keys and are served through the CDN with long cache lifetimes.
4. Rejected files are deleted and the uploader is told why.

Bulk import by image URL fetches through an egress proxy that blocks private and link-local addresses and enforces size and type limits ([security](../05-trust/security.md) §5).

## 9. Bulk import and export

- CSV and Excel templates per category with field mapping and a dry-run mode.
- Imports run as background jobs with a row-level result report (created, updated, matched to canonical, sent to review, rejected with reason).
- Price rules, caps and attribute validation apply to every row exactly as in the single-listing flow.
- Exports neutralise spreadsheet formula injection (cells beginning with `=`, `+`, `-`, `@`).

## 10. Acceptance criteria

- A listing missing a mandatory category attribute cannot be published through any path (form, bulk import).
- Importing a file where 90% of rows carry known GTINs creates offers for those rows without reviewer involvement.
- A seller without the required licence cannot activate an offer in a regulated category.
- Uploaded files that fail signature or malware checks never reach the public bucket.
