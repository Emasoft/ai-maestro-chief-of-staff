"""Real (non-mocked) guard tests for the R26-R40 governance propagation (COS#21).

These assert the COS plugin internalized the AI Maestro security-governance core
(GOVERNANCE-RULES.md R26-R40): the persona carries the rule table, the old-model
statements are reversed (the MANAGER creates teams + the 5-base; the COS completes
under a mandate; agents never hold a governance password; installs route via the
core skills, not the Claude CLI), and the 5-base-invariant / R31-FREEZE gap is
filled in the boundaries doc + README. They read the real files; a regression
turns the matching test red. (This is the COS equivalent of the MANAGER plugin's
governance-scenarios — COS ships pytest guards, not markdown scenarios.)
"""

from __future__ import annotations

import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
AGENTS = PLUGIN_ROOT / "agents"
DOCS = PLUGIN_ROOT / "docs"
SKILLS = PLUGIN_ROOT / "skills"
PERSONA = AGENTS / "ai-maestro-chief-of-staff-main-agent.md"


def test_persona_has_r26_r40_governance_section() -> None:
    """The COS persona carries the R26-R40 governance section citing the key rules."""
    text = PERSONA.read_text(encoding="utf-8")
    assert "R26-R40" in text, "persona missing the R26-R40 governance section"
    for rule in ("R26", "R28", "R29", "R30", "R31", "R32", "R36", "R39"):
        assert rule in text, f"persona governance section missing {rule}"


def test_persona_team_model_reversed_to_manager_creates() -> None:
    """Persona states the MANAGER creates the team+COS+5-base; no old 'COS forms team' / 'R12'."""
    text = PERSONA.read_text(encoding="utf-8")
    low = text.lower()
    assert "you do not form teams" in low or "manager creates the team" in low, (
        "persona must state the MANAGER (not the COS) creates the team"
    )
    assert not re.search(r"\bR12\b", text), "persona still cites the old R12 for the 5-base (now R30/R31)"
    assert "you form teams after manager" not in low, "persona still says the COS forms teams"


def test_perm_mgmt_skill_clean_of_agent_password() -> None:
    """The permission-management skill tree holds no agent-held governance password / --password (R32)."""
    pm = SKILLS / "amcos-permission-management"
    offenders = []
    for f in pm.rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        if re.search(r"--password|governancePassword|GOV_PASSWORD", t):
            offenders.append(f.relative_to(PLUGIN_ROOT).as_posix())
    assert not offenders, f"agent-held password mechanism still present in: {offenders}"


def test_no_agent_held_password_anywhere_in_agent_facing_docs() -> None:
    """No command/skill/agent doc reintroduces an agent-held governance password (R32, TRDD-1846EVM2).

    The narrower test above passed for months while commands/amcos-request-approval.md
    documented --governance-password with a worked example — a guard scoped to one skill
    cannot see the same defect one directory over. This one scans every agent-facing doc
    tree. Prohibition prose is fine; a FLAG, a payload FIELD, or a $-substituted literal
    is not.
    """
    offenders = []
    for tree in ("commands", "skills", "agents"):
        for f in (PLUGIN_ROOT / tree).rglob("*.md"):
            t = f.read_text(encoding="utf-8")
            if re.search(r"--governance-password|\"governancePassword\"|\$GOV_PWD", t):
                offenders.append(f.relative_to(PLUGIN_ROOT).as_posix())
    assert not offenders, (
        f"agent-held governance-password mechanism present in: {offenders}. "
        "R32: a sudo password is requested only of the USER, only via the UI — "
        "no flag, no payload field, no substituted literal."
    )


def test_approval_coordinator_no_agent_password() -> None:
    """amcos-approval-coordinator no longer holds/passes a governance password; authz is AID (R32/R28)."""
    t = (AGENTS / "amcos-approval-coordinator.md").read_text(encoding="utf-8")
    assert "--password" not in t and "governancePassword" not in t, (
        "approval-coordinator still references an agent-held governance password"
    )
    assert "R32" in t and "AID" in t, "approval-coordinator must state AID-based authz (R32/R28)"


def test_team_create_delete_is_manager_only() -> None:
    """The team-registry spec marks team create/delete MANAGER-only and drops --password (R29.1/R32)."""
    t = (DOCS / "TEAM_REGISTRY_SPECIFICATION.md").read_text(encoding="utf-8")
    assert "MANAGER-only" in t, "team-spec must mark team create/delete MANAGER-only"
    assert "--password" not in t, "team-spec still shows an agent-passed --password"


def test_role_boundaries_has_5base_invariant_and_freeze() -> None:
    """ROLE_BOUNDARIES states the invariant 5-base and the R31 incomplete-team FREEZE; MANAGER may create agents."""
    t = (DOCS / "ROLE_BOUNDARIES.md").read_text(encoding="utf-8")
    assert "FROZEN" in t and "R31" in t, "ROLE_BOUNDARIES missing the R31 incomplete-team FREEZE"
    assert "5-member base is invariant" in t or "5 base members" in t, (
        "ROLE_BOUNDARIES missing the invariant-5-base statement"
    )
    assert "Create agents directly (delegates to AMCOS)" not in t, (
        "ROLE_BOUNDARIES still says the MANAGER cannot create agents directly (contradicts R29.1)"
    )


def test_readme_has_foundational_security_rules() -> None:
    """README documents the R26-R40 foundational security rules + the incomplete-team FREEZE."""
    t = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    assert "R26-R40" in t, "README missing the R26-R40 section"
    assert "FREEZE" in t or "frozen" in t.lower(), "README missing the incomplete-team FREEZE"


def test_install_routes_via_core_skills_not_claude_cli() -> None:
    """Plugin install/config routes via the core ai-maestro skills, never the Claude CLI (R27)."""
    for rel in ("agents/amcos-plugin-configurator.md", "commands/amcos-configure-plugins.md"):
        t = (PLUGIN_ROOT / rel).read_text(encoding="utf-8")
        assert "claude plugin install" not in t and "claude plugin uninstall" not in t, (
            f"{rel} still calls the Claude CLI directly for install (violates R27.2)"
        )


def test_role_briefing_comm_routing_not_user_directly() -> None:
    """role-briefing escalates via the COS/MANAGER, not 'message/escalate user directly' (R38/R39)."""
    t = (SKILLS / "amcos-onboarding" / "references" / "role-briefing.md").read_text(encoding="utf-8")
    low = t.lower()
    assert "message user directly" not in low, "role-briefing still says 'message user directly'"
    assert "escalate to user" not in low, "role-briefing still has a bare 'escalate to user' comm-routing line"


def test_no_escalation_to_generic_user_anywhere() -> None:
    """Plugin-wide: human-in-the-loop escalation addresses the MAESTRO, never a generic 'user' (R36/R37; MANAGER Ruling 1)."""
    pat = re.compile(r"escalate to (the )?user|notify user directly|contact user for", re.I)
    offenders = []
    for sub in ("agents", "commands", "skills", "docs", "shared"):
        for f in (PLUGIN_ROOT / sub).rglob("*.md"):
            if pat.search(f.read_text(encoding="utf-8")):
                offenders.append(f.relative_to(PLUGIN_ROOT).as_posix())
    if pat.search((PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")):
        offenders.append("README.md")
    assert not offenders, f"escalation to a generic 'user' (not the MAESTRO) still present in: {offenders}"
