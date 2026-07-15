# Table Semantic Profile skill

A reusable GitHub Copilot agent skill for generating strict database table profiles used by RAG-based table discovery and text-to-SQL routing.

The skill tells an agent how to document table grain, business intent, valid and invalid query use cases, complete column semantics, joins, and exact categorical values without inventing database facts.

## Canonical instruction file

- [SKILL.md](.github/skills/table-semantic-profile/SKILL.md)
- [Profile template](.github/skills/table-semantic-profile/templates/table-profile-template.md)
- [Validated example](.github/skills/table-semantic-profile/references/example-profile.md)
- [Structural validator](.github/skills/table-semantic-profile/scripts/validate_profile.py)

Direct download:

https://raw.githubusercontent.com/rujulwalvekar/table-semantic-profile-schema/main/.github/skills/table-semantic-profile/SKILL.md

## Install as a project skill

Copy the skill directory into a target repository:

```bash
mkdir -p .github/skills
cp -R /path/to/table-semantic-profile-schema/.github/skills/table-semantic-profile .github/skills/
```

GitHub Copilot can load project skills from `.github/skills`, `.claude/skills`, or `.agents/skills`. See GitHub's official [agent skills documentation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-copilot-coding-agent/add-agent-skills).

## Install as a personal Copilot skill

```bash
mkdir -p ~/.copilot/skills
cp -R /path/to/table-semantic-profile-schema/.github/skills/table-semantic-profile ~/.copilot/skills/
```

GitHub Copilot can then use the skill across local projects when the task matches the skill description.

## Use as repository-wide instructions

The repository also includes `.github/copilot-instructions.md`. Copy it into another repository if every table-profile task in that repository should be routed to this skill.

## Generate a profile

Give Copilot authoritative inputs such as:

- DDL or catalog output
- Column comments and governed definitions
- Verified joins and cardinality
- Domain-owner notes
- Safely sampled categorical values
- Nearby tables that are easy to confuse

Then ask:

> Generate a semantic profile for this table using the `table-semantic-profile` skill. Do not infer missing business facts. Ask for missing required metadata before producing the final profile.

## Validate a profile

```bash
python3 .github/skills/table-semantic-profile/scripts/validate_profile.py path/to/profile.md
```

The validator checks structural requirements. A human or domain owner must still confirm business meaning, grain, joins, units, and enum values.

## Contract

A valid profile:

- Begins with strict YAML frontmatter
- Uses the four required H2 sections in order
- States both positive and negative routing boundaries
- Documents every queryable physical column
- Specifies copyable joins and cardinality
- Includes 3–5 rows of exact categorical values
- Contains no placeholders, fabricated values, or conversational filler
