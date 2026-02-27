---
name: amcos-transfer-management
description: Manages agent transfers between teams using GovernanceRequest API
author: Emasoft
version: 1.0.0
---

# AMCOS Transfer Management

## Overview

Manages agent transfers between teams using the GovernanceRequest API. A transfer moves an agent from a source team to a target team, requiring approval from both sides before execution.

## API Endpoint

```
POST /api/governance/transfers/
```

## TransferRequest States

| State | Description |
|-------|-------------|
| `pending` | Request created, awaiting source approval |
| `source-approved` | Source COS + manager approved |
| `target-approved` | Target COS + manager approved (both sides done) |
| `executed` | Agent successfully moved to target team |
| `rejected` | Transfer denied by any required approver |

**Flow:** `pending` → `source-approved` → `target-approved` → `executed` or `rejected`

- A rejection at any stage moves the request to `rejected`.
- Both source and target COS + managers must approve before execution.

## Operations

| Operation | Method | Path |
|-----------|--------|------|
| Create transfer request | `POST` | `/api/governance/transfers/` |
| Approve transfer | `POST` | `/api/governance/transfers/{id}/approve` |
| Execute transfer | `POST` | `/api/governance/transfers/{id}/execute` |
| Reject transfer | `POST` | `/api/governance/transfers/{id}/reject` |

## Approval Requirements

- **Source team:** COS approval + manager approval required
- **Target team:** COS approval + manager approval required
- All four approvals must be granted before execution

## References

- `references/op-create-transfer-request.md` - Procedure for creating a transfer request
- `references/op-approve-transfer-request.md` - Procedure for approving a transfer request
