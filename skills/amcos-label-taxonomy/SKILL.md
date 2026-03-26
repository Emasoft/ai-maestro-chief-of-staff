---
name: amcos-label-taxonomy
description: Use when applying or checking GitHub labels for agent assignment and status tracking. Trigger with label management or taxonomy lookup requests.
context: fork
agent: ai-maestro-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
---

# AMCOS Label Taxonomy

## Overview

This skill provides the label taxonomy for the Chief of Staff Agent (AMCOS) role. AMCOS manages assignment labels, monitors status/priority labels, and keeps labels synchronized with the AI Maestro team registry.

## Prerequisites

1. GitHub repository with label support
2. GitHub CLI (`gh`) installed and authenticated
3. Access to AI Maestro REST API (`$AIMAESTRO_API`)

## Instructions

1. Identify the label category needed (assign, status, priority)
2. Check if label exists on the issue/PR
3. Apply or modify label using `gh` CLI
4. Verify label was applied correctly
5. Update team registry if assignment labels changed

### Checklist

Copy this checklist and track your progress:

- [ ] Correct label category identified (assign/status/priority)
- [ ] Label exists in repo or created with `gh label create`
- [ ] Label applied to correct issue/PR
- [ ] Team registry updated if assignment changed

## Output

| Output Type | Example |
|-------------|---------|
| Label Applied | `assign:amoa-svgbbox-orchestrator` |
| Status Updated | `status:in-progress` applied |
| Registry Synced | `current_issues: [42, 43]` updated |

## Labels AMCOS Manages

### Assignment Labels (`assign:*`)

| Label | Description |
|-------|-------------|
| `assign:<agent-name>` | Specific agent assigned |
| `assign:orchestrator` | AMOA handling |
| `assign:human` | Human intervention required |

AMCOS tracks assignments, reassigns when agents become unavailable, and clears assignments on termination.

## Kanban and Label Details

Full kanban column system, status labels, priority labels, and quick reference. See [kanban-and-label-details](references/kanban-and-label-details.md) — Topics: Kanban Columns and Label Details, Table of Contents, Kanban Columns (Canonical 5-Status System), Task Routing Rules, Status Labels AMCOS Updates, Labels AMCOS Monitors, Priority Labels (`priority:*`), Status Labels (`status:*`), Quick Reference: AMCOS Label Responsibilities, Labels AMCOS Never Sets, Checklist

## Error Handling

| Error | Solution |
|-------|----------|
| Label not found | Create with `gh label create` |
| Permission denied | Verify GitHub token has repo scope |
| Duplicate assign labels | Remove old before adding new |
| Registry out of sync | Run sync check via REST API |

## Examples

**Input:** "Assign issue #42 to agent libs-svg-svgbbox"

**Output:**
```
gh issue edit 42 --add-label "assign:libs-svg-svgbbox"
[DONE] Label assign:libs-svg-svgbbox applied to #42. Registry updated.
```

## Operational Procedures

- [op-assign-agent-to-issue](references/op-assign-agent-to-issue.md) — Topics: Operation: Assign Agent to Issue, Contents, Purpose, When to Use, Prerequisites, Procedure, Step 1: Verify Issue Exists, Step 2: Remove Existing Assignment (if any), Check for existing assign:* labels, Step 3: Add Assignment Label, Step 4: Update Status from Backlog to Ready, Step 5: Update Team Registry, Step 6: Verify Assignment, Expected output should include: assign:$AGENT_NAME, status:ready, Example, Step 1: Add assignment label, Step 2: Update status, Step 3: Update registry via REST API, Step 4: Verify, Error Handling, Rollback, Remove the partial assignment

## Resources

- [kanban-and-label-details](references/kanban-and-label-details.md) — Topics: Kanban Columns and Label Details, Table of Contents, Kanban Columns (Canonical 5-Status System), Task Routing Rules, Status Labels AMCOS Updates, Labels AMCOS Monitors, Priority Labels (`priority:*`), Status Labels (`status:*`), Quick Reference: AMCOS Label Responsibilities, Labels AMCOS Never Sets, Checklist

