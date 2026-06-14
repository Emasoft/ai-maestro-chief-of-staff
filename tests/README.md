# Tests

Real, non-mocked tests for the `ai-maestro-chief-of-staff` plugin. Every test
reads the actual shipped files or imports the actual scripts — there are no
mocks, fakes, or conceptual tests. A test going red means a real regression.

## How to run

The canonical gate (exactly what `scripts/publish.py` runs before a release):

```bash
uv run --with pytest pytest tests/ -x -q --tb=short
```

The contributor-facing runner — same pytest run, plus a Unicode result table
(test name + docstring + outcome) and a 0/non-zero exit:

```bash
uv run --with pytest python tests/run-all-tests.py
```

Both exit 0 on all-pass and non-zero on any failure, so CI and a human get the
same verdict.

## What is covered

| File | Covers |
|------|--------|
| `test_component_contracts.py` | Every skill, agent, command, and hook + the manifests. Parametrized + dynamically discovered, so a new component is covered automatically. Asserts: parseable frontmatter, present name/description, skill name == dir, every relative SKILL.md link resolves, hooks.json valid + its scripts exist, plugin.json `dependencies` array, agent.toml CC floor. |
| `test_governance_structure.py` | The issue-#17 governance fixes stay in place: the four design zones, PRRD `project-id:` + SILVER rules, all TRDDs on the v2 `column:` schema (no v1 `status:`), the ORCH-owned dialog-loops doc, and refreshed docs free of the stale 5-status-as-workflow framing. |
| `test_memory_skills.py` | This plugin's ADOPTION of the janitor-hosted global 3-scope memory system (TRDD-59581001): the per-plugin `cos-memory-*` skills + `rules/memory-protocol.md` mirror are removed, `CLAUDE.md` points at the global `janitor-memory-*` skills + the recall rule and keeps the COS-specific moments, `.gitignore` re-includes `.claude/project/memory/**` (no bare `.claude/` line), the seeded PROJECT hub + `MEMORY.md` are schema-valid, and no live surface still wires the removed skills. (Memory BEHAVIOR is the janitor's suite, not duplicated here.) |

Validator behavior is NOT tested here: this plugin ships no local validator
scripts. All plugin validation runs through the remote CPV validator
(`cpv-remote-validate plugin . --strict`), which carries its own test suite
upstream in `Emasoft/claude-plugins-validation`.

## Conventions

- **No mocks.** If a script needs a live service to test, we test its pure
  logic offline instead of mocking the service.
- **pytest style** — module-level `def test_*` functions, each with a one-line
  docstring (the runner prints it as the test's description).
- **Stdlib + pytest only** — the plugin declares zero runtime dependencies, so
  the tests do too (frontmatter is parsed with a tiny stdlib helper, not PyYAML).
- Slow tests (those that need heavy deps or are skipped on CI) are marked 🐌 in
  the result table. There are currently none — the whole suite runs in well
  under a second.
