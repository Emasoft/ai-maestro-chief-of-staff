---
name: amcos-recovery-execution-ref
description: Use when consulting detailed recovery execution references. Trigger with recovery execution lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Recovery Execution Reference

## Overview

Reference material for recovery execution. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-recovery-execution` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-recovery-execution` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "How do I restart an unresponsive agent?"

```bash
cat references/recovery-operations.md | head -60
```

**Expected result:** Health check procedures, failure classification, and recovery strategies (retry, restart, hibernate-wake, replace).

## Resources

- [recovery-operations](references/recovery-operations.md) — Health checks, failure classification, recovery execution, restart procedures, logging, coordination
- [recovery-strategies](references/recovery-strategies.md) — Wait/retry, soft/hard restart, hibernate-wake, resource adjustment, replacement, troubleshooting
