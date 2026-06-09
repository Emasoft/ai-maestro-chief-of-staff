---
name: amcos-acknowledgment-protocol-ref
description: Use when consulting detailed acknowledgment protocol references. Trigger with acknowledgment protocol lookups. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Acknowledgment Protocol Reference

## Overview

Reference material for acknowledgment protocol. Consult for detailed procedures.

## Prerequisites

- AI Maestro installed. See `amcos-acknowledgment-protocol` for full prerequisites.

## Instructions

1. Identify the topic you need from the Resources section below
2. Open the referenced file for detailed procedures and examples
3. Follow the procedures described in the reference file

## Output

Reference material — no direct output.

## Error Handling

See `amcos-acknowledgment-protocol` for error handling.

## Examples

```bash
# Look up acknowledgment timeout policy
cat references/acknowledgment-protocol.md | grep -A5 "Timeout"
```

Expected: timeout values and reminder intervals for each ACK type.

## Checklist

Copy this checklist and track your progress:
- [ ] Identify the acknowledgment topic needed
- [ ] Open the correct reference file
- [ ] Follow the documented procedure

## Resources

- [acknowledgment-protocol](references/acknowledgment-protocol.md) — Acknowledgment protocol reference: triggers, procedure, formats, troubleshooting
  - 3.1 What is the acknowledgment protocol - Understanding coordination
  - 3.2 When to require acknowledgments - Acknowledgment triggers
    - 3.2.1 Disruptive operations - Agent will be interrupted
    - 3.2.2 State-changing operations - Agent context affected
    - 3.2.3 Multi-agent coordination - Synchronized actions needed
  - 3.3 Acknowledgment procedure - Step-by-step process
    - 3.3.1 Send acknowledgment request - Ask for "ok"
    - 3.3.2 Start timeout timer - 2 minute maximum wait
    - 3.3.3 Send reminders - At 30s, 60s, 90s intervals
    - 3.3.4 Process response - Handle "ok" or other responses
    - 3.3.5 Proceed or timeout - Continue or handle no response
  - 3.4 Acknowledgment message format - Standard request structure
  - 3.5 Reminder message format - Standard reminder structure
  - 3.6 Response handling - What agents can send back
  - 3.7 Timeout behavior - What happens without response
  - 3.8 Examples - Acknowledgment scenarios
  - 3.9 Troubleshooting - Acknowledgment issues
