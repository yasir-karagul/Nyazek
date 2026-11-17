# Ledger & Reconciliation

**Authoritative for:** money representation and rounding, chart of accounts, posting rules for every financial event, ledger invariants, reconciliation.
**Related:** [payments](payments.md) · [commission-wallet-payouts](commission-wallet-payouts.md) · [tax-invoicing](tax-invoicing.md) · [business-model](../01-product/business-model.md)
**Gate:** the chart of accounts, posting rules and IFRS 15 timing must be validated by Nyazek's accountant before the ledger schema is frozen (Phase 1 exit criterion).

---

## 1. Principles

- LED-1 Every financial event produces exactly one balanced journal entry. Single-sided entries do not exist.
- LED-2 The journal is append-only. Corrections are new reversing entries that reference the original. No row is updated or deleted; the database role used by the application has no `UPDATE` or `DELETE` privilege on journal tables.
- LED-3 The ledger records Nyazek's obligations and assets **regardless of where cash physically sits** (PSP, courier, bank). The custody model (D-09) changes which asset account is debited, not the liabilities.
- LED-4 Every journal entry has a unique idempotency key derived from its business event (for example `escrow-release:<subOrderId>:<releaseSeq>`, where `releaseSeq` numbers the partial releases of one sub-order, WAL-4), so a retried event can never post twice.
- LED-5 Seller wallet balances are **views over ledger accounts**, never separately stored numbers that could drift.
- LED-6 The ledger is kept as one **book per market and legal entity**, in that market's functional currency. A journal entry never mixes currencies or books. Consolidation and currency translation across markets happen outside the platform, in the group's accounting system. Only the Iraq book exists at launch.
- LED-7 Books are closed monthly by Finance. A closed period accepts no new entries dated inside it; corrections are posted in the open period with a reference to the original entry.
- LED-8 When a sub-order reaches a terminal state without delivery (or `DELIVERY_FAILED`), every amount it still holds in 2100 is either refunded (JE-14) or recognised (JE-40), so INV-7 holds.

## 2. Money

- MON-1 Amounts are integers (`BIGINT`) in the platform minor unit of their currency (whole dinars for IQD). Floating-point money is prohibited in code, storage and APIs.
- MON-2 Every amount in an API, event or table is paired with a currency code (`IQD` at launch).
- MON-3 Proportional calculations (commission, coupon allocation across lines, partial refunds, loyalty allocation) are computed per order line, rounded half-up to an integer, and any remainder is distributed by the largest-remainder method so parts always sum exactly to the whole.
- MON-4 Price step: offer prices, shipping fees, COD fees and fixed-amount coupons must be multiples of `cfg:money.price_step` (default 250 IQD), the smallest practical cash unit.
- MON-5 Payable totals: percentage discounts and loyalty redemptions are adjusted so that each sub-order's amount payable is a multiple of the price step; the adjustment always favours the customer and is borne by whoever funds the discount. Rules MON-4 and MON-5 are the recommended resolution of D-12 and apply to all payment methods so that COD and prepaid totals are identical.
- MON-6 The rounding and allocation functions exist once, in the backend Money library, with property-based tests. Clients never compute money ([architecture](../06-platform/architecture.md) ARC-6).
- MON-7 Display: Western digits and the format `125,000 IQD` (English) / `125,000 د.ع` (Arabic) unless Design decides otherwise under D-19.
- MON-8 A currency table defines, per currency, the **platform exponent** (decimal places stored), the price step and the display format. IQD has exponent 0 and step 250 even though ISO 4217 lists three decimals, because fils are not used; libraries and providers that assume the ISO exponent must not be trusted for formatting or amounts (PAY-19). The table is published to clients through app configuration. This is what lets a later market use a two- or three-decimal currency without changing the Money library ([market-expansion](../01-product/market-expansion.md) §3).

## 3. Chart of accounts (indicative)

Sub-ledger dimensions are shown in brackets. Account numbers are placeholders for the accountant.

| Code | Account | Type | Dimensions |
|---|---|---|---|
| 1100 | PSP Clearing | Asset | PSP |
| 1110 | Collections Bank (COD) | Asset | bank account |
| 1120 | Courier COD Receivable | Asset | courier |
| 1130 | Operating Bank | Asset | bank account |
| 1140 | Seller Receivable (wallet deficits) | Asset | seller |
| 1150 | Courier Claims Receivable | Asset | courier |
| 1160 | Chargebacks Pending | Asset | PSP |
| 1200 | 1P Inventory | Asset | – |
| 2100 | Customer Funds Held (escrow liability) | Liability | sub-order |
| 2110 | Seller Payable (wallet available) | Liability | seller |
| 2120 | Customer Refund Payable | Liability | refund |
| 2130 | Courier Payable | Liability | courier |
| 2140 | Loyalty Points Liability | Liability | – |
| 2150 | Tax Payable | Liability | tax region |
| 2160 | Payouts in Transit | Liability | payout |
| 2170 | Supplier Payable (1P) | Liability | supplier |
| 2180 | Unallocated Receipts | Liability | PSP |
| 2190 | COD Remittance Suspense | Liability | courier |
| 4100 | Commission Revenue | Revenue | category |
| 4110 | Shipping Revenue | Revenue | – |
| 4120 | Advertising Revenue | Revenue | – |
| 4130 | COD Fee Revenue | Revenue | – |
| 4200 | 1P Sales Revenue | Revenue | category |
| 5100 | Promotion Expense (platform-funded discounts) | Expense | campaign |
| 5110 | Loyalty Expense | Expense | – |
| 5120 | Logistics Expense | Expense | courier |
| 5140 | Payment Processing Fees | Expense | PSP |
| 5150 | Losses and Write-offs | Expense | reason |
| 5200 | Cost of Goods Sold (1P) | Expense | category |

Seller wallet mapping: **Available** = balance of 2110 for the seller minus active holds; **Pending** = the seller's expected net share of 2100 for their unreleased sub-orders; **Awaiting courier remittance** = the part of Pending whose COD collection is not yet `RECONCILED` (cash still in 1120, or remitted to 1110 but not yet matched) ([commission-wallet-payouts](commission-wallet-payouts.md) §2).

## 4. Posting rules

"Item value" means the line price after seller-funded discounts. "Cash part" means what the customer actually paid for items. Platform-funded discount + loyalty redemption + cash part = item value.

### 4.1 Order funding

| ID | Event | Debit | Credit |
|---|---|---|---|
| JE-1 | Prepaid payment succeeded | 1100 PSP Clearing (amount paid) | 2100 Customer Funds Held |
| JE-2 | COD cash collected at delivery | 1120 Courier COD Receivable | 2100 Customer Funds Held |
| JE-3 | Platform-funded coupon applied (posted with JE-1 or JE-2) | 5100 Promotion Expense | 2100 Customer Funds Held |
| JE-4 | Loyalty points redeemed (posted with JE-1 or JE-2) | 2140 Loyalty Points Liability | 2100 Customer Funds Held |
| JE-5 | COD remittance received from courier | 1110 Collections Bank (amount received) | 1120 Courier COD Receivable (matched waybills); 2190 COD Remittance Suspense (any excess or unidentified amount, resolved by JE-31) |
| JE-6 | PSP settlement received | 1130 Operating Bank; 5140 Processing Fees | 1100 PSP Clearing |

After JE-1–JE-4, account 2100 for a sub-order equals item value + shipping fee + COD fee.

### 4.2 Delivery and release

| ID | Event | Debit | Credit |
|---|---|---|---|
| JE-7 | Delivered: shipping fee earned | 2100 (shipping fee) | 4110 Shipping Revenue |
| JE-8 | Delivered: COD fee earned | 2100 (COD fee) | 4130 COD Fee Revenue |
| JE-9 | Escrow released, 3P | 2100 (item value) | 2110 Seller Payable (item value − commission); 4100 Commission Revenue (commission) |
| JE-10 | Escrow released, 1P | 2100 (item value) | 4200 1P Sales Revenue |
| JE-11 | 1P cost of sale (with JE-10) | 5200 COGS | 1200 1P Inventory |
| JE-12 | Courier invoice or accrual per shipment | 5120 Logistics Expense | 2130 Courier Payable |
| JE-13 | Courier paid | 2130 Courier Payable | 1130 Operating Bank |

Commission is recognised at release (JE-9), when the hold has elapsed and the sale is no longer expected to reverse. v6 described commission as "accrued at confirmation, charged at release"; no accrual entry is posted before release. The accountant confirms the recognition point.

### 4.3 Refunds

| ID | Event | Debit | Credit |
|---|---|---|---|
| JE-14 | Refund approved **before** release (or for a sub-order never delivered) | 2100 (item value + refundable shipping fee + refundable COD fee still held) | 2120 Customer Refund Payable (cash part + refundable shipping fee + refundable COD fee); 5100 Promotion Expense (reversal of platform discount); 2140 Loyalty Liability (points restored) |
| JE-15 | Refund approved **after** release, 3P | 2110 Seller Payable (item value − commission); 4100 Commission Revenue (commission reversal) | 2120 Customer Refund Payable (cash part); 5100 Promotion Expense (reversal); 2140 Loyalty Liability (restored) |
| JE-16 | Refund approved after release, 1P | 4200 1P Sales Revenue | 2120; 5100; 2140 as above |
| JE-17 | Refund paid to customer | 2120 Customer Refund Payable | 1100 PSP Clearing or 1130 Operating Bank |
| JE-18 | Shipping or COD fee refunded after it was earned | 4110 Shipping Revenue or 4130 COD Fee Revenue | 2120 Customer Refund Payable |
| JE-19 | Shipping cost charged to the seller (seller-fault failed delivery, [logistics](../02-commerce/logistics.md) §7, or seller-paid return shipping, [returns-disputes](../02-commerce/returns-disputes.md) §3) | 2110 Seller Payable | 5120 Logistics Expense (recovery) |
| JE-20 | Return shipping deducted from customer refund | reduces the 2120 credit in JE-14/JE-15 | 5120 Logistics Expense (recovery) |
| JE-21 | Refund funded by Nyazek (goodwill, courier fault pending claim) | 5150 Losses and Write-offs | 2120 Customer Refund Payable |
| JE-40 | Prepaid sub-order reaches `DELIVERY_FAILED` with a shipping fee that is not refunded (ORD-9) | 2100 (retained shipping fee) | 4110 Shipping Revenue |
| JE-41 | Money received that matches no payable order (payment after the deadline, overpayment, duplicate success; PAY-8–PAY-10) | 1100 PSP Clearing | 2180 Unallocated Receipts |
| JE-42 | Refund of an unallocated receipt approved (PAY-20) | 2180 Unallocated Receipts | 2120 Customer Refund Payable |
| JE-46 | Refund transfer returned after success | 1130 Operating Bank or 1100 PSP Clearing | 2120 Customer Refund Payable |

Partial refunds use the same entries with proportional amounts per MON-3. If JE-15 makes 2110 negative, the deficit is handled per [commission-wallet-payouts](commission-wallet-payouts.md) §5.

### 4.4 Payouts, ads, loyalty, other

| ID | Event | Debit | Credit |
|---|---|---|---|
| JE-22 | Payout instructed | 2110 Seller Payable | 2160 Payouts in Transit |
| JE-23 | Payout confirmed | 2160 Payouts in Transit | 1130 Operating Bank or 1100 PSP Clearing |
| JE-24 | Payout failed | 2160 Payouts in Transit | 2110 Seller Payable |
| JE-45 | Payout returned by the bank after it was executed | 1130 Operating Bank or 1100 PSP Clearing | 2110 Seller Payable |
| JE-47 | Every bank, wallet or PSP fee charged to Nyazek on a refund or payout | 5140 Payment Processing Fees | 1130 Operating Bank or 1100 PSP Clearing |
| JE-48 | Payout transfer fee recovered from the seller when PO-9 makes the seller bear it (posted with JE-47) | 2110 Seller Payable | 5140 Payment Processing Fees (recovery) |
| JE-49 | Seller receivable written off (dual control, after the recovery terms of WAL-10 are exhausted) | 5150 Losses and Write-offs | 1140 Seller Receivable |
| JE-25 | Ad spend billed (validated clicks) | 2110 Seller Payable | 4120 Advertising Revenue |
| JE-26 | Invalid-click credit | 4120 Advertising Revenue | 2110 Seller Payable |
| JE-27 | Loyalty points earned | 5110 Loyalty Expense | 2140 Loyalty Points Liability |
| JE-28 | Loyalty points expired or reversed | 2140 Loyalty Points Liability | 5110 Loyalty Expense |
| JE-29 | Seller referral bonus | 5100 Promotion Expense | 2110 Seller Payable |
| JE-30 | Chargeback lost or accepted ([payments](payments.md) §8; JE-30a and JE-30b are the receipt and win entries there). Seller liable: posted like a refund, from 2100 for the unreleased part (as JE-14) and, for the released part, 2110 net of commission with 4100 commission and 4110/4130 fee reversals (as JE-15, JE-18). Platform liable (CBK-2): 5150 | 2100, or 2110 + 4100 + 4110/4130, or 5150, as stated | 1160 Chargebacks Pending |
| JE-31 | Manual adjustment (dual control) | per approved request | per approved request |
| JE-32 | COD shortfall written off or claimed from courier | 5150 Losses (or 2130 Courier Payable offset) | 1120 Courier COD Receivable |
| JE-33 | Wallet deficit reclassified at period end | 1140 Seller Receivable | 2110 Seller Payable |

Failed delivery (RTO) of a COD order posts no funding entry (no cash was collected); logistics cost follows JE-12 and cost attribution follows [logistics](../02-commerce/logistics.md) §7.

**Accountant decisions flagged:** treatment of loyalty points for 1P sales as deferred revenue rather than expense; gross or net presentation of shipping; timing of promotion expense.

### 4.5 1P inventory and courier claims

| ID | Event | Debit | Credit |
|---|---|---|---|
| JE-34 | 1P goods receipt ([first-party-operations](../03-sellers/first-party-operations.md) FP-5) | 1200 1P Inventory (quantity × unit cost) | 2170 Supplier Payable |
| JE-35 | Supplier paid | 2170 Supplier Payable | 1130 Operating Bank |
| JE-36 | 1P stock decrease (damaged, expired, lost, count correction); reversed for an increase | 5150 Losses and Write-offs (or 2170 where the supplier credits a return) | 1200 1P Inventory |
| JE-37 | 1P return restocked as resellable (posted with the refund entry JE-16) | 1200 1P Inventory (original cost) | 5200 COGS |
| JE-38 | 3P parcel lost or destroyed by the courier: seller compensated at the value set by the courier contract | 1150 Courier Claims Receivable (5150 for any part Nyazek bears) | 2110 Seller Payable |
| JE-39 | Courier claim settled (paid, or offset against the courier's invoice) | 1130 Operating Bank or 2130 Courier Payable | 1150 Courier Claims Receivable |
| JE-43 | 1P parcel lost or destroyed in transit (goods were still in 1P Inventory, since JE-11 posts only at release) | 5150 Losses and Write-offs | 1200 1P Inventory (cost) |
| JE-44 | Courier claim recognised for a loss Nyazek bore (1P lost parcel, JE-21 goodwill refund for courier damage, return parcel lost) | 1150 Courier Claims Receivable | 5150 Losses and Write-offs (recovery) |

The customer's refund for a lost prepaid parcel is JE-14; a lost COD parcel collected no cash and needs no refund. The costing method behind JE-11, JE-36 and JE-37 is decision D-42. 1P goods stay in 1200 until release (JE-11) or loss (JE-43); the accountant confirms this timing with D-42.

Tax: the tax rate is 0% at launch ([tax-invoicing](tax-invoicing.md)). When a non-zero rate applies, tax on 1P sales is credited to 2150 at release; tax on 3P sales follows the seller-of-record model and D-26, and needs new posting rules approved by the accountant before any rate other than 0% is enabled.

### 4.6 Treasury requirement

Seller payables can exceed customer cash held by the PSP because Nyazek funds platform coupons, loyalty redemptions and free shipping from its own money, and because COD cash arrives in a different account. A daily **funding position report** compares cash by location (1100, 1110, 1130) with liabilities by due date (2110, 2120, 2130, 2160, 2180). Finance tops up the payout account before each payout run; a payout run does not start if funds are insufficient.

## 5. Data model (logical)

- `account(id, code, name, type, normal_side, allows_negative)`
- `journal_entry(id, entry_type, idempotency_key UNIQUE, occurred_at, posted_at, reverses_entry_id, order_id, sub_order_id, reference_type, reference_id, created_by)`
- `journal_line(id, entry_id, account_id, side, amount > 0, currency, seller_id, courier_id, psp_id, …)`
- `account_balance(account_id, dimension_key, balance, updated_entry_id)` maintained in the same transaction as the lines.

Invariants enforced in the database:

- INV-1 For every entry, total debits = total credits (deferred constraint trigger at commit).
- INV-2 `amount > 0`; a line has exactly one side.
- INV-3 Accounts with `allows_negative = false` (2100 per sub-order, 2120, 2160, 2180, 2190, 1120 per courier) can never go below zero.
- INV-4 Journal tables are insert-only for the application role.

Invariants verified by jobs:

- INV-5 Trial balance nets to zero (every 5 minutes on balances; full recomputation from lines daily).
- INV-6 `account_balance` equals the sum of its lines (daily full check; sampled continuously).
- INV-7 For every sub-order in a terminal state, 2100 for that sub-order is zero.
- INV-8 Sum of seller-visible wallet figures equals the corresponding ledger balances.

Any invariant failure is a Severity 1 alert and suspends payout runs until cleared. INV-7 is checked when a sub-order becomes terminal and again daily; LED-8 guarantees it for every non-delivered terminal state.

## 6. Reconciliation

| Reconciliation | Inputs | Frequency | Match key | Exceptions |
|---|---|---|---|---|
| PSP payments | PSP webhooks, PSP settlement file or API, journal JE-1/JE-6 | Daily per PSP | PSP transaction reference | Paid at PSP but no order; order paid but missing at PSP; amount mismatch; fee mismatch |
| COD remittance | Courier delivery manifest, remittance statement, bank statement, journal JE-2/JE-5 | Per remittance and daily | Waybill number | Short or over remittance; delivered but not remitted beyond SLA; remitted but not marked delivered |
| Refunds | Refund requests, PSP refund confirmations or manual transfer references, journal JE-14–JE-17 | Daily | Refund ID | Refund stuck; refund paid twice; destination rejected |
| Payouts | Payout instructions, bank or PSP confirmations, journal JE-22–JE-24 | Per payout run | Payout ID | Failed or returned transfer |
| Courier invoices | Shipments, courier invoice lines, journal JE-12 | Per invoice | Waybill number | Charge for unknown shipment; weight dispute |

Rules:

- REC-1 Any mismatch, of any amount, opens an exception case assigned to Finance (COD cases jointly with Logistics) and raises an alert. There is no tolerance threshold at launch; no screen may offer one.
- REC-2 A payment confirmed by webhook but absent from the settlement file, or the reverse, is flagged within 24 hours.
- REC-3 Exception cases have states `OPEN → INVESTIGATING → RESOLVED` with a mandatory resolution note and, where money moves, a dual-control adjustment (JE-31).
- REC-4 The daily reconciliation summary is stored and visible to Finance and Compliance roles.
- REC-5 After a regional failover or restore, a full reconciliation against every PSP and courier runs before payouts resume, to recover transactions inside the recovery-point window ([reliability-sre](../06-platform/reliability-sre.md) §4).
- REC-6 Finance signs off the previous business day's PSP and COD reconciliation summary. Signing off records the exceptions still open, which stay assigned. A payout run cannot be approved while that sign-off is missing; open exception cases do not block the run unless they concern a seller in the run, whose payout is then held for the disputed amount.

## 7. Acceptance criteria

- Property-based tests: for random orders with mixed discounts, partial cancellations and partial refunds, all ledger invariants hold and 2100 returns to zero at terminal state.
- Posting the same business event twice creates one journal entry.
- The application database role cannot update or delete journal rows (integration test).
- A scripted month of synthetic PSP, COD and payout files reconciles with zero unexplained differences (Phase 4 launch gate).
