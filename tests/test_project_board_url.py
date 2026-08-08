"""Real unit tests for the project-board URL parse (TRDD-6SL6UY6N / ai-maestro#133).

These exercise the PURE parse — `_parse_project_board_url` — which needs no
server, no CLI, and no auth. Nothing here is mocked: the function is total over
its input and returns a plain tuple, so the tests call the real thing.

The load-bearing assertions are the NEGATIVE ones. A test that checks `owner`
and `number` came out right passes just as happily when a fabricated `repo`
rides along beside them, and a fabricated repo is exactly the defect
ai-maestro#133 removed from the server UI (`repo = owner`): it produces a link
that validates and then points at a repo-scoped board that does not exist. So
every org/user-board case asserts `repo IS None` explicitly.

Stdlib + pytest only (the plugin declares zero runtime dependencies).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# The scripts live alongside the package; add to path like run-all-tests.py does.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from amcos_team_registry import _parse_project_board_url  # noqa: E402


class TestRepoScopedBoard:
    """A /<owner>/<repo>/projects/<n> URL keeps its repo — full task CRUD."""

    def test_repo_scoped_url_yields_all_three_fields(self) -> None:
        """A repo-scoped board URL parses to (owner, number, repo) with the repo kept."""
        owner, number, repo = _parse_project_board_url(
            "https://github.com/Emasoft/ai-maestro/projects/12"
        )
        assert owner == "Emasoft"
        assert number == 12
        assert repo == "ai-maestro"

    def test_number_is_an_int_not_a_string(self) -> None:
        """The board number is returned as int, since the server schema demands a JSON number."""
        _, number, _ = _parse_project_board_url(
            "https://github.com/Emasoft/ai-maestro/projects/7"
        )
        assert isinstance(number, int)
        assert not isinstance(number, str)

    def test_scheme_and_host_are_optional(self) -> None:
        """A bare github.com/... form parses identically to the https:// form."""
        assert _parse_project_board_url(
            "github.com/Emasoft/ai-maestro/projects/3"
        ) == _parse_project_board_url(
            "https://github.com/Emasoft/ai-maestro/projects/3"
        )


class TestOrgAndUserBoards:
    """An org/user board is browse-only, and its repo must stay ABSENT."""

    @pytest.mark.parametrize("kind", ["orgs", "users"])
    def test_org_board_returns_repo_none(self, kind: str) -> None:
        """An org/user board parses to (owner, number) with repo None — never fabricated."""
        owner, number, repo = _parse_project_board_url(
            f"https://github.com/{kind}/Emasoft/projects/12"
        )
        assert owner == "Emasoft"
        assert number == 12
        # THE assertion this file exists for. Checking owner/number alone would
        # pass with a fabricated repo sitting beside them.
        assert repo is None, (
            f"repo must be None for an {kind} board — got {repo!r}. A fabricated "
            "repo promotes a browse-only board to CRUD-capable and points at a "
            "repo-scoped board that does not exist (ai-maestro#133)."
        )

    @pytest.mark.parametrize("kind", ["orgs", "users"])
    def test_org_owner_is_not_the_literal_prefix(self, kind: str) -> None:
        """The org/user branch must win over the repo-scoped branch, which it also matches.

        Both shapes are 4 segments with "projects" at index 2, so if the
        repo-scoped test ran first an org board would parse as owner="orgs" with
        repo=<the real owner> — a link that validates and points nowhere.
        """
        owner, _, repo = _parse_project_board_url(
            f"https://github.com/{kind}/Emasoft/projects/12"
        )
        assert owner != kind, f"owner parsed as the literal {kind!r} prefix"
        assert owner == "Emasoft"
        assert repo != "Emasoft", "the owner leaked into the repo slot"


class TestMalformedInputFailsLoudly:
    """No silent drop and no guessing — a bad URL raises."""

    @pytest.mark.parametrize(
        "bad",
        [
            "https://github.com/Emasoft/ai-maestro",          # a repo, not a board
            "https://github.com/Emasoft/ai-maestro/issues/5",  # wrong collection
            "https://github.com/Emasoft/projects/12",          # too few segments
            "https://github.com/orgs/Emasoft/projects",        # no number
            "",
            "not a url at all",
        ],
    )
    def test_unparseable_url_raises(self, bad: str) -> None:
        """A URL that names no board raises ValueError rather than yielding a partial link."""
        with pytest.raises(ValueError):
            _parse_project_board_url(bad)

    @pytest.mark.parametrize("bad_number", ["0", "-1", "abc", "1.5"])
    def test_non_positive_or_non_numeric_board_number_raises(self, bad_number: str) -> None:
        """A board number that is not a positive integer raises, matching the server's min(1)."""
        with pytest.raises(ValueError):
            _parse_project_board_url(
                f"https://github.com/Emasoft/ai-maestro/projects/{bad_number}"
            )
