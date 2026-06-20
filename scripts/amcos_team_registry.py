#!/usr/bin/env python3
"""
AMCOS Team Registry Manager

Manages team registries via the immutable AI Maestro CLI layer (#20).
Creates, updates, and queries teams and their agent memberships by calling
the frozen-interface CLIs (aimaestro-teams.sh / aimaestro-agent.sh), which
wrap the server API and resolve auth internally — never the HTTP API directly.

Usage:
    python amcos_team_registry.py create --team <name> --repo <url> [--project-board <url>]
    python amcos_team_registry.py add-agent --team <name> --agent-name <name> --role <role> --plugin <plugin> --host <host>
    python amcos_team_registry.py remove-agent --team <name> --agent-name <name>
    python amcos_team_registry.py update-status --team <name> --agent-name <name> --status <status>
    python amcos_team_registry.py list [--team <name>]
    python amcos_team_registry.py kanban-velocity --team <name>
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from amcos_kanban import ensure_kanban_columns, kanban_velocity
from amcos_output_utils import AmcosOutput

# Frozen-CLI names, env-overridable exactly like amcos_notify_agent.py (#20).
# The CLIs wrap the teams/agents API and resolve auth internally; this script
# shells out to them and never touches the HTTP API.
TEAMS_CLI = os.environ.get("AIMAESTRO_TEAMS_CLI", "aimaestro-teams.sh")
AGENT_CLI = os.environ.get("AIMAESTRO_AGENT_CLI", "aimaestro-agent.sh")
AMP_KANBAN_LIST_CLI = os.environ.get("AMP_KANBAN_LIST_CLI", "amp-kanban-list.sh")


# Role constraints for team composition validation.
# All worker roles map to governance role "member".
class RoleConstraint:
    """Role constraint data."""

    def __init__(
        self,
        min_count: int,
        max_count: int,
        plugin: str,
        governance_role: str = "member",
    ):
        self.min = min_count
        self.max = max_count
        self.plugin = plugin
        # Governance role used when registering the agent with the CLI
        self.governance_role = governance_role


ROLE_CONSTRAINTS: dict[str, RoleConstraint] = {
    "orchestrator": RoleConstraint(1, 1, "ai-maestro-orchestrator-agent", "member"),
    "architect": RoleConstraint(1, 1, "ai-maestro-architect-agent", "member"),
    "integrator": RoleConstraint(0, 10, "ai-maestro-integrator-agent", "member"),
    "programmer": RoleConstraint(1, 20, "ai-maestro-programmer-agent", "member"),
}


def get_timestamp() -> str:
    """Get current ISO8601 timestamp."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run_cli(argv: list[str], context: str) -> dict[str, Any]:
    """Run a frozen-CLI command, returning a result dict.

    Preserves the caller contract used throughout this module:
      - success: {"success": True} with parsed JSON under "data" (object/array)
        or the raw text under "raw" (when stdout is non-JSON but non-empty);
      - failure: {"success": False, "error": "<context>: <detail>"}.
    The CLI resolves auth internally and prints "Error: ..." to stderr on
    non-zero exit (see aimaestro-teams.sh / aimaestro-agent.sh).
    """
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    except (subprocess.SubprocessError, OSError) as exc:
        return {"success": False, "error": f"{context}: CLI invocation failed: {exc}"}
    if result.returncode != 0:
        return {
            "success": False,
            "error": f"{context}: {result.stderr.strip() or 'non-zero exit'}",
        }
    out = result.stdout.strip()
    if not out:
        return {"success": True}
    if out.startswith(("{", "[")):
        try:
            return {"success": True, "data": json.loads(out)}
        except json.JSONDecodeError:
            return {"success": True, "raw": out}
    return {"success": True, "raw": out}


def _parse_repo_url(repo_url: str) -> tuple[str, str]:
    """Decompose a GitHub repo URL into (owner, repo).

    Accepts https://github.com/<owner>/<repo> or the same with a trailing
    '.git'. Strips scheme/host and the optional '.git' suffix. Raises
    ValueError when the URL does not contain an <owner>/<repo> pair.
    """
    # Drop scheme (anything up to '://') if present, then drop the host segment.
    path = repo_url.split("://", 1)[-1]
    if "/" in path:
        path = path.split("/", 1)[1]  # strip the host (e.g. github.com)
    path = path.strip("/")
    if path.endswith(".git"):
        path = path[: -len(".git")]
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        raise ValueError(
            f"Cannot parse owner/repo from repository URL: {repo_url!r}"
        )
    return parts[0], parts[1]


def validate_team_name(name: str) -> tuple[bool, str]:
    """Validate team name format: <repo>-<type>-team."""
    if not name.endswith("-team"):
        return False, "Team name must end with '-team'"

    parts = name.rsplit("-", 2)
    if len(parts) < 3:
        return False, "Team name must be: <repo-name>-<project-type>-team"

    return True, "Valid"


def create_team(
    team_name: str, repo_url: str, project_board_url: str | None = None
) -> dict[str, Any]:
    """Create a new team via the immutable CLI (aimaestro-teams.sh create)."""
    # Validate team name format locally before invoking the CLI
    valid, msg = validate_team_name(team_name)
    if not valid:
        raise ValueError(msg)

    owner, repo = _parse_repo_url(repo_url)
    argv = [
        TEAMS_CLI,
        "create",
        "--name",
        team_name,
        "--gh-owner",
        owner,
        "--gh-repo",
        repo,
    ]
    # `created_by` is dropped: the server infers the creator from CLI/AID auth.
    if project_board_url:
        # DECOUPLE-BLOCKED ai-maestro#36: github_project — aimaestro-teams.sh create has no --gh-project flag yet; field dropped until it ships.
        print(
            "Warning: project_board_url given but aimaestro-teams.sh create has "
            "no --gh-project flag (ai-maestro#36) — creating team without it.",
            file=sys.stderr,
        )
    result = _run_cli(argv, f"Create team '{team_name}'")
    if not result.get("success"):
        return result

    # COS#11 / #26: after a successful create, ensure the new board carries the
    # canonical 14-stage column set (the TRDD `column:` enum, which COS owns).
    # design (c) verify-and-correct: this GETs the board and only --sets on
    # drift, so the common case (server default already matches) is a no-op.
    # Fail-fast — propagate any CLI error from the column-ensure as the create
    # result so a half-configured team is never reported as a clean success.
    team_id = _extract_created_team_id(result.get("data"))
    if team_id is None:
        return {
            "success": False,
            "error": (
                f"Create team '{team_name}': succeeded but could not resolve the "
                "new team id from the CLI response to ensure kanban columns "
                f"(got: {result.get('data')!r})"
            ),
        }
    kanban_result = ensure_kanban_columns(team_id, _run_cli, TEAMS_CLI)
    if not kanban_result.get("success"):
        return kanban_result
    result["kanban"] = kanban_result
    return result


def _extract_created_team_id(create_data: Any) -> str | None:
    """Resolve the new team's id from `aimaestro-teams.sh create` output.

    The server returns `{team: {id, ...}, needsChiefOfStaff} ` (verified:
    ai-maestro services/teams-service.ts createTeam → POST /api/teams). Also
    tolerate a bare team object `{id, ...}` in case the wire shape ever
    flattens, mirroring _resolve_team_id's id/_id/name tolerance. Returns the
    id string, or None when it cannot be resolved (caller fails fast).
    """
    if not isinstance(create_data, dict):
        return None
    team = create_data.get("team")
    if not isinstance(team, dict):
        team = create_data  # bare team object fallback
    tid = team.get("id") or team.get("_id")
    return str(tid) if tid else None


def add_agent(
    team_id: str,
    agent_name: str,
    role: str,
    plugin: str,
    host: str,
    ai_maestro_address: str | None = None,
) -> dict[str, Any]:
    """Add an agent to a team via the immutable CLI (aimaestro-agent.sh create).

    Cross-CLI: team membership for a brand-new agent is created through the
    agent CLI's `create` (which accepts --team/--title/--plugin/--label).
    """
    # Validate role locally
    if role not in ROLE_CONSTRAINTS:
        raise ValueError(
            f"Invalid role: {role}. Valid roles: {list(ROLE_CONSTRAINTS.keys())}"
        )

    # Check plugin matches role
    expected_plugin = ROLE_CONSTRAINTS[role].plugin
    if plugin != expected_plugin:
        raise ValueError(
            f"Role '{role}' requires plugin '{expected_plugin}', got '{plugin}'"
        )

    governance_role = ROLE_CONSTRAINTS[role].governance_role

    # DECOUPLE-BLOCKED ai-maestro#36: add-agent — aimaestro-agent.sh create
    # requires a working directory (--dir <path>, hard-required) AND has NO
    # --status flag (verified against agent-commands.sh cmd_create: the only
    # --status is on `list`; create errors "Working directory is required").
    # add_agent()'s signature carries no working-dir, and host/ai_maestro_address
    # are server-inferred (dropped) — so the registry cannot synthesize a valid
    # `agent create` invocation here without a --dir value it does not have.
    # Pending MANAGER design call (same residual class as github_project /
    # update-status): either agent-create gains a registry-mode that defaults
    # --dir, or the registry grows a working-dir parameter. Fail-fast rather
    # than emit a CLI call the frozen interface would reject.
    _ = (governance_role, host, ai_maestro_address)  # referenced; intentionally unused until the verb ships
    return {
        "success": False,
        "error": (
            f"add-agent '{agent_name}' to team '{team_id}' DECOUPLE-BLOCKED ai-maestro#36: "
            "aimaestro-agent.sh create requires --dir (no working-dir in "
            "add_agent signature) and exposes no --status flag — no clean "
            "registry-side mapping. Pending MANAGER design call."
        ),
    }


def remove_agent(team_id: str, agent_id: str) -> dict[str, Any]:
    """Remove an agent from a team via the immutable CLI (aimaestro-teams.sh remove-agent)."""
    argv = [TEAMS_CLI, "remove-agent", team_id, agent_id]
    return _run_cli(argv, f"Remove agent '{agent_id}' from team '{team_id}'")


def update_team(team_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    """Update a team via the immutable CLI (aimaestro-teams.sh update).

    Maps known `updates` keys to verified flags; unknown keys are skipped
    with a stderr warning (never crash).
    """
    # Verified aimaestro-teams.sh update flag surface.
    key_to_flag = {
        "name": "--name",
        "description": "--description",
        "agents": "--agents",
        "orchestrator": "--orchestrator",
    }
    argv = [TEAMS_CLI, "update", team_id]
    for key, value in updates.items():
        flag = key_to_flag.get(key)
        if flag is None:
            print(
                f"Warning: update_team: unknown key '{key}' has no "
                "aimaestro-teams.sh update flag — skipped.",
                file=sys.stderr,
            )
            continue
        argv.extend([flag, str(value)])
    return _run_cli(argv, f"Update team '{team_id}'")


def list_teams() -> dict[str, Any]:
    """List all teams via the immutable CLI (aimaestro-teams.sh list).

    Returns {"success": True, "teams": [...]} so callers keep doing
    data.get("teams", []); on failure returns {"success": False, "error": ...}.
    The CLI may return a plain array or a {"teams": [...]} wrapper.
    """
    result = _run_cli([TEAMS_CLI, "list"], "List teams")
    if not result.get("success"):
        return result
    data = result.get("data")
    if isinstance(data, list):
        teams = data
    elif isinstance(data, dict):
        teams = data.get("teams", [])
    else:
        teams = []
    return {"success": True, "teams": teams}


def get_team_by_name(team_name: str) -> dict[str, Any] | None:
    """Find a team by name from the CLI. Returns the team dict or None."""
    data = list_teams()
    teams = data.get("teams", [])
    for team in teams:
        if team.get("name") == team_name:
            return team
    return None


def _resolve_team_id(team_name: str) -> str:
    """Resolve a team name to its id. Raises if not found."""
    team = get_team_by_name(team_name)
    if team is None:
        raise ValueError(f"Team '{team_name}' not found")
    # The registry may use 'id', '_id', or 'name' as identifier
    return str(team.get("id") or team.get("_id") or team["name"])


def _resolve_agent_id(team: dict[str, Any], agent_name: str) -> str:
    """Resolve an agent name to its id within a team. Raises if not found."""
    agents = team.get("agents", [])
    for agent in agents:
        if agent.get("name") == agent_name:
            return str(agent.get("id") or agent.get("_id") or agent["name"])
    raise ValueError(
        f"Agent '{agent_name}' not found in team '{team.get('name', '?')}'"
    )


def format_team_list(team: dict[str, Any]) -> str:
    """Format a single team's agents as a readable list."""
    lines = []
    team_name = team.get("name", "unknown")
    lines.append(f"Team: {team_name}")
    lines.append(f"Repository: {team.get('repository', 'N/A')}")
    lines.append("")
    lines.append("Agents:")
    lines.append("-" * 80)
    lines.append(f"{'Name':<25} {'Role':<15} {'Host':<20} {'Status':<10}")
    lines.append("-" * 80)

    for agent in team.get("agents", []):
        lines.append(
            f"{agent.get('name', '?'):<25} {agent.get('role', '?'):<15} "
            f"{agent.get('host', '?'):<20} {agent.get('status', '?'):<10}"
        )

    lines.append("")
    lines.append(f"Last Updated: {team.get('contacts_last_updated', 'N/A')}")
    return "\n".join(lines)


def format_all_teams(data: dict[str, Any]) -> str:
    """Format all teams as a readable summary."""
    teams = data.get("teams", [])
    if not teams:
        return "No teams registered."

    lines = []
    for team in teams:
        lines.append(format_team_list(team))
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    out = AmcosOutput("amcos_team_registry")
    parser = argparse.ArgumentParser(
        description="AMCOS Team Registry Manager (immutable CLI layer)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Create a new team
    python amcos_team_registry.py create --team svgbbox-library-team \\
        --repo https://github.com/Emasoft/svgbbox \\
        --project-board https://github.com/orgs/Emasoft/projects/12

    # Add an agent
    python amcos_team_registry.py add-agent --team svgbbox-library-team \\
        --agent-name svgbbox-programmer-001 --role programmer \\
        --plugin ai-maestro-programmer-agent --host macbook-dev-01

    # Remove an agent
    python amcos_team_registry.py remove-agent --team svgbbox-library-team \\
        --agent-name svgbbox-programmer-001

    # Update agent status
    python amcos_team_registry.py update-status --team svgbbox-library-team \\
        --agent-name svgbbox-programmer-001 --status hibernated

    # List all teams
    python amcos_team_registry.py list

    # List a specific team
    python amcos_team_registry.py list --team svgbbox-library-team
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new team")
    create_parser.add_argument("--team", required=True, help="Team name")
    create_parser.add_argument("--repo", required=True, help="GitHub repository URL")
    create_parser.add_argument("--project-board", help="GitHub Projects board URL")

    # Add agent command
    add_parser = subparsers.add_parser("add-agent", help="Add agent to team")
    add_parser.add_argument("--team", required=True, help="Team name")
    add_parser.add_argument("--agent-name", required=True, help="Agent name")
    add_parser.add_argument("--role", required=True, help="Agent role")
    add_parser.add_argument("--plugin", required=True, help="Plugin name")
    add_parser.add_argument("--host", required=True, help="Host machine")
    add_parser.add_argument(
        "--address", help="AI Maestro address (default: agent name)"
    )

    # Remove agent command
    remove_parser = subparsers.add_parser("remove-agent", help="Remove agent from team")
    remove_parser.add_argument("--team", required=True, help="Team name")
    remove_parser.add_argument(
        "--agent-name", required=True, help="Agent name to remove"
    )

    # Update status command
    status_parser = subparsers.add_parser("update-status", help="Update agent status")
    status_parser.add_argument("--team", required=True, help="Team name")
    status_parser.add_argument("--agent-name", required=True, help="Agent name")
    status_parser.add_argument("--status", required=True, help="New status")

    # List command
    list_parser = subparsers.add_parser("list", help="List teams and agents")
    list_parser.add_argument("--team", help="Team name (omit to list all teams)")

    # Kanban velocity command (COS#11 parts 2-4): read-only per-column /
    # per-assignee task distribution over the team board.
    velocity_parser = subparsers.add_parser(
        "kanban-velocity", help="Per-column / per-assignee task counts for a team"
    )
    velocity_parser.add_argument("--team", required=True, help="Team name")

    args = parser.parse_args()

    try:
        if args.command == "create":
            result = create_team(args.team, args.repo, args.project_board)
            out.log(f"Created team: {args.team}")
            out.log_json(result, label="create")
            print(json.dumps(result, separators=(",", ":")))
            out.summary("DONE", f"Team '{args.team}' created")
            out.close()
            return 0 if result.get("success") else 1

        elif args.command == "add-agent":
            team_id = _resolve_team_id(args.team)
            result = add_agent(
                team_id,
                args.agent_name,
                args.role,
                args.plugin,
                args.host,
                args.address,
            )
            out.log(f"Add agent '{args.agent_name}' to team '{args.team}'")
            out.log_json(result, label="add-agent")
            print(json.dumps(result, separators=(",", ":")))
            if result.get("success"):
                out.summary("DONE", f"Agent '{args.agent_name}' added to '{args.team}'")
                out.close()
                return 0
            out.summary("FAILED", result.get("error", "add-agent failed"))
            out.close()
            return 1

        elif args.command == "remove-agent":
            team = get_team_by_name(args.team)
            if team is None:
                raise ValueError(f"Team '{args.team}' not found")
            team_id = str(team.get("id") or team.get("_id") or team["name"])
            agent_id = _resolve_agent_id(team, args.agent_name)
            result = remove_agent(team_id, agent_id)
            out.log(f"Remove agent '{args.agent_name}' from team '{args.team}'")
            out.log_json(result, label="remove-agent")
            print(json.dumps(result, separators=(",", ":")))
            if result.get("success"):
                out.summary(
                    "DONE", f"Agent '{args.agent_name}' removed from '{args.team}'"
                )
                out.close()
                return 0
            out.summary("FAILED", result.get("error", "remove-agent failed"))
            out.close()
            return 1

        elif args.command == "update-status":
            team = get_team_by_name(args.team)
            if team is None:
                raise ValueError(f"Team '{args.team}' not found")

            valid_statuses = ["active", "hibernated", "offline", "terminated"]
            if args.status not in valid_statuses:
                raise ValueError(
                    f"Invalid status: {args.status}. Valid: {valid_statuses}"
                )

            # DECOUPLE-BLOCKED ai-maestro#36: update-status — no generic agent-status-set verb (agent update=tags/task/model only; hibernate/wake/restart are actions, not label-sets). Pending MANAGER design call (same class as approval_manager.sync_local_to_api).
            result = {
                "success": False,
                "error": (
                    "update-status DECOUPLE-BLOCKED ai-maestro#36: no generic "
                    "agent-status-set verb in the frozen CLI (aimaestro-agent.sh "
                    "update sets tags/task/model only; hibernate/wake/restart are "
                    "lifecycle ACTIONS, not registry status-label sets). Pending "
                    "MANAGER design call."
                ),
            }
            out.log(f"update-status '{args.agent_name}' -> '{args.status}'")
            out.log_json(result, label="update-status")
            print(json.dumps(result, separators=(",", ":")))
            out.summary("FAILED", result["error"])
            out.close()
            return 1

        elif args.command == "list":
            if args.team:
                team = get_team_by_name(args.team)
                if team is None:
                    raise ValueError(f"Team '{args.team}' not found")
                out.log(format_team_list(team))
            else:
                data = list_teams()
                if not data.get("success"):
                    raise RuntimeError(data.get("error", "List teams failed"))
                out.log(format_all_teams(data))
            out.summary("DONE", "Team listing complete")
            out.close()
            return 0

        elif args.command == "kanban-velocity":
            team_id = _resolve_team_id(args.team)
            result = kanban_velocity(team_id, _run_cli, AMP_KANBAN_LIST_CLI)
            out.log(f"kanban-velocity for team '{args.team}'")
            out.log_json(result, label="kanban-velocity")
            print(json.dumps(result, separators=(",", ":")))
            if result.get("success"):
                out.summary("DONE", f"velocity for '{args.team}': {result.get('total', 0)} tasks")
                out.close()
                return 0
            out.summary("FAILED", result.get("error", "kanban-velocity failed"))
            out.close()
            return 1

    except Exception as e:
        out.log(f"Error: {e}")
        out.close()
        return 1

    out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
