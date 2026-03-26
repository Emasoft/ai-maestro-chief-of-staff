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
agent: ai-maestro-chief-of-staff-main-agent
---

# Pre-Operation Notification

## Overview

Pre-operation notifications warn agents about upcoming disruptive operations before they happen. This ensures agents have time to save work and acknowledge readiness via AMP protocol.

## Prerequisites

- AI Maestro running with AMP protocol
- AMP initialized: `amp-init.sh --auto`
- Target agents registered and reachable

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

### Checklist

Copy this checklist and track your progress:

- [ ] Identified affected agents and validated team membership
- [ ] Composed and sent AMP notification via `amp-send.sh`
- [ ] Tracked acknowledgments and handled any timeouts

See op-pre-operation-notification in Resources

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

**Input:** Skill install scheduled for agent `code-impl-auth` in 30s

```bash
amp-send.sh code-impl-auth "Pre-Op: Skill Install in 30s" \
  "Upcoming skill installation. Expected downtime: 30s. Please save work and reply ok."
```

**Expected result:** Agent receives notification and replies `"ok"` within 60s; operation proceeds.

## Resources

- [op-pre-operation-notification](references/op-pre-operation-notification.md) — Pre-op notification procedure
  - When to Use
  - Prerequisites
  - Procedure
    - Step 1: Identify Affected Agents
    - Step 2: Compose Notification Message
    - Step 3: Send Notification
    - Step 4: Track Acknowledgments
    - Step 5: Handle Timeout
  - Checklist
  - Examples
    - Example 1: Skill Installation Notification
    - Example 2: Timeout Final Notice
    - Example 3: System Maintenance Broadcast
  - Error Handling
  - Related Operations
