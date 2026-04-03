---
name: amcos-post-op-notification-ref
description: Use when consulting detailed post op notification references. Trigger with post op notification lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Post Op Notification Reference

## Overview

Reference material for post op notification. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-post-op-notification` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-post-op-notification` for error handling.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify topic needed from Resources below
- [ ] Open and read the referenced file
- [ ] Follow the procedures in the reference file

## Examples

**Input:** "Send a post-operation notification after skill installation"

```bash
cat references/post-operation-notifications.md | head -50
```

**Expected result:** Notification procedure with success confirmation, message composition, AMP send, verification request, and logging.

## Resources

- [post-operation-notifications](references/post-operation-notifications.md) — When to send, notification procedure, verification format, examples, troubleshooting
