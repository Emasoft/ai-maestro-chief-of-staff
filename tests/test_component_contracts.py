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

import ast
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

    A COMMENT inside the block does NOT end it. That distinction is load-bearing,
    not pedantry: this reader used to treat any non-`- Tool` line as the start of
    the next top-level key, so a leading `# ...` comment truncated the list to
    empty. Two agents carry exactly such a comment — added by COS#27 to record
    that their spawn tool was removed ON PURPOSE — so the prose documenting a
    security decision silently blinded every check of it. `amcos-staff-planner`
    and `amcos-performance-reporter` parsed as `[]`, meaning the defunct-tool
    guard had been asserting nothing on the two files it was written for: a `Task`
    entry re-added below the comment would have passed. Terminate only on a real
    top-level key — non-blank, non-comment, and unindented.
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
            if not line.strip() or line.lstrip().startswith("#"):
                continue  # blank / comment — still inside the block
            if not line[:1].isspace():  # a new top-level key ends the list
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
    assert fm.get("name") == skill.parent.name, f"{skill}: name '{fm.get('name')}' != dir '{skill.parent.name}'"


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
    orphans = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and re.search(r"-ref[a-z]?$", d.name)]
    assert not orphans, f"orphaned duplicate skill dirs reappeared: {orphans}"


def test_no_committed_audit_artifacts_in_skills() -> None:
    """No AUDIT_REPORT.md / FINAL_AUDIT_RESULTS.md / audit_tools/ left in skills."""
    leaked = [str(p.relative_to(PLUGIN_ROOT)) for p in SKILLS_DIR.glob("*/*") if p.name in {"AUDIT_REPORT.md", "FINAL_AUDIT_RESULTS.md", "audit_tools"}]
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
    assert not bad, f"{agent.name} declares defunct tool(s) {bad}; the subagent-spawn tool is 'Agent' (see {', '.join(sorted(DEFUNCT_TOOLS))} → Agent)"


def test_agent_templates_teach_no_defunct_tool() -> None:
    """The authoring templates must not teach a defunct tool name (COS#27 root cause).

    Fixing only the shipped agents leaves the bug's SOURCE intact: every agent
    later authored from a template would reinherit `Task`. The templates are
    the single point where the name propagates, so they are asserted too.
    """
    offenders = [f"{p.relative_to(PLUGIN_ROOT)}:{i}" for p in SKILLS_DIR.rglob("*template*.md") for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if re.match(r"^\s+-\s+(%s)\s*(#.*)?$" % "|".join(sorted(DEFUNCT_TOOLS)), line)]
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
    forked = [p for p in SKILL_FILES if (parse_frontmatter(p.read_text(encoding="utf-8")) or {}).get("context") == "fork"]
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
    assert not bad, f"{cmd.name} declares defunct tool(s) {bad} in allowed-tools; the subagent-spawn tool is 'Agent' — and if the command does not spawn subagents, DROP the entry rather than renaming it (least privilege)"


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
            assert isinstance(group.get("hooks"), list), f"hooks.{event} group missing a 'hooks' list"


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
    assert re.match(r"^[\^~>=]", str(entry.get("version", ""))), "ai-maestro-plugin dependency must carry a semver range pin (fleet convention, cpv#106)"


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


# Handles assembled at runtime so THIS FILE never contains the literals it
# forbids — a guard that trips on its own source teaches the next author to add
# an exemption, and an exempted guard is a disabled one.
#
# `@owner` is here for the same reason as the concrete handle: it is itself a
# real GitHub org, so the PLACEHOLDER pages an account too — before substitution
# and after. Guarding only the concrete handle left the byline TEMPLATE (the
# thing actually copied into comments) unguarded, which is backwards.
_FORBIDDEN_HANDLES = ("@" + "Emasoft", "@" + "owner")


def _tracked_prose_files() -> list[Path]:
    """Every git-TRACKED .md file — the shippable population, per `git ls-files`.

    Not a glob: an untracked scratch file is not shipped and a tracked one in an
    unexpected directory still is, so the index is the only honest census.
    """
    out = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=PLUGIN_ROOT,
        capture_output=True,
        text=True,
        check=True,
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
            for handle in _FORBIDDEN_HANDLES:
                if handle in line:
                    offenders.append(f"{path.relative_to(PLUGIN_ROOT)}:{i}")
                    break
    assert not offenders, (
        f"{len(offenders)} shipped line(s) carry a literal paging handle and would "
        f"notify a real account when copied into a GitHub body: {offenders}. "
        "Write the name as a plain word ('via the shared Emasoft gh auth'). "
        "Backticking is NOT a fix — a template is copied OUT of its code span, so "
        "the character itself has to go."
    )


def test_paging_handle_guard_scans_a_real_population() -> None:
    """Guard the VACUOUS PASS: the check above asserts nothing over an empty file list.

    `git ls-files` returns nothing when run outside the work tree or when the
    glob stops matching, and the scan would then pass while inspecting zero
    files — green, and blind. Pin a floor so that collapse is visible.
    """
    n = len(_tracked_prose_files())
    assert n >= 40, f"only {n} tracked .md files found, expected >= 40 — the owner-handle scan is running over a near-empty population and is not actually checking anything."


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
    assert "model" not in fm, f"{agent.name} pins `model: {fm.get('model')}` — role-plugin agents must OMIT it and inherit the session model (RP-MODEL-01). The launcher owns the cost decision; a pinned artifact spends their budget for them."


MAIN_AGENT = AGENTS_DIR / "ai-maestro-chief-of-staff-main-agent.md"
SKILL_MENU_HEADING = "## Skill References"


def _slice_unique(text: str, anchor: str, terminator: str, must_contain: str) -> str:
    """Select a section by PROPERTY, refusing ambiguity — never by first match.

    Two guarantees, and ARCHITECT's point (ai-maestro#131) is that either alone is
    weaker than both: a uniqueness check still lets a guard pick *something* when
    the anchor is unique-but-wrong, and a content check still lets it pick the
    first of several candidates that happens to qualify.

    1. REFUSE when the anchor does not occur exactly once, reporting the count,
       instead of silently taking the first hit.
    2. ASSERT the selected slice carries a marker only the real section can carry,
       folding the failure mode into the selection rather than leaving it as a
       separate assertion a mis-selected slice could still satisfy.

    Both anchors here occur exactly once today, so nothing is broken — but the
    likeliest future edit is the one that breaks it: a cross-reference naming the
    section, written from elsewhere in the same file. `str.index` would then
    select the prose mention and every assertion in the class would start passing
    or failing for reasons unrelated to the invariant. This repo has already been
    bitten three times by a selector reporting on the wrong occurrence.
    """
    hits = text.count(anchor)
    assert hits != 0, (
        f"anchor {anchor!r} is ABSENT. This is a distinct failure from ambiguity "
        "and the more dangerous one: `.find` returns -1, so a naive slice becomes "
        "the WHOLE document, and a positive 'does it contain X' assertion then "
        "passes because the document trivially contains its own content. CORE "
        "measured that shape growing a slice 10,095 -> 214,697 chars while its "
        "test stayed green (ai-maestro#131). Re-anchor or fix the source."
    )
    assert hits == 1, f"anchor {anchor!r} occurs {hits} times — refusing to guess which is the real section. A first-match slice would pick one and the guard would silently stop testing what it claims to test."
    rest = text[text.index(anchor) + len(anchor) :]
    m = re.search(terminator, rest)
    section = rest[: m.start()] if m else rest
    assert must_contain in section, f"the slice selected by {anchor!r} does not contain {must_contain!r}, so it is the wrong slice however it was found."
    return section


def _skill_menu_section() -> str:
    """The persona's skill-menu section ONLY — heading to the next `## `.

    Scope is the entire point (RP-SKILL-MENU-01, via AUTONOMOUS). Matching skill
    names against the WHOLE persona passes while the menu quietly loses an entry,
    because the frontmatter `skills:` preload list names every skill near the top
    of the file — so a file-wide search always finds a "mention" and the menu can
    rot untouched underneath it. Measured here before the fix: 23 skills on disk,
    23 findable file-wide, only 17 in the menu.
    """
    # `amcos-` is the marker only the real menu can carry: every shipped skill is
    # named `amcos-*`, so a slice without one is not the menu.
    return _slice_unique(
        MAIN_AGENT.read_text(encoding="utf-8"),
        SKILL_MENU_HEADING,
        r"\n## ",
        "amcos-",
    )


def test_every_skill_appears_in_the_persona_menu() -> None:
    """Every shipped skill must be listed in the persona's menu SECTION (RP-SKILL-MENU-01).

    A skill absent from the menu still loads, so nothing breaks loudly — the agent
    simply never learns the skill exists and silently stops routing to it. That is
    the failure this guards: not a crash, a capability quietly going unused.
    """
    section = _skill_menu_section()
    on_disk = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir())
    missing = [s for s in on_disk if s not in section]
    assert not missing, f"{len(missing)} skill(s) exist but are absent from '{SKILL_MENU_HEADING}': {missing}. They are still preloaded, so nothing fails — the agent just never learns they exist. Add a menu line; do NOT widen this check to the whole file, which passes on the frontmatter preload list alone."


def test_skill_menu_scope_is_narrower_than_the_file() -> None:
    """Guard the guard: prove the menu section is a strict SUBSET of the persona.

    If `_skill_menu_section` ever returned the whole file (heading renamed, parse
    broken), the check above would still pass while asserting nothing — the exact
    vacuity RP-SKILL-MENU-01 warns about. Pin that the section is materially
    smaller than the document it lives in.
    """
    section = _skill_menu_section()
    whole = MAIN_AGENT.read_text(encoding="utf-8")
    assert len(section) < len(whole) * 0.5, f"the skill-menu section is {len(section)} chars of a {len(whole)}-char persona — that is not a section, and the menu check has degenerated into a file-wide search that passes on the frontmatter preload list."


# --- The second transport (ai-maestro#131) ------------------------------------
#
# Claude Code 2.1.224 added a native cross-session transport (`SendMessage` /
# `ListAgents`) alongside AMP. The R6 graph is defined over AI-Maestro TITLES and
# enforced by the server on the AMP path; the native directory keys on SESSION
# NAMES, so there is no identity for a graph check to key on and no 403 can ever
# arrive there. Measured in this session 2026-08-11T19:28:17+0200: `ListAgents`
# returned 18 peers INCLUDING an `ai-maestro-autonomous-agent-*` session — a
# title this persona forbids — addressable by name with nothing in the way.
#
# The persona must therefore say the rule binds on WHO is contacted rather than
# on the transport. These are three separate assertions on purpose: naming the
# tools and disclaiming enforcement are independent failures, and a body that
# merely name-dropped `SendMessage` would satisfy a keyword scan while still
# implying the server covers it.

_NATIVE_TRANSPORT_TOOLS = ("SendMessage", "ListAgents")


def test_persona_names_the_native_transport() -> None:
    """The persona must NAME the second transport it is silent about otherwise.

    A restriction the reader cannot map onto the tool in front of them is not a
    restriction. Before this guard the persona mentioned `403` four times and
    these two tool names zero times, so every statement of the rule pointed at
    the one path that is policed and none at the one that is not.
    """
    text = MAIN_AGENT.read_text(encoding="utf-8")
    missing = [t for t in _NATIVE_TRANSPORT_TOOLS if t not in text]
    assert not missing, f"the persona never names {missing} — the harness transport that carries no AID and cannot 403. An agent reading only about the API believes the server covers a path it has no enforcement point on (ai-maestro#131)."


def test_persona_states_the_native_transport_is_not_policed() -> None:
    """Naming the tools is not enough — the persona must DISCLAIM enforcement there.

    This is the assertion that cannot be satisfied by vocabulary. A persona could
    name `SendMessage` in passing (e.g. listing its tools) and still leave every
    statement of the rule reading as server-guaranteed. What has to survive is the
    load-bearing claim: no check exists on that path, so the agent is the
    enforcement point.
    """
    text = MAIN_AGENT.read_text(encoding="utf-8")
    assert "you are the only enforcement point" in text.lower(), "the persona names the native transport but never says it is UNPOLICED. Vocabulary is not a warning: without the disclaimer the four `403` promises still read as covering every path (ai-maestro#131)."
    assert "is not a licence to contact it" in text.lower(), "the persona does not say that `ListAgents` visibility confers no permission. An agent told 'you may message only X' and then handed a directory of everyone will reason its way around the rule."
    assert "untrusted data" in text.lower(), "the persona does not say inbound cross-session messages carry no server-side identity check. This matters most for a title that DOES receive authenticated instructions over AMP — on arrival the two look alike, and only one of them was checked."


def test_shipped_subagents_cannot_reach_a_peer_session() -> None:
    """The subagent restriction must be MECHANICAL, not merely asserted in prose.

    The persona tells subagents they cannot message peers. For the agents this
    plugin ships that is enforced by the `tools:` allowlist rather than by any
    server — so it holds only as long as no allowlist grows `SendMessage`. Pin it,
    because the failure is silent: a subagent that gained the tool would be able
    to contact any listed session, with no AMP identity and nothing to refuse it.
    """
    offenders = []
    for agent in AGENT_FILES:
        if agent == MAIN_AGENT:
            continue
        tools = _declared_tools(agent.read_text(encoding="utf-8"))
        if any(t in _NATIVE_TRANSPORT_TOOLS for t in tools):
            offenders.append(agent.name)
    assert not offenders, f"{offenders} declare a native cross-session tool. Subagents have no AMP identity, so nothing would authenticate or refuse them — the R6 graph would bind them with no enforcement point at all."


# --- The RECEIVE side (ai-maestro#131, MAINTAINER's mirror finding) -----------
#
# The fleet screen asked every persona "do you claim a forbidden SEND returns
# 403?". Nobody asked the mirror question: "does the persona tell the agent where
# messages ARRIVE?". Measured here 2026-08-11 before the fix: this persona named
# ZERO inbound channels; three exist. (The two `amp-inbox` hits in skills/ are an
# allowed-tools declaration and a mid-procedure step, not a wake rule.)
#
# The receive failure is worse than the send failure and that is why it is
# guarded: a forbidden send at least leaves an artifact on the recipient, while a
# missed receive produces a SUCCESSFUL-looking wake — inbox drained, nothing
# found, work resumed — with live directives still waiting and nobody able to
# notice. Silence on an unpolled channel reads exactly like absence.
#
# For COS specifically the blast radius is not its own thread: as the team's sole
# entry point and Tier-1 approver, a missed inbound strands a member who has no
# other path in and cannot distinguish silence from refusal.

INBOUND_HEADING = "### Inbound discipline"


def _inbound_section() -> str:
    """The inbound bullet ONLY — heading to the next heading of any level.

    Scoping is load-bearing here and the trap is specific to this file: the
    send-side fix (v2.25.0) put `SendMessage` into the Communication Permissions
    section, so a whole-file `assert "SendMessage" in persona` now passes on THAT
    text alone and would green-light an AMP-only inbound rule. The guard would
    assert nothing precisely because an earlier fix succeeded.
    """
    # `amp-inbox` is the marker only the real bullet can carry: it enumerates the
    # channels, so a slice missing channel 1 is the wrong slice however it was
    # found (ARCHITECT's sharpening — refuse ambiguity AND assert the marker).
    return _slice_unique(
        MAIN_AGENT.read_text(encoding="utf-8"),
        INBOUND_HEADING,
        r"\n#{1,3} ",
        "amp-inbox",
    )


def test_persona_enumerates_every_inbound_channel_not_just_amp() -> None:
    """The inbound rule must name all THREE arrival channels, not only AMP."""
    bullet = _inbound_section()
    assert "amp-inbox" in bullet, "channel 1 (AMP) unnamed"
    assert "SendMessage" in bullet or "cross-session-message" in bullet, "channel 2 (direct session channel) unnamed — it is never in `amp-inbox` and there is nothing to poll, so an agent that does not know it exists loses every peer message that lands mid-turn."
    assert re.search(r"(?i)never\b[^.]{0,60}in\s+`?amp-inbox", bullet), "the rule does not state that channel 2 NEVER appears in amp-inbox — without it, draining AMP still reads as draining everything."
    assert re.search(r"(?i)gh issue list", bullet), "channel 3 (GitHub threads) unnamed. GitHub cannot notify an agent, so a thread awaiting your reply is invisible until you look for it."
    assert re.search(r"(?i)never call the inbox clear on the strength of one", bullet), "the rule does not forbid declaring the inbox clear from one channel — which is the whole failure mode."


R428_HEADING = "### R42.8 — your ONE cross-agent power"


def test_persona_states_r42_8_and_its_limits() -> None:
    """The one cross-agent capability this title holds must be stated WITH its limits.

    R42.8 grants MANAGER and CHIEF-OF-STAFF alone the power to answer a prompt
    blocking another agent — "one narrow power the others do not [hold]". This
    persona named it ZERO times, discovered 2026-08-12 while reading a consolidated
    ruling that had gone unread for five days. A capability an agent does not know
    it has is not thereby safe: the eight constraints are what separate an unblock
    from R42.1 injection, which is ABSOLUTE, so a role prompt that omits them
    cannot bind at the moment of use.

    Asserted at the CONSTRAINT level, not the rule name, for the reason this repo
    has now hit repeatedly: naming R42.8 while omitting the limits would satisfy a
    keyword scan while leaving the dangerous half unsaid. The two clauses pinned
    individually are the ones whose absence would be actively harmful — the
    ASSISTANT exclusion (its rationale is laundering an instruction into apparent
    human intent) and the server-enforced clause (an agent that believes its own
    restraint is the check has misunderstood where the boundary lives).

    Source: Emasoft/ai-maestro@governance-rules tip 7b5e02ca,
    design/specs/governance-spec.md (NORMATIVE per the 4.8.0 authority inversion).
    """
    section = _slice_unique(MAIN_AGENT.read_text(encoding="utf-8"), R428_HEADING, r"\n### ", "R42.1")
    # Case-INSENSITIVE: these assert that a CONCEPT is present, not how it was
    # typed. Emphasis is legitimate prose ("your **OWN team** only"), and a
    # case-sensitive check reds on correct text — which is how a guard becomes
    # noise and then gets deleted. Caught here on the first run against my own
    # wording, and it is the same trap as ATOM-41UD-NYIU (a case-sensitive grep
    # reporting zero links on a page that had them).
    lowered = section.lower()
    for token, why in (
        ("block-state", "the permitted verb set is unstated"),
        ("read-prompt", "the permitted verb set is unstated"),
        ("answer", "the permitted verb set is unstated"),
        ("own team", "(c) title-scope missing — COS may unblock its OWN team only"),
        ("sole notary", "(e) identity-prompt escalation missing"),
        ("audited", "(h) the ledger requirement is missing"),
    ):
        assert token in lowered, f"R42.8 stated without {token!r} — {why}"

    # (d) asserts the PROHIBITION, not the word. Seeding the removal of "never an
    # ASSISTANT, under any title" left a bare `"assistant" in section` check GREEN,
    # because the word survives in the surrounding rationale ("an ASSISTANT is the
    # surface a human talks through"). A guard that passes on prose explaining WHY
    # a rule exists, after the rule itself was deleted, is the exact failure this
    # file exists to prevent — found by seeding it rather than by reading it.
    assert re.search(r"never an assistant", lowered), "(d) missing: the persona no longer PROHIBITS unblocking an ASSISTANT. The word may still appear in the rationale — that is not the rule. This is the one target whose text is indistinguishable from its human's own input."

    assert re.search(r"(?i)never your own restraint", section), "(g) missing: the persona does not say the SERVER is the enforcement point. An agent that believes its own restraint is the check will treat a successful call as an authorized one."
    assert re.search(r"(?i)inject|queue", section), "the persona does not warn off `inject`/`queue`. They express the CALLER's decision, which is exactly what R42.1 revokes, and the server 403s them cross-agent — a reader who reaches for them is heading into a denial."


def _prose(text: str) -> str:
    """Lowercased, whitespace-collapsed prose — for asserting a CLAIM, not typography.

    Markdown wraps at ~88 columns and carries `> ` blockquote prefixes, so a claim
    that reads as one sentence is stored with newlines and quote markers inside
    it: "an agent asking\\n> for a fleet restart" does not match the sentence it
    plainly states. Matching raw text makes a guard fail when a paragraph is
    REWRAPPED while the rule is unchanged — which is how a guard becomes noise and
    then gets deleted. Same lesson as the case-sensitive check that redded on the
    correct prose `your **OWN team** only`.

    Found by this guard failing on its own first run against text I had just
    written, which is the cheap way to find it.
    """
    return re.sub(r"[\s>]+", " ", text.lower())


R427_HEADING = "### R42.7 is NOT yours"


def test_persona_states_r42_7_is_infrastructure_and_asking_is_the_violation() -> None:
    """R42.7 is the carve-out NEXT to ours, and it is not ours (Q6, ai-maestro#76).

    Its subject is the server acting as the absorbed janitor daemon — "never an
    agent, never a title, holding no AID". Constraint (f) is what binds a COS: no
    agent may invoke it, and *an agent asking for a fleet restart remains an R42.1
    violation*. So the prohibition covers the REQUEST, not merely the act, and a
    persona that stated only "you cannot restart the fleet" would leave the polite
    ask looking available.

    This guard exists because of WHERE the rule sits. R42.8 (which this title DOES
    hold) and R42.7 (which it does not) are adjacent exceptions to the same rule,
    and the failure mode of adjacency is generalization: "R42 has exceptions and I
    hold one" decaying into "I hold the neighbouring one too". Naming R42.8 without
    naming its neighbour is the shape that permits it.

    Source: Emasoft/ai-maestro@governance-rules tip 7b5e02ca,
    design/specs/governance-spec.md (NORMATIVE per the 4.8.0 authority inversion).
    """
    section = _slice_unique(MAIN_AGENT.read_text(encoding="utf-8"), R427_HEADING, r"\n### ", "R42.1")
    lowered = _prose(section)

    # The load-bearing clause: the REQUEST is the offence. A guard that only
    # checked "no agent may invoke it" would stay green on a persona that dropped
    # this, and dropping it is precisely what makes asking feel available.
    assert re.search(r"asking for a fleet restart remains an r42\.1 violation", lowered), "(f) missing: the persona does not say that ASKING for a fleet restart is itself an R42.1 violation. Without it a reader concludes only that it cannot perform the restart, and routes the request to someone who can."
    assert "no agent may invoke it" in lowered, "(f) missing: the persona does not state that NO agent may invoke R42.7. Holding R42.8 makes the neighbouring exception read as available."
    # The subject line — infrastructure, not a title. Without it R42.7 reads as a
    # power some title holds, and the only question left is which one.
    assert "never a title" in lowered, "the persona does not say R42.7's subject is infrastructure that is never an agent and never a title. A capability with no stated holder invites the reader to nominate themselves."
    # (a) and (b) are the REASON it is safe to automate, and the reason an
    # agent-requested restart is not: a request selects a target (destroying
    # uniformity) and the selection expresses the requester's decision
    # (destroying zero-content).
    for token, why in (
        ("uniform", "(a) missing — a targeted restart is injection under another name"),
        ("zero content", "(b) missing — the operation's inability to express anything"),
    ):
        assert token in lowered, f"R42.7 stated without {token!r} — {why}"


R3910_ANCHOR = "- **An ASSISTANT is invisible to you unless R39.10"


def test_persona_states_r39_10_assistant_visibility_and_its_four_limits() -> None:
    """An ASSISTANT is uncontactable unless R39.10 opened it, and then narrowly.

    R39.7 makes a user's ASSISTANT invisible to every agent but the MANAGER.
    R39.10 is the ONLY door: once the user permits MANAGER collaboration, MANAGER
    may pair another agent with the ASSISTANT on ONE shared GitHub project. A COS
    can be that agent, so this binds — but the persona must carry the four limits
    that survive the opening, because each one is a way the door gets read as
    wider than it is.

    Asserted at the LIMIT level rather than on "R39.10", since naming the rule
    while omitting the limits is exactly the failure this file keeps finding: the
    dangerous reading is not "I may never contact an ASSISTANT" (harmlessly
    over-strict) but "collaboration was arranged, so the ASSISTANT is now a peer I
    may direct" — which is wrong on scope, on refusability, and on who may end it.
    """
    section = _slice_unique(MAIN_AGENT.read_text(encoding="utf-8"), R3910_ANCHOR, r"\n### ", "R41")
    lowered = _prose(section)

    assert "r39.7" in lowered, "the persona does not state the DEFAULT (R39.7 invisibility). Without the default, R39.10 reads as a general permission rather than an exception."
    assert re.search(r"shared github project", lowered), "the scope of the opening is unstated. R39.10 is scoped to ONE specific shared project; unscoped, it reads as general mutual visibility."
    assert "refusable" in lowered, "R41 missing: the persona does not say every task routed to an ASSISTANT is refusable. An ASSISTANT is never a forced mandate target, and a COS that assumes otherwise will read a refusal as insubordination."
    assert "generally visible" in lowered, "the non-expansion limit is missing: R39.10 does NOT make the ASSISTANT generally visible. This is the clause that stops one project's collaboration from being treated as standing contact."
    # The USER's override is last because it is the one a MANAGER-arranged
    # collaboration makes easiest to forget: the arrangement came from MANAGER,
    # so MANAGER feels like the authority that governs it. It is not.
    assert re.search(r"user may at any time", lowered), "the USER's override is missing. The user may order its ASSISTANT to stop or pause, or to refuse specific MANAGER orders, and that authority overrides the very MANAGER arrangement that created the link."


R52_HEADING = "## The Write Boundary — Two Roots"


def test_persona_states_r52_write_boundary_with_reads_unrestricted() -> None:
    """R52 confines WRITES to two roots — and leaves READS unrestricted.

    At runtime a COS is one of "the running server and its agents", so R52 binds
    it directly. Two failure directions, and the guard pins both: writing outside
    `~/.aimaestro/` + `~/agents/` (the rule's purpose — a shared host comes back
    unchanged), and over-applying it into a refusal to READ. The spec is explicit
    that the asymmetry is deliberate: "reading another tool's files is how a
    harness cooperates, writing them is how it corrupts them."

    The blind-spot clause is asserted because it is the session's recurring theme
    in the spec's own words: `write-boundary.ts` is a TEXTUAL scan, so a write
    routed through a local variable is invisible to it. A green gate proves the
    write was not SPELLED out-of-root — never that it was in-bounds.
    """
    section = _slice_unique(MAIN_AGENT.read_text(encoding="utf-8"), R52_HEADING, r"\n## ", "~/.aimaestro/")
    lowered = _prose(section)

    assert "~/agents/" in section, "R52.1 states TWO roots; the persona names only one. A single-root reading outlaws writing an agent's own working directory."
    assert re.search(r"reads are unrestricted", lowered), "the read/write asymmetry is missing. R52 restricts WRITES; a persona that states it as a blanket path rule produces an agent that will not read the files it needs, and cites governance for it."
    assert re.search(r"asking that cli", lowered), "R52.4 missing: where another tool's CLI owns a file, it is mutated by asking that CLI, never by hand-editing. Two writers over one file do not disagree until the other side changes its schema."
    # The enforcement's own stated limitation. Without this, a passing gate is
    # read as a verification — the exact class of defect this suite exists for.
    assert re.search(r"never proves the write was in-bounds", lowered), "the enforcement's STATED blind spot is missing. `write-boundary.ts` is a textual scan blind to a write through a local variable, so a green gate is not evidence the write was in-bounds."


CHECKLIST_HEADING = "### Terminal columns are checklist-gated"


def test_persona_states_checklist_gate_including_the_empty_checklist_shape() -> None:
    """A terminal column needs a checklist that EXISTS (>=1 box) and is fully checked.

    Two shapes are false completions and the second is the one that gets dropped:
    a terminal column with any unchecked box, and a terminal column with NO
    checklist at all. The "≥1 box" half was added 2026-07-31 (TRDD-9QV4ZCYY)
    because without it the gate was VACUOUS — stated only over boxes that are
    unchecked, it passes on a card with no boxes. Measured that day on ai-maestro:
    87 of 108 open cards and 46 archived `completed` cards carried no checklist,
    so the "hard gate" was inert across most of the corpus it governed.

    That is the same defect class this whole file guards, arriving from outside:
    a check that passes because it read nothing. So the assertion here is on the
    EMPTY-checklist half specifically — a persona could state the gate correctly
    for unchecked boxes and reproduce the original vacuity exactly.

    THIS GUARD WAS ITSELF VACUOUS ON ITS FIRST FALSIFICATION, for the identical
    reason it exists to catch. `≥1 box` appears TWICE in the section: once in the
    RULE, once in the paragraph EXPLAINING the rule. Seeding the deletion of the
    rule's `(≥1 box)` left the rationale's copy behind and a bare
    `"≥1 box" in section` stayed GREEN — a guard passing on prose that explains
    why a rule exists, after the rule itself was deleted. Same shape as the R42.8
    `"assistant" in section` case earlier in this thread, found the same way:
    by seeding, not by reading. The assertion now anchors the phrase to its
    RULE POSITION (`checklist exists (≥1 box)`), which the rationale cannot
    satisfy. Writing a rationale next to a rule makes the rule harder to guard —
    the words are present either way, so only position distinguishes them.
    """
    section = _slice_unique(
        MAIN_AGENT.read_text(encoding="utf-8"),
        CHECKLIST_HEADING,
        r"\n### ",
        "pre-block-column",
    )
    lowered = _prose(section)

    assert "checklist exists (≥1 box)" in lowered, (
        "the EXISTENCE half is missing from the RULE. Without '>=1 box' stated as a condition of the gate, it is the original vacuous form: expressed only over unchecked boxes, it passes on a card with no checklist at all. Anchored to rule position on purpose — the phrase also appears in the rationale below, where it cannot rescue a deleted rule."
    )
    assert "no checklist at all" in lowered, "the persona does not name the empty-checklist shape as a false completion. It is the shape that carried 87 of 108 cards past the gate."
    for col in ("complete", "published", "live"):
        assert col in lowered, f"terminal column {col!r} unnamed — the gate's scope is partial"
    assert re.search(r"transition into a terminal column", lowered), "the gate's SCOPE is missing: it binds the transition INTO a terminal column, not the card's whole life. Absent that, an open card with no checklist reads as a violation and the board fills with false flags."
    # The remedy matters as much as the detection: ticking boxes to clear the
    # gate manufactures the very evidence the checklist was supposed to be.
    assert re.search(r"never to tick the boxes retroactively", lowered), "the persona does not forbid retroactively ticking the boxes. That 'fixes' the flag by fabricating a verification record — strictly worse than the false completion it clears."


def test_persona_says_blocked_does_not_suspend_checking() -> None:
    """Blocked licenses stopping WORK, never stopping CHECKING (ARCHITECT, #131).

    Distinct from the enumeration guard above and worth its own assertion: an
    agent can name all three channels and still stop polling them the moment it
    declares itself blocked. ARCHITECT measured that exact conflation — fifteen
    consecutive truthful "blocked, stopping" replies while a directive addressed
    to them sat unread. Every report correct; four days lost. The failure is not
    a missing channel, it is a correct status sentence used as permission to stop
    looking.
    """
    bullet = _inbound_section()
    assert re.search(r"(?i)stopping work.{0,40}never.{0,20}stopping checking", bullet), "the inbound rule does not separate stopping WORK from stopping CHECKING. Without it, 'blocked on a human decision' silently reads as permission to stop polling, and each individual report stays true while the outage accumulates."


def test_session_start_hook_echoes_the_inbound_duty() -> None:
    """The wake-time surface must carry the duty, not only the persona.

    The persona is one copy, and a wake that never reads it never sees the rule.
    This hook's `summary(extra=...)` is the ONLY agent-visible output at wake —
    everything `format_status_summary` builds goes to a log file nothing reads
    then. Assert against the stdout path specifically, because a banner line
    would look identical in source while reaching no one.
    """
    src = (PLUGIN_ROOT / "scripts" / "amcos_session_start.py").read_text(encoding="utf-8")
    # Select the call that CARRIES `extra=`, not the first textual match. There
    # are two `out.summary(` sites and the first is a WARN early-exit, so
    # `src.index(...)` silently windows the wrong one — the selector picking a
    # true-but-irrelevant occurrence, which is the same failure this file
    # already guards twice (empty tools list, file-wide menu search).
    calls = [src[m.start() : m.start() + 900] for m in re.finditer(r"out\.summary\(", src)]
    assert calls, "no out.summary(...) call site found at all"
    call = next((c for c in calls if "extra=" in c), "")
    assert call, "no out.summary(...) passes `extra=`. `out.log(...)` writes to the LOG FILE, which nothing reads at wake — putting the inbound duty there is a false claim of wake-time coverage."
    for token, why in (
        ("amp-inbox", "channel 1 unnamed in the wake echo"),
        ("peer sessions", "channel 2 unnamed in the wake echo"),
        ("gh issue list", "channel 3 unnamed in the wake echo"),
    ):
        assert token in call, f"{why} — `{token}` absent from the summary() call"
    assert re.search(r"(?i)never stopping checking", call), "the wake echo omits that being blocked does not suspend the check — the one rule that had to survive with no persona loaded."


def test_inbound_guard_is_scoped_not_file_wide() -> None:
    """Guard the guard: prove the section is a strict subset of the persona.

    If `_inbound_section` ever returned the whole file, every assertion above
    would pass on unrelated text — `SendMessage` and `amp-inbox` both appear
    elsewhere in this repo's prose. That is the vacuity this whole issue is about,
    reproduced inside its own fix.
    """
    section = _inbound_section()
    whole = MAIN_AGENT.read_text(encoding="utf-8")
    assert len(section) < len(whole) * 0.25, f"the inbound section is {len(section)} chars of a {len(whole)}-char persona — that is not a section, and the check has degenerated into a file-wide search that passes on the send-side text."


# A NAMED section anchor: a heading marker plus an actual title. ARCHITECT's
# discriminator (ai-maestro#131), and it came out of falsifying rather than
# reasoning: a bare "\n## " is a DELIMITER (legitimate as a section-END search),
# while "## Communication Permissions" NAMES a section and must never be located
# by first match.
_NAMED_SECTION_ANCHOR = re.compile(r"^\s*#{1,6}\s+\w{2,}")


def _first_match_section_selections(path: Path) -> list[str]:
    """Find `.index(X)` / `.find(X)` where X resolves to a NAMED section anchor.

    Resolves `NAME = "literal"` bindings in ANY scope before matching. Each
    widening came from a guard being vacuous on a tree it had not been measured
    against, in both directions:

    - literal-only (upstream's first version) catches nothing here — every
      selector in this file uses a constant (`SKILL_MENU_HEADING`,
      `INBOUND_HEADING`), so it scored 0 of 2 on this tree while looking enforced;
    - module-level-only (this file's first version) scored 1 of 2 on ARCHITECT's,
      whose anchor is bound inside the helper. Seeding that shape here showed the
      same hole locally — the guard passed green on it.

    **ADOPTION STEP, not optional:** run this against your own pre-fix commit and
    confirm it reddens. If it does not, it is not covering your shape, and a
    measurement inherited from the tree that produced the fix is worth nothing —
    that is the one failure in this family that cannot be fixed by writing the
    guard more carefully.

    KNOWN BLIND SPOTS, stated because a guard's misses are worth more to the next
    reader than its hit rate: an anchor built at runtime (f-string, concatenation,
    a value read from disk) or passed in as a parameter cannot be resolved
    statically and will NOT be caught. `_slice_unique` is such a case and is the
    SAFE path — its `anchor` is a parameter and it counts occurrences before
    selecting — so exclusion there is correct rather than a gap.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    consts: dict[str, str] = {}
    # ANY scope, not just module level. Collecting only `tree.body` was this
    # guard's own vacuity: ARCHITECT adopted that version unmodified and still
    # scored 1 of 2, because their miss binds the anchor INSIDE the helper
    # (`marker = "..."` then `persona.find(marker)`). Verified the same hole here
    # by seeding that exact shape — my guard passed green on it. A name reused in
    # two functions can in principle mis-resolve, but that yields a LOUD false
    # positive, never a silent miss, which is the correct direction for a net.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name):
                        consts[tgt.id] = node.value.value

    offenders: list[str] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr not in {"index", "find"} or not node.args:
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            value = arg.value
        elif isinstance(arg, ast.Name) and arg.id in consts:
            value = consts[arg.id]
        else:
            continue
        if _NAMED_SECTION_ANCHOR.match(value):
            offenders.append(f"line {node.lineno}: .{node.func.attr}({value!r})")
    return offenders


def test_no_first_match_selection_of_a_named_section() -> None:
    """Suite-wide convention: never locate a NAMED section by first match.

    Adopted after ARCHITECT and I each fixed a selector and each then found a
    SECOND one of the same shape in our own tree that the first fix did not
    prompt us to check. Fixing an instance demonstrably does not fix the class,
    in either of our hands — so the convention has to be enforced rather than
    remembered, because the condition under which it rots is that nothing is red.

    Deliberately narrow: it does not ban `.find`/`.index` generally. A frontmatter
    terminator, a section-END search, and an argv lookup are correct by
    definition, and a guard that fired on those would be noise — which is how a
    guard earns its way into being ignored.
    """
    offenders = _first_match_section_selections(Path(__file__))
    assert not offenders, (
        "first-match selection of a named section: " + "; ".join(offenders) + ". Use _slice_unique(), which refuses on ambiguity and asserts the "
        "slice carries a marker only the real section can carry. A first-match "
        "slice silently picks the wrong occurrence the moment a cross-reference "
        "names the section, and the guard then passes or fails for reasons "
        "unrelated to the invariant."
    )


# Every anchor shape, with its expected verdict. This is the miss list as CODE
# rather than prose — ARCHITECT found (ai-maestro#131) that they had fixed their
# all-scope resolver while seeding controls for only two shapes, so nothing
# proved the third stayed covered. Same hole was live here: my controls were
# ephemeral shell commands, so narrowing the resolver back to module scope would
# have left the suite green. Fixing a resolver and not pinning its shape is this
# thread's own defect one more time — a check that cannot fail, reporting a pass.
_ANCHOR_SHAPE_FIXTURE = """
_MODULE_CONST = "## Approval Tiers"


def literal(t):
    return t.index("## Communication Permissions")


def module_const(t):
    return t.find(_MODULE_CONST)


def function_local(t):
    marker = "### Inbound discipline"
    return t.find(marker)


def delimiter(t):
    return t.find("\\n## ")


def runtime_built(t, name):
    return t.find(f"## {name}")


def parameterised(t, anchor):
    return t.index(anchor)
"""

_SHAPES_COVERED = ("## Communication Permissions", "## Approval Tiers", "### Inbound discipline")


# ARITY is an axis independent of how the anchor is BOUND (literal, module
# constant, function-local, ...). CORE found the half neither ARCHITECT nor I had
# — **absence** — because ours were both ambiguity, so a canonical guard
# summarising our two findings as "refuse when the anchor is ambiguous" would have
# shipped `count > 1` (false when `count == 0`) and been adopted green by the one
# tree whose only real defect it could not see. `_slice_unique` already refused
# absence, because `== 1` happens to be the `!= 1` predicate CORE argues for:
# correct by construction, not by anticipation, and pinned by nothing.
#
# The two controls below are SEPARATE ON PURPOSE, per CORE's measurement. One test
# holding both assertions reds for either weakening under the SAME name — it
# reports that something broke without reporting which door is open. Split, the
# failing test NAME carries the axis, and the independence becomes an executable
# property rather than a claim: each reddens only for the weakening of its own
# predicate, and neither covers for the other.
_ARITY_DOC = "# Title\n\nbody with amp-inbox in it\n\n## Other\n"


def test_slice_unique_refuses_an_ABSENT_anchor() -> None:
    """Absence is the dangerous arity: `.find` → -1 → the slice becomes the DOCUMENT.

    Every positive assertion then passes, because a document trivially contains
    its own content. CORE measured that shape growing a slice 10,095 → 214,697
    chars with the test still green (ai-maestro#131).

    A marker assertion cannot substitute for this check: the vacuous slice is a
    SUPERSET of the real section, so "carries a marker only the real section can
    carry" passes on it. The discriminator for arity is arity.
    """
    with pytest.raises(AssertionError, match="is ABSENT"):
        _slice_unique(_ARITY_DOC, "### Nope Missing", r"\n#{1,3} ", "amp-inbox")


def test_slice_unique_refuses_a_DUPLICATED_anchor() -> None:
    """Ambiguity: a first-match slice would silently pick one of several.

    The realistic trigger is a cross-reference naming the section, added from
    elsewhere in the same file — an ordinary edit that makes the guard start
    passing or failing for reasons unrelated to the invariant.
    """
    with pytest.raises(AssertionError, match="occurs 2 times"):
        _slice_unique(_ARITY_DOC + "\n## Other\n", "## Other", r"\n#{1,3} ", "amp-inbox")


def test_slice_unique_returns_a_proper_subset_when_arity_is_correct() -> None:
    """The property a vacuous slice violates while every positive assertion passes."""
    section = _slice_unique(_ARITY_DOC, "# Title", r"\n#{1,3} ", "amp-inbox")
    assert len(section) < len(_ARITY_DOC), "a correctly-anchored slice must be smaller than the document; if it is not, the slice degenerated to the whole file and asserts nothing."


def test_first_match_detector_covers_every_anchor_shape(tmp_path: Path) -> None:
    """The shape table is EXECUTABLE: each anchor shape asserted, covered or not.

    Three shapes must be caught — literal, module constant, function-local. Each
    was added only after a guard measured green on the tree that produced it and
    blind on another's, so a regression here is not hypothetical: it is how both
    of the previous two versions failed.

    The two known-uncovered shapes are asserted as UNCAUGHT rather than omitted.
    A blind spot left out of the table is indistinguishable from one nobody
    thought of, and if coverage is ever extended this test says so out loud
    instead of passing quietly with a stale docstring.
    """
    fixture = tmp_path / "shapes.py"
    fixture.write_text(_ANCHOR_SHAPE_FIXTURE, encoding="utf-8")
    found = _first_match_section_selections(fixture)
    blob = " ".join(found)

    for anchor in _SHAPES_COVERED:
        assert anchor in blob, f"anchor shape {anchor!r} is NOT caught. If the resolver was narrowed (e.g. back to module scope only), the convention guard has silently stopped covering a shape it was widened to catch."
    assert "\n## " not in blob, "a bare delimiter was flagged — the guard now fires on correct code (section-END searches), and a noisy guard earns its way into being ignored."
    assert len(found) == len(_SHAPES_COVERED), f"expected exactly {len(_SHAPES_COVERED)} hits, got {len(found)}: {found}. A runtime-built (f-string) or parameterised anchor cannot be resolved by parsing; if one is now caught, extend _SHAPES_COVERED and the docstring's blind-spot list together."


def test_declared_tools_survives_a_comment_in_the_block() -> None:
    """A `#` comment inside `tools:` must not truncate the parsed list.

    Regression pin. The reader used to end the block at any non-`- Tool` line, so
    a leading comment yielded `[]` — and `[]` passes every check that intersects
    against a forbidden set. Two shipped agents lead their block with a comment
    recording that a spawn tool was deliberately removed (COS#27), so the note
    explaining the safety property disabled the test enforcing it. Both spellings
    are asserted: leading comment, and comment interleaved between entries.
    """
    leading = "---\ntools:\n  # why there is no spawn tool\n  - Bash\n  - Read\n---\n"
    assert _declared_tools(leading) == ["Bash", "Read"], f"a leading comment truncated the tools list to {_declared_tools(leading)} — an empty list silently passes every forbidden-tool check, which is how a guard stops guarding."
    interleaved = "---\ntools:\n  - Bash\n\n  # note\n  - Read\nskills:\n  - x\n---\n"
    assert _declared_tools(interleaved) == ["Bash", "Read"], f"comment/blank between entries truncated the list to {_declared_tools(interleaved)}"
    assert _declared_tools("---\ntools:\n  - Bash\nskills:\n  - x\n---\n") == ["Bash"], "a genuine top-level key must still END the block"


def test_every_subagent_declares_a_parseable_tool_allowlist() -> None:
    """Every subagent must parse to a NON-EMPTY allowlist.

    This is the assertion that would have caught the parser bug on the day the
    COS#27 comments landed. An agent whose allowlist reads as empty is
    indistinguishable — to every guard in this file — from one that declares
    nothing and inherits the full tool surface.
    """
    empty = [a.name for a in AGENT_FILES if a != MAIN_AGENT and not _declared_tools(a.read_text(encoding="utf-8"))]
    assert not empty, f"{empty} parse to an EMPTY tools allowlist. Either the agent really declares none (it then inherits everything, including the native cross-session transport), or the reader is truncating — both are defects, and both make every tool check on that file vacuous."


def test_subagent_transport_guard_scans_a_real_population() -> None:
    """Guard the guard: an empty subagent list would pass the check above vacuously."""
    subagents = [a for a in AGENT_FILES if a != MAIN_AGENT]
    assert len(subagents) >= 5, f"only {len(subagents)} subagent(s) discovered — the allowlist check above asserts nothing on an empty or truncated population."
    assert all(_declared_tools(a.read_text(encoding="utf-8")) for a in subagents), "a subagent declares NO tools at all, which parses as an empty allowlist and would pass the transport check while actually inheriting everything."
