#!/usr/bin/env python3
"""
amcos_session_start.py - Initialize Chief of Staff state on session start.

SessionStart hook that loads the Chief of Staff state file and outputs a system
message summarizing the staff status to help Claude resume work seamlessly.

State file: .claude/chief-of-staff-state.local.md

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from SessionStart hook event.
    Outputs system message to stdout with staff status summary.
    Creates state file if not exists.

Exit codes:
    0 - Success (state loaded or created)
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from amcos_output_utils import AmcosOutput


def get_state_file(cwd: str) -> Path:
    """Get the Chief of Staff state file path.

    Args:
        cwd: Current working directory

    Returns:
        Path to .claude/chief-of-staff-state.local.md
    """
    return Path(cwd) / ".claude" / "chief-of-staff-state.local.md"


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def create_default_state() -> str:
    """Create default state file content.

    Returns:
        Default state file content as markdown
    """
    timestamp = get_timestamp()
    return f"""# Chief of Staff State

**Last Updated**: {timestamp}
**Session Count**: 1

## Active Agents

| Agent | Role | Status | Last Heartbeat |
|-------|------|--------|----------------|
| _No agents registered_ | - | - | - |

## Pending Tasks

- No pending tasks

## Resource Alerts

- None

## Session History

### {timestamp}
- Session started
- State file initialized
"""


def read_file_safely(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def write_file_safely(path: Path, content: str) -> bool:
    """Write file content safely with error handling."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except OSError as e:
        print(f"ERROR: Cannot write file {path}: {e}", file=sys.stderr)
        return False


def parse_active_agents(content: str) -> list[dict[str, str]]:
    """Parse active agents from state file.

    Args:
        content: State file content

    Returns:
        List of agent dictionaries with name, role, status, heartbeat
    """
    agents: list[dict[str, str]] = []

    # Find the Active Agents table
    in_table = False
    header_passed = False

    for line in content.split("\n"):
        if "## Active Agents" in line:
            in_table = True
            continue
        if in_table:
            if line.startswith("##"):
                break
            if line.startswith("|"):
                if "Agent" in line and "Role" in line:
                    header_passed = False
                    continue
                if "---" in line:
                    header_passed = True
                    continue
                if header_passed and "_No agents" not in line:
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        agents.append(
                            {
                                "name": parts[0],
                                "role": parts[1],
                                "status": parts[2],
                                "heartbeat": parts[3],
                            }
                        )

    return agents


def parse_pending_tasks(content: str) -> list[str]:
    """Parse pending tasks from state file.

    Args:
        content: State file content

    Returns:
        List of pending task descriptions
    """
    tasks: list[str] = []

    in_section = False
    for line in content.split("\n"):
        if "## Pending Tasks" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##"):
                break
            if line.strip().startswith("-"):
                task = line.strip().lstrip("-").strip()
                if task and "No pending tasks" not in task:
                    tasks.append(task)

    return tasks


def parse_resource_alerts(content: str) -> list[str]:
    """Parse resource alerts from state file.

    Args:
        content: State file content

    Returns:
        List of resource alert descriptions
    """
    alerts: list[str] = []

    in_section = False
    for line in content.split("\n"):
        if "## Resource Alerts" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##"):
                break
            if line.strip().startswith("-"):
                alert = line.strip().lstrip("-").strip()
                if alert and alert != "None":
                    alerts.append(alert)

    return alerts


def format_status_summary(
    out: AmcosOutput,
    agents: list[dict[str, str]],
    tasks: list[str],
    alerts: list[str],
    session_count: int,
) -> None:
    """Format staff status and write verbose banner to log file.

    Args:
        out: AmcosOutput instance for logging
        agents: List of active agent dicts
        tasks: List of pending tasks
        alerts: List of resource alerts
        session_count: Number of sessions
    """
    out.log("=" * 60)
    out.log("CHIEF OF STAFF - SESSION START")
    out.log("=" * 60)

    out.log(f"\nSession #{session_count}")

    if agents:
        out.log("\nACTIVE AGENTS:")
        for agent in agents:
            status_icon = "+" if agent["status"].lower() == "active" else "?"
            out.log(
                f"  [{status_icon}] {agent['name']} ({agent['role']}) - {agent['status']}"
            )
    else:
        out.log("\nNo active agents registered.")

    if tasks:
        out.log(f"\nPENDING TASKS ({len(tasks)}):")
        for task in tasks[:5]:
            out.log(f"  - {task[:70]}")
        if len(tasks) > 5:
            out.log(f"  ... and {len(tasks) - 5} more")

    if alerts:
        out.log("\n!!! RESOURCE ALERTS !!!")
        for alert in alerts:
            out.log(f"  ! {alert}")

    out.log("")
    out.log("=" * 60)
    out.log("State file: .claude/chief-of-staff-state.local.md")
    out.log("=" * 60)


def increment_session_count(content: str) -> str:
    """Increment session count in state file content.

    Args:
        content: State file content

    Returns:
        Updated content with incremented session count
    """
    # Find and increment session count
    match = re.search(r"\*\*Session Count\*\*:\s*(\d+)", content)
    if match:
        old_count = int(match.group(1))
        new_count = old_count + 1
        content = content.replace(
            f"**Session Count**: {old_count}", f"**Session Count**: {new_count}"
        )
    else:
        # Add session count if missing
        content = content.replace(
            "# Chief of Staff State\n",
            "# Chief of Staff State\n\n**Session Count**: 1\n",
        )

    return content


def get_session_count(content: str) -> int:
    """Get session count from state file content.

    Args:
        content: State file content

    Returns:
        Session count integer
    """
    match = re.search(r"\*\*Session Count\*\*:\s*(\d+)", content)
    if match:
        return int(match.group(1))
    return 1


def main() -> int:
    """Main entry point for SessionStart hook.

    Reads session info from stdin, loads or creates Chief of Staff state file,
    and outputs a status summary to stdout.

    Returns:
        Exit code: 0 for success
    """
    out = AmcosOutput("amcos_session_start")

    # Read hook input from stdin (may be empty for SessionStart)
    try:
        stdin_data = sys.stdin.read()
        if stdin_data.strip():
            hook_input = json.loads(stdin_data)
        else:
            hook_input = {}
    except json.JSONDecodeError:
        hook_input = {}

    out.log_json(hook_input, label="hook_input")

    # Get working directory from input or environment
    cwd = hook_input.get("cwd", os.getcwd())
    state_file = get_state_file(cwd)
    out.log(f"State file: {state_file}")

    # Create state file if not exists
    if not state_file.exists():
        out.log("State file not found, creating default")
        default_content = create_default_state()
        if not write_file_safely(state_file, default_content):
            out.summary("WARN", "Could not create state file")
            out.close()
            return 0  # Silent failure
        content = default_content
    else:
        content = read_file_safely(state_file)
        if not content:
            out.log("State file empty, recreating default")
            content = create_default_state()
            write_file_safely(state_file, content)

    # Increment session count and update timestamp
    content = increment_session_count(content)
    timestamp = get_timestamp()

    # Update last updated timestamp
    content = re.sub(
        r"\*\*Last Updated\*\*:\s*[^\n]+", f"**Last Updated**: {timestamp}", content
    )

    # Save updated state
    write_file_safely(state_file, content)

    # Parse state
    agents = parse_active_agents(content)
    tasks = parse_pending_tasks(content)
    alerts = parse_resource_alerts(content)
    session_count = get_session_count(content)

    # Write verbose banner to log file
    format_status_summary(out, agents, tasks, alerts, session_count)

    # Print concise summary to stdout for the hook consumer
    out.summary("DONE", f"Session #{session_count} initialized")
    out.close()

    return 0


def _cli() -> None:
    """Entrypoint wrapper so the exit call lives inside a function, not at module scope."""
    raise SystemExit(main())


if __name__ == "__main__":
    _cli()
