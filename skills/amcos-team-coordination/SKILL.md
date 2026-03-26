---
name: amcos-team-coordination
description: Use when coordinating team members across agent sessions, assigning roles, managing messaging, and maintaining team status. Trigger with team formation, updates, or coordination needs.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging API access, session name resolution, and inter-agent communication capabilities. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff Team Coordination Skill

## Overview

Team coordination manages distributed agent teams, assigns roles, coordinates messaging between members, and maintains awareness of all active teammates and their current status.

## Prerequisites

1. Team registry is accessible
2. AI Maestro messaging is available
3. Agent roles are defined

## Instructions

1. Identify coordination need
2. Query team registry for current state
3. Execute coordination action
4. Update team registry and notify agents

### Checklist

Copy this checklist and track your progress:

- [ ] Verify team registry is accessible and current
- [ ] Confirm all target agents are active
- [ ] Send coordination messages via AI Maestro API
- [ ] Update roster with new assignments or status

## Output

| Coordination Type | Output |
|-------------------|--------|
| Team formation | New team created, agents assigned |
| Role assignment | Agent roles updated, registry modified |
| Status sync | All agents aligned on current state |

## Core Procedures

### PROCEDURE 1: Assign Agent Roles

**When/Steps:** Identify role, match capabilities, send assignment message, confirm acceptance, update roster.

### PROCEDURE 2: Send Team Messages

**When/Steps:** Identify recipients, compose with priority, send via AI Maestro API, confirm delivery, log.

See team-messaging in Resources below

### PROCEDURE 3: Maintain Teammate Awareness

**When/Steps:** Poll for active sessions, query status, update roster, identify inactive agents, flag issues.

## Examples

**Input:** "Assign agent libs-svg-renderer the role of QA lead"

```bash
amp-send.sh libs-svg-renderer "Role Assignment: QA Lead" \
  "You are assigned QA lead for the SVG pipeline team. Please acknowledge."
```

**Expected result:** Agent receives role assignment, replies with acknowledgment, roster updated.

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent does not respond to role | Retry with higher priority, check if active, escalate after 3 attempts |
| Messages not delivered | Verify AI Maestro running, check session names, validate format |
| Team roster stale | Force refresh via polling, clear and rebuild, verify registry |

## Resources

- [team-messaging](references/team-messaging.md) — Team message types, priority, routing, delivery
  - Team Message Types
  - Message Priority Levels
  - Sending Broadcast Messages
  - Sending Targeted Messages
  - Message Routing Rules
  - Confirming Message Delivery
  - Team Messaging Examples
  - Troubleshooting
