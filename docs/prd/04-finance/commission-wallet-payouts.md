# Commission, Seller Wallet & Payouts

**Authoritative for:** commission rules, escrow hold and release, seller wallet balances and holds, negative balances, payout cycles, methods and statements.
**Related:** [ledger-reconciliation](ledger-reconciliation.md) · [payments](payments.md) · [returns-disputes](../02-commerce/returns-disputes.md) · [seller-dashboard](../03-sellers/seller-dashboard.md) · [business-model](../01-product/business-model.md)

---

## 1. Commission

### 1.1 Schedule

- COM-1 Commission applies to 3P sub-orders only. 1P sales carry no commission.
- COM-2 Rates are defined at three levels; the most specific rule wins: product type → sub-category → top-level category.
- COM-3 The schedule is a versioned table with effective dates, edited by the Finance Manager under dual control and published on the seller fees page. An increase takes effect no earlier than `cfg:commission.notice_days` (default 30) after publication and sellers are notified; decreases may take effect at once. There are no seller-specific rates at launch.
- COM-4 The approved schedule is an owner decision (D-20). v6's example rates (4%–12%) cannot produce the stated 12%–18% blended take rate; the two must be reconciled before launch.
- COM-5 The rate that applies is frozen on each order line at order placement. Later schedule changes affect only new orders.

### 1.2 Base and calculation

| Case | Commission base |
|---|---|
| No discount | Line item price × quantity |
| Seller-funded coupon or deal | Discounted line value |
| Platform-funded coupon or loyalty redemption | Pre-discount line value (the seller is not penalised for a discount Nyazek funds). Recommended default for D-10 |
| Shipping fee, COD fee, tax | Never included |

Commission per line = base × rate, rounded per MON-3 ([ledger-reconciliation](ledger-reconciliation.md)).

### 1.3 Lifecycle

| Event | Effect |
|---|---|
| Order placed | Rate and expected commission stored on the line (no ledger entry) |
| Escrow released | Commission charged: posting JE-9 |
| Cancelled, rejected, auto-cancelled, delivery failed, lost | No commission |
| Full refund after release | Commission fully reversed (JE-15) |
| Partial refund after release | Commission reversed in proportion to the refunded item value |
| Dispute resolved for customer | Same as refund, referencing the dispute |
| Dispute resolved for seller | Commission retained |

## 2. Wallet balances

The wallet is a set of views over ledger accounts ([ledger-reconciliation](ledger-reconciliation.md) LED-5).

| Balance | Definition | Payable |
|---|---|---|
| Pending | Expected net proceeds (item value − expected commission) of sub-orders that are paid or COD-delivered but not yet released | No |
| ↳ Awaiting courier remittance | Subset of Pending: COD delivered, cash not yet remitted and reconciled | No |
| Available | Seller Payable balance minus active holds | Yes |
| On hold | Sum of active holds | No |

Every wallet movement shown to the seller references its origin: sub-order, return, dispute, payout, ad invoice or adjustment. Movement types (also the filter values): sale release, commission, refund, shipping charge, payout, payout returned, transfer fee, adjustment, chargeback, ad spend, ad credit, referral bonus, courier compensation. Holds are shown separately from movements because they post no entries.

## 3. Escrow hold and release

- WAL-1 The hold starts at proof of delivery.
- WAL-2 Hold length = `cfg:escrow.hold_days` (default 7), or the line's effective return window (the category window, or the seller's longer store window, RET-6) if longer when `cfg:escrow.hold_follows_return_window` (default true) is set. This is the recommended resolution of the D-03 timing question and removes most post-release recoveries.
- WAL-3 Release conditions, all required: sub-order `DELIVERED`; hold elapsed; for COD, the collection is `RECONCILED` or `WRITTEN_OFF`. Releases continue while a seller is suspended; the suspension hold (§4) keeps the released amount from being paid out.
- WAL-4 An open return or dispute blocks release only for the affected lines' value (the units in the return or dispute). The rest of the sub-order is released on schedule as a **partial release**; the blocked value is released later, or refunded, when the return or dispute ends. Each release has its own sequence number and idempotency key (`escrow-release:<subOrderId>:<releaseSeq>`, LED-4) and records the amounts per line.
- WAL-5 Each release posts JE-9 (or JE-10 and JE-11 for 1P) and emits `escrow.released`. The sub-order moves to `COMPLETED` only when every non-cancelled unit is settled, that is released or refunded, and no return or dispute on it is open.
- WAL-6 Early release when the customer confirms receipt is **not** enabled at launch (D-22). Customer confirmation is recorded as evidence only. v6 implied early release; it adds refund-recovery risk for no seller benefit while payouts are periodic.

## 4. Holds

| Hold | Trigger | Amount | Released when |
|---|---|---|---|
| Chargeback | Card dispute opened on released lines (unreleased value is blocked from release instead, CBK-1) | Released part of the disputed value | Chargeback resolved |
| Reconciliation exception | Open REC-6 exception concerning the seller | Disputed amount | Exception resolved |
| Return after release | Return approved on released lines | Refund value | Refund posted (JE-15) or return closed without refund |
| Dispute after release | Dispute opened on released lines | Disputed value | Dispute closed (after any review, DSP-4) |
| Risk | Risk case on the seller | Set by Fraud/Risk Manager (dual control above threshold) | Case closed |
| Payout-destination change | New destination verified | First payout only | 72 hours after verification |
| Suspension | Seller status `SUSPENDED` (including a temporary fraud freeze, SEL-3) | Entire Available balance | Suspension lifted or account closed and settled |

Holds reduce Available, are visible to the seller with a reason, and never post ledger entries by themselves.

## 5. Negative balance

- WAL-7 A refund, chargeback or adjustment after release may make Seller Payable negative.
- WAL-8 A deficit is recovered automatically from subsequent releases before any payout.
- WAL-9 While in deficit, ad campaigns pause.
- WAL-10 If a deficit persists for `cfg:wallet.deficit_grace_cycles` (default 2) payout cycles, the seller becomes `RESTRICTED` (no new offers) and the case goes to the Seller Manager; recovery terms follow the Seller Agreement. A deficit that cannot be recovered is written off under dual control (JE-49).
- WAL-11 Deficits are reported as Seller Receivable at period end (JE-33).

## 6. Payouts

### 6.1 Cycle

- PO-1 Default cycle: monthly, cut-off at 23:59 market time on the last calendar day (v6). Recommended under D-03: weekly for sellers in good standing (P1), monthly retained for new sellers during their first 30 days and for sellers at performance Level 2 or worse. The cycle is a per-seller setting controlled by Finance: `cfg:payout.default_cycle` (default MONTHLY).
- PO-2 A payout includes the Available balance at the cut-off time, if at least `cfg:payout.min_amount` (default 25,000 IQD). Smaller balances roll over without expiry.
- PO-3 Payout runs require Finance approval under dual control and a sufficient funding position ([ledger-reconciliation](ledger-reconciliation.md) §4.6).

### 6.2 Methods

| Method | Priority | Notes |
|---|---|---|
| Bank transfer (Iraqi banks) | P0 | File-based fallback always available |
| Zain Cash, Asia Hawala, FastPay | P0 where the provider supports payouts, otherwise P1 | Per PSP capability matrix |
| Cash pickup at partner locations | P1, subject to D-30 | Requires a contracted partner network and identity check at pickup |

- PO-4 The destination must belong to the verified KYC identity (account-holder name match).
- PO-5 Adding or changing a destination requires re-authentication with 2FA, verification of the destination, notification to the previous contact details, and a 72-hour hold on the first payout to it.
- PO-6 Payout states:

| State | Entered when | Next | Ledger |
|---|---|---|---|
| `CREATED` | Payout run computed at cut-off | `APPROVED`, `REJECTED` | – |
| `APPROVED` | Second Finance approver approves the run (PO-3) | `INSTRUCTED` | – |
| `REJECTED` | An approver removes the payout from the run, with reason | terminal; the amount stays Available for the next run | – |
| `INSTRUCTED` | Sent to the bank or provider (API or file) | `EXECUTED`, `FAILED` | JE-22 |
| `EXECUTED` | Provider confirms, or Finance records the bank reference | `RETURNED` | JE-23 |
| `FAILED` | Provider rejects | `RETRY_SCHEDULED` | JE-24 |
| `RETRY_SCHEDULED` | Waiting for the next run after the seller confirms the destination | `CREATED` (in the next run) | – |
| `RETURNED` | Funds come back after execution | `RETRY_SCHEDULED` | JE-45 |

A failed or returned payout notifies seller and Finance.

- PO-11 Payout run states: `DRAFT` (computed) → `PENDING_APPROVAL` → `APPROVED` → `EXECUTING` → `COMPLETED`, or `COMPLETED_WITH_FAILURES` when any payout failed; `DRAFT` or `PENDING_APPROVAL` → `CANCELLED`. A run cannot be approved while REC-6 sign-off is missing or the funding position is insufficient.

### 6.3 Statements

- PO-7 Each payout produces a statement (PDF and CSV): opening balance, releases by sub-order, commission, refunds, shipping charged to the seller, courier compensation, ad spend and ad credits, referral bonuses, chargebacks, adjustments, payouts returned, transfer fee (when the seller bears it), holds placed and released, payout amount, closing balance.
- PO-8 A commission invoice is issued per settlement period ([tax-invoicing](../04-finance/tax-invoicing.md) §3).
- PO-9 Transfer fees charged by the bank or wallet for a payout are borne according to `cfg:payout.transfer_fee_bearer` (default NYAZEK) (D-43). When the seller bears them, the fee is a separate, labelled line on the statement, never a silent reduction.
- PO-10 The final payout of a `CLOSING` account ignores the minimum payout amount. A balance that cannot be paid because the destination is invalid and the seller does not respond is kept as a liability and handled as counsel directs for unclaimed funds.

## 7. Other wallet rules

- A suspended seller's balance is frozen; open obligations (refunds, chargebacks) are still settled from it.
- On account closure, final settlement happens after the last return window and any open dispute have closed.
- Ad spend is debited only from Available; campaigns pause when Available is insufficient ([advertising](../02-commerce/advertising.md)).
- Manual adjustments (credit or debit) require a reason, an attachment where relevant, and dual control; they appear in the seller's history as "adjustment" with the reason.

## 8. Acceptance criteria

- For any sequence of release, partial refund, chargeback and payout, the wallet figures shown to the seller equal the ledger balances.
- A COD sub-order is never released before its collection is `RECONCILED` or `WRITTEN_OFF`.
- A payout cannot be instructed for more than Available, to an unverified destination, or without two distinct approvers.
- Changing the commission schedule does not alter the commission on existing orders.
