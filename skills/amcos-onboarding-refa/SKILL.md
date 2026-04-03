---
name: amcos-onboarding-refa
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

**Input:** "Prepare a project handoff document for the auth module"

```bash
cat references/project-handoff.md | head -60
```

**Expected result:** Handoff template with project overview, current state, key files, conventions, and verification steps.

## Resources

- [project-handoff](references/project-handoff.md) — Handoff preparation, overview, state sharing, conventions, knowledge transfer, verification, examples, troubleshooting
