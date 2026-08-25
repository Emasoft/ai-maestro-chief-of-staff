# Kanban Columns and Label Details

## Table of Contents

- [Kanban Columns (ratified 22-column pipeline)](#kanban-columns-ratified-22-column-pipeline)
- [Task Routing Rules](#task-routing-rules)
- [Status Labels AMCOS Updates](#status-labels-amcos-updates)
- [Labels AMCOS Monitors](#labels-amcos-monitors)
- [Quick Reference: AMCOS Label Responsibilities](#quick-reference-amcos-label-responsibilities)
- [Labels AMCOS Never Sets](#labels-amcos-never-sets)
- [Checklist](#checklist)

---

## Kanban Columns (ratified 22-column pipeline)

> The team board is a **1:1 mirror** of the authoritative TRDD `column:`
> pipeline — not a separate workflow and NOT a projection. The TRDD `column:`
> lifecycle is the source of truth; each lane IS one `column:` value. An earlier
> **8-column** model (v2.20.0) was **superseded** by the MANAGER's ai-maestro#2
> decision (a) (COS#11): a collapse hid the human gate and the
> publish/deploy tails, so the board now carries every `column:` as its own lane,
> keeping the two governance review gates (`ai_review`, `human_review`) DISTINCT
> and `blocked`/`failed`/`superseded` first-class.

**The lanes** (the canonical column set lives in the `amcos-prrd-trdd-kanban`
skill — the single source of truth; 19 lifecycle + 3 exception, the TRDD
`column:` values in lifecycle order):

`backburner · approval · design · design_ai_review · design_human_review · todo · verify_assumptions · plan · dispatch · dev · testing · ai_review · human_review · complete · publish · published · deploy · live · live_auditing` + exceptions `blocked · failed · superseded`

COS sets this column schema once, at team creation, via the deployed
`kanban-config` CLI verb (the per-team column **backend** is gated on
ai-maestro#2); COS does NOT move cards between lanes.

> **Note — the `status:*` issue-labels below are a separate, coarser layer.** The
> operational `status:*` GitHub-issue labels AMCOS sets/monitors (next sections)
> have NOT been expanded one-per-lane; that label-taxonomy change touches live
> issue labels across teams and is a separate MANAGER decision, not part of the
> board-model ratification.

## Task Routing Rules

- **Small tasks**: `dev` -> `testing` -> `ai_review` -> `complete` -> release
- **Big tasks**: `dev` -> `testing` -> `ai_review` -> `human_review` -> `complete` -> release
- **`human_review` is a DISTINCT lane** (never folded into `ai_review`): the MANAGER mediates the human gate (R6.6). Not all tasks pass through it — only significant changes needing human judgment.

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

