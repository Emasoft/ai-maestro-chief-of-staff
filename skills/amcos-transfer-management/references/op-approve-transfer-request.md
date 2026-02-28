# OP: Approve Transfer Request

## Table of Contents

- [Purpose](#purpose)
- [Prerequisites](#prerequisites)
- [Approval Matrix](#approval-matrix)
- [Procedure](#procedure)
- [Request Payload](#request-payload)
- [State Transitions After Approval](#state-transitions-after-approval)
- [Error Conditions](#error-conditions)

## Purpose

Approve a pending TransferRequest. Both source and target sides must approve before execution.

## Prerequisites

- TransferRequest must exist and not be in `rejected` or `executed` state
- Approver must be an authorized approver (COS or manager of source/target team)

## Approval Matrix

| Approver Role | Approves For | Required State |
|---------------|-------------|----------------|
| Source COS | Source side | `pending` |
| Source Manager | Source side | `pending` |
| Target COS | Target side | `pending` or `source-approved` |
| Target Manager | Target side | `pending` or `source-approved` |

## Procedure

1. **Retrieve request** - Get the TransferRequest by ID
2. **Verify approver role** - Confirm the caller is an authorized approver
3. **Submit approval** - Call `POST /api/governance/transfers/{id}/approve` with payload
4. **State transition** - System updates state if all approvals for a side are complete

## Request Payload

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `approver_id` | string | yes | ID of the approving agent |
| `approver_role` | string | yes | `source-cos`, `source-manager`, `target-cos`, or `target-manager` |
| `decision` | string | yes | `approve` or `reject` |
| `comment` | string | no | Optional justification |

## State Transitions After Approval

| Current State | Event | New State |
|---------------|-------|-----------|
| `pending` | Both source approvals received | `source-approved` |
| `source-approved` | Both target approvals received | `target-approved` |
| `target-approved` | System executes transfer | `executed` |
| any | Any approver rejects | `rejected` |

## Error Conditions

- `404` - TransferRequest not found
- `403` - Caller is not an authorized approver
- `409` - Request already in terminal state (`executed` or `rejected`)
