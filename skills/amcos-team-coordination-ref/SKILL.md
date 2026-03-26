---
name: amcos-team-coordination-ref
description: Use when consulting detailed team coordination references. Trigger with team coordination lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Team Coordination Reference

## Overview

Reference material for team coordination. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-team-coordination` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-team-coordination` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Assign the developer role to a new team member"

```bash
cat references/role-assignment.md | head -50
```

**Expected result:** Role definitions, capability matching, assignment procedure, confirmation protocol, and transition handling.

## Resources

- [teammate-awareness](references/teammate-awareness.md) — Team roster management, status polling, activity detection, inactive handling, examples
- [role-assignment](references/role-assignment.md) — Role definitions, matching, assignment procedure, confirmation, transitions, examples
