# OP: Create Transfer Request

## Purpose

Create a new TransferRequest to move an agent from the source team to a target team.

## Prerequisites

- Agent must be an active member of the source team
- Requester must have permission to initiate transfers
- Target team must exist and have capacity

## Procedure

1. **Validate agent membership** - Confirm the agent belongs to the current (source) team
2. **Validate target team** - Confirm target team exists and can accept the agent
3. **Submit request** - Call `POST /api/governance/transfers/` with payload
4. **Notify approvers** - Source COS, source manager, target COS, target manager

## Request Payload

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | yes | ID of the agent to transfer |
| `source_team_id` | string | yes | Current team of the agent |
| `target_team_id` | string | yes | Destination team |
| `reason` | string | yes | Justification for the transfer |
| `requested_by` | string | yes | ID of the requester |

## Response

| Field | Value |
|-------|-------|
| `id` | Unique TransferRequest ID |
| `state` | `pending` |
| `created_at` | Timestamp |

## Error Conditions

- `404` - Agent or team not found
- `409` - Agent already has a pending transfer
- `403` - Requester lacks permission
