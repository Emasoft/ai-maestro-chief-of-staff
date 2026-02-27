#!/usr/bin/env python3
"""
amcos_design_search.py - Search design documents by UUID, type, status, or keyword.

Searches .md files in the design/ directory, parsing YAML frontmatter
(using stdlib regex, no PyYAML) to extract metadata fields: uuid, type,
status, title, author, date. Supports filtering by keyword, document type,
status, and UUID prefix match. Output in text table or JSON format.

Dependencies: Python 3.8+ stdlib only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


# =============================================================================
# Data Structures
# =============================================================================


@dataclass
class DesignDocMeta:
    """Metadata extracted from a design document's YAML frontmatter."""

    filepath: str
    filename: str
    uuid: str = ""
    doc_type: str = ""
    status: str = ""
    title: str = ""
    author: str = ""
    date: str = ""
    raw_frontmatter: dict[str, str] = field(default_factory=dict)


# =============================================================================
# Frontmatter Parsing
# =============================================================================


def _parse_frontmatter(content: str) -> dict[str, str]:
    """Parse YAML frontmatter from a markdown file using regex (no PyYAML).

    Expects frontmatter delimited by --- at the start of the file.
    Handles simple key: value pairs only (no nested structures).

    Returns a dict of key-value pairs. Values are always strings.
    """
    # Match YAML frontmatter block at the start of the file
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    result: dict[str, str] = {}

    for line in frontmatter_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Match key: value (with optional quotes around value)
        kv_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)$', line)
        if kv_match:
            key = kv_match.group(1).strip()
            value = kv_match.group(2).strip()
            # Strip surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            result[key] = value

    return result


def _extract_metadata(filepath: Path, content: str) -> DesignDocMeta:
    """Extract metadata from a design document.

    Parses the YAML frontmatter and also tries to extract the title
    from the first # header if not present in frontmatter.
    """
    fm = _parse_frontmatter(content)

    # If title is not in frontmatter, try to get it from the first # header
    title = fm.get("title", "")
    if not title:
        # Look for first # header after frontmatter
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()

    return DesignDocMeta(
        filepath=str(filepath),
        filename=filepath.name,
        uuid=fm.get("uuid", ""),
        doc_type=fm.get("type", ""),
        status=fm.get("status", ""),
        title=title,
        author=fm.get("author", ""),
        date=fm.get("date", ""),
        raw_frontmatter=fm,
    )


# =============================================================================
# Search Functions
# =============================================================================


def _find_design_docs(design_dir: Path) -> list[Path]:
    """Find all .md files in the design directory recursively."""
    if not design_dir.exists():
        return []
    return sorted(design_dir.rglob("*.md"))


def _matches_query(doc: DesignDocMeta, content: str, query: str) -> bool:
    """Check if a document matches a text query (case-insensitive)."""
    query_lower = query.lower()
    # Search in title, filename, and full content
    return (
        query_lower in doc.title.lower()
        or query_lower in doc.filename.lower()
        or query_lower in content.lower()
    )


def search_design_docs(
    project_root: Path,
    query: str | None = None,
    doc_type: str | None = None,
    status: str | None = None,
    uuid_prefix: str | None = None,
) -> list[DesignDocMeta]:
    """Search design documents by various criteria.

    Args:
        project_root: Path to the project root directory
        query: Text keyword to search in title and content (case-insensitive)
        doc_type: Filter by document type (exact match, case-insensitive)
        status: Filter by document status (exact match, case-insensitive)
        uuid_prefix: Filter by UUID prefix match (case-insensitive)

    Returns:
        List of matching DesignDocMeta objects
    """
    design_dir = project_root / "design"
    docs = _find_design_docs(design_dir)
    results: list[DesignDocMeta] = []

    for doc_path in docs:
        try:
            content = doc_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        meta = _extract_metadata(doc_path, content)

        # Apply filters
        if doc_type and meta.doc_type.lower() != doc_type.lower():
            continue
        if status and meta.status.lower() != status.lower():
            continue
        if uuid_prefix and not meta.uuid.lower().startswith(uuid_prefix.lower()):
            continue
        if query and not _matches_query(meta, content, query):
            continue

        results.append(meta)

    return results


# =============================================================================
# Output Formatting
# =============================================================================


def _print_text_table(results: list[DesignDocMeta]) -> None:
    """Print results as a formatted text table."""
    if not results:
        print("No matching documents found.")
        return

    # Calculate column widths
    fn_width = max(len(r.filename) for r in results)
    fn_width = max(fn_width, 8)  # minimum width for "Filename" header
    type_width = max((len(r.doc_type) for r in results), default=4)
    type_width = max(type_width, 4)
    status_width = max((len(r.status) for r in results), default=6)
    status_width = max(status_width, 6)

    # Clamp widths to reasonable maximums
    fn_width = min(fn_width, 40)
    type_width = min(type_width, 15)
    status_width = min(status_width, 12)
    title_width = 40

    header = f"{'Filename':<{fn_width}}  {'Type':<{type_width}}  {'Status':<{status_width}}  {'Title':<{title_width}}"
    print(header)
    print("-" * len(header))

    for r in results:
        fn = r.filename[:fn_width]
        dtype = (r.doc_type or "-")[:type_width]
        st = (r.status or "-")[:status_width]
        title = (r.title or "-")[:title_width]
        print(f"{fn:<{fn_width}}  {dtype:<{type_width}}  {st:<{status_width}}  {title:<{title_width}}")

    print(f"\nFound {len(results)} document(s)")


def _print_json(results: list[DesignDocMeta]) -> None:
    """Print results as JSON array."""
    output = []
    for r in results:
        d = asdict(r)
        # Remove raw_frontmatter from default output to keep it clean
        d.pop("raw_frontmatter", None)
        output.append(d)
    print(json.dumps(output, indent=2))


# =============================================================================
# CLI
# =============================================================================


def _create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Search design documents by UUID, type, status, or keyword",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Text keyword to search in title and content",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Project root directory containing design/ (default: current directory)",
    )
    parser.add_argument(
        "--type",
        dest="doc_type",
        type=str,
        default=None,
        help="Filter by document type (e.g., pdr, spec, feature, decision, architecture, requirement, handoff)",
    )
    parser.add_argument(
        "--status",
        type=str,
        default=None,
        help="Filter by document status (e.g., draft, review, approved, rejected, superseded, archived)",
    )
    parser.add_argument(
        "--uuid",
        type=str,
        default=None,
        help="Filter by UUID prefix match",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    return parser


def main() -> int:
    """Main entry point."""
    args = _create_parser().parse_args()
    project_root = args.project_root.resolve()

    # Require at least one filter
    if not any([args.query, args.doc_type, args.status, args.uuid]):
        # No filter given -- show all documents
        pass

    design_dir = project_root / "design"
    if not design_dir.exists():
        print(f"ERROR: Design directory does not exist: {design_dir}", file=sys.stderr)
        return 1

    results = search_design_docs(
        project_root=project_root,
        query=args.query,
        doc_type=args.doc_type,
        status=args.status,
        uuid_prefix=args.uuid,
    )

    if args.output_format == "json":
        _print_json(results)
    else:
        _print_text_table(results)

    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
