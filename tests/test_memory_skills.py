"""Real (non-mocked) tests for this plugin's ADOPTION of the global memory system.

ai-maestro-chief-of-staff no longer ships per-plugin memory skills — it adopts
the janitor-hosted global 3-scope wiki (TRDD-59581001). The plugin's testable
memory responsibility is therefore its ADOPTION STATE, not memory behavior: the
per-plugin surfaces are gone, CLAUDE.md points at the global system and carries
the COS-specific moments, the .gitignore re-includes the PROJECT memory scope,
the seeded PROJECT pages are schema-valid, and no live surface still wires the
removed skills. (The recall/write/grep-fallback BEHAVIOR is the janitor's
responsibility, tested in the janitor's own suite — not duplicated here.)
"""

import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

REMOVED_SURFACES = [
    PLUGIN_ROOT / "skills" / "cos-memory-recall",
    PLUGIN_ROOT / "skills" / "cos-memory-write",
    PLUGIN_ROOT / "rules" / "memory-protocol.md",
]

GLOBAL_SKILLS = ("janitor-memory-recall", "janitor-memory-write", "janitor-memory-update")

# Live plugin surfaces that must not wire the removed skills. design/ (TRDDs that
# legitimately name the deletion targets), CLAUDE.md (its "do NOT re-create" note
# names them by design), and this test file are intentionally out of scope.
SCAN_ROOTS = ("agents", "skills", "commands", "hooks", "rules")
SCAN_FILES = ("README.md", "ai-maestro-chief-of-staff.agent.toml")
SCAN_SUFFIXES = {".md", ".toml", ".json", ".py", ".sh"}


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-frontmatter parser for the flat note schema used in tests."""
    assert text.startswith("---\n"), "note must open with a frontmatter fence"
    fm_block = text.split("---", 2)[1]
    fields: dict = {}
    current_map: dict | None = None
    for line in fm_block.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_map is not None:
            key, _, value = line.strip().partition(":")
            current_map[key.strip()] = value.strip().strip('"')
        else:
            key, _, value = line.partition(":")
            value = value.strip()
            if value == "":
                current_map = {}
                fields[key.strip()] = current_map
            else:
                fields[key.strip()] = value.strip('"')
                current_map = None
    return fields


def test_per_plugin_memory_surfaces_removed() -> None:
    """The superseded per-plugin memory skills + rule mirror no longer ship."""
    for p in REMOVED_SURFACES:
        assert not p.exists(), f"{p.relative_to(PLUGIN_ROOT)} must be removed (superseded by the global system)"


def test_claude_md_points_at_global_system() -> None:
    """CLAUDE.md adopts the global janitor skills + the recall rule + names the PROJECT scope."""
    cm = PLUGIN_ROOT / "CLAUDE.md"
    assert cm.exists(), "plugin CLAUDE.md must exist (it folds the COS-specific memory guidance)"
    body = cm.read_text(encoding="utf-8")
    for sk in GLOBAL_SKILLS:
        assert sk in body, f"CLAUDE.md must reference the global skill {sk}"
    assert "markdown-memory-recall.md" in body, "CLAUDE.md must reference the global recall rule"
    assert ".claude/project/memory" in body, "CLAUDE.md must name the PROJECT memory scope"


def test_claude_md_carries_cos_specific_moments() -> None:
    """CLAUDE.md preserves the COS-role recall/write moments folded from the removed surfaces."""
    body = (PLUGIN_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "approval tier" in body, "must keep the classify-approval-tier recall moment"
    assert ("recurring agent failure" in body or "recurring alert" in body), \
        "must keep the recurring-failure/alert recall moment"


def test_gitignore_reincludes_project_memory_scope() -> None:
    """.gitignore widens .claude/ to /** and re-includes .claude/project/memory/**, with no bare line."""
    gi = (PLUGIN_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert not re.search(r"(?m)^\.claude/?$", gi), \
        "no bare .claude/ ignore line may remain (it would prune the re-included memory tree)"
    assert "!.claude/project/memory/**" in gi, "the PROJECT memory re-include exception must be present"


def test_seeded_project_pages_are_schema_valid() -> None:
    """The bootstrapped PROJECT scope ships a schema-valid architecture hub + a MEMORY.md index."""
    memdir = PLUGIN_ROOT / ".claude" / "project" / "memory"
    hub = memdir / "architecture.md"
    index = memdir / "MEMORY.md"
    assert hub.exists(), "architecture hub must be seeded"
    assert index.exists(), "MEMORY.md index must be seeded"
    fm = parse_frontmatter(hub.read_text(encoding="utf-8"))
    assert fm["name"] == "architecture", "hub name must be 'architecture'"
    assert fm["description"], "hub description must be non-empty"
    assert fm["metadata"]["node_type"] == "memory"
    assert fm["metadata"]["tier"] == "hub", "the seeded page must be the hub tier"
    assert "architecture.md" in index.read_text(encoding="utf-8"), "MEMORY.md must link the hub"


def test_no_live_surface_references_removed_skills() -> None:
    """No live agent/skill/manifest surface still wires the removed cos-memory-* skills."""
    offenders = []
    candidates = [PLUGIN_ROOT / f for f in SCAN_FILES]
    for root in SCAN_ROOTS:
        candidates += list((PLUGIN_ROOT / root).rglob("*"))
    for path in candidates:
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "cos-memory-recall" in text or "cos-memory-write" in text:
            offenders.append(str(path.relative_to(PLUGIN_ROOT)))
    assert not offenders, f"these live surfaces still reference the removed skills: {offenders}"


def test_main_agent_uses_global_skills() -> None:
    """The main agent's Durable Memory directive points at the global skills, not the removed ones."""
    agent = (PLUGIN_ROOT / "agents" / "ai-maestro-chief-of-staff-main-agent.md").read_text(encoding="utf-8")
    assert "/janitor-memory-recall" in agent, "main agent must invoke the global recall skill"
    assert "cos-memory-recall" not in agent and "cos-memory-write" not in agent, \
        "main agent must not reference the removed per-plugin skills"
