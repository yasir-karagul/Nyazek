# Returns, Refunds & Disputes

**Authoritative for:** return eligibility and windows, return shipping cost, return and dispute state machines, refund amounts and timing, customer-abuse controls, the money-back guarantee.
**Related:** [checkout-orders](checkout-orders.md) · [payments](../04-finance/payments.md) §6 · [commission-wallet-payouts](../04-finance/commission-wallet-payouts.md) · [logistics](logistics.md) §9 · [fraud-risk](../05-trust/fraud-risk.md)

---

## 1. How the pieces fit

| Mechanism | Used when | Decided by |
|---|---|---|
| Cancellation | Before the parcel is shipped | Automatic ([checkout-orders](checkout-orders.md) §8) |
| Return | Customer received the item and wants to send it back, or received it damaged, wrong or not as described | Seller (Nyazek for 1P), with automatic approval on silence |
| Dispute | Escalation: non-delivery despite a "delivered" status; seller rejected a return or the inspection; customer rejects a partial-refund proposal; refund not received | Nyazek admin, binding on the platform |

**Money-back guarantee:** a customer who does not receive the order, or receives an item that is damaged, wrong, defective or not as described, gets a full refund of the affected items, plus the original shipping and COD fees when the whole sub-order is affected (§5). They never pay return shipping for such an item (§3).

## 2. Eligibility and windows

- RET-1 The return window is set per category: `cfg:returns.default_window_days` (default 7) unless the category overrides it. It starts at proof of delivery.
- RET-2 Returns are requested per line and quantity; a customer may return some items of a sub-order.

| Reason | Eligible | Evidence |
|---|---|---|
| Defective, damaged, wrong item, not as described, expired | Always within the window, for every category | Photo or video required |
| Change of mind | Only for categories flagged "change-of-mind returnable"; item unused and in original packaging | Photo required above `cfg:returns.proof_value_threshold` (default 100,000 IQD) |

Non-returnable for change of mind: opened hygiene and personal-care items, intimate wear, perishable food, customised items, medicines. These remain returnable when damaged, wrong, expired or not as described.

The per-category windows and flags are owner-configurable; the proposed defaults are ratified under D-36.

- RET-9 **Seller store policy.** A 3P seller may improve, never reduce, the category policy in two ways (page `SL-SET-POLICY`): a longer return window, up to `cfg:returns.max_seller_window_days` (default 30); and free change-of-mind return shipping, in categories that allow change-of-mind returns. The values in force at order placement are stored on each line with the category policy (RET-6) and drive the escrow hold (WAL-2). 1P follows the category policy.

## 3. Return shipping cost (recommended default, D-05)

| Reason | 3P order | 1P order |
|---|---|---|
| Defective, damaged in seller packing, wrong item, not as described, expired | Seller pays (wallet debit) | Nyazek pays |
| Damaged in transit, courier at fault | Courier, per claim; Nyazek fronts the cost | Courier, per claim |
| Change of mind | Customer pays the change-of-mind return fee, deducted from the refund, unless the seller offers free returns (RET-9), in which case the seller pays (JE-19) | Customer pays, deducted from the refund |

- RET-10 The change-of-mind return fee is the return-shipping rate for the parcel's destination zone and weight tier from Nyazek's rate card ([logistics](logistics.md) §4), capped at the refund amount. It is shown before the request is submitted (REF-6) and posted per JE-20.

v5 charged the seller in every case, which invites abuse.

## 4. Return state machine

| State | Entered when | Next | Timer |
|---|---|---|---|
| `REQUESTED` | Customer submits lines, reason, evidence and (for COD) the refund account | `APPROVED`, `REJECTED`, `CANCELLED` | Seller response `cfg:returns.seller_response_hours` (default 48); silence ⇒ `APPROVED` |
| `APPROVED` | Seller or system approves; return shipment created | `IN_TRANSIT`, `EXPIRED`, `CANCELLED` | Customer hand-over within `cfg:returns.handover_days` (default 7) |
| `REJECTED` | Seller rejects with reason and evidence | `IN_DISPUTE` (customer opens a dispute), `CLOSED` | Customer may dispute within `cfg:disputes.open_after_decision_days` (default 7); silence ⇒ `CLOSED` |
| `IN_TRANSIT` | Courier collects from customer | `RECEIVED`, `LOST` | Courier SLA |
| `RECEIVED` | Delivered to the seller or Nyazek | `ACCEPTED`, `CONTESTED` | Inspection `cfg:returns.inspection_hours` (default 48); silence ⇒ `ACCEPTED` |
| `ACCEPTED` | Inspection passes, auto-accepted, the customer accepts a partial-refund proposal, or a dispute is resolved for the customer or split | `REFUNDED` | Refund SLA (PAY-15) |
| `CONTESTED` | Seller reports a problem (item differs, used, missing parts) with evidence, optionally proposing a partial refund | `ACCEPTED` (customer accepts the partial refund), `IN_DISPUTE` | Customer response `cfg:returns.contest_response_hours` (default 72); silence ⇒ dispute opened automatically |
| `IN_DISPUTE` | A dispute is open on this return (§6) | `ACCEPTED` (on `RESOLVED_CUSTOMER` or `RESOLVED_SPLIT`, including after a review), `CLOSED` (only when the dispute reaches `CLOSED` with `RESOLVED_SELLER`, or is withdrawn) | Dispute timers, including the review window |
| `REFUNDED` | Refund succeeded | `CLOSED` | – |
| `EXPIRED` | Customer did not hand over in time | `CLOSED` | – |
| `LOST` | Return parcel lost by courier | `ACCEPTED` (customer refunded in full; courier claim: 3P seller compensated per JE-38, 1P loss and claim per JE-43 and JE-44) | – |
| `CANCELLED` | Customer withdraws before hand-over | `CLOSED` | – |
| `CLOSED` | End of the record | terminal | – |

- RET-11 Outcome for the goods: after `ACCEPTED` the goods stay with the seller (restocked per RET-4). When a received return ends `CLOSED` without refund (`RESOLVED_SELLER`, after the review window), the seller sends the item back to the customer through a reverse shipment Nyazek arranges; the customer bears that shipping for change-of-mind returns, the seller in every other case. The customer may instead leave the item with the seller, recorded on the return.
- RET-12 Inspection at `RECEIVED` records, per unit, one of the conditions in RET-4 and the outcome accept or contest; `DAMAGED` or `NOT_AS_SENT` requires photo evidence and a note when the seller contests.

- RET-3 Seller inaction never blocks a refund: both waiting steps auto-advance in the customer's favour.
- RET-4 Inspection outcome records the item condition: `RESELLABLE`, `DAMAGED`, `NOT_AS_SENT`. Only `RESELLABLE` prompts the seller to restock ([inventory](inventory.md) STK-5).
- RET-5 For low-value items below `cfg:returns.returnless_threshold` (default 0, disabled) the admin may enable refund without return (P2).
- RET-6 The return window, the change-of-mind flag and the non-returnable flag that apply to an order line are those in force when the order was placed; they are stored on the line. Later changes to a category's policy, or moving the product to another category, affect only new orders.
- RET-7 The returnable quantity of a line is the delivered quantity minus quantities already in a return that is not `REJECTED`, `EXPIRED` or `CANCELLED`. A request above it is refused.

### 4.1 Replacement

v6 required the customer to request a replacement before a refund. That conflicts with the money-back guarantee and needs a fulfilment flow v6 never specified. At launch every accepted return ends in a refund; the customer reorders if they still want the item. An optional "replace instead" choice is P1. This change is listed for ratification under D-25.

### 4.2 Warranty claims after the return window

- RET-8 After the return window closes, a defect is a **warranty** matter between the customer and the warranty provider named on the listing (seller, brand or service centre; type and duration are mandatory listing data where the category requires them). At launch the customer raises it through a support ticket linked to the order; Support connects the customer with the seller and records the outcome. A seller who refuses a valid warranty obligation is handled as a policy violation ([seller-performance](../03-sellers/seller-performance.md)). A structured warranty-claim flow is P2. Nyazek is the warranty contact for 1P items.

## 5. Refund amount and execution

| Component | Refunded? |
|---|---|
| Cash paid for the returned lines (stored allocation) | Yes |
| Original shipping fee | Only when the whole sub-order is returned for a seller-, courier- or Nyazek-fault reason |
| COD fee | Same rule as shipping fee |
| Return shipping | Deducted when the customer pays it (§3) |
| Platform coupon and loyalty points used on the lines | Not paid in cash; coupon usage is not restored for partial returns; redeemed points are restored if not expired ([loyalty](loyalty.md) §5) |
| Points earned on the lines | Reversed |

Refund saga: `return ACCEPTED` or `dispute RESOLVED` → Returns creates a `Refund` request → Ledger posts JE-14 or JE-15 (with commission reversal and a wallet hold or debit) → Payments executes by the route in [payments](../04-finance/payments.md) §6 → on success JE-17, credit note issued, notifications sent. Each step is idempotent.

- REF-1 Prepaid orders are refunded to the original method. COD orders are refunded to the customer's verified refund account (D-02 recommended default). No store credit exists.
- REF-2 If the escrow for the affected lines is still held, the refund comes from it; if already released, it is recovered from the seller's wallet (possibly creating a deficit, WAL-7).
- REF-3 The customer sees the refund status and expected timing at every step.
- REF-4 A partial return never causes a retroactive shipping charge, even if the remaining items would not have reached the free-delivery threshold (same principle as ORD-6).
- REF-5 A return or refund that falls due while the seller is `SUSPENDED`, `CLOSING` or `CLOSED` is handled by Nyazek in the seller's place (approval, inspection where possible) and paid to the customer on schedule. The amount is recovered from the seller's frozen balance or recorded as Seller Receivable (WAL-7, JE-33).
- REF-6 Before submitting a return request the customer is shown the expected refund amount, each deduction (return shipping for change of mind) and the refund destination.

## 6. Disputes

### 6.1 Opening

| Type | Who can open | Window |
|---|---|---|
| Non-delivery (status says delivered) | Customer | Within `cfg:disputes.non_delivery_days` (default 7) of the delivered status |
| Order not arriving (no movement) | Customer | After the promised delivery date + `cfg:disputes.not_arrived_grace_days` (default 3); usually resolved by Logistics before a dispute is needed |
| Return rejected or contested | Customer (automatic on silence after `CONTESTED`) | Within `cfg:disputes.open_after_decision_days` (default 7) of the seller's decision |
| Refund not received | Customer | After the refund SLA has passed |

A dispute blocks escrow release for the affected value (WAL-4) or, after release, places a wallet hold.

### 6.2 State machine

| State | Entered when | Next | Timer |
|---|---|---|---|
| `OPENED` | Customer opens with reason and evidence | `SELLER_RESPONSE` (immediately, after both parties are notified), `WITHDRAWN` | – |
| `SELLER_RESPONSE` | Both parties notified; seller may respond with evidence or accept the claim | `RESOLVED_CUSTOMER` (seller accepts), `UNDER_REVIEW`, `WITHDRAWN` | `cfg:disputes.mediation_hours` (default 48) |
| `UNDER_REVIEW` | Mediation window ended without agreement | `RESOLVED_CUSTOMER`, `RESOLVED_SELLER`, `RESOLVED_SPLIT` | Admin decision within `cfg:disputes.decision_hours` (default 72) |
| `RESOLVED_*` | Decision recorded with reasons; refund or release executed at once | `REVIEW_REQUESTED`, `CLOSED` | Review window `cfg:disputes.review_request_hours` (default 48); silence ⇒ `CLOSED` |
| `REVIEW_REQUESTED` | A party requests review with new evidence (DSP-4) | `RESOLVED_*` (final, by a different admin), then `CLOSED` | `cfg:disputes.decision_hours` |
| `WITHDRAWN` | Customer withdraws (only from `OPENED` or `SELLER_RESPONSE`) | `CLOSED` | – |
| `CLOSED` | End of the record | terminal | – |

- DSP-1 For non-delivery disputes the investigation uses the proof of delivery, courier scans and call logs; no refund is issued before the investigation concludes, which must be within the decision timer.
- DSP-2 Decisions are made by a Support Agent up to `cfg:disputes.agent_limit` (default 250,000 IQD) and require a second approver (Finance Manager) above it.
- DSP-3 `RESOLVED_SPLIT` records the refund amount and who bears it (seller, courier, Nyazek goodwill).
- DSP-4 Each party may request one review of a decision within the review window by providing new evidence; a different admin reviews it. After that the decision is final on the platform. A refund already paid to the customer is never clawed back: if the review favours the seller, Nyazek compensates the seller (5150 → 2110, JE-31). If the review favours the customer, the additional refund is executed as for a first decision.
- DSP-6 A dispute opened on a return drives that return's state (`IN_DISPUTE`, then the outcome in §4). A non-delivery or not-arriving dispute resolved for the customer creates a refund for the affected lines (JE-14 or JE-15) with the cost attributed per DSP-3.
- DSP-5 Every dispute event, evidence item, decision and accounting entry is audited and references the dispute ID.

## 7. Customer-abuse controls

- A return-abuse score per customer is derived from return rate, contested returns, `NOT_AS_SENT` outcomes and refused deliveries.
- Above `cfg:returns.abuse_proof_threshold`, every return requires photo or video proof regardless of value.
- Above `cfg:returns.abuse_restrict_threshold`, change-of-mind returns are disabled for the customer and the account is reviewed by Risk. Fault-based returns are never blocked.
- Thresholds are set during the closed beta.

## 8. Fault attribution for damage

Damage reported on delivery is investigated: courier at fault → courier liable; inadequate seller packaging → seller liable; undetermined → Nyazek absorbs. The customer's refund does not wait for attribution.

## 9. Acceptance criteria

- With the seller silent at every step, a valid return still reaches `REFUNDED` within the configured timers.
- A partial return of a discounted multi-item sub-order refunds exactly the stored cash allocation of the returned lines, reverses proportional commission and earned points, and leaves the ledger balanced.
- A return approved after escrow release produces a wallet hold immediately and a debit at refund.
- A dispute above the agent limit cannot be resolved by a single admin.
