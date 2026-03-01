# Quick Fix: Replace File-Based jq Patterns with REST API Equivalents
Generated: 2026-02-27

## Changes Made

### File: `skills/amcos-permission-management/references/approval-workflow-engine.md`
- Section 3.2: Replaced file location `pending-approvals.json` with REST API source note
- Section 3.3: Replaced `jq ... pending-approvals.json > tmp && mv tmp` with `curl -s -X PATCH "$AIMAESTRO_API/api/v1/governance/requests/<id>"`
- Section 5.3: Replaced json snippet + file update note with `curl -s -X PATCH` example
- Section 6.2: Replaced "Update status to timeout in pending-approvals.json" with REST API PATCH call
- Section 7.4: Replaced `jq ... pending-approvals.json` with `curl -s -X PATCH` for approved status
- Section 8.1: Replaced `jq ... pending-approvals.json` with `curl -s -X PATCH` for executing status

### File: `skills/amcos-permission-management/references/op-request-approval.md`
- Step 5: Replaced `jq ... $PENDING_FILE > temp.json && mv` with `curl -s -X POST "$AIMAESTRO_API/api/v1/governance/requests"`

### File: `skills/amcos-permission-management/references/op-track-pending-approvals.md`
- Prerequisites: Replaced file path with REST API endpoint reference
- Step 1: Replaced `mkdir -p` + file init with API health check curl
- Step 2: Replaced `jq ... $PENDING_FILE > temp.json && mv` with `curl -s -X POST`
- Step 3: Replaced `jq '.pending | to_entries[]'` with `curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending" | jq`
- Step 4: Replaced `jq -r '.pending | keys[]' $PENDING_FILE` with API call + PATCH for updates
- Step 5: Replaced `jq ... $PENDING_FILE` timeout checks with `curl` with `?min_age_seconds=` query params
- Step 6: Replaced `jq ... $PENDING_FILE > temp.json && mv` with `curl -s -X PATCH`
- Step 7: Replaced `jq -r '.pending | group_by'` with REST API calls
- Example: Replaced `cat $PENDING_FILE` + `jq` with `curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending"`
- Error Handling: Replaced file-based errors with API-based equivalents

### File: `skills/amcos-permission-management/references/op-handle-approval-timeout.md`
- Prerequisites: Replaced file path with REST API endpoint
- Step 1: Added curl command to query request by ID via REST API

### File: `skills/amcos-agent-lifecycle/references/op-update-team-registry.md`
- Prerequisites: Replaced file path reference with REST API verification
- Step 5: Replaced `cp .ai-maestro/team-registry.json .ai-maestro/team-registry.backup.*` with REST API state snapshot via `curl`

### File: `skills/amcos-agent-lifecycle/references/op-hibernate-agent.md`
- Error table: Replaced "manually edit team-registry.json" with REST API verification command

### File: `skills/amcos-agent-lifecycle/references/workflow-checklists.md`
- Checklist "Forming Team": Replaced file existence check with `curl -s "$AIMAESTRO_API/api/teams"` verification
- Checklist "Updating Team Registry": Replaced `cp` backup with REST API snapshot command

## Verification
- Post-edit grep for `jq.*pending-approvals.json` in skills/*/references/*.md: 0 matches (PASS)
- Post-edit grep for `jq.*team-registry.json` in skills/*/references/*.md: 0 matches (PASS)
- Post-edit grep for `PENDING_FILE=` in skills/*/references/*.md: 0 matches (PASS)
- Pattern followed: REST API via `curl -s "$AIMAESTRO_API/api/v1/governance/requests"` and `curl -s "$AIMAESTRO_API/api/teams"`

## Files Modified
1. `skills/amcos-permission-management/references/approval-workflow-engine.md` - 6 jq/file patterns replaced
2. `skills/amcos-permission-management/references/op-request-approval.md` - 1 jq/file pattern replaced
3. `skills/amcos-permission-management/references/op-track-pending-approvals.md` - 9 jq/file patterns replaced
4. `skills/amcos-permission-management/references/op-handle-approval-timeout.md` - 2 file references updated
5. `skills/amcos-agent-lifecycle/references/op-update-team-registry.md` - 2 file references replaced
6. `skills/amcos-agent-lifecycle/references/op-hibernate-agent.md` - 1 error table entry replaced
7. `skills/amcos-agent-lifecycle/references/workflow-checklists.md` - 2 checklist items replaced

## Notes
- `record-keeping.md` and `workflow-examples.md` references to `team-registry.json` are prose documentation (example paths in narrative), not jq commands - left as-is
- `op-deliver-role-briefing.md` reference is inside a quoted message string for agent briefing - left as-is (informational content, not an executable command)
- The `success-criteria.md` file was already using REST API curl calls - no changes needed there
