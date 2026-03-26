---
name: amcos-skill-management
description: Use when validating skill directory structure, reindexing skills for Perfect Skill Suggester, or managing skill activation and discovery. Trigger with skill validation, indexing, or update requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to skill directories, skills-ref validator, and Perfect Skill Suggester (PSS) if using reindexing features. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff - Skill Management Skill

## Overview

Skill management enables the Chief of Staff to validate, index, and maintain agent skills across plugins and projects. Covers skill directory validation, PSS reindexing, and skill discovery optimization.

## Prerequisites

1. Skill validation scripts are available
2. PSS (Perfect Skill Suggester) is configured if reindexing
3. Skill directories are accessible

## Instructions

1. Identify skill operation needed (validate, reindex, update)
2. Execute the operation
3. Verify skill integrity
4. Notify agents of skill changes

Copy this checklist and track your progress:

- [ ] Confirm skill directory exists and contains SKILL.md
- [ ] Run skills-ref validate and check YAML frontmatter
- [ ] Verify PSS index reflects current skill state
- [ ] Notify affected agents of any skill changes

## Output

| Operation | Output |
|-----------|--------|
| Validate | Validation report with issues |
| Reindex | PSS index updated |
| Update | Skill content modified, agents notified |

## Core Procedures

### PROCEDURE 1: Validate Skill Structure

**When/Steps:** Run skills-ref validate, check YAML frontmatter, verify references, confirm TOC accuracy.

See [skill-validation](references/skill-validation.md) — Topics: Skill Validation Reference, Table of Contents, 1.2 Validation requirements

### PROCEDURE 2: Reindex Skills for PSS

**When/Steps:** Run pss-reindex-skills, verify index updated, test skill discovery.

See [skill-reindexing](references/skill-reindexing.md) — Topics: Skill Reindexing Reference, Table of Contents, 2.2 When to reindex

### PROCEDURE 3: Configure PSS Integration

**When/Steps:** Review descriptions, add keywords, configure weights, test discovery.

See [pss-integration](references/pss-integration.md) — Topics: PSS Integration Reference, Table of Contents, 3.2 How PSS works

### Generate Agent Prompt XML

Use skills-ref to-prompt to generate available_skills XML blocks for agent prompt definitions.

See [op-generate-agent-prompt-xml](references/op-generate-agent-prompt-xml.md) — Topics: Generate Agent Prompt XML, Contents, When to Use

## Examples

**Input:** `skills-ref validate skills/amcos-onboarding/`

**Output:** `PASS: SKILL.md frontmatter valid, 3 references found, TOC consistent`

See [skill-overview-and-examples](references/skill-overview-and-examples.md) — Topics: Skill Management - Overview, Examples, and Reference, Table of Contents, What Is Skill Management

## Error Handling

| Issue | Resolution |
|-------|------------|
| Skill validation fails | See [skill-validation](references/skill-validation.md) — Topics: Skill Validation Reference, Table of Contents, 1.2 Validation requirements
| Skill not in PSS suggestions | See [skill-reindexing](references/skill-reindexing.md) — Topics: Skill Reindexing Reference, Table of Contents, 2.2 When to reindex
| Poor keyword matching | See [pss-integration](references/pss-integration.md) — Topics: PSS Integration Reference, Table of Contents, 3.2 How PSS works

## Resources

- [skill-validation](references/skill-validation.md) — Topics: Skill Validation Reference, Table of Contents, 1.2 Validation requirements

---

**Version:** 1.0
**Last Updated:** 2025-02-01
