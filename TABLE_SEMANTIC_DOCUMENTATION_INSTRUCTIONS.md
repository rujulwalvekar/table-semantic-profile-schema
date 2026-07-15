# Table Semantic Documentation Instructions

## 1. Purpose

Use this document to create consistent semantic descriptions of database tables for a tax system. The descriptions will help an AI agent, retrieval system, or text-to-SQL system identify the correct table before generating a query.

The objective is not merely to describe what columns exist. The objective is to explain:

- What business concept the table represents
- What one row represents
- Which questions the table can answer
- Which questions it must not answer
- Which nearby tables are easy to confuse with it
- How it joins to related tables
- What its codes, dates, amounts, statuses, and identifiers mean
- Which reference tables define its values
- Which restrictions apply to sensitive taxpayer and account data

Treat an incorrect semantic statement as worse than a missing statement. Never invent business meaning, joins, code values, units, or table relationships.

## 2. Required storage approach

This instruction document is the only required supporting file.

A system does not need one physical Markdown file per database table. Physical file boundaries and retrieval boundaries are separate concerns.

Use the following approach:

1. Maintain this file as the single source of instructions.
2. Create one logical semantic profile for each table.
3. Store generated profiles in whichever format is easiest to maintain:
   - One profile per file
   - Multiple profiles grouped into one domain file
   - Structured catalog records rendered as Markdown
4. During embedding, split the content so each table profile becomes its own retrieval unit.
5. Attach the table name, domain, tax type, jurisdiction, and profile version as vector metadata.

For a large tax system, group profiles by business domain rather than putting every table into one manually maintained document. Suggested domains include:

- Taxpayer identity
- Taxpayer accounts
- Registrations
- Returns and filing obligations
- Assessments
- Payments
- Refunds
- Collections
- Penalties and interest
- Audits and cases
- Correspondence
- General ledger
- Reference data

File space is not the main concern. Maintainability, ownership, stale documentation, merge conflicts, and reliable retrieval are the real concerns.

## 3. Retrieval design

Use two-stage retrieval.

### Stage 1: Select the business domain

Identify whether the question concerns accounts, returns, payments, assessments, refunds, collections, reference data, or another tax domain.

### Stage 2: Select the table

Within the selected domain, compare table profiles using:

- Primary business intent
- Row granularity
- Valid query use cases
- Explicit exclusions
- Important columns
- Valid relationships
- Tax type and jurisdiction
- Current-state versus historical-event semantics
- Nearby tables that should not be selected

Do not select tables through column-name similarity alone. Tax systems commonly reuse names such as `status_cd`, `acct_id`, `period_id`, `amount`, and `effective_dt` across unrelated business processes.

After selecting the table, retrieve its detailed schema and join instructions.

## 4. Required sources

Collect or inspect the following before generating a final table profile:

1. Fully qualified physical table name
2. Database catalog or DDL
3. Primary and foreign keys
4. Unique and not-null constraints
5. Business data dictionary
6. Domain-owner or subject-matter-expert documentation
7. Tax type and jurisdiction
8. One-row granularity
9. Column meanings
10. Valid joins and relationship cardinality
11. Code and reference-table mappings
12. Exact categorical values
13. Amount units, currencies, and sign conventions
14. Date and timestamp semantics
15. Data classification and access restrictions
16. Similar tables that serve different purposes
17. Validated production queries when available

Resolve conflicting information in this order:

1. Database constraints and catalog metadata for physical names, types, and keys
2. Governed data contracts and approved dictionaries
3. Tax-domain-owner documentation
4. Validated production query patterns
5. DDL comments and transformation code
6. Naming conventions only as a lead for investigation

Do not finalize a profile while required business semantics remain unknown.

## 5. Rules for generating a profile

### Rule 1: Preserve physical names

Use the exact database, schema, table, and column names. Do not rename columns into friendlier names inside the schema definition.

### Rule 2: State one-row granularity first

The profile must explain exactly what one row represents.

Good examples:

- One tax account for one taxpayer, tax type, and jurisdiction
- One filed return version for one filing obligation and tax period
- One posted financial transaction against one tax account
- One assessment component for one assessment and liability type
- One effective-dated description for one reference code

Bad examples:

- Tax information
- Account data
- Return records
- Payment details

### Rule 3: Separate positive and negative use cases

State both:

- Questions the table should answer
- Similar questions that belong to another table

The negative boundaries are essential because tax systems contain many tables with overlapping identifiers and status fields.

### Rule 4: Document every queryable column

For each column, state:

- Exact physical name
- Physical data type
- Primary-key or foreign-key role
- Business meaning
- Expanded abbreviation
- Unit or currency
- Sign convention
- Null meaning
- Applicable tax type or jurisdiction
- Relevant time zone
- Whether the value is derived
- Whether the value is current, historical, or effective-dated
- Reference table when the value is coded

Do not merely restate the column name.

Bad:

`assmt_amt`: Assessment amount.

Good:

`assmt_amt`: Original assessed liability in the currency identified by `currency_cd`. A positive value increases the taxpayer's liability. Excludes penalties and interest, which are stored as separate assessment components.

### Rule 5: Document joins as executable facts

Every relationship must include:

- Fully qualified source table and column
- Fully qualified target table and column
- Cardinality
- Additional predicates required for correctness
- Effective-date condition when applicable
- Jurisdiction or tenant condition when applicable

Do not infer a relationship because two columns have similar names.

### Rule 6: Use real categorical values

Include exact stored values for important filters such as:

- Account status
- Return status
- Payment status
- Assessment type
- Tax type
- Filing frequency
- Transaction type
- Collection status
- Jurisdiction
- Currency
- Active/inactive indicators

Preserve exact case and spelling. Do not fabricate enum values.

### Rule 7: Protect sensitive information

Never place real taxpayer or account data into semantic profiles or embedding examples.

Use synthetic values for:

- Taxpayer identifiers
- Tax account numbers
- Government-issued identifiers
- Names
- Addresses
- Email addresses
- Phone numbers
- Bank accounts
- Payment instruments
- Filing information
- Investigation or audit identifiers

Describe the format and meaning without exposing real values.

### Rule 8: Avoid conversational filler

Write concise, declarative statements. Do not include commentary such as “This table is useful because” or “You may want to consider.”

## 6. Tax-system semantic requirements

### 6.1 Taxpayer and account identity

Distinguish among:

- A person or organization
- A taxpayer registration
- A tax account
- A filing obligation
- A tax period
- An account balance
- An account transaction

Document whether an identifier is global, jurisdiction-specific, tax-type-specific, or system-generated.

Never assume that one taxpayer has only one account or that one account represents only one filing period.

### 6.2 Reference data

For every coded column, document:

- The reference table that defines the code
- The code key and description column
- Whether the code is effective-dated
- Whether inactive codes remain valid for historical records
- Whether meaning changes by jurisdiction, tax type, language, or version
- Which business date must be used to select the correct reference row

Do not copy an entire reference table into every operational profile. Document the relationship and retrieve the reference-table profile when needed.

A reference-table profile must explain:

- What code set it governs
- Whether codes are globally unique
- Effective and expiration dates
- Active/inactive behavior
- Display descriptions and language
- Hierarchical parent codes when applicable
- Which operational tables use the code set

### 6.3 Financial amounts

For every amount, document:

- Currency source
- Debit/credit or liability/payment sign convention
- Whether a positive value increases or decreases the taxpayer's balance
- Gross versus net meaning
- Whether tax, penalty, interest, fees, adjustments, reversals, or refunds are included
- Original versus outstanding amount
- Posted versus pending status
- Rounding behavior when material

Never describe an amount simply as “the amount.”

### 6.4 Dates and timestamps

For every temporal column, state the event it represents:

- Filing date
- Receipt date
- Processing date
- Posting date
- Effective date
- Due date
- Assessment date
- Payment date
- Reversal date
- Tax-period start or end
- Account open or close date

Also state:

- Time zone
- Inclusive or exclusive boundary
- Whether the value is supplied by the taxpayer or generated by the system
- Whether later corrections can change it

### 6.5 Current state versus history

Explicitly identify whether a table contains:

- Current state
- Immutable events
- Effective-dated history
- Periodic snapshots
- Change-data-capture records
- Revisions or versions

Do not use a current-state table for historical point-in-time analysis unless the table explicitly supports it.

Do not aggregate every version of a return or assessment without first identifying the authoritative version.

### 6.6 Returns and filing obligations

Document distinctions among:

- Expected filing obligation
- Submitted return
- Accepted return
- Rejected return
- Amended return
- Authoritative return version
- Return line items
- Calculated liability

State which version and status should be used for financial or compliance reporting.

### 6.7 Assessments

Document distinctions among:

- Self-assessment
- System-generated assessment
- Auditor assessment
- Original assessment
- Reassessment
- Assessment component
- Adjustment
- Reversal
- Outstanding assessed balance

State whether penalties and interest are included or stored separately.

### 6.8 Payments and refunds

Document distinctions among:

- Payment instruction
- Payment receipt
- Posted payment
- Payment allocation
- Reversed payment
- Refund request
- Approved refund
- Issued refund
- Returned or failed payment

State whether an amount represents received cash, allocated cash, or an accounting entry.

### 6.9 Security and access

Classify sensitive columns and state whether the table contains:

- Personally identifiable information
- Tax-return information
- Financial-account information
- Audit or investigation data
- Authentication or security data

Do not include credentials, access tokens, unmasked identifiers, or real personal data in examples.

## 7. Exact table-profile structure

Generate each table profile with the following sections and names. Replace every placeholder before publication.

```markdown
---
table_name: "[database].[schema].[table]"
domain: "[tax business domain]"
tax_types: ["[tax type or ALL]"]
jurisdictions: ["[jurisdiction or ALL]"]
tags: ["[retrieval term 1]", "[retrieval term 2]", "[retrieval term 3]"]
granularity: "[exact meaning of one row]"
temporal_behavior: "[current state, event, effective-dated history, snapshot, or versioned]"
data_classification: "[public, internal, confidential, restricted, or applicable classification]"
---

## 1. Semantic Boundaries

**Primary Intent:** [One sentence describing the table's business purpose.]

### USE THIS TABLE FOR

- [Specific question or calculation the table can answer.]
- [Specific question or calculation the table can answer.]

### DO NOT USE THIS TABLE FOR

- [Confusing use case and the correct alternative table.]
- [Confusing use case and the correct alternative table.]

## 2. Schema Definition

| Column Name | Data Type | Key Role | Semantic Description | Reference/Classification |
|---|---|---|---|---|
| `[column]` | `[physical type]` | `[PK, FK, PK/FK, or None]` | [Complete business meaning.] | [Reference table or data classification.] |

## 3. Relationships and Joins

- `[target table]`: `[source table].[source column]` = `[target table].[target column]` ([cardinality]); [additional predicates or effective-date rule].

## 4. Reference Data and Valid Values

| Column | Reference Table | Exact Example Values | Effective-Date Rule | Meaning |
|---|---|---|---|---|
| `[coded column]` | `[reference table]` | `[exact values]` | `[rule or Not applicable]` | [Meaning.] |

## 5. Query and Aggregation Rules

- [Required filter for authoritative or posted records.]
- [Deduplication or version-selection rule.]
- [Amount aggregation and sign rule.]
- [Required jurisdiction, tax type, tenant, or effective-date predicate.]

## 6. Safe Sample Data

| [Selected non-sensitive columns] |
|---|
| [Synthetic values preserving real formats and exact enums] |

## 7. Known Confusions

- `[similar table]`: [Why it is different and when to use it.]

## 8. Validated Question Examples

- [Natural-language question this table should retrieve for.]
- [Natural-language question this table should retrieve for.]
```

The generated profile must not contain unresolved placeholders or real sensitive data.

## 8. Tax-account example

The following example demonstrates the required level of specificity. Names and values are synthetic.

```markdown
---
table_name: "tax_core.account.tax_account"
domain: "Taxpayer Accounts"
tax_types: ["INCOME_TAX", "SALES_TAX"]
jurisdictions: ["US-EXAMPLE"]
tags: ["tax account", "account status", "registration", "filing frequency"]
granularity: "One tax account for one taxpayer, tax type, and jurisdiction"
temporal_behavior: "Current state"
data_classification: "Restricted"
---

## 1. Semantic Boundaries

**Primary Intent:** Stores the current registration and operating status of each taxpayer's tax account for a specific tax type and jurisdiction.

### USE THIS TABLE FOR

- Finding the active tax accounts registered to a taxpayer.
- Determining the filing frequency and account status for a tax type.
- Joining filing obligations, returns, and account transactions to their owning tax account.

### DO NOT USE THIS TABLE FOR

- Calculating historical account balances; use `tax_finance.ledger.account_transaction` and its balance rules.
- Determining which returns were filed; use `tax_filing.return.tax_return`.
- Reconstructing historical account status; use `tax_core.account.tax_account_status_history`.

## 2. Schema Definition

| Column Name | Data Type | Key Role | Semantic Description | Reference/Classification |
|---|---|---|---|---|
| `tax_account_id` | UUID | PK | System-generated identifier for one taxpayer, tax type, and jurisdiction account. It is not the taxpayer's public registration number. | Restricted identifier |
| `taxpayer_id` | UUID | FK | Identifier of the person or organization that owns the tax account. | Joins `tax_core.party.taxpayer.taxpayer_id`; restricted identifier |
| `tax_type_cd` | VARCHAR(30) | FK | Exact code identifying the tax program administered through the account. | `tax_reference.tax_type.tax_type_cd` |
| `jurisdiction_cd` | VARCHAR(20) | FK | Jurisdiction responsible for administering the account. | `tax_reference.jurisdiction.jurisdiction_cd` |
| `account_status_cd` | VARCHAR(20) | FK | Current operating status of the account. This is not a historical status event. | `tax_reference.account_status.account_status_cd` |
| `filing_frequency_cd` | VARCHAR(20) | FK | Current expected return filing cadence. Historical obligations retain their own applicable frequency. | `tax_reference.filing_frequency.filing_frequency_cd` |
| `opened_dt` | DATE | None | Calendar date on which the tax account became active in the jurisdiction. | Internal |
| `closed_dt` | DATE | None | Calendar date on which the account ceased operating. Null while the account remains open. | Internal |

## 3. Relationships and Joins

- `tax_core.party.taxpayer`: `tax_core.account.tax_account.taxpayer_id` = `tax_core.party.taxpayer.taxpayer_id` (Many-to-One).
- `tax_reference.tax_type`: `tax_core.account.tax_account.tax_type_cd` = `tax_reference.tax_type.tax_type_cd` (Many-to-One); apply the reference row effective on the business date when descriptions are historical.
- `tax_reference.jurisdiction`: `tax_core.account.tax_account.jurisdiction_cd` = `tax_reference.jurisdiction.jurisdiction_cd` (Many-to-One).

## 4. Reference Data and Valid Values

| Column | Reference Table | Exact Example Values | Effective-Date Rule | Meaning |
|---|---|---|---|---|
| `account_status_cd` | `tax_reference.account_status` | `ACTIVE`, `SUSPENDED`, `CLOSED` | Use the reference row active on the reporting date. | Current ability of the account to operate. |
| `filing_frequency_cd` | `tax_reference.filing_frequency` | `MONTHLY`, `QUARTERLY`, `ANNUAL` | Use the account's current value only for current-state questions. | Expected filing cadence. |

## 5. Query and Aggregation Rules

- Filter `account_status_cd = 'ACTIVE'` only when the question explicitly asks for currently active accounts.
- Do not infer historical status from the current `account_status_cd`.
- Join by `tax_account_id` when a downstream table provides it; do not reconstruct the account from taxpayer and tax type unless the governed relationship requires it.
- Include jurisdiction when comparing registration or filing behavior across tax administrations.

## 6. Safe Sample Data

| `tax_account_id` | `tax_type_cd` | `jurisdiction_cd` | `account_status_cd` | `filing_frequency_cd` |
|---|---|---|---|---|
| `00000000-0000-4000-8000-000000000001` | `INCOME_TAX` | `US-EXAMPLE` | `ACTIVE` | `ANNUAL` |
| `00000000-0000-4000-8000-000000000002` | `SALES_TAX` | `US-EXAMPLE` | `SUSPENDED` | `QUARTERLY` |

## 7. Known Confusions

- `tax_core.account.tax_account_status_history`: Contains effective-dated status history; use it for point-in-time account status.
- `tax_finance.ledger.account_balance`: Contains calculated financial balances; use it for amounts owed or available credits.
- `tax_filing.obligation.filing_obligation`: Contains expected returns by tax period; use it for filing compliance.

## 8. Validated Question Examples

- Which income-tax accounts are currently active?
- What filing frequency is assigned to this sales-tax account?
- Which tax accounts belong to this taxpayer in the selected jurisdiction?
```

## 9. Reference-table example

```markdown
---
table_name: "tax_reference.account_status"
domain: "Reference Data"
tax_types: ["ALL"]
jurisdictions: ["ALL"]
tags: ["account status", "reference code", "active account", "closed account"]
granularity: "One effective-dated definition for one tax-account status code"
temporal_behavior: "Effective-dated history"
data_classification: "Internal"
---

## 1. Semantic Boundaries

**Primary Intent:** Defines the allowed tax-account status codes and their business descriptions over time.

### USE THIS TABLE FOR

- Translating an account status code into its governed description.
- Determining whether a code was valid on a specified business date.
- Identifying which status codes represent operational or closed accounts.

### DO NOT USE THIS TABLE FOR

- Finding the current status of a taxpayer's account; use `tax_core.account.tax_account`.
- Reconstructing an account's status history; use `tax_core.account.tax_account_status_history`.

## 2. Schema Definition

| Column Name | Data Type | Key Role | Semantic Description | Reference/Classification |
|---|---|---|---|---|
| `account_status_cd` | VARCHAR(20) | PK | Exact status code stored on account records. | Internal code |
| `effective_dt` | DATE | PK | First calendar date on which this definition is valid. | Internal |
| `expiration_dt` | DATE | None | Last calendar date on which this definition is valid. Null means no scheduled expiration. | Internal |
| `status_desc` | VARCHAR(200) | None | Governed business description displayed to users. | Internal |
| `operational_ind` | CHAR(1) | None | `Y` when accounts in this status may perform normal filing and payment activity; otherwise `N`. | Internal enum |

## 3. Relationships and Joins

- `tax_core.account.tax_account`: `tax_core.account.tax_account.account_status_cd` = `tax_reference.account_status.account_status_cd` (One-to-Many); select the reference row effective on the relevant business date.

## 4. Reference Data and Valid Values

| Column | Reference Table | Exact Example Values | Effective-Date Rule | Meaning |
|---|---|---|---|---|
| `account_status_cd` | Self-defining | `ACTIVE`, `SUSPENDED`, `CLOSED` | `business_date >= effective_dt AND business_date <= COALESCE(expiration_dt, business_date)` | Governed account status. |
| `operational_ind` | Self-defining | `Y`, `N` | Same effective-date rule as the status row. | Whether normal account activity is permitted. |

## 5. Query and Aggregation Rules

- Apply an effective-date predicate whenever a historical business date is available.
- Do not join only on `account_status_cd` when multiple effective versions can exist.
- Do not treat `operational_ind = 'N'` as equivalent to `CLOSED`; suspended statuses may also be non-operational.

## 6. Safe Sample Data

| `account_status_cd` | `effective_dt` | `expiration_dt` | `status_desc` | `operational_ind` |
|---|---|---|---|---|
| `ACTIVE` | `2020-01-01` | null | `Active` | `Y` |
| `SUSPENDED` | `2020-01-01` | null | `Suspended` | `N` |
| `CLOSED` | `2020-01-01` | null | `Closed` | `N` |

## 7. Known Confusions

- `tax_core.account.tax_account`: Stores the status assigned to a specific account, not the definition of the code.
- `tax_core.account.tax_account_status_history`: Stores account-specific status changes over time.

## 8. Validated Question Examples

- What does the account status code `SUSPENDED` mean?
- Which account statuses were valid on the reporting date?
- Which statuses prevent normal filing activity?
```

## 10. Embedding and chunking instructions

For each completed table profile:

1. Create one routing chunk containing:
   - Frontmatter
   - Primary intent
   - Granularity
   - USE and DO NOT USE boundaries
   - Known confusions
   - Validated question examples
2. Create one or more detail chunks containing:
   - Schema definition
   - Relationships
   - Reference values
   - Query and aggregation rules
3. Attach the same `table_name` metadata to every chunk from the profile.
4. Attach domain, tax type, jurisdiction, temporal behavior, and data classification metadata.
5. Retrieve routing chunks first.
6. Retrieve detail chunks only after selecting candidate tables.
7. Rerank candidate tables using the full user question and explicit semantic boundaries.
8. Retrieve validated query examples separately when available.

Do not embed an entire multi-table catalog as one vector. Do not split a table profile into anonymous chunks that lose the table name.

## 11. Completion checklist

Do not publish or embed a table profile until all statements below are true:

- [ ] The fully qualified table name is correct.
- [ ] The profile states exactly what one row represents.
- [ ] Tax type and jurisdiction scope are explicit.
- [ ] Temporal behavior is explicit.
- [ ] Data classification is explicit.
- [ ] Primary intent is one concise business statement.
- [ ] At least two valid use cases are documented.
- [ ] At least two realistic exclusions are documented.
- [ ] Nearby confusing tables are named.
- [ ] Every queryable column is documented.
- [ ] Abbreviations are expanded.
- [ ] Amount units and sign conventions are explicit.
- [ ] Date meanings and time zones are explicit.
- [ ] Coded columns identify their reference tables.
- [ ] Effective-dated joins include their date predicates.
- [ ] Composite, jurisdiction, or tenant join conditions are complete.
- [ ] Current-state and historical tables are distinguished.
- [ ] Version-selection and deduplication rules are explicit.
- [ ] Exact enum values come from authoritative sources.
- [ ] Samples contain no real taxpayer or account data.
- [ ] No join or business meaning was inferred without evidence.
- [ ] No placeholder remains.
- [ ] A routing agent can explain why this table is better than its nearest alternatives.

## 12. Final standard

A good semantic profile must allow an agent to answer four questions before it writes SQL:

1. Is this the correct table for the user's business question?
2. What exactly does one row represent?
3. Which filters, versions, effective dates, and joins are required for correctness?
4. Which similar table should be used instead when this table is wrong?

If the profile cannot answer all four questions, it is incomplete.
