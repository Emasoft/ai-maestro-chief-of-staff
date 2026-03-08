---
name: amcos-permission-management
description: Use when requesting GovernanceRequest approval for agent lifecycle ops (spawn, terminate, hibernate, wake, plugin install). Trigger with permission requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging system and GovernanceRequest API (v1). Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 2.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# AMCOS Permission Management Skill -- GovernanceRequest

## Overview

Permission management uses the **GovernanceRequest** state machine to obtain authorization before executing privileged operations. AMCOS submits requests via the API; they transition through defined states until dual approval is obtained or rejected.

**States:** `pending -> remote-approved/local-approved -> dual-approved -> executed/rejected`

## Prerequisites

1. GovernanceRequest API available at `POST /api/v1/governance/requests`
2. Agent roles and team membership defined
3. Source and target manager identities known

## When Approval Is Required

| Operation | Scope | Approval Type |
|-----------|-------|---------------|
| Agent Spawn | local | sourceManager only |
| Agent Spawn | cross-team | dual-manager |
| Agent Terminate | any | sourceManager (+ target if cross-team) |
| Agent Hibernate/Wake | local | sourceManager only |
| Plugin Install | any | sourceManager (+ target if cross-team) |
| Critical Operation | any | dual-manager + governance password |

## Instructions

### PROCEDURE 1: Submit GovernanceRequest

1. Identify operation type and scope (local vs cross-team)
2. Determine required approvers
3. Compose payload and `POST /api/v1/governance/requests`
4. Receive `requestId` and `status: pending`

### PROCEDURE 2: Track GovernanceRequest State

1. `GET /api/v1/governance/requests/{requestId}` to poll state
2. Monitor transitions through approval states
3. Handle rate limiting (`429` -- back off exponentially)

### PROCEDURE 3: Handle Timeouts and Escalation

| Elapsed | Action |
|---------|--------|
| 60s | Send reminder to pending approver(s) |
| 90s | Send urgent notification |
| 120s | Auto-action: proceed (spawn/wake) or abort (terminate/hibernate/critical) |

- [ ] Determine operation scope (local vs cross-team)
- [ ] Identify required approvers (source and/or target manager)
- [ ] Submit GovernanceRequest via API and obtain requestId
- [ ] Poll request state until dual-approved or rejected
- [ ] Handle timeouts per escalation timeline

## Output

Successful approval returns JSON with `status: "dual-approved"` and approvals from sourceManager and targetManager. Rejected requests return `status: "rejected"` with a `reason` field.

## Governance Details

See `references/governance-details-and-examples.md` for payload format, governance password, local approval, rate limiting, audit trail, API responses, and examples.
  - [GovernanceRequest Payload](#governancerequest-payload)
  - [Governance Password](#governance-password)
  - [Simplified Local Approval](#simplified-local-approval)
  - [Rate Limiting](#rate-limiting)
  - [Audit Trail](#audit-trail)
  - [Quick Checklist](#quick-checklist)
  - [API Response (Primary)](#api-response-primary)
  - [Offline Degradation](#offline-degradation)
  - [Example 1: Spawn Agent (Local, Same Team)](#example-1-spawn-agent-local-same-team)
  - [Example 2: Cross-Team Plugin Install](#example-2-cross-team-plugin-install)
  - [Plugin Prefix Reference](#plugin-prefix-reference)

## Error Handling

| Issue | Resolution |
|-------|------------|
| Manager offline | Escalation timeline applies (60s/90s/120s) |
| API returns 429 | Back off per Retry-After header |
| targetManager unknown | Query via `GET /api/v1/teams/{teamId}/manager` |
| Governance password rejected | Re-request from sourceManager |
| Conflicting approvals | Latest timestamp wins; log conflict |

## Examples

**Input:** `POST /api/v1/governance/requests` with `{"operation": "agent-spawn", "scope": "local", "sourceTeam": "libs-svg", "sourceManager": "libs-svg-lead"}`

**Output:** `{"requestId": "gr-0042", "status": "pending"}` then after sourceManager approval: `{"requestId": "gr-0042", "status": "dual-approved"}`

See `references/governance-details-and-examples.md` for full examples.

## Resources

- `references/governance-details-and-examples.md`
- `references/approval-request-procedure.md`
- `references/approval-tracking.md`
- `references/approval-escalation.md`
- `references/approval-types-detailed.md`
- `references/approval-workflow-engine.md`

---

**Version:** 2.0
**Last Updated:** 2026-02-27
