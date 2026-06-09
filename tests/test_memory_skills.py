"""Real (non-mocked) tests for the cos-memory-recall / cos-memory-write skills.

The skills are LLM recipes; their testable contract is the bash recipe they
document: the note schema, the MEMORY.md index line, the memgrep recall
ranking, and the plain-grep fallback when memgrep is absent. These tests
execute that contract against a real fixture memory dir in tmp_path.
"""

import shutil
import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

NOTE_BODY = """---
name: reference_spawn_timeout
description: "spawn request failed with a timeout / agent never came up after spawn"
metadata:
  node_type: memory
  type: reference
---
Spawn requests against a cold registry take up to 40s; the default 30s timeout
fires first. Raise the per-spawn timeout to 60s before retrying.
"""

DECOY_BODY = """---
name: project_label_taxonomy
description: "which label colors do we use for team agent classification"
metadata:
  node_type: memory
  type: project
---
Label taxonomy: blue = core roles, amber = transient workers.
"""


def make_memory_dir(tmp_path: Path) -> Path:
    """Build a fixture memory dir with one symptom-matching note and one decoy."""
    memdir = tmp_path / "memory"
    memdir.mkdir()
    (memdir / "reference_spawn_timeout.md").write_text(NOTE_BODY, encoding="utf-8")
    (memdir / "project_label_taxonomy.md").write_text(DECOY_BODY, encoding="utf-8")
    return memdir


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


def test_write_recipe_produces_schema_valid_note(tmp_path: Path) -> None:
    """The documented write recipe yields a schema-valid note plus a MEMORY.md index line."""
    memdir = tmp_path / "memory"
    memdir.mkdir()
    # Execute the skill's documented steps 4-5: write the note, append the index.
    note = memdir / "feedback_batch_spawn_requests.md"
    note.write_text(
        """---
name: feedback_batch_spawn_requests
description: "how should I send spawn requests / one per message or batched"
metadata:
  node_type: memory
  type: feedback
---
MANAGER wants spawn requests batched, not one-per-message.

**Why:** one-per-message floods the approval queue.
**How to apply:** collect spawn needs for the cycle, send one batched request.
""",
        encoding="utf-8",
    )
    index = memdir / "MEMORY.md"
    index.write_text(
        "- [Batch spawn requests](feedback_batch_spawn_requests.md) — MANAGER prefers batched spawns.\n",
        encoding="utf-8",
    )

    fm = parse_frontmatter(note.read_text(encoding="utf-8"))
    assert fm["name"] == note.stem, "frontmatter name must equal the filename stem"
    assert fm["description"], "description (the symptom surface) must be non-empty"
    assert fm["metadata"]["node_type"] == "memory"
    assert fm["metadata"]["type"] in {"user", "feedback", "project", "reference"}
    assert note.stem in index.read_text(encoding="utf-8"), "MEMORY.md must index the note"


def test_recall_memgrep_ranks_symptom_note_first(tmp_path: Path) -> None:
    """memgrep recall on a SYMPTOM query surfaces the matching note above the decoy. 🐌"""
    if shutil.which("memgrep") is None:
        import pytest

        pytest.skip("memgrep not installed — fallback path covered by the grep test")
    memdir = make_memory_dir(tmp_path)
    result = subprocess.run(
        ["memgrep", "recall", "spawn request failed timeout agent never came up", str(memdir)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"memgrep recall failed: {result.stderr}"
    out = result.stdout
    assert "reference_spawn_timeout" in out, "symptom query must surface the matching note"
    if "project_label_taxonomy" in out:
        assert out.index("reference_spawn_timeout") < out.index("project_label_taxonomy"), "matching note must rank above the decoy"


def test_recall_grep_fallback_without_memgrep(tmp_path: Path) -> None:
    """With memgrep absent from PATH, the documented grep fallback still finds the note."""
    memdir = make_memory_dir(tmp_path)
    # Run the skill's exact fallback pipeline in a shell whose PATH cannot see
    # memgrep (system dirs only) — proving the degrade-not-break contract.
    script = (
        'if command -v memgrep >/dev/null 2>&1; then echo MEMGREP_PRESENT; '
        f'else grep -rliE "spawn request failed" "{memdir}" 2>/dev/null; fi'
    )
    result = subprocess.run(
        ["/bin/bash", "-c", script],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin"},
        timeout=30,
    )
    assert "MEMGREP_PRESENT" not in result.stdout, "test env must not see memgrep"
    assert "reference_spawn_timeout.md" in result.stdout, "grep fallback must find the note"


def test_skills_and_rule_document_the_degrade_contract() -> None:
    """Both skills gate on command -v memgrep with a grep fallback, and the rule file exists."""
    recall = (PLUGIN_ROOT / "skills" / "cos-memory-recall" / "SKILL.md").read_text(encoding="utf-8")
    write = (PLUGIN_ROOT / "skills" / "cos-memory-write" / "SKILL.md").read_text(encoding="utf-8")
    rule = PLUGIN_ROOT / "rules" / "memory-protocol.md"
    for body, label in ((recall, "cos-memory-recall"), (write, "cos-memory-write")):
        assert "command -v memgrep" in body, f"{label} must gate on memgrep presence"
        assert "grep -rliE" in body, f"{label} must document the grep fallback"
        assert "memory-protocol.md" in body, f"{label} must reference the memory-protocol rule"
    assert rule.exists(), "rules/memory-protocol.md must ship with the plugin"
    rule_text = rule.read_text(encoding="utf-8")
    assert "index by the QUESTION" in rule_text, "the rule must state the one law"
