# Product Overview, Vision, Goals & KPIs

**Authoritative for:** what Nyazek is, the problem, vision and goals, success metrics, competitive positioning.
**Related:** [users-personas](users-personas.md) · [user-journeys](user-journeys.md) · [business-model](business-model.md) · [scope-priorities](scope-priorities.md) · [market-expansion](market-expansion.md) · [data-analytics](../06-platform/data-analytics.md) §4

---

## 1. Summary

Nyazek (نيازك) is a trust-first, multi-vendor marketplace that launches in Iraq and is planned to expand to Syria and the Gulf. It combines a first-party retail operation (1P, the Nyazek Official Store) with a third-party seller marketplace (3P) on one platform.

| Aspect | Decision |
|---|---|
| Launch market | Iraq; all 19 governorates |
| Planned expansion | Syria and the Gulf states, after launch, one market at a time ([market-expansion](market-expansion.md)) |
| Currency | Iraqi dinar (IQD) only at launch; one currency per market |
| Languages | Arabic (default, RTL) and English |
| Clients at launch | Three web applications on one backend: Storefront (customers), Seller Dashboard (sellers and staff), Admin Panel (Nyazek staff) |
| Clients after launch | Flutter apps for Android and iOS on the same API |
| Architecture | Modular monolith, API-first, client-agnostic ([architecture](../06-platform/architecture.md)) |
| Engineering model | Claude as the sole AI engineering agent under human supervision ([claude-workflow](../08-engineering/claude-workflow.md)) |
| Identity | Customer, seller and admin accounts are strictly separate; one email belongs to exactly one account ([identity-access](../05-trust/identity-access.md)) |
| Timeline | Six months from kickoff (kickoff date and scope fit: D-15) |

## 2. Problem

Iraqi e-commerce is fragmented across social-media groups, classifieds, single-brand sites and informal messaging networks.

- No single destination where customers can discover, compare and buy across categories with confidence.
- Poor customer experience: inconsistent product information, no standard IQD pricing, no formal return policies, no customer protection.
- A growth ceiling for legitimate retailers, who lack the infrastructure, reach and tools to sell online professionally.

Regional platforms have signalled interest in Iraq, which makes a locally built, locally optimised marketplace time-sensitive.

## 3. Vision and goals

**Vision.** To be Iraq's most trusted, comprehensive and convenient marketplace, where every Iraqi can buy anything and every Iraqi business can sell to everyone.

**Strategic goals**

1. Become the default all-category online shopping destination in Iraq before regional competitors gain traction.
2. Build trust through verified sellers, customer protection, held payments and a money-back guarantee.
3. Give sellers professional tools that make Nyazek their primary online channel.
4. Reach product-market fit in Iraq within six months of launch, and build the platform so that Syria and the Gulf can be added as markets without redesign ([market-expansion](market-expansion.md) §3).

## 4. Success metrics

Definitions are authoritative in [data-analytics](../06-platform/data-analytics.md) §4.

| KPI | 6 months after launch | 12 months after launch | Priority |
|---|---|---|---|
| GMV (delivered) | 500M IQD / month | 2B IQD / month | P0 |
| Monthly active customers (MAC) | 20,000 | 100,000 | P0 |
| Active sellers | 200 | 1,000 | P0 |
| Active listings (offers) | 50,000 | 250,000 | P0 |
| Purchase frequency | 1.5 orders / customer / month | 2.5 orders / customer / month | P0 |

### 4.1 The targets are mutually inconsistent (D-01)

MAC requires at least one delivered order, purchase frequency is orders ÷ MAC, and the planning AOV is 50,000–100,000 IQD ([business-model](business-model.md)).

| Horizon | Orders / month (MAC × frequency) | Implied GMV at AOV 50K–100K | Stated GMV | Gap |
|---|---|---|---|---|
| 6 months | 20,000 × 1.5 = 30,000 | 1.5B – 3.0B IQD | 500M IQD | Implied is 3×–6× higher |
| 12 months | 100,000 × 2.5 = 250,000 | 12.5B – 25B IQD | 2B IQD | Implied is 6.25×–12.5× higher |

Read the other way, the stated GMV supports only about 3,300–6,700 active customers at six months. Also, 1.5–2.5 orders per active customer per month is high for a new general marketplace.

**D-01:** the owner re-baselines the set (recommended: derive GMV from MAC × frequency × AOV). Until then these figures are capacity-planning inputs only ([reliability-sre](../06-platform/reliability-sre.md) §5), not acceptance criteria.

### 4.2 Operational KPIs (tracked from launch; targets set in the closed beta)

Payment success rate per method · COD confirmation rate · COD RTO rate · on-time delivery by courier and governorate · seller SLA compliance · return and dispute rates · refund time · search zero-result rate · support first-response time · KYC and catalogue review turnaround · contribution margin per order.

## 5. Competitive differentiation

| Dimension | Nyazek's intended advantage | Dependency |
|---|---|---|
| Payments | COD plus the main Iraqi wallets from day one | PSP or aggregator contracts (D-11); custody model (D-09) |
| Cultural fit | Arabic-first RTL design, Iraqi dialect in search synonyms, Iraq-specific categories and address model | Design-system corrections (D-19) |
| Supply | Early onboarding of Iraqi retailers and brands; seller reviews and history create switching costs | Seller acquisition before launch; payout cadence (D-03) |
| Trust | Held payments, money-back guarantee, verified sellers | KYC operations; dispute handling capacity |
| Logistics | Courier abstraction, governorate-level serviceability, COD controls | Courier contracts and capabilities (D-28) |
| Timing | First-mover brand recognition | Launch date (D-15) |

These are goals, not facts: each depends on external agreements listed in the release plan as long-lead items. v6 described them as an "insurmountable moat"; none is durable without execution, and regional entrants can contract the same couriers and payment providers.

## 6. Assumptions

- A PSP or aggregator will support the launch wallets with refund capability or an agreed manual process.
- At least two couriers will cover the 19 governorates between them with COD and a workable remittance cycle.
- Legal entity and e-commerce licence can be obtained before launch (D-14).
- A human team exists for KYC review, catalogue review, support, finance operations and logistics exceptions; the platform automates, it does not remove these roles ([release-plan](../00-governance/release-plan.md) §6).
- The KPIs, personas and unit economics in this set describe Iraq. Each expansion market gets its own targets in its market-entry assessment (MKT-10).
