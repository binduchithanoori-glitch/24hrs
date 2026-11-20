# Stylora project overview

## Objectives

Stylora's objective is to make fashion discovery more practical by translating a shopper's style intent and budget into product suggestions and outfit combinations. In the available prototype, recommendations are grounded in supplied product data, with recorded price and availability used as constraints.

## Target users

- Budget-conscious shoppers who want to state a spending cap in plain language.
- People shopping for a particular occasion, colour, or style direction.
- Shoppers who want help combining individual catalog items into a look.

These are intended user groups inferred from the prototype's supported inputs; no user research or frontend onboarding was present in the inspected files.

## Main features

**Implemented in the inspected styling-engine prototype:**

- Natural-language preference parsing for common budgets, styles, colours, occasions, and categories.
- Optional Gemini-based intent extraction with deterministic fallback.
- Product filtering using supplied price and availability, relevance scoring, and short reason strings.
- Outfit composition from a dress or a top-and-bottom combination, with optional finishing categories and a total-price limit.
- Demo catalog data, explicitly marked simulated.

**Unverified / planned:**

- Interactive frontend, its pages, controls, and end-to-end workflow.
- HTTP API and frontend integration.
- Live retailer catalog, price, stock, or affiliate integrations.
- User accounts, saved preferences, and persistent history.
- Checkout, payment, delivery, and order tracking.

## Innovation and uniqueness

The prototype combines conversational intent with explicit budget filtering and multi-item outfit assembly. Its key trust property is that it ranks caller-provided product records rather than inventing price or availability. Optional language-model use is scoped to parsing preferences; deterministic logic performs the product filtering, scoring, and outfit assembly. The sample catalog is simulated, so production claims depend on connecting verified catalog data.
