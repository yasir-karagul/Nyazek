# Market Expansion: Syria and the Gulf

**Authoritative for:** the expansion scope, the market concept, what must be market-ready at the Iraq launch and what is deferred, market profiles, market-entry gates.
**Status:** Iraq is the only launch market. Statements about other countries come from public sources as of November 2026 (§7) and must be validated by local counsel and tax advisers before any market entry. Nothing in this document is legal or tax advice.
**Related:** [overview-vision-kpis](overview-vision-kpis.md) · [scope-priorities](scope-priorities.md) · [architecture](../06-platform/architecture.md) §6 · [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §2 · [tax-invoicing](../04-finance/tax-invoicing.md) · [compliance-legal](../05-trust/compliance-legal.md) · [open-decisions](../00-governance/open-decisions.md) D-39 to D-41

---

## 1. Scope

- Nyazek launches in **Iraq only** (v1.0). The planned expansion markets are **Syria** and the **Gulf** (Saudi Arabia, United Arab Emirates, Kuwait, Qatar, Bahrain, Oman). Order and timing are an owner decision (D-40).
- Opening another market is post-launch work (priority **Future**). No screen, operation or integration for another market is built in v1.0.
- What **is** P0 is **market readiness** (§3): design constraints that make a later market a configuration, integration and operations project instead of a rewrite. They cost little now and are very expensive to retrofit into a ledger, an order model and three clients.

## 2. The market concept

| ID | Rule |
|---|---|
| MKT-1 | A **market** is a country in which Nyazek operates, with its own legal entity or branch, currency, tax regime, payment methods, couriers, address model, legal documents, catalogue rules and operating team. Markets are identified by ISO 3166-1 alpha-2 codes (`IQ`, `SY`, `SA`, `AE`, `KW`, `QA`, `BH`, `OM`). |
| MKT-2 | A market is not a language. **Locale** is language and formatting; **market** is the commercial and legal context. Arabic and English are available in every market; a market may add languages (Kurdish, D-13). |
| MKT-3 | Each market is a **domestic marketplace**: sellers established in the market sell to customers with delivery addresses in the market, in the market's currency, delivered by that market's couriers. Cross-border selling and fulfilment are out of scope (D-41, decided; revisited at the second market). |
| MKT-4 | Every order, seller entity, offer, price, stock record, shipment, payment, journal entry, issued document, legal acceptance and market-scoped configuration value belongs to exactly one market. |
| MKT-5 | An account is registered in one market. The one-email-one-account rule (ID-1) holds across all markets. A seller entity belongs to one market; selling in another market requires an entity established and verified there (one login managing entities in several markets is not supported; revisited at the second market, D-41). |
| MKT-6 | Canonical product content (title, attributes, images) may be shared between markets. Offers, prices, stock, availability, compliance flags, prohibited and restricted lists, commission schedules and return policies are per market. |
| MKT-7 | One codebase serves all markets. Whether markets share one deployment and database or run as separate deployments (needed where a data-localisation rule requires it) is decided per market at entry (D-39, decided). The architecture must not preclude either. |

## 3. Readiness requirements at the Iraq launch (P0)

| Area | Requirement | Specified in |
|---|---|---|
| Market context | Country, currency, time zone, phone ranges, administrative divisions, price step, quiet hours and working week come from market configuration, never from literals in business logic | [architecture](../06-platform/architecture.md) §6 |
| Money | Integer amounts in the currency's platform minor unit, always with a currency code; a per-currency exponent and price step; no arithmetic across currencies | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) MON-1, MON-8 |
| Ledger | One book per market and legal entity in its functional currency; no journal entry mixes currencies | [ledger-reconciliation](../04-finance/ledger-reconciliation.md) LED-6 |
| Tax and documents | Tax region and category on every line; inclusive or exclusive presentation per market; document templates, numbering series and an e-invoicing port per market | [tax-invoicing](../04-finance/tax-invoicing.md) TAX-5, TAX-6 |
| Addresses and geo data | A generic hierarchy (country → level 1 → level 2 → level 3) with per-market labels and required fields | [checkout-orders](../02-commerce/checkout-orders.md) ADR-5 |
| Phone numbers | E.164 with valid mobile ranges per market | [identity-access](../05-trust/identity-access.md) §3.1 |
| Configuration | Every `cfg:` value can be overridden per market (market value, else platform default) | [admin-governance](../05-trust/admin-governance.md) §5 |
| Providers | PSP, courier, SMS and e-invoicing adapters are selected per market behind the existing ports | [architecture](../06-platform/architecture.md) ARC-8 |
| Legal content and consent | Legal documents, policy versions, acceptance and consent records per market | [support-cms](../02-commerce/support-cms.md) CMS-2 |
| Catalogue compliance | Prohibited and restricted lists, regulated categories and licences per market | [catalog-listings](../02-commerce/catalog-listings.md) §7 |
| Notifications | Sender IDs, templates, quiet hours and time zone per market | [notifications-messaging](../02-commerce/notifications-messaging.md) NTF-2 |
| Metrics | A market dimension on every metric; no sum across currencies without an explicit, dated conversion | [data-analytics](../06-platform/data-analytics.md) §4 |
| Language | All strings in message catalogues; search synonyms and dialect terms per market | [search-buy-box](../02-commerce/search-buy-box.md) §1.2 |
| Data location | Storage and databases region-pinned and relocatable per market | [infrastructure-devops](../06-platform/infrastructure-devops.md) INF-7 |

- MKT-8 Readiness means the data model, contracts and configuration **carry** the market. It does not mean building market switchers, multi-currency display, currency conversion or cross-market administration in v1.0. Only `IQ` is enabled.
- MKT-9 A static check fails the build when market literals (`IQD`, `+964`, `Asia/Baghdad`, the governorate list, the 250 price step) appear in business logic outside market configuration, seed data and tests.

## 4. Deferred until a market is opened

Market selection in the clients · a second currency in display, quotes or the ledger · currency conversion and consolidated reporting · market-specific payment, courier, SMS and e-invoicing adapters · market-specific KYC document sets · VAT-inclusive pricing and VAT invoices · per-market legal pack · cross-market admin roles and reporting · data-localised deployments.

## 5. Market profiles

Indicative only. Each row is re-verified in the market-entry assessment (§6).

| Market | Currency (ISO decimals) | VAT | Payments landscape | Points that change the product |
|---|---|---|---|---|
| Iraq (launch) | IQD (3 in ISO; fils unused, platform exponent 0, price step 250) | None general | COD dominant; mobile wallets | Reference market for this PRD |
| Syria | SYP, redenominated on 1 January 2026 (100 old = 1 new) | Counsel to confirm | Cash-based; mobile wallets (Syriatel Cash, MTN Cash, Sham Cash); international card networks reconnected during 2026 | Currency volatility and price display rules; COD-first; unstructured addresses; sanctions were largely lifted in 2025–2026 but screening of parties and banks stays mandatory; licensing and tax rules under reform |
| Saudi Arabia | SAR (2) | 15% | Cards, mada, wallets, buy-now-pay-later; COD share falling | VAT-inclusive prices and tax invoices; mandatory e-invoicing integrated with the tax authority; E-Commerce Law and commercial registration; Personal Data Protection Law with rules on transfers abroad; structured national address |
| United Arab Emirates | AED (2) | 5% | Cards, wallets, buy-now-pay-later | VAT invoices; e-invoicing being phased in for business transactions; federal data-protection law; no postal codes; UTC+4; Saturday–Sunday weekend |
| Kuwait | KWD (3) | Not introduced | Cards, KNET | Three-decimal currency |
| Qatar | QAR (2) | Not introduced | Cards | Data-protection law |
| Bahrain | BHD (3) | 10% | Cards, Benefit | Three-decimal currency; VAT invoices; data-protection law |
| Oman | OMR (3) | 5% | Cards | Three-decimal currency; VAT invoices; data-protection law; UTC+4 |

Product consequences already reflected in §3: currencies with zero, two and three decimals; tax-inclusive pricing with compliant invoices and real-time e-invoicing; payment-method types beyond wallets and COD (instalments and buy-now-pay-later stay out of scope until a market needs them); structured and unstructured address models; data-transfer rules that may force a separate deployment.

## 6. Market entry

- MKT-10 Work on a new market starts only after an owner decision (D-40) based on a written market-entry assessment: demand, competition, unit economics, regulation, sanctions exposure, payment and courier options, staffing.
- MKT-11 Recommended precondition: Iraq has completed P0 and P1, shows three consecutive months of clean reconciliation and a stable or improving contribution margin, and on-call is staffed (D-27).
- MKT-12 Entry gates (all required before a market goes live):

| Gate | Evidence |
|---|---|
| Legal entity, licences and registrations | Counsel sign-off for the market |
| Legal pack | Terms, privacy, returns, seller agreement and disclosures in the market's required form |
| Tax | Registration, invoice form, e-invoicing compliance, accountant sign-off of the market's book |
| Payments and custody | At least one PSP contract; custody model confirmed for the market (D-09 repeated per market) |
| Logistics | Two couriers, serviceability matrix, geo reference dataset, COD remittance terms |
| Messaging | SMS routes and sender ID; templates reviewed for dialect |
| Configuration | The market's `cfg:` set ratified; price step and currency format decided |
| Data location | Residency and transfer position decided; deployment model chosen (D-39) |
| Risk and compliance | Sanctions and AML screening rules for the market; KYC document set |
| Security | Penetration-test delta for new integrations |
| Operations | Named owners for every admin role in the market; support in the local dialect |
| Supply | Seller acquisition and catalogue seeding plan met |
| Beta | Closed beta in the market with exit criteria met |

## 7. Sources (November 2026)

- Syria sanctions: [CRS, July 2026](https://www.everycrsreport.com/files/2026-07-10_IN12712_48cb7e51ec796dfc5ce9d67c5b07ae1d3dbdd633.html), [Cleary Gottlieb, July 2026](https://www.clearytradewatch.com/2026/07/u-s-government-removes-syria-from-list-of-state-sponsors-of-terrorism/), [Just Security](https://www.justsecurity.org/125619/removing-syria-state-sponsor-terrorism-designation/)
- Syrian currency: [bne IntelliNews](https://www.intellinews.com/syria-rolls-out-new-currency-in-redenomination-push-418039/), [Arab News](https://www.arabnews.pk/node/2627711/middle-east)
- Syrian payments: [The New Arab](https://www.newarab.com/news/visa-mastercard-arrive-syria-will-help-economy), [The Fintech Times](https://thefintechtimes.com/syria-can-fintech-rebuild-a-country-after-revolution-and-war/)
- Gulf VAT: [Khaleej Times](https://www.khaleejtimes.com/gcc-vat-overhaul-set-to-tighten-cross-border-trade-raise-compliance-stakes), [VATupdate on Kuwait](https://www.vatupdate.com/2026/07/24/kuwait-keeps-vat-off-the-table-no-adoption-in-the-2026-2030-fiscal-plan/), [PwC tax summaries, Qatar](https://taxsummaries.pwc.com/qatar/corporate)
- Saudi Arabia: [Chambers TMT 2026](https://practiceguides.chambers.com/practice-guides/tmt-2026/saudi-arabia/trends-and-developments), [Chambers Data Protection 2026](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/saudi-arabia), [Mondaq legal guide](https://www.mondaq.com/saudiarabia/contracts-and-commercial-law/1672154/online-business-in-saudi-arabia-legal-guide-for-entrepreneurs-and-investors)
- UAE e-invoicing: [KPMG](https://kpmg.com/us/en/taxnewsflash/news/2026/07/tnf-uae-phased-implementation-of-e-invoicing-beginning-january-1-2027.html), [Fonoa](https://www.fonoa.com/resources/blog/uae-national-electronic-invoicing-system-rollout)

## 8. Acceptance criteria

- Creating a second market in a test environment (different currency exponent, price step, time zone, phone range, address labels and tax rate) requires configuration and seed data only; the order, quote, ledger and document suites pass for it unchanged.
- The static check in MKT-9 passes.
- No API response, event or document carries an amount without its currency.
