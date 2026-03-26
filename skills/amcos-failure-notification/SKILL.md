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

See [op-failure-notification](references/op-failure-notification.md) — Topics: Failure Notification, Contents, When to Use, Prerequisites, Procedure, Step 1: Capture Error Details, Step 2: Compose Failure Message, Step 3: Send Failure Notification, Step 4: Provide Recovery Guidance, Step 5: Log Failure, Checklist, Examples, Example 1: Skill Installation Failure, Example 2: Agent Restart Failure, Example 3: Configuration Change Failure, Example 4: Timeout Failure Notification, Error Severity Levels, Error Handling, Related Operations

### Edge Cases

### Proactive Handoff

### Design Document Protocol

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

```bash
# Send failure notification after skill install error
amp-send.sh code-impl-auth "FAILURE: skill install" high \
  '{"type":"failure","error":"Skill validation failed - missing SKILL.md","recovery":"Fix SKILL.md and retry"}'
```

Expected: agent receives failure details with recovery steps; failure logged with timestamp.

## Checklist

Copy this checklist and track your progress:
- [ ] Capture error details and determine severity
- [ ] Send failure notification via amp-send.sh with recovery guidance
- [ ] Log failure and escalate if needed

## Resources

