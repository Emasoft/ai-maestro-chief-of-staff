---
trdd-id: Q7BZ8N3M
title: Resolve the nine terminal-column cards that fail the checklist gate
column: todo
created: 2026-08-12T12:42:35+0200
updated: 2026-08-12T12:42:35+0200
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

## Acceptance criteria

- [ ] A disposition chosen (1/2/3) and recorded here with its rationale.
- [ ] Each of the nine cards resolved per that disposition, one at a time, no scripted sweep.
- [ ] No box ticked retroactively anywhere; any box that is checked is checked against
      named evidence.
- [x] A guard added that fails when a card enters a terminal column without a complete
      checklist, so this cannot recur silently. → `tests/test_board_discipline.py`
      (4 tests, suite 322 → 326). Done AHEAD of the disposition on purpose: it is the
      only box here that does not depend on which of 1/2/3 is chosen, since the tenth
      violation is prevented identically either way.
- [ ] Suite green, ruff clean.

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
