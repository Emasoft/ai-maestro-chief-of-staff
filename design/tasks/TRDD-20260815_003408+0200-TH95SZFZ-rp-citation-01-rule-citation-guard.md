---
trdd-id: TH95SZFZ
title: Adopt RP-CITATION-01 rule-citation guard once the hub ratifies it
column: human_review
pre-block-column: todo
created: 2026-08-15T00:34:08+0200
updated: 2026-08-19T04:37:00+0200
current-owner: cos-plugin-dev-session
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: infra
min-approval-requirement: none
blocked-by: []
external-refs: [ai-maestro#145]
---

# Adopt RP-CITATION-01 rule-citation guard once the hub ratifies it

## ⏵ STATE — 2026-08-19

At `column: human_review`: the wait is on hub#145 RATIFICATION, a decision only the USER can
take (verified OPEN 2026-08-16, last event 2026-08-13 — pending a decision, not evidence).
The pointer lives in `external-refs:`, not `blocked-by:`, per the hub's interim grammar
(2026-08-19): trddgrep cannot yet express an external blocker (hub card TRDD-PTFPGSLV adds the
syntax; when it ships and `trddgrep validate` stops ERRORing on issue refs, a `blocked` +
`blocked-by: [gh:Emasoft/ai-maestro#145]` form becomes available again). On ratification:
implement per the card body.

## Why

Hub fleet-alignment directive (TRDD-BDRWMBDC, 2026-08-15) cites hub#145: rule citations
and rule versions in fleet repos break SILENTLY — a cited `R<nn>.<m>` can drift from the
canon (renumbered, re-versioned, deleted) with nothing going red. hub#145 is a PROPOSAL
by the PROGRAMMER (MEMBER — non-binding, explicitly not ratified), shipping two reference
implementations. Implementing ahead of ratification risks building against a spec that
changes at ratification.

## What (on ratification)

1. Read the ratified RP-CITATION-01 text + the reference implementations on hub#145.
2. Add a COS test guard that every `R<nn>(.<m>)?` / `PRRD G/S<n>.<v>` citation in shipped
   prose (git-tracked `.md`, per the `git ls-files` population lesson) resolves against
   the canon source, pinned by ref per the "never cite a rule without naming the ref" rule.
3. Wire it into the existing test suite (same style as `test_no_paging_owner_handle_in_shipped_prose`).

## Acceptance

- [ ] Guard exists, red on a fabricated dead citation (falsified both directions).
- [ ] Population = git-tracked shipped prose, floor-pinned.
- [ ] Passes on the current tree or every failure triaged to a real drift.

## Approval log
