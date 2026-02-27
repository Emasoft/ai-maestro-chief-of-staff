#!/usr/bin/env python3
"""
pss_reindex_skills.py - Local PSS (Perfect Skill Suggester) skill reindexing.

Scans a skills directory for SKILL.md files, extracts metadata from each
(name, description, triggers, categories, keywords), and generates a skills
index JSON file.

This is a simplified LOCAL version. The full PSS reindex uses the
/pss-reindex-skills slash command with AI analysis via parallel agents.
The remote version is triggered by amcos_reindex_skills.py which delegates
to another agent session via AI Maestro.

Dependencies: Python 3.8+ stdlib only

Usage:
    pss_reindex_skills.py [--skills-dir PATH] [--output FILE] [--verbose]

Exit codes:
    0 - Success
    1 - Error (directory not found, parse error)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKILL_FILENAME = "SKILL.md"
DEFAULT_SKILLS_DIR = "skills"
DEFAULT_OUTPUT_FILE = "skills-index.json"

# Frontmatter fields we extract
KNOWN_FRONTMATTER_FIELDS = frozenset({
    "name", "description", "triggers", "categories", "keywords",
    "context", "agent", "user-invocable", "version",
})


# ---------------------------------------------------------------------------
# YAML frontmatter extraction (stdlib only)
# ---------------------------------------------------------------------------


def extract_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter fields from SKILL.md content.

    Handles:
    - key: scalar_value
    - key: [item1, item2] (inline list)
    - key:\\n  - item1\\n  - item2 (block list)

    Args:
        content: Full file content.

    Returns:
        Dict of extracted frontmatter fields.
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    result: dict[str, Any] = {}
    lines = frontmatter_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            i += 1
            continue

        kv_match = re.match(r"^([\w][\w-]*)\s*:\s*(.*)", line)
        if not kv_match:
            i += 1
            continue

        key = kv_match.group(1)
        value = kv_match.group(2).strip()

        if value.startswith("[") and value.endswith("]"):
            # Inline list: [item1, item2, item3]
            inner = value[1:-1]
            inline_items = [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
            result[key] = inline_items
            i += 1
        elif value:
            # Scalar value
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            result[key] = value
            i += 1
        else:
            # Possible block list or empty value
            items: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                if not next_stripped or next_stripped.startswith("#"):
                    i += 1
                    continue
                if next_stripped.startswith("- "):
                    item = next_stripped[2:].strip().strip("'\"")
                    items.append(item)
                    i += 1
                else:
                    break
            result[key] = items if items else ""

    return result


# ---------------------------------------------------------------------------
# Content-based extraction (fallback when no frontmatter)
# ---------------------------------------------------------------------------


def extract_from_content(content: str, skill_dir: Path) -> dict[str, Any]:
    """Extract skill metadata from SKILL.md content when frontmatter is absent.

    Falls back to parsing the first heading as name and the first paragraph
    as description.

    Args:
        content: Full file content.
        skill_dir: Path to the skill directory (used for fallback name).

    Returns:
        Dict with 'name' and 'description' at minimum.
    """
    result: dict[str, Any] = {}

    # Try to get name from first H1 heading
    h1_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if h1_match:
        result["name"] = h1_match.group(1).strip()
    else:
        # Fall back to directory name
        result["name"] = skill_dir.name

    # Try to get description from first non-heading paragraph
    lines = content.split("\n")
    desc_lines: list[str] = []
    past_heading = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if past_heading:
                break
            past_heading = True
            continue
        if past_heading and stripped:
            desc_lines.append(stripped)
        elif past_heading and not stripped and desc_lines:
            break

    if desc_lines:
        result["description"] = " ".join(desc_lines)

    return result


# ---------------------------------------------------------------------------
# Skill scanning
# ---------------------------------------------------------------------------


def scan_skill_directory(skill_dir: Path, verbose: bool = False) -> dict[str, Any] | None:
    """Scan a single skill directory and extract its metadata.

    Args:
        skill_dir: Path to a skill directory containing SKILL.md.
        verbose: If True, print progress to stderr.

    Returns:
        Skill metadata dict, or None if SKILL.md not found.
    """
    skill_file = skill_dir / SKILL_FILENAME
    if not skill_file.exists():
        return None

    if verbose:
        print(f"  Scanning: {skill_dir.name}", file=sys.stderr)

    content = skill_file.read_text(encoding="utf-8")

    # Try frontmatter first
    metadata = extract_frontmatter(content)

    # Fall back to content-based extraction
    if not metadata.get("name"):
        fallback = extract_from_content(content, skill_dir)
        for key, val in fallback.items():
            if key not in metadata or not metadata[key]:
                metadata[key] = val

    # Ensure minimum fields
    entry: dict[str, Any] = {
        "skill_name": metadata.get("name", skill_dir.name),
        "description": metadata.get("description", ""),
        "triggers": metadata.get("triggers", []),
        "categories": metadata.get("categories", []),
        "keywords": metadata.get("keywords", []),
        "path": str(skill_dir),
        "has_frontmatter": bool(extract_frontmatter(content)),
    }

    # Normalize list fields (might be strings if single value)
    for list_field in ("triggers", "categories", "keywords"):
        val = entry[list_field]
        if isinstance(val, str):
            entry[list_field] = [val] if val else []

    if verbose:
        trigger_count = len(entry["triggers"])
        cat_count = len(entry["categories"])
        kw_count = len(entry["keywords"])
        print(
            f"    name={entry['skill_name']}, "
            f"triggers={trigger_count}, categories={cat_count}, keywords={kw_count}",
            file=sys.stderr,
        )

    return entry


def scan_skills_tree(skills_dir: Path, verbose: bool = False) -> list[dict[str, Any]]:
    """Scan an entire skills directory tree for SKILL.md files.

    Looks for SKILL.md in immediate subdirectories (each subdirectory is
    assumed to be one skill).

    Args:
        skills_dir: Root directory containing skill subdirectories.
        verbose: If True, print progress to stderr.

    Returns:
        List of skill metadata dicts.
    """
    skills: list[dict[str, Any]] = []

    if not skills_dir.is_dir():
        return skills

    # Check if this directory itself contains SKILL.md
    if (skills_dir / SKILL_FILENAME).exists():
        entry = scan_skill_directory(skills_dir, verbose)
        if entry:
            skills.append(entry)

    # Scan subdirectories
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name.startswith("_"):
            continue

        entry = scan_skill_directory(child, verbose)
        if entry:
            skills.append(entry)

    return skills


# ---------------------------------------------------------------------------
# Index generation
# ---------------------------------------------------------------------------


def generate_index(skills: list[dict[str, Any]], skills_dir: str) -> dict[str, Any]:
    """Generate a skills index JSON structure.

    Args:
        skills: List of skill metadata dicts.
        skills_dir: Path that was scanned (for metadata).

    Returns:
        Index dict ready for JSON serialization.
    """
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "pss_reindex_skills.py (local)",
        "source_directory": skills_dir,
        "skill_count": len(skills),
        "skills": skills,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error.
    """
    parser = argparse.ArgumentParser(
        description="Local PSS skill reindexing - scan skills and generate index JSON"
    )
    parser.add_argument(
        "--skills-dir",
        type=str,
        default=None,
        help=f"Skills directory to scan (default: ./{DEFAULT_SKILLS_DIR})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help=f"Output file path (default: ./{DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print scan progress to stderr",
    )

    args = parser.parse_args()

    # Resolve skills directory
    if args.skills_dir:
        skills_dir = Path(args.skills_dir)
    else:
        skills_dir = Path.cwd() / DEFAULT_SKILLS_DIR

    if not skills_dir.exists():
        result = {"success": False, "error": f"Skills directory not found: {skills_dir}"}
        print(json.dumps(result, indent=2))
        return 1

    if not skills_dir.is_dir():
        result = {"success": False, "error": f"Not a directory: {skills_dir}"}
        print(json.dumps(result, indent=2))
        return 1

    if args.verbose:
        print(f"Scanning skills in: {skills_dir}", file=sys.stderr)

    # Scan
    skills = scan_skills_tree(skills_dir, verbose=args.verbose)

    if args.verbose:
        print(f"Found {len(skills)} skill(s)", file=sys.stderr)

    # Generate index
    index = generate_index(skills, str(skills_dir))

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(index, indent=2, default=str) + "\n", encoding="utf-8")
        if args.verbose:
            print(f"Wrote index to: {output_path}", file=sys.stderr)
        # Also print success summary to stdout
        summary = {
            "success": True,
            "skill_count": len(skills),
            "output_file": str(output_path),
        }
        print(json.dumps(summary, indent=2))
    else:
        # Print full index to stdout
        print(json.dumps(index, indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
