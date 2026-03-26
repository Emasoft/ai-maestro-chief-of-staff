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

See [role-assignment](references/role-assignment.md) — Topics: Role Assignment Reference, Table of Contents, 1.2 Standard Role Definitions

### PROCEDURE 2: Send Team Messages

**When/Steps:** Identify recipients, compose with priority, send via AI Maestro API, confirm delivery, log.

See [team-messaging](references/team-messaging.md) — Topics: Team Messaging Reference, Table of Contents, 2.2 Message Priority Levels

### PROCEDURE 3: Maintain Teammate Awareness

**When/Steps:** Poll for active sessions, query status, update roster, identify inactive agents, flag issues.

See [teammate-awareness](references/teammate-awareness.md) — Topics: Teammate Awareness Reference, Table of Contents, 3.2 Polling Agent Status

## Examples

**Input:** "Assign agent libs-svg-renderer the role of QA lead for the SVG pipeline team"

**Output:** "Role assigned: libs-svg-renderer -> QA lead. AMP notification sent (priority: high). Roster updated. Awaiting acknowledgment."

See [coordination-overview-and-examples](references/coordination-overview-and-examples.md) — Topics: Team Coordination - Overview, Examples, and Reference, Table of Contents, What Is Team Coordination

## Error Handling

| Issue | Resolution |
|-------|------------|
| Agent does not respond to role | Retry with higher priority, check if active, escalate after 3 attempts |
| Messages not delivered | Verify AI Maestro running, check session names, validate format |
| Team roster stale | Force refresh via polling, clear and rebuild, verify registry |

## Resources

- [role-assignment](references/role-assignment.md) — Topics: Role Assignment Reference, Table of Contents, 1.2 Standard Role Definitions

---

**Version:** 1.0
**Last Updated:** 2025-02-01
