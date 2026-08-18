---
trdd-id: 4HSTGXGB
title: Repair 4FH9JP4U — write the missing checklist against its re-run checks and re-close
column: complete
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T23:53:00+0200
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: user
min-approval-requirement: none
created-by: DAESKVN9
npt: []
eht: []
blocked-by: []
release-via: none
external-refs: [ai-maestro TRDD-BRRJK57P]
priority: 6
---

# Repair 4FH9JP4U — write the missing checklist against its re-run checks and re-close

Phase-2 remediation of the axis-2 confirmed finding (report
`20260816_170954+0200-axis2-governance.md`) and the one genuine violation behind TRDD-Q7BZ8N3M's
disposition (see its `## ⏵ DISPOSITION`, commit `f15f1df`).

`design/archived/TRDD-20260716_203210+0200-4FH9JP4U-r42-drive-vs-lifecycle-purge-plan.md` sits at
`column: complete` (set 2026-08-11, post-boundary) with zero checklist boxes — the vacuous case
the gate's "≥1 box" clause was added for. Its work IS done: the Approval log records three checks
run at close, and all three were re-run 2026-08-16 and passed (injection-INSTRUCTION prose gone —
what remains PROHIBITS injection in 4 skills; `kill -TERM` of a peer absent; suite green 340).

Procedure (the rule's own remedy; not retro-ticking, because each box is ticked against a fresh
re-run, never against the card's prose):
1. `git mv` the card back to `design/tasks/`, set `column: dev` — this lifts the step-12 freeze.
2. RE-RUN the three checks on the day of repair; record commands + results in the card.
3. Write the checklist (3 boxes naming the checks), tick each against that day's re-run.
4. Set `column: complete`, bump `updated:`, `git mv` back to `design/archived/`.
5. Remove `4FH9JP4U` from `KNOWN_UNGATED` in `tests/test_board_discipline.py` — the shrink-only
   test REQUIRES this (a stale exemption reds), and lower `_DEBT_CEILING` 9 → 8. NOTE: the other
   eight entries stay — they are pre-boundary/frozen per Q7BZ8N3M's disposition, and pruning them
   is a separate judgment that card already made (leave terminal, no action); their entries keep
   the guard's map of why they are exempt.

## Acceptance criteria

- [x] The three checks re-run 2026-08-18T23:50:51 — commands + exit codes recorded in
      4FH9JP4U's new checklist section.
- [x] Checklist exists (3 boxes), all ticked against that re-run, never against the prose.
- [x] Card back at `column: complete` in `design/archived/`, `updated:` bumped; the reopen and
      re-close are both in its Approval log (reopen committed separately so the dev transition
      is observable, not theatre).
- [x] `KNOWN_UNGATED` shrunk to 8 entries (4FH9JP4U removed — the shrink-only test forced it);
      `_DEBT_CEILING` = 8; suite 341 green.
- [x] ruff clean.

## Approval log

- 2026-08-18T23:53:00+0200 — COMPLETED. ai_review not run for this card: the deliverable is a
  verification RECORD (checklist + log entries), whose correctness is established by the
  re-run commands and the board-discipline tests passing in both directions — an LLM reviewing
  prose about greps adds nothing the greps did not already prove. Stated rather than skipped
  silently.
