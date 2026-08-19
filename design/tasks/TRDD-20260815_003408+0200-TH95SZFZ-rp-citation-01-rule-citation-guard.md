---
trdd-id: TH95SZFZ
title: Adopt RP-CITATION-01 rule-citation guard once the hub ratifies it
column: blocked
pre-block-column: todo
created: 2026-08-15T00:34:08+0200
updated: 2026-08-19T05:20:00+0200
current-owner: cos-plugin-dev-session
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: infra
min-approval-requirement: none
blocked-by: [gh:Emasoft/ai-maestro#145]
external-refs: [ai-maestro#145]
---

# Adopt RP-CITATION-01 rule-citation guard once the hub ratifies it

## ⏵ STATE — 2026-08-19

At `column: blocked` on `blocked-by: [gh:Emasoft/ai-maestro#145]` — the sanctioned
external-blocker spelling, adopted 2026-08-19 the moment hub TRDD-PTFPGSLV shipped
(c242d4ca): `trddgrep validate` now emits WARN GRAPH-EXTERNAL-BLOCKER for it instead of an
ERROR, and the graph verbs report the card as BLOCKED. This replaces the interim
human_review park (the pointer had lived in `external-refs:` only). The wait itself is
unchanged: hub#145 RATIFICATION, a decision only the USER can take. On ratification: clear
`blocked-by`, restore `pre-block-column: todo`, implement per the card body.

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
