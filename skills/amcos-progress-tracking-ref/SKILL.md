---
name: amcos-progress-tracking-ref
description: Use when consulting detailed progress tracking references. Trigger with progress tracking lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Progress Tracking Reference

## Overview

Reference material for progress tracking. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-progress-tracking` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-progress-tracking` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Recover a session after unexpected interruption"

```bash
cat references/op-recover-session.md | head -50
```

**Expected result:** 6-step recovery procedure: load memory files, read work/task state, validate consistency, confirm resumption.

## Resources

- [op-recover-session](references/op-recover-session.md) — Session recovery procedure, scenarios, checklist
- [16-memory-archival](references/16-memory-archival.md) — Archival triggers, procedures, organization, examples
- [op-update-task-progress](references/op-update-task-progress.md) — Task state updates, blockers, dependencies, timestamps
- [18-using-scripts](references/18-using-scripts.md) — Memory script commands, workflows, troubleshooting
