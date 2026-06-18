---
trdd-id: 562b49e3-0569-4b6c-9565-f4a085940601
title: Propagate governance R26-R40 into the COS persona, skills, docs + governance SCEN
column: dev
created: 2026-06-18T20:54:20+0200
updated: 2026-06-18T21:15:52+0200
current-owner: cos
assignee: cos
priority: 2
severity: HIGH
effort: L
labels: [governance, persona, security]
task-type: docs
parent-trdd: null
npt: []
eht: []
blocked-by: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
must-pass-tests-before-merge: true
publish-target: emasoft-claude-plugins
publish-channel: stable
test-requirements: [lint, governance-scenarios]
audit-requirements: [security-scan]
review-requirements: []
runtime-targets: [macos, linux]
impacts: []
attempts: 0
last-test-result: not-run
implementation-commits: []
external-refs: ["github.com/Emasoft/ai-maestro-chief-of-staff/issues/21", "github.com/Emasoft/ai-maestro/issues/37"]
---

# TRDD-562b49e3 — Propagate governance R26-R40 into the COS persona, skills, docs + governance SCEN

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-18

**What this is:** MANAGER work order COS#21 (Emasoft/ai-maestro-chief-of-staff#21). Internalize
governance rules **R26-R40** (GOVERNANCE-RULES.md **v4.0.2**, security-governance core landed v4.0.0)
into the COS plugin's OWN persona + skills + docs, add a `tests/scenarios/governance-scenarios.md`,
clean the CPV `--strict` gate, and publish via the canonical pipeline. Reference impl = the MANAGER's
own AMAMA plugin **ai-maestro-assistant-manager-agent v2.12.0**.

**Current state:**
- Canonical rules FETCHED → `reports_dev/governance/GOVERNANCE-RULES.md` (v4.0.2; R26-R40 bodies at 1211-1369).
- COS#21 ACKed (issuecomment-4745175907). TRDD authored + committed (3e822f8).
- **Phase 1 audit DONE** → `reports/governance/20260618_210115+0200-r26-r40-audit.md` (verbatim-verified;
  19 files w/ hits across 252 scanned; per-file `path:line` + suggested reversal). Dominant: R32 password
  (8 files), R29 "COS forms team" (9), R30/R31, R27 (2), R38/R39 (2 LOW); R26/R28 clean; R33-R40 = gaps to ADD.
- **STRATEGY CHANGE:** a 4-agent parallel edit swarm was launched but ALL died on fleet rate-limiting
  (API "temporarily limiting requests") — 1 correct partial edit landed, no other damage. Switched to
  doing the edits **MYSELF inline, serially** (transparent + rate-limit-resilient; right call for governance).
- **Edits progress (2/~20 files):** (1) `agents/amcos-approval-coordinator.md` — R32 fully reversed
  (c6f0218). (2) `agents/ai-maestro-chief-of-staff-main-agent.md` (the persona) — R29/R30/R31 reversals
  (MANAGER creates team+COS+5-base; mandate-gated; R31 FREEZE) + a new **R26-R40 governance section**
  (table) + residual `R12`→`R30` fix; verified clean; committed (029a6ea). The persona governance table
  is the canonical in-plugin summary the other files can point at.

**NEXT ACTION:** continue the inline edits, per the audit report's per-file guidance. Remaining files,
grouped: **R32** → skills/amcos-permission-management/SKILL.md + its 4 refs (governance-details-and-examples,
op-track-pending-approvals, op-request-approval, approval-workflow-engine), commands/amcos-request-approval.md,
docs/TEAM_REGISTRY_SPECIFICATION.md (also R29). **R29** → agents/ai-maestro-chief-of-staff-main-agent.md
(persona — also R30/R31), docs/AGENT_OPERATIONS.md, docs/FULL_PROJECT_WORKFLOW.md,
skills/amcos-agent-coordination/references/workflow-checklists.md,
skills/amcos-team-coordination/references/coordination-overview-and-examples.md,
skills/amcos-agent-spawning/references/workflow-examples.md. **R30/R31 + R33-R40 GAPS** → persona +
docs/ROLE_BOUNDARIES.md + README.md (add the 5-base invariant, the R31 FREEZE, and a new R26-R40
governance section incl. signed-ledger SOT / foreign-host MAESTRO approval / one-MAESTRO / MAESTRO-DELEGATE /
ASSISTANT model). **R27** → agents/amcos-plugin-configurator.md, commands/amcos-configure-plugins.md.
**R38/R39 LOW** → skills/amcos-onboarding/references/{role-briefing,onboarding-overview-and-examples}.md.
Commit per cluster (protect work vs rate-limit). Then: tests/scenarios/governance-scenarios.md → CPV --strict → publish v2.19.0.

**Load-bearing facts / gotchas:**
- Canonical source is GOVERNANCE-RULES.md v4.0.x R26-R40 — NOT ai-maestro#37 (that's R23/R24/R25,
  decoupling+memory+three-pillars; COS#21 conflated them).
- The R32 rule (agents NEVER sudo; AID+title+portfolio token IS the authz; sudo is USER-via-UI only)
  directly reinforces the still-open #25 `AIMAESTRO_GOV_PASSWORD` DECOUPLE-BLOCKED marker: COS must
  NEVER hold or perform the governance password — it surfaces it to the MAESTRO. Keep the two consistent.
- Bright-line OLD-model phrases to reverse (from COS#21): "COS assignment is USER-only",
  "MANAGER recommends COS", any agent using a sudo / governance password, any "incomplete team operates".
- publish is gated on CPV `--strict` clean (the plugin ships ZERO local validators — remote CPV only)
  + the plugin's own test runner. Pre-push hook permits only publish.py ancestry.
- Per RULE 0: commit before any destructive edit; stage files BY NAME (never `git add -A`).

**SUPERSEDED — do NOT carry forward:** (none yet)

**Durable artifacts to read before acting:**
- `reports_dev/governance/GOVERNANCE-RULES.md` (the fetched canonical rules; R26-R40 @ 1211-1369).
- COS#21 body (the work order + COS-specific emphasis) and its ACK.
- AMAMA reference impl: ai-maestro-assistant-manager-agent v2.12.0 (persona+skills+docs+governance-scenarios.md).

## The R26-R40 rules (authoritative summary; full bodies in the fetched file)

- **R26** Identity immutability — no agent self-changes TITLE/ROLE/NAME/AID; only USER(MAESTRO)/MANAGER/own-team-COS (NAME/AID only on compromise).
- **R27** Self-install only via core-plugin skills + MANAGER/COS approval + server CPV scan.
- **R28** Three-check API authz: AID id → TITLE privilege → portfolio approval/mandate token (server-side; never trust client-supplied id/title/scope).
- **R29** MANAGER team/agent lifecycle authority: creates/deletes teams (auto-creating COS + 5 base members) + AUTONOMOUS + MAINTAINER, no USER approval.
- **R30** COS needs a MANAGER mandate to create agents; the 5-member base is invariant; customization = extra MEMBER-titled agents (on the member-agent role-plugin) only.
- **R31** Incomplete-team freeze: a team missing any of its 5 base members is FROZEN (only COS active, others hibernated) until complete.
- **R32 (CRITICAL)** No agent sudo gates — AID+title+portfolio token IS the authz; sudo is requested ONLY of the USER, ONLY via the UI; SUPERSEDES the prior X-Sudo-Token-for-agents design.
- **R33** Signed-ledger recovery of agent auth on token loss.
- **R34 (CRITICAL)** The signed ledger is the ultimate SOT (valid AID with no ledger history = untrusted; imported agents re-issue an AID via USER sudo, ledger-recorded).
- **R35 (CRITICAL)** Foreign agent/user needs MAESTRO UI approval before its AID is accepted (ledger-recorded).
- **R36** Users have AIDs; exactly one MAESTRO per host; obey only the active MAESTRO.
- **R37 (CRITICAL)** MANAGER obeys only the MAESTRO; a single MAESTRO-DELEGATE at a time (original suspended; no two MAESTROs; delegate can't manage MAESTRO title/attrs/password, uses own sudo).
- **R38** Non-MAESTRO users can't change agents/teams; kanban+PR workflow; restricted messaging (own-team COS, MANAGER, users — v4.0.2: user↔user FORBIDDEN); subordinate to MANAGER/COS.
- **R39 (CRITICAL)** Users have no terminal → an auto-created ASSISTANT agent (ai-maestro-assistant-role-agent); no team; "Assistant of <user>"; obeys its user + MAESTRO; user may edit its panel except NAME/TITLE/ROLE/TEAM.
- **R40** Foreign-user creation needs MAESTRO approval per-op; MANAGER may restrict specific API commands to specific foreign users.

## Plan (phased; ≤5 files per phase, verify between phases)

1. **Audit** (read-only, delegable): grep the COS tree for the OLD-model bright-line phrases + any
   sudo/governance-password agent usage + COS-creation/assignment wording. Output: file:line hit list
   grouped by which R-rule governs the fix. Cross-check the existing persona's COS-creation/authority
   sections against R29/R30/R31.
2. **Persona edits** (`agents/*.md`, the main COS agent persona): reverse old-model statements; add an
   explicit R26-R40 governance section with the COS emphasis (created-by-MANAGER, mandate-gated agent
   creation, 5-base invariant + freeze, AID-not-sudo authz, R6-v3 sole gateway, obey active MAESTRO).
3. **Skills + docs edits**: same reversal in skills/ SKILL.md bodies + references, and docs/ (incl. any
   governance/authority reference docs, the team-registry spec, onboarding).
4. **Scenarios**: add `tests/scenarios/governance-scenarios.md` exercising the COS-relevant rules
   (R28/R29/R30/R31/R32/R36 at minimum) per the repo's SCENARIOS_TESTS_RULES conventions; mirror AMAMA.
5. **Verify + ship**: run the plugin's test runner; CPV `--strict` → clean (devitalize/fix, never
   suppress); bump to **v2.19.0** (MAJOR-ish governance change → minor bump is fine, persona/docs only);
   publish via publish.py; `gh run watch` CI; report on COS#21 + ai-maestro#37.

### Derived tasks / consequences to verify
- Keep #25 (`AIMAESTRO_GOV_PASSWORD`) consistent with R32 — the repoint, when it lands, must SURFACE the
  password to the MAESTRO, never have the COS perform sudo. Update the #25 marker note to cite R32.
- The COS-creation reversal (R29: MANAGER creates the COS) may contradict existing onboarding/dialog
  docs that describe USER-driven COS setup — audit ALL of them, not just the persona (the "grep the
  WHOLE plugin" lesson).
- Ensure no governance-scenario test opens external resources without teardown (browser/process/file).

## Acceptance criteria
- [ ] Persona + skills + docs internalize R26-R40 with the COS emphasis; all OLD-model statements reversed.
- [ ] `tests/scenarios/governance-scenarios.md` added (COS-relevant rules covered) + passes the runner.
- [ ] `grep` for the old bright-line phrases over the published tree returns zero.
- [ ] CPV `--strict` = 0/0/0/0; plugin test runner green; CI green.
- [ ] Published (v2.19.0); reported on COS#21 + ai-maestro#37 with the version + self-id line.
