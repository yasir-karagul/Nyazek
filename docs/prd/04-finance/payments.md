# Payments

**Authoritative for:** payment methods, funds-custody model, payment and COD-collection state machines, PSP integration rules, refunds execution, chargebacks, card-data scope.
**Related:** [ledger-reconciliation](ledger-reconciliation.md) · [checkout-orders](../02-commerce/checkout-orders.md) · [fraud-risk](../05-trust/fraud-risk.md) · [returns-disputes](../02-commerce/returns-disputes.md) · [logistics](../02-commerce/logistics.md)

---

## 1. Methods

All transactions are in the market's currency: IQD in Iraq, the only market at launch ([market-expansion](../01-product/market-expansion.md)). There is no customer wallet or stored balance. Payment methods are enabled per market.

| Method | Priority | Type |
|---|---|---|
| Cash on Delivery (COD) | P0 | Cash collected by courier; subject to the COD risk engine ([fraud-risk](../05-trust/fraud-risk.md) §4) |
| Zain Cash | P0 | Mobile wallet, redirect or app hand-off |
| Asia Hawala | P0 | Mobile wallet / transfer |
| FastPay | P0 | Digital wallet |
| Visa / Mastercard | P1 | PSP-hosted payment page only |
| Qi Card, First Iraqi Bank (FIB), Nass Wallet | P1, subject to D-11 | Direct or through an aggregator |

D-11: evaluate a Central Bank-licensed aggregator that exposes several of these methods behind one integration. If selected, the aggregator replaces individual adapters and the P0 list is delivered through it. Each wallet integration is an external dependency with its own onboarding lead time ([release-plan](../00-governance/release-plan.md) §5).

Excluded from v1.0: eDinar, customer wallet, instalments, buy-now-pay-later.

## 2. Funds custody (D-09, decided)

v6 stated as fact that a licensed PSP holds customer funds in segregated accounts and releases them on Nyazek's instruction. **This is an unverified assumption.** Many PSPs simply settle to the merchant's bank account on a fixed cycle and offer no marketplace escrow or split settlement; COD cash never touches a PSP at all.

| Model | Description | Consequence |
|---|---|---|
| A. PSP-held escrow | PSP holds funds per order and pays sellers on instruction | Matches v6; requires a PSP that offers it |
| B. Segregated client account | PSP settles to a Nyazek bank account that is segregated from operating funds and used only for seller and refund payments | Likely practical default; counsel must confirm whether a licence or other authorisation is required |
| C. Commingled operating account | Not acceptable | – |

Decision (D-09): model A where the contracted PSP offers it, otherwise model B; model C is never used. Counsel and the PSP confirm the model in use, and any authorisation it needs, before launch ([release-plan](../00-governance/release-plan.md) §4, gate 5).

Requirements independent of the model:

- PAY-1 The internal ledger tracks every dinar owed to customers and sellers ([ledger-reconciliation](ledger-reconciliation.md) LED-3).
- PAY-2 Customer and seller funds are never used for Nyazek's operating expenses.
- PAY-3 Public wording ("escrow", "customer protection") is approved by counsel once the custody model in use is confirmed (D-09). Until then, product copy says "Nyazek holds your payment until delivery is confirmed".
- PAY-4 Float income (v6 §5.4) is not assumed in any plan.

## 3. Entities

| Entity | Scope | Purpose |
|---|---|---|
| `PaymentIntent` | One per prepaid order attempt | Tracks one attempt to pay an order with one method |
| `PaymentAllocation` | Per sub-order within a succeeded intent | Splits the paid amount across sub-orders for refunds and release |
| `CodCollection` | One per shipment of a COD sub-order | Cash expected, collected and remitted. A multi-seller COD order has several collections because parcels are delivered separately |
| `Refund` | Per sub-order, referencing lines | One movement of money back to a customer |
| `Chargeback` | Per card payment | Card dispute raised through the PSP |

v6 modelled COD as a single order-level payment; that cannot represent parcels delivered on different days by different couriers.

## 4. State machines

### 4.1 PaymentIntent (prepaid)

| State | Entered when | Next |
|---|---|---|
| `CREATED` | Customer places a prepaid order | `PENDING`, `CANCELLED`, `EXPIRED` |
| `PENDING` | Customer redirected to PSP or wallet app | `SUCCEEDED`, `FAILED`, `EXPIRED` |
| `SUCCEEDED` | Verified webhook or status query confirms full amount | terminal for the intent; refunds are separate |
| `FAILED` | PSP reports failure or decline | terminal; customer may retry with a new intent until the order's payment deadline (PAY-18) |
| `EXPIRED` | No confirmation within `cfg:payments.intent_ttl_minutes` (default 30) or by the order's payment deadline, whichever is earlier | `SUCCEEDED` only for a confirmation that arrives before the order's payment deadline (PAY-9); otherwise terminal, and a later confirmation is handled by PAY-9 |
| `CANCELLED` | Customer abandons before redirect | terminal |

### 4.2 CodCollection

| State | Entered when | Next |
|---|---|---|
| `EXPECTED` | COD sub-order is placed (saga step 5a) | `COLLECTED`, `NOT_COLLECTED` (failed, refused or `LOST`), `VOID` |
| `COLLECTED` | Courier reports delivery with cash collected (JE-2) | `REMITTED`, `EXCEPTION` (not remitted within the courier's remittance SLA, [logistics](../02-commerce/logistics.md) §8) |
| `REMITTED` | Remittance containing this waybill is received (JE-5) | `RECONCILED`, `EXCEPTION` |
| `RECONCILED` | Amount matches per waybill | terminal |
| `EXCEPTION` | Amount differs, cash is missing, or remittance is overdue | `RECONCILED` (difference resolved), `WRITTEN_OFF` |
| `WRITTEN_OFF` | Shortfall written off or claimed from the courier under dual control (JE-32) | terminal |
| `NOT_COLLECTED` | Delivery failed or refused, or the parcel was lost before delivery | terminal |
| `VOID` | Sub-order cancelled before shipping | terminal |

A COD sub-order whose collection is `WRITTEN_OFF` is still released to the seller (the customer paid; the loss is Nyazek's or the courier's).

### 4.3 Refund

| State | Entered when | Next |
|---|---|---|
| `REQUESTED` | Created by Orders, Returns & Disputes, or Payments itself (PAY-8, PAY-9, PAY-10) | `AWAITING_DESTINATION`, `PROCESSING`, `CANCELLED` |
| `AWAITING_DESTINATION` | COD refund and the customer has no verified refund account, or the destination was rejected | `PROCESSING` (account verified), `MANUAL_REVIEW` (no account after `cfg:refunds.destination_wait_days` (default 14)) |
| `PROCESSING` | Sent to the PSP API or placed in the manual disbursement queue (PAY-14) | `SUCCEEDED`, `FAILED` |
| `SUCCEEDED` | Provider confirmation or external reference recorded (JE-17) | `RETURNED` |
| `FAILED` | Provider error or rejection | `PROCESSING` (automatic retry, at most `cfg:refunds.max_retries` (default 3)), `MANUAL_REVIEW` |
| `MANUAL_REVIEW` | Finance must act | `PROCESSING`, `AWAITING_DESTINATION`, `CANCELLED` |
| `RETURNED` | The transfer bounced after success (JE-46) | `AWAITING_DESTINATION`, `PROCESSING` |
| `CANCELLED` | Created in error and never paid; dual control; reverses its approval entry | terminal |

- PAY-20 Refunds originated by Payments (overpayment, payment after the deadline, duplicate success) have no order lines: they refund the received amount from Unallocated Receipts (JE-41, JE-42) and never touch the order's escrow.
- PAY-21 Each state change notifies the customer where it affects them (refund sent, destination needed, destination rejected, refund failed and under review) ([notifications-messaging](../02-commerce/notifications-messaging.md)).

## 5. Integration rules (every PSP adapter)

- PAY-5 Payment creation is idempotent: one idempotency key per intent.
- PAY-6 State changes come only from verified webhooks (signature, timestamp tolerance, replay protection; for edge-buffered webhooks as API-11 states) or from a server-to-server status query. The browser return page only displays status and polls ([api-standards](../06-platform/api-standards.md) API-13).
- PAY-7 Pending intents are polled every minute until terminal; the nightly reconciliation is the final safety net.
- PAY-8 The confirmed amount must equal the intent amount exactly. An underpayment or overpayment marks the intent `FAILED`, posts the received amount to Unallocated Receipts (JE-41), refunds it automatically (PAY-20) and raises an alert.
- PAY-9 **Late success.** A confirmation that arrives after an intent expired but **before** the order's payment deadline is treated as a normal success. A confirmation for an order that has no payable sub-order left (all cancelled) is handled in the same way. A confirmation that arrives **after** the deadline never revives the order (its sub-orders are terminal `CANCELLED`): the amount is posted to Unallocated Receipts (JE-41) and refunded automatically (PAY-20), and the customer is told the order expired and offered "restore to cart" (CRT-7). Money is never kept without an order.
- PAY-10 **Duplicate success** (two intents succeed for one order): the second is posted to Unallocated Receipts (JE-41) and refunded automatically (PAY-20).
- PAY-11 Each adapter declares a capability matrix: redirect or in-app, webhook support, status query, full refund API, partial refund API, payout API, settlement file format, sandbox availability. Missing capabilities select the documented fallback (PAY-14, PAY-17).
- PAY-12 A circuit breaker hides a method at checkout when its error rate or latency exceeds `cfg:payments.circuit_error_rate` (default 30% over 5 minutes); Finance and on-call are alerted; the method returns after successful health probes.
- PAY-13 Requests and responses are logged with secrets and personal data redacted. Sandbox contract tests for each adapter run in CI and nightly against the provider sandbox where one exists.
- PAY-18 While an order is `AWAITING_PAYMENT` the customer may retry with the same or another **prepaid** method. Switching to cash on delivery is not a retry: the customer places a new order, which passes COD eligibility and confirmation like any other.
- PAY-19 Adapters convert between the platform's integer amounts and the unit each provider expects (for example a provider that expresses IQD in fils); the conversion is covered by adapter tests (MON-8).

## 6. Refund execution

| Original method | Refund route | Notes |
|---|---|---|
| Wallet or card with refund API | Original method through the PSP | Default |
| Wallet without refund API, or refund API failure | PAY-14 manual disbursement | |
| COD | Customer's verified refund account (mobile wallet or bank), D-02 | Customer adds the account once; ownership is confirmed by OTP to the customer's verified phone (in an order-lookup session, GST-4, to the order's phone) |

- PAY-14 **Manual disbursement queue.** Refunds that cannot be executed by API appear in the Finance refund queue with the destination details. Finance executes the transfer, records the external reference, and a second Finance user confirms above `cfg:refunds.dual_control_threshold` (default 250,000 IQD). The refund becomes `SUCCEEDED` only with a reference.
- PAY-15 Refund SLA: executed within `cfg:refunds.execution_sla_days` (default 3 business days) of approval; overdue refunds alert Finance.
- PAY-16 A refund can never exceed the amount paid for the affected lines minus earlier refunds; enforced in the database.
- PAY-17 COD refund accounts: maximum `cfg:refunds.max_refund_accounts` (default 2) per customer; a refund account used by more than one customer account is a risk signal ([fraud-risk](../05-trust/fraud-risk.md)).

## 7. COD specifics

- Cash flow: courier collects → remits to the collections account within the courier's remittance SLA → per-waybill reconciliation → funds become eligible for release.
- A seller is never paid from COD cash that has not been remitted and reconciled ([commission-wallet-payouts](commission-wallet-payouts.md) WAL-3).
- Amount collected must equal the amount payable. Partial acceptance at the door is not supported at launch: the customer accepts or refuses the whole parcel.
- Courier controls (exposure caps, ageing, penalties) are in [logistics](../02-commerce/logistics.md) §8.
- Optional COD handling fee: `cfg:cod.fee` (default 0 IQD), shown as its own line, Nyazek revenue, never seller revenue (P1).

## 8. Chargebacks (cards, P1)

| State | Entered when | Next | Ledger |
|---|---|---|---|
| `RECEIVED` | PSP notifies a chargeback; the PSP withholds the amount | `EVIDENCE_SUBMITTED`, `ACCEPTED` | JE-30a: Dr 1160 Chargebacks Pending, Cr 1100 PSP Clearing |
| `EVIDENCE_SUBMITTED` | Finance submits proof of delivery and order evidence before the PSP deadline | `WON`, `LOST` | – |
| `ACCEPTED` | Finance decides not to contest | terminal | JE-30 |
| `WON` | PSP returns the amount | terminal | JE-30b: Dr 1100, Cr 1160 |
| `LOST` | PSP keeps the amount | terminal | JE-30 |

- CBK-1 `RECEIVED` opens a Finance case. It blocks release of the sub-order's unreleased value (as WAL-4 does for a dispute) and places a hold on Available for any part already released ([commission-wallet-payouts](commission-wallet-payouts.md) §4). Both are lifted at `WON`. At `ACCEPTED` or `LOST` the amount is posted per JE-30.
- CBK-2 Liability at `ACCEPTED` or `LOST`: the seller bears it when the proof of delivery is missing or the seller was at fault; Nyazek bears it (5150) when delivery is proven, including card fraud on a payment the platform accepted.
- Chargeback ratio per method is a monitored metric.

## 9. Card data scope

- Nyazek systems never store, process or transmit card numbers. Card entry happens only on a page hosted by a PCI-DSS Level 1 certified PSP (redirect preferred).
- Nyazek completes the applicable self-assessment questionnaire annually (SAQ A where eligibility is met under the PCI-DSS version in force).
- "Saved cards" (P1) stores PSP tokens only.

## 10. Operational fallbacks required at launch

| Capability | Automated path | P0 fallback |
|---|---|---|
| Refunds | PSP refund API | Manual disbursement queue (PAY-14) |
| Seller payouts | PSP or bank payout API | Bank transfer file generated per payout run, executed by Finance under dual control |
| Settlement reconciliation | Settlement file or API | Manual upload of statement in CSV |
| COD remittance | Courier API or statement file | Manual CSV upload by Logistics |

## 11. Monitoring

Payment success rate per method, median time to confirmation, pending-intent age, webhook failure rate, refund ageing, duplicate and late successes, circuit-breaker state, chargeback ratio. Alert thresholds are in [reliability-sre](../06-platform/reliability-sre.md) §3.

## 12. Acceptance criteria

- Replayed, out-of-order and forged webhooks do not change state incorrectly (adapter test suite per PSP).
- A payment that succeeds after expiry results in either a valid order or an automatic full refund.
- A refund larger than the refundable remainder is rejected by the database.
- With the PSP sandbox offline, COD checkout continues to work and the affected method disappears from checkout within the circuit-breaker window.
