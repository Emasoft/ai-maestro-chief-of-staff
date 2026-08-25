#!/usr/bin/env python3
"""AMCOS Kanban column governance + velocity (COS#11 / #26 server-half).

The CHIEF-OF-STAFF owns the column-ID SET a team's board must carry — that set
is exactly the TRDD-v2 `column:` enum. The AI Maestro server owns the column
PRESENTATION (label/color/icon) via its `DEFAULT_KANBAN_COLUMNS`. This module
enforces that layer boundary:

  - `KANBAN_BOARD_COLUMN_IDS` is COS's single source of truth for the set
    (14 lifecycle stages + 3 orthogonal exception states).
  - `ensure_kanban_columns()` (design (c) "verify-and-correct") reads a team's
    live column config, compares the returned id SET to the canonical set, and
    only `--set`s a fallback config when they DRIFT. The common case — a team
    with no custom config renders the server default, which already matches —
    is a duplication-free no-op.
  - The fallback `DEFAULT_BOARD_COLUMNS` mirrors the server's label/color so
    the rare drift-correct path can satisfy the PUT schema (`color` is
    REQUIRED). It is exercised ONLY on drift, keeping the steady state free of
    a label/color sync burden.

CLI invocation is injected (a `run_cli` callable + the teams-CLI name) so this
module reuses `amcos_team_registry._run_cli` (the one CLI helper) without a
circular import, and so the pure set/shape logic is testable with zero server.
"""

from __future__ import annotations

import json
from collections import Counter
from typing import Any, Callable

# COS's source of truth for the BOARD column-ID SET == the 3-pillars 3.0.0
# 22-column board (spec `@spec:kanban-columns v2`, 3P-KAN-01/04, USER-ratified
# 2026-08-23): 19 lifecycle stages, then 3 orthogonal exception states. The 5
# BRACKET values (proposal, planned, refused, completed, cancelled) are legal
# `column:` values but sit OUTSIDE the board (3P-KAN-20), so they do not appear
# here. Order is the canonical lifecycle order; the assertion in
# ensure_kanban_columns compares as a SET (a team may legitimately reorder),
# but the order documents the pipeline.
KANBAN_BOARD_COLUMN_IDS: list[str] = [
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

# The 5 bracket values legal in `column:` but never board columns (3P-KAN-20).
BRACKET_COLUMN_VALUES: frozenset[str] = frozenset(
    {"proposal", "planned", "refused", "completed", "cancelled"}
)

# Fallback column config used ONLY on the drift-correct path. The PUT Zod schema
# (ai-maestro/app/api/teams/[id]/kanban-config/route.ts) makes `color` REQUIRED,
# so every entry MUST carry id+label+color. label/color/icon are MIRRORED from
# the server's DEFAULT_KANBAN_COLUMNS — that is the server's presentation SoT,
# duplicated here only so the rare correction can pass validation.
#
# Keep in sync with ai-maestro types/team.ts DEFAULT_KANBAN_COLUMNS.
DEFAULT_BOARD_COLUMNS: list[dict[str, str]] = [
    {"id": "backburner", "label": "Backburner", "color": "bg-gray-500", "icon": "Archive"},
    {"id": "approval", "label": "Approval", "color": "bg-fuchsia-400", "icon": "ShieldCheck"},
    {"id": "design", "label": "Design", "color": "bg-indigo-400", "icon": "PenTool"},
    {"id": "design_ai_review", "label": "Design AI Review", "color": "bg-violet-400", "icon": "Bot"},
    {"id": "design_human_review", "label": "Design Human Review", "color": "bg-rose-400", "icon": "UserCheck"},
    {"id": "todo", "label": "To Do", "color": "bg-gray-400", "icon": "Circle"},
    {"id": "verify_assumptions", "label": "Verify Assumptions", "color": "bg-sky-400", "icon": "BadgeCheck"},
    {"id": "plan", "label": "Plan", "color": "bg-cyan-500", "icon": "ListTree"},
    {"id": "dispatch", "label": "Dispatch", "color": "bg-cyan-400", "icon": "Send"},
    {"id": "dev", "label": "Dev", "color": "bg-blue-400", "icon": "Code"},
    {"id": "testing", "label": "Testing", "color": "bg-amber-400", "icon": "FlaskConical"},
    {"id": "ai_review", "label": "AI Review", "color": "bg-purple-400", "icon": "Bot"},
    {"id": "human_review", "label": "Human Review", "color": "bg-pink-400", "icon": "UserCheck"},
    {"id": "complete", "label": "Complete", "color": "bg-emerald-400", "icon": "CheckCircle2"},
    {"id": "publish", "label": "Publish", "color": "bg-teal-400", "icon": "UploadCloud"},
    {"id": "published", "label": "Published", "color": "bg-green-500", "icon": "PackageCheck"},
    {"id": "deploy", "label": "Deploy", "color": "bg-orange-400", "icon": "Rocket"},
    {"id": "live", "label": "Live", "color": "bg-lime-500", "icon": "Radio"},
    {"id": "live_auditing", "label": "Live Auditing", "color": "bg-yellow-400", "icon": "Activity"},
    {"id": "blocked", "label": "Blocked", "color": "bg-red-500", "icon": "Ban"},
    {"id": "failed", "label": "Failed", "color": "bg-rose-600", "icon": "XCircle"},
    {"id": "superseded", "label": "Superseded", "color": "bg-slate-500", "icon": "Replace"},
]


def _extract_column_ids(get_data: Any) -> list[str]:
    """Pull the column id list out of a `kanban-config --get` payload.

    The GET handler returns `{columns: [{id,label,color,...}, ...]}` (verified:
    ai-maestro/app/api/teams/[id]/kanban-config/route.ts → getKanbanConfig).
    Returns the ids in order; an empty/absent/malformed `columns` yields [] so
    the caller treats it as drift (and corrects), never as a false match.
    """
    if not isinstance(get_data, dict):
        return []
    columns = get_data.get("columns")
    if not isinstance(columns, list):
        return []
    return [c["id"] for c in columns if isinstance(c, dict) and isinstance(c.get("id"), str)]


def ensure_kanban_columns(
    team_id: str,
    run_cli: Callable[[list[str], str], dict[str, Any]],
    teams_cli: str,
) -> dict[str, Any]:
    """Ensure team `team_id`'s board carries the canonical 14-stage column set.

    Design (c) verify-and-correct:
      1. `kanban-config <team_id> --get` and read the returned column-id SET.
      2. If it equals KANBAN_BOARD_COLUMN_IDS as a SET → no-op ("columns OK").
      3. Otherwise (drift / empty) → `--set` DEFAULT_BOARD_COLUMNS to correct.

    Fail-fast: a non-zero exit on EITHER CLI call propagates as
    {"success": False, "error": ...} — never silently swallowed. Idempotent:
    on a board that already matches (the common case, since the server default
    already matches the canonical set) it performs the GET and returns without
    a PUT, so re-running it is safe and cheap.

    `run_cli`/`teams_cli` are injected so this reuses amcos_team_registry's one
    CLI helper without a circular import. Returns:
      - {"success": True, "action": "ok", ...}   — already correct, no PUT
      - {"success": True, "action": "corrected", ...} — drift fixed via --set
      - {"success": False, "error": ...}         — a CLI call failed
    """
    get_result = run_cli(
        [teams_cli, "kanban-config", team_id, "--get"],
        f"kanban-config --get for team '{team_id}'",
    )
    if not get_result.get("success"):
        # Fail-fast — do not attempt a blind --set on an unknown current state.
        return get_result

    current_ids = _extract_column_ids(get_result.get("data"))
    if set(current_ids) == set(KANBAN_BOARD_COLUMN_IDS):
        # Common case: the team already renders the canonical set (server
        # default or an equivalent custom config). No duplication, no PUT.
        return {
            "success": True,
            "action": "ok",
            "team_id": team_id,
            "message": "columns OK",
        }

    # Drift (or empty/unparseable) — correct it with the mirrored fallback.
    # The CLI takes the columns JSON ARRAY and wraps it into {columns: ...}.
    columns_json = json.dumps(DEFAULT_BOARD_COLUMNS, separators=(",", ":"))
    set_result = run_cli(
        [teams_cli, "kanban-config", team_id, "--set", columns_json],
        f"kanban-config --set for team '{team_id}'",
    )
    if not set_result.get("success"):
        return set_result
    return {
        "success": True,
        "action": "corrected",
        "team_id": team_id,
        "message": (
            f"kanban columns drifted (had {sorted(set(current_ids))}); "
            "set to the canonical 14-stage set"
        ),
    }


def summarize_velocity(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Pure reducer: counts of tasks per column and per assignee.

    Input is the task list from `amp-kanban-list` — the `/api/teams/<id>/tasks`
    payload's `tasks` array, where each task has `status` (the column id) and an
    optional `assigneeAgentId` (verified: ai-maestro types/task.ts Task). An
    unassigned task is bucketed under "unassigned". No server access — this is
    the testable core of the COS#11 velocity/distribution read (parts 2-4).
    """
    per_column: Counter[str] = Counter()
    per_assignee: Counter[str] = Counter()
    for task in tasks:
        if not isinstance(task, dict):
            continue
        status = task.get("status")
        if isinstance(status, str) and status:
            per_column[status] += 1
        assignee = task.get("assigneeAgentId")
        per_assignee[assignee if isinstance(assignee, str) and assignee else "unassigned"] += 1
    return {
        "total": sum(per_column.values()),
        "per_column": dict(per_column),
        "per_assignee": dict(per_assignee),
    }


def kanban_velocity(
    team_id: str,
    run_cli: Callable[[list[str], str], dict[str, Any]],
    amp_kanban_list_cli: str,
) -> dict[str, Any]:
    """Read-only velocity/distribution over the team board (COS#11 parts 2-4).

    Lists the team's tasks via `amp-kanban-list --team <team_id>` and reduces
    them to per-column / per-assignee counts via summarize_velocity. Fail-fast
    on a CLI error. Returns {"success": True, **summary} or the CLI error dict.

    The CLI emits the `/api/teams/<id>/tasks` JSON: `{tasks: [...]}` (verified:
    ai-maestro scripts/amp-kanban-list.sh → app/api/teams/[id]/tasks/route.ts).
    A bare array is tolerated too in case the wire shape ever flattens.
    """
    result = run_cli(
        [amp_kanban_list_cli, "--team", team_id],
        f"amp-kanban-list for team '{team_id}'",
    )
    if not result.get("success"):
        return result
    data = result.get("data")
    if isinstance(data, dict):
        tasks = data.get("tasks", [])
    elif isinstance(data, list):
        tasks = data
    else:
        tasks = []
    summary = summarize_velocity(tasks if isinstance(tasks, list) else [])
    return {"success": True, "team_id": team_id, **summary}
