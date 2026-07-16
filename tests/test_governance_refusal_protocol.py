"""Real (non-mocked) guard tests for the refusal protocol — "an approver is a
GUIDE, not a GATE" (COS#28, USER-ratified 2026-07-16).

Per the decision documented in `test_governance_r26_r40.py`, the COS ships
**executable pytest guards** rather than a prose scenarios file: a guard reads
the real shipped persona and turns red on regression, whereas prose cannot fail.

Why this surface earns a guard: the failure mode it prevents is *invisible from
the refuser's side*. A correct refusal and a destructive one look identical in
the COS's own log — the damage happens downstream, in the proposer's session.
So the persona text IS the control, and silent erosion of it (a well-meaning
"tighten the persona" edit dropping the relay half, say) would be undetectable
in operation. These tests make that erosion loud.

The last test is deliberately cross-surface: it pins the persona's claim that
`respond --decision rejected` cannot emit a reasonless "no" to the actual
argparse definition in `scripts/amcos_approval_manager.py`. If someone makes
`--comment` optional later, the persona would be lying and the tool would
re-open exactly the hole this protocol exists to close.

Stdlib + pytest only, matching the rest of the suite.
"""

from __future__ import annotations

import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
PERSONA = PLUGIN_ROOT / "agents" / "ai-maestro-chief-of-staff-main-agent.md"
APPROVAL_MANAGER = PLUGIN_ROOT / "scripts" / "amcos_approval_manager.py"


def _persona() -> str:
    """Persona text with every whitespace run collapsed to a single space.

    The persona is hard-wrapped prose, so a rule can legitimately straddle a
    line break ("never refuse the\\n   need"). Matching raw text would make an
    innocent re-wrap turn this suite red while a DELETED rule is what must turn
    it red — so normalize first and assert on the meaning, not the layout.
    """
    return re.sub(r"\s+", " ", PERSONA.read_text(encoding="utf-8"))


def test_persona_has_first_class_guide_not_a_gate_section() -> None:
    """The persona carries a first-class 'GUIDE, not a GATE' refusal section (COS#28 ask)."""
    t = _persona()
    assert "GUIDE, Not a GATE" in t, "persona missing the guide-not-a-gate section heading"
    assert "A Refusal Is a Design Review" in t, "persona missing the refusal-is-a-design-review framing"


def test_persona_states_refusing_is_the_start_not_the_end() -> None:
    """The persona states that refusing STARTS the work on a proposal rather than ending it."""
    t = _persona()
    assert "START of the work on a proposal, not the end" in t, (
        "persona missing the 'refusing is the start, not the end' rule"
    )


def test_persona_carries_all_four_refusal_elements() -> None:
    """The persona spells out all four mandatory elements of any refusal it emits."""
    t = _persona()
    for element, needle in (
        ("precise defect", "The precise defect"),
        ("bar for acceptance", "The bar for acceptance"),
        ("invitation to re-propose", "invitation to re-propose"),
        ("push toward alternatives", "A push toward alternatives"),
    ):
        assert needle in t, f"persona refusal protocol missing element: {element}"


def test_persona_refuses_the_implementation_never_the_need() -> None:
    """The persona keeps the 'refuse the implementation, never the need' invariant."""
    t = _persona()
    assert "Refuse the implementation; never refuse the need" in t, (
        "persona missing 'refuse the implementation; never refuse the need'"
    )


def test_persona_requires_iteration_rounds() -> None:
    """The persona frames repeated refine-and-re-propose rounds as the process working."""
    t = _persona()
    assert "ITERATE" in t, "persona missing the iteration duty"
    assert "job working, not failing" in t, "persona missing 'rounds is the job working, not failing'"


def test_persona_states_the_channel_is_the_message_not_the_tool() -> None:
    """The persona states the AMP message is the channel and the tool is only the record."""
    t = _persona()
    assert "THE CHANNEL IS THE MESSAGE, NOT THE TOOL" in t, "persona missing the message-is-the-channel rule"
    assert "was never communicated" in t, (
        "persona missing 'a decision that exists only in the file record was never communicated'"
    )


def test_persona_says_passing_the_tool_check_does_not_discharge_the_message_duty() -> None:
    """The persona denies that satisfying the CLI's --comment check discharges the message duty."""
    t = _persona()
    assert "does NOT discharge the message" in t, (
        "persona must state that passing the tool check does not discharge the message duty"
    )


def test_persona_relay_half_carries_reasoning_down_intact() -> None:
    """The persona's COS-unique relay half forbids passing the MANAGER's verdict without its reasoning."""
    t = _persona()
    assert "RELAY half" in t, "persona missing the COS-unique relay half"
    assert "the bar, and the invitation intact" in t, (
        "relay half must require defect/bar/invitation to survive the hop down"
    )


def test_persona_relay_half_carries_counter_arguments_back_up() -> None:
    """The persona's relay half requires the proposer's counter-arguments to flow back up to the MANAGER."""
    t = _persona()
    assert "Carry the counter-arguments back UP" in t, "relay half must carry replies back up"
    assert "in both directions" in t, "relay half must state the dialogue survives the hop in both directions"


def test_persona_relay_half_refuses_to_invent_or_pass_a_bare_verdict() -> None:
    """The persona requires asking the MANAGER for missing refusal elements rather than inventing or forwarding a bare verdict."""
    t = _persona()
    assert "ask the MANAGER" in t, "relay half must require asking the MANAGER for missing elements"
    assert "do not invent them" in t, "relay half must forbid inventing the reasoning"


def test_persona_proposer_side_corollary_forbids_deleting_work_on_a_bare_no() -> None:
    """The persona forbids deleting working code that depended on a proposal on the strength of a bare 'no'."""
    t = _persona()
    assert "never delete working code that depended on a proposal" in t, (
        "persona missing the corollary's never-delete-working-code rule"
    )
    assert "ask first" in t, "persona corollary must require asking before destroying dependent work"


def test_persona_corollary_binds_from_the_moment_a_proposal_is_drafted() -> None:
    """The persona binds the corollary from draft time, forbidding pre-conceded destruction in the ask."""
    t = _persona()
    assert "DRAFT a proposal" in t, "corollary must bind from the moment a proposal is drafted"
    assert "cheap exit" in t, "corollary must explain that pre-conceding invites the approver's cheap exit"


def test_persona_names_the_github_issue_as_the_channel_absent_an_amp_thread() -> None:
    """The persona names the cross-repo GitHub issue as the message channel when no AMP thread exists."""
    t = _persona()
    assert "cross-repo GitHub issue IS the message" in t, (
        "persona must name the cross-repo issue as the channel where no AMP thread exists"
    )


def test_persona_points_at_the_canonical_write_up() -> None:
    """The persona points at the canonical USER-scope wikimem write-up of the principle."""
    t = _persona()
    assert "manager-is-a-guide-not-a-gate.md" in t, "persona missing the canonical write-up pointer"


def test_core_responsibility_names_the_guide_duty() -> None:
    """Core Responsibility 7 names the guide-not-gate duty so it is visible when scanning the list."""
    t = _persona()
    assert "Approval Filtering & Refusal Quality" in t, (
        "Core Responsibility 7 must name refusal quality, not filtering alone"
    )
    assert "GUIDE, not a GATE" in t, "Core Responsibility 7 must name the guide-not-gate duty"


def test_respond_verb_cannot_emit_a_reasonless_no() -> None:
    """The approval CLI's respond verb requires --comment, so a rejection can never be reasonless.

    Cross-surface guard: the persona asserts this property of the tool. If
    --comment ever becomes optional, the persona's claim silently becomes false
    and the reasonless-"no" hole reopens.
    """
    src = APPROVAL_MANAGER.read_text(encoding="utf-8")
    match = re.search(r'respond_parser\.add_argument\(\s*"--comment"\s*,\s*required=True', src)
    assert match is not None, (
        "amcos_approval_manager.py: `respond --comment` must stay required=True — "
        "the persona relies on a rejection never being reasonless"
    )
