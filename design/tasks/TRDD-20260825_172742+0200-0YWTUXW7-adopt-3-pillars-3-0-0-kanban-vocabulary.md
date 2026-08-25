---
trdd-id: 0YWTUXW7
title: Adopt the 3-pillars 3.0.0 22-column kanban vocabulary across the plugin
column: dev
created: 2026-08-25T17:27:42+0200
updated: 2026-08-25T17:27:42+0200
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: infra
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: hub-fleet-prep
min-approval-requirement: none
external-refs: [ai-maestro:TRDD-UNTF690M, ai-maestro:governance-rules@c8b0e9cb]
implementation-commits: []
---

# Adopt the 3-pillars 3.0.0 22-column kanban vocabulary

USER-ordered fleet prep, relayed by the hub session 2026-08-25: the kanban
vocabulary is now the 22-column board of 3-pillars spec 3.0.0 (`@spec:
kanban-columns v2`, 3P-KAN-01/04/17/18/19/20, USER-ratified 2026-08-23), plus
the 5 bracket values (`proposal`, `planned`, `refused`, `completed`,
`cancelled`) legal in `column:` but outside the board — legal set 27.
Authority verified first-hand at Emasoft/ai-maestro branch `governance-rules`
head `c8b0e9cb` (remote head confirmed via `git ls-remote`).

## Scope (found by a full-repo scan, all migrated)

- `scripts/amcos_kanban.py` — board enum → 22 in 3.0.0 order (constants renamed
  `KANBAN_BOARD_COLUMN_IDS` / `DEFAULT_BOARD_COLUMNS`; new
  `BRACKET_COLUMN_VALUES`); the 5 new column configs mirror the server's
  `DEFAULT_KANBAN_COLUMNS` (types/team.ts) labels/colors/icons verbatim.
- `tests/test_kanban.py`, `tests/test_board_discipline.py` — expectations → 22
  board / 27 legal.
- Docs: `TEAM_REGISTRY_SPECIFICATION.md`, `AGENT_OPERATIONS.md`,
  `FULL_PROJECT_WORKFLOW.md` (design now BEFORE todo).
- Skills: `amcos-prrd-trdd-kanban/SKILL.md`,
  `amcos-label-taxonomy/references/kanban-and-label-details.md`.
- Agent personas: 5 sub-agents + main agent ("17-column" → "22-column").

Existing cards are grandfathered per 3P-KAN-21 — no card re-columned.
No writer of the retired `approval-tier:` field exists in this repo (scanned);
live field is `min-approval-requirement:`.

## Upstream defect found, reported, and fixed same hour

`ai-maestro app/api/teams/[id]/kanban-config/route.ts` still capped the PUT
schema at `columns: .max(20)` while the server's own `DEFAULT_KANBAN_COLUMNS`
has 22 entries — the route 422'd its own default, and this plugin's
drift-correct path would have failed against it. Reported to the hub session
2026-08-25 per its defects-only reply protocol; hub fixed it as ai-maestro
`e3446edf` (`.max(27)` = the 3P-KAN-20 legal set), verified first-hand in the
hub tree. This repo aligns TO the ratified spec, never to a stale validator.

## Acceptance criteria

- [x] Full-repo scan finds zero live "17-column" / "14 lifecycle" /
      `14STAGE` references (verified: grep sweep NONE).
- [x] Board enum, fallback config, and tests carry the 22 columns in ratified
      order; bracket values recognized as legal-but-off-board.
- [x] Full test suite green (343 passed).

## Approval log
