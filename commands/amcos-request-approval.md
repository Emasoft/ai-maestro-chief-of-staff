---
name: amcos-request-approval
description: "Submit a GovernanceRequest for agent operations via AI Maestro API"
argument-hint: "--type <T> --agent <A> --reason <R> [--scope] [--urgent] [--timeout]"
allowed-tools: ["Bash", "Read"]
user-invocable: true
---

# AMCOS Request Approval Command

Submit a **GovernanceRequest** for sensitive agent operations via the `amcos-permission-management` skill. The request follows the GovernanceRequest state machine until approval or rejection.

## GovernanceRequest States

```
pending → local-approved / remote-approved → dual-approved → executed
        → rejected
```

## Usage

1. Compose GovernanceRequest payload with operation details
2. Submit via `amcos-permission-management` skill
3. Track state via `/amcos-check-approval-status` command
4. Execute only after `local-approved` (local) or `dual-approved` (cross-team)

## Operations Requiring GovernanceRequest

| Operation | Scope | Approvers | Elevation gate |
|-----------|-------|-----------|-----------|
| `spawn` | local | sourceManager | No |
| `spawn` | cross-team | sourceManager + targetManager | No |
| `terminate` | local | sourceManager | No |
| `terminate` | cross-team | sourceManager + targetManager | No |
| `hibernate` | local | sourceManager | No |
| `wake` | local | sourceManager | No |
| `install` | local | sourceManager | No |
| `install` | cross-team | sourceManager + targetManager | No |
| `replace` | any | sourceManager (+ targetManager) | No |
| `critical` | any | dual-manager | **USER via UI (R32)** |

Critical operations are additionally gated by an elevation password that is requested **only of
the USER, only via the AI Maestro UI** (R32). The COS never holds, passes, or submits one — there is
no password argument on this command and no password field in the payload.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--type <TYPE>` | **Yes** | Operation type |
| `--agent <NAME>` | **Yes** | Target agent name |
| `--reason <TEXT>` | **Yes** | Justification |
| `--scope <SCOPE>` | No | `local` (default) or `cross-team` |
| `--target-cos <NAME>` | If cross-team | Target COS session |
| `--target-manager <NAME>` | If cross-team | Target manager session |
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
  --scope cross-team --target-cos amcos-backend --target-manager amama-backend \
  --reason "Need worker on backend team for data migration"

# Critical operation (server elevation gate: the USER approves via the UI — R32; no password argument exists)
/amcos-request-approval --type critical --agent prod-deployer --urgent \
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
  "sourceManager": "amama-main",
  "targetCOS": null,
  "targetManager": null,
  "operation": {
    "action": "terminate",
    "target": "old-worker",
    "parameters": {}
  },
  "justification": "Agent has critical unrecoverable bug",
  "impact": {"scope": "local", "risk_level": "high"},
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
  "sourceManager": "amama-frontend",
  "targetCOS": "amcos-backend",
  "targetManager": "amama-backend",
  "operation": {
    "action": "spawn",
    "target": "backend-worker",
    "parameters": {}
  },
  "justification": "Need worker on backend team for data migration",
  "impact": {"scope": "cross-team", "risk_level": "medium"},
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
    sourceManager:  amama-main        [pending]
    targetManager:  n/a (local)

  Reason: Agent has critical unrecoverable bug

=======================================================================
  Use /amcos-check-approval-status --request-id GR-20260227150000-a1b2c3d4
=======================================================================
```

## Rate Limiting

- Max 10 GovernanceRequests/minute per COS
- Back off exponentially on repeated failures

## Tracking Location

```
~/.aimaestro/governance/pending/GR-20260227150000-a1b2c3d4.json
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Rate limited | Too many requests | Back off and retry |
| Elevation gate pending | Critical op awaiting the USER's UI approval (R32) | Wait; do not attempt to supply a password |
| Unknown target manager | Invalid targetManager | Query team registry |
| Service unreachable | AI Maestro down | Check if AI Maestro is running |
| Missing `--target-cos` | Cross-team without target | Provide target COS and manager |

## Related Commands

- `/amcos-check-approval-status` - Check GovernanceRequest state
- `/amcos-wait-for-approval` - Wait for approval with timeout
- `/amcos-notify-manager` - Send notification to manager
- `/amcos-staff-status` - View all agents
