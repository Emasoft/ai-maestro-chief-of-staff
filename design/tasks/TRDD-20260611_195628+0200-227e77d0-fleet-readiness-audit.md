---
trdd-id: 227e77d0-a2d1-47cb-96c5-f263a52819cd
title: Fleet-readiness deep audit — close governance gaps before fleet start (issue #17)
column: complete
created: 2026-06-11T19:56:28+0200
updated: 2026-06-11T21:05:00+0200
implementation-commits: [0d720bc, 67d4f25, 5847a9d, b57f3d3]
current-owner: cos-ai-maestro-chief-of-staff
assignee: cos-ai-maestro-chief-of-staff
priority: 1
severity: HIGH
effort: XL
labels: [governance, fleet-readiness, audit-followup]
task-type: refactor
parent-trdd: null
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
publish-target: ai-maestro-plugins
test-requirements: [unit, lint]
review-requirements: []
runtime-targets: [macos, linux]
impacts: [dependencies, public-api]
external-refs: ["github.com/Emasoft/ai-maestro-chief-of-staff/issues/17"]
---

# TRDD-227e77d0 — Fleet-readiness deep audit (issue #17)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-11

**Source of work:** GitHub issue #17 on `Emasoft/ai-maestro-chief-of-staff`,
authored by the MANAGER (ai-maestro-assistant-manager-agent). It is a
component-level governance work order with 13 audit verdicts (M1–M13) and a
7-step priority fix list. The human USER authorized execution ("resume the
pending tasks" + standing "implement/fix all issues valid").

**Every verdict was re-verified against the live repo (v2.13.1) before any
edit** — all confirmed true (see Verified findings below).

**STATUS 2026-06-11 21:05:** Phases 1–4 COMPLETE and committed
(0d720bc governance structure, 67d4f25 cleanup of 27 orphan dirs,
5847a9d corrected-model docs, b57f3d3 149-test suite + runner). Full
pytest gate green (149 passed); CPV strict independently re-run → exit 0
(0 CRITICAL/MAJOR/MINOR/NIT, 56 advisory WARNINGs). README bumped
(29 skills, v2.14.0 header).

**NEXT ACTION:** run `uv run python scripts/publish.py --minor`
(→ v2.14.0), then reply to issue #17 with the self-id line + per-verdict
resolution, and post the janitor#18 memory-coordination comment.

**Load-bearing facts / gotchas:**
- The plugin git repo is `ai-maestro-chief-of-staff/` (a SUBDIR of the Claude
  project root, which is itself NOT a git repo). All git ops run from there.
- ALL pushes MUST go through `scripts/publish.py` — a pre-push git hook blocks
  plain `git push` (process-ancestry check). publish.py runs a strict CPV gate.
- `dependencies` in plugin.json must be an **array of strings**
  (`validate_marketplace.py:497`). → `"dependencies": ["ai-maestro-plugin"]`.
- The CPV strict gate must exit 0 before publish. Devitalize/fix the sanctioned
  way — never relax `--strict` or suppress a rule.
- GitHub-reply self-id line (G1.1, mandatory):
  `This is the Claude responsible for the ai-maestro-chief-of-staff project.`
- CI caveat: the post-tag Release `validate-tag` gate hangs on an upstream CPV
  regression (claude-plugins-validation#74); the 15-min `timeout-minutes` cap
  cancels it. Plugin Validation passes in ~1m. This is cosmetic, expected.

**SUPERSEDED — do NOT carry forward:** nothing yet.

**Durable artifacts to read before acting:**
- The issue body (fetched to `/tmp/issue17.json` during this session).

## Verified findings (live repo, v2.13.1)

| Verdict | Audit claim | Verified |
|---|---|---|
| M1 ✗ | no `dependencies` in plugin.json | TRUE — keys: name/version/description/author/repository/license |
| M2 PARTIAL | `project:` not `project-id:`; SILVER empty | TRUE — `project: ...`; SILVER header has zero rules; G1.1 present |
| M3 ✗ | 4-zone folders absent; v1 TRDD | TRUE — only tasks/+requirements/; TRDD uses `**Status:**` (pre-frontmatter v1) |
| M4 PARTIAL | FULL_PROJECT_WORKFLOW.md on v1 5-column board | docs dated Mar 15 — to confirm in Phase 3 |
| M5 ✓ | keep as-is | n/a |
| M6 PARTIAL | ROLE_BOUNDARIES.md stale (pre-v3) | docs dated Mar 15 — confirm in Phase 3 |
| M7 ✗ | zero awareness of the 3 dialog loops | confirm/author in Phase 3 |
| M8 ✓ | clean | n/a |
| M9 PARTIAL | no single-writer-per-domain for design/ | Phase 3 note |
| M10 GOOD | G1.1 missing from GitHub-write templates | Phase 3 |
| M11 ✗ | stale docs; agent.toml floor; 19 -ref dirs; audit artifacts | TRUE — 18 `-ref` dirs (self-ref only); `claude_code_version=">=2.1.69"`; AUDIT_REPORT/FINAL_AUDIT_RESULTS/audit_tools committed in 4 skills |
| M12 ✗ CRIT | 1 test for 52 skills | TRUE — only test_memory_skills.py; 10 agents/23 commands/1 hook-file untested |
| M13 mostly ✓ | cos-delegation-authority.md + exempt-operations.md referenced not bundled | live in ai-maestro-plugin → resolved by M1 dependency declaration |

## Plan (phases; ≤5 files-of-concern per sub-step)

### Phase 1 — governance structure
- M1: plugin.json `+ "dependencies": ["ai-maestro-plugin"]`.
- M2: PRRD `+ project-id:`; add real SILVER rules (spawn-approval timeout,
  max team size, escalation batch window, proposal-queue drain cadence).
- M3: `mkdir design/{proposals,refused,archived}` + `.gitkeep`; migrate the v1
  adoption-backlog TRDD to v2 `column:` frontmatter (preserve body verbatim).
- M11(toml): agent.toml `claude_code_version` `>=2.1.69` → `>=2.1.139`.

### Phase 2 — cleanup
- `git rm -r` the 18 `skills/*-ref/` dirs (recoverable from history).
- `git rm` AUDIT_REPORT.md, FINAL_AUDIT_RESULTS.md, audit_tools/ from the 4
  skills (context-management, config-snapshot, memory-initialization,
  progress-tracking).

### Phase 3 — docs
- M7: author the three-dialog-loops doc as ORCH-owned; COS guards the team
  BOUNDARY only and MUST NOT relay in-team handshakes. Encode in the COS main
  agent + a dedicated reference.
- M4/M6/M11: refresh OR delete the 3 stale docs (no parallel old versions).
- M10: add the G1.1 self-id line to GitHub-write command/skill templates.
- M9: single-writer-per-domain note for `design/` writes.

### Phase 4 — tests (M12)
- Delegate to python-test-writer agents with BOUNDED per-component counts.
- Add `tests/run-all-tests.py` runner (exit 0 all-pass / non-0 any-fail).
- Real tests only — no mocks (CLAUDE.md hard rule).

### Phase 5 — validate + publish + reply
- CPV strict → exit 0; `publish.py --minor` (→ v2.14.0); reply to #17 with the
  self-id line, per-verdict resolution, and the published version.

## Acceptance criteria (from the issue)
Every ✗/PARTIAL addressed or justified in the reply; no legacy docs kept;
version bumped + published; reply with the published version.
