# Kanban Columns and Label Details

## Table of Contents

- [Kanban Columns (Canonical 8-Column System)](#kanban-columns-canonical-8-column-system)
- [Task Routing Rules](#task-routing-rules)
- [Status Labels AMCOS Updates](#status-labels-amcos-updates)
- [Labels AMCOS Monitors](#labels-amcos-monitors)
- [Quick Reference: AMCOS Label Responsibilities](#quick-reference-amcos-label-responsibilities)
- [Labels AMCOS Never Sets](#labels-amcos-never-sets)
- [Checklist](#checklist)

---

## Kanban Columns (Canonical 8-Column System)

The full workflow uses these 8 status columns:

| # | Column Code | Display Name | Label | Description |
|---|-------------|-------------|-------|-------------|
| 1 | `backlog` | Backlog | `status:backlog` | Entry point for new tasks |
| 2 | `todo` | Todo | `status:todo` | Ready to start |
| 3 | `in-progress` | In Progress | `status:in-progress` | Active work |
| 4 | `ai-review` | AI Review | `status:ai-review` | Integrator agent reviews ALL tasks |
| 5 | `human-review` | Human Review | `status:human-review` | User reviews BIG tasks only (via EAMA) |
| 6 | `merge-release` | Merge/Release | `status:merge-release` | Ready to merge |
| 7 | `done` | Done | `status:done` | Completed |
| 8 | `blocked` | Blocked | `status:blocked` | Blocked at any stage |

## Task Routing Rules

- **Small tasks**: In Progress -> AI Review -> Merge/Release -> Done
- **Big tasks**: In Progress -> AI Review -> Human Review -> Merge/Release -> Done
- **Human Review** is requested via EAMA (Assistant Manager asks user to test/review)
- Not all tasks go through Human Review -- only significant changes requiring human judgment

## Status Labels AMCOS Updates

| Label | When AMCOS Sets It |
|-------|------------------|
| `status:blocked` | When pausing work (resource constraints) or agent reports blocker |
| `status:todo` | When blocker resolved and task is ready to resume |

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
- `status:in-progress` - Track for timeout/health monitoring
- `status:ai-review` - Route to EIA if not already
- `status:human-review` - Escalated for user review via EAMA
- `status:merge-release` - Ready to merge/release

## Quick Reference: AMCOS Label Responsibilities

| Action | Labels Involved |
|--------|-----------------|
| Spawn agent | Add `assign:<agent>`, update `status:todo` |
| Terminate agent | Remove `assign:<agent>`, set `status:backlog` |
| Agent blocked | Update to `status:blocked` |
| Resolve blocker | Update to `status:todo` or `status:in-progress` |
| Escalate to human | Add `assign:human` |
| Block work | Add `status:blocked` |

## Labels AMCOS Never Sets

- `type:*` - Set at issue creation
- `effort:*` - Set during triage by EOA
- `review:*` - Managed by EIA
- `priority:*` - Set by EOA or EAMA (AMCOS can suggest changes)

## Checklist

Copy this checklist and track your progress:

- [ ] Identify label category (assign/status/priority)
- [ ] Check existing labels on issue with `gh issue view <number>`
- [ ] Remove conflicting labels if needed
- [ ] Apply new label via `gh issue edit --add-label`
- [ ] Verify label appears correctly
- [ ] Update team registry via AI Maestro REST API if agent assignment changed
