#!/usr/bin/env python3
"""
amcos_repair_memory.py - Repair corrupted memory files for AI Maestro Chief of Staff.

Detects and repairs corruption in design/memory/ files:
- Missing design/memory/ directory
- Missing memory files (activeContext.md, progress.md, patterns.md)
- Missing required sections in activeContext.md and progress.md
- Malformed markdown headers (missing ##)
- Duplicate sections (keeps first occurrence)

Dependencies: Python 3.8+ stdlib only
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# =============================================================================
# Constants
# =============================================================================

# Required sections for each memory file.
# Keys are the filename stems, values are lists of section headers that must exist.
REQUIRED_SECTIONS: dict[str, list[str]] = {
    "activeContext": [
        "## Current Focus",
        "## Active Decisions",
        "## Recent Errors",
    ],
    "progress": [
        "## Completed",
        "## In Progress",
    ],
    "patterns": [],
}

# Default content templates used when creating missing files from scratch.
TEMPLATES: dict[str, str] = {
    "activeContext": """# Active Context

## Current Focus

**Updated**: {timestamp}

No active focus set.

## Active Decisions

- No decisions recorded yet.

## Recent Errors

No errors recorded.
""",
    "progress": """# Progress Log

## Completed

No completed items yet.

## In Progress

No items in progress.
""",
    "patterns": """# Patterns & Conventions

## General

No patterns recorded yet.
""",
}


# =============================================================================
# Data Structures
# =============================================================================


@dataclass
class RepairAction:
    """A single repair action that was performed (or would be performed in dry-run)."""

    file: str
    description: str
    severity: str  # "info", "warning", "error"


@dataclass
class RepairReport:
    """Aggregated report of all repair actions."""

    actions: list[RepairAction] = field(default_factory=list)
    unrecoverable: list[str] = field(default_factory=list)

    @property
    def action_count(self) -> int:
        return len(self.actions)

    @property
    def has_unrecoverable(self) -> bool:
        return len(self.unrecoverable) > 0


# =============================================================================
# Repair Functions
# =============================================================================


def _get_timestamp() -> str:
    """Get current timestamp in standard format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _read_file(path: Path) -> str:
    """Read file content. Returns empty string if file does not exist or cannot be read."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _write_file(path: Path, content: str) -> bool:
    """Write content to file. Creates parent directories if needed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except OSError as e:
        print(f"ERROR: Cannot write {path}: {e}", file=sys.stderr)
        return False


def _fix_malformed_headers(content: str) -> tuple[str, list[str]]:
    """Fix markdown headers that are missing the ## prefix.

    Looks for lines that match known section names but lack proper markdown header syntax.
    Returns the fixed content and a list of descriptions of what was fixed.
    """
    fixes: list[str] = []
    known_sections = [
        "Current Focus",
        "Active Decisions",
        "Recent Errors",
        "In-Flight Errors",
        "Completed",
        "In Progress",
        "General",
        "Patterns & Conventions",
        "Progress Log",
        "Active Context",
    ]
    lines = content.split("\n")
    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Check if the line is a known section name without markdown header prefix
        if stripped in known_sections and not stripped.startswith("#"):
            new_lines.append(f"## {stripped}")
            fixes.append(f"Fixed malformed header: '{stripped}' -> '## {stripped}'")
        else:
            new_lines.append(line)
    return "\n".join(new_lines), fixes


def _remove_duplicate_sections(content: str) -> tuple[str, list[str]]:
    """Remove duplicate ## sections, keeping only the first occurrence of each.

    Returns the fixed content and a list of descriptions of what was removed.
    """
    fixes: list[str] = []
    # Split content into sections by ## headers
    # Each section starts with a ## line (except possibly the first chunk which is the file header)
    section_pattern = re.compile(r"^(## .+)$", re.MULTILINE)
    parts = section_pattern.split(content)

    # parts alternates between: [pre-header text, header1, body1, header2, body2, ...]
    if len(parts) < 3:
        # No ## headers found or only one section -- nothing to deduplicate
        return content, fixes

    result_parts: list[str] = [parts[0]]  # Keep the preamble (before first ## header)
    seen_headers: set[str] = set()

    # Iterate over (header, body) pairs
    i = 1
    while i < len(parts) - 1:
        header = parts[i]
        body = parts[i + 1]
        header_normalized = header.strip().lower()
        if header_normalized in seen_headers:
            fixes.append(f"Removed duplicate section: '{header.strip()}'")
        else:
            seen_headers.add(header_normalized)
            result_parts.append(header)
            result_parts.append(body)
        i += 2

    # Handle trailing header without body (edge case)
    if i < len(parts):
        header = parts[i]
        header_normalized = header.strip().lower()
        if header_normalized not in seen_headers:
            result_parts.append(header)

    return "".join(result_parts), fixes


def _ensure_required_sections(content: str, file_stem: str) -> tuple[str, list[str]]:
    """Ensure all required sections exist in the file content.

    Missing sections are appended at the end of the file.
    Returns the fixed content and a list of descriptions of what was added.
    """
    required = REQUIRED_SECTIONS.get(file_stem, [])
    if not required:
        return content, []

    fixes: list[str] = []
    for section_header in required:
        if section_header not in content:
            # Append the missing section at the end
            content = (
                content.rstrip("\n") + f"\n\n{section_header}\n\nNo entries yet.\n"
            )
            fixes.append(f"Added missing section: '{section_header}'")

    return content, fixes


def repair_memory(project_root: Path, dry_run: bool, verbose: bool) -> RepairReport:
    """Repair corrupted memory files.

    Checks for and repairs:
    1. Missing design/memory/ directory
    2. Missing memory files
    3. Malformed markdown headers
    4. Duplicate sections
    5. Missing required sections

    Args:
        project_root: Path to the project root directory containing design/memory/
        dry_run: If True, report what would be fixed without modifying files
        verbose: If True, print detailed progress

    Returns:
        RepairReport with all actions taken and any unrecoverable issues
    """
    report = RepairReport()
    memory_dir = project_root / "design" / "memory"
    timestamp = _get_timestamp()

    # Step 1: Check and create memory directory
    if not memory_dir.exists():
        report.actions.append(
            RepairAction(
                file="design/memory/",
                description="Created missing memory directory",
                severity="warning",
            )
        )
        if not dry_run:
            try:
                memory_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                report.unrecoverable.append(f"Cannot create memory directory: {e}")
                return report
        if verbose:
            print(f"{'[DRY-RUN] Would create' if dry_run else 'CREATED'}: {memory_dir}")

    # Step 2: Check and create missing memory files
    file_map = {
        "activeContext": memory_dir / "activeContext.md",
        "progress": memory_dir / "progress.md",
        "patterns": memory_dir / "patterns.md",
    }

    for stem, path in file_map.items():
        if not path.exists():
            template_content = TEMPLATES[stem].format(timestamp=timestamp)
            report.actions.append(
                RepairAction(
                    file=str(path.relative_to(project_root)),
                    description="Created missing file from template",
                    severity="warning",
                )
            )
            if not dry_run:
                if not _write_file(path, template_content):
                    report.unrecoverable.append(f"Cannot create {path}")
                    continue
            if verbose:
                print(f"{'[DRY-RUN] Would create' if dry_run else 'CREATED'}: {path}")
            # File was just created from template -- no further repairs needed for this file
            continue

        # Step 3-5: Repair existing files
        content = _read_file(path)
        if not content.strip():
            # File exists but is empty -- recreate from template
            template_content = TEMPLATES[stem].format(timestamp=timestamp)
            report.actions.append(
                RepairAction(
                    file=str(path.relative_to(project_root)),
                    description="Recreated empty file from template",
                    severity="warning",
                )
            )
            if not dry_run:
                _write_file(path, template_content)
            if verbose:
                print(
                    f"{'[DRY-RUN] Would recreate' if dry_run else 'RECREATED'}: {path} (was empty)"
                )
            continue

        all_fixes: list[str] = []

        # Step 3: Fix malformed headers
        content, header_fixes = _fix_malformed_headers(content)
        all_fixes.extend(header_fixes)

        # Step 4: Remove duplicate sections
        content, dup_fixes = _remove_duplicate_sections(content)
        all_fixes.extend(dup_fixes)

        # Step 5: Ensure required sections exist
        content, section_fixes = _ensure_required_sections(content, stem)
        all_fixes.extend(section_fixes)

        # Write back if anything changed
        if all_fixes:
            for fix_desc in all_fixes:
                report.actions.append(
                    RepairAction(
                        file=str(path.relative_to(project_root)),
                        description=fix_desc,
                        severity="info",
                    )
                )
            if not dry_run:
                if not _write_file(path, content):
                    report.unrecoverable.append(
                        f"Cannot write repaired content to {path}"
                    )
            if verbose:
                prefix = "[DRY-RUN] Would apply" if dry_run else "APPLIED"
                print(f"{prefix} {len(all_fixes)} fix(es) to {path}:")
                for fix_desc in all_fixes:
                    print(f"  - {fix_desc}")
        elif verbose:
            print(f"OK: {path} (no repairs needed)")

    return report


# =============================================================================
# CLI
# =============================================================================


def _create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Repair corrupted AMCOS memory files in design/memory/",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root directory containing design/memory/ (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be repaired without modifying files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress for each file",
    )
    return parser


def main() -> int:
    """Main entry point."""
    args = _create_parser().parse_args()
    project_root = args.project_root.resolve()

    if args.dry_run:
        print(f"DRY-RUN: Scanning {project_root / 'design' / 'memory'}")
    else:
        print(f"Repairing memory files in {project_root / 'design' / 'memory'}")

    report = repair_memory(project_root, dry_run=args.dry_run, verbose=args.verbose)

    # Print summary
    if report.has_unrecoverable:
        print(f"\nUNRECOVERABLE ERRORS ({len(report.unrecoverable)}):")
        for err in report.unrecoverable:
            print(f"  FATAL: {err}")
        return 1

    if report.action_count == 0:
        print("\nAll memory files are healthy. Nothing to repair.")
    else:
        prefix = "Would repair" if args.dry_run else "Repaired"
        print(f"\n{prefix} {report.action_count} issue(s):")
        for action in report.actions:
            print(f"  [{action.severity.upper()}] {action.file}: {action.description}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
