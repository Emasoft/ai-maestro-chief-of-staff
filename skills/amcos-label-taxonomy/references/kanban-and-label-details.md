# Kanban Columns and Label Details

## Table of Contents

- [Kanban Columns (MANAGER-ratified 8-column model)](#kanban-columns-manager-ratified-8-column-model)
- [Task Routing Rules](#task-routing-rules)
- [Status Labels AMCOS Updates](#status-labels-amcos-updates)
- [Labels AMCOS Monitors](#labels-amcos-monitors)
- [Quick Reference: AMCOS Label Responsibilities](#quick-reference-amcos-label-responsibilities)
- [Labels AMCOS Never Sets](#labels-amcos-never-sets)
- [Checklist](#checklist)

---

## Kanban Columns (MANAGER-ratified 8-column model)

> The team board is the **visual projection** of the authoritative TRDD
> `column:` pipeline — not a separate workflow. The TRDD `column:` lifecycle is
> the source of truth; the board lanes are how it surfaces. The MANAGER ratified
> the **8-column model** (Tier-2, COS#11) — a simplified projection of the TRDD
> v2 lifecycle that, unlike the old collapsed 5-status set, keeps the two
> governance review gates (`ai-review`, `human-review`) DISTINCT and `blocked` a
> first-class lane.

**The 8 lanes** (the canonical column set + the full TRDD `column:`→lane mapping
live in the `amcos-prrd-trdd-kanban` skill — the single source of truth; not
duplicated here):

`backlog · todo · in-progress · ai-review · human-review · merge-release · done · blocked`

COS sets this column schema once, at team creation, via the `kanban-config` CLI
verb (not yet deployed — ai-maestro#36); COS does NOT move cards between lanes.

> **Note — the `status:*` issue-labels below are a separate, coarser layer.** The
> operational `status:*` GitHub-issue labels AMCOS sets/monitors (next sections)
> have NOT been expanded one-per-lane; that label-taxonomy change touches live
> issue labels across teams and is a separate MANAGER decision, not part of the
> board-model ratification.

## Task Routing Rules

- **Small tasks**: in-progress -> ai-review -> merge-release -> done
- **Big tasks**: in-progress -> ai-review -> human-review -> merge-release -> done
- **human-review is a DISTINCT lane** (never folded into ai-review): the MANAGER mediates the human gate (R6.6). Not all tasks pass through it — only significant changes needing human judgment.

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

