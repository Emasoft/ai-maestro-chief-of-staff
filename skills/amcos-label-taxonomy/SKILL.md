---
name: amcos-label-taxonomy
description: Use when applying or checking GitHub labels for agent assignment and status tracking. Trigger with label management or taxonomy lookup requests.
context: fork
agent: amcos-chief-of-staff-main-agent
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
workflow-instruction: "support"
procedure: "support-skill"
---

# AMCOS Label Taxonomy

## Overview

This skill provides the label taxonomy for the Chief of Staff Agent (AMCOS) role. AMCOS manages assignment labels, monitors status/priority labels, and keeps labels synchronized with the AI Maestro team registry.

## Prerequisites

1. GitHub repository with label support
2. GitHub CLI (`gh`) installed and authenticated
3. Access to AI Maestro REST API (`$AIMAESTRO_API`)

## Instructions

> **Output Rule**: All AMCOS scripts produce 2-line stdout summaries. Full output is written to `.amcos-logs/`.

1. Identify the label category needed (assign, status, priority)
2. Check if label exists on the issue/PR
3. Apply or modify label using `gh` CLI
4. Verify label was applied correctly
5. Update team registry if assignment labels changed

## Output

| Output Type | Example |
|-------------|---------|
| Label Applied | `assign:eoa-svgbbox-orchestrator` |
| Status Updated | `status:in-progress` applied |
| Registry Synced | `current_issues: [42, 43]` updated |

## Labels AMCOS Manages

### Assignment Labels (`assign:*`)

| Label | Description |
|-------|-------------|
| `assign:<agent-name>` | Specific agent assigned |
| `assign:orchestrator` | EOA handling |
| `assign:human` | Human intervention required |

AMCOS tracks assignments, reassigns when agents become unavailable, and clears assignments on termination.

## Kanban and Label Details

Full kanban column system, status labels, priority labels, and quick reference. See [kanban-and-label-details.md](references/kanban-and-label-details.md).
  - [Kanban Columns (Canonical 8-Column System)](#kanban-columns-canonical-8-column-system)
  - [Task Routing Rules](#task-routing-rules)
  - [Status Labels AMCOS Updates](#status-labels-amcos-updates)
  - [Labels AMCOS Monitors](#labels-amcos-monitors)
  - [Quick Reference: AMCOS Label Responsibilities](#quick-reference-amcos-label-responsibilities)
  - [Labels AMCOS Never Sets](#labels-amcos-never-sets)
  - [Checklist](#checklist)

## Error Handling

| Error | Solution |
|-------|----------|
| Label not found | Create with `gh label create` |
| Permission denied | Verify GitHub token has repo scope |
| Duplicate assign labels | Remove old before adding new |
| Registry out of sync | Run sync check via REST API |

## Examples

See [label-commands-and-examples.md](references/label-commands-and-examples.md) for label commands, registry sync, and full examples.
  - [AMCOS Label Commands](#amcos-label-commands)
  - [Agent Registry and Labels](#agent-registry-and-labels)
  - [Sync Check](#sync-check)
  - [Example 1: Spawning Agent and Assigning to Issue](#example-1-spawning-agent-and-assigning-to-issue)
  - [Example 2: Terminating Agent and Clearing Assignments](#example-2-terminating-agent-and-clearing-assignments)
  - [Example 3: Handling Blocked Agent](#example-3-handling-blocked-agent)

## Operational Procedures

- [op-assign-agent-to-issue.md](references/op-assign-agent-to-issue.md) - Assign agent to issue
- [op-terminate-agent-clear-assignments.md](references/op-terminate-agent-clear-assignments.md) - Clear assignments on termination
- [op-handle-blocked-agent.md](references/op-handle-blocked-agent.md) - Handle blocked agent
- [op-sync-registry-with-labels.md](references/op-sync-registry-with-labels.md) - Sync registry with labels

## Resources

- [Kanban and Label Details](references/kanban-and-label-details.md)
- [Label Commands and Examples](references/label-commands-and-examples.md)
- **AGENT_OPERATIONS.md** - Canonical operations reference (in docs/ folder)
- [GitHub Labels Documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
