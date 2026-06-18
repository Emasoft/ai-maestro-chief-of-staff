# Label Commands and Examples

## Table of Contents

- [AMCOS Label Commands](#amcos-label-commands)
- [Agent Registry and Labels](#agent-registry-and-labels)
- [Sync Check](#sync-check)
- [Example 1: Spawning Agent and Assigning to Issue](#example-1-spawning-agent-and-assigning-to-issue)
- [Example 2: Terminating Agent and Clearing Assignments](#example-2-terminating-agent-and-clearing-assignments)
- [Example 3: Handling Blocked Agent](#example-3-handling-blocked-agent)

---

## AMCOS Label Commands

### When Agent Spawned

```bash
# Assign new agent to issue
gh issue edit $ISSUE_NUMBER --add-label "assign:$NEW_AGENT_NAME"
gh issue edit $ISSUE_NUMBER --remove-label "status:backlog" --add-label "status:todo"
```

### When Agent Terminated

```bash
# Clear assignment from all agent's issues
AGENT_ISSUES=$(gh issue list --label "assign:$AGENT_NAME" --json number --jq '.[].number')
for ISSUE in $AGENT_ISSUES; do
  gh issue edit $ISSUE --remove-label "assign:$AGENT_NAME" --add-label "status:backlog"
done
```

### When Agent Blocked

```bash
# Mark issue blocked
gh issue edit $ISSUE_NUMBER --remove-label "status:in-progress" --add-label "status:blocked"
```

### When Escalating to Human

```bash
# Reassign to human
gh issue edit $ISSUE_NUMBER --remove-label "assign:$AGENT_NAME" --add-label "assign:human"
```

## Agent Registry and Labels

AMCOS keeps the team registry synchronized with the GitHub assignment labels.
The per-agent registry read/write that exposes `current_issues` has **no**
frozen-CLI verb yet:

```bash
# Read an agent's registry current_issues — BLOCKED (no frozen-CLI verb).
# <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->
# (When available it would return: {"session_name": "code-impl-01", "status": "active", "current_issues": [42, 43]})
```

## Sync Check

```bash
# Find issues assigned to agent from GitHub labels (the label side stays available)
LABELED=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number' | sort)

# Compare with the agent's registry current_issues — BLOCKED (no frozen-CLI verb).
# <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->
```

## Example 1: Spawning Agent and Assigning to Issue

**Scenario**: AMCOS spawns a new agent "implementer-1" and assigns it to issue #42.

```bash
# Step 1: Add assignment label
gh issue edit 42 --add-label "assign:implementer-1"

# Step 2: Update status from backlog to ready
gh issue edit 42 --remove-label "status:backlog" --add-label "status:todo"

# Step 3: Record the issue on the agent's registry current_issues — BLOCKED (no frozen-CLI verb).
# <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->

# Step 4: Verify
gh issue view 42 --json labels --jq '.labels[].name'
# Output: assign:implementer-1, status:todo
```

## Example 2: Terminating Agent and Clearing Assignments

**Scenario**: Agent "implementer-1" is being terminated. Clear all its assignments.

```bash
# Step 1: Find all issues assigned to agent
AGENT_ISSUES=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number')

# Step 2: Remove assignment and update status
for ISSUE in $AGENT_ISSUES; do
  gh issue edit $ISSUE --remove-label "assign:implementer-1" --add-label "status:backlog"
  echo "Cleared assignment from issue #$ISSUE"
done

# Step 3: Flip the agent's registry status to terminated — BLOCKED (no frozen-CLI verb).
# <!-- DECOUPLE-BLOCKED ai-maestro#36: issue-label assignment has no frozen-CLI verb (agent --label is a persona name, not a GitHub-issue label). Pending a follow-up verb. -->

# Step 4: Verify no issues remain assigned
gh issue list --label "assign:implementer-1"
# Output: (empty)
```

## Example 3: Handling Blocked Agent

**Scenario**: Agent reports it's blocked on issue #43. AMCOS updates status and notifies.

```bash
# Step 1: Update status to blocked
gh issue edit 43 --remove-label "status:in-progress" --add-label "status:blocked"

# Step 2: Add comment explaining blocker (body begins with the PRRD G1.1 self-id line)
gh issue comment 43 --body "This is the Claude responsible for the ai-maestro-chief-of-staff project.

Agent blocked: waiting for external API credentials. Assigned to human for resolution."

# Step 3: Escalate to human if needed
gh issue edit 43 --add-label "assign:human"

# Step 4: Verify
gh issue view 43 --json labels --jq '.labels[].name'
# Output: assign:human, status:blocked, priority:high
```
