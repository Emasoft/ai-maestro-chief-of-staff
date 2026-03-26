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

## Examples

See referenced files for step-by-step examples.

## Resources

- [pss-integration](references/pss-integration.md) — Topics: PSS Integration Reference, Table of Contents, 3.1 What is PSS integration, 3.2 How PSS works, 3.2.1 Index as superset, 3.2.2 Agent filtering, 3.2.3 Weighted scoring, 3.3 Integration procedure, 3.3.1 Description optimization, 3.3.2 Keyword embedding, PROCEDURE 1: Assess Role Requirements, PROCEDURE 2: Plan Agent Capacity, PROCEDURE 3: Create Staffing Templates, 3.3.3 Co-usage hints, Related Skills, 3.4 Categories vs keywords, 3.4.1 Categories (16), 3.4.2 Keywords, 3.5 Testing discovery, Test 1: Direct PSS Query, Using PSS command, Expected: amcos-staff-planning in results, Test 2: Check Index Entry, Verify skill is indexed, Check keywords, Test 3: Category Mapping, Check skill appears in expected category, Should include: "amcos-staff-planning", Test 4: Negative Test, Skill should NOT appear for unrelated queries, amcos-staff-planning should NOT be in results, 3.6 Examples, Example 1: Optimizing Description, Example 2: Adding Keyword Headings, Step 1, Step 2, Step 3, PROCEDURE 1: Assess Role Requirements, PROCEDURE 2: Plan Agent Capacity, PROCEDURE 3: Create Staffing Templates, Example 3: Category Alignment, ["orchestration", "planning", "lifecycle"], 3.7 Troubleshooting, Issue: Skill not suggested for expected query, Issue: Skill suggested for wrong queries, Issue: Category mismatch, Issue: Co-usage not working, Issue: Low relevance score
- [skill-reindexing](references/skill-reindexing.md) — Topics: Skill Reindexing Reference, Table of Contents, 2.1 What is skill reindexing, 2.2 When to reindex, 2.2.1 New skills added, 2.2.2 Skills modified, 2.2.3 Keywords stale, 2.3 Reindexing procedure, 2.3.1 Trigger reindex, 2.3.2 Index generation, 2.3.3 Verification, Check index file timestamp, Check skill count, Check specific skill, 2.3.4 Testing, Use PSS status command, Or query directly, 2.4 Two-pass generation, 2.4.1 Pass 1 - Factual data extraction, 2.4.2 Pass 2 - AI co-usage relationships, 2.5 Index structure, 2.6 Examples, Example 1: Reindex After Adding Skills, Add new skills, Trigger reindex, Verify new skills indexed, Should show increased count, Test discovery, Example 2: Force Full Reindex, Remove old index, Regenerate from scratch, Verify, Example 3: Reindex Specific Plugin Skills, Reindex only Chief of Staff skills, Verify, 2.7 Troubleshooting, Issue: Reindex produces empty index, Issue: Skills missing from index, Issue: Keywords not matching expectations, Issue: Index file permissions, Issue: Pass 2 fails
- [skill-validation](references/skill-validation.md) — Topics: Skill Validation Reference, Table of Contents, 1.1 What is skill validation, 1.2 Validation requirements, 1.2.1 Directory structure, 1.2.2 SKILL.md format, Skill Title, 1.2.3 References structure, 1.3 Validation procedure, 1.3.1 Using skills-ref, Validate single skill, Output, 1.3.2 Frontmatter check, Extract and validate frontmatter, 1.3.3 References check, Find all reference links in SKILL.md, 1.3.4 TOC verification, Extract TOC from reference file, Compare with actual headings, 1.4 Required frontmatter fields, 1.4.1 name, 1.4.2 description, 1.4.3 license, 1.4.4 compatibility, 1.5 Optional Claude Code fields, 1.5.1 context, 1.5.2 agent, 1.5.3 user-invocable, 1.6 Examples, Example 1: Valid Skill, Example 2: Invalid Skill (Missing Fields), Example 3: Generating Prompt XML, Generate available_skills XML for agent prompts, Output, 1.7 Troubleshooting, Issue: YAML parse error, Issue: Missing description, Issue: Invalid license, Issue: References not found, Issue: Claude Code fields cause warnings
