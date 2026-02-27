#!/usr/bin/env python3
"""
amcos_generate_team_report.py - Generate team assignments report.

Aggregates data across all .ai-maestro/team-registry.json files found in the
project tree and generates a report with team summaries, agent assignments,
role coverage, and unassigned roles.

Dependencies: Python 3.8+ stdlib only

Usage:
    amcos_generate_team_report.py [--project-root PATH] [--output FILE]
        [--format text|json|md]

Exit codes:
    0 - Success
    1 - Error (directory not found, parse error)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REGISTRY_FILENAME = "team-registry.json"
REGISTRY_DIR = ".ai-maestro"

# All roles that should be filled in a complete team
ALL_ROLES = frozenset({
    "architect",
    "orchestrator",
    "integrator",
    "programmer",
})

DEFAULT_FORMAT = "md"
VALID_FORMATS = ("text", "json", "md")


# ---------------------------------------------------------------------------
# Registry discovery and parsing
# ---------------------------------------------------------------------------


def find_registries(project_root: Path) -> list[Path]:
    """Find all team-registry.json files under the project root.

    Searches for .ai-maestro/team-registry.json in the project root and all
    immediate subdirectories (one level deep).

    Args:
        project_root: Root directory to search.

    Returns:
        List of paths to found registry files.
    """
    found: list[Path] = []

    # Check project root itself
    root_registry = project_root / REGISTRY_DIR / REGISTRY_FILENAME
    if root_registry.exists():
        found.append(root_registry)

    # Check immediate subdirectories
    if project_root.is_dir():
        for child in sorted(project_root.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("."):
                continue
            candidate = child / REGISTRY_DIR / REGISTRY_FILENAME
            if candidate.exists():
                found.append(candidate)

    return found


def parse_registry(path: Path) -> dict[str, Any] | None:
    """Parse a team-registry.json file.

    Args:
        path: Path to the registry file.

    Returns:
        Parsed registry dict, or None on error.
    """
    try:
        content = path.read_text(encoding="utf-8")
        return json.loads(content)  # type: ignore[no-any-return]
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def aggregate_registries(
    registries: list[tuple[Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Aggregate data from multiple team registries.

    Args:
        registries: List of (path, parsed_data) tuples.

    Returns:
        Aggregated report data dict.
    """
    total_agents = 0
    all_agents: list[dict[str, Any]] = []
    team_summaries: list[dict[str, Any]] = []
    agent_assignments: dict[str, list[str]] = {}  # agent_name -> list of team names
    all_filled_roles: set[str] = set()

    for path, data in registries:
        team_name = data.get("team_name", data.get("name", path.parent.parent.name))
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

            all_agents.append({
                "name": agent_name,
                "role": role,
                "team": team_name,
                "status": status,
                "plugin": agent.get("plugin", ""),
                "host": agent.get("host", ""),
            })

            # Track agent -> teams mapping
            if agent_name not in agent_assignments:
                agent_assignments[agent_name] = []
            agent_assignments[agent_name].append(team_name)

        missing_roles = sorted(ALL_ROLES - team_roles)

        team_summaries.append({
            "team_name": team_name,
            "registry_path": str(path),
            "project": project,
            "agent_count": len(agents),
            "agents": team_agent_names,
            "roles_filled": sorted(team_roles),
            "roles_missing": missing_roles,
        })

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
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total teams**: {report['total_teams']}")
    lines.append(f"- **Total agents**: {report['total_agents']}")
    if report["unassigned_roles_global"]:
        lines.append(f"- **Globally unassigned roles**: {', '.join(report['unassigned_roles_global'])}")
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
        lines.append(f"- **Registry**: `{team['registry_path']}`")
        lines.append(f"- **Agent count**: {team['agent_count']}")
        lines.append(f"- **Roles filled**: {', '.join(team['roles_filled']) if team['roles_filled'] else 'none'}")
        if team["roles_missing"]:
            lines.append(f"- **Roles missing**: {', '.join(team['roles_missing'])}")
        lines.append(f"- **Agents**: {', '.join(team['agents']) if team['agents'] else 'none'}")
        lines.append("")

    # Agent assignment matrix
    lines.append("## Agent Assignment Matrix")
    lines.append("")

    if report["agents"]:
        lines.append("| Agent | Role | Team | Status |")
        lines.append("|-------|------|------|--------|")
        for agent in sorted(report["agents"], key=lambda a: (a["team"], a["role"], a["name"])):
            lines.append(
                f"| {agent['name']} | {agent['role']} | {agent['team']} | {agent['status']} |"
            )
        lines.append("")

        # Multi-team agents
        multi_team = {name: teams for name, teams in report["agent_assignments"].items() if len(teams) > 1}
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
            lines.append(f"- **{team['team_name']}**: {', '.join(team['roles_missing'])}")

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
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
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
        lines.append(f"GLOBALLY UNASSIGNED ROLES: {', '.join(report['unassigned_roles_global'])}")
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
        description="Generate team assignments report from all team registries"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=None,
        help="Project root directory to search (defaults to current directory)",
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

    project_root = Path(args.project_root) if args.project_root else Path.cwd()
    if not project_root.is_dir():
        result = {"success": False, "error": f"Not a directory: {project_root}"}
        print(json.dumps(result, indent=2))
        return 1

    if args.verbose:
        print(f"Searching for team registries in: {project_root}", file=sys.stderr)

    # Find registries
    registry_paths = find_registries(project_root)

    if args.verbose:
        print(f"Found {len(registry_paths)} registry file(s)", file=sys.stderr)

    if not registry_paths:
        result = {
            "success": True,
            "warning": "No team-registry.json files found",
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
            print("No team-registry.json files found under the project root.")
        return 0

    # Parse registries
    registries: list[tuple[Path, dict[str, Any]]] = []
    for path in registry_paths:
        if args.verbose:
            print(f"  Parsing: {path}", file=sys.stderr)
        data = parse_registry(path)
        if data is None:
            print(f"WARNING: Failed to parse {path}", file=sys.stderr)
            continue
        registries.append((path, data))

    if not registries:
        result_err = {"success": False, "error": "All registry files failed to parse"}
        print(json.dumps(result_err, indent=2))
        return 1

    # Aggregate
    report = aggregate_registries(registries)

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
