# Compliance, Legal & Regulatory Readiness

**Authoritative for:** regulatory landscape, platform obligations and their owners, governing law and dispute tiers, liability position, contracts. This document covers **Iraq**, the launch market; the regulatory outline for Syria and the Gulf is in [market-expansion](../01-product/market-expansion.md) §5 and each new market gets its own legal pack (MKT-12).
**Status:** every statement here comes from public sources as of November 2026 and must be validated by Iraqi legal counsel. Nothing in this document is legal advice.
**Related:** [privacy-audit](privacy-audit.md) · [tax-invoicing](../04-finance/tax-invoicing.md) · [payments](../04-finance/payments.md) §2 · [open-decisions](../00-governance/open-decisions.md)

---

## 1. Governing law and dispute tiers

- Platform agreements (Terms & Conditions, Seller Agreement, Customer Protection Policy) are governed by the laws of the Republic of Iraq, with Iraqi courts as the primary forum.
- Tier 1: platform resolution ([returns-disputes](../02-commerce/returns-disputes.md) §6). Tier 2: direct negotiation for 15 business days. Tier 3: competent Iraqi courts. Commercial (seller) disputes above a threshold may go to binding arbitration at either party's election; the threshold and rules are set by counsel.
- Kurdistan Region courts, registration and commercial rules are checked separately (D-13).

### 1.1 Liability position (for counsel)

v6 limited Nyazek's liability to the commission value of the disputed transaction and disclaimed product quality for 3P sales beyond the money-back guarantee. Counsel must review these against consumer-protection law; liability caps generally cannot exclude fraud or gross negligence, and a marketplace that sets prices of shipping, handles payment and decides disputes may carry more responsibility than a pure intermediary. Product copy and policies follow counsel's wording.

## 2. Regulatory landscape

| Instrument | What public sources say | Open point for counsel |
|---|---|---|
| E-Commerce Regulation No. 4 of 2025 (Cabinet Resolution 135 of 2025; Official Gazette issue 4818 of 10 March 2025; effective April 2025) | Applies where the seller or the customer is in Iraq. E-commerce merchants need a licence from the Ministry of Trade. Requires disclosure of identity, licence number, product details, prices, terms, return policy and privacy policy; secure systems, minimal data collection, explicit consent; breach notification; tasks the General Commission for Taxes with a tax mechanism | Status of the licensing portal and implementing instructions; whether each marketplace seller needs its own licence; breach-notification timelines |
| Communications and Media Commission, Framework Regulations for Digital Platforms and Services (issued 17 February 2025) | Lists e-commerce among regulated digital services and sets tiered notification, registration or licensing duties | Whether and at which tier Nyazek is covered |
| Data protection | No comprehensive data-protection law is in force; a draft remains unenacted | Applicable privacy duties in sector rules; data-residency expectation (meaning defined with counsel, INF-8) |
| Payments | Card and wallet acceptance runs through Central Bank-licensed providers | Whether holding customer funds or COD cash before paying sellers needs authorisation (D-09) |
| Consumer protection, electronic transactions and signatures, anti-money-laundering, competition and trademark laws | General statutes apply to online sales, e-contracts, seller onboarding and pricing practices | Return-right minimums, e-contract validity, KYC and screening scope, MAP enforcement |
| Tax | No general VAT; sector taxes and customs exist | Invoice form, any platform reporting or withholding duty ([tax-invoicing](../04-finance/tax-invoicing.md)) |

## 3. Obligations and platform implications

| Obligation | Platform implication | Phase |
|---|---|---|
| Legal entity, commercial registration, e-commerce licence (D-14) | Launch-blocking. Legal workstream starts at kickoff | 1 |
| Digital-platform registration or licence, if applicable | Counsel confirms tier; resulting tasks become launch gates | 1 |
| Seller licensing | If sellers need their own licence: licence number collected at KYC and shown on the store page | 1–2 |
| Mandatory disclosures | Entity name, registration and licence number in every footer; seller identity on product and store pages; price, shipping fee, delivery estimate, return policy and terms visible before purchase | 2 |
| Consent and privacy | Consent records, policy versions, minimisation, data-subject requests ([privacy-audit](privacy-audit.md)) | 2–3 |
| Breach notification | Incident runbook includes assessment, regulator and user notification steps with Arabic and English templates; contact list maintained | 3 |
| Requests from authorities | Logged procedure owned by Compliance with counsel ([privacy-audit](privacy-audit.md) DSR-4) | 3 |
| Product safety and recalls | Recall procedure and customer notification ([catalog-listings](../02-commerce/catalog-listings.md) PRH-5) | 3 |
| Honest pricing and advertising | Reference-price rule (PRC-9), sponsored labelling (AD-6), no misleading claims | 2–3 |
| Regulated categories | Licences collected and tracked; prohibited list enforced ([catalog-listings](../02-commerce/catalog-listings.md) §2.1, §7) | 2 |
| AML and sanctions | Seller KYC and screening as required by counsel and the PSP; suspicious-activity escalation path | 1–2 |
| Age | Customers confirm they are 18 or older | 2 |
| Records | Seven-year retention of financial records and documents | 2 |
| Accessibility and language | Arabic as the primary language of all legal content | 2 |
| App stores (later) | Privacy disclosures, account deletion in-app, physical goods paid outside in-app purchase | With apps |

## 4. Contracts required before launch

| Contract | Key terms to secure |
|---|---|
| PSP or aggregator | Settlement cycle, refund and payout capability, fees, custody model, chargeback handling, sandbox, uptime |
| Couriers | Delivery SLA per zone, attempts, proof of delivery, COD remittance SLA and liability for cash, loss and damage liability, data protection, API or file exchange |
| SMS aggregator(s) | Iraqi routes, sender ID, OTP delivery targets, pricing, fallback |
| Seller Agreement | Fees, payout cycle and holds, performance levels, return cost rules, deficit recovery, data use, termination |
| 1P suppliers | Supply terms, returns to supplier, warranties |
| Cloud, edge and other processors | Data-processing terms, sub-processors, location of data |

## 5. Policies to publish

Terms & Conditions, Privacy Policy, Cookie Policy, Return & Refund Policy, Shipping Policy, Customer Protection Policy, Dispute Resolution Policy, Seller Agreement and fee schedule, Prohibited & Restricted Items Policy, intellectual-property notice procedure, loyalty programme terms (with loyalty). All are drafted by counsel, in Arabic and English, versioned in the CMS.

## 6. Sources

- Al Tamimi & Company, "Iraq's New E-Commerce Regulation" ([link](https://www.tamimi.com/law-update/real-estate-construction-and-hotels-leisure/articles/iraqs-new-e-commerce-regulation/))
- Al Tamimi & Company, "New Regulatory Framework for Digital Platforms and Services in Iraq" ([link](https://www.mondaq.com/financial-services/1684654/new-regulatory-framework-for-digital-platforms-and-services-in-iraq))
- Communications and Media Commission, Framework Regulations ([link](https://cmc.iq/ar/wp-content/uploads/2025/03/Framework-regulations-for-digital-platforms-and-services-en.pdf))
- Chambers, "Iraq: Trends and Developments 2026" ([link](https://gpg-pdf.chambers.com/corporate-m-and-a-2026/630/))

## 7. Acceptance criteria (launch gate)

- Counsel has signed off the legal documents, the custody model, the invoice form and the licence position.
- Entity and licence details are live in the footer and on seller pages.
- The breach-notification procedure has been rehearsed once.
