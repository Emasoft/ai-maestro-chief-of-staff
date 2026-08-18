---
trdd-id: 4FH9JP4U
title: R42 drive-vs-lifecycle audit — categorized purge plan (execution-gated on R42 text)
column: complete
created: 2026-07-16T20:32:10+0200
updated: 2026-08-18T23:52:00+0200
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
- **UNBLOCKED 2026-07-16T~19:32 (ai-maestro#72):** `git push origin governance-rules` landed;
  R42 is now readable — `GOVERNANCE-RULES.md` v4.5.0 L1510: **"No Agent May Drive Another Agent —
  Messaging Is the ONLY Channel"** (CRITICAL/IRON/USER-set). MANAGER confirmed my finding and said
  EXECUTE. R42's literal sets: **REVOKED** = injecting a command/keystroke/prompt/queued-input into
  ANOTHER agent's session (routes `POST …/[id]/{panel,queue,prompt/answer}`, `PATCH …/[id]/session`,
  `POST /api/sessions/[id]/{stop,restart}`; TRDD-BF3JN4TL). **PRESERVED** = hibernate/wake own-team
  (R10.3), spawn/terminate (R29/R30) — governed by R10, NOT R42; self-drive (R42.4);
  **R42.6 "Configuring is NOT driving"** (local skills/subagents/MCP/hooks + TEAM/TITLE).
- **VERDICT (corrected by THE CHECK): the config/lifecycle surface IS R42-clean, BUT the RECOVERY
  path is NOT — a real repoint, not the earlier "2-spot rephrase".** THE CHECK the MANAGER asked
  for (grep recovery for revoked routes) SURPRISED us: no direct `/api/sessions/*/restart` calls in
  scripts (task #23 migrated those), but the recovery SKILL PROSE instructs R42-revoked
  session-injection — tmux keystroke inject (`examples.md:30,38` "Send restart command via tmux
  session (exit and relaunch Claude Code)") and "send a soft/hard restart signal to the agent"
  (`op-execute-recovery-strategy.md:57,64`; `recovery-operations.md:228,291`), duplicated across
  BOTH `amcos-recovery-execution` and `amcos-failure-detection` (files DIFFER). Strategy 4
  (Hibernate-Wake) and the message-based "graceful restart request" are already R42-compliant.
- **FIX TAXONOMY (grounded in R42's sets):** soft restart → **MESSAGE the agent to self-restart**
  (R42.2 directive-as-message + R42.4 self-drive); hard restart → **hibernate→wake cycle** (R10.3
  own-team; wake reloads config per R17.21) — a server lifecycle-STATE op, NEVER the revoked
  `sessions/[id]/restart` route or a tmux keystroke; then terminate+respawn (R29/R30) / op-replace.
  Caveat (R42 rationale, HONEST LIMIT): R42 is tamper-EVIDENT not tamper-PROOF (tmux unfenced) —
  **do NOT describe R42 as a sandbox** in any rephrase.
- **EXECUTION COMPLETE 2026-07-16T~21:5x — 21 surface files repointed, verified clean, 195 tests green.**
  MANAGER approved cells 1/2/HONEST-LIMIT on ai-maestro#72 (19:45:35Z); cell 3 (terminate+respawn)
  confirmed delete+create via `op-replace-agent.md` (line 38 "no memory of the old agent") and gated
  — it ALREADY requires MANAGER approval (Phase 2), made explicit at every reference. The initial
  recovery-scoped grep UNDER-scoped: the tmux/kill/restart boilerplate was duplicated across
  `amcos-{recovery-execution,failure-detection,emergency-handoff,agent-replacement}` examples,
  `op-wake-agent.md` ×4, `op-install-plugin-remote`, `op-restart-agent-plugin`, `cli-reference`, and
  the `amcos-recovery-workflow`/`amcos-wake-agent` commands — a repo-wide re-grep (with a
  never/NOT/R42/read-only filter) found and cleared ALL of them. Worst finding: a raw
  `tmux list-panes … | kill -TERM $PID` in recovery-operations.md §4.1 (COS process-killing a peer) —
  removed. **NEXT ACTION:** publish (deferred to a deliberate release — bundles with `fa385e0`/`a0f3ed2`).
  Verify on resume: `grep -rlniE '<injection pattern>' … | filter` returns empty; `uv run pytest tests/` green.

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

## Acceptance checklist (written 2026-08-18 against that day's re-run — see Approval log)

- [x] No R42-revoked injection-INSTRUCTION prose remains in skills/ — re-run 2026-08-18T23:50:51:
      `grep -rniE '^[^|]*((Send|send) (a )?(soft|hard) restart signal|Send restart command via tmux)' skills/`
      → exit 1 (no match). What remains is prose PROHIBITING injection, in 4 skills.
- [x] No raw `kill -TERM` of a peer in skills/ or scripts/ — re-run 2026-08-18T23:50:51:
      `grep -rn "kill -TERM" skills/ scripts/` → exit 1 (no match).
- [x] Test suite green — re-run 2026-08-18T23:50:51: `uv run --with pytest pytest tests/` →
      341 passed (299 at original close; the suite grew, none red).

## Approval log

- 2026-08-11T19:54:10+0200 — COMPLETED. Closing a card whose work finished on
  2026-07-16 and which then sat at `column: dev` for 26 days claiming active
  work. Its only outstanding item was `NEXT ACTION: publish (deferred to a
  deliberate release)`; 46 `v2.*` releases have shipped since, most recently
  v2.25.1, so the deferral resolved itself long ago and nobody closed the card.
  Verified against this card's OWN acceptance check rather than its self-report,
  because a card asserting "EXECUTION COMPLETE" is a claim, not evidence:
  the R42 injection-prose grep returns empty, the raw `kill -TERM $PID` of a
  peer is gone from `recovery-operations.md`, and 299 tests pass. Not archived
  as a guess — the three checks are what closed it.
- 2026-08-18T23:50:51+0200 — REOPENED → dev, per the checklist gate's remedy: the 2026-08-11
  close was a POST-boundary terminal transition with no checklist (the vacuous case the
  "≥1 box" clause exists for; Q7BZ8N3M disposition, commit f15f1df). Audit finding
  TRDD-BRRJK57P axis 2, repair card TRDD-4HSTGXGB.
- 2026-08-18T23:52:00+0200 — RE-COMPLETED. The three closing checks were RE-RUN today (commands
  and exits in the checklist above) and the checklist written and ticked against that re-run —
  not against the 2026-08-11 prose. Work content unchanged; only the verification record the
  gate requires was added.
