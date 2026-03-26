---
name: amcos-staff-planning-ref
description: Use when consulting detailed staff planning references. Trigger with staff planning lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Staff Planning Reference

## Overview

Reference material for staff planning. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-staff-planning` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-staff-planning` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Plan capacity for a sprint with 3 agents"

```bash
cat references/capacity-planning.md | head -50
```

**Expected result:** Capacity metrics, agent inventory, task estimation, allocation calculation, and bottleneck identification.

## Resources

- [staffing-templates](references/staffing-templates.md) — Template structure, built-in templates, custom templates, validation, examples
- [capacity-planning](references/capacity-planning.md) — Capacity metrics, load balancing strategies, scaling decisions, examples
- [role-assessment](references/role-assessment.md) — Assessment procedure, capability extraction, gap analysis, examples
