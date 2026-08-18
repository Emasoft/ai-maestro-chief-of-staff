---
trdd-id: DAESKVN9
title: Phase 1 self-audit of this plugin across the four mandated axes
column: dev
scope: project
project-id: ai-maestro-chief-of-staff
created: 2026-08-16T16:59:25+0200
updated: 2026-08-16T16:59:25+0200
current-owner: ai-maestro-chief-of-staff
created-by: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: audit
mandate: true
mandated-by: user
min-approval-requirement: none
relevant-rules: [1]
release-via: none
npt: []
eht: []
blocked-by: []
external-refs: [ai-maestro TRDD-BRRJK57P]
---

# Phase 1 self-audit of this plugin across the four mandated axes

Phase 1 of the USER fleet program `TRDD-BRRJK57P` (`/Users/emanuelesabetta/ai-maestro/design/tasks/`),
relayed by the hub session. The mandate was read at its source rather than taken from the relay:
`mandate: true`, `mandated-by: user`, `approved: true`, `approval-judge: user`. A read-only audit of
this repo is Tier 0 in this repo's own scope, so nothing here waits on the authority question that
stalled the orchestrator's five cards today.

**Discovery only. Nothing is fixed in this phase** — a fix during discovery destroys the evidence
Phase 2's plan is built from.

## The four axes

1. **MISSING FEATURES** — capability this plugin's README/skills/persona PROMISE that the tree does
   not deliver.
2. **GOVERNANCE COMPLIANCE** — the 3 pillars, the R-rules this plugin claims to implement, the
   ratified GitHub baseline rulesets, the authorship self-ID convention. A citation naming real code
   is not proof the rule is ENFORCED; the rule text has to be read against the guard.
3. **SCRIPTS ALIGNMENT** — for every script/CLI shipped or called: does the copy on PATH match the
   repo copy (`cmp`, never `grep`), are the advertised flags real (`--help`), does an unknown flag
   fail loudly instead of exiting 0.
4. **BUGS / ERRORS / CONFLICTS** — real defects, plus collisions with other plugins (same command
   name, same file, same settings key, contradictory rules).

## Verify twice — pass 2 must try to REFUTE pass 1

Pass 1 discovers with a `file:line` and the exact command. Pass 2 tries to prove each candidate
WRONG: re-run it, read around it, check whether the "missing" thing exists under another name, in
another file, or by another mechanism. **Default to REFUTED when uncertain.** Refuted candidates are
reported with their refutation, never silently dropped — they are how the next auditor avoids
re-finding them.

**"Not verified" and "verified absent" are different tokens and must not collapse.** A worker
reporting "0 found, not fully verified" is evidence the WORKER STOPPED, never evidence the thing is
absent.

**Code and git settle STATUS; prose only states INTENT.** `implementation-commits:` → `git show
<sha>` → does the artifact exist on disk. A STATE block is written once and rarely refreshed, which
makes it the most confidently wrong field on a card.

## The COS-specific axis-4 surface

As chief-of-staff this repo owns the ROUTING surface, and a routing defect has a signature nobody
looks for: **a rule that is written down and not enforced produces a SUCCESS, not an error.** Look
for places where the comm graph, the R6 v3 single-entry-point rule, or the approval ladder is
contradicted by what a skill or persona actually instructs an agent to do. Cross-repo findings name
both sides; this repo does not edit the other side.

Today supplied a live instance to check the shape against: three plugin-development sessions
(this one, the assistant-manager, the orchestrator) routed a category-Z approval request along R6
v3 to each other. Every hop succeeded. None of the three held an AID or a USER delegation, so the
chain resolved to nobody and the request travelled while standing still. The rule is correct; it
describes registered agents, and nothing in it fails when the participants are not.

## Acceptance criteria

- [ ] All four axes audited, each with a pass-1 discover and a pass-2 falsify.
- [ ] Every CONFIRMED finding carries `file:line` plus the exact command that produced it, and at
      least one cited `file:line` per finding re-verified by me first-hand, not on a worker's word.
- [ ] Refuted candidates recorded one line each with the refutation.
- [ ] Report written under `reports/plugin-self-audit/`; per-axis confirmed/refuted counts returned
      to the hub WITHOUT pasting findings into the message.
- [ ] Nothing in this repo was fixed during the phase.

## Notes

- `reports/` is gitignored, so the report is evidence and does not enter git. The DECISIONS it leads
  to become Phase-2 TRDDs in this repo.
- Phase 2 works cards `todo → dispatch → dev → testing → ai_review → complete`. `human_review` is
  OUT under this program — the USER delegated that column to the hub.
