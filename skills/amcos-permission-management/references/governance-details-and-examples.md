# Governance Request Details and Examples

## Table of Contents

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

---

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

## Simplified Local Approval

When scope is **local** (same host, same team):
- Only `sourceManager` approval needed
- State: `pending -> local-approved -> executed`
- No `targetCOS`/`targetManager` fields required

## Rate Limiting

The GovernanceRequest API may rate-limit submissions:
- `429 Too Many Requests` -- retry after `Retry-After` header value
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

## Quick Checklist

Copy this checklist and track your progress:

- [ ] Identify operation requiring approval and risk level
- [ ] Submit GovernanceRequest via API (`POST /api/v1/governance/requests`)
- [ ] Send AMP notification to manager
- [ ] Wait for manager decision (poll API or use `amcos_approval_manager.py wait`)
- [ ] On approval: execute the operation
- [ ] On rejection: log reason and notify requester
- [ ] Update local YAML audit trail

## API Response (Primary)

When the API is available, the authoritative response comes from the REST API:

```json
{
  "request_id": "GR-20260227-abcd1234",
  "status": "local-approved",
  "decision": "approved",
  "decided_by": "user",
  "decided_at": "2026-02-27T10:30:00Z",
  "api_synced": true,
  "_source": "api"
}
```

## Offline Degradation

When the API is unreachable, responses include `"api_synced": false` and `"_source": "local-only"`.
Run `amcos_approval_manager.py sync` to reconcile once the API is available.

## Example 1: Spawn Agent (Local, Same Team)

```
PROCEDURE 1 -> POST /api/v1/governance/requests
  operation: spawn, scope: local, agent: worker-impl-03
PROCEDURE 2 -> Poll: pending -> local-approved (sourceManager approved in 15s)
Result: status=dual-approved (local ops need only sourceManager)
-> Proceed with agent spawn
```

## Example 2: Cross-Team Plugin Install

```
PROCEDURE 1 -> POST /api/v1/governance/requests
  operation: configure-agent, scope: cross-team
  sourceTeam: svgbbox-library-team, targetTeam: maestro-api-team
PROCEDURE 2 -> Poll: pending -> local-approved -> remote-approved -> dual-approved
PROCEDURE 3 -> 60s reminder sent to targetManager (no response yet)
Result: status=dual-approved after 75s
-> Proceed with plugin install on remote agent
```

## Plugin Prefix Reference

| Role | Prefix |
|------|--------|
| Chief of Staff | `amcos-` |
| Assistant Manager | `amama-` |
| Architect | `amaa-` |
| Orchestrator | `amoa-` |
| Integrator | `amia-` |

