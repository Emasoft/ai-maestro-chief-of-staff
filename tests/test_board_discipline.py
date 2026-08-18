"""The checklist gate, enforced on THIS repo's board (TRDD-Q7BZ8N3M).

The gate (`aimaestro-trdd-approval.md:801-824`, Emasoft/ai-maestro@governance-rules
tip 7b5e02ca): a TRDD may sit in `complete`/`published`/`live` ONLY when its bottom
checklist EXISTS (>=1 box) and every box is `- [x]`. A terminal column with any
unchecked box is a false completion — **and so is one with no checklist at all**.

Nine cards here violate it, every one transitioned 2026-08-11, i.e. inside the
governed window (the rule binds transitions from 2026-07-31 on). They are recorded
below as EXPLICIT, BOUNDED debt rather than being repaired by a sweep: eight are
`published` with work that demonstrably shipped, so moving them back to `dev` would
assert something more false than the missing checklist does, and retro-ticking a box
fabricates the very verification record the checklist was supposed to BE. The
disposition is TRDD-Q7BZ8N3M's first acceptance box and belongs to the human.

WHY THIS GUARD EXISTS ANYWAY, BEFORE THAT DECISION: the nine arose because nothing
checked. A disposition without a guard just resets the clock. This is the one part
of Q7BZ8N3M that is independent of which disposition is chosen — the tenth violation
is prevented identically either way.

The debt list is exact in BOTH directions on purpose (see the second test): a new
violation reds, and so does a stale entry for a card someone has since fixed. That
is the same technique the upstream rule used when it named its own three
non-grandfathered cards "so the boundary is auditable rather than asserted".
"""

from __future__ import annotations

import re
from pathlib import Path

DESIGN = Path(__file__).resolve().parent.parent / "design"
TERMINAL = {"complete", "published", "live"}

# id8 -> why it is here. MAY ONLY SHRINK (see test_debt_list_may_only_shrink).
KNOWN_UNGATED: dict[str, str] = {
    # Ids uppercase since `trddgrep fix` normalized trdd-id: to 8-char UPPERCASE base36
    # (2026-08-19, mechanical, updated: untouched). Dates below are the ARCHIVAL date the
    # original card used; the true transitions are June 2026 — pre-boundary, frozen
    # (Q7BZ8N3M disposition, f15f1df). These are NOT repairable debt, they are the
    # guard's map of why the eight are exempt.
    "227E77D0": "published (frozen pre-boundary), no checklist",
    "5F717DED": "published (frozen pre-boundary), no checklist",
    "0263F190": "published (frozen pre-boundary), no checklist",
    "59581001": "published (frozen pre-boundary), no checklist",
    "E3156858": "published (frozen pre-boundary), no checklist",
    "562B49E3": "published (frozen pre-boundary), 5 boxes ALL unchecked; the work shipped (v2.19.0 tag exists), the boxes were never ticked",
    "B0048A21": "published (frozen pre-boundary), no checklist",
    "5C4EB0EC": "published (frozen pre-boundary), no checklist",
}

# The measured size of the debt on 2026-08-12. The list may only SHRINK, so this
# number is a ratchet: adding a tenth entry requires editing this line, which is a
# visible, deliberate act in a diff. Without it, the escape hatch is to add a new
# violation and its exemption in the same commit and stay green.
_DEBT_CEILING = 8

_BOX = re.compile(r"^[ \t]*- \[([ xX])\]", re.MULTILINE)


def _cards() -> list[tuple[str, str, Path, int, int]]:
    """(id8, column, path, total_boxes, unchecked_boxes) for every TRDD on the board."""
    out = []
    for path in sorted(DESIGN.rglob("TRDD-*.md")):
        text = path.read_text(encoding="utf-8")
        col = re.search(r"^column:[ \t]*(\S+)", text, re.MULTILINE)
        tid = re.search(r"^trdd-id:[ \t]*(\S+)", text, re.MULTILINE)
        if not col or not tid:
            continue
        boxes = _BOX.findall(text)
        out.append((tid.group(1)[:8], col.group(1), path, len(boxes), sum(b == " " for b in boxes)))
    return out


def _failing() -> dict[str, str]:
    """Terminal cards that fail the gate, id8 -> one-line reason."""
    bad = {}
    for tid, col, _path, total, unchecked in _cards():
        if col not in TERMINAL:
            continue
        if total == 0:
            bad[tid] = f"{col}, no checklist at all"
        elif unchecked:
            bad[tid] = f"{col}, {unchecked}/{total} boxes unchecked"
    return bad


def test_the_board_is_actually_being_read() -> None:
    """Non-vacuity: prove the scan sees a corpus before any negative result is trusted.

    ARCHITECT's rule from ai-maestro#131, generalised past sweeps: verify a check by
    confirming it FINDS SOMETHING YOU KNOW IS THERE, never by confirming it runs
    without error. A `rglob` against a moved or renamed `design/` returns [], every
    assertion below passes vacuously, and the suite reports the board is clean.
    Measured cost of skipping this class of check today: a TRDD collision check that
    scanned zero roots and reported the id FREE.
    """
    cards = _cards()
    assert len(cards) >= 10, f"only {len(cards)} TRDDs found under {DESIGN} — the scan is broken, not the board clean"
    assert any(c[1] in TERMINAL for c in cards), "no terminal cards found at all; the gate would be untested"


def test_no_new_terminal_card_bypasses_the_checklist_gate() -> None:
    """The tenth violation must be impossible to create silently.

    This is the box that does not depend on how the existing nine are dispositioned:
    whichever way that goes, a card entering a terminal column without a complete
    checklist is a false completion, and nothing was catching it.
    """
    new = {tid: why for tid, why in _failing().items() if tid not in KNOWN_UNGATED}
    assert not new, (
        "terminal card(s) fail the checklist gate and are not in the recorded debt: " + "; ".join(f"{t} ({w})" for t, w in sorted(new.items())) + ". A TRDD may enter complete/published/live only when its checklist EXISTS "
        "(>=1 box) and every box is checked. Do NOT fix this by ticking boxes "
        "retroactively — that fabricates the verification record the checklist was "
        "supposed to be. Either finish the work and check the boxes against real "
        "evidence, or leave the card in a non-terminal column."
    )


def test_debt_list_may_only_shrink() -> None:
    """The exemption list is exact in BOTH directions — stale entries red too.

    A one-directional check (is every failure exempted?) rots the moment a card is
    repaired: its entry lingers, silently re-exempting the id if that card ever
    regresses. Requiring exact equality means fixing a card FORCES removing its
    entry, so the list is always the true, current debt rather than a historical
    high-water mark nobody prunes.
    """
    failing = set(_failing())
    listed = set(KNOWN_UNGATED)
    stale = listed - failing
    assert not stale, f"{sorted(stale)} are listed as ungated debt but now PASS the gate. Remove them from KNOWN_UNGATED — a stale exemption silently re-exempts that card if it ever regresses."
    assert len(listed) <= _DEBT_CEILING, f"the debt list grew to {len(listed)} (ceiling {_DEBT_CEILING}). It may only shrink. If you are adding an entry you are recording a NEW false completion as acceptable — which is the failure this file exists to prevent."


def test_every_card_declares_a_column_in_the_ratified_enum() -> None:
    """A column outside the 17-value vocabulary makes the board unreadable.

    Cheap, and it is the precondition for every other assertion here: the gate keys
    on `column:`, so a typo'd value silently removes a card from the gate's scope
    rather than failing loudly.
    """
    ratified = {
        "backburner",
        "todo",
        "design",
        "dispatch",
        "dev",
        "testing",
        "ai_review",
        "human_review",
        "complete",
        "publish",
        "published",
        "deploy",
        "live",
        "live_auditing",
        "blocked",
        "failed",
        "superseded",
        "proposal",
        "planned",
        "refused",
        "cancelled",
        "completed",
    }
    bad = [(tid, col, p.name) for tid, col, p, _t, _u in _cards() if col not in ratified]
    assert not bad, f"column value outside the ratified vocabulary: {bad}"
