---
name: amcos-request-approval
description: "Submit a GovernanceRequest for agent operations via AI Maestro API"
argument-hint: "--type <TYPE> --agent <NAME> --reason <TEXT> [--scope local|cross-team] [--urgent] [--governance-password <PWD>] [--timeout <SECONDS>]"
allowed-tools: ["Bash", "Task", "Read"]
user-invocable: true
---

# AMCOS Request Approval Command

Submit a **GovernanceRequest** to `POST /api/v1/governance/requests` for sensitive agent operations. The request follows the GovernanceRequest state machine until approval or rejection.

## GovernanceRequest States

```
pending → local-approved / remote-approved → dual-approved → executed
        → rejected
```

## Usage

1. Compose GovernanceRequest payload with operation details
2. `POST /api/v1/governance/requests`
3. Track state via `GET /api/v1/governance/requests/{requestId}`
4. Execute only after `local-approved` (local) or `dual-approved` (cross-team)

## Operations Requiring GovernanceRequest

| Operation | Scope | Approvers | Password |
|-----------|-------|-----------|----------|
| `spawn` | local | sourceManager | No |
| `spawn` | cross-team | sourceManager + targetManager | No |
| `terminate` | local | sourceManager | No |
| `terminate` | cross-team | sourceManager + targetManager | No |
| `hibernate` | local | sourceManager | No |
| `wake` | local | sourceManager | No |
| `install` | local | sourceManager | No |
| `install` | cross-team | sourceManager + targetManager | No |
| `replace` | any | sourceManager (+ targetManager) | No |
| `critical` | any | dual-manager | **Yes** |

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--type <TYPE>` | **Yes** | Operation type |
| `--agent <NAME>` | **Yes** | Target agent name |
| `--reason <TEXT>` | **Yes** | Justification |
| `--scope <SCOPE>` | No | `local` (default) or `cross-team` |
| `--target-cos <NAME>` | If cross-team | Target COS session |
| `--target-manager <NAME>` | If cross-team | Target manager session |
| `--governance-password <PWD>` | If critical | Manager-provided governance password |
| `--urgent` | No | Set priority to urgent |
| `--timeout <SECONDS>` | No | Wait for response (default: 0) |
| `--metadata <JSON>` | No | Additional context |

## Request ID Generation

```bash
REQUEST_ID="GR-$(date +%Y%m%d%H%M%S)-$(openssl rand -hex 4)"
```

## Examples

```bash
# Local spawn (single-manager approval)
/amcos-request-approval --type spawn --agent helper-tester \
  --reason "Need agent for parallel test execution"

# Cross-team spawn (dual-manager approval)
/amcos-request-approval --type spawn --agent backend-worker \
  --scope cross-team --target-cos amcos-backend --target-manager eama-backend \
  --reason "Need worker on backend team for data migration"

# Critical operation (governance password required)
/amcos-request-approval --type critical --agent prod-deployer \
  --governance-password "$GOV_PWD" --urgent \
  --reason "Emergency production deployment"

# Local terminate with wait
/amcos-request-approval --type terminate --agent old-worker \
  --reason "Agent has critical unrecoverable bug" --timeout 60
```

## GovernanceRequest Payload

```json
{
  "requestId": "GR-20260227150000-a1b2c3d4",
  "type": "terminate",
  "sourceCOS": "amcos-main",
  "sourceManager": "eama-main",
  "targetCOS": null,
  "targetManager": null,
  "operation": {
    "action": "terminate",
    "target": "old-worker",
    "parameters": {}
  },
  "justification": "Agent has critical unrecoverable bug",
  "impact": {"scope": "local", "risk_level": "high"},
  "governancePassword": null,
  "priority": "high",
  "status": "pending"
}
```

## Cross-Team Payload (Dual-Manager)

```json
{
  "requestId": "GR-20260227150100-b2c3d4e5",
  "type": "spawn",
  "sourceCOS": "amcos-frontend",
  "sourceManager": "eama-frontend",
  "targetCOS": "amcos-backend",
  "targetManager": "eama-backend",
  "operation": {
    "action": "spawn",
    "target": "backend-worker",
    "parameters": {}
  },
  "justification": "Need worker on backend team for data migration",
  "impact": {"scope": "cross-team", "risk_level": "medium"},
  "governancePassword": null,
  "priority": "high",
  "status": "pending"
}
```

## Response Tracking

```
=======================================================================
  GOVERNANCE REQUEST SUBMITTED
=======================================================================

  Request ID:       GR-20260227150000-a1b2c3d4
  Operation:        terminate
  Target Agent:     old-worker
  Scope:            local
  Priority:         high
  Status:           pending

  Approvers:
    sourceManager:  eama-main        [pending]
    targetManager:  n/a (local)

  Reason: Agent has critical unrecoverable bug

=======================================================================
  Use /amcos-check-approval-status --request-id GR-20260227150000-a1b2c3d4
=======================================================================
```

## Rate Limiting

- API may return `429 Too Many Requests`
- Respect `Retry-After` header
- Max 10 GovernanceRequests/minute per COS
- Back off exponentially on repeated 429s

## Tracking Location

```
~/.aimaestro/governance/pending/GR-20260227150000-a1b2c3d4.json
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `429 Too Many Requests` | Rate limited | Back off per Retry-After |
| `400 Invalid Password` | Wrong governance password | Re-request from manager |
| `404 Target Manager` | Unknown targetManager | Query team registry |
| API unreachable | AI Maestro down | Check if AI Maestro is running |
| Missing `--target-cos` | Cross-team without target | Provide target COS and manager |

## Related Commands

- `/amcos-check-approval-status` - Check GovernanceRequest state
- `/amcos-wait-for-approval` - Wait for approval with timeout
- `/amcos-notify-manager` - Send notification to manager
- `/amcos-staff-status` - View all agents
