"""Real (non-mocked) contract tests for every shipped component.

Every skill, agent, command, and hook in this plugin is covered here. The
tests parse the ACTUAL shipped files and assert the structural contract each
component must satisfy — valid frontmatter, a name and a description,
referenced files that actually exist, parseable manifests. They are real
(they read the real files, no mocks) and catch real regressions: a skill that
loses its description, a SKILL.md that links to a deleted reference, a
hooks.json that stops being valid JSON, a manifest that drifts.

Targets are discovered dynamically (globbed at collection time), so a new
skill/agent/command is covered automatically and a deleted one drops out — no
hardcoded inventory to forget to update.

Stdlib + pytest only (the plugin declares zero runtime dependencies); the
frontmatter parser below is intentionally tiny and dependency-free. Full
plugin validation is the remote CPV validator's job (cpv-remote-validate) —
this suite only guards the structural contracts the plugin itself owns.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PLUGIN_ROOT / "skills"
AGENTS_DIR = PLUGIN_ROOT / "agents"
COMMANDS_DIR = PLUGIN_ROOT / "commands"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
AGENT_TOML = PLUGIN_ROOT / "ai-maestro-chief-of-staff.agent.toml"


# ── dependency-free frontmatter parser (flat keys only — enough for the contract) ──
def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return the top-level YAML frontmatter as a flat dict, or None if absent.

    Only top-level `key: value` lines are captured (nested mappings are skipped
    by indentation) — sufficient for the name/description contract this asserts.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if line[0] in " \t":  # nested line — skip
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip("\"'")
    return out


def _discover(dir_path: Path, pattern: str) -> list[Path]:
    return sorted(dir_path.glob(pattern)) if dir_path.is_dir() else []


SKILL_FILES = _discover(SKILLS_DIR, "*/SKILL.md")
AGENT_FILES = [p for p in _discover(AGENTS_DIR, "*.md") if p.name != "README.md"]
COMMAND_FILES = [p for p in _discover(COMMANDS_DIR, "*.md") if p.name != "README.md"]


def _id(p: Path) -> str:
    return p.parent.name if p.name == "SKILL.md" else p.stem


# ──────────────────────────── sanity on discovery ────────────────────────────
def test_components_were_discovered() -> None:
    """The plugin actually ships skills, agents, and commands to cover."""
    assert SKILL_FILES, "no SKILL.md files discovered under skills/"
    assert AGENT_FILES, "no agent .md files discovered under agents/"
    assert COMMAND_FILES, "no command .md files discovered under commands/"


# ──────────────────────────────── skills ─────────────────────────────────────
@pytest.mark.parametrize("skill", SKILL_FILES, ids=[_id(p) for p in SKILL_FILES])
def test_skill_frontmatter_has_name_and_description(skill: Path) -> None:
    """Every SKILL.md has parseable frontmatter with a non-empty name + description."""
    fm = parse_frontmatter(skill.read_text(encoding="utf-8"))
    assert fm is not None, f"{skill} has no YAML frontmatter"
    assert fm.get("name"), f"{skill} frontmatter missing 'name'"
    assert fm.get("description"), f"{skill} frontmatter missing 'description'"


@pytest.mark.parametrize("skill", SKILL_FILES, ids=[_id(p) for p in SKILL_FILES])
def test_skill_name_matches_directory(skill: Path) -> None:
    """A skill's frontmatter 'name' equals its directory name (Claude Code contract)."""
    fm = parse_frontmatter(skill.read_text(encoding="utf-8")) or {}
    assert fm.get("name") == skill.parent.name, (
        f"{skill}: name '{fm.get('name')}' != dir '{skill.parent.name}'"
    )


@pytest.mark.parametrize("skill", SKILL_FILES, ids=[_id(p) for p in SKILL_FILES])
def test_skill_relative_links_resolve(skill: Path) -> None:
    """Every relative markdown link in a SKILL.md points at a file that exists.

    This is the regression guard for reference cleanup: a SKILL.md that links to
    a deleted references/*.md (or a removed -ref twin) fails here.
    """
    text = skill.read_text(encoding="utf-8")
    missing = []
    for m in re.finditer(r"\]\((?!https?://|#|mailto:)([^)]+)\)", text):
        target = m.group(1).split("#", 1)[0].strip()
        if not target:
            continue
        resolved = (skill.parent / target).resolve()
        if not resolved.exists():
            missing.append(target)
    assert not missing, f"{skill} links to missing files: {missing}"


def test_no_orphaned_ref_skill_dirs() -> None:
    """No `*-ref`/`*-refa..z` duplicate skill dirs remain (Phase-2 cleanup guard)."""
    orphans = [
        d.name
        for d in SKILLS_DIR.iterdir()
        if d.is_dir() and re.search(r"-ref[a-z]?$", d.name)
    ]
    assert not orphans, f"orphaned duplicate skill dirs reappeared: {orphans}"


def test_no_committed_audit_artifacts_in_skills() -> None:
    """No AUDIT_REPORT.md / FINAL_AUDIT_RESULTS.md / audit_tools/ left in skills."""
    leaked = [
        str(p.relative_to(PLUGIN_ROOT))
        for p in SKILLS_DIR.glob("*/*")
        if p.name in {"AUDIT_REPORT.md", "FINAL_AUDIT_RESULTS.md", "audit_tools"}
    ]
    assert not leaked, f"dev audit artifacts committed inside skills: {leaked}"


# ──────────────────────────────── agents ─────────────────────────────────────
@pytest.mark.parametrize("agent", AGENT_FILES, ids=[_id(p) for p in AGENT_FILES])
def test_agent_frontmatter_has_name_and_description(agent: Path) -> None:
    """Every agent .md has parseable frontmatter with a non-empty name + description."""
    fm = parse_frontmatter(agent.read_text(encoding="utf-8"))
    assert fm is not None, f"{agent} has no YAML frontmatter"
    assert fm.get("name"), f"{agent} frontmatter missing 'name'"
    assert fm.get("description"), f"{agent} frontmatter missing 'description'"


# ─────────────────────────────── commands ────────────────────────────────────
@pytest.mark.parametrize("cmd", COMMAND_FILES, ids=[_id(p) for p in COMMAND_FILES])
def test_command_frontmatter_parses(cmd: Path) -> None:
    """Every command .md has parseable frontmatter with a non-empty description."""
    fm = parse_frontmatter(cmd.read_text(encoding="utf-8"))
    assert fm is not None, f"{cmd} has no YAML frontmatter"
    assert fm.get("description"), f"{cmd} frontmatter missing 'description'"


# ───────────────────────────────── hooks ─────────────────────────────────────
def test_hooks_json_is_valid() -> None:
    """hooks.json parses as JSON and maps each event to a list of hook groups."""
    assert HOOKS_JSON.is_file(), "hooks/hooks.json is missing"
    data = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    hooks = data.get("hooks", data)
    assert isinstance(hooks, dict) and hooks, "hooks.json has no hook events"
    for event, groups in hooks.items():
        assert isinstance(groups, list), f"hooks.{event} must be a list"
        for group in groups:
            assert isinstance(group.get("hooks"), list), (
                f"hooks.{event} group missing a 'hooks' list"
            )


def test_hooks_referenced_scripts_exist() -> None:
    """Every script path referenced in hooks.json resolves to a real file."""
    text = HOOKS_JSON.read_text(encoding="utf-8")
    missing = []
    for m in re.finditer(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"'\s]+)", text):
        rel = m.group(1)
        # strip a trailing arg list if the command embeds one
        rel = rel.split()[0]
        if not (PLUGIN_ROOT / rel).exists():
            missing.append(rel)
    assert not missing, f"hooks.json references missing scripts: {missing}"


# ─────────────────────────────── manifests ───────────────────────────────────
def test_plugin_json_valid_and_dependency_declared() -> None:
    """plugin.json is valid, carries required keys, and declares its dependency (M1)."""
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    for key in ("name", "version", "description"):
        assert data.get(key), f"plugin.json missing '{key}'"
    assert re.match(r"^\d+\.\d+\.\d+$", data["version"]), "plugin.json version not semver"
    deps = data.get("dependencies")
    assert isinstance(deps, list) and all(isinstance(d, str) for d in deps), (
        "plugin.json 'dependencies' must be an array of strings"
    )
    assert "ai-maestro-plugin" in deps, "plugin.json must declare ai-maestro-plugin (M1)"


def test_agent_toml_valid() -> None:
    """The .agent.toml declares an [agent] name and pins a current CC floor (>=2.1.139, M11).

    Parsed with stdlib regex rather than tomllib so the suite runs on the
    declared floor of Python 3.10 (tomllib is 3.11+). The floor is compared as
    a numeric (major, minor, patch) tuple — a string compare would wrongly
    order 2.1.69 above 2.1.139.
    """
    text = AGENT_TOML.read_text(encoding="utf-8")
    assert re.search(r'^\s*name\s*=\s*"[^"]+"', text, re.M), ".agent.toml missing an [agent] name"
    m = re.search(r'claude_code_version\s*=\s*">=?\s*(\d+)\.(\d+)\.(\d+)"', text)
    assert m, ".agent.toml missing a claude_code_version floor"
    floor = tuple(int(g) for g in m.groups())
    assert floor >= (2, 1, 139), f".agent.toml CC floor stale: {floor}"
