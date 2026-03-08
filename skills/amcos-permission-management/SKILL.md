---
name: amcos-permission-management
description: Use when requesting GovernanceRequest approval for agent lifecycle ops. Trigger with permission requests for spawn, terminate, hibernate, wake, or plugin install.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging system and GovernanceRequest API (v1).
metadata:
  author: Emasoft
  version: 2.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# AMCOS Permission Management Skill -- GovernanceRequest

## Overview

Uses the **GovernanceRequest** state machine to authorize privileged operations. Requests transition: `pending -> remote-approved/local-approved -> dual-approved -> executed/rejected`

## Prerequisites

1. GovernanceRequest API at `POST /api/v1/governance/requests`
2. Agent roles and team membership defined
3. Source and target manager identities known

## When Approval Is Required

| Operation | Scope | Approval Type |
|-----------|-------|---------------|
| Agent Spawn | local | sourceManager |
| Agent Spawn | cross-team | dual-manager |
| Agent Terminate | any | sourceManager (+ target if cross-team) |
| Hibernate/Wake | local | sourceManager |
| Plugin Install | any | sourceManager (+ target if cross-team) |
| Critical Op | any | dual-manager + governance password |

## Instructions

### PROCEDURE 1: Submit GovernanceRequest

1. Identify operation type and scope (local vs cross-team)
2. Determine required approvers
3. `POST /api/v1/governance/requests` with payload
4. Receive `requestId` and `status: pending`

### PROCEDURE 2: Track GovernanceRequest State

1. `GET /api/v1/governance/requests/{requestId}` to poll
2. Monitor transitions through approval states
3. Handle `429` with exponential backoff

### PROCEDURE 3: Handle Timeouts and Escalation

| Elapsed | Action |
|---------|--------|
| 60s | Reminder to pending approver(s) |
| 90s | Urgent notification |
| 120s | Auto-proceed (spawn/wake) or abort (terminate/hibernate/critical) |

Copy this checklist and track your progress:

- [ ] Determine operation scope (local vs cross-team)
- [ ] Identify required approvers (source and/or target manager)
- [ ] Submit GovernanceRequest via API and obtain requestId
- [ ] Poll request state until dual-approved or rejected
- [ ] Handle timeouts per escalation timeline

## Output

Approved: JSON with `status: "dual-approved"` and both manager approvals. Rejected: `status: "rejected"` with `reason` field.

## Governance Details

See `references/governance-details-and-examples.md` for payload format, governance password, local approval, rate limiting, audit trail, API responses, and examples.

## Error Handling

| Issue | Resolution |
|-------|------------|
| Manager offline | Escalation timeline (60s/90s/120s) |
| API 429 | Back off per Retry-After header |
| targetManager unknown | `GET /api/v1/teams/{teamId}/manager` |
| Password rejected | Re-request from sourceManager |
| Conflicting approvals | Latest timestamp wins; log conflict |

## Examples

**Input:** `POST /api/v1/governance/requests` with `{"operation": "agent-spawn", "scope": "local", "sourceTeam": "libs-svg", "sourceManager": "libs-svg-lead"}`

**Output:** `{"requestId": "gr-0042", "status": "pending"}` then after approval: `{"requestId": "gr-0042", "status": "dual-approved"}`

See `references/governance-details-and-examples.md` for full examples.

## Resources

- `references/governance-details-and-examples.md`
- `references/approval-request-procedure.md`
- `references/approval-tracking.md`
- `references/approval-escalation.md`
- `references/approval-types-detailed.md`
- `references/approval-workflow-engine.md`
