# Glossary

**Authoritative for:** terms used across the documentation. A term is used with one meaning only.

| Term | Definition |
|---|---|
| 1P | First-party: products owned and sold by Nyazek through the Nyazek Official Store. Nyazek is the principal |
| 3P | Third-party: products sold by independent sellers. Nyazek is the agent and earns commission |
| Account realm | One of `CUSTOMER`, `SELLER` (owner or staff), `ADMIN`. Each has its own login surface, sessions and permissions |
| ADR | Architecture decision record, stored in `docs/adr/` |
| Allocated (stock) | Units belonging to placed orders that have not yet been handed to the courier |
| AOV | Average order value: delivered GMV ÷ delivered orders |
| Audience | The API surface a session or token is valid for: `storefront`, `seller` or `admin` |
| Audit trail | The append-only, hash-chained record of business and admin actions; distinct from operational logs |
| Available (stock) | `on_hand − reserved − allocated` |
| Available (wallet) | Seller Payable balance minus active holds; the amount eligible for payout |
| Buy Box | The default offer shown on a canonical product variant, chosen by the Buy Box score |
| Canonical product | The single shared catalogue page for a product, with content owned by Nyazek; sellers attach offers to its variants |
| Checkout session | The server-side record created when a customer proceeds from cart to checkout; it reserves stock |
| Claude | The sole AI engineering agent used on the project, working under human supervision |
| COD | Cash on delivery |
| COD collection | The record of cash expected, collected and remitted for one shipment |
| Customer | A person who shops on Nyazek: browses, orders, pays, receives, returns, reviews. The single official term in documentation, interfaces, APIs and code for what earlier versions called "buyer". Arabic interface term: العميل (proposed; confirmed in copy review). A seller's staff and Nyazek staff are never called customers |
| Computer use | Claude's capability to operate a browser or desktop to inspect designs and verify implementations |
| Configuration value (`cfg:`) | A named, typed, audited platform setting listed in the configuration register |
| Dual control | An action requested by one admin and approved by a different admin |
| Escrow hold | The period after delivery during which seller proceeds stay in Customer Funds Held before release |
| Edge-case register | The list of cross-document situations and their required behaviour in the user-journeys document (IDs `EC-n`) |
| E-invoicing | Reporting or clearing of invoices with a tax authority in a structured format, required in some Gulf markets |
| Event (domain event) | A fact published by a module through the outbox, named `<aggregate>.<past_tense>` |
| Flutter | The framework used for the Android and iOS apps |
| Functional currency | The currency in which a market's book is kept |
| GMV (delivered) | Item value of sub-orders delivered in a period, after seller-funded and before platform-funded discounts |
| GTIN | Global Trade Item Number (barcode: EAN or UPC) used to match offers to canonical variants |
| Goods receipt | The record of 1P stock received from a supplier with its quantity and unit cost |
| Handling time | Days a seller needs to prepare an order for hand-over |
| Hazardous item | An item with shipping restrictions (for example loose lithium batteries, aerosols, perfumes), flagged on the listing |
| Hold (wallet) | A reservation on a seller's Available balance for a chargeback, return, dispute, risk case or destination change |
| Identity claim | The record binding one canonical email or phone to one account across all realms |
| Idempotency key | A client-supplied key that makes a repeated request return the original result |
| IFRS 15 | The accounting standard governing revenue recognition for principal and agent models |
| Information architecture | The organisation of the applications: pages, navigation, labels and the content of each page ([09-information-architecture](../09-information-architecture/README.md)) |
| Journey | An end-to-end path through the product for a customer, seller or staff member (IDs `JC-n`, `JS-n`, `JA-n`) |
| IQD | Iraqi dinar, the currency of the Iraq market and the only currency enabled at launch |
| KYC | Seller identity and document verification |
| Listing type A / B / C | Offer on an existing canonical product / new canonical product request / seller-owned listing |
| MAC | Monthly active customers: distinct customers with at least one delivered sub-order in a calendar month |
| MAP | Minimum advertised price set by a brand for its authorised distributors |
| Market | A country in which Nyazek operates, with its own entity, currency, tax rules, providers and legal documents. Iraq is the only market at launch |
| Market readiness | The P0 design constraints that let a later market be added by configuration and integration |
| Minor unit (platform) | The smallest stored unit of a currency on the platform, set by the currency table; whole dinars for IQD |
| Modular monolith | One deployable backend structured into isolated modules with enforced boundaries |
| Module | A bounded part of the backend owning its schema, rules and public contract |
| Offer | A seller's price, stock, condition, handling time and origin for one product variant. Also the meaning of "SKU" and "listing" in KPIs |
| OpenAPI | The machine-readable API description from which TypeScript and Dart clients are generated |
| Order / Sub-order / Order line | The customer's purchase / the part fulfilled by one seller / one offer and quantity within a sub-order |
| Outbox | A table written in the same transaction as a state change, from which events are dispatched reliably |
| Page specification | The description of one page's template, content, actions, states and governing rules ([09-information-architecture](../09-information-architecture/README.md)) |
| Page template | A reusable page structure (`TPL-…`) that page specifications build on |
| P0 / P1 / P2 / Future | Launch gate / launch target (30-day fast-follow allowed) / post-launch / direction only |
| Page ID | The stable identifier of a page in the sitemap (for example `SF-PDP`) |
| PDP | Product detail page |
| Pending (wallet) | Expected net proceeds of sub-orders paid or delivered but not yet released |
| POD | Proof of delivery: delivery OTP, signature, photo or courier-app confirmation |
| Price step | The unit all prices, fees and payable totals must be a multiple of (250 IQD by default) |
| Protected path | Code that requires plan approval and two reviews (ledger, wallet, payments, identity, audit and others) |
| PSP | Payment service provider |
| Quote | The server-computed price breakdown for a cart or order, stored on the order |
| Recovery point / recovery time | Maximum data loss / maximum time to restore service in a disaster. Written in full to avoid confusion with RTO |
| Reserved (stock) | Units held by open checkout sessions and unpaid prepaid orders |
| RTL | Right-to-left layout and text direction for Arabic |
| RTO | Return to origin: a shipment that could not be delivered and goes back to the seller. In this documentation RTO never means recovery time objective |
| Saga | A multi-module flow made of local transactions linked by events, each idempotent with a compensation |
| Seller of record | The party legally selling the item: the seller for 3P, Nyazek for 1P |
| Serviceability | Whether, how fast and with which courier an address can be served |
| SLA (seller) | The time allowed for a seller to confirm an order and to make it ready to ship |
| SLO | Service-level objective: a measurable reliability target |
| Storefront / Seller Dashboard / Admin Panel | The three web applications for customers, sellers and Nyazek staff |
| Take rate | Commission revenue ÷ 3P delivered GMV |
| Tier A / B / C (courier) | Courier integration capability: full API / partial API / file-based |
| Variant | A purchasable variation of a product (for example size or colour) |
| Zero-trust access | Identity- and device-aware access control in front of the Admin origin |
