# Tax & Invoicing

**Authoritative for:** tax position and tax engine, customer documents, seller commission invoices, numbering and retention.
**Related:** [ledger-reconciliation](ledger-reconciliation.md) · [commission-wallet-payouts](commission-wallet-payouts.md) · [compliance-legal](../05-trust/compliance-legal.md)

---

## 1. Tax position at launch

- Iraq has no general value-added tax. The platform applies a 0% rate to all lines at launch.
- This is an assumption to be confirmed by tax counsel, including whether any sales tax or duty applies to specific launch categories and what the General Commission for Taxes requires under the e-commerce regulation ([compliance-legal](../05-trust/compliance-legal.md) §2).
- Prices shown to customers are tax-inclusive. Commission rates shown to sellers are tax-exclusive.
- Sellers are responsible for their own income-tax obligations.

## 2. Tax engine

- TAX-1 Every order line, shipping fee, COD fee and commission amount carries `taxRate`, `taxAmount` and `taxRegion` fields (0 and `IQ-0` at launch) in the database, APIs, events and documents.
- TAX-2 Rates are stored in a table keyed by tax region and tax category with effective dates. Product categories map to a tax category.
- TAX-3 Introducing a tax is expected to be a configuration change plus a review of document templates and counsel's rules for inclusive pricing and rounding. v6's claim of "no code changes" is not guaranteed; the abstraction keeps the change small.
- TAX-4 Tax collected is posted to Tax Payable (2150) in the same journal entry as the related revenue or liability.
- TAX-5 Whether prices are displayed tax-inclusive, the tax rates, the document templates, the mandatory fields and the numbering series are defined per market. Iraq's values are those in this document.
- TAX-6 Document issuance goes through an `EInvoicingPort`. In Iraq its adapter does nothing. In a market where invoices must be reported to or cleared by the tax authority in a structured format, the adapter performs that exchange and the document is final only when the authority's response is recorded. No such adapter is built in v1.0 ([market-expansion](../01-product/market-expansion.md) §5).

## 3. Documents

| Document | Issued for | Issuer shown | When | Series |
|---|---|---|---|---|
| Sales receipt | Each sub-order | 3P: the seller as seller of record, "issued by Nyazek on behalf of the seller". 1P: Nyazek | At `SHIPPED` (a copy travels with the parcel as the packing slip) | Per issuing entity and year |
| Credit note | Refund, failed delivery or loss after a receipt exists | Same issuer as the receipt | When the refund is approved (JE-14, JE-15, JE-16), or at `DELIVERY_FAILED` or `LOST`; its amounts equal the ledger entry | Per issuing entity and year |
| Commission invoice | Each seller, per settlement period, itemised by sub-order; commission reversed in the period (JE-15) appears as negative lines referencing the original invoice | Nyazek | At payout cut-off | Nyazek series per year |
| Payout statement | Each payout | Nyazek | At payout | Not a tax document |

Changes from v6 and reasons:

- v6 issued the customer invoice from Nyazek for every order. For 3P sales the seller is the principal, so the document must name the seller; whether Nyazek may issue it on the seller's behalf and what legal form it takes is decision D-26 for counsel.
- v6 issued one commission invoice per settled order. One itemised invoice per settlement period carries the same information with far fewer documents.
- The receipt is issued at shipping rather than at completion so the customer has it with the parcel; cancellations before shipping need no document.

Content of every document: document number and date, issuer legal name, address, registration and licence numbers, customer or seller name, order and sub-order numbers, itemised lines with unit price, quantity, discounts by funder, shipping and COD fees, tax line (0% at launch), total in the market currency (IQD in Iraq), payment method. Documents are bilingual (Arabic and English).

## 4. Numbering and immutability

- INV-N1 Numbers are sequential and gapless per series, allocated inside the issuing transaction from a locked counter row.
- INV-N2 A document is immutable after issue. Corrections are made only by a credit note that references the original, followed by a new document if needed.
- INV-N3 The rendered PDF is stored in object storage with its hash recorded; regenerating a document reproduces the stored file, not a fresh render.
- INV-N4 Documents and their data are retained for 7 years ([privacy-audit](../05-trust/privacy-audit.md) §4).

## 5. Access

- Customers download receipts and credit notes from the order page; guests through order lookup.
- Sellers download receipts for their sub-orders, commission invoices and payout statements from the Seller Dashboard.
- Finance and Compliance roles can search all documents.

## 6. Rendering

Documents are HTML templates rendered to PDF with headless Chromium to guarantee correct Arabic shaping and bidirectional text ([technology-stack](../06-platform/technology-stack.md) §3.14). Templates are versioned; the template version is stored with each document.

## 7. Acceptance criteria

- Concurrent issuance never produces duplicate or missing numbers (concurrency test).
- A refund after a receipt always produces a credit note whose amounts equal the ledger refund entry.
- Changing the tax rate table with a future effective date affects only orders placed after that date.
