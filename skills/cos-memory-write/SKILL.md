---
name: cos-memory-write
description: Capture a durable fact as a markdown memory note recallable from the SYMPTOM. Use after resolving a coordination gotcha, a failed-then-solved recovery, learning a constraint not derivable from code, or when the user says "remember this", "save a memory", "capture this gotcha", "note that for next time". Writes a schema-valid note plus the MEMORY.md index line. Write-side counterpart of cos-memory-recall.
user-invocable: true
license: Apache-2.0
compatibility: Requires file system access to the project memory dir. memgrep optional (dedup check falls back to grep).
metadata:
  author: Emasoft
  version: 1.0.0
---

# COS memory-write

## Overview

Capture one durable fact as a memory note so a future session — which will
have the SYMPTOM, not the answer — can recall it. The load-bearing decision is
the `description`: it MUST carry the words the problem will present with (the
user's words, the error, the symptom), because recall ranks on `description`
(+ `title` + `tags`). Put the symptom in `description`; put the answer in the
body.

Only capture what is NON-OBVIOUS and reusable: coordination gotchas,
constraints not in the code, confirmed preferences, hard-won recovery facts.
Do NOT capture what the repo already records (code structure, git history,
CLAUDE.md, TRDDs) or what only matters to the current conversation.

## Instructions

1. Resolve the memory dir (same as recall):

   ```bash
   MEMDIR="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"
   [ -d "$MEMDIR" ] || MEMDIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/memory"
   mkdir -p "$MEMDIR"
   ```

2. Choose `type` ∈ `user | feedback | project | reference` and a kebab slug
   (prefix the slug with the type, e.g. `feedback_…`, `reference_…`).

3. Check for an existing note that already covers this (update it rather than
   duplicate):

   ```bash
   command -v memgrep >/dev/null 2>&1 \
     && memgrep recall "<symptom>" "$MEMDIR" \
     || grep -rliE "<symptom>" "$MEMDIR" 2>/dev/null
   ```

4. Write `"$MEMDIR/<type>_<slug>.md"` with the Write tool (NOT echo), schema:

   ```yaml
   ---
   name: <type>_<slug>
   description: "<the SYMPTOM in the user's / the error's words — the words a future session will search with, NOT the answer's jargon>"
   metadata:
     node_type: memory
     type: <user|feedback|project|reference>
   ---
   <the one fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
   Link related notes with [[their-name]].>
   ```

5. Append a one-line pointer to `"$MEMDIR/MEMORY.md"` (create if missing): a
   markdown list item linking the note — dash, then `[<Title>]` immediately
   followed by `(<type>_<slug>.md)`, then ` — <one-line hook>.`

6. Sanity-check: would a future session, having only the SYMPTOM, find this
   note by searching `description`? If the description reads like the
   *answer*, rewrite it to read like the *question*.

## Correcting a memory — the 2-step non-destructive protocol

When a new discovery CONTRADICTS an existing memory:

1. **Clean the fact in place.** Replace the wrong statement in the body with
   the correct one — the body is the current truth, no "we used to think X"
   clutter inline.
2. **Demote the error to a lesson.** Record the error as a numbered footnote
   (`[^N]` in the body, `[^N]: …` under `## Notes and lessons learned` at the
   bottom), with a `[ocd:<date> lmd:<date>]` prefix and the WHY — the root
   cause, not merely "this was wrong". A lesson without a WHY cannot stop the
   next repeat.

The fact is corrected; the error is never deleted — it is demoted to a linked
lesson so future readers don't repeat it.

## Output

One note file + one MEMORY.md index line. Report the note path and the
one-line description; do NOT echo the whole note back into the conversation.

## Examples

<example>
After fixing a relay deadlock between two team agents:
  description: "two agents waiting on each other's AMP reply / team stuck, no progress"
  body: the deadlock mechanism + the staggered-reply fix.
</example>

<example>
User: remember that MANAGER wants spawn requests batched, not one-per-message
  → type: feedback; description carries "how should I send spawn requests /
    one per message or batched"; body records the batching preference with
    **Why:** and **How to apply:**.
</example>

```text
User: remember this for next time
User: save a memory about the hibernation race
User: capture this gotcha
```

## Scope

ONLY authors/updates memory notes + the MEMORY.md index. Does NOT recall (use
`cos-memory-recall`). One fact per note. Symptom-indexed description is
mandatory — it is what makes the note recallable.

## Resources

- `${CLAUDE_PLUGIN_ROOT}/rules/memory-protocol.md` — the COS memory protocol
  (the law, schema, lessons-learned conventions).
- `cos-memory-recall` — the RECALL side (find a note before you duplicate or
  correct it).
