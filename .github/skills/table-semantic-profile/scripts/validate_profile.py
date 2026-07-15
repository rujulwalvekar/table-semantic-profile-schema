#!/usr/bin/env python3
"""Validate a generated table semantic profile using only Python stdlib."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_KEYS = ("table_name", "domain", "tags", "granularity")
REQUIRED_H2 = (
    "## 1. Semantic Boundaries",
    "## 2. Schema Definition",
    "## 3. Relationships & Joins",
    "## 4. Sample Values (Categorical/Enums)",
)
SCHEMA_HEADER = "| Column Name | Data Type | Primary/Foreign Key | Semantic Description |"
SCHEMA_DIVIDER = "|---|---|---|---|"
PLACEHOLDER = re.compile(r"\[[^\]\n]+\]")


def section(text: str, start: str, end: str | None) -> str:
    start_at = text.index(start) + len(start)
    end_at = text.index(end, start_at) if end else len(text)
    return text[start_at:end_at]


def table_rows(block: str) -> list[list[str]]:
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    rows: list[list[str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        return ["Profile must begin at byte zero with YAML frontmatter (`---`)."]

    close = text.find("\n---\n", 4)
    if close < 0:
        return ["YAML frontmatter is missing its closing `---` delimiter."]

    frontmatter = text[4:close]
    body = text[close + 5 :]
    parsed: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([a-z_]+):\s*(.+)$", line)
        if not match:
            errors.append(f"Invalid frontmatter line: {line!r}")
            continue
        parsed[match.group(1)] = match.group(2).strip()

    missing = [key for key in REQUIRED_KEYS if key not in parsed]
    extra = [key for key in parsed if key not in REQUIRED_KEYS]
    if missing:
        errors.append(f"Missing frontmatter keys: {', '.join(missing)}")
    if extra:
        errors.append(f"Unexpected frontmatter keys: {', '.join(extra)}")

    table_name = parsed.get("table_name", "").strip('"\'')
    if table_name and ("." not in table_name or any(char.isspace() for char in table_name)):
        errors.append("`table_name` must be a fully qualified physical name such as `public.fact_orders`.")

    tags = parsed.get("tags", "")
    if tags and not re.fullmatch(r"\[[^\]]+\]", tags):
        errors.append("`tags` must be a non-empty YAML inline list.")

    h2 = re.findall(r"^## .+$", body, flags=re.MULTILINE)
    if tuple(h2) != REQUIRED_H2:
        errors.append("Required H2 headers must appear exactly once and in the specified order.")

    for header in REQUIRED_H2:
        if body.count(header) != 1:
            errors.append(f"Header must appear exactly once: {header}")

    if "TEMPLATE_START" in text or "TEMPLATE_END" in text or "```" in text:
        errors.append("Generated profiles must not contain template markers or code fences.")

    placeholders = PLACEHOLDER.findall(body)
    for key in ("table_name", "domain", "granularity"):
        value = parsed.get(key, "")
        if "[" in value or "]" in value:
            placeholders.append(value)
    if tags:
        tag_values = [value.strip().strip('"\'') for value in tags.strip("[]").split(",")]
        placeholders.extend(value for value in tag_values if "[" in value or "]" in value)
    if placeholders:
        errors.append(f"Unresolved placeholders remain: {', '.join(placeholders[:5])}")

    if "**Primary Intent:**" not in body:
        errors.append("Semantic Boundaries must include `**Primary Intent:**`.")
    if "### ✅ USE THIS TABLE FOR:" not in body:
        errors.append("Semantic Boundaries must include the exact USE heading.")
    if "### ❌ DO NOT USE THIS TABLE FOR:" not in body:
        errors.append("Semantic Boundaries must include the exact DO NOT USE heading.")

    if all(header in body for header in REQUIRED_H2):
        boundaries = section(body, REQUIRED_H2[0], REQUIRED_H2[1])
        use_match = re.search(
            r"### ✅ USE THIS TABLE FOR:\s*(.*?)\s*### ❌ DO NOT USE THIS TABLE FOR:\s*(.*)",
            boundaries,
            flags=re.DOTALL,
        )
        if use_match:
            use_count = len(re.findall(r"^- ", use_match.group(1), flags=re.MULTILINE))
            avoid_count = len(re.findall(r"^- ", use_match.group(2), flags=re.MULTILINE))
            if use_count < 2:
                errors.append("Include at least two concrete USE intents.")
            if avoid_count < 2:
                errors.append("Include at least two concrete DO NOT USE boundaries.")

        schema = section(body, REQUIRED_H2[1], REQUIRED_H2[2])
        if SCHEMA_HEADER not in schema or SCHEMA_DIVIDER not in schema:
            errors.append("Schema Definition must use the exact four-column Markdown table header.")
        schema_rows = table_rows(schema)
        if not schema_rows:
            errors.append("Schema Definition must contain at least one column row.")
        elif any(len(row) != 4 for row in schema_rows):
            errors.append("Every Schema Definition row must contain exactly four cells.")

        joins = section(body, REQUIRED_H2[2], REQUIRED_H2[3])
        if "No verified joins are documented for this table." not in joins:
            join_lines = re.findall(r"^- `[^`]+`:\s+`[^`]+`\s+=\s+`[^`]+`\s+\([^)]+\)$", joins, flags=re.MULTILINE)
            if not join_lines:
                errors.append("Document at least one fully specified join or use the exact no-verified-joins sentence.")

        samples = section(body, REQUIRED_H2[3], None)
        sample_rows = table_rows(samples)
        if not 3 <= len(sample_rows) <= 5:
            errors.append("Sample Values must contain 3–5 representative data rows.")
        if sample_rows and len({len(row) for row in sample_rows}) != 1:
            errors.append("Every Sample Values row must contain the same number of cells.")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_profile.py path/to/profile.md", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    errors = validate(path)
    if errors:
        print(f"FAIL: {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
