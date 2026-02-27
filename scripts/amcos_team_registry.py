#!/usr/bin/env python3
"""
AMCOS Team Registry Manager

Manages team registries via the AI Maestro REST API.
Creates, updates, and queries teams and their agent memberships.

Usage:
    python amcos_team_registry.py create --team <name> --repo <url> [--project-board <url>]
    python amcos_team_registry.py add-agent --team <name> --agent-name <name> --role <role> --plugin <plugin> --host <host>
    python amcos_team_registry.py remove-agent --team <name> --agent-name <name>
    python amcos_team_registry.py update-status --team <name> --agent-name <name> --status <status>
    python amcos_team_registry.py list [--team <name>]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any

import requests


# API base URL from environment, default to localhost
API_BASE = os.environ.get("AIMAESTRO_API", "http://localhost:23000")


# Role constraints for team composition validation.
# All worker roles map to governance role "member".
class RoleConstraint:
    """Role constraint data."""

    def __init__(self, min_count: int, max_count: int, plugin: str, governance_role: str = "member"):
        self.min = min_count
        self.max = max_count
        self.plugin = plugin
        # Governance role used when registering the agent with the API
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


def _api_url(path: str) -> str:
    """Build full API URL from a relative path."""
    return f"{API_BASE}{path}"


def _handle_response(resp: requests.Response, context: str) -> dict[str, Any]:
    """Check HTTP response and return parsed JSON, or raise on error."""
    if not resp.ok:
        # Try to extract error message from response body
        try:
            body = resp.json()
            detail = body.get("error") or body.get("detail") or body.get("message") or json.dumps(body)
        except Exception:
            detail = resp.text or resp.reason
        raise RuntimeError(f"{context}: HTTP {resp.status_code} - {detail}")
    # Some endpoints may return empty body on success (e.g. DELETE 204)
    if resp.status_code == 204 or not resp.content:
        return {}
    return resp.json()


def validate_team_name(name: str) -> tuple[bool, str]:
    """Validate team name format: <repo>-<type>-team."""
    if not name.endswith("-team"):
        return False, "Team name must end with '-team'"

    parts = name.rsplit("-", 2)
    if len(parts) < 3:
        return False, "Team name must be: <repo-name>-<project-type>-team"

    return True, "Valid"


def create_team(team_name: str, repo_url: str, project_board_url: str | None = None) -> dict[str, Any]:
    """Create a new team via the AI Maestro REST API."""
    # Validate team name format locally before hitting the API
    valid, msg = validate_team_name(team_name)
    if not valid:
        raise ValueError(msg)

    payload: dict[str, Any] = {
        "name": team_name,
        "repository": repo_url,
        "created_by": "amcos-chief-of-staff",
    }
    if project_board_url:
        payload["github_project"] = project_board_url

    resp = requests.post(_api_url("/api/teams"), json=payload, timeout=30)
    return _handle_response(resp, f"Create team '{team_name}'")


def add_agent(
    team_id: str,
    agent_name: str,
    role: str,
    plugin: str,
    host: str,
    ai_maestro_address: str | None = None,
) -> dict[str, Any]:
    """Add an agent to a team via the AI Maestro REST API."""
    # Validate role locally
    if role not in ROLE_CONSTRAINTS:
        raise ValueError(f"Invalid role: {role}. Valid roles: {list(ROLE_CONSTRAINTS.keys())}")

    # Check plugin matches role
    expected_plugin = ROLE_CONSTRAINTS[role].plugin
    if plugin != expected_plugin:
        raise ValueError(f"Role '{role}' requires plugin '{expected_plugin}', got '{plugin}'")

    # Default AI Maestro address to agent name
    if ai_maestro_address is None:
        ai_maestro_address = agent_name

    payload = {
        "name": agent_name,
        "role": role,
        "governance_role": ROLE_CONSTRAINTS[role].governance_role,
        "plugin": plugin,
        "host": host,
        "ai_maestro_address": ai_maestro_address,
        "status": "active",
    }

    resp = requests.post(_api_url(f"/api/teams/{team_id}/agents"), json=payload, timeout=30)
    return _handle_response(resp, f"Add agent '{agent_name}' to team '{team_id}'")


def remove_agent(team_id: str, agent_id: str) -> dict[str, Any]:
    """Remove an agent from a team via the AI Maestro REST API."""
    resp = requests.delete(_api_url(f"/api/teams/{team_id}/agents/{agent_id}"), timeout=30)
    return _handle_response(resp, f"Remove agent '{agent_id}' from team '{team_id}'")


def update_team(team_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    """Update a team via the AI Maestro REST API."""
    resp = requests.patch(_api_url(f"/api/teams/{team_id}"), json=updates, timeout=30)
    return _handle_response(resp, f"Update team '{team_id}'")


def list_teams() -> dict[str, Any]:
    """List all teams via the AI Maestro REST API."""
    resp = requests.get(_api_url("/api/teams"), timeout=30)
    return _handle_response(resp, "List teams")


def get_team_by_name(team_name: str) -> dict[str, Any] | None:
    """Find a team by name from the API. Returns the team dict or None."""
    data = list_teams()
    teams = data.get("teams", [])
    for team in teams:
        if team.get("name") == team_name:
            return team
    return None


def _resolve_team_id(team_name: str) -> str:
    """Resolve a team name to its API id. Raises if not found."""
    team = get_team_by_name(team_name)
    if team is None:
        raise ValueError(f"Team '{team_name}' not found")
    # The API may use 'id', '_id', or 'name' as identifier
    return str(team.get("id") or team.get("_id") or team["name"])


def _resolve_agent_id(team: dict[str, Any], agent_name: str) -> str:
    """Resolve an agent name to its API id within a team. Raises if not found."""
    agents = team.get("agents", [])
    for agent in agents:
        if agent.get("name") == agent_name:
            return str(agent.get("id") or agent.get("_id") or agent["name"])
    raise ValueError(f"Agent '{agent_name}' not found in team '{team.get('name', '?')}'")


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
    parser = argparse.ArgumentParser(
        description="AMCOS Team Registry Manager (REST API)",
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
    add_parser.add_argument("--address", help="AI Maestro address (default: agent name)")

    # Remove agent command
    remove_parser = subparsers.add_parser("remove-agent", help="Remove agent from team")
    remove_parser.add_argument("--team", required=True, help="Team name")
    remove_parser.add_argument("--agent-name", required=True, help="Agent name to remove")

    # Update status command
    status_parser = subparsers.add_parser("update-status", help="Update agent status")
    status_parser.add_argument("--team", required=True, help="Team name")
    status_parser.add_argument("--agent-name", required=True, help="Agent name")
    status_parser.add_argument("--status", required=True, help="New status")

    # List command
    list_parser = subparsers.add_parser("list", help="List teams and agents")
    list_parser.add_argument("--team", help="Team name (omit to list all teams)")

    args = parser.parse_args()

    try:
        if args.command == "create":
            result = create_team(args.team, args.repo, args.project_board)
            print(f"Created team: {args.team}")
            print(json.dumps(result, indent=2))
            return 0

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
            print(f"Added agent '{args.agent_name}' to team '{args.team}'")
            print(json.dumps(result, indent=2))
            return 0

        elif args.command == "remove-agent":
            team = get_team_by_name(args.team)
            if team is None:
                raise ValueError(f"Team '{args.team}' not found")
            team_id = str(team.get("id") or team.get("_id") or team["name"])
            agent_id = _resolve_agent_id(team, args.agent_name)
            remove_agent(team_id, agent_id)
            print(f"Removed agent '{args.agent_name}' from team '{args.team}'")
            return 0

        elif args.command == "update-status":
            team = get_team_by_name(args.team)
            if team is None:
                raise ValueError(f"Team '{args.team}' not found")
            team_id = str(team.get("id") or team.get("_id") or team["name"])

            valid_statuses = ["active", "hibernated", "offline", "terminated"]
            if args.status not in valid_statuses:
                raise ValueError(f"Invalid status: {args.status}. Valid: {valid_statuses}")

            # Use PATCH on the team to update the agent's status
            agent_id = _resolve_agent_id(team, args.agent_name)
            # Update via the team agents endpoint - PATCH the agent within the team
            resp = requests.patch(
                _api_url(f"/api/teams/{team_id}/agents/{agent_id}"),
                json={"status": args.status, "status_updated_at": get_timestamp()},
                timeout=30,
            )
            _handle_response(resp, f"Update status of '{args.agent_name}'")
            print(f"Updated '{args.agent_name}' status to '{args.status}'")
            return 0

        elif args.command == "list":
            if args.team:
                team = get_team_by_name(args.team)
                if team is None:
                    raise ValueError(f"Team '{args.team}' not found")
                print(format_team_list(team))
            else:
                data = list_teams()
                print(format_all_teams(data))
            return 0

    except requests.ConnectionError:
        print(f"Error: Cannot connect to AI Maestro API at {API_BASE}", file=sys.stderr)
        return 1
    except requests.Timeout:
        print(f"Error: Request to AI Maestro API timed out", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
