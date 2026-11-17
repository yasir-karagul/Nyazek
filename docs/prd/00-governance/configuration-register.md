# Configuration Register

**Authoritative for:** the list of platform configuration values (`cfg:` keys), their proposed defaults and owners. The behaviour each value controls is defined in the linked document, which is authoritative for its meaning.

- Values are stored in the `backoffice` configuration store: typed, validated, audited, with an effective-from time ([admin-governance](../05-trust/admin-governance.md) §5).
- Every default below is a **proposal**. The owner ratifies the set once (D-36 in [open-decisions](open-decisions.md)); values marked "closed beta" are tuned with real data before public launch.
- Many values can be overridden per category, courier, governorate or seller where the linked document says so. Every value can also be overridden per market ([market-expansion](../01-product/market-expansion.md) §3); the defaults below are the Iraq values.
- This file is generated from the `cfg:` markers in the documents and checked in CI: a key used in a document but missing here, or listed here but unused, fails the documentation check.

## `money`

Owner: Finance Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `money.price_step` | 250 IQD | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) |

## `events`

Owner: Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `events.max_attempts` | 10 | [architecture](../06-platform/architecture.md) |
| `events.retention_months` | 25 | [architecture](../06-platform/architecture.md) |

## `buybox`

Owner: Catalog Manager + Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `buybox.min_performance` | 40 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.w_price` | 40 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.w_performance` | 35 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.w_delivery` | 20 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.w_1p` | 5 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.level2_factor` | 0.85 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.hysteresis_points` | 3 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `buybox.max_interval_minutes` | 15 | [search-buy-box](../02-commerce/search-buy-box.md) |

## `search`

Owner: Catalog Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `search.w_performance` | 0.30 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `search.w_popularity` | 0.30 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `search.w_price` | 0.20 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `search.w_rating` | 0.20 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `search.w_recency` | 0.10 | [search-buy-box](../02-commerce/search-buy-box.md) |
| `search.max_page_depth` | 50 pages | [search-buy-box](../02-commerce/search-buy-box.md) |

## `catalog`

Owner: Catalog Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `catalog.min_shelf_life_days` | 30, per category | [catalog-listings](../02-commerce/catalog-listings.md) |
| `catalog.review_sla_hours` | 24 | [catalog-listings](../02-commerce/catalog-listings.md) |
| `catalog.allowed_conditions` | NEW, OPEN_BOX, REFURBISHED | [catalog-listings](../02-commerce/catalog-listings.md) |
| `catalog.cap_individual` | 50 | [catalog-listings](../02-commerce/catalog-listings.md) |
| `catalog.cap_business` | 5,000 | [catalog-listings](../02-commerce/catalog-listings.md) |
| `catalog.takedown_hours` | 24 | [catalog-listings](../02-commerce/catalog-listings.md) |

## `media`

Owner: Catalog Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `media.max_video_seconds` | 60 | [catalog-listings](../02-commerce/catalog-listings.md) |
| `media.max_video_mb` | 50 | [catalog-listings](../02-commerce/catalog-listings.md) |
| `media.max_images_per_listing` | 10 | [catalog-listings](../02-commerce/catalog-listings.md) |
| `media.max_image_mb` | 8 | [catalog-listings](../02-commerce/catalog-listings.md) |

## `pricing`

Owner: Catalog Manager / Finance Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `pricing.dumping_percent` | 50% | [pricing-promotions](../02-commerce/pricing-promotions.md) |
| `pricing.1p_margin_floor_percent` | 10% | [pricing-promotions](../02-commerce/pricing-promotions.md) |
| `pricing.reference_min_days` | 7 | [pricing-promotions](../02-commerce/pricing-promotions.md) |
| `pricing.reference_lookback_days` | 30 | [pricing-promotions](../02-commerce/pricing-promotions.md) |

## `promo`

Owner: Marketing Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `promo.seller_coupon_min_percent` | 5 | [pricing-promotions](../02-commerce/pricing-promotions.md) |
| `promo.seller_coupon_max_percent` | 70 | [pricing-promotions](../02-commerce/pricing-promotions.md) |

## `cart`

Owner: Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `cart.max_qty_per_line` | 10 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `cart.max_lines` | 50 | [checkout-orders](../02-commerce/checkout-orders.md) |

## `checkout`

Owner: Fraud/Risk Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `checkout.max_sessions_per_hour` | 10 | [checkout-orders](../02-commerce/checkout-orders.md) |

## `customers`

Owner: Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `customers.max_saved_addresses` | 3 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `customers.max_favourites` | 500 | [customer-account](../02-commerce/customer-account.md) |
| `customers.back_in_stock_alerts_max` | 50 | [customer-account](../02-commerce/customer-account.md) |

## `orders`

Owner: Super Admin (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `orders.payment_window_minutes` | 30 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `orders.confirm_sla_hours` | 24 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `orders.handover_grace_hours` | 48 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `orders.max_handling_days` | 3 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `orders.default_handling_days` | 2 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `orders.stuck_alert_hours` | 12 | [checkout-orders](../02-commerce/checkout-orders.md) |

## `inventory`

Owner: Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `inventory.reservation_ttl_minutes` | 15 | [inventory](../02-commerce/inventory.md) |
| `inventory.low_stock_default` | 3 | [inventory](../02-commerce/inventory.md) |
| `inventory.low_stock_badge_threshold` | 5 | [inventory](../02-commerce/inventory.md) |

## `shipping`

Owner: Finance Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `shipping.free_threshold` | set under D-21 | [checkout-orders](../02-commerce/checkout-orders.md) |

## `logistics`

Owner: Logistics Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `logistics.max_attempts` | 3 | [logistics](../02-commerce/logistics.md) |
| `logistics.lost_after_days` | 14 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `logistics.webhook_silence_minutes` | 60 | [logistics](../02-commerce/logistics.md) |
| `logistics.rto_confirm_hours` | 48 | [logistics](../02-commerce/logistics.md) |

## `cod`

Owner: Fraud/Risk Manager; fees and remittance with Finance

| Key | Proposed default | Defined in |
|---|---|---|
| `cod.fee` | 0 IQD | [payments](../04-finance/payments.md) |
| `cod.confirmation_window_hours` | 24 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `cod.remittance_sla_days` | 3 | [logistics](../02-commerce/logistics.md) |
| `cod.new_account_daily_orders` | 2 | [fraud-risk](../05-trust/fraud-risk.md) |
| `cod.new_account_max_value` | 250,000 | [fraud-risk](../05-trust/fraud-risk.md) |
| `cod.max_open_value` | 500,000 | [fraud-risk](../05-trust/fraud-risk.md) |
| `cod.suspend_after_failed` | 2 in the last 5 COD orders | [fraud-risk](../05-trust/fraud-risk.md) |
| `cod.new_account_delivered_orders` | 2 | [fraud-risk](../05-trust/fraud-risk.md) |
| `cod.confirm_first_order` | true | [fraud-risk](../05-trust/fraud-risk.md) |

## `returns`

Owner: Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `returns.default_window_days` | 7 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.proof_value_threshold` | 100,000 IQD | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.max_seller_window_days` | 30 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.seller_response_hours` | 48 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.handover_days` | 7 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.inspection_hours` | 48 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.contest_response_hours` | 72 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.returnless_threshold` | 0, disabled | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.abuse_proof_threshold` | set in closed beta | [returns-disputes](../02-commerce/returns-disputes.md) |
| `returns.abuse_restrict_threshold` | set in closed beta | [returns-disputes](../02-commerce/returns-disputes.md) |

## `disputes`

Owner: Super Admin (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `disputes.open_after_decision_days` | 7 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `disputes.non_delivery_days` | 7 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `disputes.not_arrived_grace_days` | 3 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `disputes.mediation_hours` | 48 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `disputes.decision_hours` | 72 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `disputes.review_request_hours` | 48 | [returns-disputes](../02-commerce/returns-disputes.md) |
| `disputes.agent_limit` | 250,000 IQD | [returns-disputes](../02-commerce/returns-disputes.md) |

## `reviews`

Owner: Support lead

| Key | Proposed default | Defined in |
|---|---|---|
| `reviews.window_days` | 30 | [reviews-qa](../02-commerce/reviews-qa.md) |
| `reviews.min_ratings_for_display` | 5 | [reviews-qa](../02-commerce/reviews-qa.md) |
| `reviews.moderation_sla_hours` | 48 | [reviews-qa](../02-commerce/reviews-qa.md) |

## `loyalty`

Owner: Marketing Manager (dual control for rates)

| Key | Proposed default | Defined in |
|---|---|---|
| `loyalty.adjust_dual_control_points` | 50,000 | [loyalty](../02-commerce/loyalty.md) |
| `loyalty.base_points_per_1000_units` | 10, points per 1,000 units of the market currency | [loyalty](../02-commerce/loyalty.md) |
| `loyalty.value_per_point` | 1, in the market currency's minor unit | [loyalty](../02-commerce/loyalty.md) |
| `loyalty.max_redeem_percent` | 20% | [loyalty](../02-commerce/loyalty.md) |
| `loyalty.referral_points` | 0, set under D-34 | [loyalty](../02-commerce/loyalty.md) |
| `loyalty.referral_monthly_cap` | 20 | [loyalty](../02-commerce/loyalty.md) |

## `ads`

Owner: Marketing Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `ads.min_cpc` | 250 | [advertising](../02-commerce/advertising.md) |
| `ads.min_daily_budget` | 5,000 | [advertising](../02-commerce/advertising.md) |
| `ads.search_slots` | 2 | [advertising](../02-commerce/advertising.md) |

## `notifications`

Owner: Marketing Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `notifications.quiet_start` | 22:00 | [notifications-messaging](../02-commerce/notifications-messaging.md) |
| `notifications.quiet_end` | 08:00 | [notifications-messaging](../02-commerce/notifications-messaging.md) |
| `notifications.promo_max_per_day` | 2 | [notifications-messaging](../02-commerce/notifications-messaging.md) |

## `support`

Owner: Support lead

| Key | Proposed default | Defined in |
|---|---|---|
| `support.auto_close_days` | 7 | [support-cms](../02-commerce/support-cms.md) |
| `support.customer_first_response_hours` | 24 | [support-cms](../02-commerce/support-cms.md) |
| `support.seller_first_response_hours` | 12 | [support-cms](../02-commerce/support-cms.md) |

## `kyc`

Owner: Seller Manager / Compliance

| Key | Proposed default | Defined in |
|---|---|---|
| `kyc.review_sla_hours` | 24 | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) |
| `kyc.max_attempts_per_30_days` | 3 | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) |
| `kyc.reverify_payout_threshold` | set by Compliance | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) |

## `sellers`

Owner: Seller Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `sellers.referral_bonus` | 0, set by the owner | [loyalty](../02-commerce/loyalty.md) |
| `sellers.vacation_max_days` | 30 | [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) |
| `sellers.bulk_price_change_confirm_percent` | 30% | [seller-dashboard](../03-sellers/seller-dashboard.md) |

## `performance`

Owner: Seller Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `performance.mapping` | as in the table below | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.min_orders` | 10 | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.level1_below` | 70 | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.level2_below` | 60 | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.level3_below` | 50 | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.level4_below` | 40 | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.recovery_days` | 14 | [seller-performance](../03-sellers/seller-performance.md) |
| `performance.appeal_sla_hours` | 48 | [seller-performance](../03-sellers/seller-performance.md) |

## `payments`

Owner: Finance Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `payments.intent_ttl_minutes` | 30 | [payments](../04-finance/payments.md) |
| `payments.circuit_error_rate` | 30% over 5 minutes | [payments](../04-finance/payments.md) |

## `refunds`

Owner: Finance Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `refunds.destination_wait_days` | 14 | [payments](../04-finance/payments.md) |
| `refunds.max_retries` | 3 | [payments](../04-finance/payments.md) |
| `refunds.dual_control_threshold` | 250,000 IQD | [payments](../04-finance/payments.md) |
| `refunds.execution_sla_days` | 3 business days | [payments](../04-finance/payments.md) |
| `refunds.max_refund_accounts` | 2 | [payments](../04-finance/payments.md) |

## `escrow`

Owner: Finance Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `escrow.hold_days` | 7 | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |
| `escrow.hold_follows_return_window` | true | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |

## `wallet`

Owner: Finance Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `wallet.deficit_grace_cycles` | 2 | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |

## `payout`

Owner: Finance Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `payout.default_cycle` | MONTHLY | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |
| `payout.min_amount` | 25,000 IQD | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |
| `payout.transfer_fee_bearer` | NYAZEK | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |

## `commission`

Owner: Finance Manager (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `commission.notice_days` | 30 | [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) |

## `content`

Owner: Content Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `content.new_arrivals_days` | 30 | [support-cms](../02-commerce/support-cms.md) |
| `content.top_rated_min_ratings` | 5 | [support-cms](../02-commerce/support-cms.md) |
| `content.home_banners_max` | 6 | [support-cms](../02-commerce/support-cms.md) |
| `content.home_row_cards` | 20 | [support-cms](../02-commerce/support-cms.md) |

## `identity`

Owner: Super Admin

| Key | Proposed default | Defined in |
|---|---|---|
| `identity.order_lookup_session_minutes` | 30 | [checkout-orders](../02-commerce/checkout-orders.md) |
| `identity.claim_cooldown_days` | 90 | [identity-access](../05-trust/identity-access.md) |
| `identity.unverified_ttl_hours` | 72 | [identity-access](../05-trust/identity-access.md) |
| `identity.otp_daily_cap` | 10 | [identity-access](../05-trust/identity-access.md) |
| `identity.phone_stale_months` | 12 | [identity-access](../05-trust/identity-access.md) |
| `identity.session_*` | customer 30 d sliding; seller 12 h idle / 7 d absolute; admin 30 min idle / 12 h absolute | [identity-access](../05-trust/identity-access.md) |
| `identity.phone_change_cooldown_hours` | 72 | [identity-access](../05-trust/identity-access.md) |

## `risk`

Owner: Fraud/Risk Manager

| Key | Proposed default | Defined in |
|---|---|---|
| `risk.hold_dual_control_threshold` | 1,000,000 IQD | [admin-governance](../05-trust/admin-governance.md) |
| `risk.review_sla_hours` | 12 | [fraud-risk](../05-trust/fraud-risk.md) |

## `privacy`

Owner: Compliance

| Key | Proposed default | Defined in |
|---|---|---|
| `privacy.dsr_sla_days` | 30 | [privacy-audit](../05-trust/privacy-audit.md) |

## `backoffice`

Owner: Super Admin (dual control)

| Key | Proposed default | Defined in |
|---|---|---|
| `backoffice.approval_ttl_hours` | 72 | [admin-governance](../05-trust/admin-governance.md) |

## `firstparty`

Owner: Finance Manager with the accountant

| Key | Proposed default | Defined in |
|---|---|---|
| `firstparty.costing_method` | WEIGHTED_AVERAGE | [first-party-operations](../03-sellers/first-party-operations.md) |

Total keys: 141.
