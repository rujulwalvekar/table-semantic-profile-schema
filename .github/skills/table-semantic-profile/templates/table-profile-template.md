---
table_name: "[schema].[table_name]"
domain: "[business domain]"
tags: ["[tag1]", "[tag2]", "[tag3]"]
granularity: "[What one row represents]"
---

## 1. Semantic Boundaries

**Primary Intent:** [One concise sentence explaining what this table represents in the business.]

### ✅ USE THIS TABLE FOR:

- [Specific query intent 1.]
- [Specific query intent 2.]

### ❌ DO NOT USE THIS TABLE FOR:

- [Realistic anti-pattern 1; name the correct alternative table when known.]
- [Realistic anti-pattern 2; name the correct alternative table when known.]

## 2. Schema Definition

| Column Name | Data Type | Primary/Foreign Key | Semantic Description |
|---|---|---|---|
| `[column_1]` | `[physical type]` | `[PK, FK, PK/FK, or None]` | [Business meaning, expanded abbreviation, units, and relevant inclusions or exclusions.] |
| `[column_2]` | `[physical type]` | `[PK, FK, PK/FK, or None]` | [Business meaning, null semantics, time zone, or derivation when relevant.] |

## 3. Relationships & Joins

- `[fully qualified target table]`: `[fully qualified source table].[source column]` = `[fully qualified target table].[target column]` ([Many-to-One/One-to-Many/One-to-One])

## 4. Sample Values (Categorical/Enums)

| `[identifier_or_context_column]` | `[categorical_column_1]` | `[categorical_column_2]` |
|---|---|---|
| `[synthetic or safe representative value]` | `[EXACT_STORED_VALUE]` | `[EXACT_STORED_VALUE]` |
| `[synthetic or safe representative value]` | `[EXACT_STORED_VALUE]` | `[EXACT_STORED_VALUE]` |
| `[synthetic or safe representative value]` | `[EXACT_STORED_VALUE]` | `[EXACT_STORED_VALUE]` |
