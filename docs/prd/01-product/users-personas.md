# Users & Personas

**Authoritative for:** customer, seller and internal personas and what each needs from the product.
**Related:** [overview-vision-kpis](overview-vision-kpis.md) · [user-journeys](user-journeys.md) · [seller-accounts-kyc](../03-sellers/seller-accounts-kyc.md) · [admin-governance](../05-trust/admin-governance.md)

---

## 1. Customer personas

| Persona | Profile | Pain | Needs | Motivators |
|---|---|---|---|---|
| Urban Explorer (primary) | 18–30, Baghdad, mobile-first, compares prices, reads reviews, buys deals on impulse | Hours spent across social groups to find products | Fast, reliable mobile experience; everything discoverable in seconds | Deals, loyalty points, brand variety |
| Family Shopper | 30–50, nationwide, desktop and mobile, deliberate, buys household essentials | Cannot trust quality or delivery promises on informal channels | Verified sellers, clear specifications, easy returns, reliable delivery | Convenience, trust signals, money-back guarantee |
| Student / Young Professional | 18–28, all served governorates, mobile, budget-conscious | Limited local availability outside Baghdad | Nationwide delivery, promotions, referral rewards | Referral bonuses, birthday reward, loyalty tiers |

Design implications common to all three: phone-number-first identity, COD as the expected default, low-bandwidth tolerance, Arabic-first content, landmark-based addresses.

These personas describe the Iraq launch market. Customer habits differ in the expansion markets (for example card and wallet payment and structured addresses in the Gulf); personas are revalidated in each market-entry assessment ([market-expansion](market-expansion.md) §6). What each persona does end to end is in [user-journeys](user-journeys.md).

## 2. Seller personas

| Seller type | Profile | Key need | Onboarding |
|---|---|---|---|
| Individual Entrepreneur | Home-based or solo seller, often phone-only | Simple listing tools, fast payout, mobile-friendly dashboard | Standard KYC review |
| Business (established retailer) | Brick-and-mortar store going online | Bulk import, order management, staff accounts | Priority KYC review |
| Brand Distributor / Importer | Authorised representative of brands | Brand protection (gating, MAP), verified badge | Priority review + brand verification |
| Nyazek 1P team | Internal merchandisers selling Nyazek's own stock | Pricing and margin control, stock receiving | Internal; operates through the Admin Panel |

A seller account is never an upgrade of a customer account; a person who buys and sells holds two accounts with different emails ([identity-access](../05-trust/identity-access.md)).

## 3. Internal users

The eleven admin roles in [admin-governance](../05-trust/admin-governance.md) are also users of the product. Their work queues (KYC, catalogue review, moderation, disputes, refunds, reconciliation, risk, logistics exceptions) are P0 features: the marketplace cannot run without them.

## 4. Other parties

| Party | Interaction |
|---|---|
| Couriers | APIs, files or a simple portal for status and COD statements ([logistics](../02-commerce/logistics.md) §1.1) |
| Payment providers | APIs, webhooks, settlement files |
| Brand owners | Requests for gating, MAP and takedowns, handled by the Catalog Manager |
| Regulators and counsel | Disclosures, records, notifications ([compliance-legal](../05-trust/compliance-legal.md)) |
