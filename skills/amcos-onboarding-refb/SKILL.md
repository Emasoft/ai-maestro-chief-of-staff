---
name: amcos-onboarding-refb
description: Use when consulting detailed onboarding references. Trigger with onboarding lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Onboarding Reference

## Overview

Reference material for onboarding. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-onboarding` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-onboarding` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Walk through the onboarding checklist for a new developer agent"

```bash
cat references/onboarding-checklist.md | head -60
```

**Expected result:** 7-phase onboarding checklist (welcome, team intro, comms, role, project, tooling, first task) with role-specific additions.

## Resources

- [onboarding-checklist](references/onboarding-checklist.md) — Checklist phases, role-specific additions, verification, documentation, examples, troubleshooting
- [role-briefing](references/role-briefing.md) — Briefing components, responsibilities, reporting structure, expectations, confirmation, examples
