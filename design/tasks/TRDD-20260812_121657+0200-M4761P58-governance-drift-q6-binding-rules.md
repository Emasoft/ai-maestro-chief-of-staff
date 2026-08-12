---
trdd-id: M4761P58
title: Audit the persona against the Q6 binding-rules list and close the remaining drift
column: dev
created: 2026-08-12T12:16:57+0200
updated: 2026-08-12T12:41:47+0200
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

**DONE (this pass) — all four read at source, classified, stated, guarded.**

| Rule | Source (tip `7b5e02ca`) | Verdict | Stated as |
|---|---|---|---|
| `R52` | `design/specs/governance-spec.md:1915-1945` | **BINDS** — at runtime COS is one of *"the running server and its agents"* | new `## The Write Boundary — Two Roots`, incl. the reads-unrestricted asymmetry and the enforcement's own stated blind spot |
| `R42.7` | `design/specs/governance-spec.md:1729-1746` | **BINDS as a PROHIBITION** — the power is infrastructure's (*"never an agent, never a title, holding no AID"*); (f) makes *asking* the violation | new `### R42.7 is NOT yours`, placed adjacent to R42.8 on purpose |
| `R39.10` | `design/specs/governance-spec.md:1625-1633` | **BINDS conditionally** — COS may be the assigned collaborator; it is the ONLY door through an ASSISTANT's R39.7 invisibility | new bullet under `### Restrictions`, with all four surviving limits |
| checklist-gated terminal columns | **`.claude/rules/aimaestro-trdd-approval.md:801-824`** — NOT in the governance spec | **BINDS** — COS moves cards | new `### Terminal columns are checklist-gated` |

**The fourth item was not where Q6's grouping implied.** Q6 lists it under "overlay
layer", and it is overlay-only — `grep` for `checklist` across the whole 184KB
governance spec returns one unrelated hit (`R21.21`, a PR audit checklist). It lives in the
**trdd-approval** overlay, not the kanban one. Worth recording because **neither overlay is
installed on this machine** (`find ~/.claude/rules -name 'aimaestro-*.md'` → empty): they are
server-installed into *registered agent workdirs*, and this is a plugin-development session.
So a rule that governs this repo's board is one that is structurally invisible from it.

**Do NOT write any of them from the Q6 summary line.** That line is an index, not the rule;
R42.8's eight constraints are invisible in it, and three of them are the ones that make the
capability safe. Confirmed again here: the R42.7 clause that actually binds a COS — that
*asking* is itself the violation — appears nowhere in the summary line.

**Guards (4 new, suite 309 → 313).** Each falsified by IN-MEMORY substitution, seed verified
to have applied first. **One came back VACUOUS on its first falsification** — the
checklist-gate guard, for the very defect it guards: `≥1 box` appears twice in the section
(once in the rule, once in the prose explaining the rule), so deleting the rule left the
rationale's copy and `"≥1 box" in section` stayed GREEN. Same shape as the R42.8
`"assistant" in section` case. The assertion is now anchored to rule position
(`checklist exists (≥1 box)`). **Writing a rationale beside a rule makes the rule harder to
guard** — the words are present either way, so only position distinguishes them.

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

## Derived finding — this repo's own board fails the rule this card just read

Applying the checklist gate to this repo (the rule binds transitions **from 2026-07-31 on**;
cards terminal before that are grandfathered and FROZEN): **9 of 10** cards in a terminal
column fail it, and **all ten transitioned 2026-08-11** — inside the governed window, so
none is grandfathered. Eight are `published` with no checklist at all; `562b49e3` is
`published` with **5 boxes, all unchecked** — including a box reading *"Published
(v2.19.0)"*, work that demonstrably shipped. Only `NB725X9W` passes.

Not repaired here, and deliberately not by a sweep. The rule's stated remedy (move back to
`dev` and flag) would, applied blindly to eight cards whose work actually shipped, make the
board assert something *more* false than the missing checklist does; and retro-ticking the
boxes fabricates the verification record the checklist was supposed to BE. Split out as
**TRDD-Q7BZ8N3M** for a per-card judgment — the "never mass-repair a stalled board with a
script" discipline applies exactly here.

## Acceptance criteria

- [x] Each of `R52`, `R42.7`, `R39.10`, checklist-gated terminal columns: read at the
      normative source, classified binds-COS / does-not, decision recorded here with the
      line reference.
- [x] Every rule classified as binding is stated in the persona **with its operative limits**,
      not merely named.
- [x] Each addition guarded at constraint level, falsified by in-memory substitution
      (no disk edit — no stale `.pyc`, no crash window), with the seed verified to have
      actually applied before trusting a GREEN.
- [x] Suite green (313), ruff clean, published.

## Notes

- Sibling: `ai-maestro#131` (the transport thread) is CONVERGED and is not this card.
- Q4 of the same mirror: no rule existing only on the `governance-rules` branch is enforced
  against an agent that read `main` (MANAGER's fairness stance, endorsed by the server).
  That does not excuse this card — I have now read the branch.
