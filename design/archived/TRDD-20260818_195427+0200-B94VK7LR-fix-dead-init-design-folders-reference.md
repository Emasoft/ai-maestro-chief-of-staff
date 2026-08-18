---
trdd-id: B94VK7LR
title: Fix the troubleshooting step that instructs running a script that does not exist
column: complete
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T23:50:30+0200
implementation-commits: [497536a]
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
release-via: publish
external-refs: [ai-maestro TRDD-BRRJK57P]
priority: 5
---

# Fix the troubleshooting step that instructs running a script that does not exist

Phase-2 remediation of axis-3's confirmed finding (report
`20260816_170956+0200-axis3-scripts.md`, hub-verified with positive control: 0 hits for the dead
name, 1 for a known-present one).

`skills/amcos-failure-notification/references/design-document-protocol.md:289` — a
troubleshooting RESOLUTION step ("design/ folder or subfolders don't exist" → "Run
`amcos_init_design_folders.py` to create structure") names a script that exists nowhere in the
repo. The worst placement for a dead reference: it is the instruction handed to someone already
stuck.

Fix: replace the step with the real remedy — a `mkdir -p design/{proposals,tasks,archived,refused}`
one-liner (verify against what the protocol doc itself defines as the required structure before
writing it), or point at whichever shipped script actually creates the layout if one exists
(verify first; the audit found none).

## Acceptance criteria

- [x] The resolution step names only commands that exist — the mkdir one-liner was RUN verbatim
      in a scratch dir before committing.
- [x] Repo grep: the only remaining `amcos_init_design_folders` hit is the deliberate historical
      note in the fixed step itself.
- [x] Suite green (341), ruff clean.

## Approval log

- 2026-08-18T23:50:30+0200 — COMPLETED. todo → dev → testing → ai_review (llm-ext ensemble 3/3
  APPROVE; report reports/llm-externalizer/20260818_234940+0200-code_task-b94.diff-18cf77.md)
  → complete. Implementation commit 497536a.
