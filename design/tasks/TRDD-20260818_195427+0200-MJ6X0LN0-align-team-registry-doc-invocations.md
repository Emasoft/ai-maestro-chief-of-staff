---
trdd-id: MJ6X0LN0
title: Align every documented amcos_team_registry.py invocation to its real argparse surface
column: ai_review
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T20:39:01+0200
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

- [ ] Every doc invocation above, run verbatim, reaches the script body (argparse accepts it) —
      proven by running each with `--help`-level dry semantics or against the parser error output.
- [ ] `grep -rn "team_registry.py" skills/ agents/ commands/` shows no remaining `--name ` or
      `--status` on add-agent, no `publish` subcommand claim.
- [ ] The persona's subcommand list (:536) matches `add_parser` calls exactly, incl.
      `kanban-velocity`.
- [ ] Suite green, ruff clean.
