# Taxonomy & Labels

**Authoritative for:** the category tree, the labels shown for order, return, dispute and other statuses, the mapping of list tabs to states, and navigation labels in Arabic and English.
**Related:** [catalog-listings](../02-commerce/catalog-listings.md) §2 · [checkout-orders](../02-commerce/checkout-orders.md) §6 · [returns-disputes](../02-commerce/returns-disputes.md) · [navigation](navigation.md)

State machines are defined in the domain documents. This document only says how each state is **named and grouped** for people. All Arabic wording here is *proposed* and is confirmed in copy review (UI-4, D-46); the strings live in the message catalogues, never in components.

---

## 1. Terminology

| English | Arabic (proposed) | Notes |
|---|---|---|
| Customer | العميل | Official term; "buyer" is not used |
| Seller | البائع | |
| Store | المتجر | A seller's storefront |
| Nyazek Official Store | متجر نيازك الرسمي | 1P badge text |
| Order | الطلب | The whole purchase |
| Shipment (customer-facing name of a sub-order) | الشحنة | Customers see "Shipment 1 of 2 from <seller>"; "sub-order" is internal |
| Favourites | المفضلة | "Wishlist" is not used |
| Cart | السلة | |
| Cash on delivery | الدفع عند الاستلام | |
| Return | الإرجاع | |
| Refund | استرداد المبلغ | |
| Dispute | النزاع | |
| Offer (seller-facing) | العرض | Customers never see the word; they see sellers and prices |
| Wallet (seller) | المحفظة | |
| Payout | التحويل | |
| Sponsored | إعلان مموّل | AD-6 |

## 2. Category tree

The ten top-level categories are fixed by [catalog-listings](../02-commerce/catalog-listings.md) §2. The second level below was ratified by the owner (D-46) so navigation, filters and seed data can be built; the Catalog Manager owns the tree and extends it (third level and deeper) in the Admin Panel. Each node needs an Arabic and an English name, a slug, an attribute schema and its compliance flags before it goes live.

| Top level | Second level |
|---|---|
| Electronics & Mobile Phones | Mobile phones · Tablets · Laptops and computers · Computer accessories · TVs and home audio · Headphones and speakers · Cameras · Gaming · Wearables · Phone accessories · Chargers and power banks |
| Fashion & Clothing | Men's clothing · Women's clothing · Modest and traditional wear · Shoes · Bags and luggage · Watches · Jewellery and accessories |
| Home & Kitchen | Furniture · Kitchen and dining · Large appliances · Small appliances · Bedding and bath · Home décor · Lighting · Storage and cleaning · Garden and outdoor |
| Beauty & Personal Care | Fragrances · Make-up · Skin care · Hair care · Men's grooming · Bath and body · Personal-care appliances |
| Groceries & Food | Pantry staples · Beverages · Tea and coffee · Snacks and sweets · Dates and nuts · Canned and packaged food · Household supplies · Fresh food (only where the zone supports perishables) |
| Baby & Kids | Diapers and wipes · Feeding · Baby care · Strollers and car seats · Toys and games · Kids' clothing and shoes |
| Sports & Outdoors | Sportswear · Fitness equipment · Team sports · Cycling · Camping and outdoor |
| Books & Stationery | Arabic books · English books · Children's books · School supplies · Office supplies · Art supplies |
| Automotive & Tools | Car accessories · Car care · Car electronics · Oils and fluids (hazardous flag) · Hand tools · Power tools · Hardware and electrical |
| Health & Pharmacy | Vitamins and supplements · Home medical devices · First aid · Personal health care · Mobility aids (non-prescription items only; seller licence required) |

## 3. Order status

### 3.1 Sub-order state → what each audience sees

| State | Customer label | Arabic (proposed) | Customer tab | Seller tab | Admin tab |
|---|---|---|---|---|---|
| `AWAITING_PAYMENT` | Awaiting payment | بانتظار الدفع | Pending | not visible | Pending |
| `ON_HOLD` (COD confirmation) | Confirm your order | يرجى تأكيد طلبك | Pending | not visible | Pending |
| `ON_HOLD` (risk review) | Being verified | قيد التحقق | Pending | not visible | Pending |
| `PENDING_SELLER_CONFIRMATION` | Order received | تم استلام الطلب | Pending | Awaiting confirmation | Pending |
| `CONFIRMED` | Being prepared | قيد التجهيز | Processing | Processing | Processing |
| `READY_TO_SHIP` | Being prepared | قيد التجهيز | Processing | Ready to ship | Processing |
| `SHIPPED` | Shipped | تم الشحن | Shipped | Shipped | Shipped |
| `OUT_FOR_DELIVERY` | Out for delivery | خرج للتوصيل | Shipped | Shipped | Shipped |
| `DELIVERED` | Delivered | تم التوصيل | Delivered | Delivered | Delivered |
| `COMPLETED` | Delivered | تم التوصيل | Delivered | Delivered (marked "Released") | Delivered |
| `DELIVERY_FAILED` | Not delivered | لم يتم التوصيل | Cancelled | Returned | Cancelled |
| `RTO_IN_TRANSIT` | Not delivered | لم يتم التوصيل | Cancelled | Returned ("Coming back") | Cancelled |
| `RTO_RECEIVED` | Not delivered | لم يتم التوصيل | Cancelled | Returned ("Received back") | Cancelled |
| `LOST` | Lost in transit | فُقدت أثناء الشحن | Cancelled | Cancelled ("Lost") | Cancelled |
| `CANCELLED` | Cancelled | ملغي | Cancelled | Cancelled | Cancelled |

- The **Returned** tab (all audiences) also lists sub-orders that have at least one return that is not rejected, expired or cancelled; such a sub-order keeps its delivery tab as well.
- Customers and sellers see the label; staff always see the exact state name next to it, and the cancel reason where there is one.
- A cancelled sub-order shows the reason in words suited to the audience: the customer sees "Cancelled by you", "Cancelled by the seller", "Not confirmed in time", "Payment not completed" (`PAYMENT_EXPIRED`), "Seller unavailable" (`SELLER_SUSPENDED`) or "Cancelled by Nyazek"; the seller sees the exact reason including whether it counts toward their metrics.
- The label for `ON_HOLD` under risk review never mentions risk or fraud.

### 3.2 Order (parent) label for the customer

| Derived status | Label | Arabic (proposed) |
|---|---|---|
| `AWAITING_PAYMENT` | Awaiting payment | بانتظار الدفع |
| `IN_PROGRESS` | In progress, with "N of M shipments delivered" when M > 1 | قيد التنفيذ |
| `COMPLETED` | Completed | مكتمل |
| `CANCELLED` | Cancelled | ملغي |
| `EXPIRED` | Payment not completed | لم يكتمل الدفع |
| `CLOSED` | Closed (no shipment was completed: "Not delivered" or "Lost" shown per shipment) | مغلق |

### 3.3 Customer tracking timeline

The tracking page shows these milestones in order, each with its time once reached: Order placed → Confirmed by seller → Ready for the courier → Shipped → Out for delivery (if reported) → Delivered. Failed attempts, rescheduling and return-to-sender appear as dated entries between milestones. Raw courier events are shown under "Courier details" with the courier's tracking number and link (SHP-1).

## 4. Return, dispute, refund, payment and other labels

| Object | State → label (customer) | Seller sees |
|---|---|---|
| Return | `REQUESTED` Requested · `APPROVED` Approved, hand over by <date> · `REJECTED` Rejected by seller (with the option to dispute) · `IN_TRANSIT` On its way back · `RECEIVED` Received, being inspected · `CONTESTED` Seller raised an issue, your answer needed · `ACCEPTED` Accepted, refund in progress · `REFUNDED` Refunded · `EXPIRED` Expired (not handed over) · `LOST` Lost in transit, refunded · `CANCELLED` Withdrawn · `IN_DISPUTE` In dispute · `CLOSED` Closed (shown with the outcome: refunded, rejected, expired or withdrawn) | Same states with the seller's deadline on `REQUESTED` (respond) and `RECEIVED` (inspect) |
| Dispute | `OPENED` Opened · `SELLER_RESPONSE` Waiting for the seller · `UNDER_REVIEW` Under review by Nyazek · `RESOLVED_CUSTOMER` Resolved in your favour · `RESOLVED_SELLER` Resolved in the seller's favour · `RESOLVED_SPLIT` Partly refunded · `REVIEW_REQUESTED` Review requested · `WITHDRAWN` Withdrawn · `CLOSED` Closed (with the final outcome) | Mirror wording ("your response needed", "resolved in your favour") |
| Refund | `REQUESTED`, `PROCESSING` In progress, expected by <date> · `AWAITING_DESTINATION` Add a refund account to receive your money · `SUCCEEDED` Refunded to <destination> · `FAILED`, `MANUAL_REVIEW`, `RETURNED` Being handled by our team · `CANCELLED` Cancelled | Wallet movement type "refund" |
| Payment | `CREATED`, `PENDING` Waiting for confirmation · `SUCCEEDED` Paid · `FAILED` Not completed · `EXPIRED` Timed out · `CANCELLED` Not started | – |
| COD collection | Customer sees "Pay <amount> on delivery" until delivered, then "Paid in cash" | Wallet: "Awaiting courier remittance" until reconciled |
| Offer (seller) | – | `DRAFT` Draft · `PENDING_REVIEW` In review · `ACTIVE` with no stock: Out of stock · `PAUSED` Paused · `SUSPENDED` Suspended (with reason) · `ARCHIVED` Archived |
| Product request (seller) | – | `DRAFT` Draft · `WITHDRAWN` Withdrawn · `SUBMITTED`, `IN_REVIEW` In review · `AUTO_REJECTED`, `REJECTED` Rejected (with reasons) · `NEEDS_CHANGES` Changes needed · `APPROVED` Approved |
| Payout (seller) | – | `CREATED`, `APPROVED` Scheduled · `INSTRUCTED` Sent to bank · `EXECUTED` Paid · `REJECTED` Not included in this run (with reason) · `FAILED`, `RETRY_SCHEDULED`, `RETURNED` Failed, action needed |
| Seller account (seller) | – | `REGISTERED` Getting started · `KYC_SUBMITTED`, `KYC_IN_REVIEW` Application in review · `NEEDS_INFO` Information needed · `REJECTED` Application not approved · `ACTIVE` Active · `RESTRICTED` Restricted (with reasons) · `SUSPENDED` Suspended · `CLOSING` Closing · `CLOSED` Closed |
| Wallet hold (seller) | – | Chargeback · Return after release · Dispute after release · Risk review · New payout destination · Account suspended · Reconciliation check (one label per hold reason in commission-wallet-payouts §4) |
| Ticket | `OPEN` Open · `IN_PROGRESS` In progress · `WAITING_ON_REQUESTER` Waiting for your reply · `RESOLVED` Resolved · `CLOSED` Closed | Same |

Status chips use a fixed colour role per meaning (neutral: waiting; informative: in progress; positive: done; warning: action needed; negative: failed or cancelled) and always carry text or an icon as well (design system §3).

## 5. Navigation labels

| Location | English | Arabic (proposed) |
|---|---|---|
| Storefront header | Categories · Deliver to · Favourites · Cart · Sign in · Create account · My account · Track an order · Sell on Nyazek | الفئات · التوصيل إلى · المفضلة · السلة · تسجيل الدخول · إنشاء حساب · حسابي · تتبّع طلب · بِع على نيازك |
| Storefront bottom bar | Home · Categories · Favourites · Cart · Account | الرئيسية · الفئات · المفضلة · السلة · حسابي |
| Account menu | My orders · Returns · Disputes · Reviews · Addresses · Refund accounts · Notifications · Personal information · Security · Privacy · Sign out | طلباتي · المرتجعات · النزاعات · التقييمات · العناوين · حسابات الاسترداد · الإشعارات · المعلومات الشخصية · الأمان · الخصوصية · تسجيل الخروج |
| Checkout steps | Cart · Address · Shipping · Payment · Confirmation | السلة · العنوان · الشحن · الدفع · التأكيد |
| Product page | Add to cart · Buy now · Other sellers · Description · Specifications · Reviews · Shipping and returns · Report this listing | أضف إلى السلة · اشترِ الآن · بائعون آخرون · الوصف · المواصفات · التقييمات · الشحن والإرجاع · الإبلاغ عن هذا المنتج |
| Seller sidebar | Home · Orders · Catalog · Returns and disputes · Wallet · Customers · Performance · Analytics · Settings | الرئيسية · الطلبات · المنتجات · المرتجعات والنزاعات · المحفظة · العملاء · الأداء · التحليلات · الإعدادات |
| Admin sidebar | Dashboard · Users · Catalogue · 1P store · Orders · Logistics · Returns and disputes · Finance · Risk · Marketing · Moderation and support · Content · Analytics · Compliance · Settings | لوحة التحكم · المستخدمون · الكتالوج · متجر نيازك · الطلبات · الشحن · المرتجعات والنزاعات · المالية · المخاطر · التسويق · الإشراف والدعم · المحتوى · التحليلات · الامتثال · الإعدادات |

## 6. Acceptance criteria

- Every state of every machine listed above has a label in both languages in the message catalogues; a test fails when a state has none.
- For every sub-order state, the customer, seller and admin lists place it in the tab given in §3.1.
- No customer-facing text contains an internal state name, "sub-order", "offer", "escrow" before counsel approves that wording (PAY-3), or the word "risk".
