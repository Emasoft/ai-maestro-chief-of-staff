"""Real (non-mocked) tests for scripts/validate_command.py.

These exercise the ACTUAL command validator: they import the real module and
call its real functions with real inputs. Where the function validates a file
on disk (`validate_command`), a real temp command `.md` is written via pytest's
`tmp_path` and the real file is read back by the validator. No mocks, no
monkeypatch, no fakes — every assertion is against the real ValidationReport
the functions produce.

Module lives in scripts/ (not an installed package), so we add scripts/ to
sys.path before importing it.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate_command as vc  # noqa: E402


def _write_command(tmp_path: Path, name: str, body: str) -> Path:
    """Write a real command .md file under tmp_path and return its path."""
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


def test_valid_command_file_passes(tmp_path: Path) -> None:
    """A well-formed command .md validates with no CRITICAL/MAJOR and EXIT_OK."""
    content = (
        "---\n"
        "name: my-command\n"
        "description: Do a useful thing for the user\n"
        "allowed-tools: Read, Write\n"
        "---\n\n"
        "You are running the my-command command. When invoked you should perform\n"
        "the requested task carefully and report the result back to the user.\n"
    )
    path = _write_command(tmp_path, "my-command.md", content)

    report = vc.validate_command(path)

    assert isinstance(report, vc.CommandValidationReport)
    assert report.has_critical is False
    assert report.has_major is False
    assert report.exit_code == vc.EXIT_OK
    assert report.command_path == str(path)


def test_unknown_frontmatter_field_is_flagged(tmp_path: Path) -> None:
    """An unrecognized frontmatter key produces a WARNING naming the unknown field."""
    content = (
        "---\n"
        "name: my-command\n"
        "description: Do a useful thing for the user\n"
        "totally-made-up-field: 123\n"
        "---\n\n"
        "You are running my-command. When invoked you should perform the task and\n"
        "report the outcome back to the user in a clear, concise manner.\n"
    )
    path = _write_command(tmp_path, "my-command.md", content)

    report = vc.validate_command(path)

    unknown_warnings = [
        r
        for r in report.results
        if r.level == "WARNING" and "Unknown frontmatter field" in r.message and "totally-made-up-field" in r.message
    ]
    assert len(unknown_warnings) == 1
    # An unknown field is a WARNING only — it must not block validation.
    assert report.has_critical is False


def test_allowed_tools_valid_list_passes() -> None:
    """A valid 'allowed-tools' list records a PASSED result and adds no MAJOR issue."""
    report = vc.CommandValidationReport(command_path="cmd.md")

    vc.validate_allowed_tools_field({"allowed-tools": ["Read", "Write", "Bash"]}, "cmd.md", report)

    passed = [r for r in report.results if r.level == "PASSED" and "'allowed-tools' field valid" in r.message]
    assert len(passed) == 1
    assert "3 tool(s)" in passed[0].message
    assert report.has_major is False


def test_allowed_tools_invalid_tool_is_flagged_major() -> None:
    """An unknown tool name in 'allowed-tools' produces a MAJOR 'Invalid tool pattern' issue."""
    report = vc.CommandValidationReport(command_path="cmd.md")

    vc.validate_allowed_tools_field({"allowed-tools": ["Read", "NotARealTool"]}, "cmd.md", report)

    major_issues = [
        r for r in report.results if r.level == "MAJOR" and "Invalid tool pattern" in r.message and "NotARealTool" in r.message
    ]
    assert len(major_issues) == 1
    assert report.has_major is True


def test_allowed_tools_empty_is_flagged_minor() -> None:
    """An empty 'allowed-tools' value yields a MINOR 'field is empty' note and no PASSED."""
    report = vc.CommandValidationReport(command_path="cmd.md")

    vc.validate_allowed_tools_field({"allowed-tools": ""}, "cmd.md", report)

    minor_issues = [r for r in report.results if r.level == "MINOR" and "'allowed-tools' field is empty" in r.message]
    assert len(minor_issues) == 1
    # Empty short-circuits before the per-tool validation, so nothing is PASSED.
    assert not any(r.level == "PASSED" for r in report.results)


def test_user_invocable_is_an_accepted_known_field(tmp_path: Path) -> None:
    """'user-invocable' is a known field, so a file using it raises no unknown-field WARNING."""
    assert "user-invocable" in vc.KNOWN_FRONTMATTER_FIELDS

    content = (
        "---\n"
        "name: my-command\n"
        "description: Do a useful thing for the user\n"
        "user-invocable: true\n"
        "---\n\n"
        "You are running my-command. When invoked you should perform the task and\n"
        "report the outcome back to the user in a clear, concise manner.\n"
    )
    path = _write_command(tmp_path, "my-command.md", content)

    report = vc.validate_command(path)

    unknown_for_user_invocable = [
        r for r in report.results if r.level == "WARNING" and "Unknown frontmatter field" in r.message and "user-invocable" in r.message
    ]
    assert unknown_for_user_invocable == []
