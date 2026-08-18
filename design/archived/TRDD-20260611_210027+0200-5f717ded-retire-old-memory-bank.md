---
trdd-id: 5F717DED
title: Retire the old session memory bank per the ratified fleet three-scope convention
column: published
created: 2026-06-11T21:00:27+0200
updated: 2026-06-11T21:35:00+0200
implementation-commits: [0395d89, 42b78fa, 0b7a001]
published-version: 2.15.0
published-at: 2026-06-11T21:27:00+0200
current-owner: cos-ai-maestro-chief-of-staff
assignee: cos-ai-maestro-chief-of-staff
priority: 2
severity: MEDIUM
effort: L
labels: [memory-system, fleet-convention, retirement]
task-type: refactor
parent-trdd: TRDD-227e77d0
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
publish-target: ai-maestro-plugins
test-requirements: [unit, lint]
impacts: [public-api]
external-refs: ["github.com/Emasoft/ai-maestro-janitor/issues/18", "github.com/Emasoft/ai-maestro-janitor/issues/16"]
---

# TRDD-5f717ded — Retire the old session memory bank (ratified fleet convention)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-11

**Authority:** the janitor (memory-system owner) RATIFIED the fleet-wide
three-scope memory convention on
[janitor#18](https://github.com/Emasoft/ai-maestro-janitor/issues/18)
(comment 2026-06-11T18:51:58Z), answering the four open questions:

1. Live session memory → **LOCAL scope** `~/.claude/projects/<project-slug>/memory/`
   (outside the repo by construction). Both `.claude/<plugin>/` and
   `design/memory/` are **non-canonical** for memory.
2. Live memory is **never committed**. A tracked shared-knowledge bank, if
   ever wanted, goes at `<git-root>/memory/` (PROJECT scope), policed by the
   janitor `memory-scope-leak` detector.
3. The old `activeContext`/`progress`/`patterns` hook+CLI bank is
   **SUPERSEDED** by the markdown-notes + memgrep system → **option 3:
   retire/delete**, not path-fix. Valuable old-bank content migrates to
   one-fact-per-note markdown in LOCAL scope, symptom-indexed.
4. One fleet-wide convention; AMAMA ratified and is executing its own
   retirement. AMCOS publicly committed to this TRDD on janitor#18.

**AMCOS's replacement is ALREADY SHIPPED and compliant:** `cos-memory-recall`
/ `cos-memory-write` + `rules/memory-protocol.md` use exactly the LOCAL scope
path, memgrep-backed with the plain-grep fallback (the supported mode until
the janitor's binaries publish — janitor#16, closed as implemented).

**EXECUTED 2026-06-11 (USER go-ahead "Complete the pending tasks"):** commit
`0395d89` deleted the 4 bank scripts + 4 bank skills (278 files) and updated
agent.toml / README / main-agent / the 2 surviving cross-ref docs. No content
migration was needed — the repo held procedure docs only; live bank data
exists solely in user projects at runtime. Ships in v2.15.0 together with the
local-validator removal (TRDD-0263f190).

**NEXT ACTION:** mark `published` once v2.15.0 is live; report the version on
janitor#18.

## Verified retirement inventory (grep-verified 2026-06-11, v2.14.0 tree)

**Scripts to delete (4 — self-contained; only each other import them; no
hook, command, or agent imports):**
- `scripts/amcos_memory_manager.py` (the bank CLI; `memory_root` default `design/memory`)
- `scripts/amcos_memory_operations.py`
- `scripts/amcos_repair_memory.py`
- `scripts/amcos_snapshot_memory.py`

**Skills to delete (4 — the bank's documented surface):**
- `skills/amcos-memory-initialization/`
- `skills/amcos-context-management/`
- `skills/amcos-progress-tracking/`
- `skills/amcos-config-snapshot/`

**References to update (the 4 skills appear in each):**
- `ai-maestro-chief-of-staff.agent.toml` — remove the 4 bundled entries
- `README.md` — Skills (29)→(25); remove the 4 rows
- `agents/ai-maestro-chief-of-staff-main-agent.md` — remove the 4 skill refs;
  point memory duties at `cos-memory-recall` / `cos-memory-write`
- `tests/` — contract tests auto-adapt (dynamic discovery); delete any
  bank-specific assertions if present

**Content migration:** before deletion, check for still-valuable knowledge in
the old bank's templates/checklists; anything worth keeping becomes
one-fact-per-note markdown in the LOCAL scope (symptom-indexed
`description:`), per the ratified convention.

**Keep (already-compliant replacements):** `cos-memory-recall`,
`cos-memory-write`, `rules/memory-protocol.md`, `tests/test_memory_skills.py`.

**Out of scope:** `.claude/amcos/handoffs/` runtime (amcos_stop_check.py:158)
— handoff snapshots, not the memory bank; gitignored runtime state is the
correct pattern per the ratified Q2.

## Acceptance criteria

- Zero references to `amcos_memory_manager` / `design/memory` /
  `activeContext` remain in shipped surfaces (scripts/skills/agents/
  commands/README/agent.toml).
- Full pytest gate green; CPV strict exit 0.
- Published as a minor release; janitor#18 informed with the version.
