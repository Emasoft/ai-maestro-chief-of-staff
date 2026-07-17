"""Guard: the replace-agent flow makes replacement decisions WITH kanban context
(COS#11 item 3), and does it the R42-compliant read-only way.

COS#11 named the gap precisely: "Agent replacement decisions are made without
kanban context (no data on in-progress task count)." The fix is a Phase-1 step
that queries the failing agent's in-flight load via the frozen CLI before the
replacement decision, feeding the impact estimate and the AMOA reassignment.

Why guard a doc step: the capability lives in skill prose, and a well-meaning
edit that drops the capture step would silently return the flow to blind
replacement — undetectable in operation until an agent is replaced mid-work with
no reassignment. The guard also pins the R42 boundary: the step must stay
READ-ONLY (amp-kanban-list is observation, not driving) and must NOT reassign
tasks itself (that is ORCHESTRATOR-owned).

Stdlib + pytest only, matching the rest of the suite.
"""

from __future__ import annotations

import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
OP = PLUGIN_ROOT / "skills" / "amcos-agent-replacement" / "references" / "op-replace-agent.md"
SKILL = PLUGIN_ROOT / "skills" / "amcos-agent-replacement" / "SKILL.md"


def _flat(p: Path) -> str:
    """Whitespace-normalized text so a re-wrap can't fail the guard, only a deletion can."""
    return re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))


def test_replace_op_captures_in_flight_kanban_load_before_deciding() -> None:
    """op-replace-agent documents capturing the failing agent's in-progress kanban load."""
    t = _flat(OP)
    assert "in-flight kanban load" in t, "op-replace-agent missing the kanban-context capture step"
    assert "amp-kanban-list.sh --assignee" in t, (
        "capture step must use the frozen CLI amp-kanban-list --assignee (successor to the removed REST call)"
    )


def test_replace_op_feeds_the_count_into_impact_not_a_placeholder() -> None:
    """The Phase-2 approval impact is data-driven from the capture, not the old 'Tasks X, Y, Z' stub."""
    t = _flat(OP)
    assert "Tasks X, Y, Z are blocked" not in t, "Phase-2 impact still uses the content-free placeholder"
    assert "from the Phase-1 kanban capture" in t, "Phase-2 impact must reference the kanban capture"


def test_replace_op_capture_is_read_only_and_not_self_reassignment() -> None:
    """The capture is read-only observation (R42) and reassignment stays ORCHESTRATOR-owned."""
    t = _flat(OP)
    assert "read-only" in t.lower(), "the kanban capture must be marked read-only (R42 observation, not driving)"
    assert "reassignment on the kanban is ORCHESTRATOR-owned" in t, (
        "the op must state COS supplies context and requests the move — it does not reassign itself"
    )


def test_skill_summary_reflects_the_kanban_context_step() -> None:
    """The SKILL top-level flow surfaces the kanban capture so it is not buried in the op detail."""
    t = _flat(SKILL)
    assert "capture the failing agent's in-progress kanban load" in t, (
        "SKILL summary step 3 must name the data-driven kanban capture"
    )
