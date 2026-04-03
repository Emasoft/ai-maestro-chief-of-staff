---
name: amcos-transfer-management-ref
description: Use when consulting detailed transfer management references. Trigger with transfer management lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Transfer Management Reference

## Overview

Reference material for transfer management. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-transfer-management` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-transfer-management` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Initiate an outbound transfer of an agent to another team"

```bash
cat references/transfer-procedures-and-examples.md | head -50
```

**Expected result:** Transfer procedure with request creation, dual-manager approval, execution, and AMP notifications.

## Resources

- [transfer-procedures-and-examples](references/transfer-procedures-and-examples.md) — Outbound/inbound transfers, approval, rejection, checklist, AMP format, examples
