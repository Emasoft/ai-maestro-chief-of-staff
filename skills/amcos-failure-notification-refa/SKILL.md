---
name: amcos-failure-notification-refa
description: Use when consulting detailed failure notification references. Trigger with failure notification lookups.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Failure Notification Reference

## Overview

Reference material for failure notification. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-failure-notification` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-failure-notification` for error handling.

## Examples

```bash
# Look up edge case protocol for AI Maestro unavailable
cat references/edge-case-protocols.md | grep -A5 "AI Maestro Unavailable"
```

Expected: detection methods and fallback communication steps.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the failure notification topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [edge-case-protocols](references/edge-case-protocols.md) — Edge case protocols for unavailable services, timeouts, approval failures
- [proactive-handoff-protocol](references/proactive-handoff-protocol.md) — Proactive handoff triggers, templates, UUID tracking
- [failure-notifications](references/failure-notifications.md) — Failure notification procedures, severity levels, recovery patterns
