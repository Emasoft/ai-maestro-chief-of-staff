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

> **Multi-repo rule**: All `gh` commands MUST include `--repo "$OWNER/$REPO"` to target the correct repository. Agents may work with multiple repos. Never assume a single repo context.

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

Full kanban column system, status labels, priority labels, and quick reference. See `references/kanban-and-label-details.md`.

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
gh issue edit 42 --add-label "assign:libs-svg-svgbbox" --repo "$OWNER/$REPO"
[DONE] Label assign:libs-svg-svgbbox applied to #42. Registry updated.
```

See `references/label-commands-and-examples.md` for label commands, registry sync, and full examples.

## Operational Procedures

- `references/op-assign-agent-to-issue.md` - Assign agent to issue
- `references/op-terminate-agent-clear-assignments.md` - Clear assignments on termination
- `references/op-handle-blocked-agent.md` - Handle blocked agent
- `references/op-sync-registry-with-labels.md` - Sync registry with labels

## Resources

- `references/kanban-and-label-details.md`
- `references/label-commands-and-examples.md`
- **AGENT_OPERATIONS.md** - Canonical operations reference (in docs/ folder)
- [GitHub Labels Documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)

