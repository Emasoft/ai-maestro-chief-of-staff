"""Real tests for the commit-msg governance self-id trailer hook (COS#24 B2).

Every commit in this repo must carry an ``Agent: ai-maestro-chief-of-staff``
git trailer so ``git blame``/``git log`` can attribute it to the plugin whose
development produced it (commit-discipline + PRRD G1.1). ``scripts/publish.py``
installs ``.githooks/commit-msg`` from an inline template and activates
``core.hooksPath`` (via the sibling pre-push installer) so the hook is live for
every commit.

Two invariants are the whole point and are tested against the REAL shipped hook
(no mocks): it is FAIL-OPEN (a rejecting commit-msg hook would block the commit,
so it always exits 0) and IDEMPOTENT (amend/rebase must never double-stamp, and
an explicit hand-written Agent trailer must be respected). A drift guard asserts
the committed file is byte-identical to the template publish.py would rewrite.

Stdlib + pytest only, matching the rest of the suite.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import publish  # noqa: E402

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SHIPPED_HOOK = PLUGIN_ROOT / ".githooks" / "commit-msg"
PUBLISH_PY = PLUGIN_ROOT / "scripts" / "publish.py"
TRAILER = "Agent: ai-maestro-chief-of-staff"


def _run_hook(msg_path: Path) -> int:
    """Invoke the real shipped hook on a message file via bash; return exit code."""
    return subprocess.run(["bash", str(SHIPPED_HOOK), str(msg_path)], check=False).returncode


def test_shipped_hook_matches_template() -> None:
    """The committed .githooks/commit-msg is byte-identical to publish.py's template.

    If they drift, a publish.py run would silently rewrite the working tree — the
    same clean-tree trap the pre-push hook guards against.
    """
    assert SHIPPED_HOOK.exists(), "shipped .githooks/commit-msg is missing"
    assert SHIPPED_HOOK.read_text(encoding="utf-8") == publish.COMMIT_MSG_HOOK_TEMPLATE


def test_shipped_hook_is_executable() -> None:
    """The committed hook carries the executable bit (git runs it directly)."""
    assert os.access(SHIPPED_HOOK, os.X_OK), ".githooks/commit-msg is not executable"


def test_ensure_commit_msg_hook_writes_and_chmods(tmp_path: Path) -> None:
    """ensure_commit_msg_hook creates the hook from the template and chmods it."""
    publish.ensure_commit_msg_hook(tmp_path)
    hook = tmp_path / ".githooks" / "commit-msg"
    assert hook.read_text(encoding="utf-8") == publish.COMMIT_MSG_HOOK_TEMPLATE
    assert os.access(hook, os.X_OK)


def test_hook_appends_agent_trailer_when_absent(tmp_path: Path) -> None:
    """A message with no Agent trailer gets one appended; exit 0."""
    msg = tmp_path / "m"
    msg.write_text("fix: something\n\nbody line\n", encoding="utf-8")
    assert _run_hook(msg) == 0
    lines = msg.read_text(encoding="utf-8").splitlines()
    assert TRAILER in lines, f"trailer not appended: {lines!r}"


def test_hook_is_idempotent(tmp_path: Path) -> None:
    """Running the hook twice leaves exactly one Agent trailer (amend/rebase safe)."""
    msg = tmp_path / "m"
    msg.write_text("chore: x\n", encoding="utf-8")
    _run_hook(msg)
    _run_hook(msg)
    body = msg.read_text(encoding="utf-8")
    assert body.count(TRAILER) == 1, f"double-stamped: {body!r}"


def test_hook_respects_existing_agent_trailer(tmp_path: Path) -> None:
    """An explicit Agent trailer is left untouched (--if-exists doNothing)."""
    msg = tmp_path / "m"
    msg.write_text("chore: x\n\nAgent: some-other-plugin\n", encoding="utf-8")
    assert _run_hook(msg) == 0
    body = msg.read_text(encoding="utf-8")
    assert "Agent: some-other-plugin" in body
    assert TRAILER not in body, "hook overrode an explicit Agent trailer"
    assert body.count("Agent:") == 1


def test_hook_fail_open_on_missing_arg() -> None:
    """No message-file argument → exit 0 (never block a commit)."""
    assert subprocess.run(["bash", str(SHIPPED_HOOK)], check=False).returncode == 0


def test_hook_fail_open_on_missing_file(tmp_path: Path) -> None:
    """A non-existent message-file path → exit 0 (never block a commit)."""
    assert _run_hook(tmp_path / "does-not-exist") == 0


def test_step_0_5_wires_commit_msg_hook() -> None:
    """publish.py's Step 0.5 actually calls ensure_commit_msg_hook (wiring guard)."""
    src = PUBLISH_PY.read_text(encoding="utf-8")
    assert "ensure_commit_msg_hook(git_root)" in src, "Step 0.5 does not install the commit-msg hook"
