#!/usr/bin/env python3
"""
Chief of Staff Skills Reindex Script

Triggers a PSS (Perfect Skill Suggester) reindex for an agent session.

Sends the /pss-reindex-skills command to the target agent via AI Maestro
AMP messaging. Supports --force and --dry-run flags.

Usage:
    python3 amcos_reindex_skills.py SESSION_NAME
    python3 amcos_reindex_skills.py SESSION_NAME --force
    python3 amcos_reindex_skills.py SESSION_NAME --dry-run

Output:
    JSON with reindex request status including:
    - success: boolean indicating if request was sent
    - session: target session name
    - status: current status (pending/sent/completed)
    - message: human-readable status message
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone

from amcos_output_utils import AmcosOutput


def send_ai_maestro_message(
    to_session: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "command",
) -> tuple[bool, str]:
    """
    Send a message via AMP CLI (amp-send).

    Args:
        to_session: Target session name
        subject: Message subject
        message: Message content
        priority: Message priority
        msg_type: Message type

    Returns:
        Tuple of (success, response_or_error)
    """
    try:
        result = subprocess.run(
            [
                "amp-send",
                to_session,
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
        if result.returncode == 0:
            return True, result.stdout.strip() or "sent"
        else:
            return False, result.stderr.strip() or "amp-send command failed"

    except subprocess.TimeoutExpired:
        return False, "Request timed out"
    except FileNotFoundError:
        return False, "amp-send not found in PATH"
    except Exception as e:
        return False, str(e)


def check_ai_maestro_available() -> bool:
    """
    Check if AMP CLI (amp-send) is available.

    Returns:
        True if amp-send is reachable, False otherwise
    """
    try:
        result = subprocess.run(
            ["amp-send", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def main() -> int:
    """Main entry point."""
    out = AmcosOutput("amcos_reindex_skills")
    parser = argparse.ArgumentParser(
        description="Trigger PSS skill reindex for an agent session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Request reindex for a session
    python3 amcos_reindex_skills.py my-session

    # Force reindex (bypass any caching)
    python3 amcos_reindex_skills.py my-session --force

    # Dry run - show what would be done
    python3 amcos_reindex_skills.py my-session --dry-run

        """,
    )

    parser.add_argument(
        "session_name", help="Name of the agent session to reindex skills for"
    )

    parser.add_argument(
        "--force", action="store_true", help="Force reindex, bypassing any caching"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually sending the request",
    )

    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Build the command message
    command = "/pss-reindex-skills"
    if args.force:
        command += " --force"

    result: dict[str, object] = {
        "session": args.session_name,
        "command": command,
        "timestamp": timestamp,
    }

    if args.dry_run:
        result.update(
            {
                "success": True,
                "status": "dry_run",
                "message": f"Would send reindex command to session '{args.session_name}'",
                "command_to_send": command,
            }
        )
        out.log_json(result, label="dry_run")
        print(json.dumps(result, separators=(",", ":")))
        out.summary("DONE", f"Dry run: reindex for '{args.session_name}'")
        out.close()
        return 0

    # Check if AMP CLI is available
    if not check_ai_maestro_available():
        result.update(
            {
                "success": False,
                "status": "stub",
                "message": "AMP CLI (amp-send) not available. This is a STUB implementation.",
                "todo": [
                    "Install AMP CLI (amp-send)",
                    "Add support for /pss-reindex-skills command via message",
                    "Add status tracking for reindex completion",
                ],
            }
        )
        out.log_json(result, label="error")
        print(json.dumps(result, separators=(",", ":")), file=sys.stderr)
        out.close()
        return 1

    # Send the reindex request via AI Maestro
    subject = "PSS Reindex Request"
    message = f"Please execute: {command}"

    success, response = send_ai_maestro_message(
        args.session_name,
        subject,
        message,
        priority="normal",
        msg_type="command_request",
    )

    if success:
        result.update(
            {
                "success": True,
                "status": "sent",
                "message": f"Reindex request sent to session '{args.session_name}'",
                "message_id": response,
                "note": "The target session must process the command manually. "
                "Automated command execution is not yet implemented.",
            }
        )
    else:
        result.update(
            {
                "success": False,
                "status": "failed",
                "message": f"Failed to send reindex request: {response}",
                "error": response,
            }
        )

    out.log_json(result, label="reindex_result")
    print(json.dumps(result, separators=(",", ":")))
    if result.get("success", False):
        out.summary("DONE", f"Reindex sent to '{args.session_name}'")
        out.close()
        return 0
    else:
        out.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
