---
trdd-id: 59581001-4f47-470e-9f16-746ce5194962
title: Adopt the janitor-hosted global 3-scope memory system; remove per-plugin memory skills
column: published
created: 2026-06-14T01:39:17+0200
updated: 2026-06-14T18:17:05+0200
published-version: 2.16.0
published-at: 2026-06-14T18:15:00+0200
current-owner: cos-ai-maestro-chief-of-staff
assignee: cos-ai-maestro-chief-of-staff
priority: 2
severity: MEDIUM
effort: L
labels: [memory-system, fleet-convention, global-memory]
task-type: refactor
parent-trdd: TRDD-5f717ded
relevant-rules: [1]
release-via: publish
delivery: direct-push
target-branch: main
publish-target: ai-maestro-plugins
test-requirements: [unit, lint]
impacts: [public-api]
external-refs: ["github.com/Emasoft/ai-maestro-chief-of-staff/issues/18", "github.com/Emasoft/ai-maestro-assistant-manager-agent/issues/15"]
---

# TRDD-59581001 — Adopt the janitor-hosted GLOBAL memory system

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-14

**Source of work:** janitor work order on THIS repo's issue **#18**
("feat(memory): adopt the global janitor-hosted markdown memory system
(3-scope)"). It UPDATES the earlier ratified convention (TRDD-5f717ded /
janitor#18): the memory system is now **janitor-hosted and global** — role
plugins ship NO per-plugin memory skills. The MANAGER sequences the rollout
(assistant-manager#15). Authorized by the USER's standing directive ("follow
the memory-migration instructions from the github issues").

**✅ SHIPPED — v2.16.0 (2026-06-14T18:15+0200).** Both gates cleared, executed,
published, CI green (Plugin Validation + Release + Notify Marketplace all ✓).
Release: https://github.com/Emasoft/ai-maestro-chief-of-staff/releases/tag/v2.16.0
Reported on my-repo #18 (issuecomment-4702329568). Commits: 33e0971 (phase 1
bootstrap), ce0688c (migration), 8594049 (release bump). What landed: removed the
3 per-plugin memory surfaces; added CLAUDE.md (COS moments + fixed recall form);
repointed all live surfaces incl. the test (grep found more than the planned 5);
proactive contract in main agent + all 9 sub-agents; PROJECT scope bootstrapped;
test rewritten to validate adoption (121 pass; CPV strict + lint 0/0/0/0). This
TRDD is now terminal (published) — do not edit the body further.

Historical gate record (both now satisfied):
- **GATE 1 — janitor publishes bootstrap + fixed global skills: ✓ CLEARED.**
  janitor **v0.8.5** shipped 2026-06-14T15:28Z and the installed cache now has
  `.../ai-maestro-janitor/0.8.5/skills/janitor-memory-bootstrap` (+ recall/write/
  update). The `[janitor-reload]` heartbeat marker fired on this auto-update.
  The fixed `~/.claude/rules/markdown-memory-recall.md` rule was already installed.
- **GATE 2 — MANAGER sequences chief-of-staff: ✗ NOT yet met.** assistant-manager#15
  latest (MANAGER, 2026-06-14T04:36) only states AMAMA is "ready to fire on your
  publish ping" about its OWN migration (TRDD-d369cf76); no explicit "chief-of-staff,
  go" / rollout-slot for THIS plugin. Posted the publish-ping + sequencing request
  on assistant-manager#15 (issuecomment-4702224544) 2026-06-14T17:37; awaiting the go.
- **Also gated by approval tier:** this TRDD is `release-via: publish` + `impacts:
  [public-api]` → Tier-2, so the publish step needs MANAGER sign-off regardless.
- **In-session prerequisite:** this Claude Code session must `/reload-plugins`
  (can't be self-invoked — asked the USER) to register the 0.8.5 `janitor-memory-bootstrap`
  skill before step 1 can run.
Do NOT execute the migration until GATE 2 is met (MANAGER go on #15/#18).

**NEXT ACTION (when the janitor publishes the bootstrap + fixed global skills,
AND the MANAGER sequences chief-of-staff):**
1. Run **`/janitor-memory-bootstrap`** once → creates `.claude/project/memory/`
   (PROJECT scope) + the gitignore exception (`.claude/**` then
   `!.claude/project/` + `!.claude/project/memory/**`) + a starter
   architecture-hub page + `MEMORY.md`.
2. **Fold plugin-UNIQUE content** from the surfaces below into a NEW plugin
   `CLAUDE.md` FIRST (the plugin has no CLAUDE.md today), THEN remove the
   per-plugin memory surfaces:
   - delete `skills/cos-memory-recall/` (110 lines)
   - delete `skills/cos-memory-write/` (125 lines)
   - delete `rules/memory-protocol.md` (110 lines)
   - update the 5 referencing surfaces (grep-verified 2026-06-14):
     `agents/ai-maestro-chief-of-staff-main-agent.md`,
     `skills/amcos-failure-notification/references/edge-case-protocols.md`,
     `skills/amcos-skill-management/references/skill-reindexing.md`,
     `README.md`, `ai-maestro-chief-of-staff.agent.toml` — repoint to the
     global `janitor-memory-{recall,write,update}` skills.
3. **Adopt the PROACTIVE CONTRACT** in `agents/ai-maestro-chief-of-staff-main-agent.md`
   AND **propagate it into all 10 sub-agent prompts** (sub-agents inherit
   nothing): recall-before-acting · write/update-after-solving ·
   maintain-the-project-wikimem · scope-routing (private→LOCAL,
   project-shared→PROJECT, cross-project→USER; unsure→LOCAL).
4. Use the **FIXED zsh-portable array recall form** wherever recall is documented:
   ```bash
   ROOTS=(); for d in "$LOCAL_MEM" "$PROJECT_MEM" "$USER_MEM"; do [ -d "$d" ] && ROOTS+=("$d"); done
   memgrep recall "$SYMPTOM" "${ROOTS[@]}"
   ```
   (the old space-joined `ROOTS="$ROOTS $d"` + unquoted `$ROOTS` returns 0
   results SILENTLY on zsh/macOS — janitor fix commit df2e563.)
5. Tests + CPV strict green; publish a minor; report the version on #18.

**SUPERSEDED — do NOT carry forward:** the v2.15.0 stance that AMCOS KEEPS
`cos-memory-recall`/`write` as the compliant replacement. The updated spec
removes them in favor of the global janitor-hosted skills.

## The 3 scopes (final, per #18 + assistant-manager#15)

| Scope | Folder | Git |
|---|---|---|
| LOCAL | `~/.claude/projects/<slug>/memory/` | machine-private (harness `# Memory` path — unchanged) |
| PROJECT | `<repo>/.claude/project/memory/` | tracked + PUSHED (gitignore exception) |
| USER/global | `${CLAUDE_PLUGIN_DATA}/memory/` (janitor plugin-data) | one canonical cross-project corpus |

## Acceptance criteria
Zero per-plugin memory skills/rule remain; PROJECT scope bootstrapped; proactive
contract in main agent + all sub-agents; fixed recall form everywhere; published;
#18 answered with the version.
