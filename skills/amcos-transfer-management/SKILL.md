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
agent: amcos-chief-of-staff-main-agent
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

> **Output Rule**: All AMCOS scripts produce 2-line stdout summaries. Full output is written to `.amcos-logs/`.

Transfer procedures involve creating a TransferRequest, obtaining dual approvals, and executing the move. See `references/transfer-procedures-and-examples.md` for detailed step-by-step procedures and API calls.
  - [Initiating a Transfer (Outbound)](#initiating-a-transfer-outbound---from-your-team)
  - [Approving a Transfer (Inbound)](#approving-a-transfer-inbound---into-your-team)
  - [Rejecting a Transfer](#rejecting-a-transfer)
  - [Transfer Checklist](#transfer-checklist)
  - [AMP Notification Format](#amp-notification-format)

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

See `references/transfer-procedures-and-examples.md` for full examples.
  - [Example 1: Outbound Transfer](#example-1-outbound-transfer-moving-an-agent-out-of-your-team)
  - [Example 2: Inbound Transfer Approval](#example-2-inbound-transfer-approval-accepting-an-agent-into-your-team)
  - [Example 3: Rejecting a Transfer](#example-3-rejecting-a-transfer)

## Resources

- `references/transfer-procedures-and-examples.md`
- `references/op-create-transfer-request.md` - Creating a TransferRequest
- `references/op-approve-transfer-request.md` - Approving/rejecting transfers

---

**Version:** 1.0.0
**Last Updated:** 2026-02-27
