#!/usr/bin/env python3
"""
amcos_generate_team_report.py - Generate team assignments report.

Fetches team data from the AI Maestro REST API (GET $AIMAESTRO_API/api/teams)
and generates a report with team summaries, agent assignments, role coverage,
and unassigned roles.

Dependencies: Python 3.8+ stdlib only

Usage:
    amcos_generate_team_report.py [--output FILE] [--format text|json|md]

Exit codes:
    0 - Success
    1 - Error (API unavailable, parse error)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_API_BASE = "http://localhost:23000"

# All roles that should be filled in a complete team
ALL_ROLES = frozenset(
    {
        "architect",
        "orchestrator",
        "integrator",
        "programmer",
    }
)

DEFAULT_FORMAT = "md"
VALID_FORMATS = ("text", "json", "md")


# ---------------------------------------------------------------------------
# API data fetching
# ---------------------------------------------------------------------------


def fetch_teams_from_api(api_base: str) -> list[dict[str, Any]]:
    """Fetch team data from the AI Maestro REST API.

    Calls GET {api_base}/api/teams and returns the list of team objects.

    Args:
        api_base: Base URL of the AI Maestro API (e.g. http://localhost:23000).

    Returns:
        List of team dicts returned by the API.

    Raises:
        SystemExit: If the API is unreachable or returns an unexpected response.
    """
    url = f"{api_base}/api/teams"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        print(
            f"ERROR: Cannot connect to AI Maestro API at {url}: {exc}", file=sys.stderr
        )
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON from API at {url}: {exc}", file=sys.stderr)
        sys.exit(1)

    # API may return a plain list or a wrapper object with a "teams" key
    if isinstance(data, list):
        return data  # type: ignore[return-value]
    if isinstance(data, dict):
        teams = data.get("teams", data.get("data", []))
        if isinstance(teams, list):
            return teams  # type: ignore[return-value]

    print(f"ERROR: Unexpected API response structure from {url}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def aggregate_registries(
    registries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate data from multiple team registries fetched from the API.

    Args:
        registries: List of team dicts returned by the AI Maestro API.

    Returns:
        Aggregated report data dict.
    """
    total_agents = 0
    all_agents: list[dict[str, Any]] = []
    team_summaries: list[dict[str, Any]] = []
    agent_assignments: dict[str, list[str]] = {}  # agent_name -> list of team names
    all_filled_roles: set[str] = set()

    for data in registries:
        team_name = data.get("team_name", data.get("name", "unknown"))
        agents = data.get("agents", data.get("roster", []))
        project = data.get("project", data.get("repository", ""))

        team_roles: set[str] = set()
        team_agent_names: list[str] = []

        for agent in agents:
            agent_name = agent.get("name", agent.get("agent_name", "unknown"))
            role = agent.get("role", "unknown")
            status = agent.get("status", "unknown")

            total_agents += 1
            team_roles.add(role)
            all_filled_roles.add(role)
            team_agent_names.append(agent_name)

            all_agents.append(
                {
                    "name": agent_name,
                    "role": role,
                    "team": team_name,
                    "status": status,
                    "plugin": agent.get("plugin", ""),
                    "host": agent.get("host", ""),
                }
            )

            # Track agent -> teams mapping
            if agent_name not in agent_assignments:
                agent_assignments[agent_name] = []
            agent_assignments[agent_name].append(team_name)

        missing_roles = sorted(ALL_ROLES - team_roles)
        # Use the API-provided team id or name as the identifier
        team_id = data.get("id", data.get("team_id", team_name))

        team_summaries.append(
            {
                "team_name": team_name,
                "team_id": str(team_id),
                "project": project,
                "agent_count": len(agents),
                "agents": team_agent_names,
                "roles_filled": sorted(team_roles),
                "roles_missing": missing_roles,
            }
        )

    unassigned_roles_global = sorted(ALL_ROLES - all_filled_roles)

    return {
        "total_teams": len(registries),
        "total_agents": total_agents,
        "teams": team_summaries,
        "agents": all_agents,
        "agent_assignments": agent_assignments,
        "unassigned_roles_global": unassigned_roles_global,
    }


# ---------------------------------------------------------------------------
# Report formatters
# ---------------------------------------------------------------------------


def format_json(report: dict[str, Any]) -> str:
    """Format report as JSON."""
    output = {
        "success": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "report": report,
    }
    return json.dumps(output, indent=2, default=str)


def format_markdown(report: dict[str, Any]) -> str:
    """Format report as Markdown."""
    lines: list[str] = []
    lines.append("# Team Assignments Report")
    lines.append("")
    lines.append(
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total teams**: {report['total_teams']}")
    lines.append(f"- **Total agents**: {report['total_agents']}")
    if report["unassigned_roles_global"]:
        lines.append(
            f"- **Globally unassigned roles**: {', '.join(report['unassigned_roles_global'])}"
        )
    else:
        lines.append("- **All roles assigned** across at least one team")
    lines.append("")

    # Per-team breakdown
    lines.append("## Per-Team Breakdown")
    lines.append("")

    for team in report["teams"]:
        lines.append(f"### {team['team_name']}")
        lines.append("")
        if team["project"]:
            lines.append(f"- **Project**: {team['project']}")
        lines.append(f"- **Team ID**: `{team['team_id']}`")
        lines.append(f"- **Agent count**: {team['agent_count']}")
        lines.append(
            f"- **Roles filled**: {', '.join(team['roles_filled']) if team['roles_filled'] else 'none'}"
        )
        if team["roles_missing"]:
            lines.append(f"- **Roles missing**: {', '.join(team['roles_missing'])}")
        lines.append(
            f"- **Agents**: {', '.join(team['agents']) if team['agents'] else 'none'}"
        )
        lines.append("")

    # Agent assignment matrix
    lines.append("## Agent Assignment Matrix")
    lines.append("")

    if report["agents"]:
        lines.append("| Agent | Role | Team | Status |")
        lines.append("|-------|------|------|--------|")
        for agent in sorted(
            report["agents"], key=lambda a: (a["team"], a["role"], a["name"])
        ):
            lines.append(
                f"| {agent['name']} | {agent['role']} | {agent['team']} | {agent['status']} |"
            )
        lines.append("")

        # Multi-team agents
        multi_team = {
            name: teams
            for name, teams in report["agent_assignments"].items()
            if len(teams) > 1
        }
        if multi_team:
            lines.append("### Multi-Team Agents")
            lines.append("")
            for name, teams in sorted(multi_team.items()):
                lines.append(f"- **{name}**: {', '.join(teams)}")
            lines.append("")
    else:
        lines.append("No agents found in any team registry.")
        lines.append("")

    # Unassigned roles
    lines.append("## Unassigned Roles")
    lines.append("")

    any_missing = False
    for team in report["teams"]:
        if team["roles_missing"]:
            any_missing = True
            lines.append(
                f"- **{team['team_name']}**: {', '.join(team['roles_missing'])}"
            )

    if not any_missing:
        lines.append("All roles are filled in all teams.")
    lines.append("")

    return "\n".join(lines)


def format_text(report: dict[str, Any]) -> str:
    """Format report as plain text."""
    lines: list[str] = []
    lines.append("TEAM ASSIGNMENTS REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    lines.append(f"Total teams: {report['total_teams']}")
    lines.append(f"Total agents: {report['total_agents']}")
    lines.append("")

    for team in report["teams"]:
        lines.append(f"--- {team['team_name']} ---")
        if team["project"]:
            lines.append(f"  Project: {team['project']}")
        lines.append(f"  Agents ({team['agent_count']}):")
        for agent_name in team["agents"]:
            lines.append(f"    - {agent_name}")
        lines.append(f"  Roles filled: {', '.join(team['roles_filled'])}")
        if team["roles_missing"]:
            lines.append(f"  Roles missing: {', '.join(team['roles_missing'])}")
        lines.append("")

    if report["unassigned_roles_global"]:
        lines.append(
            f"GLOBALLY UNASSIGNED ROLES: {', '.join(report['unassigned_roles_global'])}"
        )
    else:
        lines.append("All roles assigned across at least one team.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error.
    """
    parser = argparse.ArgumentParser(
        description="Generate team assignments report from the AI Maestro REST API"
    )
    parser.add_argument(
        "--api",
        type=str,
        default=None,
        help=f"AI Maestro API base URL (defaults to $AIMAESTRO_API or {DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output file path (defaults to stdout)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=VALID_FORMATS,
        default=DEFAULT_FORMAT,
        help=f"Output format (default: {DEFAULT_FORMAT})",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print progress to stderr",
    )

    args = parser.parse_args()

    # Resolve API base URL: CLI flag > env var > default
    api_base = args.api or os.environ.get("AIMAESTRO_API", DEFAULT_API_BASE)
    api_base = api_base.rstrip("/")

    if args.verbose:
        print(f"Fetching team data from: {api_base}/api/teams", file=sys.stderr)

    # Fetch teams from the REST API (exits on connection error)
    teams = fetch_teams_from_api(api_base)

    if args.verbose:
        print(f"Received {len(teams)} team(s) from API", file=sys.stderr)

    if not teams:
        result = {
            "success": True,
            "warning": "No teams returned by the API",
            "report": {
                "total_teams": 0,
                "total_agents": 0,
                "teams": [],
                "agents": [],
                "agent_assignments": {},
                "unassigned_roles_global": sorted(ALL_ROLES),
            },
        }
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print("No teams returned by the AI Maestro API.")
        return 0

    # Aggregate
    report = aggregate_registries(teams)

    # Format output
    if args.format == "json":
        output_text = format_json(report)
    elif args.format == "md":
        output_text = format_markdown(report)
    else:
        output_text = format_text(report)

    # Write or print
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text + "\n", encoding="utf-8")
        if args.verbose:
            print(f"Wrote report to: {output_path}", file=sys.stderr)
        # Print a brief summary to stdout
        summary = {
            "success": True,
            "total_teams": report["total_teams"],
            "total_agents": report["total_agents"],
            "output_file": str(output_path),
        }
        print(json.dumps(summary, indent=2))
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
