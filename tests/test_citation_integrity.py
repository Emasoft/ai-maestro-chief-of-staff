"""Citation + rule-version integrity gate — live run and RP-CITATION-04 controls.

Adopts RP-CITATION-01..04 (ratified ai-maestro#145; role-plugins-spec.md 1.2.0
@ 9422ec53) for this repo (TRDD-TH95SZFZ). Acceptance is "seeded both
directions and observed" — never "a check exists" — so beyond the live-tree run
this module commits the four controls over SYNTHETIC text (never
mutate-and-restore of the live PRRD: an interrupted run corrupts the repo):

  A  word changed on a continuation line       -> REDS (no silent under-coverage)
  B  pure reflow, no wording change            -> GREEN (no false positive)
  C  fixture distinguishing the whole-block
     parser from the naive one-line one        -> REDS if it cannot
  D  the naive parser installed                -> A and C observed red-blind
                                                  before any control is trusted

Each control names its seeded input inline. The gate under test is
scripts/amcos_citation_gate.py; this file and that script are self-excluded
from the gate's own corpus (RP-CITATION-03: the corpus is part of the selector).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from amcos_citation_gate import (  # noqa: E402
    check_hashes,
    compute_hashes,
    normalize,
    parse_prrd_rules,
    rule_hash,
    scan_citations,
)

# ── synthetic canon: one rule whose body WRAPS onto a continuation line ──────
# (the exact defect class RP-CITATION-03 names: a one-line regex under re.M
# silently truncates wrapped rules)
SYNTH_PRRD = """\
# Rules

- **G1.2** — Every outbound GitHub write must begin with a one-line
  self-identification of the authoring agent, carrying no at-sign.
- **S2.1** — Spawn-approval timeout is sixty minutes for normal priority.
"""

# Control A input: "sixty" -> "ninety"... no — A must hit the CONTINUATION line.
# Seeded input: on rule G1.2's continuation line, "carrying" -> "bearing".
SYNTH_PRRD_A = SYNTH_PRRD.replace("carrying no at-sign", "bearing no at-sign")

# Control B input: pure reflow of G1.2 — same words, different wrapping.
SYNTH_PRRD_B = """\
# Rules

- **G1.2** — Every outbound GitHub write must begin with a one-line self-identification
  of the authoring agent, carrying no at-sign.
- **S2.1** — Spawn-approval timeout is sixty minutes for normal priority.
"""


def naive_parse(text: str) -> dict[str, tuple[str, str]]:
    """The WRONG parser (control D): one-line `re.M` regex — first line only."""
    out: dict[str, tuple[str, str]] = {}
    for m in re.finditer(r"^- \*\*([GS])(\d+)\.(\d+)\*\*(.*)$", text, re.M):
        letter, number, version, _rest = m.groups()
        out[f"{letter}{number}"] = (version, normalize(m.group(0)))
    return out


def hashes_of(rules: dict[str, tuple[str, str]]) -> dict[str, str]:
    return {f"{k}.{v}": rule_hash(block) for k, (v, block) in rules.items()}


def test_control_a_continuation_line_edit_reds() -> None:
    """A: a word changed on a continuation line (carrying->bearing) reds the hash gate."""
    baseline = compute_hashes(SYNTH_PRRD)
    findings = check_hashes(SYNTH_PRRD_A, baseline)
    assert findings, "continuation-line edit without a bump must red"
    assert any("G1.2" in f and "WITHOUT a version bump" in f for f in findings)


def test_control_b_pure_reflow_stays_green() -> None:
    """B: a pure reflow (same words, new wrapping) of G1.2 produces zero findings."""
    baseline = compute_hashes(SYNTH_PRRD)
    assert check_hashes(SYNTH_PRRD_B, baseline) == [], "a reflow is not a revision"


def test_control_c_parser_sees_the_continuation_line() -> None:
    """C: the wrapped-rule fixture separates the whole-block parser from the naive one."""
    real_base = parse_prrd_rules(SYNTH_PRRD)
    real_edit = parse_prrd_rules(SYNTH_PRRD_A)
    assert real_base["G1"][1] != real_edit["G1"][1], (
        "whole-block parser must see the continuation-line difference"
    )


def test_control_d_naive_parser_observed_blind() -> None:
    """D: with the naive one-line parser installed, controls A and C go blind — observed."""
    naive_base = naive_parse(SYNTH_PRRD)
    naive_edit = naive_parse(SYNTH_PRRD_A)
    # The naive parser hashes the edited canon IDENTICALLY (A would stay green):
    assert hashes_of(naive_base) == hashes_of(naive_edit), (
        "expected the naive parser to be blind to the continuation-line edit — "
        "if this fails, the fixture no longer discriminates and control C is untrusted"
    )
    # ...while the real parser reds on the same seeded input (the discrimination):
    assert hashes_of(parse_prrd_rules(SYNTH_PRRD)) != hashes_of(parse_prrd_rules(SYNTH_PRRD_A))


def test_citation_gate_directions_on_synthetic_corpus() -> None:
    """Citation gate: dangling pin, superseded pin, and tier mismatch each red; a current pin, narration, and fenced examples stay green."""
    rules = parse_prrd_rules(SYNTH_PRRD)
    corpus = [(
        "docs/sample.md",
        "Cites PRRD G1.2 correctly.\n"          # current pin -> green
        "Cites PRRD G9.1 which never existed.\n"  # dangling -> red
        "Cites PRRD S2.0 which is superseded.\n"  # superseded -> red
        "Cites PRRD G2.1 with the wrong tier.\n"  # tier mismatch -> red
        "History: PRRD G1.1 → G1.2 narration stays exempt.\n"
        "```\nPRRD G7.7 inside a fence is a grammar example\n```\n"
        "Inline `PRRD G8.8` code span is exempt too.\n",
    )]
    findings, scanned, citations = scan_citations(corpus, rules)
    assert scanned == 1 and citations == 4
    assert len(findings) == 3
    assert any("G9.1" in f and "dangling" in f for f in findings)
    assert any("S2.0" in f and "superseded pin" in f for f in findings)
    assert any("G2.1" in f and "tier letter" in f for f in findings)


def test_live_tree_gate_is_green_and_non_vacuous() -> None:
    """Live run: the shipped gate exits 0 over a non-empty scanned corpus (exit 2 = could-not-run is a failure here)."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "amcos_citation_gate.py")],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, f"gate not green:\n{proc.stdout}\n{proc.stderr}"
    m = re.search(r"scanned (\d+) files", proc.stdout)
    assert m and int(m.group(1)) > 0, "non-vacuity: zero files scanned is never a pass"


def test_hash_fixture_matches_live_prrd() -> None:
    """The committed hash fixture is exactly what --update-hashes would emit for the live PRRD (no stale or missing entries)."""
    import json
    prrd = (REPO_ROOT / "design" / "requirements" / "PRRD.md").read_text(encoding="utf-8")
    fixture = json.loads(
        (REPO_ROOT / "design" / "requirements" / "PRRD-rule-hashes.json").read_text("utf-8")
    )
    assert fixture == compute_hashes(prrd)
