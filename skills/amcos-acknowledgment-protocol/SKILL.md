---
name: amcos-acknowledgment-protocol
description: Use when requesting or processing agent acknowledgments before proceeding with operations. Trigger with acknowledgment requests or ACK timeout handling.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to AI Maestro messaging system. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Acknowledgment Protocol

## Overview

Ensures agents confirm readiness before disruptive operations via ACK requests, timeout management, reminders, and timeout handling.

## Prerequisites

- AI Maestro running with AMP protocol
- AMP initialized: `amp-init.sh --auto`
- Target agents registered and reachable
- Pre-operation notification already sent (ACK follows pre-op)

## Instructions

### PROCEDURE 3: Acknowledgment Protocol

**When to use:** When agent confirmation is needed before proceeding, or when coordinating multi-agent operations.

**Workflow:**

1. **Send ACK request** - Use `amp-send.sh` to ask agent to reply "ok"
2. **Start timeout timer** - Use standardized timeout from policy table below
3. **Send reminders** - At defined intervals (e.g., 15s, 30s, 45s for pre-op ACK)
4. **Process response** - Handle "ok" or other responses
5. **Proceed or timeout** - Continue if ACK received, or follow timeout behavior

Copy this checklist and track your progress:
- [ ] Sent ACK request and started timeout timer per policy table
- [ ] Sent reminders at defined intervals if no response received
- [ ] Processed response (or timeout) and proceeded accordingly

See [op-acknowledgment-protocol](references/op-acknowledgment-protocol.md) for full procedure details and examples.

### Standardized ACK Timeout Policy

**CRITICAL:** All AMCOS components MUST use these values:

| ACK Type | Timeout | Reminders | Use Case |
|----------|---------|-----------|----------|
| Pre-operation ACK | **60s** | 15s, 30s, 45s | Before disruptive ops |
| Approval request | **2 min** | 60s, 90s | Manager approval |
| Emergency handoff | **30s** | 10s, 20s | Time-critical emergencies |
| Health check | **30s** | None | Verifying agent alive |

**Timeout behavior:** Pre-op ACK: proceed after final notice. Approval: proceed if autonomous, else abort. Emergency: proceed immediately.

## Output

| Action | Output |
|--------|--------|
| ACK request sent | Delivered, timeout timer started |
| ACK received | Agent confirmed, operation may proceed |
| Timeout reached | Final notice sent, logged, fallback taken |

## Error Handling

| Issue | Resolution |
|-------|------------|
| ACK timeout | Send final notice, log, proceed per policy |
| Reminder not delivered | Health check agent. If offline, proceed per timeout |
| Partial ACK (multi-agent) | Track per-agent. Proceed when all respond or all timeout |

## Examples

```bash
# Send ACK request before disruptive operation
amp-send.sh code-impl-auth "ACK: hibernate in 60s" high \
  '{"type":"acknowledgment-request","timeout":60}'
```

Expected: agent replies "ok" within 60s; if no reply after reminders at 15s/30s/45s, proceed with final notice.

## Checklist

Copy this checklist and track your progress:
- [ ] Send ACK request via agent-messaging with correct timeout
- [ ] Send reminders at defined intervals if no response
- [ ] Process response or handle timeout per policy

## Resources

- [op-acknowledgment-protocol](references/op-acknowledgment-protocol.md) — Full ACK procedure, timeout policy, examples
  - Contents
  - When to Apply
  - Prerequisites
  - Standardized ACK Timeout Policy
  - Procedure
  - Step 1: Send Acknowledgment Request
  - Step 2: Start Timeout Timer
  - Step 3: Send Reminders
  - Step 4: Process Response
  - Step 5: Proceed or Handle Timeout
  - Checklist
  - Examples
  - Example 1: Pre-Operation ACK Flow
  - Example 2: Approval Request ACK
  - Example 3: Emergency Handoff ACK
  - Error Handling
  - Related Operations
