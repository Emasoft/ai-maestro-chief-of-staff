#!/usr/bin/env python3
"""ECOS Design Document YAML Frontmatter Validator.

Validates YAML frontmatter in markdown design documents for the ECOS plugin.
Uses ONLY Python stdlib -- no PyYAML or external dependencies required.

Usage:
    python ecos_design_validate.py PATH [--verbose] [--format {text,json}]

Exit codes:
    0 - All validated documents are valid
    1 - One or more documents have errors, no .md files found, or path does not exist
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# All fields that MUST be present in the frontmatter
REQUIRED_FIELDS = ("uuid", "title", "type", "status", "created", "updated", "author")

# Allowed prefixes for the UUID format: PREFIX-YYYYMMDD-NNNN
VALID_UUID_PREFIXES = ("REQ", "SPEC", "ARCH", "PDR", "HAND", "MEM", "DEC", "GUUID")

# Regex that matches the full UUID format (prefix is one of VALID_UUID_PREFIXES,
# date part is exactly 8 digits, sequence part is exactly 4 digits)
UUID_PATTERN = re.compile(
    r"^(" + "|".join(VALID_UUID_PREFIXES) + r")-(\d{8})-(\d{4})$"
)

# Valid status values (compared case-insensitively)
VALID_STATUSES = {
    "draft",
    "review",
    "approved",
    "implementing",
    "completed",
    "archived",
    "implemented",
    "deprecated",
    "rejected",
}

# Valid type values (compared case-insensitively)
VALID_TYPES = {
    "requirement",
    "specification",
    "architecture",
    "handoff",
    "memory",
    "decision",
}

# ISO 8601 date patterns: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ
DATE_ONLY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


# ---------------------------------------------------------------------------
# Frontmatter Parsing (stdlib only, no PyYAML)
# ---------------------------------------------------------------------------


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file.

    The file must start with '---' on the very first line, and have a closing
    '---' on a subsequent line. Between them, each non-empty line is treated
    as 'key: value'. Quoted values (single or double) are unquoted.

    Returns:
        A dict of key-value pairs if frontmatter is found and well-formed.

    Raises:
        ValueError: If the file has no frontmatter, frontmatter doesn't start
                    on line 1, or the closing delimiter is missing.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError("No frontmatter found (file must start with '---' on line 1)")

    # Find closing ---
    closing_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_index = i
            break

    if closing_index is None:
        raise ValueError("Unclosed frontmatter (missing closing '---')")

    # Parse key: value pairs between the delimiters
    frontmatter = {}
    for line in lines[1:closing_index]:
        stripped = line.strip()
        if not stripped:
            continue
        # Split on first colon only
        colon_pos = stripped.find(":")
        if colon_pos == -1:
            continue
        key = stripped[:colon_pos].strip().lower()
        value = stripped[colon_pos + 1 :].strip()
        # Strip surrounding quotes (single or double)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        frontmatter[key] = value

    return frontmatter


# ---------------------------------------------------------------------------
# Validation Functions
# ---------------------------------------------------------------------------


def validate_uuid(value):
    """Validate UUID format: PREFIX-YYYYMMDD-NNNN.

    Returns an error message string if invalid, or None if valid.
    """
    match = UUID_PATTERN.match(value)
    if not match:
        return f"Invalid uuid format: '{value}' (expected PREFIX-YYYYMMDD-NNNN with prefix in {VALID_UUID_PREFIXES})"
    sequence = match.group(3)
    if sequence == "0000":
        return f"Invalid uuid sequence: '{value}' (sequence must be >= 0001, got 0000)"
    return None


def validate_status(value):
    """Validate status field against allowed values (case-insensitive).

    Returns an error message string if invalid, or None if valid.
    """
    if value.lower() not in VALID_STATUSES:
        return f"Invalid status '{value}' (must be one of: {', '.join(sorted(VALID_STATUSES))})"
    return None


def validate_type(value):
    """Validate type field against allowed values (case-insensitive).

    Returns an error message string if invalid, or None if valid.
    """
    if value.lower() not in VALID_TYPES:
        return f"Invalid type '{value}' (must be one of: {', '.join(sorted(VALID_TYPES))})"
    return None


def parse_date(value):
    """Parse a date string in ISO 8601 format.

    Accepts YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ.

    Returns:
        A datetime object if the value is a valid date.

    Raises:
        ValueError: If the date format or value is invalid.
    """
    if DATE_ONLY_PATTERN.match(value):
        return datetime.strptime(value, "%Y-%m-%d")
    elif DATETIME_PATTERN.match(value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    else:
        raise ValueError(
            f"Invalid date format: '{value}' (expected YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)"
        )


def validate_dates(created_str, updated_str):
    """Validate created and updated date fields.

    Checks format validity and that updated >= created.

    Returns a list of error message strings (empty list if all valid).
    """
    errors = []
    created_dt = None
    updated_dt = None

    try:
        created_dt = parse_date(created_str)
    except ValueError as exc:
        errors.append(f"Invalid 'created' date: {exc}")

    try:
        updated_dt = parse_date(updated_str)
    except ValueError as exc:
        errors.append(f"Invalid 'updated' date: {exc}")

    if created_dt is not None and updated_dt is not None:
        if updated_dt < created_dt:
            errors.append(
                f"'updated' date ({updated_str}) is before 'created' date ({created_str})"
            )

    return errors


def validate_document(filepath):
    """Validate a single markdown document's frontmatter.

    Returns a list of error message strings (empty list means valid).
    """
    errors = []

    # Parse frontmatter
    try:
        frontmatter = parse_frontmatter(filepath)
    except ValueError as exc:
        return [str(exc)]

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter or not frontmatter[field]:
            errors.append(f"Missing required field: {field}")

    # If required fields are missing, skip further validation on those fields
    if errors:
        return errors

    # Validate uuid
    uuid_error = validate_uuid(frontmatter["uuid"])
    if uuid_error:
        errors.append(uuid_error)

    # Validate status
    status_error = validate_status(frontmatter["status"])
    if status_error:
        errors.append(status_error)

    # Validate type
    type_error = validate_type(frontmatter["type"])
    if type_error:
        errors.append(type_error)

    # Validate dates
    date_errors = validate_dates(frontmatter["created"], frontmatter["updated"])
    errors.extend(date_errors)

    return errors


# ---------------------------------------------------------------------------
# File Discovery
# ---------------------------------------------------------------------------


def find_md_files(path):
    """Find all .md files at the given path.

    If path is a file, returns a list containing just that file.
    If path is a directory, recursively finds all .md files.

    Returns a sorted list of absolute file paths.

    Raises:
        FileNotFoundError: If the path does not exist.
        ValueError: If a directory contains no .md files.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")

    if os.path.isfile(path):
        return [os.path.abspath(path)]

    # Directory: walk recursively
    md_files = []
    for root, _, files in os.walk(path):
        for fname in files:
            if fname.endswith(".md"):
                md_files.append(os.path.abspath(os.path.join(root, fname)))

    if not md_files:
        raise ValueError(f"No .md files found in directory: {path}")

    return sorted(md_files)


# ---------------------------------------------------------------------------
# Output Formatting
# ---------------------------------------------------------------------------


def format_text(results, verbose=False):
    """Format validation results as human-readable text.

    Args:
        results: List of (filepath, errors_list) tuples.
        verbose: If True, show passing files as well.

    Returns:
        A formatted string.
    """
    total = len(results)
    passed = sum(1 for _, errs in results if not errs)
    failed = total - passed

    lines = [f"Validated {total} file(s): {passed} passed, {failed} failed."]

    for filepath, errs in results:
        if errs:
            for err in errs:
                lines.append(f"  [FAIL] {filepath}: {err}")
        elif verbose:
            lines.append(f"  [PASS] {filepath}")

    return "\n".join(lines) + "\n"


def format_json(results):
    """Format validation results as a JSON string.

    Args:
        results: List of (filepath, errors_list) tuples.

    Returns:
        A JSON-formatted string.
    """
    total = len(results)
    passed = sum(1 for _, errs in results if not errs)
    failed = total - passed

    error_entries = []
    for filepath, errs in results:
        for err in errs:
            error_entries.append({"file": filepath, "error": err})

    output = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": error_entries,
    }
    return json.dumps(output, indent=2) + "\n"


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------


def main():
    """Main entry point for the CLI validator."""
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter in ECOS design documents.",
        epilog="Exit code 0 means all documents are valid; 1 means errors were found.",
    )
    parser.add_argument(
        "path",
        metavar="PATH",
        help="Path to a single .md file or a directory to scan recursively.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Show extra details on passing files.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="output_format",
        help="Output format (default: text).",
    )

    args = parser.parse_args()

    # Discover files
    try:
        md_files = find_md_files(args.path)
    except (FileNotFoundError, ValueError) as exc:
        if args.output_format == "json":
            output = {"total": 0, "passed": 0, "failed": 0, "errors": [{"file": args.path, "error": str(exc)}]}
            sys.stdout.write(json.dumps(output, indent=2) + "\n")
        else:
            sys.stdout.write(f"ERROR: {exc}\n")
        sys.exit(1)

    # Validate each file
    results = []
    for filepath in md_files:
        errors = validate_document(filepath)
        results.append((filepath, errors))

    # Format and print output
    if args.output_format == "json":
        sys.stdout.write(format_json(results))
    else:
        sys.stdout.write(format_text(results, verbose=args.verbose))

    # Determine exit code: 0 if all passed, 1 if any failed
    has_failures = any(errs for _, errs in results)
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
