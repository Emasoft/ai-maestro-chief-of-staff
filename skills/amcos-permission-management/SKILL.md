---
name: amcos-permission-management
description: Use when requesting GovernanceRequest approval for agent lifecycle ops. Trigger with permission requests for spawn, terminate, hibernate, wake, or plugin install. Loaded by ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging system and GovernanceRequest API (v1).
metadata:
  author: Emasoft
  version: 2.0.0
context: fork
background: false
agent: ai-maestro-chief-of-staff-main-agent
---

# AMCOS Permission Management Skill -- GovernanceRequest

## Overview

Uses the **GovernanceRequest** state machine to authorize privileged operations. Requests transition: `pending -> remote-approved/local-approved -> dual-approved -> executed/rejected`

## Prerequisites

1. GovernanceRequest via the `aimaestro-governance.sh request` CLI (auth resolved internally)
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
| Critical Op | any | dual-manager (R28 portfolio mandate/approval token — no agent password, R32) |

## Instructions

### PROCEDURE 1: Submit GovernanceRequest

1. Identify operation type and scope (local vs cross-team)
2. Determine required approvers
3. `aimaestro-governance.sh request --type <T> [--agent …] [--payload-json …]` with the request fields (auth via AID — R28; no password)
4. Receive `requestId` and `status: pending`

### PROCEDURE 2: Track GovernanceRequest State

1. `aimaestro-governance.sh requests --status pending` (match by requestId) to poll
2. Monitor transitions through approval states
3. Handle `429` with exponential backoff

### PROCEDURE 3: Handle Timeouts and Escalation

| Elapsed | Action |
|---------|--------|
| 60s | Reminder to pending approver(s) |
| 90s | Urgent notification |
| 120s | Auto-proceed (spawn/wake) or abort (terminate/hibernate/critical) |

### Checklist

Copy this checklist and track your progress:

- [ ] Determine operation scope (local vs cross-team)
- [ ] Identify required approvers (source and/or target manager)
- [ ] Submit GovernanceRequest via API and obtain requestId
- [ ] Poll request state until dual-approved or rejected
- [ ] Handle timeouts per escalation timeline

## Output

Approved: JSON with `status: "dual-approved"` and both manager approvals. Rejected: `status: "rejected"` with `reason` field.

## Governance Details

See governance-details-and-examples in Resources for payload format and approval examples.

## Error Handling

| Issue | Resolution |
|-------|------------|
| Manager offline | Escalation timeline (60s/90s/120s) |
| API 429 | Back off per Retry-After header |
| targetManager unknown | `aimaestro-teams.sh show <team-id>` (manager is in the team object) |
| Conflicting approvals | Latest timestamp wins; log conflict |

## Examples

**Input:** Submit a local agent-spawn request

```bash
aimaestro-governance.sh request --type agent-spawn \
  --payload-json '{"operation":"agent-spawn","scope":"local","sourceTeam":"libs-svg","sourceManager":"libs-svg-lead"}'
```

**Expected result:** `{"requestId": "gr-0042", "status": "pending"}` then after approval: `{"status": "dual-approved"}`

## Resources

- [governance-details-and-examples](references/governance-details-and-examples.md) — Payload format, approval flow, rate limiting, audit, examples
  - GovernanceRequest Payload
  - Simplified Local Approval
  - Rate Limiting
  - Audit Trail
  - Quick Checklist
  - API Response (Primary)
  - Offline Degradation
  - Example 1: Spawn Agent (Local, Same Team)
  - Example 2: Cross-Team Plugin Install
  - Plugin Prefix Reference
