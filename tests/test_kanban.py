"""Real unit tests for the SERVER-INDEPENDENT kanban logic (COS#11 / #26).

These exercise ONLY the pure logic that needs no AI Maestro server and no real
CLI: the canonical column-ID set, the fallback `DEFAULT_BOARD_COLUMNS` shape,
the column-id extraction, the verify-and-correct branching in
`ensure_kanban_columns`, and the `summarize_velocity` reducer.

`ensure_kanban_columns` / `kanban_velocity` take their CLI runner as a parameter
(dependency injection), so the branching is tested by passing a real in-test
callable that returns canned CLI-result dicts. This is NOT mocking the CLI or
the server — it substitutes the side-effecting boundary the module was designed
to inject, and asserts the module's REAL decision logic (set-compare, drift →
--set, fail-fast on a non-zero exit). The live server round-trip is out of
scope here:

# integration round-trip: needs live server, see TRDD-5c4eb0ec step 5

Stdlib + pytest only (the plugin declares zero runtime dependencies).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# The scripts live alongside the package; add to path like run-all-tests.py does.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from amcos_kanban import (  # noqa: E402
    DEFAULT_BOARD_COLUMNS,
    KANBAN_BOARD_COLUMN_IDS,
    _extract_column_ids,
    ensure_kanban_columns,
    summarize_velocity,
)

# The 3-pillars 3.0.0 22-column board enum, in lifecycle order — COS's source
# of truth (spec `@spec:kanban-columns v2`, 3P-KAN-01/04; bracket values are
# deliberately absent per 3P-KAN-20).
EXPECTED_IDS = [
    "backburner",
    "approval",
    "design",
    "design_ai_review",
    "design_human_review",
    "todo",
    "verify_assumptions",
    "plan",
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
]


# ───────────────────────── canonical column-ID set ──────────────────────────
def test_canonical_ids_are_the_22_board_columns_in_order() -> None:
    """KANBAN_BOARD_COLUMN_IDS is the 22 board column ids in 3.0.0 lifecycle order."""
    assert KANBAN_BOARD_COLUMN_IDS == EXPECTED_IDS
    assert len(EXPECTED_IDS) == 22


def test_canonical_ids_have_no_duplicates() -> None:
    """The canonical id list has no duplicate entries (a SET-safe source of truth)."""
    assert len(KANBAN_BOARD_COLUMN_IDS) == len(set(KANBAN_BOARD_COLUMN_IDS))


# ──────────────────── DEFAULT_BOARD_COLUMNS shape ─────────────────────────
def test_default_columns_mirror_the_ratified_board() -> None:
    """DEFAULT_BOARD_COLUMNS carries the 22 ratified board entries (3-pillars 3.0.0)."""
    # 22 mirrors the server's own DEFAULT_KANBAN_COLUMNS (3-pillars 3.0.0).
    # The PUT route's Zod cap is .max(27) — the 3P-KAN-20 legal `column:` set —
    # since ai-maestro e3446edf (2026-08-25; COS reported the stale .max(20),
    # hub fixed same hour). No <=N assertion here: this repo aligns TO the
    # ratified spec, and the server bound is the server's test to keep.
    assert len(DEFAULT_BOARD_COLUMNS) == 22


def test_default_columns_ids_equal_canonical_set() -> None:
    """The fallback columns' ids (in order) equal KANBAN_BOARD_COLUMN_IDS."""
    assert [c["id"] for c in DEFAULT_BOARD_COLUMNS] == KANBAN_BOARD_COLUMN_IDS


def test_default_columns_every_entry_has_nonempty_id_label_color() -> None:
    """Every fallback column carries a non-empty id, label, AND color (PUT requires color)."""
    for col in DEFAULT_BOARD_COLUMNS:
        for key in ("id", "label", "color"):
            assert key in col, f"column {col!r} missing required key {key!r}"
            assert isinstance(col[key], str) and col[key].strip(), (
                f"column {col!r} has empty {key!r}"
            )


def test_default_columns_serialize_as_a_json_array() -> None:
    """The fallback serializes to a JSON ARRAY — the exact shape `--set` accepts."""
    payload = json.loads(json.dumps(DEFAULT_BOARD_COLUMNS))
    assert isinstance(payload, list) and len(payload) == 22


# ─────────────────────────── _extract_column_ids ────────────────────────────
def test_extract_column_ids_from_get_payload() -> None:
    """_extract_column_ids pulls ids in order from a {columns:[...]} GET payload."""
    data = {"columns": [{"id": "todo", "label": "x", "color": "y"}, {"id": "dev"}]}
    assert _extract_column_ids(data) == ["todo", "dev"]


@pytest.mark.parametrize("bad", [None, {}, {"columns": None}, {"columns": "x"}, [], "nope"])
def test_extract_column_ids_returns_empty_on_malformed(bad: object) -> None:
    """A missing/malformed columns payload yields [] (treated as drift, never a false match)."""
    assert _extract_column_ids(bad) == []


# ──────────────── ensure_kanban_columns verify-and-correct ──────────────────
def _ok_get(ids: list[str]) -> dict:
    return {"success": True, "data": {"columns": [{"id": i, "label": i, "color": "c"} for i in ids]}}


def test_ensure_noop_when_columns_already_match() -> None:
    """When the board already carries the canonical set, ensure is a no-op (GET only, no --set)."""
    calls: list[list[str]] = []

    def runner(argv: list[str], _ctx: str) -> dict:
        calls.append(argv)
        assert "--set" not in argv, "must NOT --set when columns already match"
        return _ok_get(list(KANBAN_BOARD_COLUMN_IDS))

    result = ensure_kanban_columns("team-1", runner, "aimaestro-teams.sh")
    assert result == {"success": True, "action": "ok", "team_id": "team-1", "message": "columns OK"}
    assert len(calls) == 1 and "--get" in calls[0]


def test_ensure_noop_ignores_column_order() -> None:
    """A reordered-but-complete board is still a no-op (the comparison is set-based)."""
    reordered = list(reversed(KANBAN_BOARD_COLUMN_IDS))

    def runner(argv: list[str], _ctx: str) -> dict:
        assert "--set" not in argv
        return _ok_get(reordered)

    result = ensure_kanban_columns("team-1", runner, "aimaestro-teams.sh")
    assert result["action"] == "ok"


def test_ensure_corrects_on_drift_with_set() -> None:
    """On a drifted board, ensure issues a --set carrying the full 17-col fallback JSON array."""
    set_payloads: list[str] = []

    def runner(argv: list[str], _ctx: str) -> dict:
        if "--get" in argv:
            return _ok_get(["todo", "dev", "done"])  # legacy / wrong set
        if "--set" in argv:
            set_payloads.append(argv[argv.index("--set") + 1])
            return {"success": True, "data": {"columns": DEFAULT_BOARD_COLUMNS}}
        raise AssertionError(f"unexpected argv {argv}")

    result = ensure_kanban_columns("team-2", runner, "aimaestro-teams.sh")
    assert result["success"] and result["action"] == "corrected"
    assert len(set_payloads) == 1
    sent = json.loads(set_payloads[0])
    assert [c["id"] for c in sent] == KANBAN_BOARD_COLUMN_IDS


def test_ensure_corrects_on_empty_board() -> None:
    """An empty/unparseable column config is treated as drift and corrected via --set."""
    saw_set = {"v": False}

    def runner(argv: list[str], _ctx: str) -> dict:
        if "--get" in argv:
            return {"success": True, "data": {"columns": []}}
        saw_set["v"] = True
        return {"success": True, "data": {"columns": DEFAULT_BOARD_COLUMNS}}

    result = ensure_kanban_columns("team-3", runner, "aimaestro-teams.sh")
    assert result["action"] == "corrected" and saw_set["v"]


def test_ensure_fail_fast_on_get_error() -> None:
    """A non-zero exit on --get fails fast (returns the error; never blind-sets)."""
    def runner(argv: list[str], _ctx: str) -> dict:
        assert "--set" not in argv, "must not --set after a failed --get"
        return {"success": False, "error": "boom: GET failed"}

    result = ensure_kanban_columns("team-4", runner, "aimaestro-teams.sh")
    assert result == {"success": False, "error": "boom: GET failed"}


def test_ensure_fail_fast_on_set_error() -> None:
    """A non-zero exit on --set propagates the error (no clean-success masking)."""
    def runner(argv: list[str], _ctx: str) -> dict:
        if "--get" in argv:
            return _ok_get(["todo"])  # drift → triggers a --set
        return {"success": False, "error": "boom: SET rejected"}

    result = ensure_kanban_columns("team-5", runner, "aimaestro-teams.sh")
    assert result == {"success": False, "error": "boom: SET rejected"}


# ─────────────────────────── summarize_velocity ─────────────────────────────
def test_summarize_velocity_counts_per_column_and_assignee() -> None:
    """summarize_velocity buckets tasks by status (column) and by assigneeAgentId."""
    tasks = [
        {"status": "dev", "assigneeAgentId": "a1"},
        {"status": "dev", "assigneeAgentId": "a2"},
        {"status": "ai_review", "assigneeAgentId": "a1"},
        {"status": "testing"},  # unassigned
    ]
    summary = summarize_velocity(tasks)
    assert summary["total"] == 4
    assert summary["per_column"] == {"dev": 2, "ai_review": 1, "testing": 1}
    assert summary["per_assignee"] == {"a1": 2, "a2": 1, "unassigned": 1}


def test_summarize_velocity_empty_list() -> None:
    """An empty task list yields zero totals and empty buckets."""
    assert summarize_velocity([]) == {"total": 0, "per_column": {}, "per_assignee": {}}


def test_summarize_velocity_skips_malformed_and_blank_status() -> None:
    """Non-dict entries and blank/missing statuses are skipped without crashing."""
    tasks = [
        {"status": "dev", "assigneeAgentId": "a1"},
        "not-a-dict",
        {"status": "", "assigneeAgentId": "a2"},  # blank status not counted as a column
        {"assigneeAgentId": "a3"},  # no status
    ]
    summary = summarize_velocity(tasks)  # type: ignore[arg-type]
    assert summary["per_column"] == {"dev": 1}
    # a2 and a3 still contribute to assignee distribution even with no/blank status.
    assert summary["per_assignee"] == {"a1": 1, "a2": 1, "a3": 1}
