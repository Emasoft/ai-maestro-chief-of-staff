---
name: amcos-transfer-management
description: Use when an agent needs to be transferred between teams. Trigger with transfer requests, transfer approvals, or transfer status checks.
user-invocable: false
license: Apache-2.0
compatibility: "AI Maestro v0.26.0+"
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ai-maestro-chief-of-staff-main-agent
---

# AMCOS Transfer Management

## Overview

Transfer management handles agent movement between teams using the GovernanceRequest API. Transfers require dual-manager approval: both source and target managers must approve before the agent is moved.

This skill is **TEAM-SCOPED**: you can only initiate transfers OUT of your team and accept transfers INTO your team.

**State Machine:** `pending -> source-approved -> target-approved -> executed` (rejection at any stage moves to `rejected`)

## Prerequisites

1. AI Maestro v0.26.0+ running locally
2. GovernanceRequest API accessible at `$AIMAESTRO_API`
3. `agent-messaging` skill and `amp-send.sh` available
4. Agent to transfer is active in source team; target team exists with capacity

## Instructions

1. Identify the agent to transfer and the target team
2. Verify the agent is active in your team and the target team has capacity
3. Submit a TransferRequest via `POST /api/v1/governance/requests` with `operation: "agent-transfer"`
4. Obtain source manager approval (your side)
5. Notify target team manager via AMP and await their approval
6. Once dual-approved, the system executes the transfer automatically
7. Verify agent appears in target team roster and is removed from source roster

Copy this checklist and track your progress:

- [ ] Confirm agent is active in source team
- [ ] Verify target team exists and has capacity
- [ ] Submit TransferRequest and obtain requestId
- [ ] Get source and target manager approvals
- [ ] Verify transfer executed and rosters updated

See `references/transfer-procedures-and-examples.md` for detailed API calls.

## Output

| Operation | Expected Output |
|-----------|----------------|
| Create TransferRequest | JSON with `id`, `state: "pending"` |
| Approve (source side) | State transitions to `source-approved` |
| Approve (target side) | State transitions to `target-approved` |
| Execute transfer | State transitions to `executed` |
| Reject transfer | State transitions to `rejected` |

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `404` on create | Agent/team ID not found | Verify IDs via registry |
| `409` on create | Pending transfer exists | Wait for existing to complete |
| `403` on approve | Not authorized approver | Verify your role matches |
| `409` on approve | Already in terminal state | No action needed |
| AMP delivery failure | Agent offline | Retry 3x with 10s intervals |
| Manager unresponsive | Approval pending | Remind after 30min, escalate after 2h |

## Examples

**Input:** Transfer agent `libs-svg-renderer` from team `libs-svg` to team `apps-editor`

**Output:** `{"requestId": "tr-0017", "state": "pending"}` -> source approves -> target approves -> `{"state": "executed", "agent": "libs-svg-renderer", "newTeam": "apps-editor"}`

See `references/transfer-procedures-and-examples.md` for full examples.

## Resources

- `references/transfer-procedures-and-examples.md`
- `references/op-create-transfer-request.md` - Creating a TransferRequest
- `references/op-approve-transfer-request.md` - Approving/rejecting transfers

---

**Version:** 1.0.0
**Last Updated:** 2026-02-27
