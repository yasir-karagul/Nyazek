# Seller Accounts, Onboarding & KYC

**Authoritative for:** seller types, registration and onboarding, KYC documents and review, seller account states, store profile, pickup addresses, vacation mode, the 1P store, account closure.
**Related:** [identity-access](../05-trust/identity-access.md) · [seller-dashboard](seller-dashboard.md) · [seller-performance](seller-performance.md) · [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) · [compliance-legal](../05-trust/compliance-legal.md)

---

## 1. Seller types

| Type | Profile | Review path |
|---|---|---|
| Individual Entrepreneur | Home-based or solo seller | Standard review |
| Business | Registered retailer or company | Priority review |
| Brand Distributor / Importer | Authorised brand representative | Priority review + brand verification |
| 1P (Nyazek Official Store) | System-owned seller entity | No KYC; operated from the Admin Panel (§8) |

- SEL-1 A seller account is never an upgrade of a customer account. A person who buys and sells uses two accounts with different emails ([identity-access](../05-trust/identity-access.md) §3).
- SEL-2 Selling is free to join; revenue comes from commission.
- SEL-7 One seller account operates exactly one store. A business that wants a second storefront registers a second seller account with its own email and KYC.
- SEL-8 A seller must be established in the market where it sells and ship from pickup addresses in that market (MKT-3). Sellers located abroad cannot register in v1.0.

## 2. Registration and onboarding

1. **Create account** on the Seller Dashboard origin: email, password, mobile phone. Email and phone are both verified; the page states "Use a business email that you do not use for shopping on Nyazek."
2. **Set up 2FA** (mandatory before continuing).
3. **Wizard step 1: Business info**: seller type, legal name, store name, categories intended, addresses.
4. **Wizard step 2: Documents**: per §3.
5. **Wizard step 3: Payout**: payout destination in the name of the KYC identity.
6. **Wizard step 4: Review and submit**: accept the Seller Agreement (version recorded).
7. **Status page**: review progress, requests for more information, decision.

The seller can save and resume the wizard. Until approval the account can only access onboarding and status pages.

## 3. KYC documents

| Document | Required for | Notes |
|---|---|---|
| National ID or passport | All sellers | Government photo ID of the owner or authorised signatory |
| Trade licence / commercial registration | Business, Brand Distributor | Valid and current |
| Tax registration number | Business, Brand Distributor | Individuals exempt at launch |
| Authorised signatory ID and proof of authority | Business, Brand Distributor | Shows the applicant may bind the company |
| Proof of business address or storefront photo | All sellers | For individuals, proof of the pickup address |
| Payout destination details | All sellers | Bank account or supported wallet in the KYC name |
| Brand authorisation letter | Brand Distributor | Issued by the brand owner; per brand |
| Regulated-category licence | Sellers in Health & Pharmacy, Groceries & Food and other regulated categories | Expiry tracked; lapse suspends affected offers |
| E-commerce licence number | If counsel confirms sellers need their own ([compliance-legal](../05-trust/compliance-legal.md) §3) | Shown on the store page if required |

## 4. KYC process

- KYC-1 **Every application is reviewed by a person** (Seller Manager role). v6's "auto-approve established retailers with verified docs" is removed: no automated source exists to verify Iraqi trade licences, and approving sellers without review is a fraud and anti-money-laundering exposure. Business and Brand Distributor applications enter a priority queue instead. Automated document verification through a vendor is a P2 option (ratification: D-24).
- KYC-2 Review target: decision or information request within `cfg:kyc.review_sla_hours` (default 24) of submission. The clock pauses while waiting for the seller. A breach alerts the Seller Manager.
- KYC-3 Outcomes: approve, reject with reasons, or request specific corrections (`NEEDS_INFO`).
- KYC-4 A rejected applicant may reapply with corrected documents, limited to `cfg:kyc.max_attempts_per_30_days` (default 3).
- KYC-5 Duplicate detection: the same identity document, trade licence, payout destination, phone or device on another seller account flags the application for review.
- KYC-6 Sanctions and watch-list screening is performed as required by counsel and the PSP.
- KYC-7 Document expiry is tracked: reminders at 30 and 7 days; on lapse of an identity or business document the seller is `RESTRICTED`; on lapse of a category licence only the affected offers are suspended.
- KYC-8 Re-verification is triggered by a payout-destination change, a change of legal name or signatory, or cumulative payouts exceeding `cfg:kyc.reverify_payout_threshold` (default set by Compliance).
- KYC-9 KYC documents are stored in a dedicated encrypted bucket; identity numbers and bank details use field-level encryption; access is limited to the Seller Manager and Compliance roles and every view is logged. Documents are never exposed through seller-facing or public APIs after upload (the seller sees status and file names only).

## 5. Seller account states

| State | Entered when | Dashboard | Offers | Orders | Payouts |
|---|---|---|---|---|---|
| `REGISTERED` | Account created and verified | Onboarding only | – | – | – |
| `KYC_SUBMITTED` / `KYC_IN_REVIEW` / `NEEDS_INFO` | Wizard submitted | Onboarding and status | – | – | – |
| `REJECTED` | KYC rejected | Status and reapply | – | – | – |
| `ACTIVE` | KYC approved | Full | Live | Normal | Normal |
| `RESTRICTED` | Performance Level 2–3, lapsed document, persistent wallet deficit (WAL-10) | Full, with warnings | Level 2: reduced visibility. Level 3, document lapse or deficit: no new offers | Normal | Normal; monthly cycle at Level 2 or worse (PO-1) |
| `SUSPENDED` | Level 4 decision, investigation, serious violation, or a temporary fraud freeze (SEL-3) | Read-only, except fulfilment actions for open sub-orders, returns and disputes, plus appeal and support | Hidden | Unconfirmed sub-orders cancelled (`SELLER_SUSPENDED`); confirmed ones stay with the seller (SLA-7); Nyazek handles returns and disputes the seller does not (REF-5) | Frozen (suspension hold) |
| `CLOSING` | Closure requested or decided | Read-only, except fulfilment actions for open sub-orders, returns and disputes | Hidden | Open orders complete; no new orders | Final settlement pending |
| `CLOSED` | Final settlement done | History export only | – | – | – |

Allowed transitions (every other transition is rejected):

| From | To | Trigger |
|---|---|---|
| `REGISTERED` | `KYC_SUBMITTED` | Seller submits the wizard |
| `KYC_SUBMITTED` | `KYC_IN_REVIEW` | Reviewer picks up the application |
| `KYC_IN_REVIEW` | `ACTIVE`, `REJECTED`, `NEEDS_INFO` | KYC decision |
| `NEEDS_INFO` | `KYC_SUBMITTED` | Seller resubmits |
| `REJECTED` | `KYC_SUBMITTED` | Reapplication within the attempt limit of KYC-4 |
| `ACTIVE` | `RESTRICTED` | Level 2 or 3, document lapse, deficit (automatic), or a Seller Manager decision with reason (policy violation short of suspension) |
| `RESTRICTED` | `ACTIVE` | Every restricting cause cleared (automatic; a manual restriction is lifted by the Seller Manager) |
| `ACTIVE`, `RESTRICTED` | `SUSPENDED` | Dual control, or temporary fraud freeze (SEL-3) |
| `SUSPENDED` | `ACTIVE` or `RESTRICTED` | Suspension lifted (dual control) or temporary freeze lapsed unconfirmed; returns to the state the causes justify |
| `ACTIVE`, `RESTRICTED`, `SUSPENDED` | `CLOSING` | Seller request (not while suspended for investigation) or admin decision |
| `CLOSING` | `CLOSED` | Final settlement done (commission-wallet-payouts §7) |

- SEL-3 Suspension is a dual-control action. In an urgent fraud case the Fraud/Risk Manager may apply an immediate temporary freeze that lapses after 24 hours unless a second approver confirms it ([admin-governance](../05-trust/admin-governance.md) §3).
- SEL-4 Every state change records actor, reason code and note, emits `seller.status_changed`, and notifies the seller with the reason and the appeal route.

## 6. Store profile and settings

- Public store page: name, logo, banner, about text, policies, rating (after the minimum count), verified badge, seller identity details required by law.
- Pickup addresses: one or more, each a structured address; an offer's shipping origin is one of them. The first is the default return address.
- Handling time default per store, overridable per offer.
- Return policy: sellers may be more generous than the platform rules, never less.
- Sellers cannot set shipping fees.
- SEL-5 A pickup address cannot be removed while an active offer uses it as its origin or a non-terminal sub-order or return ships from or to it. The seller first moves the offers to another address.
- SEL-6 The store name, logo, banner and about text pass the content pre-screen (prohibited words, contact details, links, trademark terms the seller is not authorised for). A store name can be changed at most once every 30 days; the previous store URL redirects to the new one. The store slug is unique and derived from the store name by a fixed Arabic-to-Latin transliteration, with a numeric suffix on collision; it is read-only for the seller and changes with the name. Former slugs stay reserved to the store and redirect to it; a managed list of reserved words (for example the platform name, "official", "support") cannot be used. The Seller Manager may correct a slug on `AD-USR-SELLER`; a correction holds until the next name change ([ADR-0007](../../adr/0007-decisions-from-the-ia-consistency-pass.md)).

### 6.1 Vacation mode (P1)

Pauses all offers for up to `cfg:sellers.vacation_max_days` (default 30) without performance penalty. Open orders must still be fulfilled. Offers resume automatically at the end date.

- SEL-9 Vacation mode cannot start while any of the seller's sub-orders is in `PENDING_SELLER_CONFIRMATION`; the seller confirms or rejects them first. The check runs when vacation is turned on and again at a scheduled start date; the `sellers` module asks the `orders` module through its exported query (ARC-3). A sub-order that reaches the seller during vacation (a COD hold released, a late prepaid payment) follows the normal confirmation SLA and is notified to the seller; if it is cancelled by that SLA, the cancellation is excluded from the seller's performance metrics. There is no allowance beyond the maximum duration ([ADR-0007](../../adr/0007-decisions-from-the-ia-consistency-pass.md)).

## 7. Store staff (P1)

At launch only the owner signs in. From P1 the owner invites staff with preset roles; staff are separate accounts in the seller realm ([seller-dashboard](seller-dashboard.md) §3, [identity-access](../05-trust/identity-access.md)).

## 8. The 1P store (Nyazek Official Store)

- A system-owned seller entity of type 1P, shown with a 1P badge. Its operations (goods receipts, cost, adjustments, returns) are specified in [first-party-operations](first-party-operations.md).
- Operated in the Admin Panel by the 1P Merchandiser role; it has no seller login and therefore no identity conflict.
- Uses the same offer, order, shipment and return flows as 3P, plus cost price, supplier and margin fields.
- Minimum 1P operations at launch (P0): stock receiving and adjustments with cost, pricing, margin alerts, order fulfilment through the same order screens (admin variant), returns to the Nyazek warehouse.
- Purchase orders, supplier management beyond a basic record, and warehouse pick/pack management are post-launch and must exist before 1P volume scales.
- 1P is exempt from commission and from performance consequences (levels, appeals, seller states); its score is computed like any seller's and used only for the Buy Box and search (PRF-7).

## 9. Closure

- A seller may request closure; Nyazek may close an account after investigation.
- During `CLOSING`: no new orders; open orders, returns and disputes run to completion; final payout after the last return window ends and any deficit is recovered.
- After closure the profile is anonymised except for records under legal retention; the email and phone claims are released after the cooling-off period ([identity-access](../05-trust/identity-access.md) ID-8).

## 10. Acceptance criteria

- A seller cannot create an offer or receive an order in any state other than `ACTIVE` or `RESTRICTED`.
- No seller becomes `ACTIVE` without a recorded human approval.
- An application reusing another seller's identity document is flagged.
- KYC files are not retrievable through any seller or public endpoint.
