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

### PROCEDURE 2: Reindex Skills for PSS

**When/Steps:** Run pss-reindex-skills, verify index updated, test skill discovery.

### PROCEDURE 3: Configure PSS Integration

**When/Steps:** Review descriptions, add keywords, configure weights, test discovery.

### Generate Agent Prompt XML

Use skills-ref to-prompt to generate available_skills XML blocks for agent prompt definitions.

See [op-generate-agent-prompt-xml](references/op-generate-agent-prompt-xml.md) — Topics: Generate Agent Prompt XML, Contents, When to Use, Prerequisites, Procedure, Step 1: Identify Skills to Include, List available skills, Or list skills in a plugin, Step 2: Generate XML with skills-ref, Step 3: Save to File (Optional), Step 4: Integrate into Agent Prompt, Agent System Prompt, Step 5: Verify Integration, Checklist, Examples, Example: Generate XML for AMCOS Skills, Generate for all AMCOS skills, Output:, <available_skills>, <skill>, <name>amcos-agent-spawning</name>, <description>Use when spawning, terminating, hibernating, or waking agents...</description>, <location>/path/to/skills/amcos-agent-spawning/SKILL.md</location>, </skill>, ..., </available_skills>, Example: Save and Use in Agent Definition, Generate and save, View result, Use in agent definition file, AMCOS Main Agent, Example: Programmatic Generation, Generate prompt for skills, Save to file, Example: Dynamic Skill List, Generate for all skills in a plugin dynamically, Build command, Execute, Error Handling, Related Operations

## Examples

**Input:** `skills-ref validate skills/amcos-onboarding/`

**Output:** `PASS: SKILL.md frontmatter valid, 3 references found, TOC consistent`

See [skill-overview-and-examples](references/skill-overview-and-examples.md) — Topics: Skill Management - Overview, Examples, and Reference, Table of Contents, What Is Skill Management, Skill Architecture Diagram, Skill Components, Examples: Validating a Skill, Install skills-ref if not present, Validate a skill directory, Expected output for valid skill, Skill: my-skill, Status: VALID, Warnings: 0, Errors: 0, Read skill properties, Examples: SKILL.md Frontmatter, Examples: Triggering PSS Reindex, Using PSS slash command, Or via script, Verify index updated, Examples: Generating Agent Prompt XML, Generate available_skills XML for agent prompts, Output, <available_skills>, <skill>, <name>skill-a</name>, <description>What skill-a does</description>, <location>/path/to/skill-a/SKILL.md</location>, </skill>, ..., </available_skills>, Key Takeaways, Task Checklist

## Error Handling

| Issue | Resolution |
|-------|------------|

## Resources

---

**Version:** 1.0
**Last Updated:** 2025-02-01
