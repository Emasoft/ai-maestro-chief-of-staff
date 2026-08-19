---
trdd-id: Q7BZ8N3M
title: Resolve the nine terminal-column cards that fail the checklist gate
column: completed
created: 2026-08-12T12:42:35+0200
updated: 2026-08-19T04:55:00+0200
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
min-approval-requirement: 0
relevant-rules: [1]
created-by: M4761P58
external-refs: [ai-maestro#76]
---

# Resolve the nine terminal-column cards that fail the checklist gate

Derived (EHT) from **TRDD-M4761P58**, which read the gate at its normative source and
then applied it here. Filed rather than fixed inline because the remedy needs a
**per-card judgment**, and the blanket remedy is wrong for most of these cards.

## The rule, and why these nine are not grandfathered

`aimaestro-trdd-approval.md:801-824` (`Emasoft/ai-maestro@governance-rules`, tip
`7b5e02ca`, fetched 2026-08-12): a TRDD may sit in `complete`/`published`/`live` **only
when its bottom checklist EXISTS (≥1 box) and every box is `- [x]`**. A terminal column
with any unchecked box is a false completion — **and so is one with no checklist at all**.

The grandfather boundary is **2026-07-31**: cards already terminal before it are FROZEN
and are not flagged. **All ten of this repo's terminal cards transitioned 2026-08-11**, so
every one of them is inside the governed window. Measured, not assumed:

| Card | Column | Boxes | Unchecked | Verdict |
|---|---|---|---|---|
| `227e77d0` `5f717ded` `0263f190` `59581001` `e3156858` `b0048a21` `5c4eb0ec` | `published` | 0 | — | no checklist at all |
| `562b49e3` | `published` | 5 | **5** | every box unchecked |
| `4FH9JP4U` | `complete` | 0 | — | no checklist at all |
| `NB725X9W` | `complete` | 5 | 0 | **passes** |

## Why the stated remedy must not be applied as a sweep

The rule's remedy is *move it back to `pre-block-column:` (or `dev`) and flag*. Applied
blindly here it produces a **worse falsehood than the one it clears**: eight of these are
`published`, and the work demonstrably shipped — releases exist. A board asserting that
shipped work is back in `dev` misinforms every reader, where a missing checklist merely
fails to inform them.

`562b49e3` is the instructive one. It is `published` with all five boxes unchecked,
including a box that reads *"Published (v2.19.0); reported on COS#21 + ai-maestro#37"*.
The work was done; the boxes were never ticked when the card closed. **That is exactly
what the gate cannot distinguish** — from the board alone, "done but unticked" and "never
done" are the same picture. Which is the argument FOR the gate, not against it.

**Retro-ticking is not on the table.** Ticking a box today to clear a flag fabricates the
verification record the checklist was supposed to BE. If a box's claim is true, the
evidence for it exists somewhere other than the box; if it does not, ticking it is a lie
with a checkmark on it.

## The decision this card needs

Three candidate dispositions, per card, and the choice is not purely mine — un-publishing
a card is an outward-facing assertion about released work:

1. **Leave terminal + annotate.** Add a dated note recording that the card predates this
   repo's adoption of the gate and naming the external evidence (release tag, commit) that
   substitutes for the checklist. Honest, non-destructive, but does not satisfy the rule as
   written.
2. **Move back, complete honestly, re-close.** Restore to `dev`, write the checklist that
   should have existed, verify each box against real evidence, re-advance. Correct by the
   book; expensive, and transiently asserts that shipped work is unshipped.
3. **Treat the 2026-08-11 batch as a local grandfather boundary** and apply the gate
   strictly from today forward — mirroring how the upstream rule itself handled its own 46
   pre-existing cards.

Option 3 is the closest analogue to what the rule's own authors did, and it is what I would
recommend — but it is a governance judgment about someone else's rule applied to this
repo's public history, so it is raised rather than taken.

## ⏵ DISPOSITION — DECIDED 2026-08-16 (supersedes the three options above)

**None of 1, 2 or 3. The question those options answer does not exist, because this card's
central premise is false.** The premise was: *"All ten of this repo's terminal cards
transitioned 2026-08-11, so every one of them is inside the governed window."* Measured:
**eight of the nine transitioned in JUNE 2026**, before the rule's own 2026-07-31 boundary.

| card | terminal column first set | commit |
|---|---|---|
| `227e77d0` `5f717ded` `0263f190` | 2026-06-11 | `10d57ca`, `6a986b7` |
| `59581001` `e3156858` | 2026-06-14 | `fced238`, `1bea658` |
| `562b49e3` | 2026-06-18 | `c26e442` |
| `b0048a21` | 2026-06-20 | `260bafe` |
| `5c4eb0ec` | 2026-06-22 | `146a17b` |
| **`4FH9JP4U`** | **2026-08-11** | **`779a8b2`** |

Method: `git log --follow --format='%ad %h' --date=short -S"column: <value>" -- <path> | tail -1`
— the OLDEST commit touching that column string, i.e. when it was first set. Cross-checked
against each file's `--diff-filter=A` add commit so the dates are not a `--follow` artifact.

**Where the false premise came from, because the mechanism matters more than the correction.**
The 2026-08-11 event was commit `2400fa2`, *"docs(board): file 10 terminal TRDDs into
design/archived/"*, whose own message reads: *"git mv ONLY — no frontmatter touched...
Deliberately did NOT bump `updated:`, per the TRDD rule that a mechanical repair must not."*
It was an **archival filing**, and a later reader took its date for a transition date. The
commit did the correct thing and said so; the date it left behind was simply the wrong date to
read. `updated:` was deliberately not bumped **precisely so** this would not look like a
change — and the filing date got used instead.

**What the rule actually says**, fetched verbatim from `Emasoft/ai-maestro@governance-rules`,
`rules/aimaestro/aimaestro-trdd-approval.md:801-824`, rather than quoted from this card:

> "the gate binds the TRANSITION INTO a terminal column, never the card's whole life"
>
> "GRANDFATHER BOUNDARY: a card already in a terminal column is FROZEN (IND base step 12), so
> those 46 cannot be repaired and are not flagged... What the fix changes is every terminal
> transition FROM 2026-07-31 ON."

So the eight June cards are not violations awaiting a disposition. They are **frozen and not
flagged by the rule's own terms**, and no local boundary needs declaring — the upstream
boundary already covers them. **The debt is ONE card, not nine.**

**`562b49e3` specifically: leave it alone.** It is the loudest-looking of the nine — `published`
with five boxes, all open, one of them reading *"Published (v2.19.0)"*. The hub session advised
annotating it with its release evidence. Its transition is 2026-06-18, **pre-boundary**, so IND
step 12 freezes it and the annotation would breach the freeze to satisfy a gate that does not
bind it. The hub accepted this correction: the rule it was citing had already answered the
question it asked me to work around. A card that looks worst is not the same as a card that is
in scope.

**`4FH9JP4U` is the one genuine violation** — `column: complete` set 2026-08-11, post-boundary,
zero checklist boxes in 143 lines. It is also the vacuous case the "≥1 box" clause was added
for: a gate stated only over boxes that are *unchecked* passes on a card with no boxes at all.

Its work IS done. Its `## Approval log` records three checks run at close, and all three were
re-run 2026-08-16 and still pass: the R42 injection-INSTRUCTION prose is gone (what remains is
prose *prohibiting* injection, in four skills); `kill -TERM` of a peer is absent; the suite is
green (299 then, 340 now). What is missing is the checklist section, not the verification.

Planned repair, DEFERRED (see below): move it to `column: dev` — the rule's own stated remedy,
which also lifts the step-12 freeze — write the checklist from those three checks, tick each
against the 2026-08-16 re-run, and re-advance. That is not retro-ticking: retro-ticking is
ticking a box whose verification never happened, and here the verification happened, was
recorded, and was re-run before any box is ticked.

**Why the repair is not executed in this edit.** `4FH9JP4U` is also a CONFIRMED finding of the
Phase-1 self-audit under the USER fleet mandate `TRDD-BRRJK57P` (axis 2), and that mandate is
explicit: discovery only, fix nothing, because a fix during discovery destroys the evidence the
remediation plan is built from. Phase-2 dispatch is blocked on the USER. So the disposition is
decided and recorded here; the one repair it implies is Phase-2 work.

**Corroboration, because a conclusion this convenient deserves it.** An independent audit agent
was given the rule text and the git method but NOT this conclusion, and reproduced the same
table and the same verdict — including two POST-boundary cards this card never considered
(`NB725X9W` 2026-08-08, `M4761P58` 2026-08-12), both of which PASS with full checklists. The
hub session, which owns the rule, agrees with the reading. Two advisor consultations were
dispatched to attack the conclusion and both froze without returning (16.5 KB and 17.9 KB of
transcript, flat, no verdict) — recorded here as an explicit gap rather than an endorsement I
did not receive.

**What this cost, stated plainly:** the original nine were filed on a date read from the wrong
artifact, and every option debated afterwards inherited it. Nothing was fabricated and every
individual fact in this card was true; the one thing nobody measured was whether the gate
applied at all.

## Acceptance criteria

- [x] A disposition chosen and recorded here with its rationale. → the DISPOSITION section
      above, 2026-08-16. The chosen answer is NONE of 1/2/3, because the premise the three
      options rested on was measured false.
- [x] Each of the nine cards resolved per that disposition, one at a time, no scripted sweep.
      → eight RESOLVED as "not violations, frozen pre-boundary, no action" (measured per
      card, see the table). The ninth, `4FH9JP4U`, repaired 2026-08-18 via `TRDD-4HSTGXGB`
      (Phase-2 dispatch f15f1df): reopened to `dev`, checklist written from its three recorded
      checks, each ticked against the 2026-08-18T23:50:51 re-run, re-closed to `complete`;
      `KNOWN_UNGATED` shrunk 9 → 8 (the shrink-only test forced the removal). Verified
      first-hand 2026-08-19 in `design/archived/TRDD-…-4HSTGXGB-repair-4FH9JP4U-checklist.md`.
- [x] No box ticked retroactively anywhere; any box that is checked is checked against
      named evidence. → held. The `4FH9JP4U` repair, when it runs, ticks its boxes against the
      2026-08-16 re-run of its own three recorded checks, never against its prose.
- [x] A guard added that fails when a card enters a terminal column without a complete
      checklist, so this cannot recur silently. → `tests/test_board_discipline.py`
      (4 tests, suite 322 → 326). Done AHEAD of the disposition on purpose: it is the
      only box here that does not depend on which of 1/2/3 is chosen, since the tenth
      violation is prevented identically either way.
- [x] Suite green, ruff clean. → re-run 2026-08-19T04:55: `uv run --with pytest pytest tests/`
      → 341 passed, exit 0; `ruff check .` → all checks passed, exit 0.

## Notes

- The gate lives in an overlay (`aimaestro-trdd-approval.md`), **not** in the governance
  spec, and **neither overlay is installed on this machine** — they are server-installed
  into registered agent workdirs, and this is a plugin-development session. A rule that
  governs this board is structurally invisible from it, which is why it went unapplied.
- The guard box mattered most and is now closed: nine violations arose because nothing
  checked, and a disposition without a guard just resets the clock. The nine are recorded
  in `KNOWN_UNGATED` as **explicit, bounded, shrink-only** debt — a stale entry reds as
  loudly as a new violation, so repairing a card FORCES removing its exemption, and the
  list can never quietly become a high-water mark nobody prunes. A `_DEBT_CEILING` makes
  adding a tenth entry a visible edit rather than a same-commit escape hatch.
- Whichever disposition is chosen, the mechanical work is now bounded: remove entries from
  `KNOWN_UNGATED` as cards are resolved, and the suite tells you when the list is wrong in
  either direction.

## Approval log

- 2026-08-19T04:55:00+0200 — COMPLETED by ai-maestro-chief-of-staff (tier 0, own-scope docs
  card). All five acceptance boxes closed: disposition decided 2026-08-16, the one in-scope
  violation (`4FH9JP4U`) repaired 2026-08-18 via TRDD-4HSTGXGB, guard test in place, suite
  341 green + ruff clean re-run at close.
