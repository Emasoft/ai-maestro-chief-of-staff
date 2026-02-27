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
agent: amcos-main
workflow-instruction: "support"
procedure: "support-skill"
---

# AMCOS Permission Management Skill — GovernanceRequest

## Overview

Permission management uses the **GovernanceRequest** state machine to obtain authorization before executing privileged operations. AMCOS submits a GovernanceRequest via the API; the request transitions through defined states until dual approval is obtained or the request is rejected.

## GovernanceRequest State Machine

```
                    ┌──────────────────────────────────────────────────────────┐
                    │                    GovernanceRequest                     │
                    │                                                          │
  POST /api/v1/     │   pending                                                │
  governance/       │     │                                                    │
  requests          │     ├──→ remote-approved (targetManager approved)         │
  ─────────────────►│     │        │                                            │
                    │     │        └──→ dual-approved ──→ executed              │
                    │     │                 ▲                                   │
                    │     ├──→ local-approved (sourceManager approved)          │
                    │     │        │                                            │
                    │     │        └──→ dual-approved ──→ executed              │
                    │     │                                                    │
                    │     └──→ rejected                                        │
                    └──────────────────────────────────────────────────────────┘
```

**States:** `pending → remote-approved/local-approved → dual-approved → executed/rejected`

## Prerequisites

1. GovernanceRequest API available at `POST /api/v1/governance/requests`
2. Agent roles and team membership defined
3. Source and target manager identities known

## When Approval Is Required

| Operation | Scope | Approval Type |
|-----------|-------|---------------|
| Agent Spawn | local | sourceManager only |
| Agent Spawn | cross-team | dual-manager (source + target) |
| Agent Terminate | any | sourceManager (+ targetManager if cross-team) |
| Agent Hibernate | local | sourceManager only |
| Agent Wake | local | sourceManager only |
| Plugin Install | any | sourceManager (+ targetManager if cross-team) |
| Critical Operation | any | dual-manager + governance password |

**Local operations** (same host, same team): simplified single-manager approval.
**Cross-team operations**: DUAL-MANAGER approval required (both sourceCOS→sourceManager and targetCOS→targetManager).

## GovernanceRequest Payload

```json
{
  "requestId": "GR-<timestamp>-<random>",
  "type": "agent_spawn|agent_terminate|agent_hibernate|agent_wake|plugin_install|critical_operation",
  "sourceCOS": "<chief-of-staff-session>",
  "sourceManager": "<source-manager-session>",
  "targetCOS": "<target-chief-of-staff-session>",
  "targetManager": "<target-manager-session>",
  "operation": {"action": "...", "target": "...", "parameters": {}},
  "justification": "why this operation is needed",
  "impact": {"scope": "local|cross-team", "risk_level": "low|medium|high|critical"},
  "governancePassword": "<password-if-critical>",
  "status": "pending"
}
```

## Governance Password

For **critical operations** (risk_level=critical), the manager provides a governance password:
- Password is set per-team by the manager
- Included in the GovernanceRequest payload for critical ops
- API validates password before transitioning to `approved` state
- Never log or store the password after submission

## Core Procedures

### PROCEDURE 1: Submit GovernanceRequest

1. Identify operation type and scope (local vs cross-team)
2. Determine required approvers: `sourceManager` (always), `targetManager` (if cross-team)
3. Compose GovernanceRequest payload
4. `POST /api/v1/governance/requests` with payload
5. Receive `requestId` and initial `status: pending`
6. Register in local tracking

### PROCEDURE 2: Track GovernanceRequest State

1. `GET /api/v1/governance/requests/{requestId}` to poll state
2. Monitor transitions: `pending → local-approved/remote-approved → dual-approved`
3. Handle rate limiting (API returns `429` — back off exponentially)
4. Update local tracking on each state change

### PROCEDURE 3: Handle Timeouts and Escalation

| Elapsed | Action |
|---------|--------|
| 60s | Send reminder to pending approver(s) |
| 90s | Send urgent notification |
| 120s | Auto-action: proceed (spawn/wake) or abort (terminate/hibernate/plugin/critical) |

## Simplified Local Approval

When scope is **local** (same host, same team):
- Only `sourceManager` approval needed
- State: `pending → local-approved → executed`
- No `targetCOS`/`targetManager` fields required

## Rate Limiting

The GovernanceRequest API may rate-limit submissions:
- `429 Too Many Requests` — retry after `Retry-After` header value
- Max 10 requests/minute per COS agent
- Back off exponentially on repeated 429s

## Audit Trail

```yaml
audit_trail:
  - timestamp: "ISO-8601"
    requestId: "GR-..."
    operation: "spawn|terminate|hibernate|wake|plugin_install|critical"
    scope: "local|cross-team"
    status: "pending|local-approved|remote-approved|dual-approved|executed|rejected"
    sourceCOS: "..."
    sourceManager: "..."
    targetCOS: "..."
    targetManager: "..."
    governancePasswordUsed: true|false
    decided_at: "ISO-8601"
    escalation_count: 0|1|2|3
```

**Audit file location:** `docs_dev/audit/amcos-governance-{date}.yaml`

## Error Handling

| Issue | Resolution |
|-------|------------|
| Manager offline | Escalation timeline applies (60s/90s/120s) |
| API returns 429 | Back off per Retry-After header |
| Cross-team targetManager unknown | Query team registry via `GET /api/v1/teams/{teamId}/manager` |
| Governance password rejected | Re-request password from sourceManager, do not retry blindly |
| Conflicting approvals | Latest timestamp wins; log conflict |

## Plugin Prefix Reference

| Role | Prefix |
|------|--------|
| Chief of Staff | `amcos-` |
| Assistant Manager | `eama-` |
| Architect | `eaa-` |
| Orchestrator | `eoa-` |
| Integrator | `eia-` |

## Resources

- [Approval Request Procedure](references/approval-request-procedure.md)
- [Approval Tracking](references/approval-tracking.md)
- [Approval Escalation](references/approval-escalation.md)
- [Approval Types Detailed](references/approval-types-detailed.md)
- [Approval Workflow Engine](references/approval-workflow-engine.md)

---

**Version:** 2.0
**Last Updated:** 2026-02-27
**Target Audience:** Chief of Staff Agents
