---
operation: op-assign-agent-to-issue
parent-skill: amcos-label-taxonomy
---

# Operation: Assign Agent to Issue


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify Issue Exists](#step-1-verify-issue-exists)
  - [Step 2: Remove Existing Assignment (if any)](#step-2-remove-existing-assignment-if-any)
  - [Step 3: Add Assignment Label](#step-3-add-assignment-label)
  - [Step 4: Update Status from Backlog to Ready](#step-4-update-status-from-backlog-to-ready)
  - [Step 5: Update Team Registry](#step-5-update-team-registry)
  - [Step 6: Verify Assignment](#step-6-verify-assignment)
- [Example](#example)
- [Error Handling](#error-handling)
- [Rollback](#rollback)

## Purpose

Assign a newly spawned or existing agent to a GitHub issue by applying the appropriate assignment label and updating status.

## When to Use

- When AMCOS spawns a new agent and needs to assign work
- When reassigning an issue from one agent to another
- When an agent becomes available and can take on new work

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Issue number to assign
- Agent name (session name) to assign
- Access to AI Maestro REST API (`$AIMAESTRO_API`, default `http://localhost:23000`)
- `$OWNER/$REPO` set to the target GitHub repository (e.g., `Emasoft/svgbbox`)

## Procedure

### Step 1: Verify Issue Exists

```bash
gh issue view $ISSUE_NUMBER --json number,title,labels --repo "$OWNER/$REPO"
```

Confirm the issue exists and note any existing labels.

### Step 2: Remove Existing Assignment (if any)

```bash
# Check for existing assign:* labels
EXISTING=$(gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name | select(startswith("assign:"))' --repo "$OWNER/$REPO")
if [ -n "$EXISTING" ]; then
  gh issue edit $ISSUE_NUMBER --remove-label "$EXISTING" --repo "$OWNER/$REPO"
fi
```

### Step 3: Add Assignment Label

```bash
gh issue edit $ISSUE_NUMBER --add-label "assign:$AGENT_NAME" --repo "$OWNER/$REPO"
```

### Step 4: Update Status from Backlog to Ready

```bash
gh issue edit $ISSUE_NUMBER --remove-label "status:backlog" --add-label "status:ready" --repo "$OWNER/$REPO"
```

### Step 5: Update Team Registry

```bash
curl -X PATCH "$AIMAESTRO_API/api/agents/$AGENT_NAME" \
  -H "Content-Type: application/json" \
  -d '{"current_issues_add": ['$ISSUE_NUMBER']}'
```

### Step 6: Verify Assignment

```bash
gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name' --repo "$OWNER/$REPO"
# Expected output should include: assign:$AGENT_NAME, status:ready
```

## Example

**Scenario:** Assign issue #42 to agent `implementer-1`.

```bash
# Step 1: Add assignment label
gh issue edit 42 --add-label "assign:implementer-1" --repo "$OWNER/$REPO"

# Step 2: Update status
gh issue edit 42 --remove-label "status:backlog" --add-label "status:ready" --repo "$OWNER/$REPO"

# Step 3: Update registry via REST API
curl -X PATCH "$AIMAESTRO_API/api/agents/implementer-1" \
  -H "Content-Type: application/json" \
  -d '{"current_issues_add": [42]}'

# Step 4: Verify
gh issue view 42 --json labels --jq '.labels[].name' --repo "$OWNER/$REPO"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Label not found | `assign:*` label doesn't exist | Create with `gh label create "assign:$AGENT_NAME" --repo "$OWNER/$REPO"` |
| Permission denied | Insufficient repo access | Verify GitHub token has repo scope |
| Issue not found | Invalid issue number | Verify with `gh issue list --repo "$OWNER/$REPO"` |
| Registry update fails | API error | Check AI Maestro API is running at `$AIMAESTRO_API` |

## Rollback

If assignment fails midway:

```bash
# Remove the partial assignment
gh issue edit $ISSUE_NUMBER --remove-label "assign:$AGENT_NAME" --repo "$OWNER/$REPO"
gh issue edit $ISSUE_NUMBER --add-label "status:backlog" --repo "$OWNER/$REPO"
```
