---
trdd-id: QL9OI6JW
title: Fix the pre-push hook's self-name, dead install line, and false severity claim
column: todo
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T19:54:27+0200
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: bugfix
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
priority: 4
---

# Fix the pre-push hook's self-name, dead install line, and false severity claim

Phase-2 remediation of axis-4 Findings 1+3 and the axis-3 script-quality note (reports
`20260816_232523+0200-axis4-bugs-conflicts.md` incl. addendum, `20260816_170956+0200-axis3-scripts.md`;
hub-verified). Three defects, one file — `scripts/amcos_pre_push_hook.py`:

1. **Self-name drift** (:2): docstring opens `"""pre-push-hook.py - ...` while the file ships as
   `amcos_pre_push_hook.py`. The self-reference is what ANCHORED defect 2 — a stale reference to
   a file that "names itself" reads as internally consistent.
2. **Dead install line** (:8): `cp scripts/pre-push-hook.py .git/hooks/pre-push` — that path does
   not exist (0 hits; control 1). Anyone following the docstring installs no hook.
3. **False severity claim** (:5, :10-13): docstring says only CRITICAL blocks; `main()` at :298
   is `if critical or major or minor: return 1` (its own comment: "strict mode: block on ALL
   issues including MINOR"). Fails safe, but the doc misinforms.

Fix the DOCSTRING to the code, not the code to the docstring — strict mode is the deliberate
behaviour per the in-code comment.

## Acceptance criteria

- [ ] Docstring self-name matches the real filename.
- [ ] Install line copies the file that exists; run the `cp` verbatim in a scratch clone or
      assert the source path exists before claiming done.
- [ ] Docstring states strict-mode blocking (all severities), matching :298.
- [ ] Suite green, ruff clean.
