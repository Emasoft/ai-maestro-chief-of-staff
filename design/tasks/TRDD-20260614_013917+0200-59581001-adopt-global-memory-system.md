---
trdd-id: 59581001-4f47-470e-9f16-746ce5194962
title: Adopt the janitor-hosted global 3-scope memory system; remove per-plugin memory skills
column: backburner
created: 2026-06-14T01:39:17+0200
updated: 2026-06-14T01:39:17+0200
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

**⛔ BLOCKED — do NOT execute yet.** The rollout "rides the janitor's next
publish, when the global skills ship fixed." VERIFIED 2026-06-14: the janitor's
updated memory work (the `/janitor-memory-bootstrap` skill + the zsh-array-fixed
`janitor-memory-{recall,write,update}` skills) is **committed but
unpushed/unpublished** (per MANAGER #15) — `/janitor-memory-bootstrap` is NOT in
the installed janitor cache (only the prior `janitor-memory-recall/write/update`
are). Executing now = capability gap + jumping the MANAGER's sequence. The fixed
`~/.claude/rules/markdown-memory-recall.md` rule IS already auto-installed.

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
