---
name: amcos-failure-notification
description: Use when sending failure notifications after operation errors. Trigger with failure events, error reporting, or incident notification.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to AI Maestro messaging system. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# Failure Notification

## Overview

Failure notifications inform agents when operations fail, providing error details, severity levels, and recovery guidance. Covers failure messaging, edge cases like cascading failures, and proactive handoffs.

## Prerequisites

- AI Maestro running with AMP protocol
- AMP initialized: `amp-init.sh --auto`
- Error details captured from the failed operation
- Target agents registered and reachable

## Instructions

### PROCEDURE 4: Failure Notification

**When to use:** When any operation fails (skill install, agent restart, config change, timeout).

**Workflow:**

1. **Capture error details** - Record error message, stack trace, context, timestamp
2. **Determine severity** - `critical` (system-wide), `error` (single op), `warning` (degraded)
3. **Compose failure message** - AMP template with error details, severity, recovery guidance
4. **Send to affected agents** - Use `amp-send.sh` exclusively
5. **Provide recovery guidance** - Specific next steps (retry, rollback, manual intervention)
6. **Log failure** - Record for analysis with full error context

See [references/failure-notifications.md](references/failure-notifications.md) for detailed procedures.
  <!-- TOC: failure-notifications.md -->
  - What are failure notifications
  - Failure notification procedure
  - Error severity levels
  - ...and 5 more sections
  <!-- /TOC -->

See [references/op-failure-notification.md](references/op-failure-notification.md) for the step-by-step runbook.
  <!-- TOC: op-failure-notification.md -->
  - When to Use
  - Procedure
  - Verification and Rollback
  - ...and 10 more sections
  <!-- /TOC -->

### Edge Cases

Consult edge case protocols when standard notification is insufficient:
- AI Maestro unavailable during failure reporting
- Cascading failures across multiple agents
- Agent offline when failure notification sent

See [references/edge-case-protocols.md](references/edge-case-protocols.md).
  <!-- TOC: edge-case-protocols.md -->
  - AI Maestro Unavailable
  - GitHub Unavailable
  - Cascading Failures
  - ...and 29 more sections
  <!-- /TOC -->

### Proactive Handoff

When failure requires transferring work to another agent, use the proactive handoff protocol. See [references/proactive-handoff-protocol.md](references/proactive-handoff-protocol.md).
  <!-- TOC: proactive-handoff-protocol.md -->
  - Automatic Handoff Triggers
  - Mandatory Handoff Sections
  - Protocol for Handing Off GitHub Operations
  - ...and 5 more sections
  <!-- /TOC -->

### Design Document Protocol

When failures reveal systemic issues, create a design document. See [references/design-document-protocol.md](references/design-document-protocol.md).
  <!-- TOC: design-document-protocol.md -->
  - Document UUID Format (GUUID)
  - Required Frontmatter Schema
  - Document Lifecycle
  - ...and 27 more sections
  <!-- /TOC -->

## Output

| Type | Output |
|------|--------|
| Failure alert | Notification sent with error details and severity |
| Recovery guidance | Recovery steps provided to affected agents |
| Failure log | Error context recorded with timestamp |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Not delivered | Retry after 10s. If offline, queue. See references Section 4.8 |
| AI Maestro unavailable | Fallback per edge case protocols |
| Agent cannot recover | Escalate to MANAGER with full context |
| Cascading failure | Follow cascading protocol in edge case reference |

## Examples

### Example 1: Skill Installation Failure

Send via `agent-messaging` skill:
- **To**: `code-impl-auth` | **Priority**: `high`
- **Content**: type `failure`, error "Skill validation failed - missing SKILL.md", advise continue previous work, recovery: fix and retry

### Example 2: Restart Failure with Handoff

1. Send failure: **To** `code-impl-auth`, **Priority** `critical`, error "Health check failed after 3 attempts", recovery: handoff to backup agent
2. Trigger proactive handoff protocol for pending tasks

## Resources

- [Failure Notifications](references/failure-notifications.md)
- [Failure Notification Runbook](references/op-failure-notification.md)
- [Edge Case Protocols](references/edge-case-protocols.md)
- [Design Document Protocol](references/design-document-protocol.md)
- [Proactive Handoff Protocol](references/proactive-handoff-protocol.md)
