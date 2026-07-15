---
table_name: "public.fact_billing_invoices"
domain: "Finance"
tags: ["revenue", "invoices", "payments", "historical"]
granularity: "One finalized invoice per customer per billing cycle"
---

## 1. Semantic Boundaries

**Primary Intent:** Contains finalized historical customer invoices issued for completed billing cycles.

### ✅ USE THIS TABLE FOR:

- Calculating historical invoiced revenue and settled invoice amounts.
- Checking the status of issued invoices.
- Aggregating final settlement amounts over invoice dates.

### ❌ DO NOT USE THIS TABLE FOR:

- Pending orders or shopping-cart activity; use `public.fact_pending_orders` instead.
- Current recurring revenue or forward-looking MRR; use `public.mrr_active` instead.
- Customer names or addresses; join `public.dim_customers` instead.

## 2. Schema Definition

| Column Name | Data Type | Primary/Foreign Key | Semantic Description |
|---|---|---|---|
| `invoice_id` | UUID | PK | Unique identifier assigned when the invoice is finalized. |
| `customer_id` | UUID | FK | Identifier of the billed customer. Join to `public.dim_customers.id`. |
| `billing_cycle_start_at` | TIMESTAMPTZ | None | Inclusive start of the billing cycle in UTC. |
| `billing_cycle_end_at` | TIMESTAMPTZ | None | Exclusive end of the billing cycle in UTC. |
| `st_amt` | NUMERIC(18,2) | None | Final amount settled in the currency identified by `currency_code`, after discounts and before tax. Null until settlement completes. |
| `currency_code` | CHAR(3) | None | ISO 4217 currency code used by all monetary values on the invoice. |
| `status` | VARCHAR(20) | None | Current invoice lifecycle state. Valid values appear in the sample-values section. |

## 3. Relationships & Joins

- `public.dim_customers`: `public.fact_billing_invoices.customer_id` = `public.dim_customers.id` (Many-to-One)
- `public.fact_payments`: `public.fact_billing_invoices.invoice_id` = `public.fact_payments.invoice_id` (One-to-Many)

## 4. Sample Values (Categorical/Enums)

| `invoice_id` | `status` | `currency_code` |
|---|---|---|
| `00000000-0000-4000-8000-000000000001` | `PAID` | `USD` |
| `00000000-0000-4000-8000-000000000002` | `OVERDUE` | `EUR` |
| `00000000-0000-4000-8000-000000000003` | `REFUNDED` | `USD` |
