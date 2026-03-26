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

### Checklist

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

### PROCEDURE 2: Reindex Skills for PSS

**When/Steps:** Run pss-reindex-skills, verify index updated, test skill discovery.

### PROCEDURE 3: Configure PSS Integration

**When/Steps:** Review descriptions, add keywords, configure weights, test discovery.

### Generate Agent Prompt XML

Use skills-ref to-prompt to generate available_skills XML blocks for agent prompt definitions.

See op-generate-agent-prompt-xml in Resources

## Examples

**Input:** Validate an onboarding skill directory

```bash
skills-ref validate skills/amcos-onboarding/
```

**Expected result:** `PASS: SKILL.md frontmatter valid, 3 references found, TOC consistent`

## Error Handling

| Issue | Resolution |
|-------|------------|

## Resources

- [op-generate-agent-prompt-xml](references/op-generate-agent-prompt-xml.md) — Generate XML prompt
  - When to Use
  - Prerequisites
  - Procedure
    - Step 1: Identify Skills to Include
    - Step 2: Generate XML with skills-ref
    - Step 3: Save to File (Optional)
    - Step 4: Integrate into Agent Prompt
    - Step 5: Verify Integration
  - Checklist
  - Examples
    - Example: Generate XML for AMCOS Skills
    - Example: Save and Use in Agent Definition
    - Example: Programmatic Generation
    - Example: Dynamic Skill List
  - Error Handling
  - Related Operations
