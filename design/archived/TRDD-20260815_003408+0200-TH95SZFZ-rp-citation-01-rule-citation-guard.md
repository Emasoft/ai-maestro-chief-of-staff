---
trdd-id: TH95SZFZ
title: Adopt RP-CITATION-01 rule-citation guard once the hub ratifies it
column: complete
created: 2026-08-15T00:34:08+0200
updated: 2026-08-25T18:50:00+0200
current-owner: cos-plugin-dev-session
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: infra
min-approval-requirement: none
external-refs: [ai-maestro#145]
---

# Adopt RP-CITATION-01 rule-citation guard once the hub ratifies it

## ⏵ STATE — 2026-08-25 (UNBLOCKED — implementing)

hub#145 CLOSED; ruling LANDED as spec text RP-CITATION-01..04 in ai-maestro
`design/specs/role-plugins-spec.md` 1.2.0, commit 9422ec53 (verified first-hand via
gh api: issue state CLOSED, commit exists, spec section read at that sha).
Implementing against the RATIFIED text (which supersedes this card's earlier
sketch: scope is pinned `PRRD G/S<n>.<v>` citations vs THIS repo's own PRRD —
cross-repo `R<nn>.<m>` checking is out of scope per RP-CITATION-03's scope
statement). Acceptance floor is RP-CITATION-04: controls A–D seeded both
directions over COMMITTED synthetic text, each direction's input named.

## ⏵ prior STATE — 2026-08-19 (superseded)

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

- [x] Guard exists, red on a fabricated dead citation (falsified both directions).
      `scripts/amcos_citation_gate.py` + `tests/test_citation_integrity.py`: dangling
      `PRRD G9.1` REDS, superseded `PRRD S2.0` REDS, tier-mismatch `PRRD G2.1` REDS;
      a current pin, `→` narration, and fenced/inline-code grammar examples stay GREEN.
- [x] Population = git-tracked shipped prose, floor-pinned. `git ls-files '*.md'`
      minus the canon, self-exclusions, and terminal cards by `column:` PROPERTY;
      non-vacuity: zero files scanned = exit 2, never a pass (258 files scanned live).
- [x] Passes on the current tree. Green at tree 1a113af: 258 files, 6 pinned
      citations resolved, 7 rules hashed; full suite 350 passed.

## Acceptance record (RP-CITATION-04 — inputs named, tree named)

Committed controls over SYNTHETIC text (never mutate-and-restore of the live PRRD),
observed at tree 1a113af, all in `tests/test_citation_integrity.py`:

| control | seeded input | observed |
|---|---|---|
| A | G1.2 continuation line, `carrying`→`bearing`, no bump | RED (hash mismatch names the bump-first repair) |
| B | pure reflow of G1.2, same words re-wrapped | GREEN |
| C | wrapped-rule fixture (G1.2 body spans 2 lines) | whole-block parser sees the edit; REDS if it cannot |
| D | naive one-line `re.M` parser installed | observed BLIND to A's input (hashes identical) while the real parser reds — discrimination proven before trusting A/C |

Scope statement carried: green asserts citations + rule versions ONLY; container
stamps (`prrd-version:`, `updated:`) need their own witness (open on ai-maestro#145).

## Approval log

- 2026-08-25T18:50:00+0200 — COMPLETED by ai-maestro-chief-of-staff (Tier 0 — adoption
  of a ratified SILVER spec section, own repo scope). hub#145 CLOSED; ratified text
  RP-CITATION-01..04 @ ai-maestro 9422ec53 verified first-hand before implementing.
