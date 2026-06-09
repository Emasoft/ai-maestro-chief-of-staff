---
name: cos-memory-recall
description: Recall durable project memories from a SYMPTOM before routing team work, classifying an approval tier, debugging a recurring failure, or acting on a recurring alert. Searches the markdown memory notes with memgrep (grep fallback) and returns the top notes. Use when you think "have we hit this before?", or the user says "recall memories about X", "did we already solve this". Read-only counterpart of cos-memory-write.
user-invocable: true
license: Apache-2.0
compatibility: Requires file system access to the project memory dir. memgrep optional (falls back to grep).
metadata:
  author: Emasoft
  version: 1.0.0
---

# COS memory-recall

## Overview

Recall is the FIRST step before routing/prioritising team work, classifying a
proposal's approval tier, debugging a recurring agent failure, or acting on a
recurring alert — "have we hit this before?". It searches the project's curated
markdown memory notes (the `memory/` dir) and returns the notes whose
`description`/`title`/`tags` best match your SYMPTOM. The answer is in the
matched note's body.

This is distinct from conversation/transcript search: it recalls *curated,
symptom-indexed notes*, not raw chat history.

## The one law

Query with the SYMPTOM — the user's words, the error text, the problem — NOT
the answer's jargon. A note is findable from the symptom because its author put
symptom vocabulary in `description`. (Query "rotator failed, had to log in" —
not "keychain" — to find the credentials note from the problem.)

## Instructions

1. Resolve the project memory dir (the harness per-project notes dir):

   ```bash
   MEMDIR="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')/memory"
   # If that path doesn't exist, fall back to a project-local memory/ dir:
   [ -d "$MEMDIR" ] || MEMDIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/memory"
   ```

2. Build a SYMPTOM query from the user's words / the error / the problem
   (never the answer's jargon), then recall — memgrep if present, plain grep
   otherwise:

   ```bash
   SYMPTOM="the symptom in the user's / the error's words"
   if command -v memgrep >/dev/null 2>&1; then
     memgrep recall "$SYMPTOM" "$MEMDIR"        # notes ranked best-first: path — description
   else
     grep -rliE "$SYMPTOM" "$MEMDIR" 2>/dev/null # fallback: degrade, never break
   fi
   ```

   If `memgrep` is not installed, the grep fallback works on note frontmatter
   + bodies. (memgrep lives in `ai-maestro-janitor/tools/memgrep`; install
   once with `cargo install --path <checkout>/tools/memgrep`.)

3. Read the top 1-3 notes the recall returns; the fact you need is in their
   bodies (each note's `[^N]` lessons-learned come back appended by default —
   read those too). If recall returns nothing, the memory doesn't exist yet —
   solve the problem, then capture it with `cos-memory-write`.

## Enriched recall (memgrep present)

- `memgrep recall "$SYMPTOM" "$MEMDIR" --sort lmd` — newest-modified first.
- `memgrep recall "$SYMPTOM" "$MEMDIR" --since 2026-06-01` — recent notes only.
- `memgrep find "+term -excluded" "$MEMDIR"` — note-level keyword search
  (`+` mandatory, `-` exclude, `*` wildcard, quoted phrases).
- `memgrep find "+term" "$MEMDIR" --only-notes` — search only the
  lessons-learned footnotes.

## Output

A short ranked list of `path — description` lines (memgrep) or matching paths
(grep fallback), best first. Read the top few; do NOT dump full note bodies
into the conversation — open the one you need.

## Examples

<example>
User: the spawn request for the test-runner failed again with a timeout
→ recall "spawn request failed timeout" → surfaces the spawn-retry note;
  read it WHOLE (fact + lessons) before re-deriving the diagnosis.
</example>

<example>
User: did we already decide how to prioritize refactor proposals from MEMBERs?
→ recall "prioritize refactor proposals from members" → surfaces the
  routing-decision note; apply the recorded decision instead of re-deciding.
</example>

```text
User: recall what we learned about heartbeat loss during hibernation
User: have we seen this handoff corruption before?
User: check the memory notes about approval-tier classification
```

## Scope

ONLY searches + surfaces existing memory notes (read-only). Does NOT write
notes (use `cos-memory-write`). Degrades to plain grep when memgrep is absent;
never blocks on a missing binary.

## Resources

- `${CLAUDE_PLUGIN_ROOT}/rules/memory-protocol.md` — the COS memory protocol
  (the law, the schema, recall/write moments, the correction protocol).
- `cos-memory-write` — the WRITE side (authoring + the correction protocol).
