#!/usr/bin/env python3
"""
ecos_archive_logs.py - Archive operation logs older than N days.

Scans .emasoft/logs/ for log files and moves files older than the specified
number of days into .emasoft/logs/archive/YYYY-MM/ subdirectories.
Preserves original file timestamps and reports files archived and space saved.

Dependencies: Python 3.8+ stdlib only

Usage:
    ecos_archive_logs.py [--project-root PATH] [--days 30] [--dry-run] [--verbose]

Exit codes:
    0 - Success
    1 - Error (directory not found, permission error)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOGS_DIR = ".emasoft/logs"
ARCHIVE_SUBDIR = "archive"
DEFAULT_DAYS = 30


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_logs_path(project_root: Path) -> Path:
    """Return the path to the .emasoft/logs/ directory."""
    return project_root / LOGS_DIR


def get_archive_path(project_root: Path) -> Path:
    """Return the path to the .emasoft/logs/archive/ directory."""
    return get_logs_path(project_root) / ARCHIVE_SUBDIR


def file_mtime(path: Path) -> datetime:
    """Get the modification time of a file as a timezone-aware datetime.

    Args:
        path: Path to the file.

    Returns:
        Modification time in UTC.
    """
    stat = path.stat()
    return datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)


def file_size_bytes(path: Path) -> int:
    """Get the size of a file in bytes.

    Args:
        path: Path to the file.

    Returns:
        File size in bytes.
    """
    return path.stat().st_size


def format_size(size_bytes: int) -> str:
    """Format a byte count as a human-readable string.

    Args:
        size_bytes: Size in bytes.

    Returns:
        Formatted string (e.g., '1.5 MB', '320 KB').
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


# ---------------------------------------------------------------------------
# Scanning and archiving
# ---------------------------------------------------------------------------


def find_old_logs(logs_dir: Path, cutoff: datetime) -> list[Path]:
    """Find log files older than the cutoff date.

    Only considers files directly in the logs directory (not in archive/
    or other subdirectories).

    Args:
        logs_dir: Path to the logs directory.
        cutoff: Files modified before this datetime will be returned.

    Returns:
        List of paths to old log files, sorted by modification time.
    """
    old_files: list[Path] = []

    if not logs_dir.is_dir():
        return old_files

    for entry in sorted(logs_dir.iterdir()):
        # Skip directories (including archive/)
        if not entry.is_file():
            continue

        mtime = file_mtime(entry)
        if mtime < cutoff:
            old_files.append(entry)

    # Sort oldest first
    old_files.sort(key=lambda p: file_mtime(p))
    return old_files


def archive_file(file_path: Path, archive_root: Path, verbose: bool = False) -> Path:
    """Move a log file to the archive directory, preserving timestamps.

    The file is placed in archive/YYYY-MM/ based on its modification time.

    Args:
        file_path: Path to the log file to archive.
        archive_root: Root archive directory (.emasoft/logs/archive/).
        verbose: If True, print progress to stderr.

    Returns:
        Path to the archived file.
    """
    mtime = file_mtime(file_path)
    month_dir = archive_root / mtime.strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)

    dest = month_dir / file_path.name

    # Handle name collisions by appending a counter
    if dest.exists():
        stem = file_path.stem
        suffix = file_path.suffix
        counter = 1
        while dest.exists():
            dest = month_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    if verbose:
        print(f"  {file_path.name} -> {dest.relative_to(archive_root.parent)}", file=sys.stderr)

    # Move the file (shutil.move preserves metadata on same filesystem)
    shutil.move(str(file_path), str(dest))

    return dest


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error.
    """
    parser = argparse.ArgumentParser(
        description="Archive operation logs older than N days"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=None,
        help="Project root directory (defaults to current directory)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Archive files older than this many days (default: {DEFAULT_DAYS})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be archived without moving files",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed progress to stderr",
    )

    args = parser.parse_args()

    project_root = Path(args.project_root) if args.project_root else Path.cwd()
    if not project_root.is_dir():
        result = {"success": False, "error": f"Not a directory: {project_root}"}
        print(json.dumps(result, indent=2))
        return 1

    logs_dir = get_logs_path(project_root)
    if not logs_dir.exists():
        result = {
            "success": True,
            "warning": f"Logs directory does not exist: {logs_dir}",
            "files_archived": 0,
            "space_saved": "0 B",
        }
        print(json.dumps(result, indent=2))
        return 0

    if not logs_dir.is_dir():
        result = {"success": False, "error": f"Not a directory: {logs_dir}"}
        print(json.dumps(result, indent=2))
        return 1

    # Calculate cutoff date
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=args.days)

    if args.verbose:
        print(f"Scanning: {logs_dir}", file=sys.stderr)
        print(f"Cutoff: {cutoff.strftime('%Y-%m-%d %H:%M:%S UTC')} ({args.days} days ago)", file=sys.stderr)

    # Find old files
    old_files = find_old_logs(logs_dir, cutoff)

    if not old_files:
        result = {
            "success": True,
            "files_archived": 0,
            "space_saved": "0 B",
            "space_saved_bytes": 0,
            "message": f"No log files older than {args.days} days found",
        }
        print(json.dumps(result, indent=2))
        return 0

    if args.verbose:
        print(f"Found {len(old_files)} file(s) to archive", file=sys.stderr)

    # Archive files
    archive_root = get_archive_path(project_root)
    total_size = 0
    archived_count = 0
    archived_files: list[dict[str, str]] = []

    for file_path in old_files:
        size = file_size_bytes(file_path)
        mtime = file_mtime(file_path)

        if args.dry_run:
            month_label = mtime.strftime("%Y-%m")
            if args.verbose:
                print(f"  [DRY RUN] Would archive: {file_path.name} ({format_size(size)}) -> archive/{month_label}/", file=sys.stderr)
            archived_files.append({
                "name": file_path.name,
                "size": format_size(size),
                "modified": mtime.isoformat(),
                "destination": f"archive/{month_label}/{file_path.name}",
            })
        else:
            dest = archive_file(file_path, archive_root, verbose=args.verbose)
            archived_files.append({
                "name": file_path.name,
                "size": format_size(size),
                "modified": mtime.isoformat(),
                "destination": str(dest),
            })

        total_size += size
        archived_count += 1

    result_out: dict[str, Any] = {
        "success": True,
        "dry_run": args.dry_run,
        "files_archived": archived_count,
        "space_saved": format_size(total_size),
        "space_saved_bytes": total_size,
        "cutoff_days": args.days,
        "cutoff_date": cutoff.isoformat(),
    }

    if args.verbose or args.dry_run:
        result_out["files"] = archived_files

    print(json.dumps(result_out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
