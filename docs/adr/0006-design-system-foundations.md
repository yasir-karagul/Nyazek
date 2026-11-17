# ADR-0006: Design-system foundations (D-19)

- **Status:** Accepted
- **Date:** 2026-11-17
- **Decided by:** Claude, under ADR-0005 (delegated; not a reserved item). No designer was consulted for this decision; a designer may refine values later through the normal change control; any change keeps the contrast minimums below.
- **Task:** T-0018
- **Closes:** D-19 in [open-decisions](../prd/00-governance/open-decisions.md)

## Context

[design-system-ui-workflow](../prd/07-clients/design-system-ui-workflow.md) §3 lists corrections that must be decided before any screen is produced: an Arabic typeface (Inter has no Arabic glyphs and Arabic is the default language), the contrast failure of white text on Meteor Orange, orange focus rings and thin orange text, Promo orange that cannot be told apart from Primary, missing token groups, body size and touch targets, automatic dark mode, colour as the only signal, and the numeral format. The token values themselves live in that document (§2.3); this ADR records the choices and the reasons.

Contrast ratios below were computed with the WCAG 2.2 relative-luminance formula. Required minimums: 4.5:1 for normal text, 3:1 for large text and for interface components and focus indicators.

## Decisions

### 1. Arabic typeface

| Option | For | Against |
|---|---|---|
| **Noto Sans Arabic** (chosen) | SIL Open Font License; variable weight axis (one file covers 400, 500, 700); broad Arabic-script coverage including the letters Sorani Kurdish needs (D-13) and Persian forms; neutral, highly legible at small sizes; metrics designed to sit with Latin sans faces | Less distinctive than Plex |
| IBM Plex Sans Arabic | OFL; designed as a companion to a Latin grotesk; good UI rhythm | Static weights (more files); Kurdish coverage to be verified |
| Almarai | OFL; friendly, popular in the Gulf | No 500 weight; narrower script coverage |
| Cairo | OFL; variable | Wide, geometric letterforms take more space in dense tables |

Noto Sans Arabic is chosen for coverage of later markets and Kurdish, a single variable file, and legibility in dense seller and admin tables. Inter stays the Latin face. Fonts are self-hosted and bundled in the apps (no third-party font CDN, so no request leaves for a font provider). Glyph coverage for Sorani Kurdish is checked when the token package is built (frontend guide, T-0042).

### 2. Primary colour and text on orange

| Option | Contrast | Decision |
|---|---|---|
| White on Meteor Orange `#F47B25` | 2.72:1 | Rejected (fails AA) |
| Charcoal `#333333` on Meteor Orange | 4.64:1 | Rejected for filled buttons: passes by a thin margin, and every darker hover or pressed shade lowers it below 4.5:1 |
| White on `#C2560A` (PRD suggestion) | 4.54:1 on white, but 4.24:1 when the same colour is used as text on the page background `#F8F7F5` | Rejected: fails for text links on the page background |
| **White on Primary Strong `#B4500A`** | 5.13:1; as text: 5.13:1 on white, 4.79:1 on `#F8F7F5` | **Chosen** for filled primary buttons, text links and small or thin orange icons. Darker hover and pressed shades only raise the contrast |

Meteor Orange `#F47B25` stays the brand colour for large highlights, illustrations, the logo and non-text accents where no contrast rule applies (decorative use), never for text, thin icons, borders of inputs or focus rings.

### 3. Focus indicator

A 2 px Deep Charcoal `#333333` ring with a 2 px offset (12.63:1 on white, 11.8:1 on the page background), the same on every surface. Rejected: an orange ring (2.72:1).

### 4. Promotions

Promo Accent `#FF6B00` and Meteor Orange differ by 1.05:1 and cannot be told apart. Decision: discounts and deal prices use **Deal Red `#B3261E`** (6.54:1 with white text) in a pill-shaped badge with a text label (for example "−20%"), so the meaning never depends on colour alone. Deal Red and the Error red are close (1.16:1 between them); they are kept apart by shape and content: a deal is always a pill badge with a percentage or "Deal" label next to a price, an error is always an icon with a message next to the field or action it concerns. Promo Accent is restricted to campaign artwork in banners and landing-page illustrations; it is never used for text, buttons, badges or next to a Primary element. Rejected: keeping Promo orange with a different shape only (still confusable at a glance).

### 5. Missing token groups

Semantic colours (error, success, warning, info, each with a tinted background), a neutral scale, spacing, elevation, breakpoints, motion and z-index are defined in [design-system-ui-workflow](../prd/07-clients/design-system-ui-workflow.md) §2.3 with the contrast of every text pairing at or above 4.5:1 (disabled controls exempt), and every interface-component border at or above 3:1. A dense variant (smaller row height and 14 px text) serves Seller and Admin tables.

### 6. Body size and touch targets

Body text is 16 px in both languages on every screen size; 14 px is the smallest text size and is used only for secondary text and dense tables. Arabic uses a taller line height (1.7) than Latin (1.5) because of its vertical extent. Touch targets are at least 44 × 44 CSS px on the web and 48 × 48 dp in the apps ([mobile-flutter](../prd/07-clients/mobile-flutter.md) MOB-11). Rejected: 14 px body (too small for Arabic on phones).

### 7. Light only

Every web app declares `color-scheme: light` and the apps declare a light interface style, so systems that auto-darken leave the interface unchanged (MOB-5).

### 8. Colour never the only signal

Status chips, price changes, validation and stock states always pair colour with text or an icon.

### 9. Numerals and price format

Western digits in both languages, as MON-7 sets: `125,000 IQD` (English) and `125,000 د.ع` (Arabic), with the amount isolated left-to-right inside Arabic text (§5 RTL rules). Rejected: Arabic-Indic digits by default (inconsistent with order numbers, phone numbers and payment-provider screens customers compare against). The input fields still accept Arabic-Indic digits (Phone and OTP input).

## Consequences

- D-19 is closed in the register and its decision log.
- [design-system-ui-workflow](../prd/07-clients/design-system-ui-workflow.md) gains §2.3 (decided token values), §3 points each correction to this ADR, and §4 states the primary-button colours.
- The token values become `packages/design-tokens/tokens.json` when the repository skeleton is created; the frontend guide (T-0042) covers the token generator (ADR-0004 OI-4) and the Kurdish glyph check.
- T-0019 (design briefs) can start once its other dependencies are met.
