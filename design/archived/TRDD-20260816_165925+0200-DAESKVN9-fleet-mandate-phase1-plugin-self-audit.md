---
trdd-id: DAESKVN9
title: Phase 1 self-audit of this plugin across the four mandated axes
column: complete
scope: project
project-id: ai-maestro-chief-of-staff
created: 2026-08-16T16:59:25+0200
updated: 2026-08-19T04:33:25+0200
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

- [x] All four axes audited with discover+falsify passes → 4 reports in
      `reports/plugin-self-audit/` (2026-08-16), final counts 14 CONFIRMED / 25 REFUTED /
      2 NOT-VERIFIED after the hub's re-verification and my corrections.
- [x] Citations with commands; at least one per finding re-verified first-hand (incl. catching
      the hub's own `--role` over-claim and withdrawing my two null-payload citations).
- [x] Refuted candidates recorded with refutations in each axis report.
- [x] Counts + report paths sent to the hub (2026-08-16 23:27, ledgered; hub re-verified one
      citation per axis).
- [x] Nothing fixed during the phase — every remediation landed AFTER the Phase-2 GO
      (BRRJK57P Approval log 2026-08-18T19:53:29+0200), as commits e3a3518..f8040f9.

## Approval log

- 2026-08-19T04:33:25+0200 — COMPLETED. Phase 1 delivered 2026-08-16; card held open through
  Phase 2 as the findings' anchor. All 14 CONFIRMED findings now remediated (6 Phase-2 cards,
  all complete+archived) plus the goal-driven follow-ons (trddgrep adoption 3b70ff1, R41
  adoption ab0a5a6, INTEGRATOR ownership c63a9e6). Scenario-blocker analysis written:
  reports/plugin-self-audit/20260819_043500+0200-usage-scenario-blockers.md (7 scenarios,
  2 blockers compound on ai-maestro#76/#2 — sent to the hub as asks).

## Notes

- `reports/` is gitignored, so the report is evidence and does not enter git. The DECISIONS it leads
  to become Phase-2 TRDDs in this repo.
- Phase 2 works cards `todo → dispatch → dev → testing → ai_review → complete`. `human_review` is
  OUT under this program — the USER delegated that column to the hub.
