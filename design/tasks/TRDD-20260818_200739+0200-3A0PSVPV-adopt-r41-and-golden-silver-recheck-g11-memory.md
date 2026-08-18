---
trdd-id: 3A0PSVPV
title: Adopt R41 approval-vs-mandate + PRRD golden-silver citations and re-check G1.1 templates + memory contract
column: todo
created: 2026-08-18T20:07:39+0200
updated: 2026-08-18T20:07:39+0200
current-owner: ai-maestro-chief-of-staff
assignee: ai-maestro-chief-of-staff
task-type: docs
scope: project
project-id: ai-maestro-chief-of-staff
mandate: true
mandated-by: manager
min-approval-requirement: 0
npt: []
eht: []
blocked-by: [MJ6X0LN0]
pre-block-column: todo
release-via: publish
external-refs: [ai-maestro-chief-of-staff#30, ai-maestro TRDD-BRRJK57P]
priority: 7
---

# Adopt R41 approval-vs-mandate + PRRD golden-silver citations; re-check G1.1 templates + memory contract

Fleet wave order COS#30 (AMAMA, Tier-2 under the recorded USER delegation in TRDD-BRRJK57P;
MANAGER-side card TRDD-9a16554d). Queued rather than worked inline: MJ6X0LN0's worker is editing
`agents/ai-maestro-chief-of-staff-main-agent.md` right now, and this order edits the same persona
— `blocked-by:` prevents the collision, clears when MJ6X0LN0 closes.

Adopt by CITATION, never restate:
1. **R41** (`docs/GOVERNANCE-RULES.md` v4.5.0+ on `governance-rules`; NOTE the v4.8.0 authority
   inversion — `design/specs/governance-spec.md` on the same ref is NORMATIVE, the catalog is its
   emanation): APPROVAL flows bottom-up, no agent approves a card it authored, an approval is
   CHECKABLE (verify, don't just read). MANDATE flows top-down, born approved.
2. **PRRD golden/silver authority split** cited as `PRRD G/S<number>.<version>`.

Re-check on the LIVE tree (not the installed cache):
- (A) G1.1 in skill TEMPLATES — every GitHub-posting template models the self-ID first line in
  its concrete examples; no bare @-handle anywhere (backtick handle-looking tokens).
  Prior evidence: Phase-1 axis-2 section E verified all 5 posting call sites clean on 2026-08-16;
  re-verify rather than cite, per the order.
- (B) memory recall-before-acting / write-after-solving — this repo uses the CONTRACT form
  (CLAUDE.md + persona carry it, covering sub-agents); verify it still covers all skills.

## Acceptance criteria

- [ ] Persona/decision surface cites R41 (approval vs mandate, no self-approval, checkable
      approvals) and the golden/silver split — by number, no restatement.
- [ ] Pattern A verified or fixed on the live tree, with the sweep command recorded.
- [ ] Pattern B verified or fixed on the live tree.
- [ ] Result reported on COS#30 (verified-clean is a valid result), with the COS byline, no `@`.
- [ ] Suite green, ruff clean.
