---
name: op-sync-registry-with-labels
description: Operation procedure for synchronizing team registry with GitHub issue labels.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Sync Registry with Labels


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Load Current Registry](#step-1-load-current-registry)
  - [Step 2: For Each Agent, Compare Registry vs Labels](#step-2-for-each-agent-compare-registry-vs-labels)
  - [Step 3: Identify Discrepancies](#step-3-identify-discrepancies)
  - [Step 4: Reconcile Registry to Match Labels](#step-4-reconcile-registry-to-match-labels)
  - [Step 5: Handle Orphaned Labels](#step-5-handle-orphaned-labels)
  - [Step 6: Log Sync Results](#step-6-log-sync-results)
- [Example](#example)
- [Automated Sync Script](#automated-sync-script)
- [Error Handling](#error-handling)

## Purpose

Ensure the team registry (via AI Maestro REST API) stays synchronized with GitHub issue assignment labels. Detect and resolve discrepancies.

## When to Use

- Periodically (recommended: every 10 minutes during active work)
- After agent spawn or termination
- When inconsistencies are suspected
- Before generating status reports

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Access to AI Maestro REST API (`$AIMAESTRO_API`, default `http://localhost:23000`)
- `jq` installed for JSON processing

## Procedure

### Step 1: Load Current Registry

```bash
REGISTRY=$(curl -s "$AIMAESTRO_API/api/teams/default/agents")
AGENTS=$(echo $REGISTRY | jq -r '.[].name')
```

### Step 2: For Each Agent, Compare Registry vs Labels

```bash
for AGENT in $AGENTS; do
  # Get issues from registry via REST API
  REGISTERED=$(curl -s "$AIMAESTRO_API/api/agents/$AGENT" | jq -r '.current_issues | sort | .[]' 2>/dev/null)

  # Get issues from GitHub labels
  LABELED=$(gh issue list --label "assign:$AGENT" --json number --jq '.[].number' | sort)

  echo "Agent: $AGENT"
  echo "  Registry: $REGISTERED"
  echo "  Labeled:  $LABELED"
done
```

### Step 3: Identify Discrepancies

For each agent:

| Situation | Meaning | Action |
|-----------|---------|--------|
| In registry, not labeled | Registry stale | Remove from registry |
| Labeled, not in registry | Registry outdated | Add to registry |
| Both match | Synchronized | No action needed |

### Step 4: Reconcile Registry to Match Labels

Labels are source of truth. Update registry:

```bash
for AGENT in $AGENTS; do
  # Get actual labeled issues
  LABELED_ISSUES=$(gh issue list --label "assign:$AGENT" --state open --json number --jq '[.[].number]')

  # Update registry via REST API
  curl -X PATCH "$AIMAESTRO_API/api/agents/$AGENT" \
    -H "Content-Type: application/json" \
    -d '{"current_issues": '"$LABELED_ISSUES"'}'
done
```

### Step 5: Handle Orphaned Labels

Find labels for agents not in registry:

```bash
# Get all assign:* labels in repo
ALL_ASSIGN_LABELS=$(gh label list --json name --jq '.[] | select(.name | startswith("assign:")) | .name')

for LABEL in $ALL_ASSIGN_LABELS; do
  AGENT_NAME=$(echo $LABEL | sed 's/assign://')

  # Check if agent exists in registry via REST API
  EXISTS=$(curl -s "$AIMAESTRO_API/api/agents/$AGENT_NAME" | jq -r '.name // empty')

  if [ -z "$EXISTS" ]; then
    echo "WARNING: Label '$LABEL' exists but agent not in registry"
    # Either register agent or remove labels
  fi
done
```

### Step 6: Log Sync Results

```bash
echo "Sync completed at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> docs_dev/sync-log.txt
```

## Example

**Scenario:** Check sync for agent `implementer-1`.

```bash
# Get labeled issues
LABELED=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number' | sort)
echo "Labeled: $LABELED"

# Get registered issues via REST API
REGISTERED=$(curl -s "$AIMAESTRO_API/api/agents/implementer-1" | jq -r '.current_issues | sort | .[]')
echo "Registered: $REGISTERED"

# Compare
if [ "$LABELED" = "$REGISTERED" ]; then
  echo "SYNC OK: Registry matches labels"
else
  echo "SYNC NEEDED: Discrepancy detected"
  # Update registry via REST API
  LABELED_JSON=$(gh issue list --label "assign:implementer-1" --state open --json number --jq '[.[].number]')
  curl -X PATCH "$AIMAESTRO_API/api/agents/implementer-1" \
    -H "Content-Type: application/json" \
    -d '{"current_issues": '"$LABELED_JSON"'}'
fi
```

## Automated Sync Script

For scheduled sync, create a script:

```bash
#!/bin/bash
# scripts/amcos_sync_labels.sh

AIMAESTRO_API="${AIMAESTRO_API:-http://localhost:23000}"

# Get all agents from registry via REST API
AGENTS=$(curl -s "$AIMAESTRO_API/api/teams/default/agents" | jq -r '.[].name')

for AGENT in $AGENTS; do
  # Get labeled issues (open only)
  LABELED=$(gh issue list --label "assign:$AGENT" --state open --json number --jq '[.[].number]')

  # Update registry via REST API
  curl -X PATCH "$AIMAESTRO_API/api/agents/$AGENT" \
    -H "Content-Type: application/json" \
    -d '{"current_issues": '"$LABELED"'}'
done

echo "Sync complete: $(date)"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| JSON parse error | Malformed API response | Check AI Maestro API health at `$AIMAESTRO_API` |
| gh rate limited | Too many API calls | Wait and retry with exponential backoff |
| Registry API unreachable | AI Maestro API down | Verify API is running at `$AIMAESTRO_API` |
| Agent not found | Agent not registered | Register agent with `POST $AIMAESTRO_API/api/agents/register` |
