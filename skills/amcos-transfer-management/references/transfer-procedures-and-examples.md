# Transfer Management Procedures and Examples

## Table of Contents

- [Initiating a Transfer (Outbound)](#initiating-a-transfer-outbound---from-your-team)
- [Approving a Transfer (Inbound)](#approving-a-transfer-inbound---into-your-team)
- [Rejecting a Transfer](#rejecting-a-transfer)
- [Transfer Checklist](#transfer-checklist)
- [AMP Notification Format](#amp-notification-format)
- [Example 1: Outbound Transfer](#example-1-outbound-transfer-moving-an-agent-out-of-your-team)
- [Example 2: Inbound Transfer Approval](#example-2-inbound-transfer-approval-accepting-an-agent-into-your-team)
- [Example 3: Rejecting a Transfer](#example-3-rejecting-a-transfer)

---

## Initiating a Transfer (Outbound - from YOUR team)

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

## Approving a Transfer (Inbound - into YOUR team)

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

## Rejecting a Transfer

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

## Transfer Checklist

Copy this checklist and track your progress:

- [ ] Identify agent and target team
- [ ] Verify agent is in current team roster
- [ ] Create TransferRequest with justification
- [ ] Submit GovernanceRequest to source manager
- [ ] Wait for source manager approval
- [ ] Submit GovernanceRequest to target manager
- [ ] Wait for target manager approval (dual-approved)
- [ ] Execute transfer: remove from source team, add to target team
- [ ] Notify both COS agents of completion
- [ ] Update local audit trail

## AMP Notification Format

All transfer-related AMP messages use these content types:

| Content Type | When Used |
|-------------|-----------|
| `transfer-approval-request` | Requesting an approval from a manager or COS |
| `transfer-approved` | Notifying that an approval was granted |
| `transfer-rejected` | Notifying that the transfer was rejected |
| `transfer-executed` | Notifying that the agent has been moved |

## Example 1: Outbound Transfer (Moving an agent OUT of your team)

**Scenario:** You are COS of team `team-alpha`. Agent `ampa-alpha-backend` has completed their project and is needed by `team-beta`.

```bash
# Step 1: Create the transfer request
curl -X POST "$AIMAESTRO_API/api/governance/transfers/" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "ampa-alpha-backend",
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
amp-send.sh "amama-main" "Transfer approval: ampa-alpha-backend -> team-beta" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: ampa-alpha-backend moving to team-beta. Please approve as source manager."}'

# Step 4: Notify target COS
amp-send.sh "amcos-beta" "Incoming transfer: ampa-alpha-backend" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: ampa-alpha-backend from team-alpha wants to join team-beta. Please review and approve."}'

# Step 5: After all 4 approvals received, execute
curl -X POST "$AIMAESTRO_API/api/governance/transfers/tr-001/execute" \
  -H "Content-Type: application/json"

# Step 6: Notify all parties
amp-send.sh "ampa-alpha-backend" "Transfer complete" \
  "high" '{"type": "transfer-executed", "message": "You have been transferred to team-beta. Your new COS is amcos-beta."}'
```

## Example 2: Inbound Transfer Approval (Accepting an agent INTO your team)

**Scenario:** You are COS of team `team-beta`. You receive an AMP notification that `ampa-alpha-backend` wants to join your team.

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
amp-send.sh "amama-main" "Transfer approval: ampa-alpha-backend into team-beta" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: I approved ampa-alpha-backend into team-beta as target COS. Please approve as target manager."}'
```

## Example 3: Rejecting a Transfer

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
