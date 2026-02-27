---
name: amcos-transfer-management
description: Use when an agent needs to be transferred between teams. Trigger with transfer requests, transfer approvals, or transfer status checks.
user-invocable: false
license: MIT
compatibility: "AI Maestro v0.26.0+"
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: amcos-chief-of-staff-main-agent
---

# AMCOS Transfer Management

## Overview

Transfer management handles the movement of agents between teams using the GovernanceRequest API. A transfer is a governed operation that requires dual-manager approval: both the source team manager and the target team manager must approve before the agent is moved.

This skill is **TEAM-SCOPED**: as COS, you can only initiate transfers OUT of your own team (you are the source-side approver), and accept/approve transfers INTO your own team (you are the target-side approver). You cannot initiate or approve transfers between two teams you do not manage.

**State Machine:**

```
pending → source-approved → target-approved → executed
   │            │                  │
   └────────────┴──────────────────┴──→ rejected
```

A rejection at any stage moves the request to the terminal `rejected` state.

## Prerequisites

Before using this skill, ensure:

1. AI Maestro v0.26.0+ is running locally
2. The GovernanceRequest API is accessible at `$AIMAESTRO_API` (default: `http://localhost:23000`)
3. The `agent-messaging` skill is available for inter-agent AMP notifications
4. `amp-send.sh` is available at `~/.local/bin/amp-send.sh`
5. You know your own team ID (the team you are COS of)
6. The agent to be transferred is an active member of the source team
7. The target team exists and has capacity for the agent

## Instructions

### Initiating a Transfer (Outbound - from YOUR team)

1. **Validate the agent** - Confirm the agent is an active member of YOUR team using the team registry
2. **Validate the target** - Confirm the target team exists and has capacity via `GET /api/teams/{target_team_id}`
3. **Check for existing requests** - Ensure the agent does not already have a pending TransferRequest
4. **Create the TransferRequest** - Submit to the GovernanceRequest API:
   ```bash
   curl -X POST "$AIMAESTRO_API/api/governance/transfers/" \
     -H "Content-Type: application/json" \
     -d '{
       "agent_id": "<agent-id>",
       "source_team_id": "<your-team-id>",
       "target_team_id": "<target-team-id>",
       "reason": "<justification for the transfer>",
       "requested_by": "<your-cos-id>"
     }'
   ```
5. **Record the TransferRequest ID** - Save the returned `id` for tracking
6. **Approve as source COS** - Submit your own approval for the source side:
   ```bash
   curl -X POST "$AIMAESTRO_API/api/governance/transfers/{id}/approve" \
     -H "Content-Type: application/json" \
     -d '{
       "approver_id": "<your-cos-id>",
       "approver_role": "source-cos",
       "decision": "approve",
       "comment": "Initiating transfer as source COS"
     }'
   ```
7. **Notify the source manager** - Send AMP message requesting their approval:
   ```bash
   amp-send.sh "<source-manager-session>" "Transfer approval needed" \
     "high" '{"type": "transfer-approval-request", "message": "TransferRequest <id> needs your approval as source manager. Agent <agent-id> transferring to team <target-team-id>. Reason: <reason>"}'
   ```
8. **Notify the target COS** - Send AMP message informing them of the incoming transfer:
   ```bash
   amp-send.sh "<target-cos-session>" "Incoming transfer request" \
     "high" '{"type": "transfer-approval-request", "message": "TransferRequest <id> requests agent <agent-id> to join your team from <source-team-id>. Reason: <reason>. Please review and approve/reject."}'
   ```
9. **Wait for all approvals** - Monitor the request state. The transfer advances through `source-approved` and `target-approved` as approvals arrive.
10. **Execute when dual-approved** - Once state reaches `target-approved` (all four approvals received), execute the transfer:
    ```bash
    curl -X POST "$AIMAESTRO_API/api/governance/transfers/{id}/execute" \
      -H "Content-Type: application/json"
    ```
11. **Update registries** - Update both source and target team registries to reflect the agent's new team membership

### Approving a Transfer (Inbound - into YOUR team)

1. **Receive the transfer notification** - Check AMP inbox for transfer-approval-request messages
2. **Review the request** - Retrieve the TransferRequest details:
   ```bash
   curl -s "$AIMAESTRO_API/api/governance/transfers/{id}" | jq .
   ```
3. **Evaluate fitness** - Assess whether the agent fits your team's needs and whether you have capacity
4. **Submit your approval (or rejection)** as target COS:
   ```bash
   curl -X POST "$AIMAESTRO_API/api/governance/transfers/{id}/approve" \
     -H "Content-Type: application/json" \
     -d '{
       "approver_id": "<your-cos-id>",
       "approver_role": "target-cos",
       "decision": "approve",
       "comment": "Agent accepted into target team"
     }'
   ```
5. **Notify your manager** - Send AMP message requesting the target manager's approval
6. **If rejecting**, use `"decision": "reject"` with a `comment` explaining why. The request moves to `rejected` immediately.

### Rejecting a Transfer

At any point during the approval process, any authorized approver can reject:

```bash
curl -X POST "$AIMAESTRO_API/api/governance/transfers/{id}/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "approver_id": "<your-id>",
    "approver_role": "<your-role>",
    "decision": "reject",
    "comment": "Reason for rejection"
  }'
```

After rejection, notify all involved parties via AMP that the transfer has been denied.

## Output

| Operation | Expected Output |
|-----------|----------------|
| Create TransferRequest | JSON with `id`, `state: "pending"`, `created_at` |
| Approve (source side complete) | State transitions to `source-approved` |
| Approve (target side complete) | State transitions to `target-approved` |
| Execute transfer | State transitions to `executed`, agent moved in registry |
| Reject transfer | State transitions to `rejected` at any stage |

### AMP Notification Format

All transfer-related AMP messages use these content types:

| Content Type | When Used |
|-------------|-----------|
| `transfer-approval-request` | Requesting an approval from a manager or COS |
| `transfer-approved` | Notifying that an approval was granted |
| `transfer-rejected` | Notifying that the transfer was rejected |
| `transfer-executed` | Notifying that the agent has been moved |

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `404` on create | Agent ID or team ID not found | Verify IDs via team registry and agent list before retrying |
| `409` on create | Agent already has a pending transfer | Wait for the existing transfer to complete or be rejected before creating a new one |
| `403` on approve | Caller is not an authorized approver for this transfer | Verify your role (source-cos, target-cos, source-manager, target-manager) matches your actual team relationship |
| `409` on approve | Request already in terminal state (executed/rejected) | No action needed; the request is finalized |
| AMP delivery failure | Target agent offline or session name wrong | Retry 3 times with 10-second intervals. If still failing, check agent status and session name in registry |
| Transfer executed but registry not updated | API succeeded but registry update failed | Manually update both team registries using the team registry script |
| Manager unresponsive | Approval pending for extended period | Send a reminder via AMP after 30 minutes. Escalate to EAMA after 2 hours. |

## Examples

### Example 1: Outbound Transfer (Moving an agent OUT of your team)

**Scenario:** You are COS of team `team-alpha`. Agent `epa-alpha-backend` has completed their project and is needed by `team-beta`.

```bash
# Step 1: Create the transfer request
curl -X POST "$AIMAESTRO_API/api/governance/transfers/" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "epa-alpha-backend",
    "source_team_id": "team-alpha",
    "target_team_id": "team-beta",
    "reason": "Backend work complete on alpha project. Agent skillset matches beta team needs.",
    "requested_by": "amcos-alpha"
  }'
# Response: {"id": "tr-001", "state": "pending", "created_at": "2026-02-27T10:00:00Z"}

# Step 2: Approve as source COS
curl -X POST "$AIMAESTRO_API/api/governance/transfers/tr-001/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "approver_id": "amcos-alpha",
    "approver_role": "source-cos",
    "decision": "approve",
    "comment": "Agent has completed all assigned tasks in team-alpha"
  }'

# Step 3: Notify source manager
amp-send.sh "eama-main" "Transfer approval: epa-alpha-backend → team-beta" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: epa-alpha-backend moving to team-beta. Please approve as source manager."}'

# Step 4: Notify target COS
amp-send.sh "amcos-beta" "Incoming transfer: epa-alpha-backend" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: epa-alpha-backend from team-alpha wants to join team-beta. Please review and approve."}'

# Step 5: After all 4 approvals received, execute
curl -X POST "$AIMAESTRO_API/api/governance/transfers/tr-001/execute" \
  -H "Content-Type: application/json"

# Step 6: Notify all parties
amp-send.sh "epa-alpha-backend" "Transfer complete" \
  "high" '{"type": "transfer-executed", "message": "You have been transferred to team-beta. Your new COS is amcos-beta."}'
```

### Example 2: Inbound Transfer Approval (Accepting an agent INTO your team)

**Scenario:** You are COS of team `team-beta`. You receive an AMP notification that `epa-alpha-backend` wants to join your team.

```bash
# Step 1: Check your inbox
curl -s "$AIMAESTRO_API/api/messages?agent=amcos-beta&action=list&status=unread" | jq '.messages[]'

# Step 2: Review the transfer request details
curl -s "$AIMAESTRO_API/api/governance/transfers/tr-001" | jq .
# Verify: agent capabilities match your team needs, you have capacity

# Step 3: Approve as target COS
curl -X POST "$AIMAESTRO_API/api/governance/transfers/tr-001/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "approver_id": "amcos-beta",
    "approver_role": "target-cos",
    "decision": "approve",
    "comment": "Agent capabilities match our team needs. We have capacity."
  }'

# Step 4: Notify your manager for their approval
amp-send.sh "eama-main" "Transfer approval: epa-alpha-backend into team-beta" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: I approved epa-alpha-backend into team-beta as target COS. Please approve as target manager."}'
```

### Example 3: Rejecting a Transfer

**Scenario:** You are COS of team `team-beta` and the incoming agent does not match your needs.

```bash
# Reject with explanation
curl -X POST "$AIMAESTRO_API/api/governance/transfers/tr-002/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "approver_id": "amcos-beta",
    "approver_role": "target-cos",
    "decision": "reject",
    "comment": "Team at full capacity. No open roles matching agent capabilities."
  }'

# Notify the source COS
amp-send.sh "amcos-alpha" "Transfer rejected: tr-002" \
  "normal" '{"type": "transfer-rejected", "message": "TransferRequest tr-002 rejected by target COS. Reason: Team at full capacity."}'
```

## Resources

- [op-create-transfer-request.md](references/op-create-transfer-request.md) - Step-by-step procedure for creating a TransferRequest, including payload format and error conditions
- [op-approve-transfer-request.md](references/op-approve-transfer-request.md) - Step-by-step procedure for approving or rejecting a TransferRequest, including the approval matrix and state transitions

---

**Version:** 1.0.0
**Last Updated:** 2026-02-27
**Target Audience:** Chief of Staff Agents
**Governance Version:** AI Maestro v0.26.0+
