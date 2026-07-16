---
trdd-id: 4FH9JP4U
title: R42 drive-vs-lifecycle audit — categorized purge plan (execution-gated on R42 text)
column: blocked
created: 2026-07-16T20:32:10+0200
updated: 2026-07-16T20:32:10+0200
current-owner: cos-ai-maestro-chief-of-staff
task-type: audit
release-via: publish
test-requirements: [unit]
relevant-rules: []
min-approval-requirement: none
---

# TRDD-4FH9JP4U — R42 drive-vs-lifecycle audit + purge plan

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-16

- **What this is:** the PLAN half of task #42 (R42 "no agent may drive another"). Authored
  after the MANAGER, on ai-maestro#72 (2026-07-16T17:24:25Z), confirmed R42 has **no readable
  rule body** (governance-rules stuck at v4.2.0; R42–R49 unpushed) but **explicitly invited
  planning** against the CODIFIED anchors R9 / R10.3 / R17 / R29 / R30.
- **VERDICT: the #42 purge is NEAR-EMPTY.** The R42 revocation target — steering a *running*
  session (send-command, hard process-restart-to-control, stop-to-boss) — **does not exist**
  anywhere in the COS surface (`send-command`=0, `steer`=0, `boss`=0 hits; `drive`/`stop the`
  are all governance-column / AMP-messaging / analytics, never session-steering). COS "restart"
  is **already DEFINED as a hibernate+wake lifecycle cycle** (see EVIDENCE), which R10.3
  preserves by name. So there is essentially nothing to remove.
- **NEXT ACTION (gated — do NOT execute yet):** when R42's actual text becomes readable
  (unblocks with the hub's `git push origin governance-rules`, ai-maestro#71), re-read R42, then
  apply the small REPHRASE hygiene list below ONLY if R42 draws the line where the MANAGER's
  interim reading puts it. Until then: parked.
- **BLOCKED-BY (external):** R42 rule text not codified on readable `governance-rules`
  (ai-maestro#71 / #72). pre-block-column: backburner.
- **SUPERSEDED — do NOT carry forward:** the earlier assumption (from the R41–R48 briefing) that
  #42 would be a large multi-file "purge of drive semantics." It is not — the MANAGER retracted
  the over-cited R42 paraphrase, and the audit shows the surface was already R42-clean.

## Context

Task #42 was opened to purge "COS drives its team agents" semantics down to configure + message.
R42 ("IRON: no agent may drive another") was cited as the authority. On ai-maestro#72 the MANAGER
verified the readable governance ref and found **R42 has zero rule body** — every "R42" is
changelog prose, not a rule — and told COS to keep #42 parked for EXECUTION but PLAN it now
against the rules that DO have readable bodies on v4.2.0.

## The codified rubric (MANAGER, ai-maestro#72, verbatim mapping)

| Category | Codified anchor | Disposition |
|---|---|---|
| own-team **wake / hibernate** | **R10.3** — "the CHIEF-OF-STAFF can wake or hibernate agents that belong to their own team only" | **KEEP** (preserved by name) |
| **spawn / terminate** own-team member | R29 (MANAGER lifecycle authority) + R30 (COS customization = extra MEMBER agents, under a MANAGER mandate) | **KEEP** (under mandate) |
| **recovery** of a hung/crashed own-team agent | R9 / R17 (own-team recovery); wake reloads config per R17.21 | **KEEP** — MANAGER: "`amcos-recovery-execution` Strategy 2/3 survives" |
| config change → takes effect via **hibernate→wake** (not hard restart) | R10.3 + R17.21 (`wakeAgent` reloads plugin/config on wake) | **KEEP / REPHRASE** to the lifecycle framing |
| **runtime-steer a running session** — send-command, hard process-restart-to-control, stop-to-boss | the only ops a future R42 can revoke | **REMOVE-CANDIDATE** |

## Audit result (COS context surface: `agents/ skills/ commands/ docs/`, 243 md files)

### REMOVE — runtime-steering a running session: **NONE FOUND**
- `send-command` / `send_command` = 0 hits. `steer` = 0. `boss ` = 0.
- `drive` (8) = all governance-column-transition (kanban loop driver, ORCHESTRATOR/AMOA drives
  the working transitions), AMP reminder cadence, or "data-driven" analytics. None steer a session.
- `stop the` (1) = `amcos-permission-management/references/rule-14-enforcement.md:30` "STOP the
  current task" — the READER's own AMP-priority preemption, not stopping another agent.

### KEEP-CODIFIED — lifecycle & recovery (R9/R10.3/R17/R29/R30)
- **COS "restart" is already a hibernate+wake cycle by definition** (EVIDENCE below) → R10.3 lifecycle.
- `amcos-recovery-execution/` + `amcos-failure-detection/` "Strategy: Restart Agent" for
  "Hung or crashed agent" → R9/R17 recovery (no live session to steer). KEEP.
- `agents/ai-maestro-chief-of-staff-main-agent.md:189` "Wake / hibernate / restart a member
  already in the approved R30 team" → wake/hibernate KEEP (R10.3); "restart" = the lifecycle cycle.
- `amcos-agent-termination/.../success-criteria.md:212` "if active but not responding, consider
  restarting" → recovery. KEEP.
- op-wake-agent.md:184 (many skills) "not responding after wake → restart" → recovery-after-wake. KEEP.

### REPHRASE (optional hygiene, execution-gated) — make the lifecycle framing explicit
Low-priority cosmetic edits; none is a removal. Apply only after R42's text confirms the line:
- `skills/amcos-plugin-management/references/op-restart-agent-plugin.md` ("Restart Agent After
  Plugin Changes") + `op-install-plugin-remote.md:122,125` — annotate that this restart IS the
  hibernate→wake cycle (cite R17.21 wakeAgent-reloads-config), matching the spawning skill's
  own definition, so no reader mistakes it for a process-kill-to-steer.
- `agents/…main-agent.md:189` — annotate "restart" = the hibernate+wake lifecycle op (not steering).

### EVIDENCE — COS "restart" ≡ hibernate+wake (the load-bearing finding)
- `skills/amcos-agent-spawning/references/cli-reference.md:228` — "restart an agent. This performs
  a **hibernate-wake cycle**, which is required after plugin or marketplace changes."
- `…/cli-reference.md:140` — "Each plugin operation automatically restarts the target agent
  (**hibernate + wake**)."
- `…/cli-reference.md:62` + `cli-examples.md:128` — "Restart agent | **Hibernate + wake cycle**".
- `…/cli-reference.md:239` — "You cannot restart the current agent" (no self-steering either).

## Why the purge is near-empty (bug-autopsy of the over-cite)

The R41–R48 briefing framed #42 as a large purge because "R42" was cited as settled law. It is not
codified. But independently, the COS surface never adopted runtime-steering vocabulary in the first
place — it always expressed control as lifecycle (spawn/hibernate/wake/recovery) and coordination
as AMP messaging. So the surface was R42-compliant before R42 existed. The lesson: audit the actual
surface against CODIFIED rules before scoping a "purge" from a changelog paraphrase.

## Execution gate

- **Do NOT execute** the REPHRASE list until R42's authoritative text is readable on
  `governance-rules` (ai-maestro#71 push). If R42 draws the drive/configure line exactly where the
  MANAGER's interim reading puts it (own-team wake/hibernate/recovery preserved; runtime-steering
  revoked), execution is the small REPHRASE list above — cosmetic, one patch release.
- If R42 draws the line somewhere unexpected, re-run this audit against its real text before editing.

## Source artefacts
- MANAGER R42 answer: ai-maestro#72 comment 2026-07-16T17:24:25Z.
- MANAGER push-blocker finding: ai-maestro#71 comment 2026-07-16T17:24:54Z.
