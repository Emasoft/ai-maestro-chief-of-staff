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
2. **Validate the target** - Confirm the target team exists and has capacity by inspecting the teams list: `aimaestro-teams.sh list | jq '.[] | select(.id == "<target-team-id>")'`
3. **Check for existing requests** - Ensure the agent does not already have a pending TransferRequest: `aimaestro-governance.sh transfer list --agent <agent-id> --status pending`
4. **Create the TransferRequest** - Submit via the frozen governance CLI (export `AID_AUTH` first — the server reads `requestedBy` from the authenticated identity):
   ```bash
   aimaestro-governance.sh transfer create \
     --agent "<agent-id>" \
     --from-team "<your-team-id>" \
     --to-team "<target-team-id>" \
     --note "<justification for the transfer>"
   ```
5. **Record the TransferRequest ID** - Save the returned **id** value for tracking
6. **Approve as source COS** - Resolve your own (source) approval via the CLI:
   ```bash
   aimaestro-governance.sh transfer resolve <id> --action approve
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
9. **Wait for all approvals** - Monitor the request state with `aimaestro-governance.sh transfer list --agent <agent-id>`. The transfer advances through `source-approved` and `target-approved` as approvals arrive.
10. **Execution on dual-approval** - The transfer executes automatically once all four approvals land (state reaches `target-approved` → `executed`). The frozen CLI has no separate `execute` verb; confirm completion via `aimaestro-governance.sh transfer list --agent <agent-id> --status executed`.
11. **Update registries** - Update both source and target team registries to reflect the agent's new team membership

## Approving a Transfer (Inbound - into YOUR team)

1. **Receive the transfer notification** - Check AMP inbox for transfer-approval-request messages
2. **Review the request** - Retrieve the TransferRequest details from the list:
   ```bash
   aimaestro-governance.sh transfer list | jq '.[] | select(.id == "<id>")'
   ```
3. **Evaluate fitness** - Assess whether the agent fits your team's needs and whether you have capacity
4. **Submit your approval (or rejection)** as target COS:
   ```bash
   aimaestro-governance.sh transfer resolve <id> --action approve
   ```
5. **Notify your manager** - Send AMP message requesting the target manager's approval
6. **If rejecting**, use `--action reject` with `--reject-reason` explaining why. The request moves to `rejected` immediately.

## Rejecting a Transfer

At any point during the approval process, any authorized approver can reject:

```bash
aimaestro-governance.sh transfer resolve <id> --action reject --reject-reason "Reason for rejection"
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
# Step 1: Create the transfer request (export AID_AUTH first — the server reads requestedBy from it)
aimaestro-governance.sh transfer create \
  --agent "ampa-alpha-backend" \
  --from-team "team-alpha" \
  --to-team "team-beta" \
  --note "Backend work complete on alpha project. Agent skillset matches beta team needs."
# Response: {"id": "tr-001", "state": "pending", "created_at": "2026-02-27T10:00:00Z"}

# Step 2: Approve as source COS
aimaestro-governance.sh transfer resolve tr-001 --action approve

# Step 3: Notify source manager
amp-send.sh "amama-main" "Transfer approval: ampa-alpha-backend -> team-beta" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: ampa-alpha-backend moving to team-beta. Please approve as source manager."}'

# Step 4: Notify target COS
amp-send.sh "amcos-beta" "Incoming transfer: ampa-alpha-backend" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: ampa-alpha-backend from team-alpha wants to join team-beta. Please review and approve."}'

# Step 5: All 4 approvals received -> the transfer executes automatically; confirm it landed
aimaestro-governance.sh transfer list --agent ampa-alpha-backend --status executed

# Step 6: Notify all parties
amp-send.sh "ampa-alpha-backend" "Transfer complete" \
  "high" '{"type": "transfer-executed", "message": "You have been transferred to team-beta. Your new COS is amcos-beta."}'
```

## Example 2: Inbound Transfer Approval (Accepting an agent INTO your team)

**Scenario:** You are COS of team `team-beta`. You receive an AMP notification that `ampa-alpha-backend` wants to join your team.

```bash
# Step 1: Check your inbox (use the agent-messaging skill, or amp-inbox.sh directly)
amp-inbox.sh

# Step 2: Review the transfer request details
aimaestro-governance.sh transfer list | jq '.[] | select(.id == "tr-001")'
# Verify: agent capabilities match your team needs, you have capacity

# Step 3: Approve as target COS
aimaestro-governance.sh transfer resolve tr-001 --action approve

# Step 4: Notify your manager for their approval
amp-send.sh "amama-main" "Transfer approval: ampa-alpha-backend into team-beta" \
  "high" '{"type": "transfer-approval-request", "message": "TransferRequest tr-001: I approved ampa-alpha-backend into team-beta as target COS. Please approve as target manager."}'
```

## Example 3: Rejecting a Transfer

**Scenario:** You are COS of team `team-beta` and the incoming agent does not match your needs.

```bash
# Reject with explanation
aimaestro-governance.sh transfer resolve tr-002 --action reject \
  --reject-reason "Team at full capacity. No open roles matching agent capabilities."

# Notify the source COS
amp-send.sh "amcos-alpha" "Transfer rejected: tr-002" \
  "normal" '{"type": "transfer-rejected", "message": "TransferRequest tr-002 rejected by target COS. Reason: Team at full capacity."}'
```
