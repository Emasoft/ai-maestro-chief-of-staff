# Kanban Columns and Label Details

## Table of Contents

- [Kanban Columns (Canonical 5-Status System)](#kanban-columns-canonical-5-status-system)
- [Task Routing Rules](#task-routing-rules)
- [Status Labels AMCOS Updates](#status-labels-amcos-updates)
- [Labels AMCOS Monitors](#labels-amcos-monitors)
- [Quick Reference: AMCOS Label Responsibilities](#quick-reference-amcos-label-responsibilities)
- [Labels AMCOS Never Sets](#labels-amcos-never-sets)
- [Checklist](#checklist)

---

## Kanban Columns (Canonical 5-Status System)

> These columns align with AI Maestro's task status model (`types/task.ts`).

The full workflow uses these 5 status columns:

| # | Column Code | Display Name | Label | Description |
|---|-------------|-------------|-------|-------------|
| 1 | `backlog` | Backlog | `status:backlog` | Entry point for new tasks |
| 2 | `pending` | Pending | `status:pending` | Ready to start |
| 3 | `in_progress` | In Progress | `status:in_progress` | Active work |
| 4 | `review` | Review | `status:review` | Integrator and/or user reviews the task |
| 5 | `completed` | Completed | `status:completed` | Completed and merged |

Use the `status:blocked` label to flag blocked tasks at any stage (not a separate kanban column).

## Task Routing Rules

- **Small tasks**: In Progress -> Review -> Completed
- **Big tasks**: In Progress -> Review (includes human review if needed) -> Completed
- **Human Review** within the Review column is requested via AMAMA (Assistant Manager asks user to test/review)
- Not all tasks go through human review -- only significant changes requiring human judgment

## Status Labels AMCOS Updates

| Label | When AMCOS Sets It |
|-------|------------------|
| `status:blocked` | When pausing work (resource constraints) or agent reports blocker |
| `status:pending` | When blocker resolved and task is ready to resume |

## Labels AMCOS Monitors

### Priority Labels (`priority:*`)

AMCOS uses priority for resource allocation:
- `priority:critical` - Ensure agent assigned immediately
- `priority:high` - Prioritize in staffing decisions
- `priority:normal` - Standard allocation
- `priority:low` - Can wait for resources

### Status Labels (`status:*`)

AMCOS monitors all status changes:
- `status:blocked` - May need to reassign or escalate
- `status:in_progress` - Track for timeout/health monitoring
- `status:review` - Route to AMIA; request human review via AMAMA if needed
- `status:completed` - Task finished and merged

## Quick Reference: AMCOS Label Responsibilities


| Action | Labels Involved |
|--------|-----------------|
| Spawn agent | Add `assign:<agent>`, update `status:pending` |
| Terminate agent | Remove `assign:<agent>`, set `status:backlog` |
| Agent blocked | Update to `status:blocked` |
| Resolve blocker | Update to `status:pending` or `status:in_progress` |
| Escalate to human | Add `assign:human` |
| Block work | Add `status:blocked` |

## Labels AMCOS Never Sets

- `type:*` - Set at issue creation
- `effort:*` - Set during triage by AMOA
- `review:*` - Managed by AMIA
- `priority:*` - Set by AMOA or AMAMA (AMCOS can suggest changes)

## Checklist


Copy this checklist and track your progress:

- [ ] Identify label category (assign/status/priority)
- [ ] Check existing labels on issue with `gh issue view <number>`
- [ ] Remove conflicting labels if needed
- [ ] Apply new label via `gh issue edit --add-label`
- [ ] Verify label appears correctly
- [ ] Update team registry via AI Maestro REST API if agent assignment changed

