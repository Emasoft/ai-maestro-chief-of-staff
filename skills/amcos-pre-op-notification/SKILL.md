---
name: amcos-pre-op-notification
description: Use when notifying agents about upcoming operations before execution. Trigger with pre-operation notification or pre-flight alert needs.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to AI Maestro messaging system. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-main
---

# Pre-Operation Notification

## Overview

Pre-operation notifications warn agents about upcoming disruptive operations before they happen. This ensures agents have time to save work and acknowledge readiness via AMP protocol.

## Prerequisites

- AI Maestro running with AMP protocol
- AMP initialized: `amp-init.sh --auto`
- Target agents registered and reachable

## What Are Notification Protocols?

Standardized communication patterns ensuring:
- **No surprise interruptions**: Agents know when operations affect them
- **Graceful state preservation**: Time to save work before operations
- **Acknowledgment tracking**: Operations proceed only when agents are ready

## AMP Protocol Compliance

- **Send**: Use `amp-send.sh` exclusively. Never call HTTP API directly.
- **Signing**: Ed25519-signed automatically by `amp-send.sh`.
- **Setup**: Run `amp-init.sh --auto` once per agent.

## Closed Team Messaging Enforcement (M6)

| Direction | Rule |
|-----------|------|
| **Team member -> MANAGER** | COS intercepts, reviews, forwards via AMP |
| **Team member -> external** | COS checks reachability rules, forwards if allowed |
| **External -> team member** | Must go through COS or MANAGER |

Before sending, validate recipient against `GET /api/teams`. Block and log violations.

## Instructions

### PROCEDURE 1: Pre-Operation Notification

**When to use:** Before skill/plugin installation, agent restart, configuration changes, or any disruptive operation.

**Workflow:**

1. **Identify affected agents** - Determine which agents will be impacted
2. **Validate recipients** - Check team membership via `GET /api/teams`
3. **Compose notification** - AMP template with operation details and expected downtime
4. **Send via AMP** - Use `amp-send.sh` exclusively
5. **Track acknowledgments** - Monitor for agent readiness responses
6. **Handle timeouts** - Follow ACK timeout policy (see acknowledgment protocol skill)

See [references/pre-operation-notifications.md](references/pre-operation-notifications.md) for detailed procedures.
  <!-- TOC: pre-operation-notifications.md -->
  - What are pre-operation notifications
  - When to send pre-operation notifications
  - Pre-operation notification procedure
  - ...and 4 more sections
  <!-- /TOC -->

See [references/op-pre-operation-notification.md](references/op-pre-operation-notification.md) for the step-by-step runbook.
  <!-- TOC: op-pre-operation-notification.md -->
  - When to Use
  - Procedure
  - Verification and Rollback
  - ...and 8 more sections
  <!-- /TOC -->

## Output

| Type | Output |
|------|--------|
| Pre-operation alert | Notification sent, delivery confirmed |
| Broadcast warning | Message sent to own-team agents, receipt logged |

## Error Handling

| Issue | Resolution |
|-------|------------|
| Not delivered | Check agent registration, verify AMP initialized. See references Section 1.7 |
| Agent unreachable | Health check, retry after 10s |
| Team violation | Validate against `GET /api/teams` before sending |
| AMP signing failure | Re-run `amp-init.sh --auto` |

## Examples

### Example 1: Skill Installation Pre-Notification

Send via `agent-messaging` skill:
- **To**: `code-impl-auth` | **Priority**: `high`
- **Content**: type `pre-operation`, upcoming skill installation, 30s downtime, ACK required

### Example 2: Broadcast Warning

For each agent (`code-impl-auth`, `test-engineer-01`, `docs-writer`), send:
- **Subject**: `System Maintenance in 5 Minutes` | **Priority**: `high`
- **Content**: type `broadcast`, save work and reply "ok"

## Resources

- [Pre-Operation Notifications](references/pre-operation-notifications.md)
- [Pre-Operation Runbook](references/op-pre-operation-notification.md)
- [AI Maestro Message Templates](references/ai-maestro-message-templates.md)
  <!-- TOC: ai-maestro-message-templates.md -->
  - Standard Message Format (AMP)
  - When Notifying Agents of Upcoming Operations
  - When Reporting Operation Results
  - ...and 5 more sections
  <!-- /TOC -->
