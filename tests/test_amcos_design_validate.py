"""Real (non-mocked) unit tests for scripts/amcos_design_validate.py.

Every test imports the REAL validator module and calls its REAL functions with
real inputs. The file-level functions (parse_frontmatter, validate_document)
are exercised against real temporary .md files written via pytest's tmp_path —
no mocks, no monkeypatch, no fakes. These catch real regressions: a loosened
UUID regex, a status/type allow-list drift, a frontmatter parser that stops
raising on a missing delimiter, or a required-field check that silently passes.

Stdlib + pytest only, mirroring the plugin's zero-runtime-dependency policy.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# The validator lives in scripts/, which is not an importable package, so its
# directory is prepended to sys.path. scripts/ also holds amcos_output_utils,
# the validator's own sibling import, so this one insert satisfies both.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import amcos_design_validate as adv  # noqa: E402


def test_validate_uuid_accepts_every_valid_prefix() -> None:
    """validate_uuid returns None for a well-formed UUID under each allowed prefix."""
    for prefix in adv.VALID_UUID_PREFIXES:
        value = f"{prefix}-20260611-0001"
        assert adv.validate_uuid(value) is None, f"{value} should be valid"


def test_validate_uuid_rejects_bad_format_and_zero_sequence() -> None:
    """validate_uuid returns an error string for a bad prefix, malformed shape, or 0000 sequence."""
    # Unknown prefix -> format error.
    assert adv.validate_uuid("XXX-20260611-0001") is not None
    # Date part is not exactly 8 digits -> format error.
    assert adv.validate_uuid("REQ-2026-0001") is not None
    # Sequence part is not exactly 4 digits -> format error.
    assert adv.validate_uuid("REQ-20260611-1") is not None
    # Well-formed shape but the reserved 0000 sequence -> dedicated sequence error.
    seq_err = adv.validate_uuid("REQ-20260611-0000")
    assert seq_err is not None
    assert "0000" in seq_err


def test_validate_status_is_case_insensitive_and_rejects_unknown() -> None:
    """validate_status accepts every allowed value regardless of case and rejects an unknown one."""
    for status in adv.VALID_STATUSES:
        assert adv.validate_status(status) is None
        assert adv.validate_status(status.upper()) is None
    err = adv.validate_status("notarealstatus")
    assert err is not None
    assert "notarealstatus" in err


def test_validate_type_is_case_insensitive_and_rejects_unknown() -> None:
    """validate_type accepts every allowed value regardless of case and rejects an unknown one."""
    for type_value in adv.VALID_TYPES:
        assert adv.validate_type(type_value) is None
        assert adv.validate_type(type_value.capitalize()) is None
    err = adv.validate_type("blueprint")
    assert err is not None
    assert "blueprint" in err


def test_parse_frontmatter_reads_pairs_and_raises_on_missing_delimiters(tmp_path: Path) -> None:
    """parse_frontmatter parses quoted key:value pairs and raises ValueError when a delimiter is missing."""
    good = tmp_path / "good.md"
    good.write_text(
        '---\n'
        'uuid: REQ-20260611-0001\n'
        'title: "A Real Title"\n'
        "author: 'Emasoft'\n"
        '---\n'
        'Body text below the frontmatter.\n',
        encoding="utf-8",
    )
    parsed = adv.parse_frontmatter(str(good))
    assert parsed["uuid"] == "REQ-20260611-0001"
    assert parsed["title"] == "A Real Title"  # surrounding double quotes stripped
    assert parsed["author"] == "Emasoft"  # surrounding single quotes stripped

    # File that does not start with '---' on line 1 -> ValueError.
    no_open = tmp_path / "no_open.md"
    no_open.write_text("# Heading first\nuuid: REQ-20260611-0001\n", encoding="utf-8")
    with pytest.raises(ValueError):
        adv.parse_frontmatter(str(no_open))

    # Opening '---' with no closing '---' -> ValueError.
    no_close = tmp_path / "no_close.md"
    no_close.write_text("---\nuuid: REQ-20260611-0001\ntitle: Dangling\n", encoding="utf-8")
    with pytest.raises(ValueError):
        adv.parse_frontmatter(str(no_close))


def test_validate_dates_checks_format_and_ordering() -> None:
    """validate_dates returns no errors for valid ordered dates and flags bad format and updated-before-created."""
    # Valid: date-only and datetime forms, updated after created.
    assert adv.validate_dates("2026-06-10", "2026-06-11") == []
    assert adv.validate_dates("2026-06-11T08:00:00Z", "2026-06-11T09:00:00Z") == []
    # Equal dates are allowed (updated >= created).
    assert adv.validate_dates("2026-06-11", "2026-06-11") == []
    # Malformed 'updated' date -> at least one error mentioning the bad value.
    fmt_errors = adv.validate_dates("2026-06-11", "11/06/2026")
    assert fmt_errors
    assert any("11/06/2026" in e for e in fmt_errors)
    # updated strictly before created -> ordering error.
    order_errors = adv.validate_dates("2026-06-11", "2026-06-10")
    assert order_errors
    assert any("before" in e for e in order_errors)


def test_validate_document_passes_valid_and_fails_on_missing_field(tmp_path: Path) -> None:
    """validate_document returns [] for a fully valid document and a 'Missing required field' error when author is absent."""
    valid = tmp_path / "valid.md"
    valid.write_text(
        '---\n'
        'uuid: SPEC-20260611-0007\n'
        'title: Fully Valid Document\n'
        'type: specification\n'
        'status: approved\n'
        'created: 2026-06-10\n'
        'updated: 2026-06-11\n'
        'author: Emasoft\n'
        '---\n'
        'Document body.\n',
        encoding="utf-8",
    )
    assert adv.validate_document(str(valid)) == []

    # Same document with the required 'author' field removed -> validation fails.
    missing_author = tmp_path / "missing_author.md"
    missing_author.write_text(
        '---\n'
        'uuid: SPEC-20260611-0007\n'
        'title: Missing Author Document\n'
        'type: specification\n'
        'status: approved\n'
        'created: 2026-06-10\n'
        'updated: 2026-06-11\n'
        '---\n'
        'Document body.\n',
        encoding="utf-8",
    )
    errors = adv.validate_document(str(missing_author))
    assert errors
    assert any("author" in e for e in errors)
