#!/usr/bin/env python3
"""
amcos_output_utils.py - Shared output utility for AMCOS scripts.

Provides the AmcosOutput class that redirects verbose output to timestamped
log files while printing only a 2-3 line summary to stdout. This reduces
token consumption when scripts are invoked by Claude Code hooks or commands.

Dependencies: Python 3.8+ stdlib only

Usage:
    from amcos_output_utils import AmcosOutput

    def main() -> int:
        out = AmcosOutput("amcos_my_script")
        out.log("Detailed progress message...")
        out.log_json({"key": "value"}, label="result")
        out.summary("DONE", "Completed task X successfully")
        return 0
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ANSI escape code pattern for stripping terminal colors from log output
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")

# Default log retention in days (configurable via AMCOS_LOG_RETENTION_DAYS env var)
_DEFAULT_RETENTION_DAYS = 7


class AmcosOutput:
    """Context-managed output handler that writes verbose output to log files.

    All detailed output goes to a timestamped log file under .amcos-logs/.
    Only a 2-3 line summary is printed to stdout for the parent agent/user.
    """

    def __init__(self, script_name: str, log_dir: Path | None = None) -> None:
        # Determine log directory: explicit > CLAUDE_PROJECT_DIR > cwd > home fallback
        if log_dir is not None:
            base = log_dir
        else:
            project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
            if project_dir:
                base = Path(project_dir) / ".amcos-logs"
            else:
                # Fallback: try cwd, then home
                cwd_logs = Path.cwd() / ".amcos-logs"
                base = cwd_logs if cwd_logs.parent.exists() else Path.home() / ".amcos-logs"

        self._script_name = script_name
        self._log_dir = base / script_name
        self._log_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamped log file
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self._log_path = self._log_dir / f"{ts}.log"
        self._log_file = open(self._log_path, "w", encoding="utf-8")

        # Write header to log
        self._log_file.write(f"# {script_name} - {ts} UTC\n")
        self._log_file.write(f"# PID: {os.getpid()}\n\n")

        # Auto-cleanup old logs (non-blocking, best-effort)
        self._cleanup_old_logs()

    @property
    def log_path(self) -> str:
        """Return the path to the current log file."""
        return str(self._log_path)

    def log(self, msg: str) -> None:
        """Write a message to the log file (replaces print() calls)."""
        # Strip ANSI codes before writing to log
        clean = self.strip_ansi(msg)
        self._log_file.write(clean + "\n")
        self._log_file.flush()

    def log_json(self, data: Any, label: str = "") -> None:
        """Write JSON data to the log file with indent=0 (compact but readable).

        indent=0 keeps newlines between keys (readable for debugging)
        but removes all whitespace padding (saves 50-80% vs indent=2).
        """
        if label:
            self._log_file.write(f"\n--- {label} ---\n")
        self._log_file.write(json.dumps(data, indent=0, default=str) + "\n")
        self._log_file.flush()

    def summary(self, status: str, message: str, extra: str = "") -> None:
        """Print a concise 2-3 line summary to stdout.

        Format:
            [{STATUS}] script_name - message
            Log: /path/to/logfile.log
            extra (optional third line)
        """
        print(f"[{status}] {self._script_name} - {message}")
        print(f"Log: {self._log_path}")
        if extra:
            print(extra)

    def summary_json(self, data: dict[str, Any]) -> None:
        """Print compact JSON summary to stdout (for programmatic consumers).

        Always includes status, message, and log_path keys.
        Uses separators=(",", ":") for maximum compactness.
        """
        data["log_path"] = str(self._log_path)
        print(json.dumps(data, separators=(",", ":"), default=str))

    def close(self) -> None:
        """Close the log file handle."""
        if self._log_file and not self._log_file.closed:
            self._log_file.close()

    def __del__(self) -> None:
        self.close()

    def __enter__(self) -> AmcosOutput:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Remove ANSI escape codes from text."""
        return _ANSI_RE.sub("", text)

    @staticmethod
    def is_tty() -> bool:
        """Check if stdout is a real terminal (for conditional color output)."""
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def _cleanup_old_logs(self) -> None:
        """Remove log files older than retention period (best-effort, non-blocking)."""
        try:
            retention_days = int(os.environ.get("AMCOS_LOG_RETENTION_DAYS", str(_DEFAULT_RETENTION_DAYS)))
            cutoff = datetime.now(timezone.utc).timestamp() - (retention_days * 86400)
            for log_file in self._log_dir.glob("*.log"):
                if log_file.stat().st_mtime < cutoff:
                    log_file.unlink(missing_ok=True)
        except (OSError, ValueError):
            pass  # Non-critical cleanup failure — ignore
