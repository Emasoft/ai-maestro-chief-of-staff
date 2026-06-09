---
name: amcos-skill-management-ref
description: Use when consulting detailed skill management references. Trigger with skill management lookups. Loaded by ai-maestro-chief-of-staff-main-agent
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
  - 3.1 What is PSS integration - AI-analyzed skill activation
  - 3.2 How PSS works - Discovery algorithm
    - 3.2.1 Index as superset - All skills indexed
    - 3.2.2 Agent filtering - Available skills filter
    - 3.2.3 Weighted scoring - Keyword relevance
  - 3.3 Integration procedure - Optimizing for PSS
    - 3.3.1 Description optimization - Clear use cases
    - 3.3.2 Keyword embedding - Natural keyword inclusion
    - 3.3.3 Co-usage hints - Related skill references
  - 3.4 Categories vs keywords - Understanding the difference
    - 3.4.1 Categories (16) - Fields of competence
    - 3.4.2 Keywords - Tools, actions, concepts
  - 3.5 Testing discovery - Verifying activation
  - 3.6 Examples - PSS integration scenarios
  - 3.7 Troubleshooting - Discovery issues
- [skill-reindexing](references/skill-reindexing.md) — When to reindex, two-pass generation, verification, examples
  - 2.1 What is skill reindexing - Updating PSS index
  - 2.2 When to reindex - Reindexing triggers
    - 2.2.1 New skills added - Fresh skills need indexing
    - 2.2.2 Skills modified - Content changes need re-extraction
    - 2.2.3 Keywords stale - Suggestions not matching
  - 2.3 Reindexing procedure - Step-by-step reindexing
    - 2.3.1 Trigger reindex - Running the command
    - 2.3.2 Index generation - Two-pass extraction
    - 2.3.3 Verification - Confirming index updated
    - 2.3.4 Testing - Checking skill discovery
  - 2.4 Two-pass generation - How indexing works
    - 2.4.1 Pass 1 - Factual data extraction
    - 2.4.2 Pass 2 - AI co-usage relationships
  - 2.5 Index structure - What gets indexed
  - 2.6 Examples - Reindexing scenarios
  - 2.7 Troubleshooting - Reindexing issues
- [skill-validation](references/skill-validation.md) — Validation requirements, frontmatter fields, references check, examples
  - 1.1 What is skill validation - Checking skill correctness
  - 1.2 Validation requirements - Agent Skills specification
    - 1.2.1 Directory structure - Required layout
    - 1.2.2 SKILL.md format - Frontmatter and content
    - 1.2.3 References structure - Reference file format
  - 1.3 Validation procedure - Step-by-step validation
    - 1.3.1 Using skills-ref - CLI validation tool
    - 1.3.2 Frontmatter check - YAML syntax and fields
    - 1.3.3 References check - File existence and links
    - 1.3.4 TOC verification - Heading accuracy
  - 1.4 Required frontmatter fields - Mandatory YAML fields
    - 1.4.1 name - Skill identifier
    - 1.4.2 description - Use case description
    - 1.4.3 license - License identifier
    - 1.4.4 compatibility - Requirements
  - 1.5 Optional Claude Code fields - Extended metadata
    - 1.5.1 context - Fork behavior (value: fork)
    - 1.5.2 agent - Target agent types
    - 1.5.3 user-invocable - Direct user activation
  - 1.6 Examples - Validation scenarios
  - 1.7 Troubleshooting - Validation issues
