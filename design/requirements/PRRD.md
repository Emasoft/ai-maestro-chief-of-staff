---
prrd-version: 1.1
updated: 2026-06-11T19:56:28+0200
project: ai-maestro-chief-of-staff
project-id: ai-maestro-chief-of-staff
canonical-source: design/requirements/PRRD.md
mirrors: []
---

# Project Requirements & Rules — ai-maestro-chief-of-staff

CHIEF-OF-STAFF role plugin (AMCOS) — team gateway, AMP routing, proposal relay.

## §0. Canonical source + copies

| Path | Role | Update strategy |
|---|---|---|
| `design/requirements/PRRD.md` | **CANONICAL** for this project | Edit first. Bump `prrd-version:`. Update `updated:`. |

## §I. How to read this document

Rule citation form: `PRRD G<n>.<v>` (golden, user-set) or `PRRD S<n>.<v>`
(silver, manager-mutable). Rule numbers are globally unique across G/S;
promote/demote flips the letter without changing the number. The
`get-prrd.py <n>` script returns a rule's text by bare number. Full
spec: `~/.claude/rules/prrd-design-rules.md`.

## 🥇 GOLDEN — set by the USER (immutable to MANAGER)

> **Provenance log — why a GOLDEN rule's text changed without a new USER decision.**
> A golden rule is USER-only, so any edit here needs its authority visible.
>
> - **2026-08-08 — G1.1 byline SYNCED to canon (not a new decision).** The line shipped a literal
>   `@`-handle in bare prose; an agent copying the template verbatim into an issue PAGES the real
>   account. This edit does **not** decide anything: it brings a stale copy into line with a
>   decision the USER already made — the IRON rule of **2026-08-02** ("templates carry no `@` at
>   all", which cites this very byline as its worked example) and its ratification in the fleet
>   canon of **2026-08-05**, where `R22.2` reads `(via the shared <owner> gh auth)` — *"carries NO
>   `@`, deliberately"* — with its authority column marked **Explicit (USER)**. Verified at
>   `ai-maestro@governance-rules` tip `0be8cf32` in BOTH `docs/GOVERNANCE-RULES.md` and
>   `design/specs/governance-spec.md`, read directly rather than relayed.
>   **Backticking is NOT the fix** and was not applied: a template is copied OUT of its code span,
>   so only removing the character helps. Reported by the fleet R22/R23 check (10/10 population).
>   If the owner reads this as a new decision rather than a sync, revert it — one token, one line.

- **G1.1** — Every agent that writes to GitHub (issue, issue comment, PR, PR comment, PR review, discussion, release note) MUST begin the body with a one-line self-identification of which agent/role/plugin authored it, because all AI Maestro agents share the single human-owner GitHub identity (the owner's gh CLI auth). Recommended leading line: _Posted by the Claude developing **<plugin-or-role>** (via the shared &lt;owner&gt; gh auth)._ — the template **carries NO `@`, deliberately**: a byline is copied OUT of its code span into a real comment, where an `@` linkifies and PAGES a live account, so backticks protect it where it sits and not where it is used. Naming the owner in plain words self-identifies exactly as well; the `@` only adds a notification. Commit messages SHOULD carry an `Agent: <role>` trailer.

## 🥈 SILVER — MANAGER-mutable (agents propose via COS)

- **S2.1** — Spawn-approval timeout. COS waits 60 min (normal-priority) / 10 min (urgent-priority) for MANAGER approval on a non-exempt spawn or governance request before escalating per the autonomous-fallback chain. It never spin-waits.
- **S3.1** — Max coordinated team size is 12 active members; beyond that COS proposes a sub-team split to MANAGER rather than coordinating a larger team directly.
- **S4.1** — Escalation batch window. COS batches NORMAL-priority escalations to MANAGER on a 15-minute window to protect MANAGER tokens; URGENT and HIGH escalations bypass the batch and are forwarded immediately.
- **S5.1** — Proposal-queue drain cadence. COS surfaces the team's open `design/proposals/` queue to MANAGER at least once per idle sweep (janitor-heartbeat cadence) and reports approvals back to the proposing agent the same chain.
- **S6.1** — Single-writer-per-domain. Every mutable surface under `design/` (a TRDD file, the PRRD, a proposal) has exactly one owning session; a task needing a domain it does not own delegates to the owner or takes an explicit claim before writing — derived NPT/EHT tasks follow the same rule to avoid collisions.
- **S7.1** — The three in-team dialog loops — task-comprehension handshake, in-dev issue dialog, pre-PR gate — are ORCHESTRATOR-owned and run on DIRECT ORCH↔ARCH/MEMBER/INT edges; COS guards the TEAM BOUNDARY only (R6 v3) and never relays or absorbs these in-team exchanges.
