#!/usr/bin/env python3
"""
ecos_snapshot_memory.py - Create coordinated point-in-time snapshots of ECOS memory files.

Creates, lists, and restores coordinated snapshots of all three memory files
(activeContext.md, progress.md, patterns.md) with metadata (timestamp, reason,
label, file sizes, SHA-256 hashes).

Dependencies: Python 3.8+ stdlib only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


# =============================================================================
# Constants
# =============================================================================

MEMORY_FILES = ["activeContext.md", "progress.md", "patterns.md"]
METADATA_FILENAME = "metadata.json"


# =============================================================================
# Core Functions
# =============================================================================


def _sha256(path: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _get_memory_dir(project_root: Path) -> Path:
    """Return the path to the memory directory."""
    return project_root / "design" / "memory"


def _get_snapshots_dir(project_root: Path) -> Path:
    """Return the path to the snapshots directory."""
    return _get_memory_dir(project_root) / "snapshots"


def create_snapshot(project_root: Path, reason: str, label: str | None = None) -> Path:
    """Create a coordinated snapshot of all three memory files.

    Copies activeContext.md, progress.md, and patterns.md into a timestamped
    snapshot directory, along with a metadata.json file containing the reason,
    label, file sizes, and SHA-256 hashes.

    Args:
        project_root: Path to the project root directory
        reason: Human-readable reason for the snapshot
        label: Optional short label for the snapshot directory name

    Returns:
        Path to the created snapshot directory

    Raises:
        FileNotFoundError: If the memory directory does not exist
        FileNotFoundError: If any memory file is missing
    """
    memory_dir = _get_memory_dir(project_root)
    if not memory_dir.exists():
        raise FileNotFoundError(f"Memory directory does not exist: {memory_dir}")

    # Verify all memory files exist before creating snapshot
    missing = [f for f in MEMORY_FILES if not (memory_dir / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing memory files: {', '.join(missing)}")

    # Build snapshot directory name: YYYY-MM-DD-HHMMSS[-label]
    now = datetime.now()
    dir_name = now.strftime("%Y-%m-%d-%H%M%S")
    if label:
        # Sanitize label: lowercase, replace spaces/special chars with hyphens
        safe_label = "".join(c if c.isalnum() or c == "-" else "-" for c in label.lower()).strip("-")
        if safe_label:
            dir_name = f"{dir_name}-{safe_label}"

    snapshot_dir = _get_snapshots_dir(project_root) / dir_name
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Copy files and collect metadata
    file_sizes: dict[str, int] = {}
    file_hashes: dict[str, str] = {}

    for filename in MEMORY_FILES:
        src = memory_dir / filename
        dst = snapshot_dir / filename
        shutil.copy2(src, dst)
        file_sizes[filename] = src.stat().st_size
        file_hashes[filename] = _sha256(src)

    # Write metadata
    metadata = {
        "timestamp": now.isoformat(),
        "reason": reason,
        "label": label or "",
        "dir_name": dir_name,
        "file_sizes": file_sizes,
        "file_hashes": file_hashes,
    }
    metadata_path = snapshot_dir / METADATA_FILENAME
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return snapshot_dir


def list_snapshots(project_root: Path) -> list[dict]:
    """List all existing snapshots with their metadata.

    Returns a list of metadata dicts sorted by timestamp (newest first).
    """
    snapshots_dir = _get_snapshots_dir(project_root)
    if not snapshots_dir.exists():
        return []

    results: list[dict] = []
    for entry in sorted(snapshots_dir.iterdir(), reverse=True):
        if not entry.is_dir():
            continue
        meta_path = entry / METADATA_FILENAME
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                meta["path"] = str(entry)
                results.append(meta)
            except (json.JSONDecodeError, OSError):
                # Snapshot directory exists but metadata is corrupt -- include basic info
                results.append({
                    "dir_name": entry.name,
                    "path": str(entry),
                    "timestamp": "unknown",
                    "reason": "(metadata corrupt or missing)",
                    "label": "",
                })
        else:
            results.append({
                "dir_name": entry.name,
                "path": str(entry),
                "timestamp": "unknown",
                "reason": "(no metadata.json)",
                "label": "",
            })

    return results


def restore_snapshot(project_root: Path, snapshot_path: Path) -> None:
    """Restore memory files from a snapshot directory.

    Copies the three memory files from the snapshot directory back into
    design/memory/, overwriting the current files.

    Args:
        project_root: Path to the project root directory
        snapshot_path: Path to the snapshot directory to restore from

    Raises:
        FileNotFoundError: If the snapshot directory or any memory file within it is missing
    """
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot directory does not exist: {snapshot_path}")

    memory_dir = _get_memory_dir(project_root)
    memory_dir.mkdir(parents=True, exist_ok=True)

    missing = [f for f in MEMORY_FILES if not (snapshot_path / f).exists()]
    if missing:
        raise FileNotFoundError(f"Snapshot is incomplete, missing: {', '.join(missing)}")

    for filename in MEMORY_FILES:
        src = snapshot_path / filename
        dst = memory_dir / filename
        shutil.copy2(src, dst)


# =============================================================================
# CLI
# =============================================================================


def _create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Create, list, and restore coordinated snapshots of ECOS memory files",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root directory containing design/memory/ (default: current directory)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--reason",
        type=str,
        help="Reason for creating a new snapshot (triggers snapshot creation)",
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="List all existing snapshots",
    )
    group.add_argument(
        "--restore",
        type=Path,
        metavar="SNAPSHOT_DIR",
        help="Restore memory files from a snapshot directory",
    )

    parser.add_argument(
        "--label",
        type=str,
        default=None,
        help="Optional short label appended to the snapshot directory name",
    )
    return parser


def main() -> int:
    """Main entry point."""
    args = _create_parser().parse_args()
    project_root = args.project_root.resolve()

    if args.list:
        snapshots = list_snapshots(project_root)
        if not snapshots:
            print("No snapshots found.")
            return 0
        print(f"{'Timestamp':<26} {'Label':<20} {'Reason'}")
        print("-" * 80)
        for snap in snapshots:
            ts = snap.get("timestamp", "unknown")
            label = snap.get("label", "") or "-"
            reason = snap.get("reason", "")
            print(f"{ts:<26} {label:<20} {reason}")
            print(f"  Path: {snap['path']}")
        print(f"\nTotal: {len(snapshots)} snapshot(s)")
        return 0

    if args.restore:
        restore_path = args.restore.resolve()
        print(f"Restoring memory files from {restore_path}")
        try:
            restore_snapshot(project_root, restore_path)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print("RESTORED: All memory files restored successfully")
        return 0

    # Create snapshot (--reason was provided)
    print("Creating snapshot of memory files...")
    try:
        snapshot_dir = create_snapshot(project_root, reason=args.reason, label=args.label)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"CREATED: Snapshot at {snapshot_dir}")
    # Print file details
    meta_path = snapshot_dir / METADATA_FILENAME
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for filename, size in meta["file_sizes"].items():
        print(f"  {filename}: {size} bytes (sha256: {meta['file_hashes'][filename][:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
