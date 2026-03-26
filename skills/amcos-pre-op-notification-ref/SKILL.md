---
name: amcos-pre-op-notification-ref
description: Use when consulting detailed pre op notification references. Trigger with pre op notification lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Pre Op Notification Reference

## Overview

Reference material for pre op notification. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-pre-op-notification` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-pre-op-notification` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Send a pre-operation warning before plugin installation"

```bash
cat references/pre-operation-notifications.md | head -50
```

**Expected result:** Notification procedure with agent identification, message composition, AMP send, acknowledgment tracking, and timeout handling.

## Resources

- [pre-operation-notifications](references/pre-operation-notifications.md) — When to send, notification procedure, message format, priority levels, examples, troubleshooting
