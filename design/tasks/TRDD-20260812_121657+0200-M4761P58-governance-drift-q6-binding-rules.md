---
trdd-id: M4761P58
title: Audit the persona against the Q6 binding-rules list and close the remaining drift
column: dev
created: 2026-08-12T12:16:57+0200
updated: 2026-08-12T12:16:57+0200
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
min-approval-requirement: none
relevant-rules: [1]
---

# Audit the persona against the Q6 binding-rules list and close the remaining drift

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-12

**Origin.** `ai-maestro#76` carries a consolidated eleven-ruling mirror from the server
Claude, posted **2026-08-07T22:35Z**. It went **unread for five days** because my inbound
sweep used a hand-typed watermark instead of deriving one — see the *Monitoring* note below,
which is the more important half of this card.

**Q6 verbatim** — *"Binding COS: R39.x + R39.10 (4.6.0–4.7.1, 5.3.2), authority inversion
(4.8.0), R52 write boundary (5.1.0), R42.7 (5.2.0), R42.8 (5.3.0/5.3.1); overlay layer:
min-approval-requirement supersedes approval-tier, mandate fields, checklist-gated terminal
columns, mandatory assignee, scope discriminators."*

**DONE (v2.28.0).**
- `R42.8` — full section + all eight constraints, written from the normative text, guarded
  at constraint level. This was the serious one: I hold that capability and the persona
  named it zero times.
- `assignee:` — added to the 2 open cards that lacked it.
- `approval-tier` → `min-approval-requirement` — **verified NOT applicable**; the 5 hits are
  rule-DOCUMENT filenames, not the superseded frontmatter field, which this repo never used.
  `min-approval-requirement` already on 3/3 cards. Do not "fix" these.

**NEXT ACTION (resume here).** For each of `R52` (write boundary), `R42.7`,
`R39.10`, and *checklist-gated terminal columns*: read the rule at the NORMATIVE source,
decide whether it binds **COS as an agent** (persona-worthy) or is server-side//other-title,
and only then edit. All four are currently absent from `agents/ skills/ docs/`.

**Do NOT write any of them from the Q6 summary line.** That line is an index, not the rule;
R42.8's eight constraints are invisible in it, and three of them are the ones that make the
capability safe.

**Normative source, pasted not composed:** `Emasoft/ai-maestro`, branch `governance-rules`,
tip `7b5e02ca`, file `design/specs/governance-spec.md` (NORMATIVE per the 4.8.0 authority
inversion; `docs/GOVERNANCE-RULES.md` is PROVENANCE and loses where they differ). Fetched
`2026-08-12T11:49:04+0200`. The tip MOVES — re-resolve and re-label before citing.

**COST GATE (why this card exists rather than the work continuing inline).** The spec is
**184,167 bytes**. Pulling it into the main context is what produced a `[token-anomaly]`
flag — ~1.27M weighted tokens in 5 minutes, 21.4× the session median, at $121.94/h
machine-wide. It re-bills on every later turn. On resume, extract ONLY the rule's own lines
(`grep -n` then a bounded `sed` range) and never read the whole file again.

## Monitoring — the defect that caused this, already fixed in habit but not in code

The sweep must derive its watermark from **my own last comment via the API**, never a typed
constant:

```bash
gh issue view <N> --repo Emasoft/ai-maestro --json comments | jq -r '
  ([.comments[] | select(.body | contains("Agent: ai-maestro-chief-of-staff")) | .createdAt]
    | last // "1970-01-01T00:00:00Z") as $w
  | [.comments[] | select(.createdAt > $w)] | length'
```

Two properties worth keeping: it cannot develop a blind window, and it self-clears only when
I actually reply — an item I have read but not answered stays flagged, which is correct.

**Note `gh --jq` does NOT accept `--arg`.** The first version of this pipeline used it and
returned an EMPTY string, which read as "nothing unread" — a vacuous zero, the same class of
defect as everything else in this family. Pipe to `jq` proper.

## Acceptance criteria

- [ ] Each of `R52`, `R42.7`, `R39.10`, checklist-gated terminal columns: read at the
      normative source, classified binds-COS / does-not, decision recorded here with the
      line reference.
- [ ] Every rule classified as binding is stated in the persona **with its operative limits**,
      not merely named.
- [ ] Each addition guarded at constraint level, falsified by in-memory substitution
      (no disk edit — no stale `.pyc`, no crash window), with the seed verified to have
      actually applied before trusting a GREEN.
- [ ] Suite green, ruff clean, published.

## Notes

- Sibling: `ai-maestro#131` (the transport thread) is CONVERGED and is not this card.
- Q4 of the same mirror: no rule existing only on the `governance-rules` branch is enforced
  against an agent that read `main` (MANAGER's fairness stance, endorsed by the server).
  That does not excuse this card — I have now read the branch.
