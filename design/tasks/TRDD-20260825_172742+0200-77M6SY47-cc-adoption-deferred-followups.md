---
trdd-id: 77M6SY47
title: CC-adoption deferred follow-ups from the v2.1 backlog adjudication
column: backburner
created: 2026-08-25T17:27:42+0200
updated: 2026-08-25T17:27:42+0200
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: feature
scope: project
project-id: ai-maestro-chief-of-staff
min-approval-requirement: none
parent-trdd: 23C5566E
---

# CC-adoption deferred follow-ups (from TRDD-23C5566E, adjudicated 2026-08-25)

TRDD-23C5566E's backlog was adjudicated against Claude Code 2.1.240 with every
premise re-verified against the LIVE docs (not the changelog from memory).
Items implemented or rejected are recorded in that card's closing adjudication.
These four remain wanted but not actionable today; each has a re-entry
condition. Pick ONE item up at a time — it becomes its own card (this card
then updates or closes).

## Item 1 — plugin `experimental.monitors` heartbeat (was Item B)

Replace the UserPromptSubmit heartbeat coupling with a plugin-declared
monitor. **Verified 2026-08-25:** `experimental.monitors` exists in
plugins-reference and is STILL marked experimental. Re-entry condition: the
field graduates out of `experimental.` (the original card's own gate).

## Item 2 — per-agent frontmatter hooks refactor (was Item E)

Move agent-specific hook logic from central `hooks/hooks.json` into agent
frontmatter `hooks:`. Architectural cleanup, low urgency by the original
card's own text. Re-entry condition: a sprint that already touches the hook
surface.

## Item 3 — `/goal` rewrite of the wait-for-* commands (was Item F)

**Verified 2026-08-25:** `/goal` exists in the commands reference (alongside
`/loop`). Deferred because the acceptance bar — "no regression in approval/ok
detection" — cannot be verified without a live multi-agent approval flow, and
an untested rewrite of a working coordination path is worse than polling.
Re-entry condition: a session with a live team where the flow can actually be
exercised end to end.

## Item 4 — per-spawned-agent OTEL correlation (was Item G)

Depends on the team-registry redesign (original card's own dependency, still
unmet — `amcos_team_registry.py` is CRUD over the hub CLI with no state
machine). Re-entry condition: the registry redesign lands.

## Re-check note (was Item D)

Tool-telemetry via PostToolUse was REJECTED, not deferred: `duration_ms` is
absent from the live hooks docs (verified 2026-08-25), and an every-tool-call
hook is a standing per-turn tax on every plugin user for an unrequested
dashboard. If `duration_ms` (re)appears in the docs AND a consumer asks for
per-tool latency, re-open with a fresh card citing both.

## Notes and lessons learned
