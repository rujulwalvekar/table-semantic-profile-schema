---
name: table-semantic-profile
description: Use when generating or validating database table semantic profiles for RAG-based table discovery and SQL routing. Produce strict YAML metadata, fixed semantic sections, complete column semantics, explicit join guidance, and representative categorical values without inventing database facts.
---

# Generate table semantic profiles

## Objective

Generate one precise Markdown profile per database table. Make the profile reliable enough for a retrieval system to select the correct table and reject plausible but incorrect alternatives.

Treat wrong semantic guidance as worse than missing guidance. Never invent table purpose, grain, joins, column meanings, units, enum values, or alternative tables.

## Use this skill when

- Creating a semantic profile for a database table
- Converting DDL, catalog metadata, data dictionaries, or SME notes into a retrieval document
- Documenting which table should answer a business question
- Adding table-selection boundaries to a RAG or text-to-SQL system
- Validating an existing table profile against this repository's contract

Do not use this skill to:

- Generate SQL for a user question
- Document an entire database in one profile
- Describe dashboards, metrics, APIs, or files that are not database tables
- Guess undocumented business logic from column names alone

## Required inputs

Collect or inspect all of the following before writing the final profile:

1. Fully qualified physical table name
2. Business domain
3. One-row grain
4. Complete column list and physical data types
5. Primary and foreign keys
6. Business meaning of each column
7. Units, currencies, time zones, and inclusion/exclusion rules
8. Valid joins and relationship cardinality
9. Exact categorical or enum values from real data or authoritative documentation
10. Nearby tables that are easy to confuse with this table

If required information is unavailable:

- Ask for the missing metadata or inspect an authoritative source.
- Do not infer business meaning solely from a name such as `amt`, `status`, `type`, or `date`.
- Do not publish placeholder text as a completed profile.
- Do not create a join unless both columns and the relationship are verified.
- Do not fabricate sample values.

## Source precedence

Resolve conflicting information in this order:

1. Database constraints and catalog metadata for physical names, types, and keys
2. Governed data contracts or approved data dictionaries
3. Domain-owner or subject-matter-expert documentation
4. Production query patterns that have been validated by the data owner
5. Existing comments in DDL or transformation code
6. Naming conventions only as a lead for investigation, never as final evidence

Record uncertainty outside the final profile until it is resolved. The final profile must be declarative.

## Output contract

Generate only the profile. Do not add an introduction, explanation, validation report, code fence, `TEMPLATE_START`, or `TEMPLATE_END` around the generated profile.

The output must:

1. Begin at byte zero with YAML frontmatter delimited by `---`.
2. Include exactly these frontmatter keys:
   - `table_name`
   - `domain`
   - `tags`
   - `granularity`
3. Use a fully qualified value for `table_name`.
4. Preserve these H2 headers exactly and in this order:
   - `## 1. Semantic Boundaries`
   - `## 2. Schema Definition`
   - `## 3. Relationships & Joins`
   - `## 4. Sample Values (Categorical/Enums)`
5. Use a strict four-column Markdown table for schema definition.
6. Use a strict Markdown table for sample values.
7. Use exact physical table and column names in backticks.
8. Contain no unresolved bracket placeholders.
9. Contain no conversational filler.

Start from `templates/table-profile-template.md` and replace every placeholder.

## Generation procedure

### Step 1: Establish table identity

Write:

- `table_name` as `[schema].[table]`
- `domain` as the business area that owns the meaning of the data
- `tags` as 3–8 retrieval terms that describe business concepts, not implementation details
- `granularity` as one precise singular statement of what one row represents

A good grain names the entity, event/state, and relevant time or lifecycle boundary.

Good:

- `One finalized invoice per customer per billing cycle`
- `One inventory snapshot per SKU, warehouse, and calendar day`

Bad:

- `Invoice data`
- `Customer records`
- `Various inventory information`

Completion criterion: two rows cannot have different grains while still satisfying the sentence.

### Step 2: Define semantic boundaries

Write one concise `Primary Intent` sentence.

Under `### ✅ USE THIS TABLE FOR:` include at least two query intents that this table can answer directly or through documented joins.

Under `### ❌ DO NOT USE THIS TABLE FOR:` include at least two realistic confusion cases. For each case:

- State what must not be queried from this table.
- Name the correct alternative table when one is known.
- Explain the boundary briefly when the distinction is subtle.

Prioritize anti-patterns involving:

- Current state versus historical events
- Finalized versus pending records
- Transaction facts versus aggregates
- Customer identity versus customer activity
- Gross versus net values
- Booked versus recognized revenue
- Event time versus processing time
- Snapshot versus change-log tables

Completion criterion: a routing agent can explain why this table wins over its nearest alternatives.

### Step 3: Document every column

Use the exact schema table header:

| Column Name | Data Type | Primary/Foreign Key | Semantic Description |
|---|---|---|---|

For each queryable physical column:

- Preserve its exact name and case.
- Preserve its physical data type.
- Mark `PK`, `FK`, `PK/FK`, or `None`.
- Expand abbreviations.
- State the business meaning.
- State units or currency.
- State whether tax, discounts, refunds, or fees are included when relevant.
- State the time zone and timestamp event when relevant.
- State whether null has business meaning when relevant.
- State whether the value is derived, mutable, soft-deleted, or historical when relevant.

Do not restate the column name as its description.

Bad:

- `st_amt`: Settlement amount.

Good:

- `st_amt`: Final amount settled by the payment processor in USD after discounts and before tax. Null until settlement completes.

Completion criterion: a query author can use each column without reverse-engineering its abbreviation or unit.

### Step 4: Specify joins

Write each relationship as:

`[fully qualified target table]`: `[fully qualified source table].[source column]` = `[fully qualified target table].[target column]` (`[cardinality]`)

For every join:

- Use physical names.
- Include both columns.
- Include cardinality such as Many-to-One or One-to-Many.
- Include composite-key columns together when required.
- Mention additional predicates such as tenant, effective date, or active-version constraints when required for correctness.
- Do not describe an assumed join as valid.

If the table has no verified relationships, write:

`No verified joins are documented for this table.`

Completion criterion: the join can be copied into a query without guessing missing keys.

### Step 5: Add representative sample values

Include 3–5 representative rows from authoritative documentation or safely sampled data.

Prioritize columns used in filtering:

- Status
- Type
- Category
- Currency
- Region
- Channel
- Boolean flags
- Lifecycle state

Rules:

- Preserve exact case, spelling, punctuation, and whitespace semantics.
- Put string enum values in backticks.
- Do not normalize values such as `PAID` into `Paid`.
- Do not fabricate rows.
- Do not expose secrets or sensitive personal data.
- Replace sensitive identifiers with clearly synthetic values while preserving format.
- Do not include free-text customer content unless it is essential and safely anonymized.

Completion criterion: a query-generation agent knows the exact literals to use in filters.

### Step 6: Run validation

Run:

```bash
python3 scripts/validate_profile.py path/to/profile.md
```

Fix every error. Do not call the profile complete until the validator exits successfully and the semantic review checklist passes.

## Exact profile template

Use `templates/table-profile-template.md` as the source of truth. Do not rename sections or table columns.

## Semantic review checklist

After structural validation, verify manually:

- [ ] The table name is fully qualified and physically correct.
- [ ] The grain describes exactly one row.
- [ ] Tags improve retrieval and do not repeat irrelevant technical terms.
- [ ] The primary intent describes the business entity or event.
- [ ] Use cases are answerable from this table.
- [ ] Anti-patterns name the closest confusing tables.
- [ ] Every queryable column is documented.
- [ ] Abbreviations, units, currencies, and time semantics are explicit.
- [ ] Joins include both columns and correct cardinality.
- [ ] Composite or tenant-aware joins include all required predicates.
- [ ] Sample enum values match stored values exactly.
- [ ] No sensitive data appears in examples.
- [ ] No business facts were inferred without evidence.
- [ ] No placeholder remains.

## Common failure modes

### Describing contents instead of routing intent

Bad profiles say that a table "contains invoice information." Good profiles specify which invoice questions it answers and which invoice questions belong elsewhere.

### Omitting grain

Without grain, the agent may double-count entities or aggregate snapshots as events. Write grain before any other semantic prose.

### Inventing joins

Similar column names do not prove a relationship. Require a constraint, governed contract, validated query, or owner confirmation.

### Hiding units

`amount`, `duration`, `quantity`, and `date` are incomplete without currency, unit, time zone, and event semantics.

### Using fake sample values

Fabricated enums teach the query generator invalid filters. Use exact values or leave the profile incomplete until values are available.

### Writing weak anti-patterns

"Do not use for unrelated queries" adds no routing value. Name realistic confusion cases and the correct table.

### Changing the template

Do not rename H2 headers, convert tables to bullet lists, wrap output in a code fence, add narrative before frontmatter, or add arbitrary sections. The parser depends on the contract.

## Completion standard

A profile is complete only when:

1. The structural validator passes.
2. Every required input is supported by an authoritative source.
3. The nearest alternative tables are distinguished explicitly.
4. All queryable columns and valid joins are documented.
5. Categorical samples use exact database values.
6. A retrieval agent can choose this table and explain why competing tables are wrong.
