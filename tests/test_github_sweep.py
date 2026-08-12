"""Tests for the GitHub inbound sweep.

Every test here pins a failure that was MEASURED, not imagined: a hardcoded thread
list, a keyword filter that returned zero across eight repos, a typed watermark
that opened a five-day blind window, and an empty result reported as a clean inbox.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from amcos_github_sweep import (  # noqa: E402
    EPOCH,
    SELF_MARKER,
    SweepBroken,
    Thread,
    select_recent,
    select_repos,
    unread_after_watermark,
    verify_control,
)

T131 = Thread("ai-maestro", 131, "Every role-plugin persona says a forbidden send returns 403", "2026-08-12T10:32:21Z")
T20 = Thread("ai-maestro-chief-of-staff", 20, "Remove all direct /api/* calls from COS scripts", "2026-08-11T18:05:45Z")
OLD = Thread("ai-maestro", 9, "ancient", "2026-01-01T00:00:00Z")


def test_select_recent_keeps_a_thread_that_never_names_the_role() -> None:
    """The exact thread a keyword filter dropped must survive selection.

    ARCHITECT narrowed their sweep with `title ~ "[Aa]rchitect"` and got ZERO
    across 8 repos — dropping ai-maestro#131, which is addressed to them and is
    where the work originated, because its title does not contain their name. A
    keyword is a guess about wording; it fails exactly when someone writes ABOUT
    you without NAMING you, which is the normal case for a fleet-wide finding.
    """
    assert "chief-of-staff" not in T131.title.lower()  # the trap, made explicit
    assert "cos" not in T131.title.lower()
    kept = select_recent([T131, T20, OLD], since="2026-08-05")
    assert T131 in kept, "selection dropped a thread that does not name the role"
    assert T20 in kept
    assert OLD not in kept, "selection ignored the updatedAt property"


def test_select_recent_orders_newest_first() -> None:
    """Ordering is part of the contract — a reviewer reads the top of the list."""
    assert select_recent([OLD, T20, T131], since="2020-01-01") == [T131, T20, OLD]


def test_unread_is_empty_when_my_reply_is_the_latest_comment() -> None:
    """The watermark clears only when I actually replied — and then fully."""
    comments = [
        {"createdAt": "2026-08-12T09:00:00Z", "body": "a peer says something"},
        {"createdAt": "2026-08-12T10:00:00Z", "body": f"my answer\n_{SELF_MARKER}_"},
    ]
    assert unread_after_watermark(comments) == []


def test_a_thread_i_read_but_never_answered_stays_flagged() -> None:
    """Reading is not replying, and the sweep must not treat it as such.

    This is the five-day failure in miniature: a consolidated eleven-ruling mirror
    sat unread because a hand-typed watermark had already advanced past it. A
    derived watermark cannot skip — with no reply of mine after the inbound, it
    stays flagged until I answer.
    """
    comments = [
        {"createdAt": "2026-08-07T22:35:00Z", "body": "eleven rulings for COS"},
    ]
    unread = unread_after_watermark(comments)
    assert len(unread) == 1, "an unanswered inbound must remain flagged"


def test_watermark_defaults_to_epoch_so_a_thread_i_never_touched_is_all_unread() -> None:
    """No comment of mine ⇒ EPOCH ⇒ everything unread.

    The dangerous default is 'now': a thread I have never posted on would report
    zero unread and be indistinguishable from one I am current on. That is how a
    new thread addressed to me becomes invisible.
    """
    comments = [{"createdAt": "2026-08-01T00:00:00Z", "body": "hello COS"}]
    assert unread_after_watermark(comments) == comments
    assert EPOCH < "2026-08-01T00:00:00Z"


def test_verify_control_refuses_an_empty_enumeration() -> None:
    """Zero threads is a BROKEN INSTRUMENT, never a quiet inbox.

    A sweep returning zero has the same shape as a guard that cannot fail: no
    error, no output, no signal that anything is wrong. Reporting it as 'clean' is
    the failure; raising is the fix.
    """
    with pytest.raises(SweepBroken, match="ZERO threads"):
        verify_control([], "ai-maestro#131")


def test_verify_control_refuses_when_the_known_thread_is_missing() -> None:
    """ARCHITECT's rule, executable: find a thread you KNOW is there.

    A non-empty result is not proof the sweep works — it can still be dropping the
    one input that matters, which is precisely what the keyword filter did while
    returning other repos' issues.
    """
    with pytest.raises(SweepBroken, match="control thread"):
        verify_control([T20], "ai-maestro#131")


def test_verify_control_passes_when_the_known_thread_is_present() -> None:
    """The control must not red on a working sweep, or it gets deleted."""
    verify_control([T131, T20], "ai-maestro#131")


def test_repo_selection_never_gates_on_push_time() -> None:
    """A quiet repo with a loud issue tracker must survive selection.

    THE REGRESSION THIS PINS, measured 2026-08-12 and caught by --control an hour
    after this module shipped: repo selection filtered on `pushedAt > since`. Issue
    activity is INDEPENDENT of commit activity, and the repos most likely to carry a
    thread addressed to me are governance/spec repos — weeks between pushes, daily
    issue traffic. `ai-maestro` last pushed 08-08 while ai-maestro#131 was updated
    08-12, so a narrow `--since` dropped the most important repo in the fleet before
    a single issue was listed: 5 repos survived out of 21.

    The nastiest property was that it PASSED on a wide window (--since 08-05 predates
    the 08-08 push) and failed only on a narrow one — the normal incremental sweep.
    A defect that hides during the first check you would naturally run.
    """
    records = [
        {"name": "ai-maestro", "pushedAt": "2026-08-08T15:01:30Z", "hasIssuesEnabled": True, "isArchived": False},
        {"name": "archived-thing", "pushedAt": "2026-08-12T00:00:00Z", "hasIssuesEnabled": True, "isArchived": True},
        {"name": "no-issues", "pushedAt": "2026-08-12T00:00:00Z", "hasIssuesEnabled": False, "isArchived": False},
    ]
    selected = select_repos(records)
    assert "ai-maestro" in selected, "a repo with a stale pushedAt but live issues was dropped — selection is gating on commit activity again, which is not what an inbound thread needs"
    assert "archived-thing" not in selected, "archived repos cannot receive new threads"
    assert "no-issues" not in selected, "a repo with issues disabled cannot hold one"


def test_repo_selection_defaults_to_including_a_repo_on_missing_fields() -> None:
    """Fail OPEN on unknown repo metadata — an over-broad sweep is recoverable.

    If `hasIssuesEnabled` is absent from a future gh payload, the safe default is to
    INCLUDE the repo. Excluding on a missing field is how a schema change silently
    empties an inbox, and the failure is invisible; including one extra repo costs a
    listing call and is obvious in the output.
    """
    assert select_repos([{"name": "unknown-shape"}]) == ["unknown-shape"]


def test_sweep_broken_is_not_confusable_with_a_clean_result() -> None:
    """The type distinction is the point: only a crash gets investigated.

    A broken sweep that returns [] is worse than one that raises, because the
    empty list flows onward as an inbox state. Pinning the type stops a future
    edit from 'helpfully' catching SweepBroken and returning [] instead.
    """
    assert issubclass(SweepBroken, RuntimeError)
    with pytest.raises(SweepBroken):
        verify_control([], "")
