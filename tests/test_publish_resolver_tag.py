"""Real tests for the publish pipeline's resolver-tag derivation (COS#25).

Since Claude Code 2.1.110 a version-constrained plugin dependency resolves ONLY
against git tags named `{plugin-name}--v{version}`. A plain `v2.8.0` tag is
invisible to the resolver, so a dependent fails with `no git tag satisfying
<range>` against a repo full of tags — the bug that grounded the whole fleet
(TRDD-JT3U4ZVM). `scripts/publish.py` therefore emits BOTH tag shapes.

These call the REAL `resolver_tag_name` against REAL manifest files written to
tmp_path — no mocks, no fakes. The failure modes are the point: a tag is
permanent and consumer-facing, so a manifest this function cannot read must
abort the publish rather than mint a plausible-looking `unknown--v1.2.3` tag
that no resolver will ever match.

Stdlib + pytest only, matching the rest of the suite.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from publish import resolver_tag_name  # noqa: E402

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def _manifest(root: Path, payload: str) -> Path:
    """Write a raw .claude-plugin/plugin.json under root (payload verbatim)."""
    d = root / ".claude-plugin"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "plugin.json"
    p.write_text(payload, encoding="utf-8")
    return p


def test_resolver_tag_matches_the_shipped_manifest() -> None:
    """The real repo's manifest yields `ai-maestro-chief-of-staff--v<version>`.

    Guards the exact string a consumer's resolver matches against; a typo in the
    separator (`-v` vs `--v`) is invisible until a dependent fails to install.
    """
    name = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["name"]
    assert resolver_tag_name(PLUGIN_ROOT, "9.9.9") == f"{name}--v9.9.9"
    assert resolver_tag_name(PLUGIN_ROOT, "9.9.9").startswith("ai-maestro-chief-of-staff--v")


def test_resolver_tag_derives_name_from_manifest_not_directory(tmp_path: Path) -> None:
    """The name comes from the manifest, never from the directory name.

    The resolver matches the tag against the DEPENDENCY's declared name, which
    is the manifest's — a repo whose directory is named differently must still
    publish a tag consumers can resolve.
    """
    _manifest(tmp_path, json.dumps({"name": "some-other-plugin", "version": "1.0.0"}))
    assert resolver_tag_name(tmp_path, "1.0.0") == "some-other-plugin--v1.0.0"


def test_resolver_tag_hardfails_when_manifest_missing(tmp_path: Path) -> None:
    """No manifest → abort. Never fall back to a guessed name."""
    with pytest.raises(SystemExit):
        resolver_tag_name(tmp_path, "1.0.0")


def test_resolver_tag_hardfails_when_name_absent(tmp_path: Path) -> None:
    """Manifest without 'name' → abort (the reference impl's contract)."""
    _manifest(tmp_path, json.dumps({"version": "1.0.0"}))
    with pytest.raises(SystemExit):
        resolver_tag_name(tmp_path, "1.0.0")


@pytest.mark.parametrize("payload", ['{"name": "", "version": "1.0.0"}', '{"name": "   ", "version": "1.0.0"}'])
def test_resolver_tag_hardfails_on_blank_name(tmp_path: Path, payload: str) -> None:
    """An empty/whitespace name → abort, not a `--v1.0.0` tag with no plugin.

    `.get("name")` is truthy-checked rather than presence-checked precisely
    because a blank name would otherwise sail through and mint a nameless tag.
    """
    _manifest(tmp_path, payload)
    with pytest.raises(SystemExit):
        resolver_tag_name(tmp_path, "1.0.0")


def test_resolver_tag_hardfails_on_invalid_json(tmp_path: Path) -> None:
    """Corrupt manifest → abort with a clear error, not a stack trace."""
    _manifest(tmp_path, "{not json")
    with pytest.raises(SystemExit):
        resolver_tag_name(tmp_path, "1.0.0")
