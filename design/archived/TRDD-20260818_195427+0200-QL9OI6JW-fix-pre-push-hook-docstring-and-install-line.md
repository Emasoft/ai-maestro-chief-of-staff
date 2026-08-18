---
trdd-id: QL9OI6JW
title: Fix the pre-push hook's self-name, dead install line, and false severity claim
column: complete
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T23:49:31+0200
implementation-commits: [497536a]
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

- [x] Docstring self-name matches the real filename → 0 residual `pre-push-hook.py` refs in file.
- [x] Install line copies the file that exists → `ls scripts/amcos_pre_push_hook.py` asserted.
- [x] Docstring states strict-mode blocking (all severities), matching :298 — with a comment on
      WHY it must stay coupled to main().
- [x] Suite green (341), ruff clean.

## Approval log

- 2026-08-18T23:49:31+0200 — COMPLETED. todo → dev → testing → ai_review (llm-ext ensemble 3/3
  APPROVE; report reports/llm-externalizer/20260818_234921+0200-code_task-ql9.diff-a037ad.md)
  → complete. Implementation commit 497536a.
