---
name: amcos-post-op-notification
description: Use when notifying agents after an operation completes. Trigger with post-operation notification, status update, or completion reporting.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to AI Maestro messaging system. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
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

See [references/post-operation-notifications.md](references/post-operation-notifications.md) for detailed procedures.
  <!-- TOC: post-operation-notifications.md -->
  - What are post-operation notifications
  - Post-operation notification procedure
  - Verification request format
  - ...and 3 more sections
  <!-- /TOC -->

See [references/op-post-operation-notification.md](references/op-post-operation-notification.md) for the step-by-step runbook.
  <!-- TOC: op-post-operation-notification.md -->
  - When to Use
  - Procedure
  - Verification and Rollback
  - ...and 8 more sections
  <!-- /TOC -->

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

### Example 1: Skill Installation Confirmation

Send via `agent-messaging` skill:
- **To**: `code-impl-auth` | **Priority**: `normal`
- **Content**: type `post-operation`, `security-audit` skill installed, verify skill is active

### Example 2: Configuration Change Confirmation

Send via `agent-messaging` skill:
- **To**: `test-engineer-01` | **Priority**: `normal`
- **Content**: type `post-operation`, logging level changed to `debug`, verify new entries

## Resources

- [Post-Operation Notifications](references/post-operation-notifications.md)
- [Post-Operation Runbook](references/op-post-operation-notification.md)
- [Task Completion Checklist](references/task-completion-checklist.md)
  <!-- TOC: task-completion-checklist.md -->
  - Before Reporting Task Complete
  - Acceptance Criteria Met
  - Quality Gates Passed
  - ...and 45 more sections
  <!-- /TOC -->
