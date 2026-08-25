#!/usr/bin/env python3
"""PRRD citation + rule-version integrity gate (RP-CITATION-01..03, ai-maestro#145).

Two halves, per the ratified spec (role-plugins-spec.md 1.2.0 @ 9422ec53):

1. Citation→version gate — every pinned citation (`PRRD G<n>.<v>` / `PRRD S<n>.<v>`)
   in shipped prose resolves against THIS repo's own PRRD: number exists, tier
   letter matches, version current.
2. Text→version hash gate — each rule's whole block is hashed against its version
   (committed fixture design/requirements/PRRD-rule-hashes.json), so a text edit
   without a version bump goes red. This is the half a resolution check cannot
   see: a stale pointer announces itself on the first lookup; a pointer to
   silently-mutated content never does.

Implementation constraints carried from RP-CITATION-03 (each a measured defect):
- The rule block is captured bullet → next top-level bullet / heading / EOF —
  NOT a one-line `re.M` regex, which silently truncates wrapped rules so an edit
  to a continuation line hashes identically (the gate's own defect class).
- Whitespace is normalized before hashing: a reflow is not a revision.
- The corpus excludes this gate, its test, and its fixture (self-exclusion), and
  archived terminal cards are exempt by their `column:` PROPERTY, never a path
  list (a path list over-covers or goes stale on the next archival).
- Non-vacuity keys on INPUT CONSUMED: zero files scanned is exit 2
  (could-not-run), never a pass. Zero citations over a real scan is the
  legitimate vacuous green of RP-CITATION-01.
- Site classification (RP-CITATION-02) is decided by what the sentence DOES with
  the version: historical narration (successor named in the same line) and
  grammar examples (code fences / inline code spans) are exempt. The heuristics
  deliberately prefer missing a real dangle over redding on a grammar example —
  a checker that reds on examples gets deleted, after which both defect
  directions run free.

Exit codes: 0 = green, 1 = findings, 2 = could-not-run (empty corpus / no PRRD).
`--update-hashes` regenerates the fixture — run it ONLY after a deliberate rule
edit that also bumped the version (a hash mismatch usually means "bump the rule,
THEN set the hash", not "the fixture is stale").
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PRRD_PATH = REPO_ROOT / "design" / "requirements" / "PRRD.md"
HASHES_PATH = REPO_ROOT / "design" / "requirements" / "PRRD-rule-hashes.json"

# Self-exclusion (RP-CITATION-03: the corpus is part of the selector).
SELF_EXCLUDED = {
    "scripts/amcos_citation_gate.py",
    "tests/test_citation_integrity.py",
    "design/requirements/PRRD-rule-hashes.json",
}

# Archive-eligible terminal columns (property, not path — 3P-ZON-05 set + refused).
TERMINAL_COLUMNS = {
    "complete", "completed", "cancelled", "superseded", "published", "live", "refused",
}

RULE_START_RE = re.compile(r"^- \*\*([GS])(\d+)\.(\d+)\*\*")
PINNED_CITE_RE = re.compile(r"\bPRRD\s+([GS])(\d+)\.(\d+)\b")


def parse_prrd_rules(text: str) -> dict[str, tuple[str, str]]:
    """Parse rule blocks out of PRRD text.

    Returns {"<letter><number>": (version, normalized_block_text)}.
    A rule block runs from its `- **G<n>.<v>**` bullet to the next top-level
    bullet, heading, or EOF — continuation lines included (RP-CITATION-03).
    """
    rules: dict[str, tuple[str, str]] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = RULE_START_RE.match(lines[i])
        if not m:
            i += 1
            continue
        letter, number, version = m.groups()
        block = [lines[i]]
        i += 1
        while i < len(lines) and not RULE_START_RE.match(lines[i]) and not lines[i].startswith("#"):
            # A new top-level bullet that is NOT a rule also ends the block.
            if lines[i].startswith("- "):
                break
            block.append(lines[i])
            i += 1
        key = f"{letter}{number}"
        if key in rules:
            # Duplicate rule number in the canon is itself a defect.
            raise ValueError(f"duplicate rule number in PRRD: {key}")
        rules[key] = (version, normalize(" ".join(block)))
    return rules


def normalize(text: str) -> str:
    """Whitespace-normalize: a reflow is not a revision (RP-CITATION-03)."""
    return " ".join(text.split())


def rule_hash(normalized_block: str) -> str:
    return hashlib.sha256(normalized_block.encode("utf-8")).hexdigest()


def compute_hashes(prrd_text: str) -> dict[str, str]:
    """{"G1.1": sha256, ...} for every rule in the given PRRD text."""
    return {
        f"{key}.{version}": rule_hash(block)
        for key, (version, block) in parse_prrd_rules(prrd_text).items()
    }


def is_terminal_card(text: str) -> bool:
    """True when the file's frontmatter says `column: <terminal>` (property check)."""
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    m = re.search(r"^column:\s*(\S+)\s*$", text[3:end], re.M)
    return m is not None and m.group(1) in TERMINAL_COLUMNS


def scan_citations(
    files: list[tuple[str, str]], rules: dict[str, tuple[str, str]]
) -> tuple[list[str], int, int]:
    """Check every pinned citation in the given (relpath, content) corpus.

    Returns (findings, files_scanned, citations_checked).
    """
    findings: list[str] = []
    citations = 0
    for relpath, text in files:
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue  # grammar example (RP-CITATION-02)
            for m in PINNED_CITE_RE.finditer(line):
                # Grammar example: the citation sits inside an inline code span.
                if line.count("`", 0, m.start()) % 2 == 1:
                    continue
                # Historical narration: successor named in the same line.
                if "→" in line or "->" in line or "fixed:" in line.lower():
                    continue
                citations += 1
                letter, number, version = m.groups()
                key = f"{letter}{number}"
                cur = rules.get(key)
                if cur is None:
                    # Number may exist under the other tier letter.
                    other = rules.get(("S" if letter == "G" else "G") + number)
                    if other is not None:
                        findings.append(
                            f"{relpath}:{lineno}: PRRD {letter}{number}.{version} — tier letter "
                            f"mismatch: rule {number} is currently "
                            f"{'S' if letter == 'G' else 'G'}{number}.{other[0]}"
                        )
                    else:
                        findings.append(
                            f"{relpath}:{lineno}: PRRD {letter}{number}.{version} — dangling: "
                            f"rule {number} does not exist in the PRRD"
                        )
                elif cur[0] != version:
                    findings.append(
                        f"{relpath}:{lineno}: PRRD {letter}{number}.{version} — superseded pin: "
                        f"current is {letter}{number}.{cur[0]} (float to `PRRD {letter}{number}` "
                        f"unless the version itself is load-bearing)"
                    )
    return findings, len(files), citations


def check_hashes(prrd_text: str, fixture: dict[str, str]) -> list[str]:
    """Text→version hash gate over the live PRRD against the committed fixture."""
    findings: list[str] = []
    for key, (version, block) in parse_prrd_rules(prrd_text).items():
        pinned = f"{key}.{version}"
        want = fixture.get(pinned)
        got = rule_hash(block)
        if want is None:
            findings.append(
                f"PRRD.md: {pinned} has no committed hash — if this is a deliberate new "
                f"version, regenerate the fixture (scripts/amcos_citation_gate.py --update-hashes)"
            )
        elif want != got:
            findings.append(
                f"PRRD.md: {pinned} text changed WITHOUT a version bump (hash mismatch). "
                f"The usual repair is: bump the rule's version, THEN regenerate the hash — "
                f"NOT regenerating the fixture over the unbumped text"
            )
    return findings


def shipped_corpus() -> list[tuple[str, str]]:
    """Git-tracked .md files, minus the canon itself, self-exclusions, and
    archived terminal cards (by column: property)."""
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    files: list[tuple[str, str]] = []
    for rel in out.stdout.splitlines():
        if not rel or rel in SELF_EXCLUDED:
            continue
        if rel == "design/requirements/PRRD.md":
            continue  # the canon defines rules; it does not cite itself
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        if is_terminal_card(text):
            continue  # frozen card must not lie about what it was written against
        files.append((rel, text))
    return files


def main() -> int:
    ap = argparse.ArgumentParser(
        description="PRRD citation + rule-version integrity gate (RP-CITATION-01..03)")
    ap.add_argument("--update-hashes", action="store_true",
                    help="regenerate the committed hash fixture from the current PRRD")
    args = ap.parse_args()

    if not PRRD_PATH.exists():
        print("could-not-run: PRRD.md not found", file=sys.stderr)
        return 2
    prrd_text = PRRD_PATH.read_text(encoding="utf-8")

    if args.update_hashes:
        HASHES_PATH.write_text(
            json.dumps(compute_hashes(prrd_text), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {HASHES_PATH.relative_to(REPO_ROOT)}")
        return 0

    files = shipped_corpus()
    if not files:
        print("could-not-run: zero files scanned (empty corpus is never a pass)", file=sys.stderr)
        return 2

    rules = parse_prrd_rules(prrd_text)
    cite_findings, scanned, citations = scan_citations(files, rules)

    if not HASHES_PATH.exists():
        print("could-not-run: hash fixture missing — run --update-hashes on a verified tree",
              file=sys.stderr)
        return 2
    fixture = json.loads(HASHES_PATH.read_text(encoding="utf-8"))
    hash_findings = check_hashes(prrd_text, fixture)

    findings = cite_findings + hash_findings
    # Scope statement (RP-CITATION-03): green asserts citations + rule versions
    # ONLY; container-level stamps need their own independent witness.
    print(f"scanned {scanned} files, checked {citations} pinned citations, "
          f"{len(rules)} rules hashed")
    for f in findings:
        print(f"FINDING: {f}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
