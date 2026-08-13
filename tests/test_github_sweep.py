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
    ControlStale,
    SweepBroken,
    Thread,
    acknowledge_through,
    load_acks,
    needs_attention,
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


def test_a_control_outside_the_window_is_a_STALE_CONTROL_not_a_broken_sweep() -> None:
    """Name the right culprit — the invocation, not the instrument.

    MEASURED 2026-08-13: `--since 2026-08-12T12:00:00Z --control ai-maestro#131`
    reported "the sweep is dropping inputs silently". The sweep was perfect — it
    found 9 threads, all correct — and #131 had simply last moved at 11:48:33Z,
    twelve minutes before the window, so it could not appear.

    That diagnostic is this module's own defect one level up: a check that fires
    correctly but blames the wrong thing sends the next reader hunting a
    nonexistent bug, and the first thing they do is distrust a working sweep. The
    unfiltered enumeration is what separates the two cases, which is why
    `enumerate_threads` no longer narrows.
    """
    inwindow = [T131]
    enumerated = [T131, T20]  # T20 is older than the window below
    with pytest.raises(ControlStale, match="OUTSIDE the --since window"):
        verify_control(inwindow, T20.ref, enumerated)


def test_a_control_in_neither_list_is_still_a_broken_sweep() -> None:
    """The stale-control branch must not swallow the real failure it sits beside.

    A control absent from the UNFILTERED enumeration too was never narrowed away —
    it was dropped. That is the original defect and must still raise SweepBroken,
    or adding the friendlier diagnostic would have quietly disarmed the gate.
    """
    with pytest.raises(SweepBroken, match="dropping inputs silently"):
        verify_control([T131], "ai-maestro#999999", [T131, T20])


def test_stale_control_and_broken_sweep_are_different_types() -> None:
    """Callers must be able to branch: fix your invocation vs distrust the output.

    Same reason SweepBroken is not a bare RuntimeError — collapsing two outcomes
    with opposite remedies into one type is how the wrong remedy gets applied.
    """
    assert not issubclass(ControlStale, SweepBroken)
    assert not issubclass(SweepBroken, ControlStale)


def test_omitting_the_enumeration_keeps_the_conservative_old_behaviour() -> None:
    """Without the unfiltered list the two cases are indistinguishable — over-blame.

    A caller that cannot supply the enumeration gets the pre-existing verdict: any
    missing control is a broken sweep. Over-blaming is the safe direction; the
    unsafe one is reporting a clean inbox that was never verified.
    """
    with pytest.raises(SweepBroken, match="dropping inputs silently"):
        verify_control([T131], T20.ref)


def test_my_LEGACY_byline_still_counts_as_mine() -> None:
    """The watermark is derived from my own comments — a form it cannot see is fatal.

    MEASURED 2026-08-13 across my own tracker: 32 of my comments carry ONLY the
    legacy "This is the Claude responsible for…" line and 8 only the current
    trailer. The single-literal marker was therefore blind to the MAJORITY of my
    own history, and five threads reported my own latest comment as needing
    attention — including ai-maestro-chief-of-staff#22, whose "unread" comment I
    had written myself.

    A watermark that cannot recognise its own author does not merely miscount: on a
    thread where every reply of mine predates the byline change it falls back to
    EPOCH and reports the WHOLE thread unread, forever.
    """
    legacy = [{"createdAt": "2026-06-20T17:52:26Z", "body": "This is the Claude responsible for the ai-maestro-chief-of-staff project. ## Verified verb-by-verb"}]
    assert unread_after_watermark(legacy) == [], "my own legacy-byline comment read as unread"
    byline_only = [{"createdAt": "2026-08-13T00:00:00Z", "body": "_Posted by the Claude developing **ai-maestro-chief-of-staff** (the CHIEF-OF-STAFF role)._\n\nbody"}]
    assert unread_after_watermark(byline_only) == [], "my current byline without the trailer read as unread"


def test_a_peer_QUOTING_my_trailer_does_not_advance_my_watermark() -> None:
    """THE SAFETY PROPERTY — the watermark must not be advanceable by impersonation.

    The derived watermark cannot skip by being TYPED, which is why it replaced a
    hand-typed one. But `marker in body` lets it skip by being QUOTED: a peer who
    quotes my byline or trailer counts as me, advancing the watermark past THEIR
    OWN comment and hiding it. Same five-day blind window, rebuilt out of different
    parts — and this one arrives from outside, so no discipline of mine prevents it.

    Peers on ai-maestro#131 quote me routinely, so this is not hypothetical.
    """
    peer = [{
        "createdAt": "2026-08-13T09:00:00Z",
        "body": (
            "_Posted by the Claude developing **ai-maestro-architect-agent**._\n\n"
            "> Your four collocations are all `>`-free.\n"
            "> _Agent: ai-maestro-chief-of-staff_\n\n"
            "Adopted, and here is the measurement you asked for."
        ),
    }]
    assert unread_after_watermark(peer) == peer, "a peer quoting my trailer was counted as ME, hiding their own comment — the blind window, rebuilt"


def test_an_acknowledged_thread_stops_counting_as_needing_attention() -> None:
    """A derived watermark cannot say "read, and deliberately not answering".

    It clears only on my reply — the property that makes it unable to SKIP — so a
    thread I consciously pass on stays flagged forever. Measured on my own inbox
    2026-08-13: ai-maestro#145 sat at `unread=6` after I judged that exchange not
    mine to join, permanently. A count that includes items needing no action stops
    meaning "needs attention", which is this module's own defect one level up: a
    number that cannot distinguish two states.
    """
    comments = [
        {"createdAt": "2026-08-12T22:54:10Z", "body": "peer measurement"},
        {"createdAt": "2026-08-12T23:05:36Z", "body": "peer follow-up"},
    ]
    unread = unread_after_watermark(comments)
    assert len(unread) == 2, "precondition: with no reply of mine, both are unread"
    assert needs_attention(unread, "2026-08-12T23:05:36Z") == [], "acknowledging through the newest comment must clear the flag without a reply"


def test_acknowledging_cannot_hide_a_LATER_comment() -> None:
    """THE SAFETY PROPERTY — an ack must not reintroduce the blind window.

    The original defect this module exists for was a HAND-TYPED watermark: I typed
    a time later than what I had actually read and a consolidated eleven-ruling
    mirror sat unseen for five days. An ack is only ever set to the timestamp of a
    comment the tool just DISPLAYED, so it cannot cover anything unseen — and
    anything arriving afterwards is strictly greater and still surfaces.

    If this test ever fails, the acknowledgment layer has become the typed
    watermark wearing different clothes, and it must be removed rather than fixed.
    """
    acked = "2026-08-12T23:05:36Z"
    later = [{"createdAt": "2026-08-13T01:54:55Z", "body": "a reply that needs me"}]
    assert needs_attention(later, acked) == later, "a comment newer than the ack was hidden — this is the five-day blind window, reintroduced"


def test_acks_never_move_backwards() -> None:
    """Monotonic, so a stale caller cannot silently re-open a settled decision."""
    acks = acknowledge_through({}, "ai-maestro#145", "2026-08-13T00:35:46Z")
    acks = acknowledge_through(acks, "ai-maestro#145", "2026-08-12T22:54:10Z")  # older
    assert acks["ai-maestro#145"] == "2026-08-13T00:35:46Z", "an older ack overwrote a newer one; re-acking must be idempotent, never a regression"
    assert acknowledge_through({}, "x#1", EPOCH)["x#1"] == EPOCH


def test_an_unreadable_acks_file_acknowledges_NOTHING(tmp_path) -> None:
    """Fail toward "everything still needs attention", never toward a clear inbox.

    A corrupt or absent state file must not read as "all handled" — that is a
    silent, self-clearing inbox, the worst failure this tool can have.
    """
    corrupt = tmp_path / "acks.json"
    corrupt.write_text("{not json", encoding="utf-8")
    assert load_acks(corrupt) == {}
    assert load_acks(tmp_path / "does-not-exist.json") == {}


def test_sweep_broken_is_not_confusable_with_a_clean_result() -> None:
    """The type distinction is the point: only a crash gets investigated.

    A broken sweep that returns [] is worse than one that raises, because the
    empty list flows onward as an inbox state. Pinning the type stops a future
    edit from 'helpfully' catching SweepBroken and returning [] instead.
    """
    assert issubclass(SweepBroken, RuntimeError)
    with pytest.raises(SweepBroken):
        verify_control([], "")
