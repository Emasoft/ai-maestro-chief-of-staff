---
name: amcos-post-op-notification
description: Use when notifying agents after an operation completes. Trigger with post-operation notification, status update, or completion reporting. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires access to AI Maestro messaging system. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# Post-Operation Notification

## Overview

Post-operation notifications confirm that operations completed successfully and request agents to verify results. Covers composing confirmations, sending via AMP, requesting verification, and logging outcomes.

## Prerequisites

- AI Maestro running with AMP protocol
- AMP initialized: `amp-init.sh --auto`
- The operation being reported has actually completed (verify first)
- Target agents registered and reachable

## Instructions

### PROCEDURE 2: Post-Operation Notification

**When to use:** After skill installation, agent restart, configuration changes, or any operation that affected an agent.

**Workflow:**

1. **Confirm operation completed** - Verify success before composing notification
2. **Compose success message** - AMP template with operation summary and what to verify
3. **Send via AMP** - Use `amp-send.sh` exclusively
4. **Request verification** - Ask agent to confirm the change is active
5. **Log outcome** - Record result, delivery confirmation, verification response

**Triggers:** Skill install complete, agent restart complete, config applied, maintenance complete.

### Checklist

Copy this checklist and track your progress:

- [ ] Confirmed operation completed successfully before composing notification
- [ ] Sent AMP confirmation via `amp-send.sh` and requested agent verification
- [ ] Logged outcome with timestamp and verification response

See op-post-operation-notification in Resources

## Message Type Quick Reference

| Message Type | When to Use | Requires Ack |
|--------------|-------------|--------------|
| `post-operation` | After successful operation | Optional |
| `reminder` | When awaiting verification | No |
| `acknowledgment` | Agent responding with "ok" | No |

## Output

| Type | Output |
|------|--------|
| Completion confirmation | Notification sent, delivery confirmed |
| Verification request | Request sent, awaiting agent confirmation |
| Outcome log | Result recorded with timestamp |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent does not verify | Reminder after 30s. No response after 60s: log unverified, escalate |
| Not delivered | Check registration, verify AMP. Retry after 10s |
| Verification failure reported | Log failure, trigger failure notification skill |
| Agent offline | Queue notification for delivery when agent returns |

## Examples

**Input:** Skill `security-audit` installed on `code-impl-auth`

```bash
amp-send.sh code-impl-auth "Post-Op: security-audit installed" \
  "Skill security-audit installed successfully. Please verify it is active."
```

**Expected result:** Agent receives notification, replies confirming skill is active, result logged.

## Resources

- [op-post-operation-notification](references/op-post-operation-notification.md) — Post-op notification procedure
  - When to Use
  - Prerequisites
  - Procedure
    - Step 1: Confirm Operation Completed
    - Step 2: Compose Success Message
    - Step 3: Send Confirmation
    - Step 4: Request Verification
    - Step 5: Log Outcome
  - Checklist
  - Examples
    - Example 1: Skill Installation Complete
    - Example 2: Agent Restart Complete
    - Example 3: System Maintenance Complete Broadcast
  - Error Handling
  - Related Operations
