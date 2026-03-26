---
name: amcos-skill-management-ref
description: Use when consulting detailed skill management references. Trigger with skill management lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Skill Management Reference

## Overview

Reference material for skill management. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-skill-management` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-skill-management` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Validate a skill directory and reindex for PSS"

```bash
cat references/skill-validation.md | head -50
```

**Expected result:** Validation procedure checking directory structure, SKILL.md frontmatter, references, and TOC consistency.

## Resources

- [pss-integration](references/pss-integration.md) — PSS integration, description optimization, keywords, categories, testing discovery
- [skill-reindexing](references/skill-reindexing.md) — When to reindex, two-pass generation, verification, examples
- [skill-validation](references/skill-validation.md) — Validation requirements, frontmatter fields, references check, examples
