#!/usr/bin/env python3
"""
AI Maestro Chief of Staff - Notify Agent Script (amcos_notify_agent.py)

Sends an AI Maestro message to an agent via AMP CLI (amp-send.sh).

Resolves the agent name via the AI Maestro API when available,
otherwise falls back to sending directly by session name.

Usage:
    python amcos_notify_agent.py my-agent --subject "Update" --message "Requirements changed"
    python amcos_notify_agent.py my-agent -s "Task" -m "Please review" -p high
    python amcos_notify_agent.py my-agent -s "Info" -m "Done" --type acknowledgment

Output: Human-readable status lines + JSON summary on success
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def resolve_agent(agent_name: str) -> str | None:
    """
    Resolve agent name to session name via the AI Maestro API.

    Queries $AIMAESTRO_API/api/agents?name=<agent_name>.
    Returns the session name if found, None otherwise.
    """
    api_base = os.environ.get("AIMAESTRO_API", "http://localhost:23000")
    url = f"{api_base}/api/agents?name={agent_name}"

    try:
        result = subprocess.run(
            ["curl", "-sf", url],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None

        data = json.loads(result.stdout)

        # Handle both single-agent and list responses
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("session_name") or data[0].get("name")
        if isinstance(data, dict):
            return data.get("session_name") or data.get("name")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        pass

    return None


def send_message(
    to: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "notification",
) -> bool:
    """
    Send a message via AMP CLI (amp-send).

    Args:
        to: Target agent session name
        subject: Message subject
        message: Message content
        priority: Message priority (low, normal, high, urgent)
        msg_type: Message type (notification, request, acknowledgment, etc.)

    Returns:
        True if message was sent successfully, False otherwise.
    """
    try:
        result = subprocess.run(
            [
                "amp-send",
                to,
                subject,
                message,
                "--priority",
                priority,
                "--type",
                msg_type,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0 and result.stderr:
            print(f"amp-send stderr: {result.stderr.strip()}", file=sys.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Error: amp-send timed out after 30s", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: amp-send not found on PATH", file=sys.stderr)
        return False
    except OSError as exc:
        print(f"Error running amp-send: {exc}", file=sys.stderr)
        return False


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Send an AI Maestro message to an agent via AMP CLI"
    )
    parser.add_argument(
        "agent_name",
        help="Agent session name or registered name (e.g. libs-svg-svgbbox)",
    )
    parser.add_argument("--subject", "-s", required=True, help="Message subject")
    parser.add_argument("--message", "-m", required=True, help="Message content")
    parser.add_argument(
        "--priority",
        "-p",
        choices=["low", "normal", "high", "urgent"],
        default="normal",
        help="Message priority (default: normal)",
    )
    parser.add_argument(
        "--type",
        "-t",
        dest="msg_type",
        default="notification",
        help="Message type (notification, request, acknowledgment, etc.)",
    )

    args = parser.parse_args()

    # Try to resolve agent name via the AI Maestro API
    session_name = resolve_agent(args.agent_name)
    if session_name:
        print(f"Resolved '{args.agent_name}' -> session '{session_name}'")
    else:
        # Fall back to using the provided name directly as session name
        session_name = args.agent_name
        print(f"API lookup failed; sending directly to '{session_name}'")

    # Send message
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"Sending message to '{session_name}' at {timestamp} ...")

    sent = send_message(
        to=session_name,
        subject=args.subject,
        message=args.message,
        priority=args.priority,
        msg_type=args.msg_type,
    )

    if sent:
        summary = {
            "status": "sent",
            "to": session_name,
            "subject": args.subject,
            "priority": args.priority,
            "type": args.msg_type,
            "timestamp": timestamp,
        }
        print(json.dumps(summary, indent=2))
        return 0

    print("Failed to send message. Check AI Maestro service status.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
