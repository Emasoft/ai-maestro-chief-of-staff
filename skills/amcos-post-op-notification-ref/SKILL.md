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
  - 2.1 What are post-operation notifications - Understanding confirmation messages
  - 2.2 When to send post-operation notifications - Confirmation triggers
    - 2.2.1 Skill installation complete - Skill is now active
    - 2.2.2 Agent restart complete - Agent is back online
    - 2.2.3 Configuration applied - Settings now active
    - 2.2.4 Maintenance complete - Normal operations resume
  - 2.3 Post-operation notification procedure - Step-by-step process
    - 2.3.1 Confirm operation success - Verify completion
    - 2.3.2 Compose confirmation - What to tell agents
    - 2.3.3 Send notification - Using the `agent-messaging` skill
    - 2.3.4 Request verification - Ask agent to confirm
    - 2.3.5 Log outcome - Record the result
  - 2.4 Verification request format - Asking agents to confirm
  - 2.5 Examples - Post-operation scenarios
  - 2.6 Troubleshooting - Verification issues
