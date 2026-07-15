# Table Semantic Profile Schema

## Purpose

This document defines the strict Markdown structure required for database table semantic profiles. Every profile must follow this structure so the Retrieval-Augmented Generation (RAG) pipeline can parse frontmatter, apply vector-database metadata filters, chunk sections consistently, and retrieve the correct table for a query.

## System instructions for profile generation

When generating a table profile, the output MUST strictly follow the structure between `TEMPLATE_START` and `TEMPLATE_END`.

- **YAML frontmatter:** Use valid YAML enclosed by `---`. The ingestion pipeline extracts these values for vector-database metadata filtering.
- **Headers:** Preserve the four H2 headers exactly. The retrieval system relies on these names when chunking documents.
- **Tables:** Use strict Markdown tables for the schema definition and sample values.
- **Formatting:** Use concise, declarative language. Do not include conversational filler.
- **Boundaries:** State both valid uses and explicit anti-patterns. Name the correct alternative table whenever possible.
- **Schema descriptions:** Expand abbreviations, define units, and explain inclusions or exclusions.
- **Examples:** Include representative categorical values exactly as they occur in the database.

## Required template

`TEMPLATE_START`

```markdown
---
table_name: "[schema].[table_name]"
domain: "[e.g., Billing, Inventory, HR]"
tags: ["[tag1]", "[tag2]", "[tag3]"]
granularity: "[What one row represents, e.g., One completed invoice]"
---

## 1. Semantic Boundaries

**Primary Intent:** [One concise sentence explaining what this table represents in the business.]

### ✅ USE THIS TABLE FOR:

- [Specific query intent 1, e.g., "Calculating total historical revenue."]
- [Specific query intent 2, e.g., "Finding settled or refunded invoice amounts."]

### ❌ DO NOT USE THIS TABLE FOR:

- [Anti-pattern 1, e.g., "Pending or draft orders; use `fact_pending_orders` instead."]
- [Anti-pattern 2, e.g., "Customer names or addresses; use `dim_customers` instead."]

## 2. Schema Definition

| Column Name | Data Type | Primary/Foreign Key | Semantic Description |
|---|---|---|---|
| `[column_1]` | `[type]` | `[PK/FK/None]` | [What the column means. Expand abbreviations.] |
| `[column_2]` | `[type]` | `[PK/FK/None]` | [Example: Settlement amount in USD. Excludes tax.] |

## 3. Relationships & Joins

- `[target_table_name]`: `[this_table].[column]` = `[target_table].[column]` ([Relationship type, e.g., Many-to-One])
- `[target_table_name]`: `[this_table].[column]` = `[target_table].[column]` ([Relationship type])

## 4. Sample Values (Categorical/Enums)

Provide 3–5 representative rows. Prioritize categorical columns so the retrieval and query-generation system learns the exact stored values.

| `[column_1]` | `[categorical_column_2]` | `[categorical_column_3]` |
|---|---|---|
| `[value]` | `[e.g., PAID]` | `[e.g., USD]` |
| `[value]` | `[e.g., OVERDUE]` | `[e.g., EUR]` |
```

`TEMPLATE_END`

## Example of a parsable profile

```markdown
---
table_name: "public.fact_billing_invoices"
domain: "Finance"
tags: ["revenue", "invoices", "payments", "historical"]
granularity: "One finalized invoice per customer per billing cycle"
---

## 1. Semantic Boundaries

**Primary Intent:** Contains all finalized historical customer invoices and billing records.

### ✅ USE THIS TABLE FOR:

- Calculating historical revenue and settled payments.
- Checking the status of issued invoices.
- Aggregating total settlement amounts (`st_amt`) over time.

### ❌ DO NOT USE THIS TABLE FOR:

- Pending orders or shopping-cart data; use `public.cart_abandonment` instead.
- Future revenue projections or active MRR; use `public.mrr_active` instead.
- User demographic data; join with `public.dim_customers` instead.

## 2. Schema Definition

| Column Name | Data Type | Primary/Foreign Key | Semantic Description |
|---|---|---|---|
| `invoice_id` | UUID | PK | Unique identifier for the finalized invoice. |
| `customer_id` | UUID | FK | Identifier of the billed customer. |
| `st_amt` | FLOAT | None | Settlement amount in USD. This is the final amount paid by the customer. |
| `status` | VARCHAR | None | Current state of the invoice. |

## 3. Relationships & Joins

- `public.dim_customers`: `public.fact_billing_invoices.customer_id` = `public.dim_customers.id` (Many-to-One)
- `public.fact_payments`: `public.fact_billing_invoices.invoice_id` = `public.fact_payments.invoice_id` (One-to-Many)

## 4. Sample Values (Categorical/Enums)

| `invoice_id` | `customer_id` | `st_amt` | `status` |
|---|---|---:|---|
| `a1b2...` | `c9d8...` | 150.00 | `PAID` |
| `e5f6...` | `g7h6...` | 45.50 | `OVERDUE` |
| `i9j0...` | `k1l2...` | 900.00 | `REFUNDED` |
```

## Parser contract

A generated table-profile document is valid only when:

1. YAML frontmatter is the first content in the generated profile.
2. Frontmatter contains `table_name`, `domain`, `tags`, and `granularity`.
3. The document contains each required H2 header exactly once and in the specified order.
4. Schema columns appear in a valid four-column Markdown table.
5. Sample values appear in a valid Markdown table.
6. Join expressions name both tables and both columns explicitly.
7. Semantic boundaries include at least one valid use and one invalid use.
8. The document contains no commentary outside the required profile structure.
