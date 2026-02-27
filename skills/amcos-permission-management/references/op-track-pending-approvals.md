---
name: op-track-pending-approvals
description: Operation procedure for tracking multiple pending approval requests.
workflow-instruction: "support"
procedure: "support-skill"
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

- AI Maestro running with governance API accessible at `$AIMAESTRO_API/api/v1/governance/requests`
- Request IDs from submitted approval requests
- AI Maestro for checking responses

## Procedure

### Step 1: Verify Governance API Accessible

```bash
# Uses AI Maestro REST API (not file-based)
# Verify the governance API is reachable
curl -s -o /dev/null -w "%{http_code}" "$AIMAESTRO_API/api/v1/governance/requests?status=pending"
```

### Step 2: Register New Request

When submitting a new approval request:

```bash
REQUEST_ID="$1"
OPERATION="$2"
TARGET="$3"

# Uses AI Maestro REST API (not file-based)
curl -s -X POST "$AIMAESTRO_API/api/v1/governance/requests" \
  -H "Content-Type: application/json" \
  -d "{
    \"request_id\": \"$REQUEST_ID\",
    \"operation\": \"$OPERATION\",
    \"target\": \"$TARGET\",
    \"requested_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"status\": \"pending\",
    \"reminder_sent\": false,
    \"urgent_sent\": false
  }"
```

### Step 3: Check Pending Requests Status

```bash
# Uses AI Maestro REST API (not file-based)
# List all pending requests
curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending" | jq '.[] | {
  id: .request_id,
  operation: .operation,
  target: .target,
  requested_at: .requested_at
}'
```

### Step 4: Poll for Responses

```bash
# Uses AI Maestro REST API (not file-based)
# Get all pending request IDs
PENDING_IDS=$(curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending" | jq -r '.[].request_id')

for REQUEST_ID in $PENDING_IDS; do
  # Check AI Maestro inbox for response
  # Use the agent-messaging skill to check for unread messages matching the request ID
  RESPONSE=$(check_messages_for_request_id "$REQUEST_ID" "approval-response")

  if [ -n "$RESPONSE" ]; then
    DECISION=$(echo $RESPONSE | jq -r '.content.decision')
    echo "Response received for $REQUEST_ID: $DECISION"

    # Update status via REST API
    curl -s -X PATCH "$AIMAESTRO_API/api/v1/governance/requests/$REQUEST_ID" \
      -H "Content-Type: application/json" \
      -d "{\"status\": \"$DECISION\"}"
  fi
done
```

### Step 5: Check for Timeouts

```bash
# Uses AI Maestro REST API (not file-based)
# Find requests older than 60 seconds without reminder
NEEDS_REMINDER=$(curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending&reminder_sent=false&min_age_seconds=60" \
  | jq -r '.[].request_id')

# Find requests older than 90 seconds without urgent
NEEDS_URGENT=$(curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending&urgent_sent=false&min_age_seconds=90" \
  | jq -r '.[].request_id')

echo "Needs reminder: $NEEDS_REMINDER"
echo "Needs urgent: $NEEDS_URGENT"
```

### Step 6: Update Tracking on Resolution

When approval is received:

```bash
REQUEST_ID="$1"
DECISION="$2"
DECIDED_BY="$3"

# Uses AI Maestro REST API (not file-based)
# Update the request with decision and move to resolved
curl -s -X PATCH "$AIMAESTRO_API/api/v1/governance/requests/$REQUEST_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"status\": \"$DECISION\",
    \"decided_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"decided_by\": \"$DECIDED_BY\"
  }"
```

### Step 7: Generate Status Report

```bash
# Uses AI Maestro REST API (not file-based)
# Count pending by type
echo "=== Pending Approvals Status ==="
curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending" | jq -r 'group_by(.operation) | map({
  operation: .[0].operation,
  count: length
}) | .[] | "\(.operation): \(.count) pending"'

# Recent resolutions
echo "=== Recent Resolutions ==="
curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=resolved&limit=5" \
  | jq -r '.[] | "\(.operation) \(.target): \(.status)"'
```

## Example

**Scenario:** Track multiple pending approvals for spawn, terminate, and plugin install.

```bash
# Uses AI Maestro REST API (not file-based)

# Current state after multiple requests
curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending"
# Returns JSON array of pending requests:
# [
#   {"request_id": "abc-123", "operation": "spawn", "target": "implementer-2", "requested_at": "2025-02-05T10:00:00Z", "status": "pending"},
#   {"request_id": "def-456", "operation": "terminate", "target": "test-runner-1", "requested_at": "2025-02-05T10:01:00Z", "status": "pending"}
# ]

# Check for aged requests needing escalation (older than 60s)
curl -s "$AIMAESTRO_API/api/v1/governance/requests?status=pending&min_age_seconds=60" \
  | jq '.[] | {id: .request_id, operation: .operation}'
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
| API unreachable (non-200) | AI Maestro not running | Start AI Maestro service, retry |
| JSON parse error from API | Malformed response | Check AI Maestro logs for errors |
| Request ID not found (404) | Already resolved or never registered | Query resolved requests endpoint |
| Concurrent updates | Multiple concurrent PATCH requests | AI Maestro handles atomicity server-side |

## Notes

- Keep resolved list bounded (e.g., last 100 entries)
- Archive old resolved entries to audit log
- Use request IDs consistently across all operations
- Clean up stale pending entries (>1 hour without resolution)
