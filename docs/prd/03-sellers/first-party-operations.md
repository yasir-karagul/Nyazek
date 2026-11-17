# First-Party (1P) Operations

**Authoritative for:** how the Nyazek Official Store operates: stock receiving and cost, stock adjustments, pricing and margin, fulfilment, returns to the warehouse, suppliers, 1P controls.
**Related:** [seller-accounts-kyc](seller-accounts-kyc.md) §8 · [inventory](../02-commerce/inventory.md) · [pricing-promotions](../02-commerce/pricing-promotions.md) §1.4 · [ledger-reconciliation](../04-finance/ledger-reconciliation.md) §4.5 · [admin-panel](../05-trust/admin-panel.md) · [sitemap](../09-information-architecture/sitemap.md) §8.4

---

## 1. Model

- FP-1 The 1P store is a system-owned seller entity ([seller-accounts-kyc](seller-accounts-kyc.md) §8). It uses the same catalogue, offer, order, shipment, return and review flows as 3P sellers; this document adds only what is different.
- FP-2 1P is operated in the Admin Panel by the 1P Merchandiser role. Cost and margin data are visible only to the 1P Merchandiser, Finance Manager and Super Admin.
- FP-3 1P offers obey every marketplace rule a seller obeys (price floor, reference price, listing content, prohibited items, SLAs). 1P gets no advantage beyond the published Buy Box component ([search-buy-box](../02-commerce/search-buy-box.md) §2.3).
- FP-4 At launch Nyazek operates one 1P stock location. Multiple warehouses, bin locations and pick-path management are post-launch.

## 2. Suppliers (basic record, P0)

Name, legal identifiers, contact, payment terms, currency, the brands supplied, and return-to-supplier terms. Supplier portal, purchase orders and automatic replenishment are P2.

## 3. Stock receiving and cost

- FP-5 Stock enters only through a **goods receipt**: supplier, reference (invoice or delivery note), date, and per variant the quantity received and the unit cost. A receipt increases `on_hand` and posts JE-34.
- FP-6 Cost of goods uses the method in `cfg:firstparty.costing_method` (default WEIGHTED_AVERAGE), an accountant decision (D-42). The cost applied to a sale is frozen on the order line when the stock is allocated.
- FP-7 Batch and expiry dates are recorded at receipt for categories flagged `requires_expiry`; stock is picked first-expiring-first, and units below the minimum shelf life ([catalog-listings](../02-commerce/catalog-listings.md) §2.1) are blocked from sale.
- FP-8 Serial or IMEI numbers are recorded at receipt for categories flagged `requires_serial`.

## 4. Adjustments and counts

| Adjustment | Reason codes | Control |
|---|---|---|
| Decrease | Damaged, expired, lost, sample or marketing use, count correction | Posts JE-36; above the value threshold set by Finance, dual control |
| Increase | Count correction, found | Reverses JE-36 at current average cost; dual control always |
| Return to supplier | Defective batch, recall, overstock under supplier terms | Decreases stock; posts JE-36 against the supplier payable where a credit is agreed |

- FP-9 A full stock count is performed at least quarterly; differences are posted as adjustments with the count as evidence.
- FP-10 Every receipt and adjustment is audited with actor, reason and attachment.

## 5. Pricing and margin

- 1P prices are set by the 1P Merchandiser within pricing rules; the margin alert in PRC-8 applies.
- Selling below cost requires a reason and Finance approval, and is reported.
- 1P participates in platform promotions on the same terms as sellers; discounts on 1P items are Nyazek's own cost.

## 6. Fulfilment

- 1P sub-orders appear in the admin order screens (1P variant) and follow the same state machine and SLAs; breaches feed the 1P store's score, which is used only for the Buy Box and search, never for consequences (PRF-7).
- Labels, packing slips and receipts are produced exactly as for 3P; Nyazek is the issuer of the receipt ([tax-invoicing](../04-finance/tax-invoicing.md) §3).

## 7. Returns and failed deliveries

- Returned and RTO parcels arrive at the 1P stock location and create a restock task.
- FP-11 Inspection outcome decides the stock movement: `RESELLABLE` returns to `on_hand` at its original cost (JE-37); `DAMAGED` or `NOT_AS_SENT` is written off (JE-36) or returned to the supplier.
- Return shipping cost follows [returns-disputes](../02-commerce/returns-disputes.md) §3 (1P column).

## 8. Reporting

Stock on hand and value, ageing and expiring stock, sell-through, margin by product and category, shrinkage, supplier fill rate. Finance figures come from the ledger (DAT-4).

## 9. Out of scope for v1.0

Purchase orders and replenishment planning, warehouse management, multi-location stock, consignment stock, fulfilment of 3P sellers' goods by Nyazek.

## 10. Acceptance criteria

- No 1P unit can be sold without a goods receipt that carries a cost.
- For any sequence of receipts, sales, returns and adjustments, the value of account 1200 equals quantity on hand × the costing method's unit cost.
- Cost and margin fields are absent from every API response to roles other than those in FP-2.
