---
trdd-id: B94VK7LR
title: Fix the troubleshooting step that instructs running a script that does not exist
column: todo
created: 2026-08-18T19:54:27+0200
updated: 2026-08-18T19:54:27+0200
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

- [ ] The resolution step names only commands/files that exist and work, run verbatim.
- [ ] `grep -rn "amcos_init_design_folders" .` returns 0 hits outside historical prose.
- [ ] Suite green, ruff clean.
