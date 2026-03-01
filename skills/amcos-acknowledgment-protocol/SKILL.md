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
agent: amcos-main
---

# Acknowledgment Protocol

## Overview

The acknowledgment protocol ensures agents confirm readiness before disruptive operations proceed. Covers sending ACK requests, managing timeouts with standardized intervals, sending reminders, and handling timeout scenarios.

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

**Triggers:** Disruptive operations, state-changing operations, multi-agent coordination.

See [references/acknowledgment-protocol.md](references/acknowledgment-protocol.md) for detailed procedures.
  <!-- TOC: acknowledgment-protocol.md -->
  - What is the acknowledgment protocol
  - Acknowledgment procedure
  - Timeout behavior
  - ...and 6 more sections
  <!-- /TOC -->

See [references/op-acknowledgment-protocol.md](references/op-acknowledgment-protocol.md) for the step-by-step runbook.
  <!-- TOC: op-acknowledgment-protocol.md -->
  - When to Use
  - Procedure
  - Verification and Rollback
  - ...and 9 more sections
  <!-- /TOC -->

### Standardized ACK Timeout Policy

**CRITICAL:** All AMCOS components MUST use these values:

| ACK Type | Timeout | Reminders | Use Case |
|----------|---------|-----------|----------|
| Pre-operation ACK | **60s** | 15s, 30s, 45s | Before disruptive ops |
| Approval request | **2 min** | 60s, 90s | Manager approval |
| Emergency handoff | **30s** | 10s, 20s | Time-critical emergencies |
| Health check | **30s** | None | Verifying agent alive |

Timeouts are **sequential**. Example total: 60s + 2min + 30s = 3min 30s.

**Timeout behavior:**
- Pre-op ACK: Send final notice, then proceed
- Approval: Log timeout, proceed if autonomous mode, else abort
- Emergency: Proceed immediately

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
| Unexpected response | See [references/acknowledgment-protocol.md](references/acknowledgment-protocol.md) Section 3.6 |
| Reminder not delivered | Health check agent. If offline, proceed per timeout |
| Partial ACK (multi-agent) | Track per-agent. Proceed when all respond or all timeout |

## Examples

### Example 1: Standard Pre-Operation ACK

1. Send via `agent-messaging`: **To** `code-impl-auth`, **Priority** `high`, type `acknowledgment-request`, reply "ok" within 60s
2. Send reminders at 15s, 30s, 45s if no reply
3. On `"ok"`: proceed with operation

### Example 2: ACK Timeout Handling

After 60s with no response:
1. Log: `WARNING: No ACK from code-impl-auth after 60s`
2. Send final notice: type `timeout-notice`, operation will proceed
3. Proceed with hibernate and install

## Resources

- [Acknowledgment Protocol](references/acknowledgment-protocol.md)
- [Acknowledgment Runbook](references/op-acknowledgment-protocol.md)
- [Message Response Decision Tree](references/message-response-decision-tree.md)
  <!-- TOC: message-response-decision-tree.md -->
  - Step 1: Priority Triage
  - Step 2: Message Type Routing
  - Step 3: Response Actions
  - ...and 6 more sections
  <!-- /TOC -->
