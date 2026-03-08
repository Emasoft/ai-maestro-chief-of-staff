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
agent: amcos-chief-of-staff-main-agent
---

# AI Maestro Chief of Staff Team Coordination Skill

## Overview

Team coordination manages distributed agent teams, assigns roles, coordinates messaging between members, and maintains awareness of all active teammates and their current status.

## Prerequisites

1. Team registry is accessible
2. AI Maestro messaging is available
3. Agent roles are defined

## Instructions

> **Output Rule**: All AMCOS scripts produce 2-line stdout summaries. Full output is written to `.amcos-logs/`.

1. Identify coordination need
2. Query team registry for current state
3. Execute coordination action
4. Update team registry and notify agents

## Output

| Coordination Type | Output |
|-------------------|--------|
| Team formation | New team created, agents assigned |
| Role assignment | Agent roles updated, registry modified |
| Status sync | All agents aligned on current state |

## Core Procedures

### PROCEDURE 1: Assign Agent Roles

**When/Steps:** Identify role, match capabilities, send assignment message, confirm acceptance, update roster.

See `references/role-assignment.md` and `references/op-assign-agent-roles.md`.

### PROCEDURE 2: Send Team Messages

**When/Steps:** Identify recipients, compose with priority, send via AI Maestro API, confirm delivery, log.

See `references/team-messaging.md` and `references/op-send-team-messages.md`.

### PROCEDURE 3: Maintain Teammate Awareness

**When/Steps:** Poll for active sessions, query status, update roster, identify inactive agents, flag issues.

See `references/teammate-awareness.md` and `references/op-maintain-teammate-awareness.md`.

## Examples

See `references/coordination-overview-and-examples.md` for full examples including role assignment, team broadcasts, status checks, and coordination workflows with input/output.
- What Is Team Coordination
- Team Coordination Components
- Examples: Assigning a Role to a New Agent
- Examples: Broadcasting a Team Update
- Examples: Checking Team Status
- Examples: Full Coordination Workflow with Input/Output
- Examples: Role Assignment with Input/Output
- Examples: Team Status Query with Input/Output
- Key Takeaways
- Task Checklist

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent does not respond to role | Retry with higher priority, check if active, escalate after 3 attempts |
| Messages not delivered | Verify AI Maestro running, check session names, validate format |
| Team roster stale | Force refresh via polling, clear and rebuild, verify registry |

## Resources

- `references/role-assignment.md`
- `references/team-messaging.md`
- `references/teammate-awareness.md`
- `references/coordination-overview-and-examples.md`
- `references/op-assign-agent-roles.md`
- `references/op-send-team-messages.md`
- `references/op-maintain-teammate-awareness.md`

---

**Version:** 1.0
**Last Updated:** 2025-02-01
