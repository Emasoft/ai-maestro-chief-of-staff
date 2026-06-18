---
name: op-sync-registry-with-labels
description: Operation procedure for synchronizing team registry with GitHub issue labels.
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

Ensure the team registry stays synchronized with GitHub issue assignment labels. Detect and resolve discrepancies.

> **Note**: The registry side of this sync — reading and writing an agent's
> `current_issues` from GitHub issue labels — has **no** frozen-CLI verb yet.
> <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->
> Until that verb ships, the registry-update steps below are blocked; the
> GitHub-label side (via `gh`) and the team-roster read (via the
> `ai-maestro-agents-management` skill) remain available.

## When to Use

- Periodically (recommended: every 10 minutes during active work)
- After agent spawn or termination
- When inconsistencies are suspected
- Before generating status reports

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- The `ai-maestro-agents-management` skill (to read the team roster)
- `jq` installed for JSON processing

## Procedure

### Step 1: Load Current Registry

```bash
# Read the team roster via the ai-maestro-agents-management skill, then take
# each agent's name. (Save the skill's JSON output to /tmp/amcos-registry.json.)
AGENTS=$(jq -r '.[].name' /tmp/amcos-registry.json)
```

### Step 2: For Each Agent, Compare Registry vs Labels

```bash
for AGENT in $AGENTS; do
  # Get issues currently labeled for this agent from GitHub
  LABELED=$(gh issue list --label "assign:$AGENT" --json number --jq '.[].number' | sort)

  # The per-agent registry `current_issues` read has no frozen-CLI verb yet.
  # <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->

  echo "Agent: $AGENT"
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

Labels are source of truth. The registry write that records each agent's
`current_issues` from its GitHub labels has **no** frozen-CLI verb yet:

```bash
for AGENT in $AGENTS; do
  # Get actual labeled issues (the label side, via gh, stays available)
  LABELED_ISSUES=$(gh issue list --label "assign:$AGENT" --state open --json number --jq '[.[].number]')

  # Write LABELED_ISSUES into the agent's registry current_issues — BLOCKED.
  # <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->
done
```

### Step 5: Handle Orphaned Labels

Find labels for agents not in the team roster:

```text
# Get all assign:* labels in repo
ALL_ASSIGN_LABELS=$(gh label list --json name --jq '.[] | select(.name | startswith("assign:")) | .name')

# Read the team roster once via the ai-maestro-agents-management skill into
# /tmp/amcos-registry.json, then check each label's agent against it.
for LABEL in $ALL_ASSIGN_LABELS; do
  AGENT_NAME=$(echo $LABEL | sed 's/assign://')
  EXISTS=$(jq -r --arg n "$AGENT_NAME" '.[] | select(.name == $n) | .name' /tmp/amcos-registry.json)

  if [ -z "$EXISTS" ]; then
    echo "WARNING: Label '$LABEL' exists but agent not in roster"
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

```text
# Get labeled issues (the label side, via gh, stays available)
LABELED=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number' | sort)
echo "Labeled: $LABELED"

# Reading the agent's registry current_issues, and writing them back from the
# labels, both require a registry verb that does not exist yet.
# <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->
```

## Automated Sync Script

For scheduled sync, create a script:

```text
#!/bin/bash
# scripts/amcos_sync_labels.sh

# Get all agents from the team roster via the ai-maestro-agents-management
# skill, saving its JSON to /tmp/amcos-registry.json.
AGENTS=$(jq -r '.[].name' /tmp/amcos-registry.json)

for AGENT in $AGENTS; do
  # Get labeled issues (open only) — the label side, via gh, stays available
  LABELED=$(gh issue list --label "assign:$AGENT" --state open --json number --jq '[.[].number]')

  # Writing LABELED into the agent's registry current_issues — BLOCKED.
  # <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->
done

echo "Sync complete: $(date)"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| JSON parse error | Malformed roster output | Re-run the `ai-maestro-agents-management` skill and check AI Maestro health |
| gh rate limited | Too many API calls | Wait and retry with exponential backoff |
| Roster unreachable | AI Maestro down | Verify AI Maestro is running (the `ai-maestro-agents-management` skill errors out) |
| Agent not found | Agent not registered | Register the agent via the `ai-maestro-agents-management` skill |
