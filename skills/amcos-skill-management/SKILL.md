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

See `references/skill-validation.md` and `references/op-validate-skill.md`.

### PROCEDURE 2: Reindex Skills for PSS

**When/Steps:** Run pss-reindex-skills, verify index updated, test skill discovery.

See `references/skill-reindexing.md` and `references/op-reindex-skills-pss.md`.

### PROCEDURE 3: Configure PSS Integration

**When/Steps:** Review descriptions, add keywords, configure weights, test discovery.

See `references/pss-integration.md` and `references/op-configure-pss-integration.md`.

### Generate Agent Prompt XML

Use skills-ref to-prompt to generate available_skills XML blocks for agent prompt definitions.

See `references/op-generate-agent-prompt-xml.md`.

## Examples

**Input:** `skills-ref validate skills/amcos-onboarding/`

**Output:** `PASS: SKILL.md frontmatter valid, 3 references found, TOC consistent`

See `references/skill-overview-and-examples.md` for full examples including validation, frontmatter format, PSS reindex, and XML generation.

## Error Handling

| Issue | Resolution |
|-------|------------|
| Skill validation fails | See `references/skill-validation.md` Section 1.7 |
| Skill not in PSS suggestions | See `references/skill-reindexing.md` Section 2.7 |
| Poor keyword matching | See `references/pss-integration.md` Section 3.7 |

## Resources

- `references/skill-validation.md`
- `references/skill-reindexing.md`
- `references/pss-integration.md`
- `references/validation-procedures.md`
- `references/skill-overview-and-examples.md`
- `references/op-validate-skill.md`
- `references/op-reindex-skills-pss.md`
- `references/op-generate-agent-prompt-xml.md`
- `references/op-configure-pss-integration.md`

---

**Version:** 1.0
**Last Updated:** 2025-02-01
