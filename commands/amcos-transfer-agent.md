---
name: amcos-transfer-agent
description: Transfer an agent from the current team to a target team via GovernanceRequest
allowed_agents:
  - amcos-chief-of-staff
  - amcos-team-manager
---

# /amcos-transfer-agent

## Usage

```
/amcos-transfer-agent <agent-name> --to-team <team-id>
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<agent-name>` | yes | Name or ID of the agent to transfer |
| `--to-team <team-id>` | yes | Target team ID |
| `--reason <text>` | no | Justification (prompted if omitted) |

## Steps

1. **Validate agent** - Confirm `<agent-name>` is a member of the current team
2. **Create TransferRequest** - `POST /api/governance/transfers/` with agent, source team, target team, and reason
3. **Wait for approvals** - Monitor request state until all four approvals are received or a rejection occurs
4. **Report outcome** - Print final state (`executed` or `rejected`) with details

## Example

```
/amcos-transfer-agent agent-alpha --to-team team-backend --reason "Rebalancing workload"
```

## Notes

- Both source and target COS + managers must approve
- The command polls the transfer state until a terminal state is reached
- If rejected, the rejection reason and rejecting role are displayed
