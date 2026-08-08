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
import subprocess
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


# Tool names the harness once exposed and no longer does. A declaration of one
# is silently dropped — the agent launches minus that capability — so only a
# test catches it. `Task` was renamed to `Agent` (the subagent-spawn tool).
DEFUNCT_TOOLS = frozenset({"Task"})


def _declared_tools(text: str) -> list[str]:
    """Return the agent's `tools:` list items, or [] when it declares none.

    parse_frontmatter() above captures flat `key: value` lines only and skips
    indented ones, so a YAML *list* is invisible to it — hence this second,
    equally dependency-free reader. No `tools:` key means "inherit everything",
    which is a valid (and defect-free) declaration, so [] is the right answer
    for it: the caller intersects against DEFUNCT_TOOLS and finds nothing.
    """
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    if end == -1:
        return []
    out: list[str] = []
    in_tools = False
    for line in text[3:end].splitlines():
        if re.match(r"^tools:\s*$", line):
            in_tools = True
            continue
        if in_tools:
            m = re.match(r"^\s+-\s+([A-Za-z_][\w-]*)", line)
            if m:
                out.append(m.group(1))
                continue
            if line.strip():  # a new top-level key ends the list
                in_tools = False
    return out


def _flow_tools(value: str) -> list[str]:
    """Return base tool names from a flow-style `allowed-tools: ["A", "B(spec:*)"]`.

    Commands declare their tools under a different KEY (`allowed-tools`, not
    `tools`) and in a different STYLE (inline JSON array, not a block list) than
    agents do. `_declared_tools()` above reads only the block form on agents, so
    nothing ever inspected a command's list — which is exactly how `Task`
    survived in 18 commands after the agents were fixed for COS#27, with the
    suite green the whole time. A defunct entry is silently dropped at load, so
    a test is the only thing that can catch it.

    An entry may carry a permission specifier (`Bash(python3 foo.py:*)`); only
    the base name before `(` is meaningful for a defunct-name check.
    """
    return [m.group(1) for m in re.finditer(r'"\s*([A-Za-z_][\w-]*)', value)]


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


@pytest.mark.parametrize("agent", AGENT_FILES, ids=[_id(p) for p in AGENT_FILES])
def test_agent_declares_no_defunct_tool(agent: Path) -> None:
    """No agent declares a tool name the harness no longer exposes (COS#27).

    A defunct name is NOT a hard error — the agent still launches on its other
    declared tools — so the capability just vanishes silently. That is why this
    is a test and not a runtime check: nothing else would ever tell us.

    `Task` is the trap: it reads like the spawn tool but the current name is
    `Agent`. (TaskCreate/TaskUpdate/TaskList/TaskGet are todo management — a
    different surface — so only the bare name is defunct.)
    """
    tools = _declared_tools(agent.read_text(encoding="utf-8"))
    bad = sorted(set(tools) & DEFUNCT_TOOLS)
    assert not bad, (
        f"{agent.name} declares defunct tool(s) {bad}; "
        f"the subagent-spawn tool is 'Agent' (see {', '.join(sorted(DEFUNCT_TOOLS))} → Agent)"
    )


def test_agent_templates_teach_no_defunct_tool() -> None:
    """The authoring templates must not teach a defunct tool name (COS#27 root cause).

    Fixing only the shipped agents leaves the bug's SOURCE intact: every agent
    later authored from a template would reinherit `Task`. The templates are
    the single point where the name propagates, so they are asserted too.
    """
    offenders = [
        f"{p.relative_to(PLUGIN_ROOT)}:{i}"
        for p in SKILLS_DIR.rglob("*template*.md")
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
        if re.match(r"^\s+-\s+(%s)\s*(#.*)?$" % "|".join(sorted(DEFUNCT_TOOLS)), line)
    ]
    assert not offenders, f"template(s) still teach a defunct tool name: {offenders}"


@pytest.mark.parametrize("skill", SKILL_FILES, ids=[_id(p) for p in SKILL_FILES])
def test_forked_skill_pins_background(skill: Path) -> None:
    """A `context: fork` skill must also declare `background:` (Claude Code 2.1.218).

    2.1.218 changed forked skills to run in the BACKGROUND by default. An
    unpinned one returns only an agent handle; its text arrives later as a
    notification, so the invoking agent gets NOTHING in the turn that asked —
    and nothing errors, no test fails, no log complains. Every COS skill is a
    procedure whose result drives the caller's next step (spawn->verify,
    request-approval->act, detect->classify), so all of them pin `false`.

    This is a TEST and not a line in the authoring guide because the failure is
    silent and the guide can only advise: a skill authored next month would
    reintroduce it and nothing would notice. Practice adopted from the
    integrator plugin, which chose a blocking guard over a template fix for
    exactly this reason.
    """
    fm = parse_frontmatter(skill.read_text(encoding="utf-8")) or {}
    if fm.get("context") != "fork":
        return
    assert "background" in fm, (
        f"{skill.parent.name} declares `context: fork` with no `background:` — "
        "since Claude Code 2.1.218 it runs in the BACKGROUND and returns nothing "
        "in-turn. Ask: does the caller need this output IN THE TURN IT ASKS? "
        "YES -> add `background: false` (every current COS skill answers yes, "
        "verified per-skill); NO -> set it explicitly with a comment saying the "
        "backgrounding is deliberate, so the next reader does not undo it"
    )


# Sits deliberately BELOW the actual count (22), not at it. A floor pinned to the
# current number goes red the first time a skill is legitimately retired — and a
# guard that cries wolf gets deleted, which costs the whole check. The headroom
# buys a removal or two without a test edit while still catching mass erosion.
# Reasoning adopted from ai-maestro-integrator-agent (0dff4a9), which chose the
# same margin after this guard's shape went the other way.
FORKED_SKILL_FLOOR = 15


def test_forked_skills_exist() -> None:
    """Guard the VACUOUS PASS: the check above asserts nothing if no skill forks.

    Delete every forked skill — or rename the field — and the parametrized guard
    silently degrades to zero assertions while staying green, which is the one
    failure a guard cannot report about itself. Pin a floor so that collapse is
    visible.
    """
    forked = [
        p
        for p in SKILL_FILES
        if (parse_frontmatter(p.read_text(encoding="utf-8")) or {}).get("context") == "fork"
    ]
    assert len(forked) >= FORKED_SKILL_FLOOR, (
        f"only {len(forked)} skills declare `context: fork`, expected >= "
        f"{FORKED_SKILL_FLOOR}. Either the forked skills were eroded en masse, or "
        "the `context:` value was renamed and the per-skill pairing guard above is "
        "now asserting nothing. If skills were legitimately retired, lower this "
        "floor deliberately rather than letting the pairing guard pass vacuously"
    )


# ─────────────────────────────── commands ────────────────────────────────────
@pytest.mark.parametrize("cmd", COMMAND_FILES, ids=[_id(p) for p in COMMAND_FILES])
def test_command_frontmatter_parses(cmd: Path) -> None:
    """Every command .md has parseable frontmatter with a non-empty description."""
    fm = parse_frontmatter(cmd.read_text(encoding="utf-8"))
    assert fm is not None, f"{cmd} has no YAML frontmatter"
    assert fm.get("description"), f"{cmd} frontmatter missing 'description'"


@pytest.mark.parametrize("cmd", COMMAND_FILES, ids=[_id(p) for p in COMMAND_FILES])
def test_command_declares_no_defunct_tool(cmd: Path) -> None:
    """No command declares a defunct tool in `allowed-tools` (COS#27 follow-up).

    Fixing the agents left the commands untouched because the agent guard reads
    a different key and style (see `_flow_tools`). When this was finally
    measured, 18 of 23 commands still declared `Task` — none of which spawn a
    subagent at all.

    That is why the fix was to DROP the entry rather than rename it to `Agent`:
    renaming would have granted every one of those commands a subagent-spawn
    capability it never uses, which is the opposite of least privilege.
    """
    fm = parse_frontmatter(cmd.read_text(encoding="utf-8")) or {}
    declared = _flow_tools(fm.get("allowed-tools", ""))
    bad = sorted(set(declared) & DEFUNCT_TOOLS)
    assert not bad, (
        f"{cmd.name} declares defunct tool(s) {bad} in allowed-tools; the "
        "subagent-spawn tool is 'Agent' — and if the command does not spawn "
        "subagents, DROP the entry rather than renaming it (least privilege)"
    )


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
    """plugin.json is valid, carries required keys, and declares a PINNED ai-maestro-plugin dependency (M1).

    Upstream CPV (validate_plugin.py validate_dependencies) accepts entries as
    bare strings OR objects {"name", "version", "marketplace"}; the pinned
    object form is the fleet convention (cpv#106 precedent). This asserts the
    dependency is present AND version-pinned so an upstream release cannot
    break this plugin without warning.
    """
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    for key in ("name", "version", "description"):
        assert data.get(key), f"plugin.json missing '{key}'"
    assert re.match(r"^\d+\.\d+\.\d+$", data["version"]), "plugin.json version not semver"
    deps = data.get("dependencies")
    assert isinstance(deps, list) and deps, "plugin.json 'dependencies' must be a non-empty array"
    names = [d if isinstance(d, str) else d.get("name") for d in deps if isinstance(d, (str, dict))]
    assert "ai-maestro-plugin" in names, "plugin.json must declare ai-maestro-plugin (M1)"
    entry = next(d for d in deps if isinstance(d, dict) and d.get("name") == "ai-maestro-plugin")
    assert re.match(r"^[\^~>=]", str(entry.get("version", ""))), (
        "ai-maestro-plugin dependency must carry a semver range pin (fleet convention, cpv#106)"
    )


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


# The owner handle, assembled at runtime so THIS FILE never contains the literal
# it forbids — a guard that trips on its own source teaches the next author to
# add an exemption, and an exempted guard is a disabled one.
_OWNER_HANDLE = "@" + "Emasoft"


def _tracked_prose_files() -> list[Path]:
    """Every git-TRACKED .md file — the shippable population, per `git ls-files`.

    Not a glob: an untracked scratch file is not shipped and a tracked one in an
    unexpected directory still is, so the index is the only honest census.
    """
    out = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=PLUGIN_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return [PLUGIN_ROOT / p for p in out]


def test_no_paging_owner_handle_in_shipped_prose() -> None:
    """No shipped markdown may carry a literal `@<owner>` — it PAGES a real account.

    The self-identification template is the specific hazard (R22.2). Backticks do
    NOT make it safe: a template exists to be copied OUT of its code span into a
    real comment body, where the `@` linkifies and notifies the live account. So
    the protection has to be the absence of the character, not its surroundings.

    Naming a person is not mentioning them — the byline reads the same with the
    bare word, and the `@` adds nothing but the notification.
    """
    offenders: list[str] = []
    for path in _tracked_prose_files():
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _OWNER_HANDLE in line:
                offenders.append(f"{path.relative_to(PLUGIN_ROOT)}:{i}")
    assert not offenders, (
        f"{len(offenders)} shipped line(s) carry the literal owner handle and would "
        f"page a real account when copied into a GitHub body: {offenders}. "
        f"Write the name as a plain word ('via the shared Emasoft gh auth')."
    )


def test_paging_handle_guard_scans_a_real_population() -> None:
    """Guard the VACUOUS PASS: the check above asserts nothing over an empty file list.

    `git ls-files` returns nothing when run outside the work tree or when the
    glob stops matching, and the scan would then pass while inspecting zero
    files — green, and blind. Pin a floor so that collapse is visible.
    """
    n = len(_tracked_prose_files())
    assert n >= 40, (
        f"only {n} tracked .md files found, expected >= 40 — the owner-handle "
        "scan is running over a near-empty population and is not actually "
        "checking anything."
    )


@pytest.mark.parametrize("agent", AGENT_FILES, ids=[_id(p) for p in AGENT_FILES])
def test_agent_declares_no_model_pin(agent: Path) -> None:
    """No agent — main or sub — may pin `model:` (RP-MODEL-01, role-plugins-spec 1.1.0).

    Subagents omitting it was already settled; the ruling extends it to the main
    agent. The reasoning is why this is a guard and not a preference: model choice
    is a cost/capability decision belonging to whoever LAUNCHES the session, and a
    pin in a released artifact inverts that — it lets a role author spend the
    operator's budget, on every invocation, with no way for them to opt out short
    of editing the plugin.

    Two failure modes a pin adds that omission does not have: a movable token
    (`opus` has already shifted once, under a pattern set before Opus 5 existed)
    makes a versioned artifact's behaviour change without a release; and a pin is
    the only spelling that can SILENTLY degrade under an org model restriction.
    """
    fm = parse_frontmatter(agent.read_text(encoding="utf-8")) or {}
    assert "model" not in fm, (
        f"{agent.name} pins `model: {fm.get('model')}` — role-plugin agents must "
        "OMIT it and inherit the session model (RP-MODEL-01). The launcher owns "
        "the cost decision; a pinned artifact spends their budget for them."
    )
