"""Real (non-mocked) guard tests for the approval-tier / 3-pillars governance surface (COS#24).

This is the COS's answer to COS#24 B4 ("governance scenarios"). Per the decision
documented in `test_governance_r26_r40.py`, the COS ships **executable pytest
guards**, not a markdown scenarios file — a guard reads the real shipped files
and turns red on regression, whereas a prose scenario cannot fail. These cover
the governance surface added for COS#24 A/B: the R41 approval ladder + the
`min-approval-requirement:` field (B3), the granular `ama-*` repoint (A1), and
the COS-scoped 3-pillars block on the governance-adjacent sub-agents (A2/A3).

Stdlib + pytest only, matching the rest of the suite.
"""

from __future__ import annotations

from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
AGENTS = PLUGIN_ROOT / "agents"
SKILLS = PLUGIN_ROOT / "skills"
PERSONA = AGENTS / "ai-maestro-chief-of-staff-main-agent.md"

# The 5 governance/mandate-adjacent sub-agents that received the 3-pillars block
# (A2/A3). The 4 pure-monitoring agents are intentionally excluded — they touch
# no governance decision — so this list is exact, not "all sub-agents".
GOVERNANCE_SUBAGENTS = [
    "amcos-staff-planner",
    "amcos-approval-coordinator",
    "amcos-team-coordinator",
    "amcos-lifecycle-manager",
    "amcos-recovery-coordinator",
]


def test_persona_documents_min_approval_requirement_field() -> None:
    """The persona documents the R41 `min-approval-requirement:` field (B3)."""
    t = PERSONA.read_text(encoding="utf-8")
    assert "min-approval-requirement" in t, "persona missing the min-approval-requirement field"


def test_persona_documents_the_full_authority_ladder() -> None:
    """The persona states the complete R41 ladder none<orchestrator<chief-of-staff<manager<user."""
    t = PERSONA.read_text(encoding="utf-8")
    for rung in ("none", "orchestrator", "chief-of-staff", "manager", "user"):
        assert rung in t, f"persona approval ladder missing the '{rung}' rung"


def test_persona_states_cos_is_tier1_chief_of_staff_rung() -> None:
    """The persona states the COS is the Tier-1 approver at the chief-of-staff rung.

    Load-bearing: a COS that thinks it can approve above its rung would
    self-authorize manager/user-floored work — the exact failure R41 prevents.
    """
    t = PERSONA.read_text(encoding="utf-8")
    assert "chief-of-staff" in t and "Tier-1" in t, "persona must state COS = Tier-1 / chief-of-staff rung"
    assert "born approved" in t.lower() or "born-approved" in t.lower(), "persona missing the R41 born-approved rule"


def test_persona_repointed_to_granular_ama_skills_not_the_gone_monolith() -> None:
    """The persona references the granular ama-* skills, and only names the gone
    monolithic prrd-trdd-kanban skill in a historical/negated context (A1)."""
    t = PERSONA.read_text(encoding="utf-8")
    assert "ama-trdd-transition" in t, "persona missing the granular ama-trdd-transition reference"
    for line in t.splitlines():
        if "prrd-trdd-kanban" in line and "amcos-prrd-trdd-kanban" not in line:
            assert "replaced" in line or "no longer" in line or "monolithic" in line, (
                f"persona names the gone monolithic skill without a historical marker: {line.strip()!r}"
            )


@pytest.mark.parametrize("agent", GOVERNANCE_SUBAGENTS)
def test_governance_subagent_has_3pillars_block(agent: str) -> None:
    """Each governance-adjacent sub-agent carries the COS-scoped 3-pillars block (A2/A3)."""
    t = (AGENTS / f"{agent}.md").read_text(encoding="utf-8")
    assert "Governance awareness" in t, f"{agent} missing the 3-pillars governance block"
    assert "ama-trdd-transition" in t, f"{agent} block missing the granular ama-* reference"


@pytest.mark.parametrize("agent", GOVERNANCE_SUBAGENTS)
def test_governance_subagent_states_r69_no_amp_boundary(agent: str) -> None:
    """The block states the hard R6.9 boundary: sub-agents have no AMP identity.

    This is what keeps a sub-agent from claiming to approve/transition/message
    on its own — it must RETURN to the main COS agent, which relays.
    """
    t = (AGENTS / f"{agent}.md").read_text(encoding="utf-8")
    assert "R6.9" in t, f"{agent} block missing the R6.9 no-AMP-identity boundary"
    assert "no AMP identity" in t, f"{agent} block must state sub-agents have no AMP identity"


def test_wrapper_skill_dropped_stale_raw_script_tools() -> None:
    """The overlay wrapper no longer declares the retired raw-script allowed-tools (A1).

    The granular ama-* skills own those scripts now; the wrapper DELEGATES to
    them, so re-declaring get-prrd.py/findtrdd.py/kanban.py would be dead grant.
    """
    t = (SKILLS / "amcos-prrd-trdd-kanban" / "SKILL.md").read_text(encoding="utf-8")
    fm = t.split("---", 2)[1] if t.startswith("---") else ""
    for stale in ("get-prrd.py", "findprrd.py", "findtrdd.py", "kanban.py"):
        assert stale not in fm, f"wrapper allowed-tools still grants the retired script {stale}"
