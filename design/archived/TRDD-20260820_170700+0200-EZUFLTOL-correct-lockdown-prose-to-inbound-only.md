---
trdd-id: EZUFLTOL
title: Correct the harness-lockdown prose to inbound-only after R42.9 was amended
column: complete
created: 2026-08-20T17:07:00+0200
updated: 2026-08-20T17:07:00+0200
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
min-approval-requirement: none
release-via: none
supersedes: P4OB78ST
external-refs: ["hub correction 2026-08-20 (USER directive)", "R42.9 amended — catalog 5.5.0, spec 2.6.0"]
---

# Correct the harness-lockdown prose to inbound-only after R42.9 was amended

TRDD-P4OB78ST (complete, archived, 524b921) refreshed seven persona passages to state that
a registered agent workdir carries `permissions.deny: ["SendMessage"]` — an OUTBOUND deny.
Hours later the hub relayed a USER-directed correction: R42.9 was amended (catalog 5.5.0,
spec 2.6.0). The lockdown is **INBOUND-ONLY** (`crossSessionInbound: "refuse"`); an outbound
`permissions.deny` entry is FORBIDDEN because it breaks subagent handling, and the server
invariant now REMOVES it from every agent workdir. Subagent SendMessage stays permitted.

**Verified first-hand before editing** (not taken on the peer's word): `~/agents/frank/`
`.claude/settings.local.json` carries `"deny": []` — empty — alongside
`"crossSessionInbound": "refuse"`.

P4OB78ST is terminal and frozen, so this is a new card rather than a re-open.

## Task

Rewrite the seven passages so each states the inbound-only truth, and restore the
"nothing refuses your outbound send" warnings that P4OB78ST had softened — they were
correct all along for the outbound direction.

## Acceptance criteria

- [x] Zero surviving claims that a workdir denies outbound `SendMessage`; each passage
      names `crossSessionInbound: "refuse"` and the outbound-deny prohibition instead.
- [x] The subagent/fork sections state that NO workdir setting backstops the `tools:`
      allowlist, since subagent SendMessage is deliberately permitted.
- [x] Suite green, ruff clean, trddgrep validate exit 0.

## Notes and lessons learned

The same passage went stale twice in one day, in opposite directions. The durable lesson is
not about this rule's content: **a persona that describes the ENFORCEMENT MECHANISM of a
neighbouring system inherits that system's release cadence.** The R6 obligations
("forbidden just the same") never moved; only the sentences claiming what refuses you did.
Prose that states the rule and cites the mechanism only as a dated aside survives a
mechanism change; prose that leans on the mechanism has to be rewritten every time it moves.

## Approval log

- 2026-08-20T17:07:00+0200 — COMPLETED (Tier-0 docs). Supersedes P4OB78ST's factual claims;
  that card stays archived as the record of the intermediate state.
