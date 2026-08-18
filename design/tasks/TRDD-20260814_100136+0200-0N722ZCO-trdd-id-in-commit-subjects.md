---
trdd-id: 0N722ZCO
title: Close the TRDD-id-in-commit-subject gap — measured at 2 percent compliance
column: backburner
created: 2026-08-14T10:01:36+0200
updated: 2026-08-14T10:01:36+0200
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: infra
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: self
min-approval-requirement: none
relevant-rules: [1]
external-refs: [ai-maestro#146]
---

# Close the TRDD-id-in-commit-subject gap

The `commit-discipline` rule requires the governing `TRDD-<id8>` in the subject of every
commit that implements it. Measured on this repo on 2026-08-14, while contributing to
`ai-maestro#146`:

```
last 200 commits
  touching a path outside design/          138
  whose message carries a TRDD-XXXXXXXX      3
  recall                                    2 %
```

This is a **self-mandate under Tier 0**: the work is entirely inside this plugin's own
repo and touches no governance file, no other project, and no release path.

## Why it matters beyond tidiness

`ai-maestro#146` is building the §D4 approval-ladder watchdog, whose only non-self-declared
input is git. The commit→TRDD link is what makes a diff attributable to a card, so at 2%
recall **98% of this repo's code changes are invisible to that audit** — and, more
importantly to me, un-backtrackable: the `implementation-commits:` field exists precisely so
a bug found later can be traced to the TRDD that introduced it, and it cannot be reconstructed
from history that never carried the id.

History cannot be relabelled (rewriting published history is forbidden), so this is
forward-only.

## Acceptance criteria

- [ ] Every new commit touching a path outside `design/` that implements a TRDD carries
      `TRDD-<id8>` in its subject.
- [ ] A measurement re-run over the commits made AFTER this card is opened shows recall
      materially above the 2% baseline (the baseline itself stays as the historical record).
- [ ] `implementation-commits:` on each open card is reconciled against git before the card
      leaves `testing`.

## Derived / open questions (NOT decided here)

- A `commit-msg` hook could warn (never block) when a code-touching commit omits an id.
  **Not proposed as part of this card** — a hook that fires on every commit needs its own
  design pass, and a blocking one would be worse than the gap it closes. If pursued it is a
  separate TRDD with its own acceptance criteria.
- Whether `implementation-commits:` should be derived from git rather than hand-written is
  an `ai-maestro#146` question, not this repo's, and is deliberately left there.

## Notes

Filed rather than fixed-on-impulse: the measurement is public on `ai-maestro#146`, but the
remedy is local to this repo and would otherwise vanish with the session that found it.
