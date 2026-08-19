---
name: op-track-pending-approvals
description: Operation procedure for tracking multiple pending approval requests.
---

# Operation: Track Pending Approvals


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Initialize Tracking File](#step-1-initialize-tracking-file)
  - [Step 2: Register New Request](#step-2-register-new-request)
  - [Step 3: Check Pending Requests Status](#step-3-check-pending-requests-status)
  - [Step 4: Poll for Responses](#step-4-poll-for-responses)
  - [Step 5: Check for Timeouts](#step-5-check-for-timeouts)
  - [Step 6: Update Tracking on Resolution](#step-6-update-tracking-on-resolution)
  - [Step 7: Generate Status Report](#step-7-generate-status-report)
- [Example](#example)
- [Tracking State Schema](#tracking-state-schema)
- [Error Handling](#error-handling)
- [Notes](#notes)

## Purpose

Maintain tracking of all outstanding approval requests to manage multiple concurrent operations and ensure timely responses.

## When to Use

- When managing multiple approval requests simultaneously
- When checking status of pending operations
- When generating status reports
- When handling escalation timing

## Prerequisites

- The `aimaestro-governance.sh` CLI on PATH (the frozen wrapper over the governance API)
- Request IDs from submitted approval requests
- AI Maestro for checking responses

## Procedure

### Step 1: Verify Governance Access

```bash
# Use the frozen aimaestro-governance.sh CLI (never call the API directly)
# Listing pending requests confirms governance is reachable
aimaestro-governance.sh requests --status pending
```

### Step 2: Register New Request

When submitting a new approval request:

```bash
TYPE="$1"            # request type (e.g. agent_spawn)
TARGET_HOST="$2"     # target host id
AGENT="$3"           # subject agent id

# Use the frozen aimaestro-governance.sh CLI (never call the API directly; auth via AID — R28, no password)
aimaestro-governance.sh request \
  --type "$TYPE" \
  --target-host "$TARGET_HOST" \
  --requested-by "amcos-chief-of-staff" \
  --role "chief-of-staff" \
  --agent "$AGENT"
```

### Step 3: Check Pending Requests Status

```bash
# Use the frozen aimaestro-governance.sh CLI (never call the API directly)
# List all pending requests
aimaestro-governance.sh requests --status pending | jq '.[] | {
  id: .request_id,
  operation: .operation,
  target: .target,
  requested_at: .requested_at
}'
```

### Step 4: Poll for Responses

```bash
# Use the frozen aimaestro-governance.sh CLI (never call the API directly)
# Get all pending request IDs (fetch to file, then parse)
aimaestro-governance.sh requests --status pending > /tmp/amcos-pending.json
PENDING_IDS=$(jq -r '.[].request_id' /tmp/amcos-pending.json)

for REQUEST_ID in $PENDING_IDS; do
  # Check AI Maestro inbox for response
  # Use the amp-inbox CLI to check for unread messages matching the request ID
  RESPONSE=$(check_messages_for_request_id "$REQUEST_ID" "approval-response")

  if [ -n "$RESPONSE" ]; then
    DECISION=$(echo $RESPONSE | jq -r '.content.decision')
    echo "Response received for $REQUEST_ID: $DECISION"

    # Apply the decision via the CLI (approve or reject)
    if [ "$DECISION" = "approved" ]; then
      aimaestro-governance.sh approve "$REQUEST_ID"
    elif [ "$DECISION" = "rejected" ]; then
      aimaestro-governance.sh reject "$REQUEST_ID"
    fi
  fi
done
```

### Step 5: Check for Timeouts

```bash
# Use the frozen aimaestro-governance.sh CLI (never call the API directly)
# List pending requests, then compute age client-side from requested_at to
# decide which need a 60s reminder or a 90s urgent escalation.
aimaestro-governance.sh requests --status pending > /tmp/amcos-pending.json

NOW=$(date -u +%s)
NEEDS_REMINDER=$(jq -r --argjson now "$NOW" \
  '.[] | select(((.requested_at | fromdateiso8601) + 60) <= $now) | .request_id' \
  /tmp/amcos-pending.json)
NEEDS_URGENT=$(jq -r --argjson now "$NOW" \
  '.[] | select(((.requested_at | fromdateiso8601) + 90) <= $now) | .request_id' \
  /tmp/amcos-pending.json)

echo "Needs reminder: $NEEDS_REMINDER"
echo "Needs urgent: $NEEDS_URGENT"
```

### Step 6: Update Tracking on Resolution

When approval is received:

```bash
REQUEST_ID="$1"
DECISION="$2"        # approved | rejected

# Use the frozen aimaestro-governance.sh CLI (never call the API directly; auth via AID — R28, no password)
# Apply the final decision — the CLI records decided_at / decided_by server-side
if [ "$DECISION" = "approved" ]; then
  aimaestro-governance.sh approve "$REQUEST_ID"
else
  aimaestro-governance.sh reject "$REQUEST_ID"
fi
```

### Step 7: Generate Status Report

```bash
# Use the frozen aimaestro-governance.sh CLI (never call the API directly)
# Count pending by type
echo "=== Pending Approvals Status ==="
aimaestro-governance.sh requests --status pending | jq -r 'group_by(.operation) | map({
  operation: .[0].operation,
  count: length
}) | .[] | "\(.operation): \(.count) pending"'

# Recently approved requests
echo "=== Recent Resolutions ==="
aimaestro-governance.sh requests --status approved \
  | jq -r '.[] | "\(.operation) \(.target): \(.status)"' | head -n 5
```

## Example

**Scenario:** Track multiple pending approvals for spawn, terminate, and plugin install.

```bash
# Use the frozen aimaestro-governance.sh CLI (never call the API directly)

# Current state after multiple requests
aimaestro-governance.sh requests --status pending
# Returns JSON array of pending requests:
# [
#   {"request_id": "abc-123", "operation": "spawn", "target": "implementer-2", "requested_at": "2025-02-05T10:00:00Z", "status": "pending"},
#   {"request_id": "def-456", "operation": "terminate", "target": "test-runner-1", "requested_at": "2025-02-05T10:01:00Z", "status": "pending"}
# ]

# Check for aged requests needing escalation (older than 60s) — filter client-side on requested_at
aimaestro-governance.sh requests --status pending \
  | jq --argjson now "$(date -u +%s)" \
      '.[] | select(((.requested_at | fromdateiso8601) + 60) <= $now) | {id: .request_id, operation: .operation}'
```

## Tracking State Schema

```json
{
  "pending": {
    "<request_id>": {
      "operation": "spawn|terminate|hibernate|wake|plugin_install",
      "target": "agent_name or plugin_name",
      "requested_at": "ISO-8601",
      "status": "pending|approved|rejected|modified|timeout",
      "reminder_sent": false,
      "urgent_sent": false
    }
  },
  "resolved": [
    {
      "operation": "spawn",
      "target": "implementer-1",
      "requested_at": "ISO-8601",
      "decision": "approved",
      "decided_at": "ISO-8601",
      "decided_by": "eama"
    }
  ]
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| CLI prints `Error: request … failed (network)` | AI Maestro not running | Start AI Maestro service, retry |
| JSON parse error on CLI output | Malformed response | Check AI Maestro logs for errors |
| CLI prints `Error: HTTP 404` | Already resolved or never registered | Re-run `aimaestro-governance.sh requests --status approved` to confirm |
| Concurrent updates | Multiple concurrent approve/reject calls | AI Maestro handles atomicity server-side |

## Notes

- Keep resolved list bounded (e.g., last 100 entries)
- Archive old resolved entries to audit log
- Use request IDs consistently across all operations
- Clean up stale pending entries (>1 hour without resolution)
