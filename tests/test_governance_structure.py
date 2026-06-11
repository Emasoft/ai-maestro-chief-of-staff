"""Real (non-mocked) guard tests for the issue-#17 governance structure.

These assert the corrected fleet-readiness structure stays in place: the
four-zone design folders, the v2 TRDD `column:` schema (no v1 `status:`
leftovers), the PRRD `project-id:` + real SILVER rules, and the documented
ORCH-owned dialog loops. They read the real files; if a future edit regresses
any fix, the matching test goes red.
"""

from __future__ import annotations

import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
DESIGN = PLUGIN_ROOT / "design"
PRRD = DESIGN / "requirements" / "PRRD.md"
DOCS = PLUGIN_ROOT / "docs"


def test_four_zone_design_folders_exist() -> None:
    """design/{proposals,tasks,refused,archived,requirements} all exist (M3)."""
    for zone in ("proposals", "tasks", "refused", "archived", "requirements"):
        assert (DESIGN / zone).is_dir(), f"missing design/{zone}/"


def test_prrd_has_project_id_and_silver_rules() -> None:
    """PRRD carries project-id: and at least one real SILVER rule (M2)."""
    text = PRRD.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    assert re.search(r"^project-id:\s*\S+", fm, re.M), "PRRD frontmatter missing project-id:"
    silver = re.findall(r"^- \*\*S\d+\.\d+\*\*", text, re.M)
    assert silver, "PRRD has an empty SILVER section (ungoverned operations)"


def test_all_trdds_use_v2_column_schema() -> None:
    """Every TRDD in design/tasks/ uses the v2 `column:` field, no v1 `status:`.

    A v1 `**Status:**` bold line or a bare `status:` frontmatter field is the
    leftover issue #17 forbids.
    """
    trdds = list((DESIGN / "tasks").glob("TRDD-*.md"))
    assert trdds, "no TRDDs found in design/tasks/"
    offenders = []
    for t in trdds:
        text = t.read_text(encoding="utf-8")
        fm = text.split("---", 2)[1] if text.startswith("---") else ""
        has_column = bool(re.search(r"^column:\s*\S+", fm, re.M))
        has_v1_status = bool(re.search(r"^\*\*Status:\*\*", text, re.M)) or bool(
            re.search(r"^status:\s*\S+", fm, re.M)
        )
        if not has_column or has_v1_status:
            offenders.append(t.name)
    assert not offenders, f"TRDDs not on v2 column: schema: {offenders}"


def test_dialog_loops_doc_is_orch_owned() -> None:
    """docs/DIALOG_LOOPS.md exists and states the loops are ORCH-owned, COS-boundary-only (M7)."""
    doc = DOCS / "DIALOG_LOOPS.md"
    assert doc.is_file(), "docs/DIALOG_LOOPS.md is missing"
    text = doc.read_text(encoding="utf-8").lower()
    assert "orchestrator-owned" in text or "orch-owned" in text, "DIALOG_LOOPS.md must state ORCH ownership"
    assert "boundary" in text and "never" in text, "DIALOG_LOOPS.md must state COS never relays the loops"


def test_refreshed_docs_have_no_stale_workflow_terms() -> None:
    """The refreshed governance docs no longer present the v1 5-status board as the workflow (M4/M6)."""
    for name in ("FULL_PROJECT_WORKFLOW.md", "ROLE_BOUNDARIES.md", "AGENT_OPERATIONS.md"):
        text = (DOCS / name).read_text(encoding="utf-8").lower()
        assert "5-status kanban system" not in text, f"{name} still calls the board the workflow"
        # the corrected model must name the INTEGRATOR as the completion-flip owner
        assert "integrator" in text, f"{name} must reference the INTEGRATOR role"
