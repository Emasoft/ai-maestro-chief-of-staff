# ai-maestro-chief-of-staff — plugin guidance

## Memory: the janitor-hosted global 3-scope wiki

This plugin uses the **global** AI-Maestro markdown memory system — not a
per-plugin one. The protocol, the recall law ("index by the QUESTION, not the
answer"), the note schema, the 2-step non-destructive correction protocol, and
the three scopes all live in `~/.claude/rules/markdown-memory-recall.md`. The
operations are the global skills: `janitor-memory-recall` (find by symptom),
`janitor-memory-write` (capture a fact), `janitor-memory-update` (revise). The
PROJECT scope for this repo is `.claude/project/memory/` (git-tracked,
stood up once via `/janitor-memory-bootstrap`).

Do **NOT** re-create per-plugin `*-memory-recall` / `*-memory-write` skills or a
`rules/memory-protocol.md` mirror — those were removed in favor of the global
system (TRDD-59581001). The agent prompts (the main agent + every sub-agent)
carry the proactive-use contract directly, since sub-agents inherit nothing.

Use the FIXED zsh-portable array form when composing a multi-scope recall (the
old space-joined `$ROOTS` string silently returns 0 hits on zsh/macOS):

```bash
ROOTS=(); for d in "$LOCAL_MEM" "$PROJECT_MEM" "$USER_MEM"; do [ -d "$d" ] && ROOTS+=("$d"); done
memgrep recall "$SYMPTOM" "${ROOTS[@]}"
```

### COS-specific recall/write moments (the role flavoring)

Beyond the generic "recall before acting / write after solving" contract, the
CHIEF-OF-STAFF recalls and writes at these role-specific moments:

**Recall (`/janitor-memory-recall`) BEFORE:**
- routing or prioritising team work — has this team hit this class of
  task/blocker before? what did we decide?
- classifying a proposal's approval tier — was an equivalent proposal already
  tiered / approved / refused?
- debugging a recurring agent failure (heartbeat loss, spawn failure, handoff
  corruption) — the fix is often already written down;
- acting on a recurring alert — same alert last week? read the note first.

**Write (`/janitor-memory-write`) / update (`/janitor-memory-update`) AFTER:**
- resolving a non-trivial team-coordination gotcha (relay deadlock, AMP edge
  case, approval-flow surprise);
- a failed-then-solved recovery (what actually un-stuck the agent);
- learning a durable constraint about a team agent or the project not derivable
  from code/git history;
- a confirmed user/MANAGER preference on how the team should operate.

**Scope routing:** machine-private (paths, hostnames, secrets) → LOCAL
(`~/.claude/projects/<slug>/memory/`); project-shared, no secrets → PROJECT
(`.claude/project/memory/`); cross-project → USER; **UNSURE → LOCAL**.
