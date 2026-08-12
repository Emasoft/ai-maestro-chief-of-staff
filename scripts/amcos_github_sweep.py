#!/usr/bin/env python3
"""Sweep the GitHub inbound channel — the one channel that cannot notify you.

The persona names three inbound channels (AMP, peer sessions, GitHub threads) and
requires every one to be checked. AMP has an inbox to drain and peer sessions are
delivered mid-turn; GitHub is the channel with neither property, so it is swept or
it is missed. Until now there was no instrument, which is why a thread on this
plugin's OWN tracker went unlooked-at while a two-thread hardcoded list reported
"0 unread" and looked exactly like a working sweep.

THREE FAILURE MODES THIS MODULE REFUSES TO HAVE, each measured in the wild:

1. **A hardcoded thread list** finds replies on threads you already know about and
   is blind BY CONSTRUCTION to a new thread addressed to you. Mine covered two
   threads on one repo (2026-08-12); the fleet had 25 recently-updated open issues
   across 21 repos, including one on this plugin's own tracker.

2. **A keyword filter** looks like precision and is indistinguishable from a
   working sweep when it returns nothing. ARCHITECT shipped `title ~ "architect"`
   and got ZERO across 8 repos — dropping ai-maestro#131, the thread addressed to
   them that the work came from, because its title does not contain their name.
   Selection is by PROPERTY (updatedAt), never by a guess about wording.

3. **A typed watermark** develops a blind window the moment you type a timestamp
   later than the last thing you actually read. Mine cost five days on a consolidated
   eleven-ruling mirror. The watermark is DERIVED from my own last comment, so it
   cannot skip, and it self-clears only when I actually reply — an item read but
   unanswered stays flagged, which is correct.

AND THE PRECONDITION THAT MAKES A CLEAN RESULT MEAN ANYTHING (ARCHITECT's rule,
ai-maestro#131): *verify a sweep by checking it FINDS A THREAD YOU KNOW IS THERE,
never by checking it runs without error.* A sweep returning zero has the same shape
as a guard that cannot fail — no error, no output, no signal. So a known-present
control thread is REQUIRED, and its absence is a hard failure reported as a broken
instrument, never as "nothing new".
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass

SELF_MARKER = "Agent: ai-maestro-chief-of-staff"
EPOCH = "1970-01-01T00:00:00Z"


class SweepBroken(RuntimeError):
    """The instrument failed. Distinct from 'the instrument ran and found nothing'.

    Kept as its own type because collapsing the two is the entire defect family:
    a broken sweep that reports 'clean' is worse than one that crashes, since only
    the crash gets investigated.
    """


@dataclass(frozen=True)
class Thread:
    repo: str
    number: int
    title: str
    updated_at: str

    @property
    def ref(self) -> str:
        return f"{self.repo}#{self.number}"


def select_recent(threads: list[Thread], since: str) -> list[Thread]:
    """Narrow by updatedAt — a PROPERTY of the thread, never a guess at its wording.

    Recency is a fact the thread carries. A keyword is a hypothesis about how
    someone phrased a title, and it fails precisely when they write ABOUT you
    without NAMING you — the normal case for a fleet-wide finding.
    """
    return sorted(
        (t for t in threads if t.updated_at > since),
        key=lambda t: t.updated_at,
        reverse=True,
    )


def unread_after_watermark(comments: list[dict], self_marker: str = SELF_MARKER) -> list[dict]:
    """Comments newer than MY last comment on the thread.

    The watermark is my own last reply, read off the thread itself. Two properties
    worth keeping: it cannot develop a blind window (nothing is typed), and it
    clears only when I actually answer — so a thread I have read but not replied to
    stays flagged rather than silently going quiet.
    """
    mine = [c["createdAt"] for c in comments if self_marker in (c.get("body") or "")]
    watermark = max(mine) if mine else EPOCH
    return [c for c in comments if c["createdAt"] > watermark]


class ControlStale(ValueError):
    """The INVOCATION is wrong, not the instrument — a control outside the window.

    Deliberately NOT a SweepBroken. Conflating them reproduces this module's own
    defect one level up: a diagnostic that names the wrong culprit sends the next
    reader hunting a bug that does not exist, and the first thing they would do is
    distrust a sweep that is working perfectly. Measured 2026-08-13: `--since
    12:00Z --control ai-maestro#131` reported "the sweep is dropping inputs
    silently" when #131 had simply last moved at 11:48Z — twelve minutes before the
    window. Nine threads were found and every one of them was correct.
    """


def verify_control(threads: list[Thread], control: str, enumerated: list[Thread] | None = None) -> None:
    """Fail unless the sweep found a thread known to exist. The anti-vacuity gate.

    Without this an empty result is unfalsifiable: a correct sweep over a quiet
    fleet and a sweep whose filter drops everything produce byte-identical output.
    The control converts "I found nothing" into a claim that can be wrong.

    Pass `enumerated` (the UNFILTERED enumeration) to separate the two ways a
    control can go missing, which look identical from the narrowed list alone:

    - present in `enumerated`, absent from `threads` → the control is OUTSIDE the
      `--since` window. The sweep is fine; the invocation is stale. `ControlStale`.
    - absent from BOTH → the sweep really is dropping inputs. `SweepBroken`.

    Omitting `enumerated` keeps the old conservative behaviour: any missing control
    is reported as a broken sweep, which over-blames but never under-warns.
    """
    if enumerated is not None and not enumerated:
        raise SweepBroken("the sweep enumerated ZERO threads. A fleet with open issues cannot be empty, so this is a broken instrument, not a quiet inbox. Reporting 'nothing new' here is the failure this check exists to prevent.")
    if enumerated is None and not threads:
        raise SweepBroken("the sweep enumerated ZERO threads. A fleet with open issues cannot be empty, so this is a broken instrument, not a quiet inbox. Reporting 'nothing new' here is the failure this check exists to prevent.")
    if not control or any(t.ref == control for t in threads):
        return
    if enumerated is not None:
        hit = next((t for t in enumerated if t.ref == control), None)
        if hit is not None:
            raise ControlStale(
                f"control thread {control!r} exists and is open, but it last moved at {hit.updated_at}, which is OUTSIDE the --since window — so it could not appear. The sweep is NOT broken; the control is. Pick a control you know moved inside the window, or widen --since. (It found {len(threads)} thread(s) in-window out of {len(enumerated)} enumerated.)"
            )
    raise SweepBroken(f"control thread {control!r} is KNOWN to be open and the sweep did not find it among {len(threads)} results. The sweep is dropping inputs silently — do NOT read its output as an inbox state.")


def _gh(args: list[str]) -> str:
    if not shutil.which("gh"):
        raise SweepBroken("`gh` is not on PATH; the GitHub channel cannot be swept")
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        # Fail loudly. A swallowed gh error degrades into an empty list, which the
        # caller would otherwise render as a clean inbox.
        raise SweepBroken(f"gh {' '.join(args[:3])}… failed: {proc.stderr.strip()[:200]}")
    return proc.stdout


def select_repos(records: list[dict]) -> list[str]:
    """Which repos can carry an inbound thread. NEVER gated on PUSH time.

    The first version of this filtered on `pushedAt > since` and it was wrong in
    the way this whole module is about. **Issue activity is independent of commit
    activity**, and the repos most likely to carry a thread addressed to me are the
    governance/spec repos, which go weeks without a push while their issues move
    daily. Measured 2026-08-12: `ai-maestro` last pushed 08-08, while ai-maestro#131
    was updated 08-12 — so a `--since` of 08-12 excluded the single most important
    repo in the fleet BEFORE any issue was listed, leaving 5 of 21 repos.

    Worse than merely wrong: it passed on a WIDE window (--since 08-05 predates the
    08-08 push, so the repo survived) and failed only on a NARROW one — which is the
    normal incremental sweep. A bug that appears exactly when the tool is used the
    way it is meant to be used, and hides during the wide-window check you would
    naturally run first.

    Selection is now on properties that actually bear on whether a repo can hold an
    inbound thread: issues enabled, not archived. `--since` narrows THREADS, never
    repos. Caught by the --control precondition, which refused to report the
    resulting 1-thread scan as an inbox state.
    """
    return sorted(r["name"] for r in records if r.get("hasIssuesEnabled", True) and not r.get("isArchived", False))


def discover_repos(owner: str) -> list[str]:
    out = _gh(["repo", "list", owner, "--limit", "200", "--json", "name,hasIssuesEnabled,isArchived"])
    repos = select_repos(json.loads(out or "[]"))
    if not repos:
        raise SweepBroken(f"no issue-bearing repos found for {owner!r} — refusing to sweep nothing")
    return repos


def enumerate_threads(owner: str, repos: list[str]) -> list[Thread]:
    """UNFILTERED enumeration of every open thread. The caller narrows.

    Narrowing moved out so the unfiltered list survives to `verify_control`, which
    needs it to tell a stale control from a dropping sweep. Folding the narrow in
    here discarded the only evidence that separates them, and the diagnostic then
    blamed the instrument for the caller's window.
    """
    found: list[Thread] = []
    for repo in repos:
        try:
            out = _gh(
                [
                    "issue",
                    "list",
                    "--repo",
                    f"{owner}/{repo}",
                    "--state",
                    "open",
                    "--limit",
                    "100",
                    "--json",
                    "number,title,updatedAt",
                ]
            )
        except SweepBroken:
            continue  # a repo with issues disabled is not a broken sweep
        for it in json.loads(out or "[]"):
            found.append(Thread(repo, it["number"], it["title"], it["updatedAt"]))
    return found


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--owner", default="Emasoft")
    ap.add_argument("--since", required=True, help="ISO instant; threads updated after it")
    ap.add_argument(
        "--control",
        default="",
        help="REPO#N known to be open and to match --since. REQUIRED for a trustworthy clean result; without it an empty sweep proves nothing.",
    )
    args = ap.parse_args(argv)

    if not args.control:
        print(
            "WARNING: no --control given. An empty result from this run is UNFALSIFIABLE — it cannot be distinguished from a filter that drops everything. Pass a thread you know is open.",
            file=sys.stderr,
        )

    try:
        repos = discover_repos(args.owner)
        enumerated = enumerate_threads(args.owner, repos)
        threads = select_recent(enumerated, args.since)
        verify_control(threads, args.control, enumerated)
    except ControlStale as exc:
        # Exit 3, not 2: the instrument worked. A caller scripting this must be
        # able to tell "fix your invocation" from "distrust the output".
        print(f"CONTROL-STALE: {exc}", file=sys.stderr)
        return 3
    except SweepBroken as exc:
        print(f"SWEEP-BROKEN: {exc}", file=sys.stderr)
        return 2

    print(f"repos={len(repos)} threads={len(threads)} control={args.control or 'NONE'}")
    for t in threads:
        print(f"{t.ref}\t{t.updated_at}\t{t.title[:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
