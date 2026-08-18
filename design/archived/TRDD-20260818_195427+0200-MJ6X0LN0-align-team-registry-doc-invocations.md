---
trdd-id: MJ6X0LN0
title: Align every documented amcos_team_registry.py invocation to its real argparse surface
column: complete
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T23:46:35+0200
implementation-commits: [b261e74]
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: user
min-approval-requirement: 0
created-by: DAESKVN9
npt: []
eht: []
blocked-by: []
release-via: publish
external-refs: [ai-maestro TRDD-BRRJK57P]
priority: 2
---

# Align every documented amcos_team_registry.py invocation to its real argparse surface

Phase-2 remediation of axis-1 findings 1–4
(report `reports/plugin-self-audit/20260816_170747+0200-axis1-missing-features.md`, hub-verified;
hub's severity upgrade adopted with the `--role` correction — `--role` IS real and required).

Every documented invocation of `scripts/amcos_team_registry.py` fails at the shell. The real
parser (read at :489-530): `add-agent` requires `--team --agent-name --role --plugin --host`
(optional `--address`); `remove-agent` requires `--team --agent-name`; `update-status` requires
`--team --agent-name --status`; subcommands are `create, add-agent, remove-agent, update-status,
list, kanban-velocity` — there is NO `publish`.

Sites to fix (from the audit, re-verified):
- `skills/amcos-agent-coordination/SKILL.md:91-92` — `--name`/`--status` on add-agent, missing
  `--agent-name --plugin --host`
- `skills/amcos-agent-spawning/SKILL.md:53` — same shape
- `agents/ai-maestro-chief-of-staff-main-agent.md:589` — same shape
- `agents/ai-maestro-chief-of-staff-main-agent.md:536` — lists nonexistent `publish`, omits real
  `kanban-velocity`
- `skills/amcos-agent-termination/SKILL.md:36,80,90` — remove-agent missing `--team`, wrong flag
- `skills/amcos-agent-hibernation/SKILL.md:53,99-100,107-108` — update-status missing `--team`,
  wrong flag

Note the DECOUPLE-BLOCKED marker at `scripts/amcos_team_registry.py:314-331` (ai-maestro#76):
add-agent's runtime path is itself blocked upstream. This card fixes only the DOCUMENTED
invocations to match the parser; it does not touch the upstream decoupling (that is
TRDD-8e8d6618 / #76's territory).

## Acceptance criteria

- [x] Every doc invocation reaches the script body — worker verified parser acceptance; my
      independent grep of team-registry blocks for `--name`/`--project`/`--timestamp` returned 0.
- [x] No remaining `--name`/`--status`-on-add-agent, no `publish` claim — verified by grep after
      the worker returned (decide-on-facts: not taken from its report).
- [x] Persona :536 now lists exactly create, add-agent, remove-agent, update-status, list,
      kanban-velocity — read verbatim.
- [x] Suite green (341), ruff clean.

## Approval log

- 2026-08-18T23:46:35+0200 — COMPLETED. Flow: todo → dev (lean-worker, 131 invocation sites
  across 30 files; scope was 5x the audit's headline estimate once the duplicated op-*.md
  reference sets were counted) → testing (grep + parser acceptance + suite 341) → ai_review
  (llm-ext 3-model ensemble on the skills/agents diff: 3/3 APPROVE, per-file; report
  reports/llm-externalizer/20260818_234623+0200-code_task-mj6x.diff-01548d.md) → complete.
  Implementation commit b261e74. Worker report:
  reports/plugin-self-audit/20260818_200736+0200-MJ6X0LN0-fix-report.md.
