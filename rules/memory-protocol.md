# Memory protocol — recall before acting, write what you learned (CHIEF-OF-STAFF)

The AI-Maestro markdown memory system for the CHIEF-OF-STAFF (AMCOS) role.
It is **{ tool · rule · skills }**: the `memgrep` recall engine (optional,
degrades to plain `grep`), this rule (the protocol), and the two skills
`cos-memory-recall` (search) and `cos-memory-write` (capture). It recalls
**curated, symptom-indexed markdown notes** in the project's `memory/` dir —
NOT conversation/transcript history.

This file is the COS-parameterised mirror of the canonical
`markdown-memory-recall` rule (`~/.claude/rules/markdown-memory-recall.md`
when installed user-side; reference implementation in `ai-maestro-janitor`).

## The one law: index by the QUESTION, not the answer

A memory is found from the SYMPTOM, not the solution. When you write a note,
its `description:` MUST carry the words a future session will have when the
problem RECURS — the user's words, the error text, the symptom — NOT the
jargon of the fix.

- WRONG `description`: "OAuth creds live in the macOS keychain services".
  (Findable only if you already know the answer is "keychain".)
- RIGHT `description`: "rotator failed, had to log in manually — where are
  the creds / why did the swap fail" + the keychain fact in the BODY.

Two-hop recall: a symptom query lands on the note; the note's BODY gives the
answer. `memgrep recall` ranks on `description + title + tags` ONLY. Put
symptom vocabulary in `description`; put the answer in the body.

## Recall BEFORE acting (when the COS must recall)

Run `cos-memory-recall` BEFORE:

- **routing or prioritising team work** — has this team hit this class of
  task/blocker before? what did we decide?
- **classifying a proposal's approval tier** — was an equivalent proposal
  already tiered / approved / refused?
- **debugging a recurring agent failure** (heartbeat loss, spawn failure,
  handoff corruption) — the fix is often already written down,
- **acting on a recurring alert** — same alert last week? read the note
  before re-deriving the diagnosis.

```bash
MEMDIR="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"
[ -d "$MEMDIR" ] || MEMDIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/memory"
SYMPTOM="the user's words / the error / the symptom"   # NOT the answer's jargon

if command -v memgrep >/dev/null 2>&1; then
  memgrep recall "$SYMPTOM" "$MEMDIR"      # notes ranked best-first: path — description
else
  grep -rliE "$SYMPTOM" "$MEMDIR" 2>/dev/null   # fallback: degrade, never break
fi
```

Read the top 1-3 notes; the answer is in their bodies. If recall returns
nothing, the memory doesn't exist yet — solve the problem, then capture it
with `cos-memory-write`.

`memgrep` is a Rust binary (source: `ai-maestro-janitor/tools/memgrep`;
install once with `cargo install --path <checkout>/tools/memgrep`). Until it
is installed the plain-`grep` fallback works on note frontmatter + bodies —
recall degrades, never breaks. Never block on the missing binary.

## Write AFTER learning (when the COS must write)

Run `cos-memory-write` after:

- resolving a **non-trivial team-coordination gotcha** (relay deadlock, AMP
  edge case, approval-flow surprise),
- a **failed-then-solved recovery** (what actually un-stuck the agent),
- learning a **durable constraint about a team agent or the project** that is
  not derivable from code or git history,
- a **confirmed user/MANAGER preference** on how the team should operate.

Note schema (one fact per note, `"$MEMDIR/<type>_<slug>.md"`):

```yaml
---
name: <type>_<slug>                # type ∈ user | feedback | project | reference
description: "<the SYMPTOM in the user's / the error's words — what a future session will search with>"
metadata:
  node_type: memory
  type: <user|feedback|project|reference>
---
<the one fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
Link related notes with [[their-name]].>
```

Then append one index line to `"$MEMDIR/MEMORY.md"`:
`- [<Title>](<type>_<slug>.md) — <one-line hook>.`

Before saving, recall first — update an existing note rather than duplicate.

## Correcting a memory — 2-step, non-destructive

When a new discovery CONTRADICTS an existing note:

1. **Clean the fact in place** — the body is the current truth; no
   "we used to think X" clutter inline.
2. **Demote the error to a lesson** — a numbered `[^N]` footnote under
   `## Notes and lessons learned` at the bottom of the page, carrying the
   WHY (root cause), with a `[ocd:… lmd:…]` date prefix. The fact is
   corrected; the error is never deleted — it becomes the guardrail.

## Does NOT apply to

- Conversation/transcript search (different corpus).
- The repo's own records (code structure, git history, CLAUDE.md, TRDDs) —
  never duplicate those into memory notes.
- Session-scoped facts that only matter to the current conversation.
