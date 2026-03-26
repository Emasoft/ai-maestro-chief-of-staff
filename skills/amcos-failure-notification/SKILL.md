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
agent: ai-maestro-chief-of-staff-main-agent
---

# Failure Notification

## Overview

Failure notifications inform agents when operations fail, with error details, severity levels, and recovery guidance. Covers failure messaging, cascading failures, and proactive handoffs.

## Prerequisites

- AI Maestro running with AMP protocol
- AMP initialized: `amp-init.sh --auto`
- Error details captured from the failed operation
- Target agents registered and reachable

## Instructions

### PROCEDURE 4: Failure Notification

**When to use:** When any operation fails (skill install, restart, config change, timeout).

**Workflow:**

1. **Capture error details** - Record error message, stack trace, context, timestamp
2. **Determine severity** - `critical` (system-wide), `error` (single op), `warning` (degraded)
3. **Compose failure message** - AMP template with error details, severity, recovery steps
4. **Send to affected agents** - Use `amp-send.sh` exclusively
5. **Provide recovery guidance** - Retry, rollback, or manual intervention steps
6. **Log failure** - Record for analysis with full error context

Copy this checklist and track your progress:
- [ ] Captured error details and determined severity level
- [ ] Sent failure notification via `amp-send.sh` with recovery guidance
- [ ] Logged failure with full context and triggered escalation if needed

See [failure-notifications](references/failure-notifications.md) — Topics: Failure Notifications Reference, Table of Contents, 4.2 When to send failure notifications

See [op-failure-notification](references/op-failure-notification.md) — Topics: Failure Notification, Contents, When to Use

### Edge Cases

Consult edge case protocols when standard notification is insufficient. See [edge-case-protocols](references/edge-case-protocols.md) — Topics: Edge Case Protocols for Chief of Staff Agent, Table of Contents, Project Status (Cached Data)

### Proactive Handoff

When failure requires transferring work, use the proactive handoff protocol. See [proactive-handoff-protocol](references/proactive-handoff-protocol.md) — Topics: Proactive Handoff Protocol, Automatic Handoff Triggers, Table of Contents

### Design Document Protocol

When failures reveal systemic issues, create a design document. See [design-document-protocol](references/design-document-protocol.md) — Topics: Design Document Protocol, Table of Contents, Validate a single document

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

### Concrete Input/Output

**Input:** Skill install on `code-impl-auth` fails — "Skill validation failed - missing SKILL.md"
**Output:** AMP `failure` msg (priority `high`) sent; recovery steps provided; failure logged

### Example 1: Skill Installation Failure

Send via `agent-messaging` skill:
- **To**: `code-impl-auth` | **Priority**: `high`
- **Content**: type `failure`, error "Skill validation failed - missing SKILL.md", recovery: fix and retry

### Example 2: Restart Failure with Handoff

1. Send failure: **To** `code-impl-auth`, **Priority** `critical`, error "Health check failed after 3 attempts"
2. Trigger proactive handoff protocol for pending tasks

## Resources

- [failure-notifications](references/failure-notifications.md) — Topics: Failure Notifications Reference, Table of Contents, 4.2 When to send failure notifications
